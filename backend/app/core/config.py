from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    vector_backend: str = "chroma"
    database_url: str | None = None
    rate_limit_enabled: bool = True
    cors_origins: list[str] = ["http://localhost:5173"]

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
