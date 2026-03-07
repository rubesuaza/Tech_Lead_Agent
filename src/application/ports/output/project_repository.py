"""
Re-export of ProjectRepository from domain layer (Clean Architecture).
The interface is defined in domain.ports; this module exists for backward compatibility.
Prefer: from domain.ports import ProjectRepository
"""

from domain.ports.project_repository import ProjectRepository

__all__ = ["ProjectRepository"]
