FROM python:3.11-slim

WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy application files
COPY requirements.txt .
COPY run_ecosystem_pipeline.py .
COPY phase1_cloning.py .
COPY phase2_integrity.py .
COPY phase3_dataset.py .
COPY start.sh .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create output directory
RUN mkdir -p /app/output

# Make start script executable
RUN chmod +x start.sh

# Entry point
ENTRYPOINT ["./start.sh"]
