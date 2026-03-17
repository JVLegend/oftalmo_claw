"""OftalmoClaw - Configuration Management"""

import os
from pathlib import Path
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # App
    app_name: str = "OftalmoClaw"
    app_version: str = "0.1.0"
    debug: bool = False
    secret_key: str = "change-me-to-a-random-secret-key"

    # Server
    host: str = "0.0.0.0"
    port: int = int(os.getenv("PORT", "8000"))
    log_level: str = "INFO"

    # Database
    database_url: str = "sqlite+aiosqlite:///./data/oftalmo_claw.db"

    # LLM
    openrouter_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    default_model: str = "anthropic/claude-sonnet-4-20250514"

    # Storage
    upload_dir: Path = Path("./uploads")
    max_upload_size_mb: int = 50

    # Gateway
    telegram_token: Optional[str] = None
    whatsapp_token: Optional[str] = None
    discord_token: Optional[str] = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

# Ensure directories exist
settings.upload_dir.mkdir(parents=True, exist_ok=True)
Path("./data").mkdir(parents=True, exist_ok=True)
Path("./logs").mkdir(parents=True, exist_ok=True)
