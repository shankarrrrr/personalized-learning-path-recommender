from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import copy
import models, schemas, database
from services.ai_service import ai_service
from services.graph_service import graph_service
from services.recommendation_service import recommendation_service
from typing import List, Optional

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="AI Learning Path Recommender")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "AI Learning Path API is running"}

@app.post("/onboard", response_model=schemas.OnboardResponse)
def onboard(request: schemas.OnboardRequest, db: Session = Depends(get_db)):
    history = [{"role": msg.role, "content": msg.content} for msg in request.messages]
    result = ai_service.extract_profile(history)
    
    profile_data = result.get("profile", {})
    
    if request.profile_id:
        profile = db.query(models.LearnerProfile).filter(models.LearnerProfile.id == request.profile_id).first()
        if profile:
            for k, v in profile_data.items():
                if v is not None:
                    setattr(profile, k, v)
        else:
            profile = models.LearnerProfile(**profile_data)
            db.add(profile)
    else:
        profile = models.LearnerProfile(**profile_data)
        db.add(profile)
        
    db.commit()
    db.refresh(profile)
    
    return {
        "message": result.get("message", {"role": "assistant", "content": "Tell me more!"}),
        "profile": profile,
        "career_suggestions": result.get("career_suggestions", result.get("suggested_careers", [])),
        "is_complete": result.get("is_complete", False)
    }

@app.get("/profile/{profile_id}", response_model=schemas.LearnerProfile)
def get_profile(profile_id: int, db: Session = Depends(get_db)):
    profile = db.query(models.LearnerProfile).filter(models.LearnerProfile.id == profile_id).first()
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@app.post("/path/generate", response_model=schemas.LearningPathResponse)
def generate_path(request: schemas.PathGenerateRequest, db: Session = Depends(get_db)):
    profile = db.query(models.LearnerProfile).filter(models.LearnerProfile.id == request.learner_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
        
    goal_skills = profile.interests if profile.interests else ["machine_learning"]
    known_skills = profile.known_skills or []
    
    # 1. WHAT to learn
    sorted_skills = graph_service.compute_skill_gap(goal_skills, known_skills)
    
    ordered_nodes = []
    for skill_id in sorted_skills:
        # 2. WHICH resource to use (Vector search retrieval)
        course = recommendation_service.retrieve_best_course(skill_id, db, profile)
        course_id = course.id if course else f"course_for_{skill_id}"
        ordered_nodes.append({
            "skill_id": skill_id,
            "course_id": course_id,
            "status": "locked",
            "milestone_id": "m1"
        })
        
    if ordered_nodes:
        ordered_nodes[0]["status"] = "current"
        
    learning_path = models.LearningPath(
        learner_id=profile.id,
        ordered_nodes=ordered_nodes
    )
    db.add(learning_path)
    db.commit()
    db.refresh(learning_path)
    
    return learning_path

@app.post("/progress/update")
def update_progress(request: schemas.ProgressUpdateRequest, db: Session = Depends(get_db)):
    path = db.query(models.LearningPath).filter(models.LearningPath.learner_id == request.learner_id).order_by(models.LearningPath.id.desc()).first()
    if not path:
        raise HTTPException(status_code=404, detail="Path not found")
        
    profile = db.query(models.LearnerProfile).filter(models.LearnerProfile.id == request.learner_id).first()

    # Deep copy to ensure SQLAlchemy detects the mutation on the JSON column
    nodes = copy.deepcopy(path.ordered_nodes)
    updated = False
    
    target_idx = -1
    for i, node in enumerate(nodes):
        if node["course_id"] == request.course_id:
            target_idx = i
            break
            
    if target_idx != -1:
        if request.status == "completed":
            nodes[target_idx]["status"] = "completed"
            
            # Add to known skills (deep copy to force SQLAlchemy detection)
            skill_id = nodes[target_idx]["skill_id"]
            known = copy.deepcopy(profile.known_skills or [])
            if skill_id not in known:
                known.append(skill_id)
                profile.known_skills = known
                
            # Unlock next
            if target_idx + 1 < len(nodes):
                nodes[target_idx + 1]["status"] = "current"
            updated = True
            
        elif request.status == "skipped":
            skill_id = nodes[target_idx]["skill_id"]
            exclude_ids = [n["course_id"] for n in nodes]
            alt_course = recommendation_service.retrieve_best_course(skill_id, db, profile, exclude_course_ids=exclude_ids)
            
            if alt_course:
                nodes[target_idx]["course_id"] = alt_course.id
                nodes[target_idx]["status"] = "current"
            else:
                nodes[target_idx]["status"] = "skipped"
                if target_idx + 1 < len(nodes):
                    nodes[target_idx + 1]["status"] = "current"
            updated = True
                
    if updated:
        # Reassign the whole list so SQLAlchemy marks it dirty
        path.ordered_nodes = nodes
        db.commit()
        db.refresh(path)
        db.refresh(profile)
        
    return path

@app.get("/careers", response_model=List[schemas.CareerPath])
def get_careers(
    domain: Optional[str] = Query(None, description="Filter by domain (e.g., 'Data Science', 'Web Development')"),
    difficulty_level: Optional[str] = Query(None, description="Filter by difficulty ('Beginner', 'Intermediate', 'Advanced')"),
    min_salary: Optional[int] = Query(None, description="Minimum salary filter"),
    max_salary: Optional[int] = Query(None, description="Maximum salary filter"),
    max_time_months: Optional[int] = Query(None, description="Maximum learning time in months"),
    remote_friendly: Optional[bool] = Query(None, description="Filter by remote work availability"),
    db: Session = Depends(get_db)
):
    """
    Get all career paths with optional filtering.
    
    - **domain**: Filter by career domain
    - **difficulty_level**: Filter by learning difficulty
    - **min_salary**: Minimum salary threshold
    - **max_salary**: Maximum salary threshold  
    - **max_time_months**: Maximum learning time
    - **remote_friendly**: Whether remote work is available
    """
    query = db.query(models.CareerPath)
    
    # Apply filters
    if domain:
        query = query.filter(models.CareerPath.domain == domain)
    
    if difficulty_level:
        query = query.filter(models.CareerPath.difficulty_level == difficulty_level)
        
    if min_salary:
        query = query.filter(models.CareerPath.avg_salary_max >= min_salary)
        
    if max_salary:
        query = query.filter(models.CareerPath.avg_salary_min <= max_salary)
        
    if max_time_months:
        query = query.filter(models.CareerPath.estimated_time_months <= max_time_months)
        
    if remote_friendly is not None:
        if remote_friendly:
            query = query.filter(models.CareerPath.remote_friendly.in_(["Yes", "Partial"]))
        else:
            query = query.filter(models.CareerPath.remote_friendly == "No")
    
    careers = query.all()
    return careers

@app.get("/careers/{career_id}", response_model=schemas.CareerPath)
def get_career_by_id(career_id: str, db: Session = Depends(get_db)):
    """Get a specific career path by ID."""
    career = db.query(models.CareerPath).filter(models.CareerPath.id == career_id).first()
    if career is None:
        raise HTTPException(status_code=404, detail="Career path not found")
    return career

@app.get("/careers/domains/list")
def get_career_domains(db: Session = Depends(get_db)):
    """Get all unique career domains."""
    domains = db.query(models.CareerPath.domain).distinct().all()
    return {"domains": [domain[0] for domain in domains]}

@app.get("/careers/stats/summary")
def get_career_stats(db: Session = Depends(get_db)):
    """Get summary statistics about available career paths."""
    careers = db.query(models.CareerPath).all()
    
    if not careers:
        return {"message": "No career paths found"}
    
    salaries = [(c.avg_salary_min, c.avg_salary_max) for c in careers if c.avg_salary_min and c.avg_salary_max]
    times = [c.estimated_time_months for c in careers if c.estimated_time_months]
    domains = list(set([c.domain for c in careers]))
    difficulty_levels = list(set([c.difficulty_level for c in careers]))
    
    return {
        "total_career_paths": len(careers),
        "domains": domains,
        "difficulty_levels": difficulty_levels,
        "salary_range": {
            "min": min([s[0] for s in salaries]) if salaries else None,
            "max": max([s[1] for s in salaries]) if salaries else None,
            "avg_min": sum([s[0] for s in salaries]) // len(salaries) if salaries else None,
            "avg_max": sum([s[1] for s in salaries]) // len(salaries) if salaries else None
        },
        "time_to_complete": {
            "min": min(times) if times else None,
            "max": max(times) if times else None,
            "avg": sum(times) // len(times) if times else None
        },
        "remote_friendly_count": len([c for c in careers if c.remote_friendly == "Yes"])
    }

@app.post("/careers/{career_id}/select")
def select_career_path(career_id: str, learner_id: int, db: Session = Depends(get_db)):
    """
    Select a career path for a learner and update their profile.
    This will set the learner's goal and interests based on the selected career.
    """
    # Get the career path
    career = db.query(models.CareerPath).filter(models.CareerPath.id == career_id).first()
    if not career:
        raise HTTPException(status_code=404, detail="Career path not found")
    
    # Get the learner profile
    profile = db.query(models.LearnerProfile).filter(models.LearnerProfile.id == learner_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Learner profile not found")
    
    # Update profile with career information
    profile.goal = career.title
    profile.domain = career.domain
    profile.interests = career.required_skills[:5]  # Take first 5 required skills as interests
    
    db.commit()
    db.refresh(profile)
    
    return {
        "message": f"Successfully selected career path: {career.title}",
        "career": career,
        "updated_profile": profile
    }
