__all__ = [
    "Model",
]

from django.db import models


class Model(models.Model):
    """Represents the base for defining local models."""

    class Meta:
        abstract = True
