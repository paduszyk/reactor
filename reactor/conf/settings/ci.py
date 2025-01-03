import os

from . import debug

DATABASE_URLS = {
    "sqlite": "sqlite://:memory:",
}


class Settings(debug.Settings):
    @classmethod
    def pre_load(cls):
        database_url = DATABASE_URLS[os.environ["DB_ALIAS"]]

        os.environ.setdefault("DATABASE_URL", database_url)
