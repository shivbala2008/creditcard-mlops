# src/config.py
import yaml
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

def load_params(path: str = "params.yaml") -> dict:
    params_path = PROJECT_ROOT / path
    with open(params_path, "r") as f:
        return yaml.safe_load(f)
