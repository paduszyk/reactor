from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.utils.text import capfirst, get_text_list
from django.utils.translation import gettext, ngettext
from django.utils.translation import gettext_lazy as _

from reactor.db import models
from reactor.utils.parsers import HumanName


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

    def __str__(self):
        return ": ".join(
            filter(None, [self.get_authors_str(), self.get_citation_str()]),
        )

    @property
    def authors(self):
        opts = self._meta

        return Author.objects.filter(
            contribution__work_type__app_label=opts.app_label,
            contribution__work_type__model=opts.model_name,
            contribution__work_id=getattr(self, opts.pk.name),
        ).order_by("contribution__order")

    @staticmethod
    def get_author_str(author):
        return author.human_name.short_reversed

    def get_authors_str(self):
        return (
            get_text_list(
                list(map(self.get_author_str, authors)),
                last_word=gettext("and"),
            )
            if (authors := self.authors).exists()
            else ""
        )

    def get_citation_str(self):
        return ""


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

    def get_citation_str(self):
        parts = filter(
            None,
            [
                f"{self.journal.abbreviation} {self.year_published}",
                (
                    gettext("vol. %(volume)s") % {"volume": volume}
                    if (volume := self.volume)
                    else ""
                ),
                (
                    gettext("no. %(issue)s") % {"issue": issue}
                    if (issue := self.issue)
                    else ""
                ),
                (
                    gettext("pp. %(pagination)s") % {"pagination": pagination}
                    if (pagination := self.pagination)
                    else ""
                ),
            ],
        )

        return f"{self.title}. {', '.join(parts)}."


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

    def get_authors_str(self):
        return "{}{}".format(
            super().get_authors_str(),
            ngettext(" (Ed.)", " (Eds.)", self.authors.count()) if self.edited else "",
        )

    def get_citation_str(self):
        return f"{self.title}. {self.publishing_house.name}, {self.year_published}."


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

    def get_citation_str(self):
        return "{}. {}{}.".format(
            self.title,
            gettext("In: %(book)s") % {"book": self.get_book_str()},
            (
                gettext("; pp. %(pagination)s") % {"pagination": pagination}
                if (pagination := self.pagination)
                else ""
            ),
        )

    def get_book_str(self):
        book = self.book

        return " / ".join(
            filter(None, [book.get_citation_str(), book.get_authors_str()]),
        )


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

    def get_citation_str(self):
        number_field = self._meta.get_field(
            "patent_number" if self.patent_number else "application_number",
        )

        return "{}. {}: {}. {}{}.".format(
            self.title,
            capfirst(number_field.verbose_name),
            getattr(self, number_field.name),
            (
                gettext("Applied on %(date_applied)s")
                % {"date_applied": self.date_applied}
            ),
            (
                gettext(", granted on %(date_granted)s")
                % {"date_granted": date_granted}
                if (date_granted := self.date_granted)
                else ""
            ),
        )


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

    def __str__(self):
        return "{}{}".format(
            self.human_name.short_reversed,
            (
                gettext(" (%(position_or_status)s at %(unit)s)")
                % {
                    "position_or_status": (contract.position or contract.status).name,
                    "unit": unit.get_full_abbreviation(),
                }
                if (contract := self.contract) and (unit := contract.unit)
                else ""
            ),
        )

    @property
    def human_name(self):
        return (
            HumanName(alias)
            if (alias := self.alias)
            else self.contract.person.human_name
        )


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

    def __str__(self):
        return gettext(
            "%(author)s: author no. %(order)d of %(work_model)s ID = %(work_id)d",
        ) % {
            "author": "{}{}".format(
                self.author.human_name.short_reversed,
                (
                    f" ({unit.get_full_abbreviation()})"
                    if (unit := self.get_unit())
                    else ""
                ),
            ),
            "order": self.order,
            "work_model": self.get_work_model()._meta.verbose_name,
            "work_id": self.work_id,
        }

    def get_unit(self):
        return self.unit or (
            contract.unit if (contract := self.author.contract) else None
        )

    def get_work_model(self):
        return self.work_type.model_class()
