from pathlib import Path

from schema_graph.views import Schema

from django.urls import path

from . import debug


class Settings(debug.Settings):
    @classmethod
    def pre_load(cls):
        super().pre_load()

        cls.env.read_env(Path.cwd() / ".env", overwrite=True)

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
        return [
            *super().get_urlpatterns(),
            path("schema-graph/", Schema.as_view()),
        ]
