# Iris ML Inference Service

Production-ready ML inference API using FastAPI + Docker.

## Features
- FastAPI REST API
- Sklearn model inference
- Request ID tracing
- Structured logging
- Dockerized deployment
- Health endpoint
- Production-ready structure

## Run locally
```bash
docker build -t iris-inference .
docker run -p 8000:8000 iris-inference
