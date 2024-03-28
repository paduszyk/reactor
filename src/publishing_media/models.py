from django.utils.translation import gettext_lazy as _

from reactor.db import models

__all__ = ["Journal", "Publisher"]


class Publisher(models.Model):
    """Represents a publisher."""

    # Local fields.
    name = models.CharField(_("name"), max_length=255)

    # Relations.
    media_types = models.ManyToManyField(
        "contenttypes.ContentType",
        related_name="+",
        verbose_name=_("media types"),
    )

    class Meta:
        verbose_name = _("publisher")
        verbose_name_plural = _("publishers")


class Journal(models.Model):
    """Represents a journal."""

    # Local fields.
    title = models.CharField(_("title"), max_length=255)
    abbreviation = models.CharField(_("abbreviation"), max_length=255)

    # Relations.
    publisher = models.ForeignKey(
        "publishing_media.Publisher",
        on_delete=models.CASCADE,
        verbose_name=_("publisher"),
    )

    class Meta:
        verbose_name = _("journal")
        verbose_name_plural = _("journals")
