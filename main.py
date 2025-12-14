import os
import pickle
from typing import List, Union

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

MODEL_PATH = os.getenv("MODEL_PATH", "models/model.pkl")
MODEL_VERSION = os.getenv("MODEL_VERSION", "1.0.0")

app = FastAPI(title="ML Service", version=MODEL_VERSION)

# Загрузка модели при старте
try:
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
except Exception as e:
    model = None
    print(f"Failed to load model: {e}")


class PredictRequest(BaseModel):
    features: List[List[float]]


class PredictResponse(BaseModel):
    predictions: List[Union[float, int, str]]


class HealthResponse(BaseModel):
    status: str
    model_version: str
    model_loaded: bool


@app.get("/health", response_model=HealthResponse)
def health():
    return HealthResponse(
        status="ok" if model is not None else "degraded",
        model_version=MODEL_VERSION,
        model_loaded=model is not None,
    )


@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        predictions = model.predict(request.features)
        return PredictResponse(predictions=predictions.tolist())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

