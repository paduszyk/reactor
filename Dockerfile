FROM ghcr.io/astral-sh/uv:0.13.4-python3.15-trixie-slim AS builder

ARG UV_DEPENDENCY_ARGS

WORKDIR /app/

COPY pyproject.toml uv.lock ./

ENV UV_COMPILE_BYTECODE=true
ENV UV_LOCKED=true
ENV UV_NO_DEV=true
ENV UV_NO_INSTALL_PROJECT=true
ENV UV_PYTHON_DOWNLOADS=false

RUN uv export ${UV_DEPENDENCY_ARGS} --output-file /tmp/requirements.txt \
    && if grep -q '^mysqlclient==' /tmp/requirements.txt; then \
        apt-get update \
        && apt-get install --yes --no-install-recommends \
            build-essential \
            default-libmysqlclient-dev \
            pkg-config \
        && rm -rf /var/lib/apt/lists/*; \
    fi \
    && rm /tmp/requirements.txt

RUN uv sync ${UV_DEPENDENCY_ARGS}


FROM python:3.15-slim-trixie

WORKDIR /app/

COPY --from=builder /app/.venv/ ./.venv/

RUN apt-get update \
    && apt-get install --yes --no-install-recommends \
        gettext \
    && if /app/.venv/bin/python -c "from importlib.metadata import version; version('mysqlclient')" 2>/dev/null; then \
        apt-get install --yes --no-install-recommends \
            libmariadb3; \
    fi \
    && rm -rf /var/lib/apt/lists/*

COPY reactor/ ./reactor/
COPY entrypoint.sh ./

ENV PATH=/app/.venv/bin:${PATH}

ENTRYPOINT ["./entrypoint.sh"]
