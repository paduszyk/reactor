from environs import env

from .base import BasePlugin
from .common import CommonSettings


class DotenvPlugin(BasePlugin):
    @classmethod
    def is_active(cls):
        return cls.DOTENV_FILE.exists()

    @classmethod
    def pre_load(cls):
        super().pre_load()

        env.read_env(cls.DOTENV_FILE)

    # Paths

    DOTENV_FILE = CommonSettings.BASE_DIR / ".env"


class DevSettings(CommonSettings):
    # Debugging

    DEBUG = env.bool("DJANGO_DEBUG", default=True)

    # Security

    SECRET_KEY = env.str("DJANGO_SECRET_KEY", default="django-secret-key")

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
