# Base image
FROM python:3.11-slim

# Python runtime settings
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    WORKERS=2

# Working directory inside container
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --default-timeout=300 -r requirements.txt

# Copy application code and model
COPY src/ src/
COPY models/ models/

# Application port
EXPOSE 8000

# Start FastAPI App (Production Runtime)
CMD ["sh", "-c", "gunicorn src.api:app -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --workers ${WORKERS}"]