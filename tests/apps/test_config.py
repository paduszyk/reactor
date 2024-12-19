from importlib import import_module

import appconf

from django.core.checks.registry import registry
from django.db.models.signals import ModelSignal
from django.dispatch import Signal
from django.test.utils import isolate_apps, override_settings

from reactor.apps.config import AppConfig
from reactor.db.models import Model


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


@isolate_apps("tests")
@override_settings(
    INSTALLED_APPS=[
        "tests",
    ],
)
def test_app_config_ready_connects_signals_to_model_class_method(mocker):
    # Arrange.
    model_signal = ModelSignal()

    class MockModel(Model):
        signal_receivers = {
            "receiver": model_signal,
        }

        @classmethod
        def receiver(cls, **kwargs):
            pass

        @classmethod
        def send_signal(cls):
            model_signal.send(sender=cls)

    class MockAppConfig(AppConfig):
        name = "mock_app"

        def __init__(self):
            pass

        def get_models(self):
            return [MockModel]

    mock_app_config = MockAppConfig()

    # Spy.
    spy_receiver = mocker.spy(MockModel, "receiver")

    # Act.
    mock_app_config.ready()
    MockModel.send_signal()

    # Assert.
    spy_receiver.assert_called()

    # Clean up.
    model_signal.disconnect(dispatch_uid="tests.mockmodel.receiver")


@isolate_apps("tests")
@override_settings(
    INSTALLED_APPS=[
        "tests",
    ],
)
def test_app_config_ready_connects_signals_to_model_instance_method(mocker):
    # Arrange.
    model_signal = ModelSignal()

    class MockModel(Model):
        signal_receivers = {
            "receiver": model_signal,
        }

        def receiver(self, **kwargs):
            pass

        def send_signal(self):
            model_signal.send(sender=self.__class__, instance=self)

    class MockAppConfig(AppConfig):
        name = "mock_app"

        def __init__(self):
            pass

        def get_models(self):
            return [MockModel]

    mock_app_config = MockAppConfig()

    # Spy.
    spy_receiver = mocker.spy(MockModel, "receiver")

    # Act.
    mock_app_config.ready()
    mock_instance = MockModel()
    mock_instance.send_signal()

    # Assert.
    spy_receiver.assert_called()

    # Clean up.
    model_signal.disconnect(dispatch_uid="tests.mockmodel.receiver")


@isolate_apps("tests")
@override_settings(
    INSTALLED_APPS=[
        "tests",
    ],
)
def test_app_config_ready_calls_ready_hook_from_model(mocker):
    # Arrange.
    class MockModel(Model):
        @classmethod
        def ready(cls):
            pass

    class MockAppConfig(AppConfig):
        name = "mock_app"

        def __init__(self):
            pass

        def get_models(self):
            return [MockModel]

    mock_app_config = MockAppConfig()

    # Spy.
    spy_model_ready = mocker.spy(MockModel, "ready")

    # Act.
    mock_app_config.ready()

    # Assert.
    spy_model_ready.assert_called()
