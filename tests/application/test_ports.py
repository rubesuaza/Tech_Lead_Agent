"""Unit tests for application ports (interfaces)."""

import sys
import uuid
from pathlib import Path

# tests/application/test_*.py -> parents[2] = project root
_src = Path(__file__).resolve().parents[2] / "src"
if _src.exists() and str(_src) not in sys.path:
    sys.path.insert(0, str(_src))

import pytest

from application.ports.input.project_query_use_case import ProjectQueryUseCase
from application.ports.output.project_repository import ProjectRepository
from domain.models import ProjectMaster


class TestProjectQueryUseCase:
    def test_interface_has_required_methods(self):
        assert hasattr(ProjectQueryUseCase, "get_all_projects")
        assert hasattr(ProjectQueryUseCase, "get_project_by_id")

    def test_concrete_implementation_can_be_instantiated(self):
        class StubQueryUseCase(ProjectQueryUseCase):
            def get_all_projects(self):
                return []

            def get_project_by_id(self, project_id):
                raise NotImplementedError

        stub = StubQueryUseCase()
        assert stub.get_all_projects() == []


class TestProjectRepository:
    def test_interface_has_required_methods(self):
        assert hasattr(ProjectRepository, "find_all")
        assert hasattr(ProjectRepository, "find_by_id")

    def test_concrete_implementation_can_be_instantiated(self):
        class StubRepository(ProjectRepository):
            def find_all(self):
                return []

            def find_by_id(self, project_id):
                return None

        stub = StubRepository()
        assert stub.find_all() == []
        assert stub.find_by_id(uuid.uuid4()) is None
