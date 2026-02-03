# Deployment Guide

This directory contains infrastructure and deployment configuration
for the Iris ML Inference Service.

The manifests are designed to be cloud-agnostic and demonstrate how
the service would be deployed in a container orchestration environment.

---

## Kubernetes

Kubernetes manifests are located under `deploy/k8s/`.

### Components

- **Deployment**
  - Runs the FastAPI inference service
  - Configured with multiple replicas
  - Uses health and readiness probes
  - Applies CPU and memory limits

- **Service**
  - Exposes the application internally via ClusterIP
  - Routes traffic to healthy pods only

---

## Configuration

The service is configured via environment variables:

| Variable | Description | Default |
|--------|------------|---------|
| WORKERS | Gunicorn worker processes | 2 |
| APP_PORT | Application port | 8000 |

---

## Health Checks

The following endpoints are used by Kubernetes:

- `/health` – liveness probe
- `/ready` – readiness probe

These ensure traffic is only routed to healthy and ready instances.

---

## Notes

- The service is stateless and horizontally scalable
- No persistent volumes are required
- Suitable for ECS, EKS, GKE, or any standard Kubernetes cluster
- Manifests are provided for demonstration and local testing purposes
