"""Unit tests for ProjectQueryService (use case implementation)."""
from uuid import uuid4

from src.domain.models import ProjectMaster, UseCase
from src.application.services import ProjectQueryService
from src.infrastructure.persistence import InMemoryProjectRepository


def _valid_project_master(**overrides):
    kwargs = {
        "project_id": uuid4(),
        "project_code": "PRJ-001",
        "project_name": "Order Management",
        "stack_tecnologico": {"language": "Python"},
        "coding_standards": ("PEP8",),
        "patrones_diseno": (),
        "estructura_directorios": "# Structure",
        "reglas_dominio": "# Rules",
        "checklist": "# Check",
        "lista_casos_uso": (UseCase("UC01", "Create", "medium"),),
    }
    kwargs.update(overrides)
    return ProjectMaster(**kwargs)


class TestProjectQueryService:
    """Delegation to repository port."""

    def test_get_all_projects_empty(self):
        repo = InMemoryProjectRepository()
        service = ProjectQueryService(project_repository=repo)
        assert service.get_all_projects() == []

    def test_get_all_projects_returns_repo_data(self):
        p = _valid_project_master()
        repo = InMemoryProjectRepository(initial=[p])
        service = ProjectQueryService(project_repository=repo)
        result = service.get_all_projects()
        assert len(result) == 1
        assert result[0].project_id == p.project_id

    def test_get_project_by_id_found(self):
        p = _valid_project_master()
        repo = InMemoryProjectRepository(initial=[p])
        service = ProjectQueryService(project_repository=repo)
        assert service.get_project_by_id(p.project_id) is p

    def test_get_project_by_id_not_found(self):
        repo = InMemoryProjectRepository()
        service = ProjectQueryService(project_repository=repo)
        assert service.get_project_by_id(uuid4()) is None
