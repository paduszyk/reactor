from importlib import import_module

from environ import Env

from .base import Extension
from .common import CommonSettings

Env.read_env(env_file=CommonSettings.BASE_DIR / ".env", override=True)

env = Env()


class DebugToolbarExtension(Extension):
    @classmethod
    def is_enabled(cls):
        try:
            import_module("debug_toolbar")
        except ModuleNotFoundError:
            return False

        return env.bool("DJANGO_DEBUG_TOOLBAR_ENABLED", default=True)

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
        from debug_toolbar.toolbar import debug_toolbar_urls

        return super().get_urlpatterns() + debug_toolbar_urls()


class DevelopmentSettings(CommonSettings):
    # Debugging

    DEBUG = env.bool("DJANGO_DEBUG", default=True)

    # Security

    SECRET_KEY = env.str("DJANGO_SECRET_KEY", default="secret-key")

    # Databases

    @property
    def DATABASES(self):
        if "DJANGO_DATABASE_URL" not in env:
            return {}

        return {
            "default": env.db_url("DJANGO_DATABASE_URL"),
        }

    # Storages

    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }

    MEDIA_URL = "media/"

    MEDIA_ROOT = CommonSettings.BASE_DIR / "media"

    STATIC_URL = "static/"

    STATIC_ROOT = CommonSettings.BASE_DIR / "staticfiles"


DevelopmentSettings.export()
