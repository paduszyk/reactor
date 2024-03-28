from django.contrib.contenttypes.fields import GenericRelation
from django.utils.translation import gettext_lazy as _

from reactor.db import models

__all__ = ["Department", "Institute", "Institution"]


class Unit(models.Model):
    """Represents an abstract unit."""

    # Local fields.
    name = models.CharField(_("name"), max_length=255)

    # Reverse generic relations.
    contracts = GenericRelation(
        "contracts.Contract",
        content_type_field="unit_type",
        object_id_field="unit_id",
        related_query_name="%(class)s",
    )
    contributions = GenericRelation(
        "work_contributions.Contribution",
        content_type_field="unit_type",
        object_id_field="unit_id",
        related_query_name="%(class)s",
    )

    class Meta:
        abstract = True


class Institution(Unit):
    """Represents an institution."""

    class Meta:
        verbose_name = _("institution")
        verbose_name_plural = _("institutions")


class Institute(Unit):
    """Represents an institute."""

    # Relations.
    institution = models.ForeignKey(
        "units_network.Institution",
        on_delete=models.CASCADE,
        verbose_name=_("institution"),
    )

    class Meta:
        verbose_name = _("institute")
        verbose_name_plural = _("institutes")


class Department(Unit):
    """Represents a department."""

    # Relations.
    institute = models.ForeignKey(
        "units_network.Institute",
        on_delete=models.CASCADE,
        verbose_name=_("institute"),
    )

    class Meta:
        verbose_name = _("department")
        verbose_name_plural = _("departments")
