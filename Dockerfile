FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

ARG DATABASE_ENGINE=postgres

RUN apt-get update && \
    apt-get install --yes gettext && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml uv.lock ./

ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=true

RUN uv sync --extra $DATABASE_ENGINE --frozen

COPY reactor ./reactor/
COPY entrypoint.sh ./

ENV PATH=/app/.venv/bin:$PATH

ENTRYPOINT [ "./entrypoint.sh" ]
