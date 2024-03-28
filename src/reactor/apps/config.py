from django import apps

__all__ = ["AppConfig"]


class AppConfig(apps.AppConfig):
    """Represents a base for configuring the project's apps."""
