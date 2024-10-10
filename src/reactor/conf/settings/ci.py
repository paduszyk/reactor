import os

from django.core.exceptions import ImproperlyConfigured

from . import debug

DATABASE_URLS = {
    "postgres": "postgres://postgres:postgres@localhost:5432/postgres",
    "sqlite": "sqlite://:memory:",
}


class Settings(debug.Settings):
    # Databases

    @property
    def DATABASES(self):
        try:
            database_engine = os.environ["DATABASE_ENGINE"]
        except KeyError as exc:
            msg = "DATABASE_ENGINE environment variable is not set"

            raise ImproperlyConfigured(msg) from exc

        if database_engine not in DATABASE_URLS:
            msg = (
                f"DATABASE_ENGINE environment variable is set to an invalid value: "
                f"{database_engine}; use one of: {', '.join(DATABASE_URLS)}"
            )

            raise ImproperlyConfigured(msg)

        return {"default": self.env.db_url_config(DATABASE_URLS[database_engine])}
