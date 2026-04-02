# syntax=docker/dockerfile:1
FROM python:3.13-slim

# Install uv for dependency management
COPY --from=ghcr.io/astral-sh/uv:0.5 /uv /uvx /bin/

# Keep Python from generating .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
# Force stdout and stderr streams to be unbuffered
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies first (for better layer caching)
COPY pyproject.toml uv.lock ./
# We use --frozen to ensure the lockfile is up to date and --no-install-project
# so we can build the environment before copying the whole application
RUN uv sync --frozen --no-install-project --no-dev

# Copy the application source code
COPY . .

# Synchronize the project itself
RUN uv sync --frozen --no-dev
