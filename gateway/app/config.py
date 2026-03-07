from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "OpsPulse Gateway"
    agent_base_url: str = "http://localhost:8080"
    request_timeout_seconds: float = 5.0

    model_config = SettingsConfigDict(env_prefix="OPS_PULSE_", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()

