# src/evaluate.py
import mlflow
import pandas as pd
from pathlib import Path
from joblib import load
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from src.config import load_params, PROJECT_ROOT

def main():
    params = load_params()
    data_cfg = params["data"]
    mlflow_cfg = params["mlflow"]

    test_path = PROJECT_ROOT / data_cfg["processed_test"]
    model_path = PROJECT_ROOT / "data" / "models" / "rf_model.joblib"

    test_df = pd.read_csv(test_path)
    target_col = params["train"]["target_col"]

    X_test = test_df.drop(columns=[target_col])
    y_test = test_df[target_col]

    model = load(model_path)

    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    report = classification_report(y_test, y_pred, output_dict=True)
    auc = roc_auc_score(y_test, y_proba)

    print("AUC:", auc)
    print("Classification report:", report)

    mlflow.set_tracking_uri(mlflow_cfg["tracking_uri"])
    mlflow.set_experiment(mlflow_cfg["experiment_name"])

    with mlflow.start_run(run_name="evaluation"):
        mlflow.log_metric("test_auc", auc)
        # Log confusion matrix etc. as artifacts if needed

if __name__ == "__main__":
    main()
