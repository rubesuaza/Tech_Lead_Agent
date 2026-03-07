"""
Value objects for the project master context. Immutable; only standard library.
"""
from dataclasses import dataclass
from typing import Any

from src.domain.exceptions.domain_exceptions import IncompleteMetadataException


@dataclass(frozen=True)
class UseCase:
    """Represents an item in lista_casos_uso: code, title, complexity."""

    code: str
    title: str
    complexity: str


@dataclass(frozen=True)
class InfrastructureSpecs:
    """Encapsulates db_engines, api_types, and messaging."""

    db_engines: tuple[str, ...]
    api_types: tuple[str, ...]
    messaging: tuple[str, ...]


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise IncompleteMetadataException(field_name)


@dataclass(frozen=True)
class ProjectDefinition:
    """
    Markdown contents for structure, domain rules, and checklist.
    Invariant: estructura_directorios and reglas_dominio must not be empty.
    """

    estructura_directorios: str
    reglas_dominio: str
    checklist: str

    def __post_init__(self) -> None:
        _require_non_empty(self.estructura_directorios, "estructura_directorios")
        _require_non_empty(self.reglas_dominio, "reglas_dominio")
