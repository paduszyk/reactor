from importlib import import_module

import appconf

from django.core.checks.registry import registry
from django.dispatch import Signal

from reactor.apps.config import AppConfig


def test_app_config_ready_loads_settings_from_conf_module(mocker, settings):
    # Arrange.
    class MockAppConfig(AppConfig):
        name = "mock_app"

        def __init__(self):
            pass

        def get_models(self):
            return []

    mock_app_config = MockAppConfig()

    # Mock.
    def mock_import_module(name):
        if name == "mock_app.conf":

            class MockConfModule:
                class Settings(appconf.AppConf):
                    SETTING = "value"

                    class Meta:
                        prefix = "mock_app"

                settings = Settings()

            return MockConfModule()

        raise ImportError

    mocker.patch(
        "reactor.apps.config.import_module",
        side_effect=mock_import_module,
    )

    # Act.
    mock_app_config.ready()

    # Assert.
    assert settings.MOCK_APP_SETTING == "value"


def test_app_config_ready_appends_urlpatterns_from_conf_module(mocker, settings):
    # Arrange.
    class MockAppConfig(AppConfig):
        name = "mock_app"
        label = "mock_app"

        def __init__(self):
            pass

        def get_models(self):
            return []

    mock_app_config = MockAppConfig()

    # Mock.
    def mock_import_module(name):
        if name == "mock_app.conf":

            class MockConfModule:
                class Urls:
                    urlpatterns = []

                urls = Urls()

            return MockConfModule()

        raise ImportError

    mocker.patch(
        "reactor.apps.config.import_module",
        side_effect=mock_import_module,
    )

    # Act.
    urlconf_module = import_module(settings.ROOT_URLCONF)
    urlpatterns_before = urlconf_module.urlpatterns.copy()

    mock_app_config.ready()

    urlpatterns_after = urlconf_module.urlpatterns

    # Assert.
    assert urlpatterns_after[-1].app_name == "mock_app"
    assert urlpatterns_after[-1].pattern._route == ""  # noqa: SLF001
    assert urlpatterns_after[-1].url_patterns == []

    # Clean up.
    urlconf_module.urlpatterns = urlpatterns_before


def test_app_config_ready_registers_checks_from_checks_module(mocker):
    # Arrange.
    def check(app_configs=None, **kwargs):  # noqa: ARG001
        return []

    class MockAppConfig(AppConfig):
        name = "mock_app"

        def __init__(self):
            pass

        def get_models(self):
            return []

    mock_app_config = MockAppConfig()

    # Mock.
    def mock_import_module(name):
        if name == "mock_app.checks":
            return registry.register(check)

        raise ImportError

    mocker.patch(
        "reactor.apps.config.import_module",
        side_effect=mock_import_module,
    )

    # Act.
    mock_app_config.ready()

    # Assert.
    assert check in registry.registered_checks

    # Clean up.
    registry.registered_checks.remove(check)


def test_app_config_ready_connects_signals_to_handlers_from_signals_module(mocker):
    # Arrange.
    signal = Signal()
    mock_receiver = mocker.Mock()

    class MockAppConfig(AppConfig):
        name = "mock_app"

        def __init__(self):
            pass

        def get_models(self):
            return []

    mock_app_config = MockAppConfig()

    # Mock.
    def mock_import_module(name):
        if name == "mock_app.signals":
            return signal.connect(mock_receiver)

        raise ImportError

    mocker.patch(
        "reactor.apps.config.import_module",
        side_effect=mock_import_module,
    )

    # Act.
    mock_app_config.ready()
    signal.send(mock_app_config)

    # Assert.
    mock_receiver.assert_called()

    # Clean up.
    signal.disconnect(mock_receiver)
