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

    # Relations.
    publishing_house = models.ForeignKey(
        to="publishers.PublishingHouse",
        on_delete=models.CASCADE,
        verbose_name=_("publishing house"),
    )
    discipline_set = models.ManyToManyField(
        to="evaluation.Discipline",
        verbose_name=_("disciplines"),
        blank=True,
    )

    class Meta:
        verbose_name = _("journal")
        verbose_name_plural = _("journals")
