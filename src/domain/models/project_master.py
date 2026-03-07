"""
Aggregate root: read-only consolidated view of project metadata.
Invariants: estructura_directorios and reglas_dominio non-empty; at least one coding_standard.
Only standard library; no external dependencies.
"""
from dataclasses import dataclass
from uuid import UUID
from typing import Any

from src.domain.exceptions.domain_exceptions import IncompleteMetadataException
from src.domain.models.value_objects import UseCase


def _require_non_empty_str(value: str | None, field_name: str) -> str:
    if value is None or not str(value).strip():
        raise IncompleteMetadataException(field_name)
    return str(value).strip()


def _require_at_least_one(value: list[Any] | tuple[Any, ...] | None, field_name: str) -> None:
    if not value or len(value) == 0:
        raise IncompleteMetadataException(
            field_name,
            message=f"At least one entry required in '{field_name}' for Guardian verification.",
        )


@dataclass(frozen=True)
class ProjectMaster:
    """
    Read-only aggregate for view_project_master_context.
    Identity: project_id. Includes definitions (estructura_directorios, reglas_dominio, checklist).
    """

    project_id: UUID
    project_code: str
    project_name: str
    stack_tecnologico: dict[str, Any]
    coding_standards: tuple[str, ...]
    patrones_diseno: tuple[str, ...]
    estructura_directorios: str
    reglas_dominio: str
    checklist: str
    lista_casos_uso: tuple[UseCase, ...]

    def __post_init__(self) -> None:
        # Mandatory content: structure and domain rules must not be empty
        _require_non_empty_str(self.estructura_directorios, "estructura_directorios")
        _require_non_empty_str(self.reglas_dominio, "reglas_dominio")
        # At least one coding standard required for Guardian verification
        _require_at_least_one(self.coding_standards, "coding_standards")
