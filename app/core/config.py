import os.path
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BasePath = Path(__file__).resolve().parent.parent
env_path = os.path.join(BasePath, os.environ.get('ENV_FILE', 'dev.env'))


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=env_path, env_file_encoding='utf-8')

    API_V1_STR: str = "/api/v1"

    BACKEND_CORS_ORIGINS: str = "*"

    # MONGODB_URL
    MONGODB_URL: str = ""

    # OPENAI_API_KEY
    OPENAI_API_KEY: str = "sk-proj-jnlWkUZyXwdMPMl5YmU6T3BlbkFJiHuwTUxDZNZ8EX0qUZiM"

    SYSTEM_PROMPT: str = "You are the main character in this story, talk to the other person in a short, concise way that is true to the main character's personality."

    # JWT
    SECRET_KEY: str = "secret"
    TOKEN_EXPIRED_TIME: int = 24

    # LIMITER
    REDIS_URL: str = "redis://localhost"
    REDIS_PREFIX: str = "fastapi-limiter"
    RATE_LIMIT_TIME: int = 60
    RATE_LIMIT_REQUEST: int = 50


settings = Settings()
