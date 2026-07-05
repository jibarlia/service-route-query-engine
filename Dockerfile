# syntax=docker/dockerfile:1
FROM python:3.13-slim

# Install uv (fast, reproducible dependency resolution from the lockfile).
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Install dependencies first (cached unless the lockfile changes).
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

# Copy the application (includes the bundled graph JSON under app/data/).
COPY app ./app

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
