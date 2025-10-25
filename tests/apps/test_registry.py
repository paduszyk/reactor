import pytest

from reactor.apps import registry


def test_apps_get_app_configs_returns_app_configs_within_registry_package(mocker):
    # Arrange.
    apps = registry.Apps("package_a")

    class AppConfigA:
        name = "package_a.app_a"
        label = "app_a"

        def get_models(self):
            return []

    app_config_a = AppConfigA()

    class AppConfigB:
        name = "package_b.app_b"
        label = "app_b"

        def get_models(self):
            return []

    app_config_b = AppConfigB()

    # Mock.
    mocker.patch(
        "django.apps.registry.apps.get_app_configs",
        return_value=[app_config_a, app_config_b],
    )

    # Act.
    app_configs = apps.get_app_configs()

    # Assert.
    assert app_config_a in app_configs
    assert app_config_b not in app_configs


def test_apps_get_app_config_returns_app_config_when_label_found(mocker):
    # Arrange.
    apps = registry.Apps("package")

    class AppConfig:
        name = "package.app"
        label = "app"

        def get_models(self):
            return []

    app_config = AppConfig()

    # Mock.
    mocker.patch("django.apps.registry.apps.get_app_configs", return_value=[app_config])

    # Act & assert.
    assert apps.get_app_config("app") == app_config


def test_apps_get_app_config_raises_error_when_label_not_found(mocker):
    # Arrange.
    apps = registry.Apps("package")

    class AppConfig:
        name = "package.app"
        label = "app"

        def get_models(self):
            return []

    app_config = AppConfig()

    # Mock.
    mocker.patch("django.apps.registry.apps.get_app_configs", return_value=[app_config])

    # Act & assert.
    with pytest.raises(registry.AppConfigNotFoundError):
        apps.get_app_config("does_not_exist")


def test_apps_get_models_returns_models_from_apps_within_registry_package(mocker):
    # Arrange.
    apps = registry.Apps("package_a")

    class ModelA:
        class Meta:
            label = "app_a.ModelA"

            @property
            def label_lower(self):
                return self.label.lower()

        _meta = Meta()

    class AppConfigA:
        name = "package_a.app_a"
        label = "app_a"

        def get_models(self):
            return [ModelA]

    app_config_a = AppConfigA()

    class ModelB:
        class Meta:
            label = "app_b.ModelB"

            @property
            def label_lower(self):
                return self.label.lower()

        _meta = Meta()

    class AppConfigB:
        name = "package_b.app_b"
        label = "app_b"

        def get_models(self):
            return [ModelB]

    app_config_b = AppConfigB()

    # Mock.
    mocker.patch(
        "django.apps.registry.apps.get_app_configs",
        return_value=[app_config_a, app_config_b],
    )

    # Act.
    models = apps.get_models()

    # Assert.
    assert ModelA in models
    assert ModelB not in models


@pytest.mark.parametrize(
    "model_name_or_label",
    [
        pytest.param("Model", id="name"),
        pytest.param("model", id="name (lowercase)"),
        pytest.param("app.Model", id="label"),
        pytest.param("app.model", id="label (lowercase)"),
    ],
)
def test_apps_get_model_returns_model_when_either_name_or_label_found(mocker, model_name_or_label):  # fmt: skip
    # Arrange.
    apps = registry.Apps("package")

    class Model:
        class Meta:
            label = "app.Model"

            @property
            def label_lower(self):
                return self.label.lower()

        _meta = Meta()

    class AppConfig:
        name = "package.app"
        label = "app"

        def get_models(self):
            return [Model]

    app_config = AppConfig()

    # Mock.
    mocker.patch("django.apps.registry.apps.get_app_configs", return_value=[app_config])

    # Act & assert.
    assert apps.get_model(model_name_or_label) is Model


@pytest.mark.parametrize(
    "model_name_or_label",
    [
        pytest.param("DoesNotExist", id="name"),
        pytest.param("app.DoesNotExist", id="label"),
    ],
)
def test_apps_get_model_raises_error_when_neither_name_nor_label_found(mocker, model_name_or_label):  # fmt: skip
    # Arrange.
    apps = registry.Apps("package")

    class Model:
        class Meta:
            label = "app.Model"

            @property
            def label_lower(self):
                return self.label.lower()

        _meta = Meta()

    class AppConfig:
        name = "package.app"
        label = "app"

        def get_models(self):
            return [Model]

    app_config = AppConfig()

    # Mock.
    mocker.patch("django.apps.registry.apps.get_app_configs", return_value=[app_config])

    # Act & assert.
    with pytest.raises(registry.ModelNotFoundError):
        apps.get_model(model_name_or_label)


@pytest.mark.parametrize(
    "model_name",
    [
        pytest.param("Model", id="name"),
        pytest.param("model", id="name (lowercase)"),
    ],
)
def test_apps_get_model_raises_error_when_multiple_models_with_same_name_found(mocker, model_name):  # fmt: skip
    # Arrange.
    apps = registry.Apps("package")

    class ModelA:
        class Meta:
            label = "app_a.Model"

            @property
            def label_lower(self):
                return self.label.lower()

        _meta = Meta()

    class AppConfigA:
        name = "package.app_a"
        label = "app_a"

        def get_models(self):
            return [ModelA]

    app_config_a = AppConfigA()

    class ModelB:
        class Meta:
            label = "app_b.Model"

            @property
            def label_lower(self):
                return self.label.lower()

        _meta = Meta()

    class AppConfigB:
        name = "package.app_b"
        label = "app_b"

        def get_models(self):
            return [ModelB]

    app_config_b = AppConfigB()

    # Mock.
    mocker.patch(
        "django.apps.registry.apps.get_app_configs",
        return_value=[app_config_a, app_config_b],
    )

    # Act & assert.
    with pytest.raises(registry.MultipleModelsFoundError):
        apps.get_model(model_name)
