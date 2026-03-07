from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "OpsPulse Agent"
    demo_mode: bool = False
    disk_path: str = "/"
    process_limit: int = Field(default=5, ge=1)
    sample_interval_seconds: float = Field(default=3.0, gt=0)
    history_size: int = Field(default=120, ge=1)

    model_config = SettingsConfigDict(env_prefix="OPS_PULSE_", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
