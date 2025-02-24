#!/usr/bin/env bash

set -e

export DJANGO_SETTINGS_MODULE=reactor.conf.settings.deploy

python -m django check --deploy
python -m django collectstatic --no-input
python -m django compilemessages --ignore .venv
python -m django migrate --no-input

gunicorn reactor.conf.wsgi:application
