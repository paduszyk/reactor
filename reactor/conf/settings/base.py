import inspect
import re
from importlib import import_module

from decouple import config

from django.utils.module_loading import import_string

settings_module_name = config("DJANGO_SETTINGS_MODULE")

settings_module = import_module(settings_module_name)

settings_class_name = "Settings"


class Settings:
    @classmethod
    def pre_load(cls):
        pass

    @classmethod
    def load(cls):
        cls.pre_load()

        instance = cls()

        for name, value in inspect.getmembers(instance):
            if not cls._is_setting_name(name):
                continue

            if isinstance(value, property):
                value = value.fget(instance)  # noqa: PLW2901

            setattr(settings_module, name, value)

        setattr(settings_module, settings_class_name, cls)

        cls.__name__ = settings_class_name
        cls.__qualname__ = settings_class_name
        cls.__module__ = settings_module_name

        for name in settings_module.__dict__.copy():
            if cls._in_settings_module(name):
                continue

            delattr(settings_module, name)

    @classmethod
    def get_urlpatterns(cls):
        return []

    @classmethod
    def _is_setting_name(cls, name):
        return hasattr(cls, name) and name.isupper() and not name.startswith("_")

    @classmethod
    def _in_settings_module(cls, name):
        return (
            name == settings_class_name
            or cls._is_setting_name(name)
            or re.match(r"__\w+__", name)
        )


def get_settings_class():
    return import_string(f"{settings_module_name}.{settings_class_name}")
