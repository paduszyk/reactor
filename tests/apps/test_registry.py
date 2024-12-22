import pytest

from reactor.apps.registry import Apps


def test_apps_is_not_populated_as_instantiated():
    # Act.
    apps = Apps(name_pattern=r"^tests\.")

    # Assert.
    assert not apps._populated  # noqa: SLF001


def test_apps_is_populated_when_accessing_public_method():
    # Arrange.
    class MockApps(Apps):
        def mock_method(self):
            pass

    mock_apps = MockApps(name_pattern=r"^tests\.")

    # Act.
    mock_apps.mock_method()

    # Assert.
    assert mock_apps._populated  # noqa: SLF001


def test_apps_is_not_populated_when_accessing_private_method():
    # Arrange.
    class MockApps(Apps):
        def _mock_method(self):
            pass

    mock_apps = MockApps(name_pattern=r"^tests\.")

    # Act.
    mock_apps._mock_method()  # noqa: SLF001

    # Assert.
    assert not mock_apps._populated  # noqa: SLF001


def test_apps_is_populated_only_once(mocker):
    # Arrange.
    class MockApps(Apps):
        def mock_method(self):
            pass

    mock_apps = MockApps(name_pattern=r"^tests\.")

    # Spy.
    spy_populate = mocker.spy(mock_apps, "_populate")

    # Act.
    mock_apps.mock_method()
    mock_apps.mock_method()

    # Assert.
    spy_populate.assert_called_once()


def test_apps_get_app_configs_returns_local_app_configs_only(mocker):
    # Arrange.
    apps = Apps(name_pattern=r"^tests\.")

    class MockAppConfigA:
        name = "tests.mock_app_a"
        label = "mock_app_a"

        def get_models(self, *args, **kwargs):
            return []

    class MockAppConfigB:
        name = "somewhere_else.mock_app_b"
        label = "mock_app_b"

        def get_models(self, *args, **kwargs):
            return []

    mock_app_config_a = MockAppConfigA()
    mock_app_config_b = MockAppConfigB()

    # Mock.
    mocker.patch(
        "django.apps.registry.apps.get_app_configs",
        return_value=[
            mock_app_config_a,
            mock_app_config_b,
        ],
    )

    # Act.
    app_configs = apps.get_app_configs()

    # Assert.
    assert app_configs == [mock_app_config_a]


def test_apps_get_app_config_returns_app_config_if_app_config_is_found(mocker):
    # Arrange.
    apps = Apps(name_pattern=r"^tests\.")

    class MockAppConfig:
        name = "tests.mock_app"
        label = "mock_app"

        def get_models(self, *args, **kwargs):
            return []

    mock_app_config = MockAppConfig()

    # Mock.
    mocker.patch(
        "django.apps.registry.apps.get_app_configs",
        return_value=[mock_app_config],
    )

    # Act.
    app_config = apps.get_app_config("mock_app")

    # Assert.
    assert app_config == mock_app_config


def test_apps_get_app_config_raises_lookup_error_if_app_config_is_not_found(mocker):
    # Arrange.
    apps = Apps(name_pattern=r"^tests\.")

    class MockAppConfig:
        name = "tests.mock_app"
        label = "mock_app"

        def get_models(self, *args, **kwargs):
            return []

    mock_app_config = MockAppConfig()

    # Mock.
    mocker.patch(
        "django.apps.registry.apps.get_app_configs",
        return_value=[mock_app_config],
    )

    # Arrange.
    with pytest.raises(LookupError):
        apps.get_app_config("another_app")


def test_apps_get_models_returns_models_from_all_registered_apps(mocker):
    # Arrange.
    apps = Apps(name_pattern=r"^tests\.")

    class MockModelA:
        class Meta:
            label_lower = "mock_app_a.mockmodel"

        _meta = Meta()

    class MockModelB:
        class Meta:
            label_lower = "mock_app_b.mockmodel"

        _meta = Meta()

    class MockAppConfigA:
        name = "tests.mock_app_a"
        label = "mock_app_a"

        def get_models(self, *args, **kwargs):
            return [MockModelA]

    class MockAppConfigB:
        name = "tests.mock_app_b"
        label = "mock_app_b"

        def get_models(self, *args, **kwargs):
            return [MockModelB]

    mock_app_config_a = MockAppConfigA()
    mock_app_config_b = MockAppConfigB()

    # Mock.
    mocker.patch(
        "django.apps.registry.apps.get_app_configs",
        return_value=[
            mock_app_config_a,
            mock_app_config_b,
        ],
    )

    # Act.
    models = apps.get_models()

    # Assert.
    assert models == [MockModelA, MockModelB]


@pytest.mark.parametrize(
    "model_identifier",
    [
        "mock_app.mockmodel",
        "mock_app.MockModel",
        "mockmodel",
    ],
    ids=[
        "label_lower",
        "label",
        "model_name",
    ],
)
def test_apps_get_model_returns_model_if_model_is_found(mocker, model_identifier):
    # Arrange.
    apps = Apps(name_pattern=r"^tests\.")

    class MockModel:
        class Meta:
            app_label = "mock_app"
            label_lower = "mock_app.mockmodel"

        _meta = Meta()

    class MockAppConfig:
        name = "tests.mock_app"
        label = "mock_app"

        def get_models(self, *args, **kwargs):
            return [MockModel]

    mock_app_config = MockAppConfig()

    # Mock.
    mocker.patch(
        "django.apps.registry.apps.get_app_configs",
        return_value=[mock_app_config],
    )

    # Act.
    model = apps.get_model(model_identifier)

    # Assert.
    assert model == MockModel


def test_apps_get_model_raises_lookup_error_if_model_not_found(mocker):
    # Arrange.
    apps = Apps(name_pattern=r"^tests\.")

    class MockAppConfig:
        name = "tests.mock_app"
        label = "mock_app"

        def get_models(self, *args, **kwargs):
            return []

    mock_app_config = MockAppConfig()

    # Mock.
    mocker.patch(
        "django.apps.registry.apps.get_app_configs",
        return_value=[mock_app_config],
    )

    # Act & assert.
    with pytest.raises(LookupError):
        apps.get_model("mock_app.mockmodel")


def test_apps_get_model_raises_lookup_error_if_model_found_in_multiple_apps(mocker):
    # Arrange.
    apps = Apps(name_pattern=r"^tests\.")

    class MockModelA:
        class Meta:
            app_label = "mock_app"
            label_lower = "mock_app_a.mockmodel"

        _meta = Meta()

    class MockModelB:
        class Meta:
            app_label = "mock_app"
            label_lower = "mock_app_b.mockmodel"

        _meta = Meta()

    class MockAppConfigA:
        name = "tests.mock_app_a"
        label = "mock_app_a"

        def get_models(self, *args, **kwargs):
            return [MockModelA]

    class MockAppConfigB:
        name = "tests.mock_app_b"
        label = "mock_app_b"

        def get_models(self, *args, **kwargs):
            return [MockModelB]

    mock_app_config_a = MockAppConfigA()
    mock_app_config_b = MockAppConfigB()

    # Mock.
    mocker.patch(
        "django.apps.registry.apps.get_app_configs",
        return_value=[
            mock_app_config_a,
            mock_app_config_b,
        ],
    )

    # Act & assert.
    with pytest.raises(LookupError):
        apps.get_model("mockmodel")
