#!/usr/bin/env bash

set -e

git clean -dxf -e .env

npm ci
uv sync --all-groups --frozen

uv run lefthook install --force
