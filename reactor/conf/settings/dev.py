from functools import reduce

from decouple import config

from .common import Settings as Common


class Settings(Common):
    # Debugging

    DEBUG = config("DJANGO_DEBUG", cast=bool, default=True)

    # Security

    SECRET_KEY = config("DJANGO_SECRET_KEY", default="django-insecure-secret-key")


class SettingsMixin:
    @classmethod
    def is_active(cls):
        raise NotImplementedError


class DebugToolbarMixin(SettingsMixin):
    @classmethod
    def is_active(cls):
        try:
            import debug_toolbar  # noqa: F401
        except ModuleNotFoundError:
            return False
        else:
            return True

    # Security

    INTERNAL_IPS = [
        "127.0.0.1",
    ]

    # Apps

    @property
    def INSTALLED_APPS(self):  # noqa: N802
        return [
            *super().INSTALLED_APPS,
            "debug_toolbar",
        ]

    # Middleware

    @property
    def MIDDLEWARE(self):  # noqa: N802
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


def apply_settings_mixin(base, mixin):
    if mixin.is_active():

        class Settings(mixin, base):
            pass

        return Settings

    return base


Settings = reduce(apply_settings_mixin, SettingsMixin.__subclasses__(), Settings)

Settings.load(__name__)
