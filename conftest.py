"""Pytest configuration: ensure src is on Python path for domain/application imports."""

import sys
from pathlib import Path

# Add project src to path so that "domain" and "application" packages resolve
_root = Path(__file__).resolve().parent
_src = _root / "src"
_src_str = str(_src)
if _src.exists() and _src_str not in sys.path:
    sys.path.insert(0, _src_str)


def pytest_configure(config):
    """Run path setup as early as possible during pytest startup."""
    if _src.exists() and _src_str not in sys.path:
        sys.path.insert(0, _src_str)
