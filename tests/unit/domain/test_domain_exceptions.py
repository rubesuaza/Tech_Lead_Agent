"""Unit tests for domain exceptions (business rule failures)."""
import pytest

from src.domain.exceptions import ProjectNotFoundException, IncompleteMetadataException


class TestProjectNotFoundException:
    def test_raises_with_identifier(self):
        exc = ProjectNotFoundException("PRJ-001")
        assert exc.identifier == "PRJ-001"
        assert "PRJ-001" in str(exc)

    def test_raises_with_custom_message(self):
        exc = ProjectNotFoundException("x", message="Custom message")
        assert exc.identifier == "x"
        assert str(exc) == "Custom message"


class TestIncompleteMetadataException:
    def test_raises_with_missing_field(self):
        exc = IncompleteMetadataException("reglas_dominio")
        assert exc.missing_field == "reglas_dominio"
        assert "reglas_dominio" in str(exc)

    def test_raises_with_custom_message(self):
        exc = IncompleteMetadataException("estructura_directorios", message="Custom")
        assert exc.missing_field == "estructura_directorios"
        assert str(exc) == "Custom"
