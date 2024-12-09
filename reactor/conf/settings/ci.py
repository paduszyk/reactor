import os

from django.core.exceptions import ImproperlyConfigured

from . import debug


class Settings(debug.Settings):
    # Databases

    @property
    def DATABASES(self):
        database_configs = {
            "sqlite": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": ":memory:",
            },
        }

        try:
            database_engine = os.environ["DATABASE_ENGINE"]
        except KeyError as e:
            msg = "DATABASE_ENGINE environment variable is not set"

            raise ImproperlyConfigured(msg) from e

        try:
            database_configs = {"default": database_configs[database_engine]}
        except KeyError as e:
            msg = (
                f"{database_engine!r} is not a valid value for DATABASE_ENGINE; "
                f"use one of: {', '.join(map(repr, database_configs.keys()))}"
            )

            raise ImproperlyConfigured(msg) from e

        return database_configs
