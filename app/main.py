from fastapi import FastAPI, HTTPException, status

from app.config import settings
from app.schemas import Task, TaskCreate

app = FastAPI(title=settings.app_name)

# Temporary in-memory "database" -- replaced by Postgres in Phase 2.
tasks_db: dict[int, Task] = {}
next_id = 1


@app.get("/tasks", response_model=list[Task])
def list_tasks(completed: bool | None = None):
    """List tasks, optionally filtered: /tasks?completed=true"""
    values = list(tasks_db.values())
    if completed is not None:
        values = [t for t in values if t.completed == completed]
    return values


@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate):
    global next_id
    new_task = Task(id=next_id, **task.model_dump())
    tasks_db[next_id] = new_task
    next_id += 1
    return new_task


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    task = tasks_db.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task: TaskCreate):
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")
    updated = Task(id=task_id, **task.model_dump())
    tasks_db[task_id] = updated
    return updated


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")
    del tasks_db[task_id]
