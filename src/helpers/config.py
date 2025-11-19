"""Configuration settings for the application."""

import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Settings for the EV application.
    Dynamic loading from environment variables (.env).
    """

    APP_NAME: str = "EV Routing & Battery Simulator"
    APP_VERSION: str = "1.0.0"

    # API keys
    OPENCHARGEMAP_API_KEY: str

    # Defaults
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    DEFAULT_SPEED_KMH: float = float(os.getenv("DEFAULT_SPEED_KMH", "90"))
    DEFAULT_SEGMENTS: int = int(os.getenv("DEFAULT_SEGMENTS", "10"))

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8", "extra": "allow"}

    input_file: str | None = None
    output_file: str | None = None


def get_settings() -> Settings:
    """
    Return loaded application settings.
    Uses caching pattern to prevent reloading multiple times.
    """
    return Settings()
