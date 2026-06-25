from importlib import import_module

from django import apps as django_apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.urls import include, path
from django.utils.module_loading import import_string

from .settings import AppSettings
from .urls import AppURLs

_CONF_MODULE_NAME = "conf"

_CONF_SETTINGS_INSTANCE_NAME = "settings"

_CONF_URLS_INSTANCE_NAME = "urls"

_CHECKS_MODULE_NAME = "checks"

_SIGNAL_RECEIVERS_MODULE_NAME = "signals"


class AppConfig(django_apps.AppConfig):
    _ready_hooks = (
        "_load_settings",
        "_append_urlpatterns",
        "_register_checks",
        "_connect_signal_receivers",
        "_call_model_ready_hooks",
    )

    def __init_subclass__(cls):
        super().__init_subclass__()

        if "default" not in cls.__dict__:
            cls.default = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._is_ready = False

    def ready(self):
        super().ready()

        if self._is_ready:
            return

        for ready_hook in self._ready_hooks:
            getattr(self, ready_hook)()

        self._is_ready = True

    def _import_module(self, module_name):
        module_path = f"{self.name}.{module_name}"

        try:
            return import_module(module_path)
        except ModuleNotFoundError as exc:
            if exc.name != module_path:
                msg = (
                    f"module {module_path} exists but failed to import due to missing "
                    f"dependency: {exc.name}; check imports in {module_path}"
                )
                raise ImproperlyConfigured(msg) from exc

    def _import_from_conf_module(self, attr_name, attr_type):
        conf_module = self._import_module(_CONF_MODULE_NAME)

        if conf_module is None:
            return None

        if not hasattr(conf_module, attr_name):
            return None

        attr = getattr(conf_module, attr_name)

        if not isinstance(attr, attr_type):
            msg = (
                f"'{attr_name}' object in {self.name}.conf must be an instance of "
                f"{attr_type}; got {type(attr)}"
            )
            raise ImproperlyConfigured(msg)

        return attr

    def _load_settings(self):
        self._import_from_conf_module(_CONF_SETTINGS_INSTANCE_NAME, AppSettings)

    def _append_urlpatterns(self):
        urls = self._import_from_conf_module(_CONF_URLS_INSTANCE_NAME, AppURLs)

        if urls is None:
            return

        urlpatterns = import_string(f"{settings.ROOT_URLCONF}.urlpatterns")

        route = getattr(urls, "route", "")
        app_name = getattr(urls, "app_name", None) or self.label

        urlpatterns.append(path(route, include((urls, app_name))))

    def _register_checks(self):
        self._import_module(_CHECKS_MODULE_NAME)

    def _connect_signal_receivers(self):
        self._import_module(_SIGNAL_RECEIVERS_MODULE_NAME)

    def _call_model_ready_hooks(self):
        from reactor.db.models import Model

        models = self.get_models()

        for model in models:
            if not issubclass(model, Model):
                continue

            model.ready()
