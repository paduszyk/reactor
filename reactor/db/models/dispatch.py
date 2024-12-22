from functools import partial

from django.db.models import signals

signal_receivers = {
    name: value
    for name, value in signals.__dict__.items()
    if isinstance(value, signals.Signal)
}


def connect_signals(model):
    receivers = {
        **signal_receivers,
        **getattr(model, "signal_receivers", {}),
    }

    for name, signal in receivers.items():
        if not callable(getattr(model, name, None)):
            continue

        signal.connect(
            receiver=partial(
                lambda name, sender, **kwargs: getattr(
                    kwargs.get("instance") or sender,
                    name,
                )(**kwargs),
                name,
            ),
            sender=model,
            weak=False,
            dispatch_uid=f"{model._meta.label_lower}.{name}",
        )
