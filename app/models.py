from sqlalchemy import Column, Integer, String, Text, DateTime, Date, Enum, func
from .db import Base
import enum
class Status(str, enum.Enum):
    todo ="todo"
    in_progress="in_progress"
    done="done"
class Task(Base):
    __tablename__= 'tasks'
    id= Column( Integer, primary_key= True, index= True)
    title= Column(String(200), nullable=False, index= True)
    description= Column(Text, nullable= True)
    status = Column(Enum(Status), nullable=False, default=Status.todo, server_default=Status.todo.value)
    due_date= Column(Date, nullable= True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
