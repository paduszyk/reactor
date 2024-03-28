from reactor import apps

__all__ = ["DbConfig"]


class DbConfig(apps.AppConfig):
    """Represents the `db` app and its configuration."""

    name = "reactor.db"
