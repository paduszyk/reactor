#!/usr/bin/env bash

set -e

git clean -dxf -e .env

npm install
uv sync --frozen

npx lefthook install --force
