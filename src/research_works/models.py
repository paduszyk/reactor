from django.contrib.contenttypes.fields import GenericRelation
from django.utils.translation import gettext_lazy as _

from reactor.db import models

__all__ = ["Article", "Book", "Patent"]


class Work(models.Model):
    """Represents an abstract work."""

    # Local fields.
    title = models.TextField(_("title"))
    year_published = models.PositiveSmallIntegerField(_("year published"))
    doi = models.CharField(_("DOI"), max_length=255, blank=True)

    # Reverse generic relations.
    contributions = GenericRelation(
        "work_contributions.Contribution",
        content_type_field="work_type",
        object_id_field="work_id",
        related_query_name="%(class)s",
    )

    class Meta:
        abstract = True


class Article(Work):
    """Represents an article."""

    # Local fields.
    volume_issue = models.CharField(_("volume/issue"), max_length=255, blank=True)
    pagination = models.CharField(_("pagination"), max_length=255, blank=True)

    # Relations.
    journal = models.ForeignKey(
        "publishing_media.Journal",
        on_delete=models.CASCADE,
        verbose_name=_("journal"),
    )

    class Meta:
        verbose_name = _("article")
        verbose_name_plural = _("articles")


class Book(Work):
    """Represents a book or a book chapter."""

    # Local fields.
    chapter_title = models.TextField(_("chapter title"), blank=True)
    pagination = models.CharField(_("pagination"), max_length=255, blank=True)
    isbn = models.CharField(_("ISBN"), max_length=255, blank=True)

    # Relations.
    publisher = models.ForeignKey(
        "publishing_media.Publisher",
        on_delete=models.CASCADE,
        verbose_name=_("publisher"),
    )

    class Meta:
        verbose_name = _("book/chapter")
        verbose_name_plural = _("books & chapters")


class Patent(Work):
    """Represents a patent."""

    # Local fields.
    number = models.CharField(_("number"), max_length=255)
    date_filed = models.DateField(_("date filed"))
    date_published = models.DateField(_("date published"), blank=True, null=True)

    class Meta:
        verbose_name = _("patent")
        verbose_name_plural = _("patents")

    # Patents don't use DOIs.
    doi = None

    # Patents use dates of filing and (optionally) publication.
    year_published = None
