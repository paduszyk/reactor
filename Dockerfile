FROM ghcr.io/astral-sh/uv:0.9.22-python3.14-alpine AS builder

ARG DJANGO_STORAGES_BACKEND

WORKDIR /app/

COPY .python-version pyproject.toml uv.lock ./

RUN uv sync --locked \
    && uv pip install django-storages[${DJANGO_STORAGES_BACKEND}]


FROM python:3.14-alpine

RUN apk add --no-cache gettext

WORKDIR /app/

COPY --from=builder /app/.venv/ ./.venv/
COPY reactor/ ./reactor/
COPY entrypoint.sh ./

RUN chmod +x entrypoint.sh

ENV PATH=/app/.venv/bin:${PATH}

ENV DJANGO_SETTINGS_MODULE=reactor.conf.settings.prod

ENTRYPOINT [ "./entrypoint.sh" ]
