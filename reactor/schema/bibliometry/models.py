from django.utils.translation import gettext_lazy as _

from reactor.db import models


class JournalScore(models.Model):
    # Relations.
    journal = models.ForeignKey(
        to="publishers.Journal",
        on_delete=models.CASCADE,
        verbose_name=_("journal"),
    )

    class Meta:
        abstract = True


class ImpactFactor(JournalScore):
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

    class Meta:
        verbose_name = _("Impact Factor")
        verbose_name_plural = _("Impact Factors")


class MinistryScore(JournalScore):
    # Local fields.
    value = models.PositiveSmallIntegerField(
        verbose_name=_("value"),
    )
    date_published = models.DateField(
        verbose_name=_("date published"),
    )

    class Meta:
        verbose_name = _("ministry score")
        verbose_name_plural = _("ministry scores")
