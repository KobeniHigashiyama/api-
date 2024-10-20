from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.endpoints.users import get_current_user
from app.shemas.task import TaskCreate, TaskUpdate, TaskInDB
from app.db import models
from app.db.database import get_db
from app.core.security import oauth2_scheme

router = APIRouter()

@router.post("/", response_model=TaskInDB)
def create_task(task: TaskCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    db_task = models.Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.put("/{task_id}/assign", response_model=TaskInDB)
def assign_task_to_user(task_id: int, assigned_user_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    db_task.assigned_user_id = assigned_user_id
    db.commit()
    db.refresh(db_task)
    return db_task


@router.put("/{task_id}", response_model=TaskInDB)
def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    for key, value in task.dict(exclude_unset=True).items():
        setattr(db_task, key, value)
    
    db.commit()
    db.refresh(db_task)
    return db_task


@router.get("/mytasks", response_model=list[TaskInDB])
def get_my_tasks(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    current_user = get_current_user(db, token)
    tasks = db.query(models.Task).filter(models.Task.owner_id == current_user.id).all()
    return tasks

@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    current_user = get_current_user(db, token)
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    if db_task.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to delete this task")

    db.delete(db_task)
    db.commit()
    return {"detail": "Task deleted"}