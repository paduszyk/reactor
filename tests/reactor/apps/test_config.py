__all__ = []

from importlib import import_module

import appconf
import pytest

from reactor.apps.config import AppConfig


@pytest.fixture()
def urlpatterns(settings):
    urlconf_module = import_module(settings.ROOT_URLCONF)
    urlpatterns_before = urlconf_module.urlpatterns.copy()

    yield urlconf_module.urlpatterns

    urlconf_module.urlpatterns = urlpatterns_before


@pytest.fixture()
def make_app_config(mocker):
    def _make_app_config(**kwargs):
        class AppConfigMock(AppConfig):
            def __init__(self, **kwargs):
                kwargs.setdefault("name", mocker.ANY)
                kwargs.setdefault("label", mocker.ANY)

                for key, value in kwargs.items():
                    setattr(self, key, value)

        return AppConfigMock(**kwargs)

    return _make_app_config


@pytest.mark.parametrize(
    "app_module_name",
    [
        "checks",
        "signals",
        "conf.settings",
        "conf.urls",
    ],
)
def test_app_config_ready_attempts_to_import_app_module(
    mocker,
    make_app_config,
    app_module_name,
):
    # Arrange.
    app_config_mock = make_app_config(name="app_mock")

    # Mock.
    def _import_module_mock(module_name):
        if module_name.endswith(".conf.urls"):
            return mocker.Mock(spec=["urlpatterns"], urlpatterns=[])
        raise ImportError

    import_module_mock = mocker.patch(
        "reactor.apps.config.import_module",
        side_effect=_import_module_mock,
    )

    # Act.
    app_config_mock.ready()

    # Assert.
    import_module_mock.assert_any_call(f"app_mock.{app_module_name}")


def test_app_config_ready_loads_app_settings(mocker, settings, make_app_config):
    # Arrange.
    app_config_mock = make_app_config(name=mocker.ANY)

    class AppConfMock(appconf.AppConf):
        class Meta:
            prefix = "mock"

    app_settings_module_mock = mocker.Mock(settings=AppConfMock(SETTING=mocker.ANY))

    # Mock.
    def _import_module_mock(module_name):
        if module_name.endswith(".conf.settings"):
            return app_settings_module_mock
        raise ImportError

    mocker.patch("reactor.apps.config.import_module", side_effect=_import_module_mock)

    # Act.
    app_config_mock.ready()

    # Assert.
    assert hasattr(settings, "MOCK_SETTING")
    assert settings.MOCK_SETTING == app_settings_module_mock.SETTING


def test_app_config_ready_appends_app_urlpatterns(
    mocker,
    make_app_config,
    urlpatterns,
):
    # Arrange.
    app_config_mock = make_app_config()
    app_urls_module_mock = mocker.Mock(spec=["urlpatterns"], urlpatterns=[])

    # Mock.
    def _import_module_mock(module_name):
        if module_name.endswith(".conf.urls"):
            return app_urls_module_mock
        raise ImportError

    mocker.patch("reactor.apps.config.import_module", side_effect=_import_module_mock)

    # Act.
    app_config_mock.ready()

    # Assert.
    assert urlpatterns[-1].urlconf_module == app_urls_module_mock
