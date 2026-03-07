# Infrastructure layer - adapters implementing application ports (Hexagonal)

from infrastructure.persistence.postgres_project_repository import PostgresProjectRepository

__all__ = [
    "PostgresProjectRepository",
]
