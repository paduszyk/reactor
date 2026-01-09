from .settings.base import get_settings_class

settings_class = get_settings_class()

urlpatterns = settings_class.get_urlpatterns()
