__all__ = [
    "apps",
]

import functools
import threading


class AppConfigNotFoundError(LookupError):
    msg = "app with label '{app_label}' not found"

    def __init__(self, app_label):
        super().__init__(self.msg.format(app_label=app_label))


class ModelNotFoundError(LookupError):
    msg = "model with {model_identifier} '{model_name_or_label}' not found"

    def __init__(self, model_name_or_label):
        super().__init__(
            self.msg.format(
                model_identifier="label" if "." in model_name_or_label else "name",
                model_name_or_label=model_name_or_label,
            ),
        )


class MultipleModelsFoundError(LookupError):
    msg = "multiple models named '{model_name}' found: {model_candidates}"

    def __init__(self, model_name, model_candidates):
        super().__init__(
            self.msg.format(
                model_name=model_name,
                model_candidates=", ".join(
                    f"{model_candidate._meta.label}"
                    for model_candidate in model_candidates
                ),
            ),
        )


def _ensure_populated(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self._populated:
            self._populate()

        return method(self, *args, **kwargs)

    return wrapper


class Apps:
    def __init__(self, package):
        self._package = package
        self._app_configs = {}
        self._models = {}
        self._populated = False
        self._lock = threading.RLock()

    def __repr__(self):
        return f"<{type(self).__name__} registry: package={self.package}>"

    @property
    def package(self):
        return self._package

    @_ensure_populated
    def get_app_configs(self):
        return list(self._app_configs.values())

    @_ensure_populated
    def get_app_config(self, app_label):
        try:
            return self._app_configs[app_label]
        except KeyError as exc:
            raise AppConfigNotFoundError(app_label) from exc

    @_ensure_populated
    def get_models(self):
        return list(self._models.values())

    @_ensure_populated
    def get_model(self, model_name_or_label):
        model_key = model_name_or_label.lower()

        if "." in model_key:
            try:
                return self._models[model_key]
            except KeyError as exc:
                raise ModelNotFoundError(model_name_or_label) from exc

        model_candidates = [
            self._models[model_label]
            for model_label in self._models
            if model_label.endswith(f".{model_key}")
        ]

        if not model_candidates:
            raise ModelNotFoundError(model_name_or_label)

        if len(model_candidates) > 1:
            raise MultipleModelsFoundError(model_name_or_label, model_candidates)

        return model_candidates[0]

    def _populate(self):
        if self._populated:
            return

        with self._lock:
            if self._populated:
                return

            from django.apps.registry import apps

            self._app_configs = {
                app_config.label: app_config
                for app_config in apps.get_app_configs()
                if app_config.name.startswith(f"{self.package}.")
            }
            self._models = {
                model._meta.label_lower: model
                for app_config in self._app_configs.values()
                for model in app_config.get_models()
            }

            self._populated = True


apps = Apps("reactor")
