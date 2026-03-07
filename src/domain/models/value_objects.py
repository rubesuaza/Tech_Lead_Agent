"""
Value objects for the Project Master Context domain.
Immutable; no external framework dependencies.
"""

from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class UseCase:
    """Represents an item in lista_casos_uso (code, title, complexity)."""

    code: str
    title: str
    complexity: str


@dataclass(frozen=True)
class InfrastructureSpecs:
    """Encapsulates db_engines, api_types, and messaging."""

    db_engines: Sequence[str] = ()
    api_types: Sequence[str] = ()
    messaging: Sequence[str] = ()

    def __post_init__(self):
        # Normalize to tuple for immutability (accept lists from JSON)
        for name in ("db_engines", "api_types", "messaging"):
            val = getattr(self, name)
            t = tuple(val) if val else ()
            object.__setattr__(self, name, t)
