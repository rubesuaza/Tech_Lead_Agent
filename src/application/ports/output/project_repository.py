"""
Output port (driven): contract for persistence layer.
Implemented by infrastructure adapters (e.g. SQLAlchemy over view_project_master_context).
Only standard library (abc); no framework dependencies.
"""
from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.models import ProjectMaster


class ProjectRepository(ABC):
    """Contract for the infrastructure layer to fetch data from the master view."""

    @abstractmethod
    def find_all(self) -> list[ProjectMaster]:
        """Retrieves all rows from the master view."""
        ...

    @abstractmethod
    def find_by_id(self, project_id: UUID) -> ProjectMaster | None:
        """Retrieves a specific row from the master view by project_id."""
        ...
