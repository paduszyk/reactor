__all__ = [
    "Model",
]

from django.db import models


class Model(models.Model):
    class Meta:
        abstract = True

    signal_receivers = {}

    @classmethod
    def ready(cls):
        pass
