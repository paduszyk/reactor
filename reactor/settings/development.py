from environ import Env

from .common import CommonSettings

Env.read_env(env_file=CommonSettings.BASE_DIR / ".env", override=True)

env = Env()


class DevelopmentSettings(CommonSettings):
    # Debugging

    DEBUG = env.bool("DJANGO_DEBUG", default=True)

    # Security

    SECRET_KEY = env.str("DJANGO_SECRET_KEY", default="secret-key")

    # Databases

    @property
    def DATABASES(self):
        if "DJANGO_DATABASE_URL" not in env:
            return {}

        return {
            "default": env.db_url("DJANGO_DATABASE_URL"),
        }

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


DevelopmentSettings.export()
