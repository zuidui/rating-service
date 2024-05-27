import os
import secrets

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = f"{os.environ.get('APP_NAME', 'demo').capitalize()} API"
    DESCRIPTION: str = os.environ.get("DESCRIPTION", "")
    VERSION: str = os.environ.get("APP_VERSION", "")
    PREFIX: str = os.environ.get("PREFIX", "")
    ENV: str = os.environ.get("ENV", "development")
    SECRET_KEY: str = secrets.token_urlsafe(32)
    DOC_URL: str = os.environ.get("DOC_URL", "")
    DATABASE_URL: str = os.environ.get("DATABASE_URL", "")
    REDIS_URL: str = os.environ.get("REDIS_URL", "")
    model_config = SettingsConfigDict(env_file="app/.env", env_file_encoding="utf-8")


def get_settings():
    return Settings()
