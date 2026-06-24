import functools
import inspect
from abc import ABC, abstractmethod
from importlib import import_module

from environs import env

from django.utils.module_loading import import_string

_SETTINGS_MODULE_PATH = env.str("DJANGO_SETTINGS_MODULE")

_SETTINGS_CLASS_NAME = "Settings"


def _register_extension(settings_class, extension_class):
    if not extension_class.is_enabled():
        return settings_class

    class ExtendedSettings(extension_class, settings_class):
        pass

    ExtendedSettings.__name__ = settings_class.__name__
    ExtendedSettings.__qualname__ = settings_class.__qualname__
    ExtendedSettings.__module__ = settings_class.__module__

    return ExtendedSettings


def _register_extensions(settings_class):
    extensions = BaseExtension.__subclasses__()

    return functools.reduce(_register_extension, extensions, settings_class)


class BaseExtension(ABC):
    @classmethod
    @abstractmethod
    def is_enabled(cls):
        pass


def _is_setting_name(name):
    return name.isupper() and not name.startswith("_")


def _is_settings_module_export(name):
    return (
        name == _SETTINGS_CLASS_NAME
        or _is_setting_name(name)
        or (name.startswith("__") and name.endswith("__"))
    )


class BaseSettings(ABC):
    @classmethod
    def load(cls):
        settings_module = import_module(_SETTINGS_MODULE_PATH)

        settings_class = _register_extensions(cls)
        settings_instance = settings_class()

        for name, value in inspect.getmembers(settings_instance):
            if not _is_setting_name(name):
                continue

            setting_name = name
            setting_value = (
                value.fget(settings_instance) if isinstance(value, property) else value
            )

            setattr(settings_module, setting_name, setting_value)

        settings_class.__name__ = _SETTINGS_CLASS_NAME
        settings_class.__qualname__ = _SETTINGS_MODULE_PATH
        settings_class.__module__ = _SETTINGS_MODULE_PATH

        setattr(settings_module, _SETTINGS_CLASS_NAME, settings_class)

        for name in settings_module.__dict__.copy():
            if _is_settings_module_export(name):
                continue

            delattr(settings_module, name)

    @classmethod
    @abstractmethod
    def get_urlpatterns(cls):
        pass


def get_settings_class():
    settings_class_path = f"{_SETTINGS_MODULE_PATH}.{_SETTINGS_CLASS_NAME}"

    return import_string(settings_class_path)
