"""
Input port (driving): contract for querying project data.
Consumed by adapters (e.g. HTTP); implemented by application services.
Only standard library (abc); no framework dependencies.
"""
from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.models import ProjectMaster


class ProjectQueryUseCase(ABC):
    """Defines methods to fetch project data (view_project_master_context)."""

    @abstractmethod
    def get_all_projects(self) -> list[ProjectMaster]:
        """Returns a list of all project summaries (or full aggregates per contract)."""
        ...

    @abstractmethod
    def get_project_by_id(self, project_id: UUID) -> ProjectMaster | None:
        """Returns the full ProjectMaster aggregate for the given id, or None if not found."""
        ...
