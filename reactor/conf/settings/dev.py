from importlib import import_module

from decouple import config

from .base import Plugin
from .common import Settings as Common


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


class SchemaGraphPlugin(Plugin):
    @classmethod
    def is_active(cls):
        try:
            import_module("schema_graph")
        except ModuleNotFoundError:
            return False

        return config("DJANGO_SCHEMA_GRAPH", cast=bool, default="true")

    # Apps

    @property
    def INSTALLED_APPS(self):
        return [
            *super().INSTALLED_APPS,
            "schema_graph",
        ]

    # URLs

    @classmethod
    def get_urlpatterns(cls):
        from schema_graph.views import Schema

        from django.urls import path

        return [
            *super().get_urlpatterns(),
            path("__schema__/", view=Schema.as_view()),
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
