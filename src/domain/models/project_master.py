from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Tuple
from uuid import UUID

from src.domain.exceptions import IncompleteMetadataException


@dataclass(frozen=True)
class InfrastructureSpecs:
    db_engines: Tuple[str, ...]
    api_types: Tuple[str, ...]
    messaging: Tuple[str, ...]


@dataclass(frozen=True)
class UseCase:
    code: str
    title: str
    complexity: str


@dataclass(frozen=True)
class ProjectMaster:
    project_id: UUID
    project_code: str
    project_name: str
    stack_tecnologico: Mapping[str, Any]
    coding_standards: Tuple[str, ...]
    patrones_diseno: Tuple[str, ...]
    estructura_directorios: Mapping[str, Any]
    reglas_dominio: Tuple[str, ...]
    checklist: Tuple[str, ...]

    def __post_init__(self) -> None:
        if self.estructura_directorios is None:
            raise IncompleteMetadataException(
                "La definición de estructura_directorios no puede ser nula."
            )

        if not self.reglas_dominio:
            raise IncompleteMetadataException(
                "Las reglas_dominio no pueden estar vacías."
            )

