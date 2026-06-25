import functools

from django.core import checks as django_checks
from django.core.checks import Error

from reactor.apps.config import AppConfig
from reactor.apps.registry import apps
from reactor.db.models import Model


def register(check=None, *tags, **options):
    def decorator(check):
        @functools.wraps(check)
        def wrapper(app_configs=None, **kwargs):
            if app_configs is None:
                app_configs = apps.get_app_configs()
            else:
                app_configs = [
                    app_config
                    for app_config in app_configs
                    if apps.is_app_installed(app_config.label)
                ]

            return check(app_configs, **kwargs)

        django_checks.register(wrapper, *tags, **options)

        return wrapper

    if callable(check):
        return decorator(check)

    if check is not None:
        tags += (check,)

    return decorator


@register
def check_first_party_app_config_class(app_configs, **kwargs):
    messages = []

    for app_config in app_configs:
        if not isinstance(app_config, AppConfig):
            messages += [
                Error(
                    msg=(
                        f"First-party app config class for app '{app_config.label}' "
                        f"does not inherit from {AppConfig.__module__}.{AppConfig.__name__}."  # noqa: E501
                    ),
                    obj=app_config,
                    id="core.apps.E001",
                ),
            ]

    return messages


@register
def check_first_party_model_class(app_configs, **kwargs):
    messages = []

    for app_config in app_configs:
        if not isinstance(app_config, AppConfig):
            continue

        models = app_config.get_models()

        for model in models:
            if not issubclass(model, Model):
                messages += [
                    Error(
                        msg=(
                            f"First-party app model '{model._meta.label}' does not "
                            f"inherit from {Model.__module__}.{Model.__name__}."
                        ),
                        obj=model,
                        id="core.models.E001",
                    ),
                ]

    return messages
