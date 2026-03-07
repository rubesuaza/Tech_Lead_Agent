"""
Mappers: translate DB rows (external) to domain models (internal).
No business logic; only data shape conversion.
"""

import json
from uuid import UUID
from typing import Any

from domain.models import ProjectMaster
from domain.models.value_objects import UseCase


def row_to_project_master(row: dict[str, Any]) -> ProjectMaster:
    """
    Maps a single row from view_project_master_context to ProjectMaster.
    Expects keys: project_id, project_code, project_name, stack_tecnologico,
    estructura_directorios, reglas_dominio, checklist, coding_standards,
    patrones_diseno, lista_casos_uso.
    """
    project_id = _to_uuid(row.get("project_id"))
    project_code = str(row.get("project_code") or "")
    project_name = str(row.get("project_name") or "")
    stack_tecnologico = _to_dict(row.get("stack_tecnologico"))
    estructura_directorios = _to_str_optional(row.get("estructura_directorios"))
    reglas_dominio = _to_str_optional(row.get("reglas_dominio"))
    checklist = _to_str_optional(row.get("checklist"))
    coding_standards = _to_str_tuple(row.get("coding_standards"))
    patrones_diseno = _to_str_tuple(row.get("patrones_diseno"))
    lista_casos_uso = _to_use_cases(row.get("lista_casos_uso"))

    return ProjectMaster(
        project_id=project_id,
        project_code=project_code,
        project_name=project_name,
        stack_tecnologico=stack_tecnologico,
        estructura_directorios=estructura_directorios,
        reglas_dominio=reglas_dominio,
        checklist=checklist,
        coding_standards=coding_standards,
        patrones_diseno=patrones_diseno,
        lista_casos_uso=lista_casos_uso,
    )


def _to_uuid(value: Any) -> UUID:
    if value is None:
        raise ValueError("project_id is required")
    if isinstance(value, UUID):
        return value
    if isinstance(value, str):
        return UUID(value)
    return UUID(str(value))


def _to_str_optional(value: Any) -> str | None:
    if value is None:
        return None
    return str(value).strip() or None


def _to_dict(value: Any) -> dict[str, Any]:
    if value is None:
        return {}
    if isinstance(value, dict):
        return dict(value)
    if isinstance(value, str):
        try:
            return json.loads(value) if value.strip() else {}
        except json.JSONDecodeError:
            return {}
    return {}


def _to_str_tuple(value: Any) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, tuple):
        return tuple(str(x) for x in value)
    if isinstance(value, list):
        return tuple(str(x) for x in value)
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
            return tuple(str(x) for x in parsed) if isinstance(parsed, list) else (value,)
        except json.JSONDecodeError:
            return (value,) if value else ()
    return ()


def _to_use_cases(value: Any) -> tuple[UseCase, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        try:
            value = json.loads(value) if value.strip() else []
        except json.JSONDecodeError:
            return ()
    if not isinstance(value, (list, tuple)):
        return ()
    result: list[UseCase] = []
    for item in value:
        if isinstance(item, UseCase):
            result.append(item)
        elif isinstance(item, dict):
            result.append(
                UseCase(
                    code=str(item.get("code", "")),
                    title=str(item.get("title", "")),
                    complexity=str(item.get("complexity", "")),
                )
            )
        else:
            continue
    return tuple(result)
