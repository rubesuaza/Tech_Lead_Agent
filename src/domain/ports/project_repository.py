"""
Output port (driven): contract for persistence layer.
Domain defines the interface; infrastructure adapters implement it.
"""

from abc import ABC, abstractmethod
from uuid import UUID

from domain.models import ProjectMaster


class ProjectRepository(ABC):
    """
    Output port: contract for retrieving project master data from PostgreSQL view.
    find_all(): all rows from master view.
    find_by_id(id): single row by project_id.
    """

    @abstractmethod
    def find_all(self) -> list[ProjectMaster]:
        """Retrieves all rows from the master view."""
        ...

    @abstractmethod
    def find_by_id(self, project_id: UUID) -> ProjectMaster | None:
        """Retrieves a specific row from the master view by project_id. Returns None if not found."""
        ...
