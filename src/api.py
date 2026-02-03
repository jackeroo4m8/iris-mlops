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
request_count = defaultdict(int)
request_errors = defaultdict(int)
request_latency = defaultdict(list)


@app.on_event("startup")
def startup_event():
    global service_ready
    logger.info("API startup")
    service_ready = True


@app.on_event("shutdown")
def shutdown_event():
    logger.info("API shutdown")


# Rate limiting happens before observability by design
# Blocked requests are intentionally excluded from metrics
@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    ip = request.client.host if request.client else "unknown"
    now = time.time()

    request_timestamps[ip] = [
        t for t in request_timestamps[ip]
        if now - t < WINDOW
    ]

    if len(request_timestamps[ip]) >= REQUEST_LIMIT:
        logger.warning("Rate limit exceeded | ip=%s", ip)
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    request_timestamps[ip].append(now)
    return await call_next(request)


@app.middleware("http")
async def observability_middleware(request: Request, call_next):
    start_time = time.time()
    success = True

    try:
        response = await call_next(request)
        return response
    except Exception:
        success = False
        raise
    finally:
        duration = time.time() - start_time
        path = request.url.path

        request_count[path] += 1
        request_latency[path].append(duration)
        if not success:
            request_errors[path] += 1

        logger.info(
            "Request completed | path=%s | duration=%.4f | success=%s",
            path,
            duration, 
            success
        )


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
    return {"status": "healthy"}


@app.get("/ready")
def readiness():
    if not service_ready:
        raise HTTPException(status_code=503, detail="Service not ready")
    return {"status": "ready"}


@app.get("/metrics")
def metrics():
    return {
        "request_count": dict(request_count),
        "request_errors": dict(request_errors),
        "avg_latency": {
            path: sum(times) / len(times) if times else 0
            for path, times in request_latency.items()
            if times
        }
    }


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