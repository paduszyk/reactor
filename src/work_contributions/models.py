from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.translation import gettext_lazy as _

from reactor.db import models

__all__ = ["Author", "Contribution"]


class Author(models.Model):
    """Represents an author of a work."""

    # Local fields.
    alias = models.CharField(_("alias"), max_length=255, blank=True)

    # Relations.
    contract = models.ForeignKey(
        "contracts.Contract",
        on_delete=models.SET_NULL,
        verbose_name=_("contract"),
        blank=True,
        null=True,
    )


class Contribution(models.Model):
    """Represents a contribution to a work."""

    # Local fields.
    order = models.PositiveSmallIntegerField(_("order"))

    # Relations.
    author = models.ForeignKey(
        "work_contributions.Author",
        on_delete=models.CASCADE,
        verbose_name=_("author"),
    )
    discipline = models.ForeignKey(
        "science_evaluation.Discipline",
        on_delete=models.SET_NULL,
        verbose_name=_("scientific discipline"),
        blank=True,
        null=True,
    )

    # Generic relations.
    work_type = models.ForeignKey(
        "contenttypes.ContentType",
        on_delete=models.CASCADE,
        related_name="+",
        verbose_name=_("work type"),
    )
    work_id = models.PositiveIntegerField(_("work ID"))
    work = GenericForeignKey(ct_field="work_type", fk_field="work_id")
    unit_type = models.ForeignKey(
        "contenttypes.ContentType",
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("unit type"),
        blank=True,
        null=True,
    )
    unit_id = models.PositiveIntegerField(_("unit ID"), blank=True, null=True)
    unit = GenericForeignKey(ct_field="unit_type", fk_field="unit_id")

    class Meta:
        verbose_name = _("contribution")
        verbose_name_plural = _("contributions")
