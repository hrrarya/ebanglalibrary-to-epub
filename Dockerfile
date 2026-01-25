# Base image
FROM python:3.11-slim

# Install uv
RUN pip install --no-cache-dir uv

WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock* ./

# Install deps using uv
RUN uv sync --frozen

# Copy source code
COPY . .

# Expose port
EXPOSE 2323

# Run app
CMD ["uv", "run", "python", "apis/app.py"]
