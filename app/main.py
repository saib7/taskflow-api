from fastapi import FastAPI

from app.config import settings

app = FastAPI(title=settings.app_name)


@app.get("/")
def read_root() -> dict:
    return {"message": f"Welcome to {settings.app_name}"}


@app.get("/health")
def health_check() -> dict:
    """Simple liveness check -- useful once this is ever deployed."""
    return {"status": "ok"}
