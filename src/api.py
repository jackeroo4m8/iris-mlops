import time

from collections import defaultdict
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel

from src.inference import predict
from src.logger import get_logger
from src.request_id import RequestIDMiddleware

logger = get_logger(__name__)

app = FastAPI(title="Iris ML API")
logger.info("API initialized")

app.add_middleware(RequestIDMiddleware)

service_ready = False

REQUEST_LIMIT = 100    # Requests per minute
WINDOW = 60
request_timestamps = defaultdict(list)


@app.on_event("startup")
def startup_event():
    global service_ready
    logger.info("API startup")
    service_ready = True


@app.on_event("shutdown")
def shutdown_event():
    logger.info("API shutdown")


@app.middleware("http")
async def add_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    logger.info(f"Request processed in {duration:.2f} seconds | path={request.url.path}")
    return response


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    ip = request.client.host
    now = time.time()

    # Remove old requests
    request_timestamps[ip] = [
        t for t in request_timestamps[ip] 
        if now - t < WINDOW
    ] 

    if len(request_timestamps[ip]) >= REQUEST_LIMIT:
        logger.warning(f"Rate limit exceeded | ip={ip}")
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    request_timestamps[ip].append(now)
    return await call_next(request)

class IrisInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float


@app.get("/")
def root():
    return {"status": "ok"}


@app.get("/health")
def health():
    logger.info("Health check requested")
    return {"status": "healthy"}


@app.get("/ready")
def readiness():
    if not service_ready:
        raise HTTPException(status_code=503, detail="Service not ready")
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

    except Exception as e:
        logger.exception("Prediction failed")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )