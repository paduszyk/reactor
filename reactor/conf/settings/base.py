import inspect
import sys
from importlib import import_module

from decouple import config

settings_module_name = config("DJANGO_SETTINGS_MODULE", cast=str)

settings_class_name = "Settings"


class Settings:
    @classmethod
    def load(cls):
        instance = cls()
        module = sys.modules[settings_module_name]

        for name, value in inspect.getmembers(instance):
            if not cls._is_setting_name(name):
                continue

            if isinstance(value, property):
                value = value.fget(instance)  # noqa: PLW2901

            setattr(module, name, value)

    @classmethod
    def get_urlpatterns(cls):
        return []

    @classmethod
    def _is_setting_name(cls, name):
        return hasattr(cls, name) and name.isupper() and not name.startswith("_")


def get_settings_class():
    settings_module = import_module(settings_module_name)

    return getattr(settings_module, settings_class_name)
