from functools import cache
from itertools import chain
from pathlib import Path


@cache
def get_app_configs():
    from django.apps.registry import apps

    return [
        app_config
        for app_config in apps.get_app_configs()
        if Path(__file__).parent in Path(app_config.path).resolve().parents
    ]


@cache
def get_models():
    app_configs = get_app_configs()

    return list(
        chain.from_iterable(app_config.get_models() for app_config in app_configs),
    )
