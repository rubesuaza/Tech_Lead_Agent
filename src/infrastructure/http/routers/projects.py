"""
HTTP adapter: exposes project query use case via REST.
Depends on the input port (ProjectQueryUseCase); no business logic.
"""
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException

from src.application.ports.input import ProjectQueryUseCase
from src.infrastructure.http.dto import ProjectMasterDTO
from src.infrastructure.http.deps import get_project_query_use_case


router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("", response_model=list[ProjectMasterDTO])
def list_projects(
    use_case: ProjectQueryUseCase = Depends(get_project_query_use_case),
) -> list[ProjectMasterDTO]:
    """Returns all projects from the master view."""
    projects = use_case.get_all_projects()
    return [ProjectMasterDTO.from_domain(p) for p in projects]


@router.get("/{project_id}", response_model=ProjectMasterDTO)
def get_project(
    project_id: UUID,
    use_case: ProjectQueryUseCase = Depends(get_project_query_use_case),
) -> ProjectMasterDTO:
    """Returns a single project by id."""
    project = use_case.get_project_by_id(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return ProjectMasterDTO.from_domain(project)
