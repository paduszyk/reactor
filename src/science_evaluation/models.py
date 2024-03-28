from django.utils.translation import gettext_lazy as _

from reactor.db import models

__all__ = ["Discipline", "Domain"]


class Domain(models.Model):
    """Represents a a domain of research."""

    # Local fields.
    name = models.CharField(_("name"), max_length=255)

    class Meta:
        verbose_name = _("domain of research")
        verbose_name_plural = _("domains of research")


class Discipline(models.Model):
    """Represents a scientific discipline."""

    # Local fields.
    name = models.CharField(_("name"), max_length=255)

    # Relations.
    domain = models.ForeignKey(
        "science_evaluation.Domain",
        on_delete=models.CASCADE,
        verbose_name=_("domain of research"),
    )

    class Meta:
        verbose_name = _("scientific discipline")
        verbose_name_plural = _("scientific disciplines")
