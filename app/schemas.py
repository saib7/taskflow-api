from pydantic import BaseModel, Field


class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str | None = None
    completed: bool = False


class TaskCreate(TaskBase):
    """What a client sends when creating (or fully updating) a task."""

    pass


class Task(TaskBase):
    """What we send back -- adds the server-assigned id."""

    id: int
