from django.utils.translation import gettext_lazy as _

from reactor.db import models


class PublishingHouse(models.Model):
    """Represents a publishing house."""

    name = models.CharField(
        verbose_name=_("name"),
        max_length=255,
    )

    class Meta:
        verbose_name = _("publishing house")
        verbose_name_plural = _("publishing houses")


class Journal(models.Model):
    """Represents a journal."""

    title = models.CharField(
        verbose_name=_("name"),
        max_length=255,
    )
    publishing_house = models.ForeignKey(
        to="publishers.PublishingHouse",
        on_delete=models.CASCADE,
        related_name="journals",
        related_query_name="journal",
        verbose_name=_("publishing house"),
    )

    class Meta:
        verbose_name = _("journal")
        verbose_name_plural = _("journals")
