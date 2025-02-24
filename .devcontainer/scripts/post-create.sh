#!/usr/bin/env bash

set -e

npm install --save-dev

uv sync --all-groups --all-extras
uv run lefthook install --force
