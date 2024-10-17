__all__ = [
    "NameModel",
]

from django.db import models
from django.utils.translation import gettext_lazy as _

from . import base


class NameModel(base.Model):
    name = models.CharField(
        verbose_name=_("name"),
        max_length=255,
    )

    class Meta:
        abstract = True
