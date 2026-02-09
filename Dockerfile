FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Initialize database
RUN python -m app.database

# Expose ports
EXPOSE 3000 8000

# Run both backend and frontend
CMD ["sh", "-c", "uvicorn app.api:app --host 0.0.0.0 --port 8000 & reflex run --loglevel info"]
