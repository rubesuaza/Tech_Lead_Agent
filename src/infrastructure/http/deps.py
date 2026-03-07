"""
Dependency provider for HTTP layer. Main app sets the use case instance at bootstrap.
"""
from src.application.ports.input import ProjectQueryUseCase

_use_case: ProjectQueryUseCase | None = None


def set_project_query_use_case(use_case: ProjectQueryUseCase) -> None:
    """Called at startup to inject the application service."""
    global _use_case
    _use_case = use_case


def get_project_query_use_case() -> ProjectQueryUseCase:
    """FastAPI dependency: returns the configured use case."""
    if _use_case is None:
        raise RuntimeError("ProjectQueryUseCase not configured; call set_project_query_use_case at startup")
    return _use_case
