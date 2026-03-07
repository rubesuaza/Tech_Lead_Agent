"""
In-memory adapter for ProjectRepository (view_project_master_context).
Implements the output port; no business logic. Suitable for tests and development.
"""
from uuid import UUID

from src.application.ports.output import ProjectRepository
from src.domain.models import ProjectMaster


class InMemoryProjectRepository(ProjectRepository):
    """Stores ProjectMaster instances in memory. Implements ProjectRepository port."""

    def __init__(self, initial: list[ProjectMaster] | None = None) -> None:
        self._store: dict[UUID, ProjectMaster] = {}
        for p in initial or []:
            self._store[p.project_id] = p

    def find_all(self) -> list[ProjectMaster]:
        """Returns all projects in insertion order (by first-seen id)."""
        return list(self._store.values())

    def find_by_id(self, project_id: UUID) -> ProjectMaster | None:
        """Returns the project with the given id or None."""
        return self._store.get(project_id)

    def add(self, project: ProjectMaster) -> None:
        """Convenience: add or replace a project (useful for seeding)."""
        self._store[project.project_id] = project
