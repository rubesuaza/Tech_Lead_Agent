"""Pytest configuration: ensure src is on Python path for domain/application imports."""

import sys
from pathlib import Path

# Add project src to path so that "domain" and "application" packages resolve
_root = Path(__file__).resolve().parent
_src = _root / "src"
_src_str = str(_src.resolve())
_tests_dir = _root / "tests"
_tests_str = str(_tests_dir.resolve()) if _tests_dir.exists() else None


def _ensure_src_first():
    """Put src first in sys.path and remove tests dir so application/domain resolve to src."""
    if not _src.exists():
        return
    while _src_str in sys.path:
        sys.path.remove(_src_str)
    sys.path.insert(0, _src_str)
    if _tests_str and _tests_str in sys.path:
        sys.path.remove(_tests_str)


if _src.exists():
    _ensure_src_first()


def pytest_configure(config):
    """Re-apply path setup during pytest startup (if needed)."""
    _ensure_src_first()


def pytest_collect_file(file_path, parent):
    """Before collecting any file, ensure src is first so imports resolve correctly."""
    _ensure_src_first()
    return None  # use default collection
