from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _

from reactor.db import models
from reactor.utils.parsers import HumanName


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
        related_name="person",
        related_query_name="person",
        verbose_name=_("user"),
        blank=True,
        null=True,
    )
    degree = models.ForeignKey(
        to="evaluation.Degree",
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

    def __str__(self):
        return "{}{}".format(
            self.human_name.full,
            f", {degree}" if (degree := self.degree) else "",
        )

    @property
    def human_name(self):
        return HumanName(f"{self.last_name}, {self.given_names}")


class Status(models.Model):
    # Local fields.
    name = models.CharField(
        verbose_name=_("name"),
        max_length=255,
    )

    class Meta:
        verbose_name = _("status")
        verbose_name_plural = _("statuses")

    def __str__(self):
        return self.name


class Group(models.Model):
    # Local fields.
    name = models.CharField(
        verbose_name=_("name"),
        max_length=255,
    )

    class Meta:
        verbose_name = _("group")
        verbose_name_plural = _("groups")

    def __str__(self):
        return self.name


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
        related_name="subgroups",
        related_query_name="subgroup",
        verbose_name=_("group"),
    )

    class Meta:
        verbose_name = _("subgroup")
        verbose_name_plural = _("subgroups")

    def __str__(self):
        return gettext("%(name)s (in group: %(group)s)") % {
            "name": self.name,
            "group": self.group.name,
        }


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
        related_name="positions",
        related_query_name="position",
        verbose_name=_("subgroup"),
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _("position")
        verbose_name_plural = _("positions")

    def __str__(self):
        return (
            gettext("%(name)s (in subgroup: %(subgroup)s)")
            % {
                "name": self.name,
                "subgroup": subgroup.name,
            }
            if (subgroup := self.subgroup)
            else self.name
        )


class Contract(models.Model):
    # Relations.
    person = models.ForeignKey(
        to="hr.Person",
        on_delete=models.CASCADE,
        related_name="contracts",
        related_query_name="contract",
        verbose_name=_("person"),
    )
    status = models.ForeignKey(
        to="hr.Status",
        on_delete=models.CASCADE,
        related_name="contracts",
        related_query_name="contract",
        verbose_name=_("status"),
    )
    position = models.ForeignKey(
        to="hr.Position",
        on_delete=models.SET_NULL,
        related_name="contracts",
        related_query_name="contract",
        verbose_name=_("position"),
        blank=True,
        null=True,
    )
    disciplines = models.ManyToManyField(
        to="evaluation.Discipline",
        related_name="contracts",
        related_query_name="contract",
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

    def __str__(self):
        return gettext("%(person)s (%(position_or_status)s at %(unit)s)") % {
            "person": self.person.human_name.full_reversed,
            "position_or_status": (self.position or self.status).name,
            "unit": self.unit.get_full_abbreviation(),
        }
