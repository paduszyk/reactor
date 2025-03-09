#!/usr/bin/env bash

set -e

npm install --save-dev
uv sync --all-groups --all-extras --frozen

uv run pre-commit install --install-hooks --overwrite
