#!/usr/bin/env bash

set -e

git clean -dxf -e .env

npm install --save-dev
uv sync --all-groups --frozen

uv run lefthook install --force
