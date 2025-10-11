FROM ghcr.io/astral-sh/uv:0.9-python3.14-alpine AS builder

ARG DJANGO_STORAGES_BACKEND

WORKDIR /app/

COPY pyproject.toml uv.lock ./

RUN uv sync --locked \
    && uv pip install django-storages[${DJANGO_STORAGES_BACKEND}]


FROM python:3.14-alpine

RUN apk add --no-cache gettext

WORKDIR /app/

COPY --from=builder /app/.venv/ ./.venv/
COPY reactor/ ./reactor/
COPY entrypoint.sh ./

ENV PATH=/app/.venv/bin:${PATH}

ENTRYPOINT [ "./entrypoint.sh" ]
