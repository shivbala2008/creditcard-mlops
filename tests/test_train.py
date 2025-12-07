from pathlib import Path
from src.train import main as train_main
from src.config import PROJECT_ROOT

def test_train_creates_model():
    train_main()
    model_path = PROJECT_ROOT / "data" / "models" / "rf_model.joblib"
    assert model_path.exists()
