"""Django settings for application production environments."""

from reactor.conf import env

from . import common


class Settings(common.Settings):
    """Settings for application production environments."""

    # Debugging

    DEBUG = False

    # Security

    SECRET_KEY = env.str("SECRET_KEY")

    ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

    CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS")

    # Databases

    def get_database_config(self, database_alias):
        """Return the required database configuration for an alias.

        Raises:
            ValueError: `<ALIAS>_DATABASE_URL` is missing, produces an empty
                configuration, or contains invalid connection values.
        """
        database_config = super().get_database_config(database_alias)

        if not database_config:
            msg = (
                f"required production database configuration for {database_alias!r} "
                f"is missing; set {database_alias.upper()}_DATABASE_URL to a valid "
                f"database URL"
            )
            raise ValueError(msg)

        return database_config

    # Middleware

    @property
    def MIDDLEWARE(self):
        """Return middleware with static file serving after security handling."""
        middleware = super().MIDDLEWARE.copy()

        security_middleware_index = middleware.index(
            "django.middleware.security.SecurityMiddleware",
        )

        middleware.insert(
            security_middleware_index + 1,
            "whitenoise.middleware.WhiteNoiseMiddleware",
        )

        return middleware

    # Storages

    def get_storage_config(self, storage_alias):
        """Return storage settings for production uploads or static files.

        The `staticfiles` alias uses compressed static files with manifest-based
        names, ignoring environment storage configuration. Other aliases require
        `<ALIAS>_STORAGE_JSON`, with the alias uppercased.

        Raises:
            ValueError: A required storage configuration is missing, is invalid
                JSON, or is not a non-empty object.
        """
        if storage_alias == "staticfiles":
            return {
                "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
            }

        storage_config = super().get_storage_config(storage_alias)

        if not storage_config:
            msg = (
                f"required production storage configuration for {storage_alias!r} "
                f"is missing; set {storage_alias.upper()}_STORAGE_JSON to a non-empty "
                f"JSON object"
            )
            raise ValueError(msg)

        return storage_config

    STATIC_ROOT = common.Settings.BASE_DIR / "staticfiles"

    STATIC_URL = "/static/"


Settings.export()
