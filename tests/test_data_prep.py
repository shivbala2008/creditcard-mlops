from pathlib import Path
import pandas as pd
from src.data_prep import main as data_prep_main
from src.config import PROJECT_ROOT

def test_data_prep_creates_files(tmp_path, monkeypatch):
    # Just run the function and ensure processed files exist
    data_prep_main()
    train_path = PROJECT_ROOT / "data" / "processed" / "train.csv"
    test_path = PROJECT_ROOT / "data" / "processed" / "test.csv"

    assert train_path.exists()
    assert test_path.exists()

    train_df = pd.read_csv(train_path)
    assert "Class" in train_df.columns
    assert len(train_df) > 0
