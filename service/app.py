# service/app.py
from fastapi import FastAPI
from pydantic import BaseModel
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
import time
import numpy as np

from .model_loader import get_model, get_scaler

app = FastAPI(title="Credit Card Fraud Detection API")

# Prometheus metrics
PREDICTION_COUNTER = Counter(
    "prediction_requests_total",
    "Total number of prediction requests",
    ["status"]
)

PREDICTION_LATENCY = Histogram(
    "prediction_request_latency_seconds",
    "Latency of prediction requests in seconds"
)

class TransactionFeatures(BaseModel):
    Time: float
    Amount: float
    V1: float
    V2: float
    V3: float
    V4: float
    V5: float
    V6: float
    V7: float
    V8: float
    V9: float
    V10: float
    V11: float
    V12: float
    V13: float
    V14: float
    V15: float
    V16: float
    V17: float
    V18: float
    V19: float
    V20: float
    V21: float
    V22: float
    V23: float
    V24: float
    V25: float
    V26: float
    V27: float
    V28: float

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(features: TransactionFeatures):
    start_time = time.time()
    try:
        model = get_model()
        scaler = get_scaler()

        data = np.array([[getattr(features, col) for col in features.__fields__.keys()]])
        # scale Time & Amount like training (here we simply reuse scaler.transform on full array,
        # assuming scaler fitted only on [Amount, Time] or similar).
        # If scaler is only for Amount & Time, you'll need to handle accordingly.

        # Example: apply scaler only on cols 0 (Time) and 1 (Amount)
        data_scaled = data.copy()
        data_scaled[:, :2] = scaler.transform(data[:, :2])

        proba = model.predict_proba(data_scaled)[:, 1][0]
        pred = int(proba >= 0.5)

        latency = time.time() - start_time
        PREDICTION_LATENCY.observe(latency)
        PREDICTION_COUNTER.labels(status="success").inc()

        return {"fraud_probability": proba, "prediction": pred}
    except Exception as e:
        PREDICTION_COUNTER.labels(status="error").inc()
        return {"error": str(e)}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
