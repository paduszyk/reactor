from django.core.exceptions import ImproperlyConfigured


class AppURLs:
    def __init_subclass__(cls):
        super().__init_subclass__()

        if not hasattr(cls, "urlpatterns"):
            msg = (
                f"{AppURLs.__module__}.{AppURLs.__name__} subclasses must define "
                f"'urlpatterns' attribute: {cls.__module__}.{cls.__name__}"
            )
            raise ImproperlyConfigured(msg)
