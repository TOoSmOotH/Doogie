FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install core dependencies first (these change less frequently)
RUN pip install fastapi uvicorn pydantic sqlalchemy alembic

# Install remaining dependencies
RUN pip install -r requirements.txt

# Copy application code
COPY . .

# Expose port for API
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]