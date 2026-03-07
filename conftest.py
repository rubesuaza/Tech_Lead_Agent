"""Pytest configuration: ensure src is on Python path for domain/application imports."""

import sys
from pathlib import Path

# Add project src to path so that "domain" and "application" packages resolve
_root = Path(__file__).resolve().parent
_src = _root / "src"
_src_str = str(_src)
if _src.exists():
    while _src_str in sys.path:
        sys.path.remove(_src_str)
    sys.path.insert(0, _src_str)


def pytest_configure(config):
    """Re-apply path setup during pytest startup (if needed)."""
    if _src.exists() and _src_str not in sys.path:
        sys.path.insert(0, _src_str)
