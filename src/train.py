# src/train.py

from pathlib import Path

import mlflow
import mlflow.sklearn
import pandas as pd
from joblib import dump
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score, roc_auc_score

from src.config import load_params, PROJECT_ROOT


def main():
    params = load_params()
    data_cfg = params["data"]
    model_cfg = params["model"]
    train_cfg = params["train"]
    mlflow_cfg = params.get("mlflow", {})

    # ---------- Load training data ----------
    train_path = PROJECT_ROOT / data_cfg["processed_train"]
    train_df = pd.read_csv(train_path)

    target_col = train_cfg["target_col"]
    X_train = train_df.drop(columns=[target_col])
    y_train = train_df[target_col]

    # ---------- Configure MLflow (file-based by default) ----------
    tracking_uri = mlflow_cfg.get("tracking_uri", "file:mlruns")
    experiment_name = mlflow_cfg.get("experiment_name", "creditcard_fraud")

    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(experiment_name)

    # ---------- Train model and log with MLflow ----------
    with mlflow.start_run():
        rf = RandomForestClassifier(
            n_estimators=model_cfg["n_estimators"],
            max_depth=model_cfg["max_depth"],
            class_weight=model_cfg["class_weight"],
            n_jobs=model_cfg["n_jobs"],
            random_state=train_cfg["random_state"],
        )

        rf.fit(X_train, y_train)

        y_pred = rf.predict(X_train)
        y_proba = rf.predict_proba(X_train)[:, 1]

        f1 = f1_score(y_train, y_pred)
        auc = roc_auc_score(y_train, y_proba)

        # Log params & metrics
        mlflow.log_params(
            {
                "n_estimators": model_cfg["n_estimators"],
                "max_depth": model_cfg["max_depth"],
                "class_weight": model_cfg["class_weight"],
                "n_jobs": model_cfg["n_jobs"],
            }
        )
        mlflow.log_metric("train_f1", f1)
        mlflow.log_metric("train_auc", auc)

        # Save model locally
        model_dir = PROJECT_ROOT / "data" / "models"
        model_dir.mkdir(parents=True, exist_ok=True)
        model_path = model_dir / "rf_model.joblib"
        dump(rf, model_path)

        # Log model to MLflow
        mlflow.sklearn.log_model(rf, artifact_path="rf_model")


if __name__ == "__main__":
    main()
