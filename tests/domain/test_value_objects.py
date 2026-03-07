"""Unit tests for domain value objects (UseCase, InfrastructureSpecs)."""

import sys
from pathlib import Path

_src = Path(__file__).resolve().parents[2] / "src"
if _src.exists() and str(_src) not in sys.path:
    sys.path.insert(0, str(_src))

import pytest

from domain.models.value_objects import UseCase, InfrastructureSpecs


class TestUseCase:
    def test_creation_with_required_attributes(self):
        uc = UseCase(code="UC01", title="Create Project", complexity="high")
        assert uc.code == "UC01"
        assert uc.title == "Create Project"
        assert uc.complexity == "high"

    def test_immutability(self):
        uc = UseCase(code="UC01", title="Create Project", complexity="medium")
        with pytest.raises(AttributeError):
            uc.code = "UC02"

    def test_equality_by_value(self):
        uc1 = UseCase(code="UC01", title="Create Project", complexity="low")
        uc2 = UseCase(code="UC01", title="Create Project", complexity="low")
        assert uc1 == uc2


class TestInfrastructureSpecs:
    def test_creation_with_lists(self):
        spec = InfrastructureSpecs(
            db_engines=["postgresql"],
            api_types=["REST"],
            messaging=["redis"],
        )
        assert spec.db_engines == ("postgresql",)
        assert spec.api_types == ("REST",)
        assert spec.messaging == ("redis",)

    def test_immutability(self):
        spec = InfrastructureSpecs(db_engines=[], api_types=[], messaging=[])
        with pytest.raises(AttributeError):
            spec.db_engines = ["mysql"]

    def test_stores_sequences_as_tuples(self):
        spec = InfrastructureSpecs(
            db_engines=["pg", "mysql"],
            api_types=["REST", "GraphQL"],
            messaging=[],
        )
        assert isinstance(spec.db_engines, tuple)
        assert spec.db_engines == ("pg", "mysql")
