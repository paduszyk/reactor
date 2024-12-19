__all__ = [
    "Model",
]

from django.db import models


class Model(models.Model):
    class Meta:
        abstract = True

    @classmethod
    def ready(cls):
        pass
