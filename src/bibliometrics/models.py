from django.utils.translation import gettext_lazy as _

from reactor.db import models

__all__ = [
    "CiteScore",
    "GovernmentalRating",
    "ImpactFactor",
]


class Score(models.Model):
    """Represents an abstract bibliometric score."""

    # Local fields.
    value = models.DecimalField(_("value"), max_digits=6, decimal_places=3)
    year_published = models.PositiveSmallIntegerField(_("year published"))

    class Meta:
        abstract = True


class JournalScore(Score):
    """Represents an abstract bibliometric score related to a journal."""

    # Relations.
    journal = models.ForeignKey(
        "publishing_media.Journal",
        on_delete=models.CASCADE,
        verbose_name=_("journal"),
    )

    class Meta:
        abstract = True


class ImpactFactor(JournalScore):
    """Represents the Impact Factor for a journal."""

    # Local fields.
    value_2_year = models.DecimalField(
        _("value (2-year)"),
        max_digits=6,
        decimal_places=3,
    )
    value_5_year = models.DecimalField(
        _("value (5-year)"),
        max_digits=6,
        decimal_places=3,
    )

    class Meta:
        verbose_name = _("Impact Factor")
        verbose_name_plural = _("Impact Factors")

    # Impact Factors use 5-year and 2-year values.
    value = None


class CiteScore(JournalScore):
    """Represents the CiteScore for a journal."""

    class Meta:
        verbose_name = _("CiteScore")
        verbose_name_plural = _("CiteScores")


class GovernmentalRating(JournalScore):
    """Represents the Polish governmental rating for a journal."""

    # Local fields.
    date_published = models.DateField(_("date published"))

    class Meta:
        verbose_name = _("government rating")
        verbose_name_plural = _("government ratings")

    # Government ratings use dates as they may be published more than once per year.
    year_published = None
