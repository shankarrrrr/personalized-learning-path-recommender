from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class LearnerProfileBase(BaseModel):
    goal: Optional[str] = None
    domain: Optional[str] = None
    current_level: Optional[str] = None
    known_skills: List[str] = Field(default_factory=list)
    interests: List[str] = Field(default_factory=list)
    time_budget: Optional[str] = None
    preferred_format: Optional[str] = None

class LearnerProfileCreate(LearnerProfileBase):
    pass

class LearnerProfile(LearnerProfileBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime

class ChatMessage(BaseModel):
    role: str
    content: str

class OnboardRequest(BaseModel):
    messages: List[ChatMessage]
    profile_id: Optional[int] = None

class OnboardResponse(BaseModel):
    message: ChatMessage
    profile: LearnerProfile
    career_suggestions: Optional[List[Dict[str, Any]]] = []
    is_complete: bool

class PathGenerateRequest(BaseModel):
    learner_id: int

class NodeInfo(BaseModel):
    skill_id: str
    course_id: str
    status: str
    milestone_id: str

class LearningPathResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    learner_id: int
    ordered_nodes: List[Dict[str, Any]]
    generated_at: datetime

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
    required_skills: List[str] = Field(default_factory=list)
    optional_skills: List[str] = Field(default_factory=list)
    estimated_time_months: Optional[int] = None
    difficulty_level: Optional[str] = None
    typical_job_titles: List[str] = Field(default_factory=list)
    industries: List[str] = Field(default_factory=list)
    remote_friendly: Optional[str] = "Yes"
    learning_objectives: List[str] = Field(default_factory=list)
    career_progression: List[str] = Field(default_factory=list)

class CareerPathCreate(CareerPathBase):
    id: str

class CareerPath(CareerPathBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime
    updated_at: datetime

class CareerPathFilter(BaseModel):
    domain: Optional[str] = None
    difficulty_level: Optional[str] = None
    min_salary: Optional[int] = None
    max_salary: Optional[int] = None
    max_time_months: Optional[int] = None
    remote_friendly: Optional[bool] = None
