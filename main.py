from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy.orm import Session

import models
import schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Manager API")

API_TOKEN = "demo-token"


def verify_token(x_token: str = Header(default="")):
    if x_token != API_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid or missing X-Token header")


@app.get("/")
def root():
    return {"message": "Task Manager API is running"}


@app.post("/projects", response_model=schemas.ProjectOut, dependencies=[Depends(verify_token)])
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    db_project = models.Project(**project.dict())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


@app.get("/projects/{project_id}/tasks", response_model=List[schemas.TaskOut])
def get_project_tasks(project_id: int, db: Session = Depends(get_db)):
    return db.query(models.Task).filter(models.Task.project_id == project_id).all()


@app.get("/tasks", response_model=List[schemas.TaskOut])
def list_tasks(status: Optional[str] = None, priority: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(models.Task)
    if status:
        query = query.filter(models.Task.status == status)
    if priority:
        query = query.filter(models.Task.priority == priority)
    return query.all()


@app.post("/tasks", response_model=schemas.TaskOut, dependencies=[Depends(verify_token)])
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    db_task = models.Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.get("/tasks/{task_id}", response_model=schemas.TaskOut)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.put("/tasks/{task_id}", response_model=schemas.TaskOut, dependencies=[Depends(verify_token)])
def update_task(task_id: int, task: schemas.TaskUpdate, db: Session = Depends(get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    for field, value in task.dict(exclude_unset=True).items():
        setattr(db_task, field, value)
    db.commit()
    db.refresh(db_task)
    return db_task


@app.delete("/tasks/{task_id}", dependencies=[Depends(verify_token)])
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(db_task)
    db.commit()
    return {"detail": "Task deleted"}
