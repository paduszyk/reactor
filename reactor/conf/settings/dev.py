import functools
import os
from importlib import import_module

from environs import env

from .base import BasePlugin
from .common import CommonSettings


def _is_pytest_running():
    return "PYTEST_VERSION" in os.environ


def inactive_when_pytest_running(plugin):
    is_active = plugin.is_active

    @functools.wraps(is_active)
    def wrapper(cls, *args, **kwargs):  # noqa: ARG001
        if _is_pytest_running():
            return False

        return is_active(*args, **kwargs)

    plugin.is_active = classmethod(wrapper)

    return plugin


class DotenvPlugin(BasePlugin):
    @classmethod
    def is_active(cls):
        return cls.DOTENV_FILE.exists()

    @classmethod
    def pre_load(cls):
        super().pre_load()

        env.read_env(cls.DOTENV_FILE)

    # Paths

    DOTENV_FILE = CommonSettings.BASE_DIR / ".env"


@inactive_when_pytest_running
class DebugToolbarPlugin(BasePlugin):
    @classmethod
    def is_active(cls):
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
