"""
Domain exceptions for Project Master Context.
Raised when business rules are violated or required data is missing.
"""


class ProjectNotFoundException(Exception):
    """Raised when a requested project code or id is not found."""

    def __init__(self, message: str = "Project not found", project_id: str | None = None):
        self.project_id = project_id
        super().__init__(message)


class IncompleteMetadataException(Exception):
    """Raised when critical definitions (e.g. reglas_dominio) are absent."""

    def __init__(self, message: str = "Incomplete metadata: critical definitions are absent"):
        super().__init__(message)
