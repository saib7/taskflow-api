from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import engine, get_db
from app.models import Task
from app.schemas import TaskCreate, TaskRead


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.connect() as conn:
        await conn.execute(text("SELECT 1"))
    print("Database connection OK")
    yield
    await engine.dispose()


app = FastAPI(title=settings.app_name, lifespan=lifespan)

# A reusable type alias: "a database session, provided by get_db"
DbSession = Annotated[AsyncSession, Depends(get_db)]


@app.get("/")
def read_root() -> dict:
    return {"message": f"Welcome to {settings.app_name}"}


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok"}


@app.get("/tasks", response_model=list[TaskRead])
async def list_tasks(db: DbSession, completed: bool | None = None):
    stmt = select(Task).order_by(Task.id)
    if completed is not None:
        stmt = stmt.where(Task.completed == completed)
    result = await db.execute(stmt)
    return result.scalars().all()


@app.post("/tasks", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate, db: DbSession):
    new_task = Task(**task.model_dump())
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return new_task


@app.get("/tasks/{task_id}", response_model=TaskRead)
async def get_task(task_id: int, db: DbSession):
    task = await db.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.put("/tasks/{task_id}", response_model=TaskRead)
async def update_task(task_id: int, data: TaskCreate, db: DbSession):
    task = await db.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    for field, value in data.model_dump().items():
        setattr(task, field, value)
    await db.commit()
    await db.refresh(task)
    return task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, db: DbSession):
    task = await db.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    await db.delete(task)
    await db.commit()