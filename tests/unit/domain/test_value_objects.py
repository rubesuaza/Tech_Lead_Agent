"""Unit tests for value objects: UseCase, InfrastructureSpecs, ProjectDefinition."""
import pytest

from src.domain.exceptions import IncompleteMetadataException
from src.domain.models import UseCase, InfrastructureSpecs, ProjectDefinition


class TestUseCase:
    def test_creates_with_code_title_complexity(self):
        vo = UseCase(code="UC01", title="Create Project", complexity="medium")
        assert vo.code == "UC01"
        assert vo.title == "Create Project"
        assert vo.complexity == "medium"

    def test_is_immutable(self):
        vo = UseCase(code="UC01", title="T", complexity="low")
        with pytest.raises(AttributeError):
            vo.code = "UC02"  # type: ignore


class TestInfrastructureSpecs:
    def test_creates_with_db_api_messaging(self):
        vo = InfrastructureSpecs(
            db_engines=("postgresql",),
            api_types=("REST",),
            messaging=(),
        )
        assert vo.db_engines == ("postgresql",)
        assert vo.api_types == ("REST",)
        assert vo.messaging == ()


class TestProjectDefinition:
    def test_creates_when_estructura_and_reglas_non_empty(self):
        vo = ProjectDefinition(
            estructura_directorios="# Structure",
            reglas_dominio="# Rules",
            checklist="",
        )
        assert vo.estructura_directorios == "# Structure"
        assert vo.reglas_dominio == "# Rules"

    def test_raises_when_estructura_directorios_empty(self):
        with pytest.raises(IncompleteMetadataException) as exc_info:
            ProjectDefinition(
                estructura_directorios="",
                reglas_dominio="# Rules",
                checklist="",
            )
        assert exc_info.value.missing_field == "estructura_directorios"

    def test_raises_when_estructura_directorios_whitespace_only(self):
        with pytest.raises(IncompleteMetadataException):
            ProjectDefinition(
                estructura_directorios="   ",
                reglas_dominio="# Rules",
                checklist="",
            )

    def test_raises_when_reglas_dominio_empty(self):
        with pytest.raises(IncompleteMetadataException) as exc_info:
            ProjectDefinition(
                estructura_directorios="# Structure",
                reglas_dominio="",
                checklist="",
            )
        assert exc_info.value.missing_field == "reglas_dominio"
