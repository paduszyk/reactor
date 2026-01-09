#!/bin/sh

set -e

python -m django check --fail-level=ERROR --deploy
python -m django migrate --no-input
python -m django collectstatic --no-input
python -m django compilemessages  --ignore=".venv/**"

gunicorn reactor.conf.wsgi:application
