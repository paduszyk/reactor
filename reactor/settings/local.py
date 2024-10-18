from pathlib import Path

from debug_toolbar.toolbar import debug_toolbar_urls
from schema_graph.views import Schema

from django.urls import path

from . import debug


class Settings(debug.Settings):
    """Encapsulates settings specific to local development environments."""

    @classmethod
    def pre_load(cls):
        super().pre_load()

        cls.env.read_env(Path.cwd() / ".env", overwrite=True)

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
            "schema_graph",
            "xlsx_serializer",
        ]

    # Middleware

    @property
    def MIDDLEWARE(self):
        return [
            *super().MIDDLEWARE,
            "debug_toolbar.middleware.DebugToolbarMiddleware",
        ]

    @classmethod
    def get_urlpatterns(cls):
        return [
            *super().get_urlpatterns(),
            *debug_toolbar_urls(prefix="debug-toolbar/"),
            path("schema-graph/", Schema.as_view()),
        ]
