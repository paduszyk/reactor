from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.translation import gettext_lazy as _

from reactor.db import models


class Person(models.Model):
    class GenderChoices(models.IntegerChoices):
        MAN = 1, _("man")
        WOMAN = 2, _("woman")

    last_name = models.CharField(
        verbose_name=_("last name"),
        max_length=255,
    )
    given_names = models.CharField(
        verbose_name=_("given names"),
        max_length=255,
    )
    user = models.OneToOneField(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="person",
        related_query_name="person",
        verbose_name=_("user"),
    )
    gender = models.PositiveSmallIntegerField(
        verbose_name=_("gender"),
        blank=True,
        null=True,
        choices=GenderChoices,
    )
    degree = models.ForeignKey(
        to="science_classification.Degree",
        on_delete=models.SET_NULL,
        related_name="persons",
        related_query_name="person",
        verbose_name=_("degree"),
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _("person")
        verbose_name_plural = _("persons")


class Status(models.Model):
    name = models.CharField(
        verbose_name=_("name"),
        max_length=255,
    )

    class Meta:
        verbose_name = _("status")
        verbose_name_plural = _("statuses")


class Group(models.Model):
    name = models.CharField(
        verbose_name=_("name"),
        max_length=255,
    )

    class Meta:
        verbose_name = _("group")
        verbose_name_plural = _("groups")


class Subgroup(models.Model):
    name = models.CharField(
        verbose_name=_("name"),
        max_length=255,
    )
    group = models.ForeignKey(
        to="human_resources.Group",
        on_delete=models.CASCADE,
        related_name="subgroups",
        related_query_name="subgroup",
        verbose_name=_("group"),
    )

    class Meta:
        verbose_name = _("subgroup")
        verbose_name_plural = _("subgroups")


class Position(models.Model):
    name = models.CharField(
        verbose_name=_("name"),
        max_length=255,
    )
    subgroups = models.ManyToManyField(
        to="human_resources.Subgroup",
        verbose_name=_("subgroups"),
        related_name="positions",
        related_query_name="position",
        blank=True,
    )

    class Meta:
        verbose_name = _("position")
        verbose_name_plural = _("positions")


class Contract(models.Model):
    person = models.ForeignKey(
        to="human_resources.Person",
        on_delete=models.CASCADE,
        related_name="contracts",
        related_query_name="contract",
        verbose_name=_("person"),
    )
    status = models.ForeignKey(
        to="human_resources.Status",
        on_delete=models.SET_NULL,
        related_name="contracts",
        related_query_name="contract",
        verbose_name=_("status"),
        blank=True,
        null=True,
    )
    subgroup = models.ForeignKey(
        to="human_resources.Subgroup",
        on_delete=models.SET_NULL,
        related_name="contracts",
        related_query_name="contract",
        verbose_name=_("subgroup"),
        blank=True,
        null=True,
    )
    position = models.ForeignKey(
        to="human_resources.Position",
        on_delete=models.SET_NULL,
        related_name="contracts",
        related_query_name="contract",
        verbose_name=_("position"),
        blank=True,
        null=True,
    )
    disciplines = models.ManyToManyField(
        to="science_classification.Discipline",
        verbose_name=_("disciplines"),
        related_name="contracts",
        related_query_name="contract",
        blank=True,
    )
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
