"""Unit tests for domain exceptions."""

import sys
from pathlib import Path

# tests/domain/test_*.py -> parent.parent.parent = project root
_src = Path(__file__).resolve().parents[2] / "src"
if _src.exists() and str(_src) not in sys.path:
    sys.path.insert(0, str(_src))

import pytest

from domain.exceptions import ProjectNotFoundException, IncompleteMetadataException


class TestProjectNotFoundException:
    def test_raises_with_default_message(self):
        with pytest.raises(ProjectNotFoundException) as exc_info:
            raise ProjectNotFoundException()
        assert str(exc_info.value) == "Project not found"
        assert exc_info.value.project_id is None

    def test_raises_with_custom_message_and_project_id(self):
        with pytest.raises(ProjectNotFoundException) as exc_info:
            raise ProjectNotFoundException("Project PRJ-999 not found", project_id="PRJ-999")
        assert str(exc_info.value) == "Project PRJ-999 not found"
        assert exc_info.value.project_id == "PRJ-999"


class TestIncompleteMetadataException:
    def test_raises_with_default_message(self):
        with pytest.raises(IncompleteMetadataException) as exc_info:
            raise IncompleteMetadataException()
        assert "Incomplete metadata" in str(exc_info.value)

    def test_raises_with_custom_message(self):
        with pytest.raises(IncompleteMetadataException) as exc_info:
            raise IncompleteMetadataException("reglas_dominio is missing")
        assert str(exc_info.value) == "reglas_dominio is missing"
