__all__ = [
    "AppConfig",
]

from django import apps


class AppConfig(apps.AppConfig):
    def ready(self):
        super().ready()
