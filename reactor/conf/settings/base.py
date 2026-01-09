import functools
import inspect
from abc import ABC, abstractmethod
from importlib import import_module

from decouple import config as env

from django.utils.module_loading import import_string

SETTINGS_MODULE_NAME = env("DJANGO_SETTINGS_MODULE")

SETTINGS_CLASS_NAME = "Settings"


class BasePlugin(ABC):
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


def _is_setting_name(name):
    return name.isupper() and not name.startswith("_")


def _in_settings_module(name):
    return (
        name == SETTINGS_CLASS_NAME
        or _is_setting_name(name)
        or (name.startswith("__") and name.endswith("__"))
    )


class BaseSettings(ABC):
    @classmethod  # noqa: B027
    def pre_load(cls):
        pass

    @classmethod  # noqa: B027
    def post_load(cls):
        pass

    @classmethod
    def load(cls):
        cls = functools.reduce(_apply_plugin, BasePlugin.__subclasses__(), cls)  # noqa: PLW0642

        module = import_module(SETTINGS_MODULE_NAME)
        instance = cls()

        cls.pre_load()

        for name, value in inspect.getmembers(cls):
            if not _is_setting_name(name):
                continue

            if isinstance(value, property):
                value = value.fget(instance)  # noqa: PLW2901

            setattr(module, name, value)

        cls.post_load()

        cls.__name__ = SETTINGS_CLASS_NAME
        cls.__qualname__ = SETTINGS_CLASS_NAME
        cls.__module__ = SETTINGS_MODULE_NAME

        setattr(module, SETTINGS_CLASS_NAME, cls)

        for name in module.__dict__.copy():
            if _in_settings_module(name):
                continue

            delattr(module, name)

    @classmethod
    @abstractmethod
    def get_urlpatterns(cls):
        pass


def get_settings_class():
    return import_string(f"{SETTINGS_MODULE_NAME}.{SETTINGS_CLASS_NAME}")
