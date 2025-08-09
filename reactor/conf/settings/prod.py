import json
import os

from decouple import Csv, config

from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import import_string

from .common import Settings as Common

STORAGE_VARIABLE_PREFIX = "DJANGO_STORAGE_"


class Settings(Common):
    # Debugging

    DEBUG = False

    # Security

    SECRET_KEY = config("DJANGO_SECRET_KEY")

    ALLOWED_HOSTS = config("DJANGO_ALLOWED_HOSTS", cast=Csv())

    CSRF_TRUSTED_ORIGINS = config("DJANGO_CSRF_TRUSTED_ORIGINS", cast=Csv())

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

    STATIC_URL = "static/"

    STATIC_ROOT = Common.BASE_DIR / "staticfiles"

    @property
    def STORAGES(self):
        storages = {
            "staticfiles": {
                "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
            },
        }

        for name, value in os.environ.items():
            if not name.startswith(STORAGE_VARIABLE_PREFIX):
                continue

            alias = name.removeprefix(STORAGE_VARIABLE_PREFIX).lower()

            if alias == "staticfiles":
                msg = (
                    f"the '{alias}' is a reserved alias for static files storage; "
                    f"unset the {name} variable"
                )

                raise ImproperlyConfigured(msg)

            configuration = json.loads(value)

            if not (backend := configuration.get("BACKEND")):
                msg = (
                    f"the 'BACKEND' key is missing from the '{alias}' storage; "
                    f"update the {name} variable"
                )

                raise ImproperlyConfigured(msg)

            try:
                import_string(backend)
            except ImportError as exc_info:
                msg = (
                    f"failed to import the {backend} backend for the '{alias}' storage; "
                    f"check the {name} variable"
                )

                raise ImproperlyConfigured(msg) from exc_info

            storages[alias] = configuration

        if "default" not in storages:
            msg = (
                f"the 'default' storage configuration is missing; "
                f"set the {STORAGE_VARIABLE_PREFIX}DEFAULT variable"
            )

            raise ImproperlyConfigured(msg)

        return storages


Settings.load()
