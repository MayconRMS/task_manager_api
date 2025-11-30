from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.task import Status

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[Status] = None

class TaskRead(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: Status
    created_at: datetime
    completed_at: Optional[datetime]

    class Config:
        from_attributes = True

