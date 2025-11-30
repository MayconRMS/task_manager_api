from sqlmodel import Session, select
from fastapi import HTTPException
from datetime import datetime

from app.models.task import Task
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate

def create_task_service(task: TaskCreate, db: Session, current_user: User):
    db_task = Task(**task.dict(), owner_id=current_user.id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def list_tasks_service(db: Session, current_user: User, status: str | None, skip: int, limit: int):
    query = select(Task).where(Task.owner_id == current_user.id)

    if status:
        query = query.where(Task.status == status)

    tasks = db.exec(query.offset(skip).limit(limit)).all()
    return tasks

def get_task_service(task_id: int, db: Session, current_user: User):
    task = db.get(Task, task_id)
    if not task or task.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return task

def update_task_service(task_id: int, task_data: TaskUpdate, db: Session, current_user: User):
    task = db.get(Task, task_id)

    if not task or task.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    for key, value in task_data.dict(exclude_unset=True).items():
        setattr(task, key, value)

    if task.status == "concluido" and not task.completed_at:
        task.completed_at = datetime.utcnow()

    db.add(task)
    db.commit()
    db.refresh(task)

    return task

def delete_task_service(task_id: int, db: Session, current_user: User):
    task = db.get(Task, task_id)

    if not task or task.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    db.delete(task)
    db.commit()

    return {"detail": "Tarefa deletada"}
