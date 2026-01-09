import decouple
import dj_database_url as db_url
from decouple import config as env

from .common import CommonSettings


class DevSettings(CommonSettings):
    # Debugging

    DEBUG = env("DJANGO_DEBUG", cast=decouple.strtobool, default="true")

    # Security

    SECRET_KEY = env("DJANGO_SECRET_KEY", default="django-secret-key")

    # Databases

    @property
    def DATABASES(self):
        try:
            return {
                "default": env("DJANGO_DATABASE_URL", cast=db_url.parse),
            }
        except decouple.UndefinedValueError:
            return {}

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
