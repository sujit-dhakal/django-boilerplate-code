FROM python:3.12-slim AS builder

WORKDIR /app

ARG POETRY_VERSION=2.3.1

ENV POETRY_VERSION=${POETRY_VERSION} \
    POETRY_NO_INTERACTION=1 \
    POETRY_NO_ANSI=1 \
    POETRY_VIRTUALENVS_CREATE=0 \
    VIRTUAL_ENV="/venv" \
    PATH="/venv/bin:$PATH"

RUN pip install --no-cache-dir poetry==${POETRY_VERSION} && \
    python -m venv /venv

COPY pyproject.toml poetry.lock ./

RUN poetry install --only main --no-root

FROM python:3.12-slim AS final

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    VIRTUAL_ENV="/venv" \
    PATH="/venv/bin:$PATH"

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    netcat-openbsd \
    curl && \
    rm -rf /var/lib/apt/lists/* && \
    groupadd --system --gid 1001 appuser && \
    useradd --system --uid 1001 --gid appuser --no-create-home appuser && \
    mkdir -p /app/staticfiles /app/media && \
    chown -R appuser:appuser /app/staticfiles /app/media

COPY --from=builder /venv /venv
COPY --chown=appuser:appuser . .

RUN chmod +x /app/entrypoint.sh && \
    chown appuser:appuser /app/entrypoint.sh

USER appuser

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]