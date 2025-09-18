# Use an official Python runtime as a parent image
FROM docker.io/python:3.13-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set the working directory in the container
WORKDIR /app

# Copy the project files
COPY pyproject.toml uv.lock* README.md ./

# Install dependencies with uv
RUN uv sync --frozen --no-cache

# Copy the rest of the application
COPY . /app

# Expose port 5000 for the Flask web server
EXPOSE 5000

# Run the Python script when the container launches
CMD ["uv", "run", "python", "main.py"]
