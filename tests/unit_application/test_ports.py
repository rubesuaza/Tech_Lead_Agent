"""Unit tests for application ports (interfaces)."""

import sys
import uuid
from pathlib import Path

# tests/application/test_*.py -> parents[2] = project root
_src = Path(__file__).resolve().parents[2] / "src"
if _src.exists():
    _src_str = str(_src)
    if _src_str in sys.path:
        sys.path.remove(_src_str)
    sys.path.insert(0, _src_str)

import pytest

from application.ports.input.project_query_use_case import ProjectQueryUseCase
from domain.ports.project_repository import ProjectRepository
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

    def test_stub_get_project_by_id_raises_not_implemented_error(self):
        class StubQueryUseCase(ProjectQueryUseCase):
            def get_all_projects(self):
                return []

            def get_project_by_id(self, project_id):
                raise NotImplementedError("Not implemented")

        stub = StubQueryUseCase()
        with pytest.raises(NotImplementedError, match="Not implemented"):
            stub.get_project_by_id(uuid.uuid4())

    def test_stub_get_all_projects_happy_path_returns_mock_data(self):
        mock_list = [{"project_id": str(uuid.uuid4()), "project_code": "P1"}]

        class StubQueryUseCase(ProjectQueryUseCase):
            def get_all_projects(self):
                return mock_list

            def get_project_by_id(self, project_id):
                raise NotImplementedError

        stub = StubQueryUseCase()
        assert stub.get_all_projects() == mock_list

    def test_stub_get_project_by_id_happy_path_returns_mock_master(self):
        project_id = uuid.uuid4()
        mock_master = ProjectMaster(
            project_id=project_id,
            project_code="P1",
            project_name="Proj",
            stack_tecnologico={},
            estructura_directorios="/",
            reglas_dominio=None,
            checklist=None,
            coding_standards=(),
            patrones_diseno=(),
            lista_casos_uso=(),
        )

        class StubQueryUseCase(ProjectQueryUseCase):
            def get_all_projects(self):
                return []

            def get_project_by_id(self, pid):
                return mock_master

        stub = StubQueryUseCase()
        assert stub.get_project_by_id(project_id) is mock_master
        assert stub.get_project_by_id(project_id).project_code == "P1"


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

    def test_stub_find_all_happy_path_returns_mock_list(self):
        mock_list = [
            ProjectMaster(
                project_id=uuid.uuid4(),
                project_code="P1",
                project_name="Proj",
                stack_tecnologico={},
                estructura_directorios="/",
                reglas_dominio=None,
                checklist=None,
                coding_standards=(),
                patrones_diseno=(),
                lista_casos_uso=(),
            )
        ]

        class StubRepository(ProjectRepository):
            def find_all(self):
                return mock_list

            def find_by_id(self, project_id):
                return None

        stub = StubRepository()
        assert stub.find_all() == mock_list
        assert len(stub.find_all()) == 1
        assert stub.find_all()[0].project_code == "P1"

    def test_stub_find_by_id_happy_path_returns_mock_master(self):
        project_id = uuid.uuid4()
        mock_master = ProjectMaster(
            project_id=project_id,
            project_code="P1",
            project_name="Proj",
            stack_tecnologico={},
            estructura_directorios="/",
            reglas_dominio=None,
            checklist=None,
            coding_standards=(),
            patrones_diseno=(),
            lista_casos_uso=(),
        )

        class StubRepository(ProjectRepository):
            def find_all(self):
                return []

            def find_by_id(self, pid):
                return mock_master if pid == project_id else None

        stub = StubRepository()
        assert stub.find_by_id(project_id) is mock_master
        assert stub.find_by_id(project_id).project_code == "P1"
        assert stub.find_by_id(uuid.uuid4()) is None
