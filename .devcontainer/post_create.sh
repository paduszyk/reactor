#!/usr/bin/env bash

set -e

npm clean-install
uv sync --locked

npx --no-install lefthook install --force
