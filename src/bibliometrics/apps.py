from django.utils.translation import gettext_lazy as _

from reactor import apps

__all__ = ["BibliometricsConfig"]


class BibliometricsConfig(apps.AppConfig):
    """Represents the `bibliometrics` app and its configuration."""

    name = "bibliometrics"
    verbose_name = _("Bibliometrics")
