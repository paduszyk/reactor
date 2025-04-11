from dotenv import load_dotenv

from .common import Settings as Common


class Settings(Common):
    @classmethod
    def pre_load(cls):
        super().pre_load()

        load_dotenv()

    # Debugging

    DEBUG = True

    # Security

    SECRET_KEY = "django-insecure-secret-key"  # noqa: S105

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
            path("schema-graph/", view=Schema.as_view()),
        ]


Settings.load(__name__)
