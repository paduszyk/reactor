__all__ = [
    "AppsConfig",
]

from reactor import apps


class AppsConfig(apps.AppConfig):
    """Represents the `apps` app and its configuration."""

    name = "reactor.apps"
