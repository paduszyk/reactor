__all__ = [
    "Model",
]

import functools

from django.core.exceptions import ImproperlyConfigured
from django.db.models.base import Model as BaseModel
from django.db.models.signals import ModelSignal


class Model(BaseModel):
    class Meta:
        abstract = True

    receivers = None

    @classmethod
    def ready(cls):
        cls._connect_signals()

    @classmethod
    def _receiver(cls, name, sender, **kwargs):
        receiver = getattr(kwargs.get("instance", sender), name)

        return receiver(**kwargs)

    @classmethod
    def _connect_signals(cls):
        receivers = cls.receivers or {}

        for signal, method_names in receivers.items():
            if not isinstance(signal, ModelSignal):
                msg = (
                    f"invalid 'receivers' for {cls._meta.label} model; "
                    f"keys must be instances of {ModelSignal}, got {type(signal)}"
                )
                raise ImproperlyConfigured(msg)

            for method_name in method_names:
                if not callable(getattr(cls, method_name, None)):
                    msg = (
                        f"invalid 'receivers' for {cls._meta.label} model; name "
                        f"'{method_name}' for signal {signal} does not refer to "
                        f"a model method"
                    )
                    raise ImproperlyConfigured(msg)

                signal.connect(
                    receiver=functools.partial(cls._receiver, method_name),
                    sender=cls,
                    weak=False,
                    dispatch_uid=(signal, cls._meta.label_lower, method_name),
                )
