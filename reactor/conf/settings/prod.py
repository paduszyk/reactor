from decouple import Csv, config

from .common import Settings as Common


class Settings(Common):
    # Debugging

    DEBUG = False

    # Security

    SECRET_KEY = config("DJANGO_SECRET_KEY")

    ALLOWED_HOSTS = config("DJANGO_ALLOWED_HOSTS", cast=Csv())

    SESSION_COOKIE_SECURE = True

    CSRF_COOKIE_SECURE = True

    CSRF_TRUSTED_ORIGINS = config("DJANGO_CSRF_TRUSTED_ORIGINS", cast=Csv())

    # Middleware

    @property
    def MIDDLEWARE(self):
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

    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.azure_storage.AzureStorage",
            "OPTIONS": {
                "connection_string": config("AZURE_CONNECTION_STRING"),
                "azure_container": config("AZURE_CONTAINER"),
            },
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }

    STATIC_URL = "static/"

    STATIC_ROOT = Common.BASE_DIR / "staticfiles"


Settings.load()
