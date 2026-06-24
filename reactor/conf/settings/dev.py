from environs import EnvError, env

from .common import CommonSettings

env.read_env()


class DevSettings(CommonSettings):
    # Debugging

    DEBUG = env.bool("DJANGO_DEBUG", default=True)

    # Security

    SECRET_KEY = env.str("DJANGO_SECRET_KEY", default="django-secret-key")

    # Databases

    @property
    def DATABASES(self):
        try:
            return {
                "default": env.dj_db_url("DJANGO_DATABASE_URL"),
            }
        except EnvError:
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
