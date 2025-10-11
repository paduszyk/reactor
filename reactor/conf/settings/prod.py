import json
import os

from environs import env

from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import import_string

from .base import BasePlugin
from .common import CommonSettings


class StoragesPlugin(BasePlugin):
    @classmethod
    def is_active(cls):
        return "DJANGO_STORAGES_BACKEND" in os.environ

    # Storages

    @property
    def STORAGES(self):
        storages = {}

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

        return {**getattr(super(), "STORAGES", {}), **storages}


class ProdSettings(CommonSettings):
    # Debugging

    DEBUG = False

    # Security

    SECRET_KEY = env.str("DJANGO_SECRET_KEY")

    ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS")

    CSRF_TRUSTED_ORIGINS = env.list("DJANGO_CSRF_TRUSTED_ORIGINS")

    # Middleware

    @property
    def MIDDLEWARE(self):
        middleware = super().MIDDLEWARE.copy()

        security_middleware_index = middleware.index(
            "django.middleware.security.SecurityMiddleware",
        )

        middleware.insert(
            security_middleware_index + 1,
            "whitenoise.middleware.WhiteNoiseMiddleware",
        )

        return middleware

    # Storages

    STORAGES = {
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }

    STATIC_URL = "static/"

    STATIC_ROOT = CommonSettings.BASE_DIR / "staticfiles"


ProdSettings.load()
