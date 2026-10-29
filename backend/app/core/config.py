from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    vector_backend: str = "chroma"
    database_url: str | None = None
    rate_limit_enabled: bool = True
    cors_origins: list[str] = ["http://localhost:5173"]

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    app_name: str = "PolicyPilot AI"
    domain_hint: str = ""
    summary_query: str = (
        "overview purpose key points important terms conditions exceptions limits steps"
    )
    greeting_reply: str = (
        "Hi! 👋 Ask me anything about your document, or ask for a summary or a full report."
    )
    not_found_reply: str = "I couldn't find this in the uploaded document."
    boilerplate_patterns: list[str] = []  # optional extra regexes, JSON list in .env
    boilerplate_min_ratio: float = (
        0.6  # a line on 60%+ of pages counts as header/footer
    )
    domain_stopwords: list[str] = []

    jwt_secret: str = "change-me"
    jwt_expire_minutes: int = 60 * 24


settings = Settings()
