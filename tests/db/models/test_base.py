import pytest

from django.core.exceptions import ImproperlyConfigured
from django.db.models.signals import ModelSignal

from reactor.db.models.base import Model as BaseFirstPartyModel


@pytest.mark.django_isolate_apps("tests")
def test_model_ready_calls_all_ready_hooks(mocker):
    # Arrange.
    class Model(BaseFirstPartyModel):
        _ready_hooks = (
            "ready_hook_a",
            "ready_hook_b",
        )

        class Meta:
            app_label = "tests"

        @classmethod
        def ready_hook_a(cls):
            return None

        @classmethod
        def ready_hook_b(cls):
            return None

    # Spies.
    ready_hook_a_spy = mocker.spy(Model, "ready_hook_a")
    ready_hook_b_spy = mocker.spy(Model, "ready_hook_b")

    # Act.
    Model.ready()

    # Assert.
    ready_hook_a_spy.assert_called_once()
    ready_hook_b_spy.assert_called_once()


@pytest.mark.django_isolate_apps("tests")
def test_model_ready_is_idempotent_for_same_model(mocker):
    # Arrange.
    class Model(BaseFirstPartyModel):
        _ready_hooks = ("ready_hook",)

        class Meta:
            app_label = "tests"

        @classmethod
        def ready_hook(cls):
            return None

    # Spy.
    ready_hook_spy = mocker.spy(Model, "ready_hook")

    # Act.
    Model.ready()
    Model.ready()

    # Assert.
    ready_hook_spy.assert_called_once()


@pytest.mark.django_isolate_apps("tests")
def test_model_ready_connects_class_method_as_model_signal_receiver(mocker):
    # Arrange.
    model_signal = ModelSignal()

    class Model(BaseFirstPartyModel):
        class Meta:
            app_label = "tests"

        signal_receivers = {model_signal: "receiver"}

        @classmethod
        def receiver(cls, **kwargs):
            return None

    # Spy.
    receiver_spy = mocker.spy(Model, "receiver")

    # Act.
    Model.ready()
    model_signal.send(sender=Model)

    # Assert.
    receiver_spy.assert_called_once_with(signal=model_signal)


@pytest.mark.django_isolate_apps("tests")
def test_model_ready_connects_instance_method_as_model_signal_receiver(mocker):
    # Arrange.
    model_signal = ModelSignal()

    class Model(BaseFirstPartyModel):
        class Meta:
            app_label = "tests"

        signal_receivers = {model_signal: "receiver"}

        def receiver(self, **kwargs):
            return None

    model_instance = Model()

    # Spy.
    receiver_spy = mocker.spy(model_instance, "receiver")

    # Act.
    Model.ready()
    model_signal.send(sender=Model, instance=model_instance)

    # Assert.
    receiver_spy.assert_called_once_with(signal=model_signal, instance=model_instance)


@pytest.mark.django_isolate_apps("tests")
def test_model_ready_rejects_invalid_signal_receiver_key(mocker):
    # Arrange.
    class Model(BaseFirstPartyModel):
        class Meta:
            app_label = "tests"

        signal_receivers = {mocker.sentinel.not_a_model_signal: "receiver"}

        def receiver(**kwargs):
            return None

    # Act & assert.
    with pytest.raises(ImproperlyConfigured):
        Model.ready()


@pytest.mark.django_isolate_apps("tests")
def test_model_ready_rejects_non_dict_signal_receivers(mocker):
    # Arrange.
    class Model(BaseFirstPartyModel):
        class Meta:
            app_label = "tests"

        signal_receivers = mocker.sentinel.not_a_dict

        def receiver(**kwargs):
            return None

    # Act & assert.
    with pytest.raises(ImproperlyConfigured):
        Model.ready()


@pytest.mark.django_isolate_apps("tests")
def test_model_ready_connects_single_method_name_as_string(mocker):
    # Arrange.
    model_signal = ModelSignal()

    class Model(BaseFirstPartyModel):
        class Meta:
            app_label = "tests"

        signal_receivers = {model_signal: "receiver"}

        def receiver(self, **kwargs):
            return None

    model_instance = Model()

    # Spy.
    receiver_spy = mocker.spy(model_instance, "receiver")

    # Act.
    Model.ready()
    model_signal.send(sender=Model, instance=model_instance)

    # Assert.
    receiver_spy.assert_called_once_with(signal=model_signal, instance=model_instance)


@pytest.mark.django_isolate_apps("tests")
@pytest.mark.parametrize(
    "receiver_names",
    [
        pytest.param(("receiver_a", "receiver_b"), id="tuple"),
        pytest.param(["receiver_a", "receiver_b"], id="list"),
    ],
)
def test_model_ready_connects_multiple_method_names(mocker, receiver_names):
    # Arrange.
    model_signal = ModelSignal()

    class Model(BaseFirstPartyModel):
        class Meta:
            app_label = "tests"

        signal_receivers = {model_signal: receiver_names}

        def receiver_a(self, **kwargs):
            return None

        def receiver_b(self, **kwargs):
            return None

    model_instance = Model()

    # Spy.
    receiver_a_spy = mocker.spy(model_instance, "receiver_a")
    receiver_b_spy = mocker.spy(model_instance, "receiver_b")

    # Act.
    Model.ready()
    model_signal.send(sender=Model, instance=model_instance)

    # Assert.
    receiver_a_spy.assert_called_once_with(signal=model_signal, instance=model_instance)
    receiver_b_spy.assert_called_once_with(signal=model_signal, instance=model_instance)


@pytest.mark.django_isolate_apps("tests")
@pytest.mark.parametrize(
    "invalid_receiver_names",
    [
        pytest.param(42, id="unsupported container type"),
        pytest.param({"receiver"}, id="set is unsupported"),
        pytest.param(["receiver", 42], id="list contains non-string"),
        pytest.param(("receiver", 42), id="tuple contains non-string"),
    ],
)
def test_model_ready_rejects_invalid_signal_receiver_names(invalid_receiver_names):
    # Arrange.
    model_signal = ModelSignal()

    class Model(BaseFirstPartyModel):
        class Meta:
            app_label = "tests"

        signal_receivers = {model_signal: invalid_receiver_names}

        def receiver(**kwargs):
            return None

    # Act & assert.
    with pytest.raises(ImproperlyConfigured):
        Model.ready()


@pytest.mark.django_isolate_apps("tests")
def test_model_ready_rejects_missing_signal_receiver():
    # Arrange.
    model_signal = ModelSignal()

    class Model(BaseFirstPartyModel):
        class Meta:
            app_label = "tests"

        signal_receivers = {model_signal: ["does_not_exist"]}

    # Act & assert.
    with pytest.raises(ImproperlyConfigured):
        Model.ready()


@pytest.mark.django_isolate_apps("tests")
def test_model_ready_rejects_non_callable_signal_receiver(mocker):
    # Arrange.
    model_signal = ModelSignal()

    class Model(BaseFirstPartyModel):
        class Meta:
            app_label = "tests"

        signal_receivers = {model_signal: ["receiver"]}

        receiver = mocker.NonCallableMock()

    # Act & assert.
    with pytest.raises(ImproperlyConfigured):
        Model.ready()
