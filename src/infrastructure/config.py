"""
Infrastructure configuration (DB, etc.) via pydantic-settings.
Loads from environment variables.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    """
    PostgreSQL connection settings from env.
    Defaults enforce connection via Cloud SQL Auth Proxy (localhost:5432).
    Set DB_HOST=127.0.0.1 and DB_PORT=5432 when using the proxy.
    """

    model_config = SettingsConfigDict(
        env_prefix="DB_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    host: str = "127.0.0.1"
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
