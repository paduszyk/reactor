from .settings import get_settings_class

Settings = get_settings_class()

urlpatterns = Settings.get_urlpatterns()
