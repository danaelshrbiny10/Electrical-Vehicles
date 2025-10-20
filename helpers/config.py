"""Configuration settings for the application."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings for the application."""

    APP_NAME: str
    APP_VERSION: str
    OPENCHARGEMAP_API_KEY: int


    class Config:
        """Configuration for the settings."""

        env_file = ".env"
        env_file_encoding = "utf-8"


def get_settings():
    """Get the application settings."""
    return Settings()
