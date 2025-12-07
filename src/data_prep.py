# src/data_prep.py
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from src.config import load_params, PROJECT_ROOT

def main():
    params = load_params()
    data_cfg = params["data"]
    train_cfg = params["train"]

    raw_path = PROJECT_ROOT / data_cfg["raw_path"]
    processed_train_path = PROJECT_ROOT / data_cfg["processed_train"]
    processed_test_path = PROJECT_ROOT / data_cfg["processed_test"]

    df = pd.read_csv(raw_path)

    target_col = train_cfg["target_col"]
    X = df.drop(columns=[target_col])
    y = df[target_col]

    # Scale only 'Amount' and maybe 'Time'
    scaler = StandardScaler()
    X[["Amount", "Time"]] = scaler.fit_transform(X[["Amount", "Time"]])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=train_cfg["test_size"],
        random_state=train_cfg["random_state"],
        stratify=y
    )

    train_df = pd.concat([X_train, y_train], axis=1)
    test_df = pd.concat([X_test, y_test], axis=1)

    processed_train_path.parent.mkdir(parents=True, exist_ok=True)
    processed_test_path.parent.mkdir(parents=True, exist_ok=True)

    train_df.to_csv(processed_train_path, index=False)
    test_df.to_csv(processed_test_path, index=False)

    # Save scaler for later use in API
    from joblib import dump
    models_dir = PROJECT_ROOT / "data" / "models"
    models_dir.mkdir(parents=True, exist_ok=True)
    dump(scaler, models_dir / "scaler.joblib")

if __name__ == "__main__":
    main()
