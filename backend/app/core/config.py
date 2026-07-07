"""
Central application configuration.
Loaded once as a singleton via get_settings().
"""
from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # --- App ---
    APP_NAME: str = "Synthetic User Generation Platform"
    ENV: Literal["dev", "staging", "prod"] = "dev"
    DEBUG: bool = True
    # API prefix includes /v1 to match frontend expectations
    API_PREFIX: str = "/api/v1"

    # --- Database ---
    # Defaults to local SQLite (aiosqlite) so the service runs with zero setup.
    # Point this at Postgres/Neon in staging/prod, e.g.:
    # postgresql+asyncpg://user:pass@host:5432/dbname
    DATABASE_URL: str = "sqlite+aiosqlite:///./vidzai.db"
    DATABASE_ECHO: bool = False

    # --- Auth (wired in a later milestone, present now for config completeness) ---
    JWT_SECRET_KEY: str = "change-me-in-prod"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60 * 24

    # --- LLM / AI Gateway ---
    # Provider order: Groq (this project's frontend/README specifies Groq as
    # the AI provider) -> Gemini -> Ollama -> synthetic (Faker) fallback if
    # nothing is configured/reachable. Only candidates with a key configured
    # (or, for Ollama, unconditionally as a last network attempt) are tried;
    # see app/ai/model_router.py.
    GROQ_API_KEY: str | None = None
    GROQ_MODEL: str = "groq/llama-3.3-70b-versatile"

    GEMINI_API_KEY: str | None = None
    GEMINI_MODEL: str = "gemini/gemini-1.5-flash"

    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "ollama/llama3.1"

    LLM_TEMPERATURE: float = 0.9
    LLM_MAX_TOKENS: int = 2048
    LLM_TIMEOUT_SECONDS: int = 30

    # --- Persona generation ---
    MIN_PERSONAS_PER_EXPERIMENT: int = 3
    MAX_PERSONAS_PER_EXPERIMENT: int = 12
    DEFAULT_PERSONA_COUNT: int = 6

    # --- Redis / Celery (wired in a later milestone) ---
    REDIS_URL: str = "redis://localhost:6379/0"

    # --- Logging ---
    LOG_LEVEL: str = "INFO"


@lru_cache
def get_settings() -> Settings:
    return Settings()
