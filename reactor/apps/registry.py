__all__ = [
    "apps",
]

import re
from itertools import chain


class Apps:
    def __init__(self, name_pattern):
        self._name_pattern = name_pattern
        self._app_configs = {}
        self._models = {}
        self._populated = False

    def __getattribute__(self, name):
        if not name.startswith("_") and not self._populated:
            self._populate()

        return super().__getattribute__(name)

    def get_app_configs(self):
        return list(self._app_configs.values())

    def get_app_config(self, app_label):
        try:
            return self._app_configs[app_label]
        except KeyError as exc:
            msg = f"app with label '{app_label}' not found"

            raise LookupError(msg) from exc

    def get_models(self):
        return list(self._models.values())

    def get_model(self, name_or_label):
        name_or_label = name_or_label.lower()

        candidates = [
            model
            for label, model in self._models.items()
            if label == name_or_label or label.endswith(f".{name_or_label}")
        ]

        if len(candidates) == 1:
            return candidates[0]

        msg = f"model with name or label '{name_or_label}' " + (
            "not found"
            if not candidates
            else (
                f"found in multiple apps: "
                f"{', '.join(f"'{model._meta.app_label}'" for model in candidates)}"
            )
        )

        raise LookupError(msg)

    def _populate(self):
        from django.apps.registry import apps

        self._app_configs = {
            app_config.label: app_config
            for app_config in apps.get_app_configs()
            if re.match(self._name_pattern, app_config.name)
        }
        self._models = {
            model._meta.label_lower: model
            for model in chain.from_iterable(
                app_config.get_models() for app_config in self._app_configs.values()
            )
        }
        self._populated = True


apps = Apps(name_pattern=rf"^{__package__.split('.', 1)[0]}\.")
