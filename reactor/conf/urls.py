from .settings.base import get_settings_class

settings_class = get_settings_class()

urlpatterns = settings_class.get_urlpatterns()


class AppURLs:
    def __init_subclass__(cls):
        super().__init_subclass__()

        if not hasattr(cls, "urlpatterns"):
            cls.urlpatterns = []
