import os

from . import debug

DATABASE_URLS = {
    "postgres": "postgres://postgres:postgres@localhost:5432/postgres",
    "sqlite": "sqlite://:memory:",
}


class Settings(debug.Settings):
    """Encapsulates settings specific to CI environments."""

    @property
    def DATABASES(self):
        return {
            "default": self.env.db_url_config(
                DATABASE_URLS[os.environ["DATABASE_ENGINE"]],
            ),
        }
