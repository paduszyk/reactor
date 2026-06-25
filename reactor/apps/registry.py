import functools


def requires_populated(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self._populated:
            self._populate()

        return method(self, *args, **kwargs)

    return wrapper


class AppRegistry:
    class AppNotFoundError(LookupError):
        msg = "app with label '{app_label}' not found"

        def __init__(self, app_label):
            msg = self.msg.format(app_label=app_label)
            super().__init__(msg)

    class ModelNotFoundError(LookupError):
        msg = "model with {model_identifier} '{model_name_or_label}' not found"

        def __init__(self, model_name_or_label):
            msg = self.msg.format(
                model_identifier="label" if "." in model_name_or_label else "name",
                model_name_or_label=model_name_or_label,
            )
            super().__init__(msg)

    class MultipleModelsFoundError(LookupError):
        msg = "multiple models named '{model_name}' found: {model_candidates}"

        def __init__(self, model_name, model_candidates):
            msg = self.msg.format(
                model_name=model_name,
                model_candidates=", ".join(
                    f"{model_candidate._meta.label}"
                    for model_candidate in model_candidates
                ),
            )
            super().__init__(msg)

    def __init__(self, *, root_package=None):
        self._root_package = root_package
        self._app_configs = {}
        self._models = {}
        self._populated = False

    @property
    def root_package(self):
        return self._root_package

    @requires_populated
    def get_app_configs(self):
        return list(self._app_configs.values())

    @requires_populated
    def get_app_config(self, app_label):
        try:
            return self._app_configs[app_label]
        except KeyError as exc:
            raise self.AppNotFoundError(app_label) from exc

    def is_app_installed(self, app_label):
        try:
            self.get_app_config(app_label)
        except self.AppNotFoundError:
            return False

        return True

    @requires_populated
    def get_models(self):
        return list(self._models.values())

    @requires_populated
    def get_model(self, model_name_or_label):
        model_key = model_name_or_label.lower()

        if "." in model_key:
            try:
                return self._models[model_key]
            except KeyError as exc:
                raise self.ModelNotFoundError(model_name_or_label) from exc

        model_candidates = [
            self._models[model_label]
            for model_label in self._models
            if model_label.endswith(f".{model_key}")
        ]

        if not model_candidates:
            raise self.ModelNotFoundError(model_name_or_label)

        if len(model_candidates) > 1:
            raise self.MultipleModelsFoundError(model_name_or_label, model_candidates)

        return model_candidates[0]

    def is_model_registered(self, model_name_or_label):
        try:
            self.get_model(model_name_or_label)
        except self.ModelNotFoundError:
            return False

        return True

    def _populate(self):
        from django.apps.registry import apps as django_apps

        self._app_configs = {
            app_config.label: app_config
            for app_config in django_apps.get_app_configs()
            if app_config.name.startswith(f"{self.root_package}.")
        }
        self._models = {
            model._meta.label.lower(): model
            for app_config in self._app_configs.values()
            for model in app_config.get_models()
        }
        self._populated = True


apps = AppRegistry(root_package="reactor")
