"""
ProjectMaster aggregate root.
Read-only consolidated view of project metadata (maps to view_project_master_context).
"""

from dataclasses import dataclass
from uuid import UUID
from typing import Any

from domain.exceptions import IncompleteMetadataException
from domain.models.value_objects import UseCase


@dataclass(frozen=True)
class ProjectMaster:
    """
    Aggregate root: project metadata.
    Invariant: directory_structure_definition (estructura_directorios) must not be null.
    """

    project_id: UUID
    project_code: str
    project_name: str
    stack_tecnologico: dict[str, Any]
    estructura_directorios: str | None
    reglas_dominio: str | None
    checklist: str | None
    coding_standards: tuple[str, ...]
    patrones_diseno: tuple[str, ...]
    lista_casos_uso: tuple[UseCase, ...]

    def __post_init__(self):
        if self.estructura_directorios is None:
            raise IncompleteMetadataException(
                "ProjectMaster is invalid: directory_structure_definition (estructura_directorios) must not be null"
            )
        # Normalize lists to tuples for immutability
        if not isinstance(self.coding_standards, tuple):
            object.__setattr__(self, "coding_standards", tuple(self.coding_standards or ()))
        if not isinstance(self.patrones_diseno, tuple):
            object.__setattr__(self, "patrones_diseno", tuple(self.patrones_diseno or ()))
        if not isinstance(self.lista_casos_uso, tuple):
            ucs = self.lista_casos_uso or []
            object.__setattr__(
                self,
                "lista_casos_uso",
                tuple(uc if isinstance(uc, UseCase) else UseCase(**uc) for uc in ucs),
            )
