# tests/test_train.py

from pathlib import Path
import pandas as pd

from src.config import PROJECT_ROOT
from src.data_prep import main as data_prep_main
from src.train import main as train_main


def _create_dummy_raw_csv():
    """Create a small synthetic creditcard.csv with enough samples per class."""
    raw_dir = PROJECT_ROOT / "data" / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    raw_path = raw_dir / "creditcard.csv"

    # 10 samples, balanced classes (5 zeros, 5 ones)
    n_samples = 10
    df = pd.DataFrame(
        {
            "Time": list(range(n_samples)),
            "V1": [0.1 * i for i in range(n_samples)],
            "V2": [0.2 * i for i in range(n_samples)],
            "V3": [0.3 * i for i in range(n_samples)],
            "Amount": [10.0 + i for i in range(n_samples)],
            "Class": [0, 1] * (n_samples // 2),
        }
    )

    df.to_csv(raw_path, index=False)
    return raw_path


def test_train_creates_model():
    # Arrange: dummy raw data → run data prep → have train.csv
    _create_dummy_raw_csv()
    data_prep_main()

    # Act: run training
    train_main()

    # Assert: model artifact exists
    model_path = PROJECT_ROOT / "data" / "models" / "rf_model.joblib"
    assert model_path.exists(), f"Model file not found at {model_path}"
