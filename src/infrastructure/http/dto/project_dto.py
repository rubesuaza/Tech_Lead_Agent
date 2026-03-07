"""
DTOs for ProjectMaster and UseCase. Maps domain models to API response schema.
"""
from __future__ import annotations
from uuid import UUID
from pydantic import BaseModel, ConfigDict

from src.domain.models import ProjectMaster


class UseCaseDTO(BaseModel):
    """API representation of a use case item."""

    code: str
    title: str
    complexity: str

    model_config = ConfigDict(frozen=True)


class ProjectMasterDTO(BaseModel):
    """API representation of ProjectMaster (view_project_master_context)."""

    project_id: UUID
    project_code: str
    project_name: str
    stack_tecnologico: dict[str, object]
    coding_standards: tuple[str, ...]
    patrones_diseno: tuple[str, ...]
    estructura_directorios: str
    reglas_dominio: str
    checklist: str
    lista_casos_uso: tuple[UseCaseDTO, ...]

    model_config = ConfigDict(frozen=True)

    @classmethod
    def from_domain(cls, project: ProjectMaster) -> ProjectMasterDTO:
        """Maps domain ProjectMaster to DTO."""
        return cls(
            project_id=project.project_id,
            project_code=project.project_code,
            project_name=project.project_name,
            stack_tecnologico=dict(project.stack_tecnologico),
            coding_standards=project.coding_standards,
            patrones_diseno=project.patrones_diseno,
            estructura_directorios=project.estructura_directorios,
            reglas_dominio=project.reglas_dominio,
            checklist=project.checklist,
            lista_casos_uso=tuple(
                UseCaseDTO(code=uc.code, title=uc.title, complexity=uc.complexity)
                for uc in project.lista_casos_uso
            ),
        )
