def settings():
    from pydantic_settings import BaseSettings
    from typing import Optional
    from functools import lru_cache

    class Settings(BaseSettings):
        # Base
        PROJECT_NAME: str = "API de Laudos Psicológicos"
        VERSION: str = "1.0.0"
        API_V1_STR: str = "/api/v1"

        # Database
        DATABASE_URL: str

        # Security
        SECRET_KEY: str
        ALGORITHM: str = "HS256"
        ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

        # CORS
        BACKEND_CORS_ORIGINS: list = ["http://localhost:3000"]

        # SMTP
        SMTP_TLS: bool = True
        SMTP_PORT: Optional[int] = None
        SMTP_HOST: Optional[str] = None
        SMTP_USER: Optional[str] = None
        SMTP_PASSWORD: Optional[str] = None

        # Storage
        UPLOAD_DIR: str = "uploads"
        MAX_UPLOAD_SIZE: int = 5_242_880  # 5MB

        # AI Model
        MODEL_PATH: Optional[str] = None

        class Config:
            case_sensitive = True
            env_file = ".env"

    @lru_cache()
    def get_settings():
        return Settings()

    settings = get_settings()