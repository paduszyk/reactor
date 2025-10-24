from decouple import config

from .common import CommonSettings


class DevSettings(CommonSettings):
    # Debugging

    DEBUG = config("DJANGO_DEBUG", cast=bool, default="true")

    # Security

    SECRET_KEY = config("DJANGO_SECRET_KEY", cast=str, default="django-secret-key")

    # Storages

    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }

    MEDIA_URL = "media/"

    MEDIA_ROOT = CommonSettings.BASE_DIR / "media"

    STATIC_URL = "static/"

    STATIC_ROOT = CommonSettings.BASE_DIR / "staticfiles"


DevSettings.load()
