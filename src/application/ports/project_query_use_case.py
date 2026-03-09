from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Sequence

from src.domain.models.project_master import ProjectMaster


class ProjectQueryUseCase(ABC):
    @abstractmethod
    def get_all_projects(self) -> Sequence[ProjectMaster]:
        """Devuelve un listado de proyectos disponibles."""

    @abstractmethod
    def get_project_by_id(self, id: str) -> ProjectMaster | None:
        """Devuelve el ProjectMaster asociado al identificador, o None si no existe."""

