from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Sequence

from src.domain.models.project_master import ProjectMaster


class ProjectRepository(ABC):
    @abstractmethod
    def find_all(self) -> Sequence[ProjectMaster]:
        """Recupera todos los proyectos desde la fuente de datos subyacente."""

    @abstractmethod
    def find_by_id(self, id: str) -> ProjectMaster | None:
        """Recupera un proyecto concreto por su identificador."""

