from fastapi import APIRouter, Depends, Query
from sqlmodel import Session
from typing import List

from app.schemas.task import TaskCreate, TaskRead, TaskUpdate
from app.models.user import User
from app.deps import get_db, get_current_user

from app.services.task_service import (
    create_task_service,
    list_tasks_service,
    get_task_service,
    update_task_service,
    delete_task_service
)

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=TaskRead)
def create_task(task: TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return create_task_service(task, db, current_user)

@router.get("/", response_model=List[TaskRead])
def list_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    status: str | None = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1)
):
    return list_tasks_service(db, current_user, status, skip, limit)

@router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_task_service(task_id, db, current_user)

@router.put("/{task_id}", response_model=TaskRead)
def update_task(task_id: int, task_data: TaskUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return update_task_service(task_id, task_data, db, current_user)

@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return delete_task_service(task_id, db, current_user)
