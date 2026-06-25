import pytest

from django.core.exceptions import ImproperlyConfigured
from django.db.models.base import Model as BaseDjangoModel
from django.dispatch import Signal

from reactor.apps.config import AppConfig as BaseFirstPartyAppConfig
from reactor.db.models.base import Model as BaseFirstPartyModel


def test_app_config_subclass_sets_default_true():
    # Arrange.
    class AppConfig(BaseFirstPartyAppConfig):
        pass

    # Act.
    is_default = AppConfig.default

    # Assert.
    assert is_default is True


def test_app_config_subclass_preserves_explicit_default():
    # Arrange.
    class AppConfig(BaseFirstPartyAppConfig):
        default = False

    # Act.
    is_default = AppConfig.default

    # Assert.
    assert is_default is False


def test_app_config_ready_calls_all_ready_hooks(mocker):
    # Arrange.
    class AppConfig(BaseFirstPartyAppConfig):
        _ready_hooks = (
            "ready_hook_a",
            "ready_hook_b",
        )

        def ready_hook_a(self):
            return None

        def ready_hook_b(self):
            return None

    # Mock.
    mocker.patch("django.apps.config.AppConfig.__init__", return_value=None)

    # Spy.
    ready_hook_a_spy = mocker.spy(AppConfig, "ready_hook_a")
    ready_hook_b_spy = mocker.spy(AppConfig, "ready_hook_b")

    # Act.
    app_config = AppConfig()
    app_config.ready()

    # Assert.
    ready_hook_a_spy.assert_called_once()
    ready_hook_b_spy.assert_called_once()


def test_app_config_ready_is_idempotent_for_same_instance(mocker):
    # Arrange.
    class AppConfig(BaseFirstPartyAppConfig):
        _ready_hooks = ("ready_hook",)

        def ready_hook(self):
            return None

    # Mock.
    mocker.patch("django.apps.config.AppConfig.__init__", return_value=None)

    # Spy.
    ready_hook_spy = mocker.spy(AppConfig, "ready_hook")

    # Act.
    app_config = AppConfig()
    app_config.ready()
    app_config.ready()

    # Assert.
    ready_hook_spy.assert_called_once()


def test_app_config_ready_loads_settings_from_conf_module(mocker, django_settings):
    # Arrange.
    class AppConfig(BaseFirstPartyAppConfig):
        name = "app"

    AppConfig.get_models = mocker.Mock(return_value=[])

    # Mock.
    mocker.patch("django.apps.config.AppConfig.__init__", return_value=None)

    def import_module_side_effect(module_name):
        if module_name == "app.conf":

            class ConfModule:
                def __init__(self):
                    from reactor.apps.settings import (
                        AppSettings as BaseFirstPartyAppSettings,
                    )

                    class AppSettings(BaseFirstPartyAppSettings):
                        SETTING_NAME = "app_setting_value"

                        class Meta:
                            prefix = "app"

                    self.settings = AppSettings()

            return ConfModule()

        raise ModuleNotFoundError(name=module_name)

    mocker.patch(
        "reactor.apps.config.import_module",
        side_effect=import_module_side_effect,
    )

    # Act.
    app_config = AppConfig()
    app_config.ready()

    # Assert.
    assert django_settings.APP_SETTING_NAME == "app_setting_value"


def test_app_config_ready_rejects_invalid_settings_type(mocker):
    # Arrange.
    class AppConfig(BaseFirstPartyAppConfig):
        name = "app"

    # Mock.
    mocker.patch("django.apps.config.AppConfig.__init__", return_value=None)

    def import_module_side_effect(module_name):
        if module_name == "app.conf":

            class ConfModule:
                def __init__(self):
                    self.settings = mocker.sentinel.not_app_settings

            return ConfModule()

        raise ModuleNotFoundError(name=module_name)

    mocker.patch(
        "reactor.apps.config.import_module",
        side_effect=import_module_side_effect,
    )

    # Act & assert.
    app_config = AppConfig()

    with pytest.raises(ImproperlyConfigured):
        app_config.ready()


def test_app_config_ready_rejects_conf_import_missing_dependency(mocker):
    # Arrange.
    class AppConfig(BaseFirstPartyAppConfig):
        name = "app"

    # Mock.
    mocker.patch("django.apps.config.AppConfig.__init__", return_value=None)

    def import_module_side_effect(module_name):
        if module_name == "app.conf":
            raise ModuleNotFoundError(name="module_not_found")

        raise ModuleNotFoundError(name=module_name)

    mocker.patch(
        "reactor.apps.config.import_module",
        side_effect=import_module_side_effect,
    )

    # Act & assert.
    app_config = AppConfig()

    def exc_info_check(exc_info):
        exc_cause = exc_info.__cause__

        return (
            isinstance(exc_cause, ModuleNotFoundError)
            and exc_cause.name == "module_not_found"
        )

    with pytest.raises(ImproperlyConfigured, check=exc_info_check):
        app_config.ready()


def test_app_config_ready_appends_urls_from_conf_module(mocker, django_urlpatterns):
    # Arrange.
    class AppConfig(BaseFirstPartyAppConfig):
        name = "app"
        label = "app"

    AppConfig.get_models = mocker.Mock(return_value=[])

    # Mock.
    mocker.patch("django.apps.config.AppConfig.__init__", return_value=None)

    def import_module_side_effect(module_name):
        if module_name == "app.conf":

            class ConfModule:
                def __init__(self):
                    from reactor.apps.urls import AppURLs as BaseFirstPartyAppURLs

                    class AppURLs(BaseFirstPartyAppURLs):
                        app_name = "app"
                        urlpatterns = []
                        route = ""

                    self.urls = AppURLs()

            return ConfModule()

        raise ModuleNotFoundError(name=module_name)

    mocker.patch(
        "reactor.apps.config.import_module",
        side_effect=import_module_side_effect,
    )

    # Act.
    app_config = AppConfig()
    app_config.ready()

    # Assert.
    assert django_urlpatterns[-1].app_name == "app"
    assert django_urlpatterns[-1].namespace == "app"
    assert django_urlpatterns[-1].pattern._route == ""  # noqa: SLF001
    assert django_urlpatterns[-1].url_patterns == []


def test_app_config_ready_accepts_inherited_urlpatterns(mocker, django_urlpatterns):
    # Arrange.
    class AppConfig(BaseFirstPartyAppConfig):
        name = "app"
        label = "app"

    AppConfig.get_models = mocker.Mock(return_value=[])

    # Mock.
    mocker.patch("django.apps.config.AppConfig.__init__", return_value=None)

    def import_module_side_effect(module_name):
        if module_name == "app.conf":

            class ConfModule:
                def __init__(self):
                    from reactor.apps.urls import AppURLs as BaseFirstPartyAppURLs

                    class ParentAppURLs(BaseFirstPartyAppURLs):
                        app_name = "app"
                        urlpatterns = []

                    class ChildAppURLs(ParentAppURLs):
                        route = "app/"

                    self.urls = ChildAppURLs()

            return ConfModule()

        raise ModuleNotFoundError(name=module_name)

    mocker.patch(
        "reactor.apps.config.import_module",
        side_effect=import_module_side_effect,
    )

    # Act.
    app_config = AppConfig()
    app_config.ready()

    # Assert.
    assert django_urlpatterns[-1].app_name == "app"
    assert django_urlpatterns[-1].namespace == "app"
    assert django_urlpatterns[-1].pattern._route == "app/"  # noqa: SLF001
    assert django_urlpatterns[-1].url_patterns == []


def test_app_config_ready_uses_default_url_route(mocker, django_urlpatterns):
    # Arrange.
    class AppConfig(BaseFirstPartyAppConfig):
        name = "app"
        label = "app"

    AppConfig.get_models = mocker.Mock(return_value=[])

    # Mock.
    mocker.patch("django.apps.config.AppConfig.__init__", return_value=None)

    def import_module_side_effect(module_name):
        if module_name == "app.conf":

            class ConfModule:
                def __init__(self):
                    from reactor.apps.urls import AppURLs as BaseFirstPartyAppURLs

                    class AppURLs(BaseFirstPartyAppURLs):
                        urlpatterns = []

                    self.urls = AppURLs()

            return ConfModule()

        raise ModuleNotFoundError(name=module_name)

    mocker.patch(
        "reactor.apps.config.import_module",
        side_effect=import_module_side_effect,
    )

    # Act.
    app_config = AppConfig()
    app_config.ready()

    # Assert.
    assert django_urlpatterns[-1].pattern._route == ""  # noqa: SLF001


def test_app_config_ready_uses_app_label_namespace(mocker, django_urlpatterns):
    # Arrange.
    class AppConfig(BaseFirstPartyAppConfig):
        name = "app"
        label = "app"

    AppConfig.get_models = mocker.Mock(return_value=[])

    # Mock.
    mocker.patch("django.apps.config.AppConfig.__init__", return_value=None)

    def import_module_side_effect(module_name):
        if module_name == "app.conf":

            class ConfModule:
                def __init__(self):
                    from reactor.apps.urls import AppURLs as BaseFirstPartyAppURLs

                    class AppURLs(BaseFirstPartyAppURLs):
                        urlpatterns = []

                    self.urls = AppURLs()

            return ConfModule()

        raise ModuleNotFoundError(name=module_name)

    mocker.patch(
        "reactor.apps.config.import_module",
        side_effect=import_module_side_effect,
    )

    # Act.
    app_config = AppConfig()
    app_config.ready()

    # Assert.
    assert django_urlpatterns[-1].namespace == app_config.label


def test_app_config_ready_rejects_invalid_urls_type(mocker):
    # Arrange.
    class AppConfig(BaseFirstPartyAppConfig):
        name = "app"

    # Mock.
    mocker.patch("django.apps.config.AppConfig.__init__", return_value=None)

    def import_module_side_effect(module_name):
        if module_name == "app.conf":

            class ConfModule:
                def __init__(self):
                    self.urls = mocker.sentinel.not_app_urls

            return ConfModule()

        raise ModuleNotFoundError(name=module_name)

    mocker.patch(
        "reactor.apps.config.import_module",
        side_effect=import_module_side_effect,
    )

    # Act & assert.
    app_config = AppConfig()

    with pytest.raises(ImproperlyConfigured):
        app_config.ready()


def test_app_config_ready_rejects_urls_without_urlpatterns(mocker):
    # Arrange.
    class AppConfig(BaseFirstPartyAppConfig):
        name = "app"

    # Mock.
    mocker.patch("django.apps.config.AppConfig.__init__", return_value=None)

    def import_module_side_effect(module_name):
        if module_name == "app.conf":

            class ConfModule:
                def __init__(self):
                    from reactor.apps.urls import AppURLs as BaseFirstPartyAppURLs

                    class AppURLs(BaseFirstPartyAppURLs):
                        pass

                    self.urls = AppURLs()

            return ConfModule()

        raise ModuleNotFoundError(name=module_name)

    mocker.patch(
        "reactor.apps.config.import_module",
        side_effect=import_module_side_effect,
    )

    # Act & assert.
    app_config = AppConfig()

    with pytest.raises(ImproperlyConfigured):
        app_config.ready()


def test_app_config_ready_registers_checks_from_checks_module(mocker, django_checks):
    # Arrange.
    class AppConfig(BaseFirstPartyAppConfig):
        name = "app"

    AppConfig.get_models = mocker.Mock(return_value=[])

    def check(app_configs, **kwargs):
        return []

    # Mock.
    mocker.patch("django.apps.config.AppConfig.__init__", return_value=None)

    def import_module_side_effect(module_name):
        if module_name == "app.checks":

            class ChecksModule:
                def __init__(self):
                    django_checks.register(check)

            return ChecksModule()

        raise ModuleNotFoundError(name=module_name)

    mocker.patch(
        "reactor.apps.config.import_module",
        side_effect=import_module_side_effect,
    )

    # Act.
    app_config = AppConfig()
    app_config.ready()

    # Assert.
    assert check in django_checks.registered_checks


def test_app_config_ready_connects_signal_receivers_from_signals_module(mocker):
    # Arrange.
    class AppConfig(BaseFirstPartyAppConfig):
        name = "app"

    AppConfig.get_models = mocker.Mock(return_value=[])

    signal = Signal()
    receiver_mock = mocker.Mock(return_value=None)

    # Mock.
    mocker.patch("django.apps.config.AppConfig.__init__", return_value=None)

    def import_module_side_effect(module_name):
        if module_name == "app.signals":

            class SignalsModule:
                def __init__(self):
                    signal.connect(receiver_mock)

            return SignalsModule()

        raise ModuleNotFoundError(name=module_name)

    mocker.patch(
        "reactor.apps.config.import_module",
        side_effect=import_module_side_effect,
    )

    # Act.
    app_config = AppConfig()
    app_config.ready()
    signal.send(sender=app_config)

    # Assert.
    receiver_mock.assert_called_once_with(signal=signal, sender=app_config)


@pytest.mark.django_isolate_apps("tests")
def test_app_config_ready_calls_ready_for_all_first_party_app_models(mocker):
    # Arrange.
    class ModelA(BaseFirstPartyModel):
        class Meta:
            app_label = "tests"

        @classmethod
        def ready(cls):
            return None

    class ModelB(BaseFirstPartyModel):
        class Meta:
            app_label = "tests"

        @classmethod
        def ready(cls):
            return None

    class AppConfig(BaseFirstPartyAppConfig):
        name = "app"

    AppConfig.get_models = mocker.Mock(return_value=[ModelA, ModelB])

    # Mock.
    mocker.patch("django.apps.config.AppConfig.__init__", return_value=None)

    def import_module_side_effect(module_name):
        raise ModuleNotFoundError(name=module_name)

    mocker.patch(
        "reactor.apps.config.import_module",
        side_effect=import_module_side_effect,
    )

    # Spy.
    model_a_ready_spy = mocker.spy(ModelA, "ready")
    model_b_ready_spy = mocker.spy(ModelB, "ready")

    # Act.
    app_config = AppConfig()
    app_config.ready()

    # Assert.
    model_a_ready_spy.assert_called_once()
    model_b_ready_spy.assert_called_once()


@pytest.mark.django_isolate_apps("tests")
def test_app_config_ready_does_not_call_ready_for_non_first_party_models(mocker):
    # Arrange.
    class FirstPartyModel(BaseFirstPartyModel):
        class Meta:
            app_label = "tests"

        @classmethod
        def ready(cls):
            return None

    class DjangoModel(BaseDjangoModel):
        class Meta:
            app_label = "tests"

        @classmethod
        def ready(cls):
            return None

    class AppConfig(BaseFirstPartyAppConfig):
        name = "app"

    AppConfig.get_models = mocker.Mock(return_value=[FirstPartyModel, DjangoModel])

    # Mock.
    mocker.patch("django.apps.config.AppConfig.__init__", return_value=None)

    def import_module_side_effect(module_name):
        raise ModuleNotFoundError(name=module_name)

    mocker.patch(
        "reactor.apps.config.import_module",
        side_effect=import_module_side_effect,
    )

    # Spy.
    first_party_model_ready_spy = mocker.spy(FirstPartyModel, "ready")
    django_model_ready_spy = mocker.spy(DjangoModel, "ready")

    # Act.
    app_config = AppConfig()
    app_config.ready()

    # Assert.
    first_party_model_ready_spy.assert_called_once()
    django_model_ready_spy.assert_not_called()
