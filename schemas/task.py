from pydantic import BaseModel
from typing import Optional
from enum import Enum



class TaskStatus(str, Enum):
    todo = "To Do"
    in_progress = "In Progress"
    complete = "Completed"



class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None



class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None


class TaskOut(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: TaskStatus



class MessageResponse(BaseModel):
    message: str