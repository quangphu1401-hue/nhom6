from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/agrobi_db"
    
    # API Keys
    OPENWEATHER_API_KEY: str = ""
    GEMINI_API_KEY: str = ""
    
    # Application
    SECRET_KEY: str = "your-secret-key-change-in-production"
    DEBUG: bool = True
    CORS_ORIGINS: str = "http://localhost:3000,http://127.0.0.1:5500,http://localhost:5500"
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS_ORIGINS string thành list"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

