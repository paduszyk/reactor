import pytest

from django.core.exceptions import ImproperlyConfigured
from django.db.models.signals import ModelSignal
from django.test.utils import isolate_apps, override_settings

from reactor.db.models import base


@isolate_apps("tests")
@override_settings(INSTALLED_APPS=["tests"])
def test_model_ready_connects_signal_to_model_class_method(mocker):
    # Arrange.
    model_signal = ModelSignal()

    class Model(base.Model):
        class Meta:
            app_label = "tests"

        receivers = {model_signal: ["class_method"]}

        @classmethod
        def class_method(cls, **kwargs):
            pass

    Model.ready()

    # Spy.
    class_method_spy = mocker.spy(Model, "class_method")

    # Act.
    model_signal.send(sender=Model)

    # Assert.
    class_method_spy.assert_called_once_with(signal=model_signal)

    # Clean up.
    model_signal.disconnect(
        sender=Model,
        dispatch_uid=(model_signal, "tests.model", "class_method"),
    )


@isolate_apps("tests")
@override_settings(INSTALLED_APPS=["tests"])
def test_model_ready_connects_signal_to_model_instance_method(mocker):
    # Arrange.
    model_signal = ModelSignal()

    class Model(base.Model):
        class Meta:
            app_label = "tests"

        receivers = {model_signal: ["instance_method"]}

        def instance_method(self, **kwargs):
            pass

    Model.ready()
    instance = Model()

    # Spy.
    instance_method_spy = mocker.spy(instance, "instance_method")

    # Act.
    model_signal.send(sender=Model, instance=instance)

    # Assert.
    instance_method_spy.assert_called_once_with(signal=model_signal, instance=instance)

    # Clean up.
    model_signal.disconnect(
        sender=Model,
        dispatch_uid=(model_signal, "tests.model", "instance_method"),
    )


@isolate_apps("tests")
@override_settings(INSTALLED_APPS=["tests"])
def test_model_ready_raises_error_for_invalid_signal_in_receivers():
    # Arrange.
    class NotASignal:
        pass

    not_a_signal = NotASignal()

    class Model(base.Model):
        class Meta:
            app_label = "tests"

        receivers = {not_a_signal: ["instance_method"]}

        def instance_method(self, **kwargs):
            pass

    # Act & assert.
    with pytest.raises(ImproperlyConfigured):
        Model.ready()


@isolate_apps("tests")
@override_settings(INSTALLED_APPS=["tests"])
def test_model_ready_raises_error_for_invalid_method_name_in_receivers():
    # Arrange.
    model_signal = ModelSignal()

    class Model(base.Model):
        class Meta:
            app_label = "tests"

        receivers = {model_signal: ["does_not_exist"]}

    # Act & assert.
    with pytest.raises(ImproperlyConfigured):
        Model.ready()
