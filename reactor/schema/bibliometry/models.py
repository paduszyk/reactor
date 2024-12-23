from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _

from reactor.db import models


class ImpactFactor(models.Model):
    # Local fields.
    value_2_year = models.DecimalField(
        verbose_name=_("2-year value"),
        max_digits=6,
        decimal_places=3,
    )
    value_5_year = models.DecimalField(
        verbose_name=_("5-year value"),
        max_digits=6,
        decimal_places=3,
    )
    year_published = models.PositiveSmallIntegerField(
        verbose_name=_("year published"),
    )

    # Relations.
    journal = models.ForeignKey(
        to="publishers.Journal",
        on_delete=models.CASCADE,
        related_name="impact_factors",
        related_query_name="impact_factor",
        verbose_name=_("journal"),
    )

    class Meta:
        verbose_name = _("Impact Factor")
        verbose_name_plural = _("Impact Factors")

    def get_journal_str(self):
        publishing_house = (journal := self.journal).publishing_house

        return (
            f"{journal.abbreviation} "
            f"({publishing_house.abbreviation or publishing_house.name})"
        )

    def __str__(self):
        return gettext(
            "IF[%(journal)s; %(year_published)d] = "
            "%(value_2_year).3f (2-year) / %(value_5_year).3f (5-year)",
        ) % {
            "journal": self.get_journal_str(),
            "year_published": self.year_published,
            "value_2_year": self.value_2_year,
            "value_5_year": self.value_5_year,
        }


class MinistryScore(models.Model):
    # Local fields.
    value = models.PositiveSmallIntegerField(
        verbose_name=_("value"),
    )
    date_published = models.DateField(
        verbose_name=_("date published"),
    )

    # Relations.
    journal = models.ForeignKey(
        to="publishers.Journal",
        on_delete=models.CASCADE,
        related_name="ministry_scores",
        related_query_name="ministry_score",
        verbose_name=_("journal"),
    )

    class Meta:
        verbose_name = _("ministry score")
        verbose_name_plural = _("ministry scores")

    def get_journal_str(self):
        publishing_house = (journal := self.journal).publishing_house

        return (
            f"{journal.abbreviation} "
            f"({publishing_house.abbreviation or publishing_house.name})"
        )

    def __str__(self):
        return gettext("MS[%(journal)s; %(date_published)s] = %(value)d") % {
            "journal": self.get_journal_str(),
            "date_published": self.date_published,
            "value": self.value,
        }
