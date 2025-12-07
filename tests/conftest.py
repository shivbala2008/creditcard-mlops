# tests/conftest.py
import sys
from pathlib import Path

# Add project root to sys.path so "import src.xxx" works
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
