# Use a base image with Python
FROM python:3.13-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV POETRY_VERSION=1.8.3
ENV POETRY_HOME=/opt/poetry
ENV PATH="$POETRY_HOME/bin:$PATH"

# Install system dependencies
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Set work directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry install --no-dev --no-interaction --no-ansi

# Copy source code
COPY PokeDex/ ./PokeDex/

# Expose port
EXPOSE 8000

# Run the application
CMD ["poetry", "run", "uvicorn", "PokeDex.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]