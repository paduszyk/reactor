import functools

from django.core.exceptions import ImproperlyConfigured
from django.db import models as django_models
from django.db.models.signals import ModelSignal


class Model(django_models.Model):
    _is_ready = False
    _ready_hooks = ("_connect_signal_receivers",)

    class Meta:
        abstract = True

    @classmethod
    def ready(cls):
        if cls._is_ready:
            return

        for ready_hook in cls._ready_hooks:
            getattr(cls, ready_hook)()

        cls._is_ready = True

    @staticmethod
    def _dispatch_signal_receiver(method_name, sender, **kwargs):
        signal_receiver = getattr(kwargs.get("instance", sender), method_name)

        return signal_receiver(**kwargs)

    @classmethod
    def _connect_signal_receivers(cls):
        signal_receivers = getattr(cls, "signal_receivers", {})

        if not isinstance(signal_receivers, dict):
            detail = (
                "must be a dict of model signals to receiver method names, "
                f"got {type(signal_receivers)}"
            )
            raise cls._invalid_signal_receivers_error(detail)

        for model_signal, receiver_names in signal_receivers.items():
            if not isinstance(model_signal, ModelSignal):
                detail = (
                    f"keys must be instances of {ModelSignal}, got {type(model_signal)}"
                )
                raise cls._invalid_signal_receivers_error(detail)

            if isinstance(receiver_names, str):
                receiver_names = (receiver_names,)  # noqa: PLW2901
            elif not isinstance(receiver_names, (list, tuple)):
                detail = (
                    f"values must be strings or lists/tuples of strings, "
                    f"got {type(receiver_names)} for signal {model_signal}"
                )
                raise cls._invalid_signal_receivers_error(detail)

            for receiver_name in receiver_names:
                if not isinstance(receiver_name, str):
                    detail = (
                        f"method name for signal {model_signal} must be a string, "
                        f"got {type(receiver_name)}"
                    )
                    raise cls._invalid_signal_receivers_error(detail)

                if not (
                    hasattr(cls, receiver_name)
                    and callable(getattr(cls, receiver_name))
                ):
                    detail = (
                        f"name '{receiver_name}' for signal {model_signal} does "
                        f"not refer to a model method"
                    )
                    raise cls._invalid_signal_receivers_error(detail)

                model_signal.connect(
                    receiver=functools.partial(
                        cls._dispatch_signal_receiver,
                        receiver_name,
                    ),
                    sender=cls,
                    weak=False,
                    dispatch_uid=(model_signal, cls._meta.label_lower, receiver_name),
                )

    @classmethod
    def _invalid_signal_receivers_error(cls, detail):
        msg = f"invalid 'signal_receivers' for {cls._meta.label} model; {detail}"
        return ImproperlyConfigured(msg)
