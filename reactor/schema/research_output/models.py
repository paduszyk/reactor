from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.translation import gettext_lazy as _

from reactor.db import models


class OutputItem(models.Model):
    """Represents an abstract output item."""

    title = models.TextField(
        verbose_name=_("title"),
    )
    year_published = models.PositiveSmallIntegerField(
        verbose_name=_("year published"),
    )
    doi = models.CharField(
        verbose_name=_("DOI"),
        max_length=255,
        blank=True,
    )

    class Meta:
        abstract = True


class Article(OutputItem):
    """Represents an article."""

    volume = models.CharField(
        verbose_name=_("volume"),
        max_length=255,
        blank=True,
    )
    issue = models.CharField(
        verbose_name=_("issue"),
        max_length=255,
        blank=True,
    )
    pagination = models.CharField(
        verbose_name=_("pagination"),
        max_length=255,
        blank=True,
    )
    journal = models.ForeignKey(
        to="publishers.Journal",
        on_delete=models.CASCADE,
        related_name="articles",
        related_query_name="article",
        verbose_name=_("journal"),
    )

    class Meta:
        verbose_name = _("article")
        verbose_name_plural = _("articles")


class Author(models.Model):
    alias = models.CharField(
        verbose_name=_("alias"),
        max_length=255,
        blank=True,
    )
    contract = models.ForeignKey(
        to="human_resources.Contract",
        on_delete=models.SET_NULL,
        related_name="authors",
        related_query_name="author",
        verbose_name=_("contract"),
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _("author")
        verbose_name_plural = _("authors")


class Contribution(models.Model):
    """Represents an abstract contribution to an output item."""

    order = models.PositiveSmallIntegerField(
        verbose_name=_("order"),
    )
    discipline = models.ForeignKey(
        to="science_classification.Discipline",
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("discipline"),
        blank=True,
        null=True,
    )
    unit_type = models.ForeignKey(
        to="contenttypes.ContentType",
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("unit type"),
        blank=True,
        null=True,
    )
    unit_id = models.PositiveBigIntegerField(
        verbose_name=_("unit ID"),
        blank=True,
        null=True,
    )
    unit = GenericForeignKey(
        ct_field="unit_type",
        fk_field="unit_id",
    )

    class Meta:
        abstract = True


class ArticleContribution(Contribution):
    """Represents an article contribution."""

    author = models.ForeignKey(
        to="research_output.Author",
        on_delete=models.CASCADE,
        related_name="article_contributions",
        related_query_name="article_contribution",
        verbose_name=_("author"),
    )
    article = models.ForeignKey(
        to="research_output.Article",
        on_delete=models.CASCADE,
        related_name="contributions",
        related_query_name="contribution",
        verbose_name=_("article"),
    )

    class Meta:
        verbose_name = _("article contribution")
        verbose_name_plural = _("article contributions")
