from abc import ABC, abstractmethod

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


for settings_mixin in SettingsMixin.__subclasses__():
    if settings_mixin.is_active():
        Settings = type("Settings", (settings_mixin, Settings), {})

Settings.load(__name__)
