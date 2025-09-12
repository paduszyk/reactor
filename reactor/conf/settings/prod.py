import json
import os

from environs import env

from .base import BasePlugin
from .common import CommonSettings


class StoragesPlugin(BasePlugin):
    @classmethod
    def is_active(cls):
        return "DJANGO_STORAGES" in os.environ

    @property
    def STORAGES(self):
        storages = {}

        for name, value in os.environ.items():
            if not name.startswith(prefix := "DJANGO_STORAGES_"):
                continue

            alias = name.removeprefix(prefix).lower()
            config = json.loads(value)

            storages[alias] = config

        return {**super().STORAGES, **storages}


class ProdSettings(CommonSettings):
    # Debugging

    DEBUG = False

    # Security

    SECRET_KEY = env.str("DJANGO_SECRET_KEY")

    ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", subcast=str)

    CSRF_TRUSTED_ORIGINS = env.list("DJANGO_CSRF_TRUSTED_ORIGINS", subcast=str)

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
