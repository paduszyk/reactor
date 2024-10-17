from django.utils.translation import gettext_lazy as _

from reactor.db import models


class Degree(models.Model):
    name = models.CharField(
        verbose_name=_("name"),
        max_length=255,
    )

    class Meta:
        verbose_name = _("degree")
        verbose_name_plural = _("degrees")


class Domain(models.Model):
    name = models.CharField(
        verbose_name=_("name"),
        max_length=255,
    )

    class Meta:
        verbose_name = _("domain")
        verbose_name_plural = _("domains")


class Discipline(models.Model):
    name = models.CharField(
        verbose_name=_("name"),
        max_length=255,
    )
    domain = models.ForeignKey(
        to="science_classification.Domain",
        on_delete=models.CASCADE,
        related_name="disciplines",
        related_query_name="discipline",
        verbose_name=_("domain"),
    )

    class Meta:
        verbose_name = _("discipline")
        verbose_name_plural = _("disciplines")
