from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class LearnerProfileBase(BaseModel):
    goal: Optional[str] = None
    domain: Optional[str] = None
    current_level: Optional[str] = None
    known_skills: List[str] = []
    interests: List[str] = []
    time_budget: Optional[str] = None
    preferred_format: Optional[str] = None

class LearnerProfileCreate(LearnerProfileBase):
    pass

class LearnerProfile(LearnerProfileBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class ChatMessage(BaseModel):
    role: str
    content: str

class OnboardRequest(BaseModel):
    messages: List[ChatMessage]
    profile_id: Optional[int] = None

class OnboardResponse(BaseModel):
    message: ChatMessage
    profile: LearnerProfile
    is_complete: bool

class PathGenerateRequest(BaseModel):
    learner_id: int

class NodeInfo(BaseModel):
    skill_id: str
    course_id: str
    status: str
    milestone_id: str

class LearningPathResponse(BaseModel):
    id: int
    learner_id: int
    ordered_nodes: List[Dict[str, Any]]
    generated_at: datetime
    
    class Config:
        orm_mode = True

class ProgressUpdateRequest(BaseModel):
    learner_id: int
    course_id: str
    status: str # 'done', 'skipped'

class CareerPathBase(BaseModel):
    title: str
    description: str
    domain: str
    avg_salary_min: Optional[int] = None
    avg_salary_max: Optional[int] = None
    job_growth: Optional[str] = None
    demand_level: Optional[str] = None
    required_skills: List[str] = []
    optional_skills: List[str] = []
    estimated_time_months: Optional[int] = None
    difficulty_level: Optional[str] = None
    typical_job_titles: List[str] = []
    industries: List[str] = []
    remote_friendly: Optional[str] = "Yes"
    learning_objectives: List[str] = []
    career_progression: List[str] = []

class CareerPathCreate(CareerPathBase):
    id: str

class CareerPath(CareerPathBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class CareerPathFilter(BaseModel):
    domain: Optional[str] = None
    difficulty_level: Optional[str] = None
    min_salary: Optional[int] = None
    max_salary: Optional[int] = None
    max_time_months: Optional[int] = None
    remote_friendly: Optional[bool] = None
