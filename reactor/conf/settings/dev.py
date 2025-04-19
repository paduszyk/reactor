from .common import Settings as Common


class Settings(Common):
    # Debugging

    DEBUG = True

    # Security

    SECRET_KEY = "django-insecure-secret-key"  # noqa: S105

    INTERNAL_IPS = [
        "127.0.0.1",
    ]

    # Apps

    @property
    def INSTALLED_APPS(self):  # noqa: N802
        return [
            *super().INSTALLED_APPS,
            "debug_toolbar",
            "schema_graph",
            "xlsx_serializer",
        ]

    # Middleware

    @property
    def MIDDLEWARE(self):  # noqa: N802
        return [
            *super().MIDDLEWARE,
            "debug_toolbar.middleware.DebugToolbarMiddleware",
        ]

    # URLs

    @classmethod
    def get_urlpatterns(cls):
        import debug_toolbar
        from schema_graph.views import Schema

        from django.urls import include, path

        return [
            *super().get_urlpatterns(),
            path("debug-toolbar/", include(debug_toolbar.urls)),
            path("schema-graph/", view=Schema.as_view()),
        ]

    # Storages

    STATIC_URL = "static/"

    STATIC_ROOT = Common.BASE_DIR / "staticfiles"


Settings.load(__name__)
