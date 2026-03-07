"""Pytest configuration. Ensures 'src' is importable from project root."""
import sys
from pathlib import Path

# Project root (Tech_Lead_Agent)
ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
