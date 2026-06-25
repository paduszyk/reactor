import pytest

from django.apps.config import AppConfig as BaseDjangoAppConfig
from django.db.models.base import Model as BaseDjangoModel

from reactor.apps.config import AppConfig as BaseFirstPartyAppConfig
from reactor.core import checks
from reactor.db.models.base import Model as BaseFirstPartyModel


def test_register_wraps_check_function(django_checks):
    # Arrange.
    def check(app_configs, **kwargs):
        return []

    # Act.
    registered_check = checks.register(check)

    # Assert.
    assert registered_check in django_checks.registered_checks


def test_register_wraps_decorated_check(django_checks):
    # Arrange & act.
    @checks.register
    def check(app_configs, **kwargs):
        return []

    # Assert.
    assert check in django_checks.registered_checks


def test_register_wraps_tagged_decorated_check(django_checks):
    # Arrange & act.
    @checks.register("tag")
    def check(app_configs, **kwargs):
        return []

    # Assert.
    assert check in django_checks.registered_checks


def test_register_wraps_tagged_check_function_with_check_argument(mocker, django_checks):  # fmt: skip
    # Arrange.
    def check(app_configs, **kwargs):
        return []

    # Act.
    registered_check = checks.register(check, "tag")

    # Assert.
    assert registered_check in django_checks.registered_checks


def test_register_wraps_decorated_check_with_empty_options(django_checks):
    # Arrange & act.
    @checks.register()
    def check(app_configs, **kwargs):
        return []

    # Assert.
    assert check in django_checks.registered_checks


@pytest.mark.usefixtures("django_checks")
def test_register_uses_app_registry_by_default(mocker):
    # Arrange.
    check_mock = mocker.Mock(return_value=[])
    apps_mock = mocker.patch("reactor.core.checks.apps")

    # Act.
    registered_check = checks.register(check_mock)
    registered_check()

    # Assert.
    check_mock.assert_called_once_with(apps_mock.get_app_configs.return_value)


@pytest.mark.usefixtures("django_checks")
def test_register_filters_explicit_app_configs_by_registry(mocker):
    # Arrange.
    check_mock = mocker.Mock(return_value=[])
    installed_app_config_mock = mocker.Mock()
    other_app_config_mock = mocker.Mock()

    # Mock.
    def is_app_installed_side_effect(app_label):
        return app_label == installed_app_config_mock.label

    mocker.patch(
        "reactor.core.checks.apps.is_app_installed",
        side_effect=is_app_installed_side_effect,
    )

    # Act.
    registered_check = checks.register(check_mock)
    registered_check(app_configs=[installed_app_config_mock, other_app_config_mock])

    # Assert.
    check_mock.assert_called_once_with([installed_app_config_mock])


def test_check_first_party_app_config_class_accepts_subclass(mocker):
    # Arrange.
    app_config_mock = mocker.Mock(spec=BaseFirstPartyAppConfig)

    # Mock.
    mocker.patch(
        "reactor.core.checks.apps.get_app_configs",
        return_value=[app_config_mock],
    )

    # Act.
    messages = checks.check_first_party_app_config_class()

    # Assert.
    assert messages == []


def test_check_first_party_app_config_class_rejects_django_app_config(mocker):
    # Arrange.
    first_party_app_config_mock = mocker.Mock(
        spec=BaseFirstPartyAppConfig,
        label="first_party_app",
    )
    django_app_config_mock = mocker.Mock(
        spec=BaseDjangoAppConfig,
        label="django_app",
    )

    # Mock.
    mocker.patch(
        "reactor.core.checks.apps.get_app_configs",
        return_value=[first_party_app_config_mock, django_app_config_mock],
    )

    # Act.
    messages = checks.check_first_party_app_config_class()

    # Assert.
    assert len(messages) == 1
    assert messages[0].id == "core.apps.E001"


@pytest.mark.django_isolate_apps("tests")
def test_check_first_party_model_class_accepts_subclass(mocker):
    # Arrange.
    class Model(BaseFirstPartyModel):
        class Meta:
            app_label = "tests"

    app_config_mock = mocker.Mock(
        spec=BaseFirstPartyAppConfig,
        get_models=mocker.Mock(return_value=[Model]),
    )

    # Mock.
    mocker.patch(
        "reactor.core.checks.apps.get_app_configs",
        return_value=[app_config_mock],
    )

    # Act.
    messages = checks.check_first_party_model_class()

    # Assert.
    assert messages == []


@pytest.mark.django_isolate_apps("tests")
def test_check_first_party_model_class_rejects_django_model(mocker):
    # Arrange.
    class FirstPartyModel(BaseFirstPartyModel):
        class Meta:
            app_label = "tests"

    class DjangoModel(BaseDjangoModel):
        class Meta:
            app_label = "tests"

    app_config_mock = mocker.Mock(
        spec=BaseFirstPartyAppConfig,
        get_models=mocker.Mock(return_value=[FirstPartyModel, DjangoModel]),
    )

    # Mock.
    mocker.patch(
        "reactor.core.checks.apps.get_app_configs",
        return_value=[app_config_mock],
    )

    # Act.
    messages = checks.check_first_party_model_class()

    # Assert.
    assert len(messages) == 1
    assert messages[0].id == "core.models.E001"
    assert messages[0].obj == DjangoModel


@pytest.mark.django_isolate_apps("tests")
def test_check_first_party_model_class_skips_django_app_config(mocker):
    # Arrange.
    class DjangoModel(BaseDjangoModel):
        class Meta:
            app_label = "tests"

    django_app_config_mock = mocker.Mock(
        spec=BaseDjangoAppConfig,
        get_models=mocker.Mock(return_value=[DjangoModel]),
    )

    # Mock.
    mocker.patch(
        "reactor.core.checks.apps.get_app_configs",
        return_value=[django_app_config_mock],
    )

    # Act.
    messages = checks.check_first_party_model_class()

    # Assert.
    assert messages == []
