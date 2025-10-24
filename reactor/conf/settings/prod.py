import json
import os
import sys
from importlib import import_module
from pathlib import Path

from decouple import Csv, config

from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import import_string

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
                config = json.loads(value)
            except json.JSONDecodeError as exc:
                msg = (
                    f"the '{alias}' storage config is not a valid JSON; "
                    f"check the {name} environment variable"
                )
                raise ImproperlyConfigured(msg) from exc

            if not isinstance(config, dict):
                msg = (
                    f"the '{alias}' storage config is not a JSON dict; "
                    f"check the {name} environment variable"
                )
                raise ImproperlyConfigured(msg)

            if (backend := config.get("BACKEND")) is None:
                msg = (
                    f"the '{alias}' storage config must define the BACKEND key; "
                    f"check the {name} environment variable"
                )
                raise ImproperlyConfigured(msg)

            try:
                import_string(backend)
            except ImportError as exc:
                msg = (
                    f"could not import backend for the '{alias}' storage config; "
                    f"check the {name} environment variable"
                )
                raise ImproperlyConfigured(msg) from exc

            storages[alias] = config

        if "default" not in storages:
            msg = (
                "at least the 'default' storage backend must be defined; "
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

        return config("DJANGO_WHITENOISE", cast=bool, default="true")

    @classmethod
    def post_load(cls):
        super().post_load()

        if "collectstatic" in sys.argv:
            Path.mkdir(cls.STATIC_ROOT, exist_ok=True)

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

    SECRET_KEY = config("DJANGO_SECRET_KEY", cast=str)

    ALLOWED_HOSTS = config("DJANGO_ALLOWED_HOSTS", cast=Csv(cast=str))

    SESSION_COOKIE_SECURE = True

    CSRF_COOKIE_SECURE = True

    CSRF_TRUSTED_ORIGINS = config("DJANGO_CSRF_TRUSTED_ORIGINS", cast=Csv(cast=str))


ProdSettings.load()
