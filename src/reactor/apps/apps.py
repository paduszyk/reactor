from reactor import apps

__all__ = ["AppsConfig"]


class AppsConfig(apps.AppConfig):
    """Represents the `apps` app and its configuration."""

    name = "reactor.apps"
