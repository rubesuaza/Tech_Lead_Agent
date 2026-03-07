"""Unit tests for application port interfaces (input/output)."""
import pytest
from uuid import uuid4

from src.domain.models import ProjectMaster, UseCase
from src.application.ports.input import ProjectQueryUseCase
from src.application.ports.output import ProjectRepository


def _sample_project_master():
    return ProjectMaster(
        project_id=uuid4(),
        project_code="PRJ-001",
        project_name="Test",
        stack_tecnologico={},
        coding_standards=("PEP8",),
        patrones_diseno=(),
        estructura_directorios="# Struct",
        reglas_dominio="# Rules",
        checklist="",
        lista_casos_uso=(UseCase("UC01", "Create", "low"),),
    )


class TestProjectQueryUseCase:
    """Input port: get_all_projects, get_project_by_id."""

    def test_interface_has_get_all_projects(self):
        assert hasattr(ProjectQueryUseCase, "get_all_projects")
        assert getattr(ProjectQueryUseCase.get_all_projects, "__isabstractmethod__", False) or "get_all_projects" in ProjectQueryUseCase.__abstractmethods__

    def test_interface_has_get_project_by_id(self):
        assert hasattr(ProjectQueryUseCase, "get_project_by_id")

    def test_cannot_instantiate_without_implementation(self):
        with pytest.raises(TypeError):
            ProjectQueryUseCase()  # type: ignore


class TestProjectRepository:
    """Output port: find_all, find_by_id."""

    def test_interface_has_find_all(self):
        assert hasattr(ProjectRepository, "find_all")

    def test_interface_has_find_by_id(self):
        assert hasattr(ProjectRepository, "find_by_id")

    def test_cannot_instantiate_without_implementation(self):
        with pytest.raises(TypeError):
            ProjectRepository()  # type: ignore
