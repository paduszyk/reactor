FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install gettext --yes && apt-get clean
RUN python -m pip install poetry

COPY poetry.lock pyproject.toml ./

RUN poetry install --only main --extras prod

COPY src/ ./
COPY manage.py ./
COPY entrypoint.sh ./

ENV DJANGO_SETTINGS_MODULE=reactor.conf.settings
ENV DJANGO_CONFIGURATION=Prod

ENTRYPOINT [ "./entrypoint.sh" ]
