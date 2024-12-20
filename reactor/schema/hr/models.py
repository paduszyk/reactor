from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.translation import gettext_lazy as _

from reactor.db import models


class Person(models.Model):
    # Local fields.
    last_name = models.CharField(
        verbose_name=_("last name"),
        max_length=255,
    )
    given_names = models.CharField(
        verbose_name=_("given names"),
        max_length=255,
    )

    # Relations.
    user = models.OneToOneField(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        verbose_name=_("user"),
        blank=True,
        null=True,
    )
    degree = models.ForeignKey(
        to="evaluation.Degree",
        on_delete=models.SET_NULL,
        verbose_name=_("degree"),
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _("person")
        verbose_name_plural = _("persons")


class Status(models.Model):
    # Local fields.
    name = models.CharField(
        verbose_name=_("name"),
        max_length=255,
    )

    class Meta:
        verbose_name = _("status")
        verbose_name_plural = _("statuses")


class Group(models.Model):
    # Local fields.
    name = models.CharField(
        verbose_name=_("name"),
        max_length=255,
    )

    class Meta:
        verbose_name = _("group")
        verbose_name_plural = _("groups")


class Subgroup(models.Model):
    # Local fields.
    name = models.CharField(
        verbose_name=_("name"),
        max_length=255,
    )

    # Relations.
    group = models.ForeignKey(
        to="hr.Group",
        on_delete=models.CASCADE,
        verbose_name=_("group"),
    )

    class Meta:
        verbose_name = _("subgroup")
        verbose_name_plural = _("subgroups")


class Position(models.Model):
    # Local fields.
    name = models.CharField(
        verbose_name=_("name"),
        max_length=255,
    )

    # Relations.
    subgroup = models.ForeignKey(
        to="hr.Subgroup",
        on_delete=models.SET_NULL,
        verbose_name=_("subgroup"),
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _("position")
        verbose_name_plural = _("positions")


class Contract(models.Model):
    # Relations.
    person = models.ForeignKey(
        to="hr.Person",
        on_delete=models.CASCADE,
        verbose_name=_("person"),
    )
    status = models.ForeignKey(
        to="hr.Status",
        on_delete=models.CASCADE,
        verbose_name=_("status"),
    )
    position = models.ForeignKey(
        to="hr.Position",
        on_delete=models.SET_NULL,
        verbose_name=_("position"),
        blank=True,
        null=True,
    )
    discipline_set = models.ManyToManyField(
        to="evaluation.Discipline",
        verbose_name=_("disciplines"),
        blank=True,
    )

    # Generic relations.
    unit_type = models.ForeignKey(
        to="contenttypes.ContentType",
        on_delete=models.CASCADE,
        related_name="+",
        verbose_name=_("unit type"),
    )
    unit_id = models.PositiveBigIntegerField(
        verbose_name=_("unit ID"),
    )
    unit = GenericForeignKey(
        ct_field="unit_type",
        fk_field="unit_id",
    )

    class Meta:
        verbose_name = _("contract")
        verbose_name_plural = _("contracts")
