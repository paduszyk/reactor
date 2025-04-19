from decouple import Csv, config

from .common import Settings as Common


class Settings(Common):
    # Debugging

    DEBUG = False

    # Security

    SECRET_KEY = config("DJANGO_SECRET_KEY", cast=str)

    ALLOWED_HOSTS = config("DJANGO_ALLOWED_HOSTS", cast=Csv())

    CSRF_TRUSTED_ORIGINS = config("DJANGO_CSRF_TRUSTED_ORIGINS", cast=Csv())

    # Middleware

    @property
    def MIDDLEWARE(self):  # noqa: N802
        middleware = super().MIDDLEWARE.copy()

        # Insert `whitenoise` middleware right after Django's `SecurityMiddleware`:
        # https://whitenoise.readthedocs.io/en/stable/django.html#enable-whitenoise.

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
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }

    STATIC_URL = "static/"

    STATIC_ROOT = Common.BASE_DIR / "staticfiles"

    # WSGI

    WSGI_APPLICATION = "reactor.conf.wsgi.application"


Settings.load(__name__)
