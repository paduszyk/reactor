__all__ = [
    "Model",
]

from django.db import models


class Model(models.Model):
    """Represents a base for defining models in first-party apps."""

    class Meta:
        abstract = True
