from django.utils.translation import gettext_lazy as _

from reactor.db import models


class Degree(models.Model):
    # Local fields.
    name = models.CharField(
        verbose_name=_("name"),
        max_length=255,
    )

    class Meta:
        verbose_name = _("degree")
        verbose_name_plural = _("degrees")


class Domain(models.Model):
    # Local fields.
    name = models.CharField(
        verbose_name=_("name"),
        max_length=255,
    )

    class Meta:
        verbose_name = _("domain")
        verbose_name_plural = _("domains")


class Discipline(models.Model):
    # Local fields.
    name = models.CharField(
        verbose_name=_("name"),
        max_length=255,
    )

    # Relations.
    domain = models.ForeignKey(
        to="evaluation.Domain",
        on_delete=models.CASCADE,
        verbose_name=_("domain"),
    )

    class Meta:
        verbose_name = _("discipline")
        verbose_name_plural = _("disciplines")
