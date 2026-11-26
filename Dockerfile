
FROM python:3.12-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copy dependency definitions
COPY pyproject.toml uv.lock ./

# Install dependencies inside the container
RUN uv sync --frozen

# Copy application source
COPY src ./src


# Run the RAGAS evaluation pipeline
CMD ["uv", "run", "python", "-m", "src.test.evaluation_pipeline"]
