import pytest

from reactor.apps.registry import AppRegistry, requires_populated


def test_requires_populated_populates_once_for_same_instance(mocker):
    # Arrange.
    class Registry:
        _populated = False

        def _populate(self):
            self._populated = True

        @requires_populated
        def execute(self):
            return None

    # Spy.
    populate_spy = mocker.spy(Registry, "_populate")

    # Act.
    registry = Registry()
    registry.execute()
    registry.execute()

    # Assert.
    populate_spy.assert_called_once()


def test_app_registry_population_is_idempotent_for_same_registry(mocker):
    # Arrange.
    class AppConfig:
        name = "package.app"
        label = "app"

        def get_models(self):
            return []

    app_config = AppConfig()

    # Mock.
    mocker.patch(
        "django.apps.registry.apps.get_app_configs",
        return_value=[app_config],
    )

    @requires_populated
    def populate(self):
        return None

    mocker.patch.object(AppRegistry, "populate", populate, create=True)

    # Spy.
    _populate_spy = mocker.spy(AppRegistry, "_populate")

    # Act.
    app_registry = AppRegistry(root_package="package")
    app_registry.populate()
    app_registry.populate()

    # Assert.
    _populate_spy.assert_called_once()


def test_app_registry_get_app_configs_filters_by_registry_package(mocker):
    # Arrange.
    class MatchingAppConfig:
        name = "matching_package.app"
        label = "app"

        def get_models(self, *args, **kwargs):
            return []

    matching_app_config = MatchingAppConfig()

    class OtherAppConfig:
        name = "other_package.app"
        label = "app"

        def get_models(self, *args, **kwargs):
            return []

    other_app_config = OtherAppConfig()

    # Mock.
    mocker.patch(
        "django.apps.registry.apps.get_app_configs",
        return_value=[matching_app_config, other_app_config],
    )

    # Act.
    app_registry = AppRegistry(root_package="matching_package")
    app_configs = app_registry.get_app_configs()

    # Assert.
    assert matching_app_config in app_configs
    assert other_app_config not in app_configs


def test_app_registry_get_app_config_finds_by_label(mocker):
    # Arrange.
    class AppConfig:
        name = "package.app"
        label = "app"

        def get_models(self):
            return []

    app_config = AppConfig()

    # Mock.
    mocker.patch(
        "django.apps.registry.apps.get_app_configs",
        return_value=[app_config],
    )

    # Act.
    app_registry = AppRegistry(root_package="package")
    found_app_config = app_registry.get_app_config("app")

    # Assert.
    assert found_app_config == app_config


def test_app_registry_get_app_config_rejects_missing_label(mocker):
    # Arrange.
    class AppConfig:
        name = "package.app"
        label = "app"

        def get_models(self):
            return []

    app_config = AppConfig()

    # Mock.
    mocker.patch(
        "django.apps.registry.apps.get_app_configs",
        return_value=[app_config],
    )

    # Act & assert.
    app_registry = AppRegistry(root_package="package")

    with pytest.raises(app_registry.AppNotFoundError):
        app_registry.get_app_config("does_not_exist")


@pytest.mark.parametrize(
    ("app_label", "expected"),
    [
        pytest.param("app", True, id="installed"),
        pytest.param("does_not_exist", False, id="not installed"),
    ],
)
def test_app_registry_is_app_installed_checks_by_label(mocker, app_label, expected):
    # Arrange.
    class AppConfig:
        name = "package.app"
        label = "app"

        def get_models(self):
            return []

    app_config = AppConfig()

    # Mock.
    mocker.patch(
        "django.apps.registry.apps.get_app_configs",
        return_value=[app_config],
    )

    # Act.
    app_registry = AppRegistry(root_package="package")
    is_app_installed = app_registry.is_app_installed(app_label)

    # Assert.
    assert is_app_installed is expected


def test_app_registry_get_models_filters_by_registry_package(mocker):
    # Arrange.
    class MatchingModel:
        class Meta:
            label = "app.MatchingModel"

        _meta = Meta()

    class MatchingAppConfig:
        name = "matching_package.app"
        label = "app"

        def get_models(self):
            return [MatchingModel]

    matching_app_config = MatchingAppConfig()

    class OtherModel:
        class Meta:
            label = "app.OtherModel"

        _meta = Meta()

    class OtherAppConfig:
        name = "other_package.app"
        label = "app"

        def get_models(self):
            return [OtherModel]

    other_app_config = OtherAppConfig()

    # Mock.
    mocker.patch(
        "django.apps.registry.apps.get_app_configs",
        return_value=[matching_app_config, other_app_config],
    )

    # Act.
    app_registry = AppRegistry(root_package="matching_package")
    registered_models = app_registry.get_models()

    # Assert.
    assert MatchingModel in registered_models
    assert OtherModel not in registered_models


@pytest.mark.parametrize(
    "model_name_or_label",
    [
        pytest.param("Model", id="name"),
        pytest.param("model", id="name (lowercase)"),
        pytest.param("app.Model", id="label"),
        pytest.param("app.model", id="label (lowercase)"),
    ],
)
def test_app_registry_get_model_finds_by_name_or_label(mocker, model_name_or_label):
    # Arrange.
    class Model:
        class Meta:
            label = "app.Model"

        _meta = Meta()

    class AppConfig:
        name = "package.app"
        label = "app"

        def get_models(self):
            return [Model]

    app_config = AppConfig()

    # Mock.
    mocker.patch(
        "django.apps.registry.apps.get_app_configs",
        return_value=[app_config],
    )

    # Act.
    app_registry = AppRegistry(root_package="package")
    found_model = app_registry.get_model(model_name_or_label)

    # Assert.
    assert found_model is Model


@pytest.mark.parametrize(
    "model_name_or_label",
    [
        pytest.param("DoesNotExist", id="name"),
        pytest.param("app.DoesNotExist", id="label"),
    ],
)
def test_app_registry_get_model_rejects_missing_model(mocker, model_name_or_label):
    # Arrange.
    class Model:
        class Meta:
            label = "app.Model"

        _meta = Meta()

    class AppConfig:
        name = "package.app"
        label = "app"

        def get_models(self):
            return [Model]

    app_config = AppConfig()

    # Mock.
    mocker.patch(
        "django.apps.registry.apps.get_app_configs",
        return_value=[app_config],
    )

    # Act & assert.
    app_registry = AppRegistry(root_package="package")

    with pytest.raises(app_registry.ModelNotFoundError):
        app_registry.get_model(model_name_or_label)


@pytest.mark.parametrize(
    ("model_name_or_label", "expected"),
    [
        pytest.param("Model", True, id="name"),
        pytest.param("model", True, id="name (lowercase)"),
        pytest.param("app.Model", True, id="label"),
        pytest.param("app.model", True, id="label (lowercase)"),
        pytest.param("DoesNotExist", False, id="missing name"),
        pytest.param("app.DoesNotExist", False, id="missing label"),
    ],
)
def test_app_registry_is_model_registered_checks_identifier(mocker, model_name_or_label, expected):  # fmt: skip
    # Arrange.
    class Model:
        class Meta:
            label = "app.Model"

        _meta = Meta()

    class AppConfig:
        name = "package.app"
        label = "app"

        def get_models(self):
            return [Model]

    app_config = AppConfig()

    # Mock.
    mocker.patch(
        "django.apps.registry.apps.get_app_configs",
        return_value=[app_config],
    )

    # Act.
    app_registry = AppRegistry(root_package="package")
    is_model_registered = app_registry.is_model_registered(model_name_or_label)

    # Assert.
    assert is_model_registered is expected


@pytest.mark.parametrize(
    "model_name",
    [
        pytest.param("Model", id="name"),
        pytest.param("model", id="name (lowercase)"),
    ],
)
def test_app_registry_get_model_rejects_multiple_matches(mocker, model_name):
    # Arrange.
    class ModelA:
        class Meta:
            label = "app_a.Model"

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
    app_registry = AppRegistry(root_package="package")

    with pytest.raises(app_registry.MultipleModelsFoundError):
        app_registry.get_model(model_name)
