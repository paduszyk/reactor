# Build
# =====

FROM ghcr.io/astral-sh/uv:python3.13-alpine AS builder

WORKDIR /app/

COPY pyproject.toml uv.lock ./

RUN uv sync --no-dev --frozen

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
