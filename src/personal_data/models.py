from django.conf import settings
from django.utils.translation import gettext_lazy as _

from reactor.db import models

__all__ = [
    "Degree",
    "Gender",
    "Person",
]


class Gender(models.Model):
    """Represents a gender."""

    # Local fields.
    name = models.CharField(_("name"), max_length=255)

    class Meta:
        verbose_name = _("gender")
        verbose_name_plural = _("genders")


class Degree(models.Model):
    """Represents an academic degree or title."""

    # Local fields.
    name = models.CharField(_("name"), max_length=255)

    class Meta:
        verbose_name = _("degree/title")
        verbose_name_plural = _("degrees & titles")


class Person(models.Model):
    """Represents a person."""

    # Local fields.
    first_name = models.CharField(_("first name"), max_length=255)
    middle_names = models.CharField(_("middle names"), max_length=255, blank=True)
    last_name = models.CharField(_("last name"), max_length=255)

    # Relations.
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("user"),
    )
    gender = models.ForeignKey(
        "personal_data.Gender",
        on_delete=models.SET_NULL,
        verbose_name=_("gender"),
        blank=True,
        null=True,
    )
    degree = models.ForeignKey(
        "personal_data.Degree",
        on_delete=models.SET_NULL,
        verbose_name=_("degree/title"),
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _("person")
        verbose_name_plural = _("persons")
