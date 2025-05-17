from importlib import import_module

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


@plugins.register
class DebugToolbarPlugin(plugins.Plugin):
    @classmethod
    def is_active(cls):
        try:
            import_module("debug_toolbar")
        except ModuleNotFoundError:
            return False

        return env.bool("DJANGO_DEBUG_TOOLBAR", default=True)

    # Security

    INTERNAL_IPS = [
        "127.0.0.1",
    ]

    # Apps

    @property
    def INSTALLED_APPS(self):
        return [
            *super().INSTALLED_APPS,
            "debug_toolbar",
        ]

    # Middleware

    @property
    def MIDDLEWARE(self):
        return [
            *super().MIDDLEWARE,
            "debug_toolbar.middleware.DebugToolbarMiddleware",
        ]

    # URLs

    @classmethod
    def get_urlpatterns(cls):
        from django.urls import include, path

        return [
            *super().get_urlpatterns(),
            path("__debug__/", include("debug_toolbar.urls")),
        ]


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
