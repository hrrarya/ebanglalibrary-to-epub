# Base image
FROM python:3.11-slim

# Install system dependencies required for pandoc and epub generation
RUN apt-get update && apt-get install -y \
    pandoc \
    cron \
    nano \
    && rm -rf /var/lib/apt/lists/*

# Install cron
RUN crontab -r || true
RUN (crontab -l 2>/dev/null; echo "0 0 * * * rm -rf /app/epub/*"; echo "0 0 * * * rm -rf /app/md/*") | crontab -


# Install uv
RUN pip install --no-cache-dir uv

WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock* ./

# Install deps using uv
RUN uv sync --frozen --no-dev

# Copy source code
COPY . .

# Create necessary directories
RUN mkdir -p epub md

# Expose port (matching the app.py port)
EXPOSE 23223

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run app using hypercorn for production
CMD ["uv", "run", "hypercorn", "apis.app:app", "--bind", "0.0.0.0:8000"]
