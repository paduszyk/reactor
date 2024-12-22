from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.utils.translation import gettext_lazy as _

from reactor.db import models


class Work(models.Model):
    # Local fields.
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
    file = models.FileField(
        verbose_name=_("file"),
        blank=True,
    )

    # Reverse generic relations.
    contributions = GenericRelation(
        "output.Contribution",
        content_type_field="work_type",
        object_id_field="work_id",
        related_query_name="%(class)s",
    )

    class Meta:
        abstract = True


class Article(Work):
    # Local fields.
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

    # Relations.
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


class Book(Work):
    # Local fields.
    edited = models.BooleanField(
        verbose_name=_("edited"),
        default=False,
    )
    isbn = models.CharField(
        verbose_name=_("ISBN"),
        max_length=255,
        blank=True,
    )

    # Relations.
    publishing_house = models.ForeignKey(
        to="publishers.PublishingHouse",
        on_delete=models.CASCADE,
        related_name="books",
        related_query_name="book",
        verbose_name=_("publishing house"),
    )

    class Meta:
        verbose_name = _("book")
        verbose_name_plural = _("books")


class Chapter(Work):
    # Local fields.
    pagination = models.CharField(
        verbose_name=_("pagination"),
        max_length=255,
        blank=True,
    )

    # Relations.
    book = models.ForeignKey(
        to="output.Book",
        on_delete=models.CASCADE,
        related_name="chapters",
        related_query_name="chapter",
        verbose_name=_("book"),
    )

    # Chapter's publication year is the same as the book's.
    year_published = None

    class Meta:
        verbose_name = _("chapter")
        verbose_name_plural = _("chapters")


class Patent(Work):
    # Local fields.
    application_number = models.CharField(
        verbose_name=_("application number"),
        max_length=255,
    )
    date_applied = models.DateField(
        verbose_name=_("date applied"),
    )
    patent_number = models.CharField(
        verbose_name=_("patent number"),
        max_length=255,
        blank=True,
    )
    date_granted = models.DateField(
        verbose_name=_("date granted"),
        blank=True,
        null=True,
    )
    implemented = models.BooleanField(
        verbose_name=_("implemented"),
        default=False,
    )

    # Patents don't have DOIs.
    doi = None

    # Patents use dates instead of years.
    year_published = None

    class Meta:
        verbose_name = _("patent")
        verbose_name_plural = _("patents")


class Author(models.Model):
    # Local fields.
    alias = models.CharField(
        verbose_name=_("alias"),
        max_length=255,
        blank=True,
    )

    # Relations.
    contract = models.ForeignKey(
        to="hr.Contract",
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
    # Local fields.
    order = models.PositiveSmallIntegerField(
        verbose_name=_("order"),
    )

    # Relations.
    author = models.ForeignKey(
        to="output.Author",
        on_delete=models.CASCADE,
        verbose_name=_("author"),
    )
    discipline = models.ForeignKey(
        to="evaluation.Discipline",
        on_delete=models.SET_NULL,
        related_name="contributions",
        related_query_name="contribution",
        verbose_name=_("discipline"),
        blank=True,
        null=True,
    )

    # Generic relations.
    work_type = models.ForeignKey(
        to="contenttypes.ContentType",
        on_delete=models.CASCADE,
        related_name="+",
        verbose_name=_("work type"),
    )
    work_id = models.PositiveBigIntegerField(
        verbose_name=_("work ID"),
    )
    work = GenericForeignKey(
        ct_field="work_type",
        fk_field="work_id",
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
        verbose_name = _("contribution")
        verbose_name_plural = _("contributions")
