from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


ROOT_ENV_FILE = Path(__file__).resolve().parents[2] / ".env"


class Settings(BaseSettings):
    app_name: str = "Mythadis AI Debate Arena"
    version: str = "0.1.0-local-foundation"
    openai_api_key: str = ""
    gemini_api_key: str = ""
    openai_model: str = "gpt-4.1-mini"
    gemini_model: str = "gemini-2.5-flash"

    model_config = SettingsConfigDict(
        env_file=(ROOT_ENV_FILE, ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
