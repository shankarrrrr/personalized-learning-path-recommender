from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models, schemas, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="AI Learning Path Recommender")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow frontend to access
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
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
    # This will be wired up to ai_service to chat and extract profile
    # For now, returning a mock response
    return {
        "message": {"role": "assistant", "content": "Tell me more about your goals!"},
        "profile": {
            "id": 1,
            "goal": "Learn Python",
            "created_at": "2026-08-27T00:00:00Z"
        },
        "is_complete": False
    }

@app.get("/profile/{profile_id}", response_model=schemas.LearnerProfile)
def get_profile(profile_id: int, db: Session = Depends(get_db)):
    profile = db.query(models.LearnerProfile).filter(models.LearnerProfile.id == profile_id).first()
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@app.post("/path/generate", response_model=schemas.LearningPathResponse)
def generate_path(request: schemas.PathGenerateRequest, db: Session = Depends(get_db)):
    # Wire up to graph_service to generate path
    return {
        "id": 1,
        "learner_id": request.learner_id,
        "ordered_nodes": [],
        "generated_at": "2026-08-27T00:00:00Z"
    }
