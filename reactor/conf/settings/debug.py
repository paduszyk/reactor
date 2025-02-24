import os

from decouple import config

from django.core.exceptions import ImproperlyConfigured

from .common import Settings as Common


class Debug(Common):
    # Debugging

    DEBUG = True

    # Security

    SECRET_KEY = "django-insecure-secret-key"  # noqa: S105


class Local(Debug):
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

    @classmethod
    def get_urlpatterns(cls):
        from debug_toolbar.toolbar import debug_toolbar_urls

        return [
            *super().get_urlpatterns(),
            *debug_toolbar_urls(prefix="debug-toolbar/"),
        ]


class CI(Debug):
    @classmethod
    def pre_load(cls):
        super().pre_load()

        engine = config("DATABASE_ENGINE")

        try:
            url = cls.DATABASE_URLS[engine]
        except KeyError as exc_info:
            msg = (
                f"unsupported database engine {engine!r}; "
                f"expected one of: {', '.join(map(repr, cls.DATABASE_URLS))}"
            )

            raise ImproperlyConfigured(msg) from exc_info

        os.environ["DATABASE_URL"] = url

    # Databases

    DATABASE_URLS = {
        "sqlite": "sqlite://:memory:",
        "postgres": "postgres://postgres:postgres@localhost:5432/postgres",
    }


Settings = CI if config("CI", default=False, cast=bool) else Local

Settings.load(__name__)
