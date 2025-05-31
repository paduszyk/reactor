from decouple import config

from .common import Settings as Common


class Settings(Common):
    # Debugging

    DEBUG = config("DJANGO_DEBUG", cast=bool, default=True)

    # Security

    SECRET_KEY = config("DJANGO_SECRET_KEY", default="django-secret-key")

    # Storages

    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }

    STATIC_URL = "static/"

    STATIC_ROOT = Common.BASE_DIR / "staticfiles"

    MEDIA_URL = "media/"

    MEDIA_ROOT = Common.BASE_DIR / "media"


Settings.load()
