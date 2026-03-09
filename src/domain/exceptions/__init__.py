class ProjectNotFoundException(Exception):
    """Se dispara cuando no se encuentra un proyecto con el identificador solicitado."""


class IncompleteMetadataException(Exception):
    """Se dispara cuando faltan definiciones críticas del contexto de proyecto."""

