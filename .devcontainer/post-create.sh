#!/usr/bin/env bash

set -e

git clean -dxf -e .env

npm clean-install
uv sync --all-groups --frozen

npx lefthook install --force
