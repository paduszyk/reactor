from django.utils.translation import gettext_lazy as _

from reactor.db import models


class PublishingHouse(models.Model):
    # Local fields.
    name = models.CharField(
        verbose_name=_("name"),
        max_length=255,
    )
    abbreviation = models.CharField(
        verbose_name=_("abbreviation"),
        max_length=255,
        blank=True,
    )

    class Meta:
        verbose_name = _("publishing house")
        verbose_name_plural = _("publishing houses")


class Journal(models.Model):
    # Local fields.
    title = models.CharField(
        verbose_name=_("title"),
        max_length=255,
    )
    abbreviation = models.CharField(
        verbose_name=_("abbreviation"),
        max_length=255,
    )
    issn_p = models.CharField(
        verbose_name=_("p-ISSN"),
        max_length=255,
        blank=True,
    )
    issn_e = models.CharField(
        verbose_name=_("e-ISSN"),
        max_length=255,
        blank=True,
    )

    # Relations.
    publishing_house = models.ForeignKey(
        to="publishers.PublishingHouse",
        on_delete=models.CASCADE,
        related_name="journals",
        related_query_name="journal",
        verbose_name=_("publishing house"),
    )
    disciplines = models.ManyToManyField(
        to="evaluation.Discipline",
        related_name="journals",
        related_query_name="journal",
        verbose_name=_("disciplines"),
        blank=True,
    )

    class Meta:
        verbose_name = _("journal")
        verbose_name_plural = _("journals")
