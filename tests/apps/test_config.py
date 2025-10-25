from importlib import import_module

import pytest

from django.conf import settings
from django.core.checks.registry import registry as checks_registry
from django.core.exceptions import ImproperlyConfigured
from django.dispatch.dispatcher import Signal
from django.test.utils import isolate_apps, override_settings

from reactor.apps import config
from reactor.db import models


def test_app_config_ready_loads_settings_from_app_conf_module(mocker, settings):
    # Arrange.
    class AppConfig(config.AppConfig):
        name = "app"

        def __init__(self):
            pass

        def get_models(self):
            return []

    app_config = AppConfig()

    # Mock.
    def import_module_mock(module_name):
        if module_name == "app.conf":

            class AppConfModule:
                def __init__(self):
                    from reactor.conf import settings

                    class AppSettings(settings.AppSettings):
                        SETTING = "value"

                        class Meta:
                            prefix = "app"

                    self.settings = AppSettings()

            return AppConfModule()

        raise ModuleNotFoundError

    mocker.patch("reactor.apps.config.import_module", side_effect=import_module_mock)

    # Act.
    app_config.ready()

    # Assert.
    assert settings.APP_SETTING == "value"


def test_app_config_ready_raises_error_when_app_settings_type_invalid(mocker):
    # Arrange.
    class AppConfig(config.AppConfig):
        name = "app"

        def __init__(self):
            pass

        def get_models(self):
            return []

    app_config = AppConfig()

    # Mock.
    def import_module_mock(module_name):
        if module_name == "app.conf":

            class AppConfModule:
                def __init__(self):
                    class NotAppSettings:
                        pass

                    self.settings = NotAppSettings()

            return AppConfModule()

        raise ModuleNotFoundError

    mocker.patch("reactor.apps.config.import_module", side_effect=import_module_mock)

    # Act & assert.
    with pytest.raises(ImproperlyConfigured):
        app_config.ready()


def test_app_config_ready_appends_urlconf_from_app_conf_module(mocker):
    # Arrange.
    class AppConfig(config.AppConfig):
        name = "app"
        label = "app"

        def __init__(self):
            pass

        def get_models(self):
            return []

    app_config = AppConfig()

    # Mock.
    def import_module_mock(module_name):
        if module_name == "app.conf":

            class AppConfModule:
                def __init__(self):
                    from reactor.conf import urls

                    class AppURLs(urls.AppURLs):
                        app_name = "app"
                        urlpatterns = []
                        route = ""

                    self.urls = AppURLs()

            return AppConfModule()

        raise ModuleNotFoundError

    mocker.patch("reactor.apps.config.import_module", side_effect=import_module_mock)

    # Act.
    urlconf_module = import_module(settings.ROOT_URLCONF)
    urlpatterns_before = urlconf_module.urlpatterns.copy()

    app_config.ready()

    urlpatterns_after = urlconf_module.urlpatterns

    # Assert.
    assert urlpatterns_after[-1].app_name == "app"
    assert urlpatterns_after[-1].pattern._route == ""  # noqa: SLF001
    assert urlpatterns_after[-1].url_patterns == []

    # Clean up.
    urlconf_module.urlpatterns = urlpatterns_before


def test_app_config_ready_raises_error_when_app_urls_type_invalid(mocker):
    # Arrange.
    class AppConfig(config.AppConfig):
        name = "app"

        def __init__(self):
            pass

        def get_models(self):
            return []

    app_config = AppConfig()

    # Mock.
    def import_module_mock(module_name):
        if module_name == "app.conf":

            class AppConfModule:
                def __init__(self):
                    class NotAppURLs:
                        pass

                    self.urls = NotAppURLs()

            return AppConfModule()

        raise ModuleNotFoundError

    mocker.patch("reactor.apps.config.import_module", side_effect=import_module_mock)

    # Act & assert.
    with pytest.raises(ImproperlyConfigured):
        app_config.ready()


def test_app_config_ready_registers_checks_from_app_checks_module(mocker):
    # Arrange.
    def check(app_configs=None, **kwargs):
        return []

    class AppConfig(config.AppConfig):
        name = "app"

        def __init__(self):
            pass

        def get_models(self):
            return []

    app_config = AppConfig()

    # Mock.
    def import_module_mock(module_name):
        if module_name == "app.checks":

            class AppChecksModule:
                def __init__(self):
                    checks_registry.register(check)

            return AppChecksModule()

        raise ModuleNotFoundError

    mocker.patch("reactor.apps.config.import_module", side_effect=import_module_mock)

    # Act.
    app_config.ready()

    # Assert.
    assert check in checks_registry.registered_checks

    # Clean up.
    checks_registry.registered_checks.remove(check)


def test_app_config_ready_connects_signals_from_app_signals_module(mocker):
    # Arrange.
    signal = Signal()

    class AppConfig(config.AppConfig):
        name = "app"

        def __init__(self):
            pass

        def get_models(self):
            return []

    app_config = AppConfig()

    # Mock.
    receiver_mock = mocker.Mock(return_value=None)

    def import_module_mock(module_name):
        if module_name == "app.signals":

            class AppSignalsModule:
                def __init__(self):
                    signal.connect(receiver_mock)

            return AppSignalsModule()

        raise ModuleNotFoundError

    mocker.patch("reactor.apps.config.import_module", side_effect=import_module_mock)

    # Act.
    app_config.ready()
    signal.send(sender=app_config)

    # Assert.
    receiver_mock.assert_called_once_with(signal=signal, sender=app_config)

    # Clean up.
    signal.disconnect(receiver_mock)


@isolate_apps("tests")
@override_settings(INSTALLED_APPS=["tests"])
def test_app_config_ready_calls_ready_for_all_app_models(mocker):
    # Arrange.
    class ModelA(models.Model):
        class Meta:
            app_label = "tests"

        @classmethod
        def ready(cls):
            pass

    class ModelB(models.Model):
        class Meta:
            app_label = "tests"

        @classmethod
        def ready(cls):
            pass

    class AppConfig(config.AppConfig):
        name = "app"

        def __init__(self):
            pass

        def get_models(self):
            return [ModelA, ModelB]

    app_config = AppConfig()

    # Spy.
    model_a_ready_spy = mocker.spy(ModelA, "ready")
    model_b_ready_spy = mocker.spy(ModelB, "ready")

    # Act.
    app_config.ready()

    # Assert.
    model_a_ready_spy.assert_called_once()
    model_b_ready_spy.assert_called_once()
