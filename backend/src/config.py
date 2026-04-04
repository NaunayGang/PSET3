"""Application configuration."""

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load values from .env in local development.
load_dotenv()


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database
    DATABASE_URL: str = "postgresql://opscenter:opscenter@localhost:5432/opscenter"

    # JWT
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Application
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"

    # CORS
    CORS_ALLOW_ORIGINS: str = "http://localhost:8501,http://localhost:3000,http://localhost:8000"
    CORS_ALLOW_METHODS: str = "*"
    CORS_ALLOW_HEADERS: str = "*"
    CORS_ALLOW_CREDENTIALS: bool = True

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.CORS_ALLOW_ORIGINS.split(",") if origin.strip()]

    @property
    def cors_methods(self) -> list[str]:
        return [method.strip() for method in self.CORS_ALLOW_METHODS.split(",") if method.strip()]

    @property
    def cors_headers(self) -> list[str]:
        return [header.strip() for header in self.CORS_ALLOW_HEADERS.split(",") if header.strip()]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
