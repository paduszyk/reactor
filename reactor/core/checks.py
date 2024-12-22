from django.core import checks

from reactor.apps import AppConfig, apps
from reactor.db import models


@checks.register()
def check_app_config_base_class(app_configs=None, **kwargs):
    app_configs = app_configs or apps.get_app_configs()

    return [
        checks.Error(
            (
                f"AppConfig should be subclassed from "
                f"{AppConfig.__module__}.{AppConfig.__name__}."
            ),
            obj=f"<AppConfig: {app_config.label}>",
            id="reactor.E001",
        )
        for app_config in app_configs
        if not isinstance(app_config, AppConfig)
    ]


@checks.register()
def check_model_base_class(app_configs=None, **kwargs):
    app_configs = app_configs or apps.get_app_configs()

    return [
        checks.Error(
            (
                f"Model should be subclassed from "
                f"{models.Model.__module__}.{models.Model.__name__}."
            ),
            obj=f"<Model: {model._meta.label}>",
            id="reactor.E002",
        )
        for model in apps.get_models()
        if not issubclass(model, models.Model)
    ]
