from fastapi import FastAPI, Depends, HTTPException
from typing import Literal, Optional
from sqlalchemy.orm import Session
from datetime import date
from .db import Base, engine, get_db
from . import models, schema

app = FastAPI(title="TASK MANAGER API", version="0.2.0")
@app.on_event("startup")
def on_startup():
	Base.metadata.create_all(bind=engine)

@app.get("/health",tags= ["meta"])
def health():
	return {"status": "ok"}
@app.post("/tasks", response_model=schema.TaskOut, tags=["tasks"])
def create_task(payload: schema.TaskCreate, db: Session= Depends(get_db)):
	task=models.Task(
		title=payload.title,
		description= payload.description,
		status= payload.status,
		due_date= payload.due_date
	)
	db.add(task)
	db.commit()
	db.refresh(task)
	return task
@app.get("/tasks", response_model=list[schema.TaskOut], tags=["tasks"])
def list_tasks(
    status: Optional[schema.StatusLiteral] = None,
    due_before: Optional[date] = None,
    due_after: Optional[date] = None,
    db: Session = Depends(get_db),
):
	q = db.query(models.Task)
	if status:
		q = q.filter(models.Task.status == status)
	if due_before:
		q = q.filter(models.Task.due_date != None).filter(models.Task.due_date <= due_before)  # noqa: E71
	if due_after:
		q = q.filter(models.Task.due_date != None).filter(models.Task.due_date >= due_after)  # noqa: E711
	return q.order_by(models.Task.created_at.desc()).all()
@app.get("/tasks/{task_id}", response_model=schema.TaskOut, tags=["tasks"])
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
@app.put("/tasks/{task_id}", response_model=schema.TaskOut, tags=["tasks"])
def update_task(task_id: int, payload: schema.TaskCreate, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in payload.dict().items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task
@app.patch("/tasks/{task_id}", response_model=schema.TaskOut, tags=["tasks"])
def patch_task(task_id: int, payload: schema.TaskUpdate, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    update_data = payload.dict(exclude_unset=True)

    # (safer) Only allow known fields
    for key in {"title", "description", "status", "due_date"} & update_data.keys():
        setattr(task, key, update_data[key])

    db.commit()
    db.refresh(task)
    return task
@app.delete("/tasks/{task_id}", tags=["tasks"])
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"ok": True}