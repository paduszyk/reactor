"""Root URL configuration supplied by the active settings class."""

from django.conf import settings

from .settings.base import get_settings_class

_settings_class = get_settings_class(settings.SETTINGS_MODULE)

urlpatterns = _settings_class.get_urlpatterns()
