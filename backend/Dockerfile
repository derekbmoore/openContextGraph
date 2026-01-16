FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libmagic1 \
    portaudio19-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
# Pre-install CPU-only Torch to avoid pulling CUDA libs (saves ~3GB)
RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Run
ENV PYTHONPATH=/app
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8082"]
