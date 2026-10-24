#!/bin/sh

set -e

python -m django check --fail-level=ERROR --deploy
python -m django migrate --no-input --database=default
python -m django collectstatic --no-input
python -m django compilemessages --ignore=".venv"

exec gunicorn reactor.conf.wsgi:application
