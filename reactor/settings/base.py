import abc
import inspect
from importlib import import_module

from environ import Env

env = Env()

_SETTINGS_MODULE_PATH = env.str("DJANGO_SETTINGS_MODULE")

_SETTINGS_CLASS_NAME = "_Settings"


class Extension(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def is_enabled(cls):
        pass


def _get_enabled_extensions():
    extensions = Extension.__subclasses__()

    return [extension for extension in extensions if extension.is_enabled()]


def _apply_enabled_extensions(base_settings_class):
    enabled_extensions = _get_enabled_extensions()

    if not enabled_extensions:
        return base_settings_class

    enabled_extensions.reverse()

    return type(_SETTINGS_CLASS_NAME, (*enabled_extensions, base_settings_class), {})


def _is_setting_name(name):
    return name.isupper() and not name.startswith("_")


def _in_settings_module_exports(name):
    return (
        name == _SETTINGS_CLASS_NAME
        or _is_setting_name(name)
        or (name.startswith("__") and name.endswith("__"))
    )


class Settings(abc.ABC):
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        cls._is_exported = False

    @classmethod
    def export(cls):
        if cls._is_exported:
            return

        settings_module = import_module(_SETTINGS_MODULE_PATH)

        settings_class = _apply_enabled_extensions(cls)
        settings_instance = settings_class()

        for name, value in inspect.getmembers(settings_instance):
            if not _is_setting_name(name):
                continue

            setattr(settings_module, name, value)

        settings_class.__name__ = _SETTINGS_CLASS_NAME
        settings_class.__qualname__ = _SETTINGS_CLASS_NAME
        settings_class.__module__ = _SETTINGS_MODULE_PATH

        for name in settings_module.__dict__.copy():
            if _in_settings_module_exports(name):
                continue

            delattr(settings_module, name)

        setattr(settings_module, _SETTINGS_CLASS_NAME, settings_class)

        cls._is_exported = True

    @classmethod
    @abc.abstractmethod
    def get_urlpatterns(cls):
        pass


def get_settings_class():
    from django.utils.module_loading import import_string

    settings_class_path = f"{_SETTINGS_MODULE_PATH}.{_SETTINGS_CLASS_NAME}"

    return import_string(settings_class_path)
