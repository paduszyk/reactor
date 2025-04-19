from decouple import config

from django.utils.module_loading import import_string


def get_settings_class():
    settings_module = config("DJANGO_SETTINGS_MODULE", cast=str)

    return import_string(f"{settings_module}.Settings")
