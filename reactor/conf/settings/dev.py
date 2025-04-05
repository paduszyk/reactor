from abc import ABC, abstractmethod
from functools import reduce

from decouple import config

from .common import Settings as Common


class Settings(Common):
    # Debugging

    DEBUG = config("DJANGO_DEBUG", cast=bool, default=True)

    # Security

    SECRET_KEY = config("DJANGO_SECRET_KEY", default="django-insecure-secret-key")


class SettingsMixin(ABC):
    @classmethod
    @abstractmethod
    def is_active(cls):
        pass


def apply_settings_mixin(base, mixin):
    if mixin.is_active():

        class Settings(mixin, base):
            pass

        return Settings

    return base


Settings = reduce(apply_settings_mixin, SettingsMixin.__subclasses__(), Settings)

Settings.load(__name__)
