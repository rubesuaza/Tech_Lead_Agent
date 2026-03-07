"""
Infrastructure configuration (DB, etc.) via pydantic-settings.
Loads from environment variables.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    """PostgreSQL connection settings from env."""

    model_config = SettingsConfigDict(
        env_prefix="DB_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    host: str = "localhost"
    port: int = 5432
    name: str = "tech_lead_agent"
    user: str = ""
    password: str = ""

    @property
    def dsn(self) -> str:
        """Connection string for psycopg."""
        return (
            f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"
        )
