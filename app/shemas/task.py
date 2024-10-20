from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    is_completed: bool = False
    priority: Optional[int] = 3
    deadline: Optional[datetime] = None
    assigned_user_id: Optional[int] = None  # ID пользователя, которому назначена задача

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    pass

class TaskInDB(TaskBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
