from decouple import Csv, config

from .common import Settings as Common


class Settings(Common):
    # Debugging

    DEBUG = False

    # Security

    SECRET_KEY = config("SECRET_KEY")

    ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())

    CSRF_TRUSTED_ORIGINS = config("CSRF_TRUSTED_ORIGINS", cast=Csv())

    # Middleware

    @property
    def MIDDLEWARE(self):
        middleware = super().MIDDLEWARE.copy()

        # Insert the `whitenoise` middleware right after Django's `SecurityMiddleware`:
        # https://whitenoise.readthedocs.io/en/stable/django.html#enable-whitenoise.

        security_middleware_index = middleware.index(
            "django.middleware.security.SecurityMiddleware",
        )

        middleware.insert(
            security_middleware_index + 1,
            "whitenoise.middleware.WhiteNoiseMiddleware",
        )

        return middleware

    # WSGI

    WSGI_APPLICATION = "reactor.conf.wsgi.application"

    # Storages

    STORAGES = {
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }


Settings.load(__name__)
