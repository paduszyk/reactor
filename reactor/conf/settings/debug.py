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


for settings_mixin in SettingsMixin.__subclasses__():
    if settings_mixin.is_active():
        Settings = type("Settings", (settings_mixin, Settings), {})

Settings.load(__name__)
