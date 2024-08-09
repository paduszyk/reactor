__all__ = [
    "AppConfig",
]

from contextlib import suppress
from importlib import import_module

from django import apps
from django.utils.module_loading import import_string

CHECKS_MODULE_NAME = "checks"

SIGNALS_MODULE_NAME = "signals"

SETTINGS_MODULE_NAME = "conf.settings"

URLS_MODULE_NAME = "conf.urls"


class AppConfig(apps.AppConfig):
    """Represents a base for configuring first-party apps."""

    def ready(self):
        super().ready()

        self._register_system_checks()
        self._connect_signal_receivers()
        self._load_settings()
        self._append_urlpatterns()

    def _import_module(self, module_name):
        with suppress(ImportError):
            return import_module(f"{self.name}.{module_name}")

    def _register_system_checks(self):
        self._import_module(CHECKS_MODULE_NAME)

    def _connect_signal_receivers(self):
        self._import_module(SIGNALS_MODULE_NAME)

    def _load_settings(self):
        self._import_module(SETTINGS_MODULE_NAME)

    def _append_urlpatterns(self):
        if (urls_module := self._import_module(URLS_MODULE_NAME)) is None:
            return

        from django.conf import settings
        from django.urls import include, path

        urlpatterns = import_string(f"{settings.ROOT_URLCONF}.urlpatterns")

        route = getattr(urls_module, "route", "")
        app_name = getattr(urls_module, "app_name", self.label)

        urlpatterns.append(path(route, include((urls_module, app_name))))
