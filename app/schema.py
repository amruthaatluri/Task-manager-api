from datetime import date, datetime
from pydantic import BaseModel, Field
from typing import Optional, Literal
StatusLiteral= Literal["todo", "done", "in_progress"]
class TaskBase(BaseModel):
    title: str= Field(..., max_length=200)
    description: Optional[str]= None
    status: StatusLiteral= 'todo'
    due_date: Optional[date]= None
class TaskCreate(TaskBase):
    pass
class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    status: Optional[StatusLiteral] = None
    due_date: Optional[date] = None
class TaskOut(BaseModel):
    id: int
    title: str = Field(..., max_length=200)
    description: Optional[str] = None
    status: StatusLiteral = "todo"
    due_date: Optional[date] = None
    created_at: datetime
    updated_at: datetime

class config():
    from_attributes= True
