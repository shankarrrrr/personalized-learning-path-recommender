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
