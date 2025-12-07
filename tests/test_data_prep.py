# tests/test_data_prep.py

from pathlib import Path
import pandas as pd

from src.data_prep import main as data_prep_main
from src.config import PROJECT_ROOT


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


def test_data_prep_creates_files():
    # Arrange: create dummy raw CSV
    _create_dummy_raw_csv()

    # Act: run data prep pipeline
    data_prep_main()

    # Assert: processed train/test files exist
    processed_train = PROJECT_ROOT / "data" / "processed" / "train.csv"
    processed_test = PROJECT_ROOT / "data" / "processed" / "test.csv"

    assert processed_train.exists(), f"{processed_train} was not created"
    assert processed_test.exists(), f"{processed_test} was not created"
