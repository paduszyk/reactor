#!/usr/bin/env bash

set -e

poetry run python manage.py check --deploy
poetry run python manage.py collectstatic --no-input
poetry run python manage.py compilemessages
poetry run python manage.py migrate --no-input

poetry run gunicorn reactor.conf.wsgi:application
