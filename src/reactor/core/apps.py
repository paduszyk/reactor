__all__ = [
    "CoreConfig",
]

from reactor import apps


class CoreConfig(apps.AppConfig):
    """Represents the `core` app and its configuration."""

    name = "reactor.core"
