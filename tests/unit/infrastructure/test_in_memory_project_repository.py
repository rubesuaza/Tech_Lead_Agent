"""Unit tests for InMemoryProjectRepository adapter."""
import pytest
from uuid import uuid4

from src.domain.models import ProjectMaster, UseCase
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


class TestInMemoryProjectRepository:
    """Contract fulfillment: find_all and find_by_id."""

    def test_find_all_empty(self):
        repo = InMemoryProjectRepository()
        assert repo.find_all() == []

    def test_find_all_returns_initial(self):
        p1 = _valid_project_master(project_code="A")
        p2 = _valid_project_master(project_code="B")
        repo = InMemoryProjectRepository(initial=[p1, p2])
        result = repo.find_all()
        assert len(result) == 2
        assert {r.project_code for r in result} == {"A", "B"}

    def test_find_by_id_returns_none_when_missing(self):
        repo = InMemoryProjectRepository()
        assert repo.find_by_id(uuid4()) is None

    def test_find_by_id_returns_project(self):
        p = _valid_project_master()
        repo = InMemoryProjectRepository(initial=[p])
        assert repo.find_by_id(p.project_id) is p

    def test_add_then_find(self):
        repo = InMemoryProjectRepository()
        p = _valid_project_master()
        repo.add(p)
        assert repo.find_by_id(p.project_id) is p
        assert len(repo.find_all()) == 1
