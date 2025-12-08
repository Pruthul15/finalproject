from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import Optional, List


class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5434/fastapi_db"
    
    # JWT Settings
    JWT_SECRET_KEY: str = "your-super-secret-key-change-this-in-production"
    JWT_REFRESH_SECRET_KEY: str = "your-refresh-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Security
    SECRET_KEY: str = "fallback-secret-key"  # ADD THIS
    BCRYPT_ROUNDS: int = 12
    CORS_ORIGINS: List[str] = ["*"]
    
    # Redis - ADD THESE
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_URL: Optional[str] = "redis://localhost:6379/0"
    
    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra='ignore'  # Change from 'forbid' to 'ignore'
    )


settings = Settings()


@lru_cache()
def get_settings() -> Settings:
    return Settings()
