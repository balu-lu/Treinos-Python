FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1
ENV POETRY_VERSION=1.8.3
ENV POETRY_HOME=/opt/poetry
ENV PATH="$POETRY_HOME/bin:$PATH"

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-dev --no-interaction --no-ansi

COPY APIs/ ./APIs/

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "APIs.app:app", "--host", "0.0.0.0", "--port", "8000"]
