"""
Dependency provider for HTTP layer. Main app sets the use case instance at bootstrap.
Uses a holder object instead of a global for testability and explicit dependency scope.
"""
from src.application.ports.input import ProjectQueryUseCase


class _UseCaseHolder:
    """Holds the configured use case instance (avoids module-level global)."""

    instance: ProjectQueryUseCase | None = None


_holder = _UseCaseHolder()


def set_project_query_use_case(use_case: ProjectQueryUseCase) -> None:
    """Called at startup to inject the application service."""
    _holder.instance = use_case


def get_project_query_use_case() -> ProjectQueryUseCase:
    """FastAPI dependency: returns the configured use case."""
    if _holder.instance is None:
        raise RuntimeError("ProjectQueryUseCase not configured; call set_project_query_use_case at startup")
    return _holder.instance
