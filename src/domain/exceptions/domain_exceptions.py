"""
Domain exceptions. Raised when business rules or lookups fail.
No external framework dependencies.
"""


class ProjectNotFoundException(Exception):
    """Raised when a requested project code or id is not found."""

    def __init__(self, identifier: str, message: str | None = None):
        self.identifier = identifier
        super().__init__(message or f"Project not found: {identifier}")


class IncompleteMetadataException(Exception):
    """Raised when critical definitions (e.g. reglas_dominio) are absent."""

    def __init__(self, missing_field: str, message: str | None = None):
        self.missing_field = missing_field
        super().__init__(message or f"Incomplete metadata: missing or empty '{missing_field}'")
