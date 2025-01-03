import os

from django.utils.module_loading import import_string


def get_settings_class():
    settings_module = os.environ["DJANGO_SETTINGS_MODULE"]

    return import_string(f"{settings_module}.Settings")
