from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = ""
    status: Optional[str] = "todo"
    priority: Optional[str] = "medium"
    project_id: Optional[int] = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    project_id: Optional[int] = None


class TaskOut(TaskBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = ""


class ProjectOut(ProjectCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
