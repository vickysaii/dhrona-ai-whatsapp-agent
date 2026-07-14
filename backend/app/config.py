import os
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # -----------------------------
    # Application Settings
    # -----------------------------
    APP_NAME: str = "WhatsApp AI Business Agent"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # -----------------------------
    # Supabase
    # -----------------------------
    SUPABASE_URL: str = Field(...)
    SUPABASE_KEY: str = Field(...)

    # -----------------------------
    # Groq
    # -----------------------------
    GROQ_API_KEY: str
    GROQ_MODEL: str = "llama-3.3-70b-versatile"

    # -----------------------------
    # WhatsApp Cloud API
    # -----------------------------
    WHATSAPP_PHONE_NUMBER_ID: str = Field(...)
    WHATSAPP_BUSINESS_ACCOUNT_ID: str = Field(...)
    WHATSAPP_ACCESS_TOKEN: str = Field(...)
    WHATSAPP_VERIFY_TOKEN: str = Field(...)

    # -----------------------------
    # Redis
    # -----------------------------
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = ""
    REDIS_DB: int = 0

    # -----------------------------
    # JWT
    # -----------------------------
    JWT_SECRET: str = Field(...)
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    SETTINGS_ID: str = "default"

    model_config = SettingsConfigDict(
        env_file=os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            ".env",
        ),
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()