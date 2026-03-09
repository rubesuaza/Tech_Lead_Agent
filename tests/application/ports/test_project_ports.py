import inspect

from src.application.ports.project_query_use_case import ProjectQueryUseCase
from src.application.ports.project_repository import ProjectRepository
from src.domain.models.project_master import ProjectMaster


def test_project_query_use_case_is_abstract():
    assert inspect.isabstract(ProjectQueryUseCase)


def test_project_query_use_case_contract():
    methods = {
        name: func
        for name, func in inspect.getmembers(ProjectQueryUseCase, predicate=inspect.isfunction)
    }

    assert "get_all_projects" in methods
    assert "get_project_by_id" in methods

    sig_all = inspect.signature(methods["get_all_projects"])
    sig_by_id = inspect.signature(methods["get_project_by_id"])

    # self only
    assert list(sig_all.parameters.keys()) == ["self"]
    # self, id
    assert list(sig_by_id.parameters.keys()) == ["self", "id"]


def test_project_repository_is_abstract():
    assert inspect.isabstract(ProjectRepository)


def test_project_repository_contract():
    methods = {
        name: func
        for name, func in inspect.getmembers(ProjectRepository, predicate=inspect.isfunction)
    }

    assert "find_all" in methods
    assert "find_by_id" in methods

    sig_all = inspect.signature(methods["find_all"])
    sig_by_id = inspect.signature(methods["find_by_id"])

    # self only
    assert list(sig_all.parameters.keys()) == ["self"]
    # self, id
    assert list(sig_by_id.parameters.keys()) == ["self", "id"]


def test_port_type_hints_reference_project_master():
    get_all = ProjectQueryUseCase.get_all_projects
    find_all = ProjectRepository.find_all

    assert ProjectMaster.__name__ in str(get_all.__annotations__.get("return", ""))
    assert ProjectMaster.__name__ in str(find_all.__annotations__.get("return", ""))

