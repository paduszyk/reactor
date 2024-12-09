from . import debug


class Settings(debug.Settings):
    # Security

    INTERNAL_IPS = [
        "127.0.0.1",
    ]

    # Databases

    @property
    def DATABASES(self):
        return {
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": self.BASE_DIR / "db.sqlite3",
            },
        }

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
        from schema_graph.views import Schema

        from django.urls import include, path

        return [
            *super().get_urlpatterns(),
            path("debug-toolbar/", include("debug_toolbar.urls")),
            path("schema-graph/", Schema.as_view()),
        ]
