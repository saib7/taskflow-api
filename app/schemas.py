from pydantic import BaseModel, ConfigDict, Field


class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str | None = None
    completed: bool = False


class TaskCreate(TaskBase):
    pass


class TaskRead(TaskBase):
    id: int
    model_config = ConfigDict(from_attributes=True)  # build this from task.id, task.title, etc.
    