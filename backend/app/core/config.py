from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "MindScope Backend"
    app_env: str = "development"
    api_prefix: str = "/api/v1"
    database_url: str
    cors_origins: str = "http://localhost:4200,http://127.0.0.1:4200"
    cors_origin_regex: str = r"https?://(localhost|127\.0\.0\.1)(:\d+)?"
    supabase_url: str = ""
    supabase_jwks_url: str = ""
    supabase_jwt_audience: str = "authenticated"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def supabase_issuer(self) -> str:
        return f"{self.supabase_url.rstrip('/')}/auth/v1"


@lru_cache
def get_settings() -> Settings:
    return Settings()
