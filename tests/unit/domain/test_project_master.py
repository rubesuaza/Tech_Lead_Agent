"""Unit tests for ProjectMaster aggregate: invariants and API."""
import pytest
from uuid import uuid4

from src.domain.exceptions import IncompleteMetadataException
from src.domain.models import ProjectMaster, UseCase


def _valid_project_master_kwargs(**overrides):
    base = {
        "project_id": uuid4(),
        "project_code": "PRJ-001",
        "project_name": "Order Management",
        "stack_tecnologico": {"language": "Python", "framework": "FastAPI"},
        "coding_standards": ["PEP8"],
        "patrones_diseno": [],
        "estructura_directorios": "# Directory structure",
        "reglas_dominio": "# Domain rules",
        "checklist": "# Checklist",
        "lista_casos_uso": (UseCase("UC01", "Create", "medium"),),
    }
    base.update(overrides)
    return base


class TestProjectMasterInvariants:
    """Business rules from DOMAIN DEFINITION: mandatory content and coding_standards."""

    def test_creates_when_all_invariants_met(self):
        pm = ProjectMaster(**_valid_project_master_kwargs())
        assert pm.project_code == "PRJ-001"
        assert len(pm.coding_standards) >= 1
        assert pm.estructura_directorios.strip() != ""
        assert pm.reglas_dominio.strip() != ""

    def test_raises_when_estructura_directorios_empty(self):
        with pytest.raises(IncompleteMetadataException) as exc_info:
            ProjectMaster(
                **_valid_project_master_kwargs(estructura_directorios="")
            )
        assert "estructura_directorios" in exc_info.value.missing_field or "estructura" in str(exc_info.value).lower()

    def test_raises_when_reglas_dominio_empty(self):
        with pytest.raises(IncompleteMetadataException):
            ProjectMaster(
                **_valid_project_master_kwargs(reglas_dominio="")
            )

    def test_raises_when_reglas_dominio_none(self):
        with pytest.raises(IncompleteMetadataException):
            ProjectMaster(
                **_valid_project_master_kwargs(reglas_dominio=None)  # type: ignore
            )

    def test_raises_when_coding_standards_empty(self):
        with pytest.raises(IncompleteMetadataException) as exc_info:
            ProjectMaster(
                **_valid_project_master_kwargs(coding_standards=[])
            )
        assert "coding_standards" in str(exc_info.value).lower() or exc_info.value.missing_field == "coding_standards"

    def test_raises_when_coding_standards_empty_tuple(self):
        with pytest.raises(IncompleteMetadataException):
            ProjectMaster(
                **_valid_project_master_kwargs(coding_standards=())
            )

    def test_is_immutable(self):
        pm = ProjectMaster(**_valid_project_master_kwargs())
        with pytest.raises(AttributeError):
            pm.project_code = "other"  # type: ignore
