"""Django settings for application development environments."""

from reactor.conf import env

from . import common


class Settings(common.Settings):
    """Settings for application development environments."""

    # Debugging

    DEBUG = env.bool("DEBUG", default=True)

    # Security

    SECRET_KEY = env.str("SECRET_KEY", default="secret-key")

    # URLs

    @classmethod
    def get_urlpatterns(cls):
        """Return shared routes with local media serving when debugging is enabled."""
        urlpatterns = super().get_urlpatterns()

        from django.conf import settings
        from django.conf.urls.static import static

        urlpatterns += [
            *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
        ]

        return urlpatterns

    # Storages

    def get_storage_config(self, storage_alias):
        """Return local file storage settings for the requested alias.

        The `staticfiles` alias uses Django's development static file storage.
        Other aliases store uploads in separate subdirectories of `MEDIA_ROOT`,
        with matching URL prefixes under `MEDIA_URL`. Environment storage
        configuration is not used.
        """
        if storage_alias == "staticfiles":
            return {
                "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
            }

        return {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
            "OPTIONS": {
                "location": self.MEDIA_ROOT / storage_alias,
                "base_url": self.MEDIA_URL + storage_alias + "/",
            },
        }

    STATIC_ROOT = common.Settings.BASE_DIR / "staticfiles"

    STATIC_URL = "/static/"

    MEDIA_ROOT = common.Settings.BASE_DIR / "media"

    MEDIA_URL = "/media/"


Settings.export()
