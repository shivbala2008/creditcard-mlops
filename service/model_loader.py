from pathlib import Path
from joblib import load

BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_PATH = BASE_DIR / "data" / "models" / "rf_model.joblib"
SCALER_PATH = BASE_DIR / "data" / "models" / "scaler.joblib"

_model = None
_scaler = None

def get_model():
    global _model
    if _model is None:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
        _model = load(MODEL_PATH)
    return _model

def get_scaler():
    global _scaler
    if _scaler is None:
        if not SCALER_PATH.exists():
            raise FileNotFoundError(f"Scaler file not found at {SCALER_PATH}")
        _scaler = load(SCALER_PATH)
    return _scaler
