from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, ForeignKey
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
    domain = Column(String)
    skills_taught = Column(JSON, default=list)
    prerequisites = Column(JSON, default=list)
    level = Column(String)
    format = Column(String)
    duration = Column(String)
    embedding_vector = Column(JSON, nullable=True) # Will store list of floats if used locally

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
