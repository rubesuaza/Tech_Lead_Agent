"""
PostgreSQL adapter for ProjectRepository (output port).
Uses SQLAlchemy Core to read from view_project_master_context and maps rows to domain ProjectMaster.
"""

from uuid import UUID

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from domain.ports.project_repository import ProjectRepository
from domain.models import ProjectMaster
from infrastructure.config import DatabaseSettings
from infrastructure.persistence.mappers import row_to_project_master

view_name = "view_project_master_context"


def _sqlalchemy_url(settings: DatabaseSettings) -> str:
    """Build SQLAlchemy URL from settings (psycopg driver)."""
    base = settings.dsn
    if base.startswith("postgresql://"):
        return base.replace("postgresql://", "postgresql+psycopg://", 1)
    return base


class PostgresProjectRepository(ProjectRepository):
    """
    Driven adapter: implements ProjectRepository using SQLAlchemy and PostgreSQL.
    Queries the view_project_master_context view.
    """

    def __init__(self, settings: DatabaseSettings | None = None):
        self._settings = settings or DatabaseSettings()
        self._engine: Engine | None = None

    def _get_engine(self) -> Engine:
        if self._engine is None:
            self._engine = create_engine(_sqlalchemy_url(self._settings))
        return self._engine

    def find_all(self) -> list[ProjectMaster]:
        """Retrieves all rows from the master view."""
        engine = self._get_engine()
        with engine.connect() as conn:
            result = conn.execute(text(f"SELECT * FROM {view_name}"))
            columns = result.keys()
            return [
                row_to_project_master(dict(zip(columns, row)))
                for row in result.fetchall()
            ]

    def find_by_id(self, project_id: UUID) -> ProjectMaster | None:
        """Retrieves a specific row from the master view by project_id."""
        engine = self._get_engine()
        with engine.connect() as conn:
            result = conn.execute(
                text(f"SELECT * FROM {view_name} WHERE project_id = :pid"),
                {"pid": str(project_id)},
            )
            row = result.fetchone()
            if row is None:
                return None
            columns = result.keys()
            return row_to_project_master(dict(zip(columns, row)))
