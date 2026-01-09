from importlib import import_module

import decouple
import dj_database_url as db_url
from decouple import config as env

from .base import BasePlugin
from .common import CommonSettings


class DebugToolbarPlugin(BasePlugin):
    @classmethod
    def is_active(cls):
        try:
            import_module("debug_toolbar")
        except ModuleNotFoundError:
            return False

        return env("DJANGO_DEBUG_TOOLBAR", cast=decouple.strtobool, default="true")

    # Security

    INTERNAL_IPS = [
        "127.0.0.1",
    ]

    # Apps

    @property
    def INSTALLED_APPS(self):
        return [
            *super().INSTALLED_APPS,
            "debug_toolbar",
        ]

    # Middleware

    @property
    def MIDDLEWARE(self):
        return [
            *super().MIDDLEWARE,
            "debug_toolbar.middleware.DebugToolbarMiddleware",
        ]

    # URLs

    @classmethod
    def get_urlpatterns(cls):
        from debug_toolbar.toolbar import debug_toolbar_urls

        return super().get_urlpatterns() + debug_toolbar_urls()


class DevSettings(CommonSettings):
    # Debugging

    DEBUG = env("DJANGO_DEBUG", cast=decouple.strtobool, default="true")

    # Security

    SECRET_KEY = env("DJANGO_SECRET_KEY", default="django-secret-key")

    # Databases

    @property
    def DATABASES(self):
        try:
            return {
                "default": env("DJANGO_DATABASE_URL", cast=db_url.parse),
            }
        except decouple.UndefinedValueError:
            return {}

    # Storages

    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }

    MEDIA_URL = "media/"

    MEDIA_ROOT = CommonSettings.BASE_DIR / "media"

    STATIC_URL = "static/"

    STATIC_ROOT = CommonSettings.BASE_DIR / "staticfiles"


DevSettings.load()
