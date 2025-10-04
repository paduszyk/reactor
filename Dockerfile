FROM ghcr.io/astral-sh/uv:0.8-python3.13-alpine AS builder

ARG DJANGO_STORAGES_BACKEND

WORKDIR /app/

COPY pyproject.toml uv.lock ./

RUN uv sync --locked \
    && uv pip install django-storages[${DJANGO_STORAGES_BACKEND}]


FROM python:3.13-alpine

RUN apk add --no-cache gettext

WORKDIR /app/

COPY --from=builder /app/.venv/ ./.venv/
COPY reactor/ ./reactor/
COPY entrypoint.sh ./

ENV PATH=/app/.venv/bin:${PATH}

ENTRYPOINT [ "./entrypoint.sh" ]
