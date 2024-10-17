from django.utils.translation import gettext_lazy as _

from reactor.db import models


class ImpactFactor(models.Model):
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


class MinisterialRating(models.Model):
    value = models.PositiveSmallIntegerField(
        verbose_name=_("value"),
    )
    date_published = models.DateField(
        verbose_name=_("date published"),
    )
    journal = models.ForeignKey(
        to="publishers.Journal",
        on_delete=models.CASCADE,
        related_name="ministerial_ratings",
        related_query_name="ministerial_rating",
        verbose_name=_("journal"),
    )

    class Meta:
        verbose_name = _("ministerial rating")
        verbose_name_plural = _("ministerial ratings")
