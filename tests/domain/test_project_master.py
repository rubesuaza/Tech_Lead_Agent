"""Unit tests for ProjectMaster aggregate root."""

import sys
import uuid
from pathlib import Path

_src = Path(__file__).resolve().parents[2] / "src"
if _src.exists() and str(_src) not in sys.path:
    sys.path.insert(0, str(_src))

import pytest

from domain.exceptions import IncompleteMetadataException
from domain.models.project_master import ProjectMaster
from domain.models.value_objects import UseCase


class TestProjectMaster:
    def test_creation_with_required_attributes(self):
        pid = uuid.uuid4()
        pm = ProjectMaster(
            project_id=pid,
            project_code="PRJ-001",
            project_name="Order Management",
            stack_tecnologico={"language": "Python"},
            estructura_directorios="# Dir structure",
            reglas_dominio="# Rules",
            checklist="# Checklist",
            coding_standards=[],
            patrones_diseno=[],
            lista_casos_uso=[],
        )
        assert pm.project_id == pid
        assert pm.project_code == "PRJ-001"
        assert pm.project_name == "Order Management"
        assert pm.estructura_directorios == "# Dir structure"

    def test_invalid_when_estructura_directorios_is_none_raises(self):
        with pytest.raises(IncompleteMetadataException) as exc_info:
            ProjectMaster(
                project_id=uuid.uuid4(),
                project_code="PRJ-001",
                project_name="Test",
                stack_tecnologico={},
                estructura_directorios=None,
                reglas_dominio="",
                checklist="",
                coding_standards=[],
                patrones_diseno=[],
                lista_casos_uso=[],
            )
        assert "directory_structure" in str(exc_info.value).lower() or "estructura" in str(exc_info.value).lower()

    def test_immutability(self):
        pm = ProjectMaster(
            project_id=uuid.uuid4(),
            project_code="PRJ-001",
            project_name="Test",
            stack_tecnologico={},
            estructura_directorios="# Struct",
            reglas_dominio="",
            checklist="",
            coding_standards=[],
            patrones_diseno=[],
            lista_casos_uso=[],
        )
        with pytest.raises(AttributeError):
            pm.project_code = "PRJ-002"

    def test_lista_casos_uso_holds_use_case_objects(self):
        uc = UseCase(code="UC01", title="Create", complexity="high")
        pm = ProjectMaster(
            project_id=uuid.uuid4(),
            project_code="PRJ-001",
            project_name="Test",
            stack_tecnologico={},
            estructura_directorios="# Struct",
            reglas_dominio="",
            checklist="",
            coding_standards=[],
            patrones_diseno=[],
            lista_casos_uso=[uc],
        )
        assert len(pm.lista_casos_uso) == 1
        assert pm.lista_casos_uso[0].code == "UC01"
