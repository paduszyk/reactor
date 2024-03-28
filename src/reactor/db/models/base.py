from django.db import models

__all__ = ["Model"]


class Model(models.Model):
    """Represents a base for defining models in the project's app."""

    class Meta:
        abstract = True
