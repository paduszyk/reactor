from django.contrib.contenttypes.fields import GenericRelation
from django.utils.translation import gettext_lazy as _

from reactor.db import models


class Unit(models.Model):
    # Local fields.
    name = models.CharField(
        verbose_name=_("name"),
        max_length=255,
    )
    abbreviation = models.CharField(
        verbose_name=_("abbreviation"),
        max_length=255,
    )

    # Reverse generic relations.
    contracts = GenericRelation(
        to="hr.Contract",
        content_type_field="unit_type",
        object_id_field="unit_id",
        related_query_name="%(class)s",
    )
    contributions = GenericRelation(
        to="output.Contribution",
        content_type_field="unit_type",
        object_id_field="unit_id",
        related_query_name="%(class)s",
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_full_abbreviation()})"

    def get_parent(self):
        return None

    def get_ancestors(self):
        ancestors = [self]

        while parent := ancestors[-1].get_parent():
            ancestors.append(parent)

        return ancestors[1:]

    def get_full_name(self):
        return self._get_full_field("name", sep=", ")

    def get_full_abbreviation(self):
        return self._get_full_field("abbreviation", sep="/")

    def _get_full_field(self, field_name, *, sep):
        return sep.join(
            getattr(ancestor, field_name) for ancestor in [self, *self.get_ancestors()]
        )


class Institution(Unit):
    class Meta:
        verbose_name = _("institution")
        verbose_name_plural = _("institutions")

    def get_parent(self):
        return None


class Institute(Unit):
    # Relations.
    institution = models.ForeignKey(
        to="units.Institution",
        on_delete=models.CASCADE,
        related_name="institutes",
        related_query_name="institute",
        verbose_name=_("institution"),
    )

    class Meta:
        verbose_name = _("institute")
        verbose_name_plural = _("institutes")

    def get_parent(self):
        return self.institution


class Department(Unit):
    # Relations.
    institute = models.ForeignKey(
        to="units.Institute",
        on_delete=models.CASCADE,
        related_name="departments",
        related_query_name="department",
        verbose_name=_("institute"),
    )

    class Meta:
        verbose_name = _("department")
        verbose_name_plural = _("departments")

    def get_parent(self):
        return self.institute
