"""
PostgreSQL adapter for ProjectRepository (output port).
Reads from view_project_master_context and maps rows to domain ProjectMaster.
"""

from uuid import UUID

import psycopg

from application.ports.output.project_repository import ProjectRepository
from domain.models import ProjectMaster
from infrastructure.config import DatabaseSettings
from infrastructure.persistence.mappers import row_to_project_master

VIEW_NAME = "view_project_master_context"


class PostgresProjectRepository(ProjectRepository):
    """
    Driven adapter: implements ProjectRepository using PostgreSQL.
    Queries the view_project_master_context view.
    """

    def __init__(self, settings: DatabaseSettings | None = None):
        self._settings = settings or DatabaseSettings()

    def find_all(self) -> list[ProjectMaster]:
        """Retrieves all rows from the master view."""
        with psycopg.connect(self._settings.dsn) as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {VIEW_NAME}")
                columns = [d.name for d in cur.description]
                rows = (dict(zip(columns, row)) for row in cur.fetchall())
                return [row_to_project_master(r) for r in rows]

    def find_by_id(self, project_id: UUID) -> ProjectMaster | None:
        """Retrieves a specific row from the master view by project_id."""
        with psycopg.connect(self._settings.dsn) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"SELECT * FROM {VIEW_NAME} WHERE project_id = %s",
                    (str(project_id),),
                )
                row = cur.fetchone()
                if row is None:
                    return None
                columns = [d.name for d in cur.description]
                return row_to_project_master(dict(zip(columns, row)))
