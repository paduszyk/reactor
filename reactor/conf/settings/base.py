import inspect
import re
from abc import ABC, abstractmethod
from functools import reduce
from importlib import import_module

from decouple import config

from django.utils.module_loading import import_string

settings_module_name = config("DJANGO_SETTINGS_MODULE")

settings_module = import_module(settings_module_name)

settings_class_name = "Settings"


class Plugin(ABC):
    @classmethod
    @abstractmethod
    def is_active(cls):
        pass


def _apply_plugin(base, plugin):
    if not plugin.is_active():
        return base

    class Settings(plugin, base):
        pass

    return Settings


def _is_setting_name(settings_class, name):
    return hasattr(settings_class, name) and name.isupper() and not name.startswith("_")


def _in_settings_module(settings_class, name):
    return (
        name == settings_class_name
        or _is_setting_name(settings_class, name)
        or re.match(r"__\w+__", name)
    )


class Settings(ABC):
    @classmethod
    def load(cls):
        settings_class = reduce(_apply_plugin, Plugin.__subclasses__(), cls)

        settings = settings_class()

        for name, value in inspect.getmembers(settings):
            if not _is_setting_name(settings_class, name):
                continue

            setattr(settings_module, name, value)

        settings_class.__name__ = settings_class_name
        settings_class.__qualname__ = settings_class_name
        settings_class.__module__ = settings_module_name

        setattr(settings_module, settings_class_name, settings_class)

        for name in settings_module.__dict__.copy():
            if _in_settings_module(settings_class, name):
                continue

            delattr(settings_module, name)

    @classmethod
    @abstractmethod
    def get_urlpatterns(cls):
        pass


def get_settings_class():
    return import_string(f"{settings_module_name}.{settings_class_name}")
