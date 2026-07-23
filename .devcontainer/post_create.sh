#!/usr/bin/env bash

set -e

npm clean-install
uv sync --locked

npm exec --no -- lefthook install --force
