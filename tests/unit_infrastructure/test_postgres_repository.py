"""Unit tests for PostgresProjectRepository (adapter implements port)."""

import sys
import uuid
from pathlib import Path
from unittest.mock import MagicMock, patch

_src = Path(__file__).resolve().parents[2] / "src"
if _src.exists():
    _src_str = str(_src)
    if _src_str in sys.path:
        sys.path.remove(_src_str)
    sys.path.insert(0, _src_str)

from domain.ports.project_repository import ProjectRepository
from domain.models import ProjectMaster
from infrastructure.config import DatabaseSettings
from infrastructure.persistence.postgres_project_repository import PostgresProjectRepository


class TestPostgresProjectRepository:
    def test_implements_project_repository_port(self):
        repo = PostgresProjectRepository()
        assert isinstance(repo, ProjectRepository)

    def test_has_find_all_and_find_by_id(self):
        assert hasattr(PostgresProjectRepository, "find_all")
        assert hasattr(PostgresProjectRepository, "find_by_id")

    def test_find_all_returns_mapped_domain_models(self):
        project_id = uuid.uuid4()
        mock_row = (
            str(project_id),
            "PRJ-01",
            "Test Project",
            '{"backend": "python"}',
            "/app",
            "rules",
            "[]",
            '["pep8"]',
            '["hexagonal"]',
            '[]',
        )
        columns = (
            "project_id", "project_code", "project_name", "stack_tecnologico",
            "estructura_directorios", "reglas_dominio", "checklist",
            "coding_standards", "patrones_diseno", "lista_casos_uso",
        )
        mock_result = MagicMock()
        mock_result.keys.return_value = columns
        mock_result.fetchall.return_value = [mock_row]

        mock_conn = MagicMock()
        mock_conn.execute.return_value = mock_result
        mock_conn.__enter__ = MagicMock(return_value=mock_conn)
        mock_conn.__exit__ = MagicMock(return_value=None)

        mock_engine = MagicMock()
        mock_engine.connect.return_value = mock_conn

        settings = DatabaseSettings(host="127.0.0.1", port=5432, name="test", user="u", password="p")
        with patch("infrastructure.persistence.postgres_project_repository.create_engine", return_value=mock_engine):
            repo = PostgresProjectRepository(settings=settings)
            repo._engine = mock_engine
            result = repo.find_all()

        assert len(result) == 1
        assert isinstance(result[0], ProjectMaster)
        assert result[0].project_id == project_id
        assert result[0].project_code == "PRJ-01"
        assert result[0].project_name == "Test Project"
        assert result[0].stack_tecnologico == {"backend": "python"}
        assert result[0].estructura_directorios == "/app"

    def test_find_all_empty_result_returns_empty_list(self):
        mock_result = MagicMock()
        mock_result.keys.return_value = []
        mock_result.fetchall.return_value = []

        mock_conn = MagicMock()
        mock_conn.execute.return_value = mock_result
        mock_conn.__enter__ = MagicMock(return_value=mock_conn)
        mock_conn.__exit__ = MagicMock(return_value=None)

        mock_engine = MagicMock()
        mock_engine.connect.return_value = mock_conn

        settings = DatabaseSettings(host="127.0.0.1", port=5432, name="test", user="u", password="p")
        with patch("infrastructure.persistence.postgres_project_repository.create_engine", return_value=mock_engine):
            repo = PostgresProjectRepository(settings=settings)
            repo._engine = mock_engine
            result = repo.find_all()

        assert result == []

    def test_find_by_id_returns_mapped_domain_model(self):
        project_id = uuid.uuid4()
        mock_row = (
            str(project_id),
            "PRJ-02",
            "Other Project",
            '{}',
            "/other",
            None,
            None,
            '[]',
            '[]',
            '[]',
        )
        columns = (
            "project_id", "project_code", "project_name", "stack_tecnologico",
            "estructura_directorios", "reglas_dominio", "checklist",
            "coding_standards", "patrones_diseno", "lista_casos_uso",
        )
        mock_result = MagicMock()
        mock_result.keys.return_value = columns
        mock_result.fetchone.return_value = mock_row

        mock_conn = MagicMock()
        mock_conn.execute.return_value = mock_result
        mock_conn.__enter__ = MagicMock(return_value=mock_conn)
        mock_conn.__exit__ = MagicMock(return_value=None)

        mock_engine = MagicMock()
        mock_engine.connect.return_value = mock_conn

        settings = DatabaseSettings(host="127.0.0.1", port=5432, name="test", user="u", password="p")
        with patch("infrastructure.persistence.postgres_project_repository.create_engine", return_value=mock_engine):
            repo = PostgresProjectRepository(settings=settings)
            repo._engine = mock_engine
            result = repo.find_by_id(project_id)

        assert result is not None
        assert isinstance(result, ProjectMaster)
        assert result.project_id == project_id
        assert result.project_code == "PRJ-02"
        assert result.estructura_directorios == "/other"

    def test_find_by_id_not_found_returns_none(self):
        mock_result = MagicMock()
        mock_result.fetchone.return_value = None

        mock_conn = MagicMock()
        mock_conn.execute.return_value = mock_result
        mock_conn.__enter__ = MagicMock(return_value=mock_conn)
        mock_conn.__exit__ = MagicMock(return_value=None)

        mock_engine = MagicMock()
        mock_engine.connect.return_value = mock_conn

        settings = DatabaseSettings(host="127.0.0.1", port=5432, name="test", user="u", password="p")
        with patch("infrastructure.persistence.postgres_project_repository.create_engine", return_value=mock_engine):
            repo = PostgresProjectRepository(settings=settings)
            repo._engine = mock_engine
            result = repo.find_by_id(uuid.uuid4())

        assert result is None
