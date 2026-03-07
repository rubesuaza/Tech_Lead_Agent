"""
Dependency injection wiring for FastAPI.
Provides factory functions for use with Depends().
"""

from application.ports.output.project_repository import ProjectRepository
from infrastructure.config import DatabaseSettings
from infrastructure.persistence.postgres_project_repository import PostgresProjectRepository


def get_db_settings() -> DatabaseSettings:
    """Returns database settings from environment (for Depends)."""
    return DatabaseSettings()


def get_project_repository(
    settings: DatabaseSettings | None = None,
) -> ProjectRepository:
    """Returns the PostgreSQL implementation of ProjectRepository (for Depends)."""
    return PostgresProjectRepository(settings=settings or get_db_settings())
