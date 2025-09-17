# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set the working directory in the container
WORKDIR /app

# Copy the project files
COPY pyproject.toml uv.lock* ./

# Install dependencies with uv
RUN uv sync --frozen --no-cache

# Copy the rest of the application
COPY . /app

# Run the Python script when the container launches
CMD ["uv", "run", "python", "main.py"]
