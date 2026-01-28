from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.inference import predict
from src.logger import get_logger
from src.request_id import RequestIDMiddleware

logger = get_logger(__name__)

app = FastAPI(title="Iris ML API")

app.add_middleware(RequestIDMiddleware)

@app.on_event("shutdown")
def shutdown_event():
    logger.info("API shutting down gracefully")

logger.info("API initialized")


class IrisInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float


@app.get("/")
def health_check():
    return {"status": "ok"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/ready")
def readiness_check():
    return {"status": "ready"}

@app.post("/predict")
def predict_iris(input: IrisInput):
    logger.info("Prediction request received")

    try:
        result = predict(input.model_dump())

        logger.info(
            "Prediction response sent | class=%s",
            result["class_label"]
        )
        return result

    except Exception:
        logger.exception("Prediction failed")
        raise HTTPException(
            status_code=500,
            detail="Internal server error during prediction"
        )
