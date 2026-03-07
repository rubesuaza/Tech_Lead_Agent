"""Unit tests for PostgresProjectRepository (adapter implements port)."""

import sys
import uuid
from pathlib import Path

_src = Path(__file__).resolve().parents[2] / "src"
if _src.exists():
    _src_str = str(_src)
    if _src_str in sys.path:
        sys.path.remove(_src_str)
    sys.path.insert(0, _src_str)

from application.ports.output.project_repository import ProjectRepository
from infrastructure.persistence.postgres_project_repository import PostgresProjectRepository


class TestPostgresProjectRepository:
    def test_implements_project_repository_port(self):
        repo = PostgresProjectRepository()
        assert isinstance(repo, ProjectRepository)

    def test_has_find_all_and_find_by_id(self):
        assert hasattr(PostgresProjectRepository, "find_all")
        assert hasattr(PostgresProjectRepository, "find_by_id")
