import uuid

import pytest
from dataclasses import FrozenInstanceError

from src.domain.exceptions import IncompleteMetadataException
from src.domain.models.project_master import (
    InfrastructureSpecs,
    ProjectMaster,
    UseCase,
)


def _make_valid_project_master(**overrides) -> ProjectMaster:
    base = {
        "project_id": uuid.uuid4(),
        "project_code": "TECH-001",
        "project_name": "Tech Lead Agent",
        "stack_tecnologico": {"backend": "python", "framework": "fastapi"},
        "coding_standards": ("pep8", "pep257"),
        "patrones_diseno": ("hexagonal", "ddd"),
        "estructura_directorios": {"src": ["domain", "application", "infrastructure"]},
        "reglas_dominio": ("regla_1",),
        "checklist": ("item_1", "item_2"),
    }
    base.update(overrides)
    return ProjectMaster(**base)


def test_project_master_valid_creation():
    project = _make_valid_project_master()

    assert project.project_code == "TECH-001"
    assert project.project_name == "Tech Lead Agent"
    assert project.stack_tecnologico["backend"] == "python"
    assert "domain" in project.estructura_directorios["src"]


def test_project_master_is_immutable():
    project = _make_valid_project_master()

    with pytest.raises(FrozenInstanceError):
        project.project_name = "Otro nombre"


def test_project_master_requires_directory_structure_definition():
    with pytest.raises(IncompleteMetadataException):
        _make_valid_project_master(estructura_directorios=None)


def test_project_master_requires_reglas_dominio():
    with pytest.raises(IncompleteMetadataException):
        _make_valid_project_master(reglas_dominio=())


def test_infrastructure_specs_is_immutable():
    specs = InfrastructureSpecs(
        db_engines=("postgresql",),
        api_types=("rest",),
        messaging=("kafka",),
    )

    assert specs.db_engines == ("postgresql",)

    with pytest.raises(FrozenInstanceError):
        specs.db_engines = ()


def test_use_case_is_immutable():
    use_case = UseCase(code="UC-001", title="Listar proyectos", complexity="M")

    assert use_case.code == "UC-001"
    assert use_case.title == "Listar proyectos"

    with pytest.raises(FrozenInstanceError):
        use_case.title = "Otro título"

