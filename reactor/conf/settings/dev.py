from environ import Env

from . import common

_env = Env()


class Settings(common.Settings):
    """Settings for application development environments."""

    # Debugging

    DEBUG = _env.bool("DEBUG", default=True)

    # Security

    SECRET_KEY = _env.str("SECRET_KEY", default="secret-key")

    # Databases

    def get_database_config(self, database_alias):
        """Parse the database URL configured for an alias in the environment.

        The variable name is the uppercase alias followed by `_DATABASE_URL`.
        An absent variable produces an empty configuration for that alias so
        management commands that do not require a database can run without
        database environment variables.
        """
        database_url_env_name = f"{database_alias.upper()}_DATABASE_URL"

        if database_url_env_name not in _env:
            return {}

        return _env.db(database_url_env_name)

    # URLs

    @classmethod
    def get_urlpatterns(cls):
        """Append development media-serving routes to the shared URL patterns.

        Django's static-file helper uses the active `MEDIA_URL` and `MEDIA_ROOT`
        settings. It adds routes only when `DEBUG` is enabled and `MEDIA_URL` is
        a local URL prefix.
        """
        urlpatterns = super().get_urlpatterns()

        from django.conf import settings
        from django.conf.urls.static import static

        urlpatterns += [
            *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
        ]

        return urlpatterns

    # Storages

    def get_storage_config(self, storage_alias):
        """Configure local storage for a development storage alias.

        The `staticfiles` alias uses Django's static-files storage. Other aliases
        use filesystem storage in an alias-named directory beneath `MEDIA_ROOT`,
        with the corresponding URL beneath `MEDIA_URL`.
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
