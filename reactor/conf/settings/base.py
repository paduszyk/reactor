import inspect
from abc import ABC, abstractmethod
from importlib import import_module

from decouple import config

from django.utils.module_loading import import_string

settings_module_name = config("DJANGO_SETTINGS_MODULE")

settings_module = import_module(settings_module_name)

settings_class_name = "Settings"


def _is_setting_name(name):
    return name.isupper() and not name.startswith("_")


def _in_settings_module(name):
    return (
        name == settings_class_name
        or _is_setting_name(name)
        or (name.startswith("__") and name.endswith("__"))
    )


class Settings(ABC):
    @classmethod
    def load(cls):
        settings = cls()

        for name, value in inspect.getmembers(cls):
            if not _is_setting_name(name):
                continue

            if isinstance(value, property):
                value = value.fget(settings)  # noqa: PLW2901

            setattr(settings_module, name, value)

        cls.__name__ = settings_class_name
        cls.__qualname__ = settings_class_name
        cls.__module__ = settings_module_name

        setattr(settings_module, settings_class_name, cls)

        for name in settings_module.__dict__.copy():
            if _in_settings_module(name):
                continue

            delattr(settings_module, name)

    @classmethod
    @abstractmethod
    def get_urlpatterns(cls):
        pass


def get_settings_class():
    return import_string(f"{settings_module_name}.{settings_class_name}")
