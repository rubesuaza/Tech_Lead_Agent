"""
Input port (driving): use case for querying project data.
Defines the application contract for fetching project master context.
"""

from abc import ABC, abstractmethod
from uuid import UUID

from domain.models import ProjectMaster


class ProjectQueryUseCase(ABC):
    """
    Input port: interface to fetch project data.
    get_all_projects(): list of project summaries.
    get_project_by_id(id): full ProjectMaster aggregate.
    """

    @abstractmethod
    def get_all_projects(self) -> list[dict]:
        """Returns a list of all project summaries (e.g. project_id, project_code, project_name, stack_tecnologico)."""
        ...

    @abstractmethod
    def get_project_by_id(self, project_id: UUID) -> ProjectMaster:
        """Returns the full ProjectMaster aggregate for the given id. Raises ProjectNotFoundException if not found."""
        ...
