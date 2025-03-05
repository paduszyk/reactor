from abc import ABC, abstractmethod
from pathlib import Path

from environ import Env

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


class DotenvMixin(SettingsMixin):
    @classmethod
    def is_active(cls):
        if (env_file := (Path.cwd() / ".env")).exists():
            cls.env_file = env_file

            return True

        return False

    @classmethod
    def pre_load(cls):
        super().pre_load()

        Env.read_env(cls.env_file, overwrite=False)


class DebugToolbarMixin(SettingsMixin):
    @classmethod
    def is_active(cls):
        try:
            import debug_toolbar  # noqa: F401
        except ModuleNotFoundError:
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
        from debug_toolbar.toolbar import debug_toolbar_urls

        return [
            *super().get_urlpatterns(),
            *debug_toolbar_urls(),
        ]


for settings_mixin in SettingsMixin.__subclasses__():
    if settings_mixin.is_active():
        Settings = type("Settings", (settings_mixin, Settings), {})

Settings.load(__name__)
