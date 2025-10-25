__all__ = [
    "AppConfig",
]

from contextlib import suppress
from importlib import import_module

from django.apps.config import AppConfig as BaseAppConfig
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.urls import include, path
from django.utils.module_loading import import_string


class AppConfig(BaseAppConfig):
    def __init_subclass__(cls):
        super().__init_subclass__()

        if not hasattr(cls, "default"):
            cls.default = True

    def ready(self):
        super().ready()

        self._load_settings()
        self._append_urlpatterns()
        self._register_checks()
        self._connect_signals()
        self._models_ready()

    def _import_module(self, module_name):
        with suppress(ModuleNotFoundError):
            return import_module(f"{self.name}.{module_name}")

    def _load_settings(self):
        if not (
            (conf_module := self._import_module("conf"))
            and (settings := getattr(conf_module, "settings", None)) is not None
        ):
            return

        from reactor.conf.settings import AppSettings

        if not isinstance(settings, AppSettings):
            msg = (
                f"'settings' object in {self.name}.conf must be an instance of "
                f"{AppSettings}; got {type(settings)}"
            )
            raise ImproperlyConfigured(msg)

    def _append_urlpatterns(self):
        if not (
            (conf_module := self._import_module("conf"))
            and (urls := getattr(conf_module, "urls", None)) is not None
        ):
            return

        from reactor.conf.urls import AppURLs

        if not isinstance(urls, AppURLs):
            msg = (
                f"'urls' object in {self.name}.conf must be an instance of "
                f"{AppURLs}; got {type(urls)}"
            )
            raise ImproperlyConfigured(msg)

        route = getattr(urls, "route", "")
        app_name = getattr(urls, "app_name", self.label)

        urlpatterns = import_string(f"{settings.ROOT_URLCONF}.urlpatterns")

        urlpatterns.append(path(route, include((urls, app_name))))

    def _register_checks(self):
        self._import_module("checks")

    def _connect_signals(self):
        self._import_module("signals")

    def _models_ready(self):
        models = self.get_models()

        from reactor.db.models.base import Model

        for model in models:
            if not issubclass(model, Model):
                continue

            model.ready()
