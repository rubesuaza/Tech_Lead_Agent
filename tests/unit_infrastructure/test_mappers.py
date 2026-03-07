"""Unit tests for persistence mappers (DB row -> domain)."""

import sys
import uuid
from pathlib import Path

_src = Path(__file__).resolve().parents[2] / "src"
if _src.exists():
    _src_str = str(_src)
    if _src_str in sys.path:
        sys.path.remove(_src_str)
    sys.path.insert(0, _src_str)

import pytest

from domain.models import ProjectMaster
from domain.models.value_objects import UseCase
from infrastructure.persistence.mappers import row_to_project_master


class TestRowToProjectMaster:
    def test_maps_full_row_to_project_master(self):
        project_id = uuid.uuid4()
        row = {
            "project_id": str(project_id),
            "project_code": "PRJ-01",
            "project_name": "Test Project",
            "stack_tecnologico": '{"backend": "python"}',
            "estructura_directorios": "/app",
            "reglas_dominio": "rules",
            "checklist": "[]",
            "coding_standards": '["pep8"]',
            "patrones_diseno": '["hexagonal"]',
            "lista_casos_uso": '[{"code": "UC1", "title": "Case 1", "complexity": "medium"}]',
        }
        got = row_to_project_master(row)
        assert isinstance(got, ProjectMaster)
        assert got.project_id == project_id
        assert got.project_code == "PRJ-01"
        assert got.project_name == "Test Project"
        assert got.stack_tecnologico == {"backend": "python"}
        assert got.estructura_directorios == "/app"
        assert got.coding_standards == ("pep8",)
        assert got.patrones_diseno == ("hexagonal",)
        assert len(got.lista_casos_uso) == 1
        assert got.lista_casos_uso[0] == UseCase(code="UC1", title="Case 1", complexity="medium")

    def test_estructura_directorios_required_for_domain_invariant(self):
        row = {
            "project_id": str(uuid.uuid4()),
            "project_code": "X",
            "project_name": "Y",
            "stack_tecnologico": {},
            "estructura_directorios": "required",
            "reglas_dominio": None,
            "checklist": None,
            "coding_standards": [],
            "patrones_diseno": [],
            "lista_casos_uso": [],
        }
        got = row_to_project_master(row)
        assert got.estructura_directorios == "required"

    def test_missing_estructura_directorios_raises_incomplete_metadata(self):
        from domain.exceptions import IncompleteMetadataException
        row = {
            "project_id": str(uuid.uuid4()),
            "project_code": "X",
            "project_name": "Y",
            "stack_tecnologico": {},
            "estructura_directorios": None,
            "reglas_dominio": None,
            "checklist": None,
            "coding_standards": [],
            "patrones_diseno": [],
            "lista_casos_uso": [],
        }
        with pytest.raises(IncompleteMetadataException):
            row_to_project_master(row)
