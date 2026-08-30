from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship
import datetime
from database import Base

class LearnerProfile(Base):
    __tablename__ = "learner_profiles"

    id = Column(Integer, primary_key=True, index=True)
    goal = Column(String, nullable=True)
    domain = Column(String, nullable=True)
    current_level = Column(String, nullable=True)
    known_skills = Column(JSON, default=list) # List of skills
    interests = Column(JSON, default=list)
    time_budget = Column(String, nullable=True)
    preferred_format = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    learning_paths = relationship("LearningPath", back_populates="learner")

class Course(Base):
    __tablename__ = "courses"

    id = Column(String, primary_key=True, index=True) # string IDs from seed data
    title = Column(String, index=True)
    description = Column(Text)
    domain = Column(String, index=True)  # indexed for domain filtering
    skills_taught = Column(JSON, default=list)
    prerequisites = Column(JSON, default=list)
    level = Column(String, index=True)  # indexed for level filtering
    format = Column(String)
    duration = Column(String)
    embedding_vector = Column(JSON, nullable=True) # Will store list of floats if used locally

    # Real-course metadata (TASK-006)
    platform = Column(String, nullable=True)        # e.g. Coursera, Udemy, freeCodeCamp, YouTube
    course_url = Column(String, nullable=True)      # canonical link to the course
    instructor = Column(String, nullable=True)       # author / channel / university
    rating = Column(Float, nullable=True)            # 0.0 - 5.0
    rating_count = Column(Integer, nullable=True)   # number of ratings
    price = Column(String, nullable=True)            # 'Free', '$49.99', 'Subscription', etc.
    is_free = Column(Boolean, default=True)          # convenience boolean for filtering
    language = Column(String, default="English")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class LearningPath(Base):
    __tablename__ = "learning_paths"

    id = Column(Integer, primary_key=True, index=True)
    learner_id = Column(Integer, ForeignKey("learner_profiles.id"))
    ordered_nodes = Column(JSON, default=list) # list of dicts: skill_id, course_id, status, milestone_id
    generated_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    learner = relationship("LearnerProfile", back_populates="learning_paths")

class ProgressLog(Base):
    __tablename__ = "progress_logs"

    id = Column(Integer, primary_key=True, index=True)
    learner_id = Column(Integer, ForeignKey("learner_profiles.id"))
    course_id = Column(String, ForeignKey("courses.id"))
    status = Column(String) # locked, in_progress, done, skipped
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    optional_score = Column(Integer, nullable=True)

class CareerPath(Base):
    __tablename__ = "career_paths"

    id = Column(String, primary_key=True, index=True)  # e.g., "data_scientist"
    title = Column(String, index=True)  # e.g., "Data Scientist"
    description = Column(Text)  # Career overview and what they do
    domain = Column(String)  # e.g., "Data Science", "Web Development"
    
    # Job market information
    avg_salary_min = Column(Integer)  # Minimum salary range
    avg_salary_max = Column(Integer)  # Maximum salary range
    job_growth = Column(String)  # e.g., "+22% (Much faster than average)"
    demand_level = Column(String)  # "High", "Medium", "Low"
    
    # Learning information  
    required_skills = Column(JSON, default=list)  # List of skill IDs needed
    optional_skills = Column(JSON, default=list)  # Nice-to-have skills
    estimated_time_months = Column(Integer)  # Time to complete learning path
    difficulty_level = Column(String)  # "Beginner", "Intermediate", "Advanced"
    
    # Additional metadata
    typical_job_titles = Column(JSON, default=list)  # Related job titles
    industries = Column(JSON, default=list)  # Industries that hire for this role
    remote_friendly = Column(String, default="Yes")  # Remote work availability
    
    # Learning path information
    learning_objectives = Column(JSON, default=list)  # What you'll learn
    career_progression = Column(JSON, default=list)  # Career advancement path
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
