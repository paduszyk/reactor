from pathlib import Path

from schema_graph.views import Schema

from django.urls import include, path

from . import debug


class Settings(debug.Settings):
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
            "django_extensions",
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

    # URLs

    @classmethod
    def get_urlpatterns(cls):
        return [
            *super().get_urlpatterns(),
            path("debug-toolbar/", include("debug_toolbar.urls")),
            path("schema-graph/", Schema.as_view()),
        ]

    # Django extensions

    SHELL_PLUS = "ipython"
