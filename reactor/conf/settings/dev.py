from importlib import import_module

from environs import EnvError, env

from .base import BaseExtension
from .common import CommonSettings

env.read_env()


class DebugToolbarExtension(BaseExtension):
    @classmethod
    def is_enabled(cls):
        try:
            import_module("debug_toolbar")
        except ModuleNotFoundError:
            return False

        return env.bool("DJANGO_DEBUG_TOOLBAR", default=True)

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


class DevSettings(CommonSettings):
    # Debugging

    DEBUG = env.bool("DJANGO_DEBUG", default=True)

    # Security

    SECRET_KEY = env.str("DJANGO_SECRET_KEY", default="django-secret-key")

    # Databases

    @property
    def DATABASES(self):
        try:
            return {
                "default": env.dj_db_url("DJANGO_DATABASE_URL"),
            }
        except EnvError:
            return {}

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


DevSettings.load()
