from django.contrib.contenttypes.fields import GenericRelation
from django.utils.translation import gettext_lazy as _

from reactor.db import models


class Unit(models.Model):
    """Represents an abstract organizational unit."""

    name = models.CharField(
        verbose_name=_("name"),
        max_length=255,
    )
    contracts = GenericRelation(
        to="human_resources.Contract",
        content_type_field="unit_type",
        object_id_field="unit_id",
        related_query_name="%(class)s",
    )

    class Meta:
        abstract = True


class University(Unit):
    """Represents a university.

    Universities are the at the top of the hierarchy of organizational units.
    """

    class Meta:
        verbose_name = _("university")
        verbose_name_plural = _("universities")


class Faculty(Unit):
    """Represents a faculty within a university."""

    university = models.ForeignKey(
        to="units_network.University",
        on_delete=models.CASCADE,
        related_name="faculties",
        related_query_name="faculty",
        verbose_name=_("university"),
    )

    class Meta:
        verbose_name = _("faculty")
        verbose_name_plural = _("faculties")


class Department(Unit):
    """Represents a department within a faculty."""

    faculty = models.ForeignKey(
        to="units_network.Faculty",
        on_delete=models.CASCADE,
        related_name="departments",
        related_query_name="department",
        verbose_name=_("faculty"),
    )

    class Meta:
        verbose_name = _("department")
        verbose_name_plural = _("departments")
