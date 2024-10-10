from . import common


class Settings(common.Settings):
    # Debugging

    DEBUG = True

    # Security

    SECRET_KEY = "django-insecure-secret-key"  # noqa: S105

    ALLOWED_HOSTS = ["*"]

    # URLs

    @classmethod
    def get_urlpatterns(cls):
        from django.conf.urls.static import static

        return [
            *super().get_urlpatterns(),
            *static(cls.MEDIA_URL, document_root=cls.MEDIA_ROOT),
        ]

    # Media

    MEDIA_URL = "media/"

    @property
    def MEDIA_ROOT(self):
        return self.BASE_DIR / "media"
