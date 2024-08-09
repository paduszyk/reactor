__all__ = [
    "urlpatterns",
]

from django.conf import settings
from django.utils.module_loading import import_string

Configuration = import_string(settings.CONFIGURATION)

urlpatterns = Configuration.get_urlpatterns()
