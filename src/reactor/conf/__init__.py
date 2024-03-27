from django.utils.module_loading import import_string

__all__ = ["get_configuration_class"]


def get_configuration_class():
    from django.conf import settings

    return import_string(settings.CONFIGURATION)
