import os

import dj_database_url as db_url

from django.core.exceptions import ImproperlyConfigured

from . import debug

DATABASE_ENGINE_ENV = "DATABASE_ENGINE"

DATABASE_URLS = {
    "postgres": "postgres://postgres:postgres@localhost:5432/postgres",
    "sqlite": "sqlite://:memory:",
}


class Settings(debug.Settings):
    @classmethod
    def pre_load(cls):
        try:
            database_engine = os.environ[DATABASE_ENGINE_ENV]
        except KeyError as e:
            msg = f"{DATABASE_ENGINE_ENV} environment variable is not set"

            raise ImproperlyConfigured(msg) from e

        try:
            database_url = DATABASE_URLS[database_engine]
        except KeyError as e:
            msg = (
                f"{database_engine!r} is not a valid value for {DATABASE_ENGINE_ENV}; "
                f"use one of: {', '.join(map(repr, DATABASE_URLS.keys()))}"
            )

            raise ImproperlyConfigured(msg) from e

        os.environ.setdefault(db_url.DEFAULT_ENV, database_url)
