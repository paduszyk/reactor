from importlib import import_module

from decouple import config

from .base import BasePlugin
from .common import CommonSettings


class DebugToolbarPlugin(BasePlugin):
    @classmethod
    def is_active(cls):
        try:
            import_module("debug_toolbar")
        except ModuleNotFoundError:
            return False

        return config("DJANGO_DEBUG_TOOLBAR", cast=bool, default="true")

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

    DEBUG = config("DJANGO_DEBUG", cast=bool, default="true")

    # Security

    SECRET_KEY = config("DJANGO_SECRET_KEY", cast=str, default="django-secret-key")

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
