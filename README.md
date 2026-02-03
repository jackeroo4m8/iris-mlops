# Iris ML Inference Service

Production-ready machine learning inference API built with FastAPI and Docker.

This service exposes a REST API for Iris flower classification using a trained
scikit-learn model and follows real-world backend and MLOps best practices.

---

## Features

- FastAPI-based REST API
- Iris classification inference
- Production server using Gunicorn + Uvicorn workers
- Dockerized runtime
- Multi-worker scaling via environment variables
- Health and readiness probes
- Request timing and structured logging
- Basic rate limiting
- Resource limits support (CPU / memory)
- CI/CD with GitHub Actions
- Docker images published to GitHub Container Registry (GHCR)

---

to this:

```md
## Project Structure

```text
src/
├── api.py          # FastAPI application
├── inference.py    # Model inference logic
├── logger.py       # Logging configuration
├── request_id.py   # Request ID middleware
├── utils.py
models/
Dockerfile
requirements.txt
BACKLOG.md
README.md


## Run locally
python -m uvicorn src.api:app --reload

## Run with Docker
docker run -p 8000:8000 ghcr.io/jackeroo4m8/iris-mlops:latest

## Scale workers
docker run -e WORKERS=4 -p 8000:8000 ghcr.io/jackeroo4m8/iris-mlops:latest

## Endpoints
- GET /health
- GET /ready
- POST /predict
- GET /metrics

## Production notes
- Gunicorn manages workers and signals
- Resource limits supported
- Timeouts enabled
- Ready for ECS / Kubernetes

## Example Usage

### Predict

Request:
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2
  }'

Response:
```json
{
  "class_index": 0,
  "class_label": "setosa"
}


```md
## Configuration

| Variable | Description | Default |
|--------|------------|---------|
| WORKERS | Number of Gunicorn workers | 2 |
| APP_PORT | Application port | 8000 |

## Non-Goals

- No persistent storage (stateless service)
- In-memory rate limiting (no Redis)
- Metrics are local (not Prometheus-integrated yet)

## Deployment

Infrastructure and deployment manifests are documented under `deploy/`.