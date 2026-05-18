# config.py
import os
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # MongoDB
    MONGO_URL: str
    DATABASE_NAME: str = "ftds_db"

    # SMTP Configuration
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASSWORD: str
    
    # Admin Email (Map to CONTACT_RECEIVER_EMAIL from .env)
    ADMIN_EMAIL: str = Field(alias="CONTACT_RECEIVER_EMAIL")

    @field_validator("SMTP_PASSWORD", mode="before")
    @classmethod
    def sanitize_password(cls, v: str) -> str:
        if isinstance(v, str):
            return v.replace(" ", "").strip()
        return v

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
