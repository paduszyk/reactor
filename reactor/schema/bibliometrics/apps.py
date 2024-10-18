from django.utils.translation import gettext_lazy as _

from reactor import apps


class BibliometricsConfig(apps.AppConfig):
    """Represents the `bibliometrics` app and its configuration."""

    name = "reactor.schema.bibliometrics"
    verbose_name = _("Bibliometrics")
