from environs import env

from reactor.conf.settings import build_settings, plugins

from .common import CommonSettings


@plugins.register
class DotenvPlugin(plugins.Plugin):
    @classmethod
    def is_active(cls):
        return cls.DOTENV_FILE.exists()

    @classmethod
    def pre_load(cls):
        super().pre_load()

        env.read_env(path=cls.DOTENV_FILE)

    # Paths

    DOTENV_FILE = CommonSettings.BASE_DIR / ".env"


class DevSettings(CommonSettings):
    # Debugging

    DEBUG = env.bool("DJANGO_DEBUG", default=True)

    # Security

    SECRET_KEY = env.str("DJANGO_SECRET_KEY", default="django-insecure-secret-key")

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

    STATIC_ROOT = CommonSettings.BASE_DIR / "staticfiles"

    MEDIA_URL = "media/"

    MEDIA_ROOT = CommonSettings.BASE_DIR / "media"


Settings = build_settings(base=DevSettings)

Settings.load(__name__)
