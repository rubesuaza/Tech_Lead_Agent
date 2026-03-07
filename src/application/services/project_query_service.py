"""
Application service: implements ProjectQueryUseCase using ProjectRepository.
Lives in application layer; depends only on ports (output) and domain.
"""
from uuid import UUID

from src.application.ports.input import ProjectQueryUseCase
from src.application.ports.output import ProjectRepository
from src.domain.models import ProjectMaster


class ProjectQueryService(ProjectQueryUseCase):
    """Concrete implementation: delegates to ProjectRepository (view_project_master_context)."""

    def __init__(self, project_repository: ProjectRepository) -> None:
        self._repository = project_repository

    def get_all_projects(self) -> list[ProjectMaster]:
        """Returns all project summaries from the master view."""
        return self._repository.find_all()

    def get_project_by_id(self, project_id: UUID) -> ProjectMaster | None:
        """Returns the ProjectMaster for the given id, or None if not found."""
        return self._repository.find_by_id(project_id)
