import dj_database_url as db_url
from dotenv import dotenv_values, load_dotenv

from django.core.exceptions import ImproperlyConfigured

from . import debug


class Settings(debug.Settings):
    @classmethod
    def pre_load(cls):
        if db_url.DEFAULT_ENV not in dotenv_values():
            msg = f"{db_url.DEFAULT_ENV} environment variable is not set in '.env'"

            raise ImproperlyConfigured(msg)

        load_dotenv()

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
        from schema_graph.views import Schema

        from django.urls import include, path

        return [
            *super().get_urlpatterns(),
            path("debug-toolbar/", include("debug_toolbar.urls")),
            path("schema-graph/", Schema.as_view()),
        ]

    # Serializers

    SERIALIZATION_MODULES = {
        "xlsx": "xlsx_serializer",
    }

    # Extensions

    SHELL_PLUS = "ipython"

    SHELL_PLUS_IMPORTS = [
        "from django.apps.registry import apps",
    ]
