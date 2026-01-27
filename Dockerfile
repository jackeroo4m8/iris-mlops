# Base image
FROM python:3.11-slim

# Python runtime settings
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

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

# Start FastAPI App
CMD ["python", "-m", "uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]
