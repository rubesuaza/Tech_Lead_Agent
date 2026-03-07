"""
Application bootstrap: builds FastAPI app and wires dependencies.
Infrastructure adapters (repository, HTTP) are configured here.
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.application.services import ProjectQueryService
from src.infrastructure.http.deps import set_project_query_use_case
from src.infrastructure.http.routers import projects
from src.infrastructure.persistence import InMemoryProjectRepository


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize dependencies at startup."""
    repository = InMemoryProjectRepository(initial=[])
    use_case = ProjectQueryService(project_repository=repository)
    set_project_query_use_case(use_case)
    yield
    # Teardown if needed (e.g. close DB pool)


def create_app() -> FastAPI:
    """Factory for the FastAPI application."""
    app = FastAPI(
        title="Tech Lead Agent API",
        description="Tech Lead Agent - Clean Architecture",
        version="0.1.0",
        lifespan=lifespan,
    )
    app.include_router(projects.router, prefix="/api")
    return app


app = create_app()
