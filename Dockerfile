# Build
# =====

FROM ghcr.io/astral-sh/uv:python3.13-alpine AS builder

ARG DJANGO_STORAGES_BACKENDS

WORKDIR /app/

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen && uv pip install django-storages[${DJANGO_STORAGES_BACKENDS}]


# Runtime
# =======

FROM python:3.13-alpine

RUN apk add --no-cache gettext

WORKDIR /app/

COPY --from=builder /app/.venv/ ./.venv/
COPY reactor/ ./reactor/
COPY entrypoint.sh ./

ENV PATH=/app/.venv/bin:${PATH}

ENTRYPOINT [ "./entrypoint.sh" ]
