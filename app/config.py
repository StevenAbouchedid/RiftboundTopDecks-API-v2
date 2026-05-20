"""
Application configuration
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings"""
    
    # API
    API_VERSION: str = "v2"
    API_TITLE: str = "Riftbound Stats V2 API"
    API_DESCRIPTION: str = "FastAPI backend for Riftbound Stats"
    DEBUG: bool = True
    
    # Database
    DATABASE_V2_URL: str
    
    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:3001"
    
    # Redis (optional)
    REDIS_URL: str | None = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
