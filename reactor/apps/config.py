__all__ = [
    "AppConfig",
]

from contextlib import suppress
from importlib import import_module

from django import apps
from django.conf import settings
from django.urls import include, path
from django.utils.module_loading import import_string


class AppConfig(apps.AppConfig):
    def ready(self):
        super().ready()

        self._load_conf()
        self._register_checks()
        self._connect_signals()
        self._models_ready()

    def _load_conf(self):
        if not (conf_module := self._import_module("conf")):
            return

        if not (urls := getattr(conf_module, "urls", None)):
            return

        urlpatterns = import_string(f"{settings.ROOT_URLCONF}.urlpatterns")

        route = getattr(urls, "route", "")
        app_name = getattr(urls, "app_name", self.label)

        urlpatterns.append(path(route, include((urls, app_name))))

    def _register_checks(self):
        self._import_module("checks")

    def _connect_signals(self):
        self._import_module("signals")

        models = self.get_models()

        from reactor.db.models import Model
        from reactor.db.models.dispatch import connect_signals

        for model in models:
            if not issubclass(model, Model):
                continue

            connect_signals(model)

    def _models_ready(self):
        models = self.get_models()

        from reactor.db.models import Model

        for model in models:
            if not issubclass(model, Model):
                continue

            model.ready()

    def _import_module(self, module_name):
        with suppress(ImportError):
            return import_module(f"{self.name}.{module_name}")
