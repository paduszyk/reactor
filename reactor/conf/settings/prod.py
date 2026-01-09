import json
import os
import sys
from importlib import import_module

import decouple
import dj_database_url as db_url
from decouple import config as env

from django.core.exceptions import ImproperlyConfigured

from .base import BasePlugin
from .common import CommonSettings


class StoragesPlugin(BasePlugin):
    @classmethod
    def is_active(cls):
        try:
            import_module("storages")
        except ModuleNotFoundError:
            return False

        return "DJANGO_STORAGES_BACKEND" in os.environ

    # Storages

    @property
    def STORAGES(self):
        storages = getattr(super(), "STORAGES", {})

        for name, value in os.environ.items():
            if not name.startswith(prefix := "DJANGO_STORAGE_"):
                continue

            alias = name.removeprefix(prefix).lower()

            try:
                storage = json.loads(value)
            except json.JSONDecodeError as exc:
                msg = (
                    f"the '{alias}' storage config is not a valid JSON; "
                    f"check the {name} environment variable"
                )
                raise ImproperlyConfigured(msg) from exc

            if not isinstance(storage, dict):
                msg = (
                    f"the '{alias}' storage config is not a JSON dict; "
                    f"check the {name} environment variable"
                )
                raise ImproperlyConfigured(msg)

            storages[alias] = storage

        if "default" not in storages:
            msg = (
                "at least the 'default' storage backend must be configured; "
                "set the DJANGO_STORAGE_DEFAULT environment variable"
            )
            raise ImproperlyConfigured(msg)

        return storages


class WhiteNoisePlugin(BasePlugin):
    @classmethod
    def is_active(cls):
        try:
            import_module("whitenoise")
        except ModuleNotFoundError:
            return False

        return env("DJANGO_WHITENOISE", cast=decouple.strtobool, default="true")

    @classmethod
    def post_load(cls):
        super().post_load()

        if "collectstatic" in sys.argv:
            cls.STATIC_ROOT.mkdir(parents=True, exist_ok=True)

    # Middleware

    @property
    def MIDDLEWARE(self):
        middleware = getattr(super(), "MIDDLEWARE", [])

        try:
            security_middleware_index = middleware.index(
                "django.middleware.security.SecurityMiddleware",
            )
        except ValueError:
            security_middleware_index = -1

        middleware.insert(
            security_middleware_index + 1,
            "whitenoise.middleware.WhiteNoiseMiddleware",
        )

        return middleware

    # Storages

    @property
    def STORAGES(self):
        storages = getattr(super(), "STORAGES", {})

        storages.update(
            staticfiles={
                "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
            },
        )

        return storages

    # Static files

    STATIC_URL = "static/"

    STATIC_ROOT = CommonSettings.BASE_DIR / "staticfiles"


class ProdSettings(CommonSettings):
    # Debugging

    DEBUG = False

    # Security

    SECRET_KEY = env("DJANGO_SECRET_KEY")

    ALLOWED_HOSTS = env("DJANGO_ALLOWED_HOSTS", cast=decouple.Csv())

    SESSION_COOKIE_SECURE = True

    CSRF_COOKIE_SECURE = True

    CSRF_TRUSTED_ORIGINS = env("DJANGO_CSRF_TRUSTED_ORIGINS", cast=decouple.Csv())

    # Databases

    @property
    def DATABASES(self):
        databases = getattr(super(), "DATABASES", {})

        for name, value in os.environ.items():
            if not name.startswith(prefix := "DJANGO_DATABASE_"):
                continue

            alias = name.removeprefix(prefix).lower()

            try:
                database = json.loads(value)
            except json.JSONDecodeError as exc:
                msg = (
                    f"the '{alias}' database config is not a valid JSON; "
                    f"check the {name} environment variable"
                )
                raise ImproperlyConfigured(msg) from exc

            if not isinstance(database, dict):
                msg = (
                    f"the '{alias}' database config is not a JSON dict; "
                    f"check the {name} environment variable"
                )
                raise ImproperlyConfigured(msg)

            if (url := database.pop("URL", None)) is not None:
                database.update(db_url.parse(url))

            databases[alias] = database

        if "default" not in databases:
            msg = (
                "at least the 'default' database must be configured; "
                "set the DJANGO_DATABASE_DEFAULT environment variable"
            )
            raise ImproperlyConfigured(msg)

        return databases


ProdSettings.load()
