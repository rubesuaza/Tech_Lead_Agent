"""Ensure src is on path when running tests under tests/."""

import sys
from pathlib import Path

_root = Path(__file__).resolve().parent.parent
_src = _root / "src"
_src_str = str(_src)
if _src.exists() and _src_str not in sys.path:
    sys.path.insert(0, _src_str)
