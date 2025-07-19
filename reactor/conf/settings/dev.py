import functools
import os
from importlib import import_module

from decouple import config

from .base import Plugin
from .common import Settings as Common


def _is_running_tests():
    return "PYTEST_VERSION" in os.environ


def inactive_on_tests(plugin):
    is_active = plugin.is_active

    @functools.wraps(is_active)
    def wrapper(*args, **kwargs):
        return not _is_running_tests() and is_active(*args, **kwargs)

    plugin.is_active = wrapper

    return plugin


@inactive_on_tests
class DebugToolbarPlugin(Plugin):
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
        from django.urls import include, path

        return [
            *super().get_urlpatterns(),
            path("__debug__/", include("debug_toolbar.urls")),
        ]


class Settings(Common):
    # Debugging

    DEBUG = config("DJANGO_DEBUG", cast=bool, default="true")

    # Security

    SECRET_KEY = config("DJANGO_SECRET_KEY", default="django-secret-key")

    # Storages

    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }

    STATIC_URL = "static/"

    STATIC_ROOT = Common.BASE_DIR / "staticfiles"

    MEDIA_URL = "media/"

    MEDIA_ROOT = Common.BASE_DIR / "media"


Settings.load()
