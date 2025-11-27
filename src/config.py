"""Global configuration management using Pydantic Settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # API Keys
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    LANGCHAIN_API_KEY: Optional[str] = None


    CSTCLOUD_API_KEY: Optional[str] = "bb1a6baf7fa816a5c8986b759d8b48b29e3419c55fcbd86991fd58559f68c99c"
    CSTCLOUD_BASE_URL: str = "https://uni-api.cstcloud.cn/v1"
    CSTCLOUD_MODEL: str = "deepseek-r1:671b"

    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/hydroagent"
    POSTGRES_USER: str = "hydroagent"
    POSTGRES_PASSWORD: str = "hydroagent"
    POSTGRES_DB: str = "hydroagent"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # LangSmith
    LANGCHAIN_TRACING_V2: bool = False
    LANGCHAIN_PROJECT: str = "hydroagent"

    # Application Settings
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


# Global settings instance
settings = Settings()

