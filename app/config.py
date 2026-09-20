"""
Central app configuration.

We read settings from environment variables (and a local .env file, for dev)
instead of hardcoding them. This is the pattern FastAPI's own docs recommend:
https://fastapi.tiangolo.com/advanced/settings/

Nothing here talks to Postgres yet -- that's Phase 2. For now this just gives
us one place to control app-wide values like the app name and debug flag.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "TaskFlow API"
    debug: bool = True

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


# A single, importable instance. Anywhere else in the app that needs a
# setting does `from app.config import settings` rather than re-reading
# environment variables itself.
settings = Settings()
