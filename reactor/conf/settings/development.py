from abc import ABC, abstractmethod
from importlib import import_module

from environs import env

from .common import Settings as Common


class Settings(Common):
    # Debugging

    DEBUG = True

    # Security

    SECRET_KEY = "django-insecure-secret-key"  # noqa: S105


class SettingsMixin(ABC):
    @classmethod
    @abstractmethod
    def is_active(cls):
        pass


class EnvironMixin(SettingsMixin):
    @classmethod
    def is_active(cls):
        return env.read_env()


class DebugToolbarMixin(SettingsMixin):
    @classmethod
    def is_active(cls):
        try:
            import_module("debug_toolbar")
        except ImportError:
            return False

        return True

    # Security

    INTERNAL_IPS = [
        "127.0.0.1",
    ]

    # Apps

    @property
    def INSTALLED_APPS(self):  # noqa: N802
        return [
            *super().INSTALLED_APPS,
            "debug_toolbar",
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
        from django.urls import include, path

        return [
            *super().get_urlpatterns(),
            path("__debug__/", include("debug_toolbar.urls")),
        ]


for settings_mixin in SettingsMixin.__subclasses__():
    if settings_mixin.is_active():
        Settings = type("Settings", (settings_mixin, Settings), {})

Settings.load(__name__)
