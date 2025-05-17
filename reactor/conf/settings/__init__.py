from functools import reduce

from environs import env

from django.utils.module_loading import import_string

from .base import plugins

SETTINGS_MODULE_NAME = env.str("DJANGO_SETTINGS_MODULE")

SETTING_CLASS_NAME = "Settings"


def build_settings(base):
    def apply_plugin(base, plugin):
        class Settings(plugin, base):
            pass

        return Settings

    active_plugins = plugins.get_active_plugins()

    return reduce(apply_plugin, active_plugins, base)


def get_settings():
    return import_string(f"{SETTINGS_MODULE_NAME}.{SETTING_CLASS_NAME}")
