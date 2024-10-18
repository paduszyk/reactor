import os

from django.utils.module_loading import import_string


def get_settings_class():
    """Return the settings class for the active environment.

    The active environment is determined by the `DJANGO_SETTINGS_MODULE` variable.
    """
    settings_module_path = os.environ["DJANGO_SETTINGS_MODULE"]

    return import_string(f"{settings_module_path}.Settings")
