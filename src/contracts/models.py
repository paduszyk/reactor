from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.translation import gettext_lazy as _

from reactor.db import models

__all__ = [
    "Contract",
    "Group",
    "Position",
    "Status",
    "Subgroup",
]


class Status(models.Model):
    """Represents a contract's status."""

    # Local fields.
    name = models.CharField(_("name"), max_length=255)

    class Meta:
        verbose_name = _("status")
        verbose_name_plural = _("statuses")


class Group(models.Model):
    """Represents a group of contracts."""

    # Local fields.
    name = models.CharField(_("name"), max_length=255)

    class Meta:
        verbose_name = _("group")
        verbose_name_plural = _("groups")


class Subgroup(models.Model):
    """Represents a subgroup of contracts."""

    # Local fields.
    name = models.CharField(_("name"), max_length=255)

    # Relations.
    group = models.ForeignKey(
        "contracts.Group",
        on_delete=models.CASCADE,
        verbose_name=_("group"),
    )

    class Meta:
        verbose_name = _("subgroup")
        verbose_name_plural = _("subgroups")


class Position(models.Model):
    """Represents a position for a contract."""

    # Local fields.
    name = models.CharField(_("name"), max_length=255)

    # Relations.
    subgroups = models.ManyToManyField(
        "contracts.Subgroup",
        verbose_name=_("subgroups"),
        blank=True,
    )

    class Meta:
        verbose_name = _("position")
        verbose_name_plural = _("positions")


class Contract(models.Model):
    """Represents a contract."""

    # Local fields.
    date_started = models.DateField(_("date started"), blank=True, null=True)
    date_ended = models.DateField(_("date ended"), blank=True, null=True)

    # Relations.
    person = models.ForeignKey(
        "personal_data.Person",
        on_delete=models.CASCADE,
        verbose_name=_("person"),
    )
    status = models.ForeignKey(
        "contracts.Status",
        on_delete=models.CASCADE,
        verbose_name=_("status"),
    )
    position = models.ForeignKey(
        "contracts.Position",
        on_delete=models.SET_NULL,
        verbose_name=_("position"),
        blank=True,
        null=True,
    )
    subgroup = models.ForeignKey(
        "contracts.Subgroup",
        on_delete=models.SET_NULL,
        verbose_name=_("subgroup"),
        blank=True,
        null=True,
    )
    disciplines = models.ManyToManyField(
        "science_evaluation.Discipline",
        verbose_name=_("disciplines"),
        blank=True,
    )

    # Generic relations.
    unit_type = models.ForeignKey(
        "contenttypes.ContentType",
        on_delete=models.CASCADE,
        related_name="+",
        verbose_name=_("unit type"),
    )
    unit_id = models.PositiveIntegerField(_("unit ID"))
    unit = GenericForeignKey(ct_field="unit_type", fk_field="unit_id")

    class Meta:
        verbose_name = _("contract")
        verbose_name_plural = _("contracts")
