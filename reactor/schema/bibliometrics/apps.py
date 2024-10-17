from django.utils.translation import gettext_lazy as _

from reactor import apps


class BibliometricsConfig(apps.AppConfig):
    name = "reactor.schema.bibliometrics"
    verbose_name = _("Bibliometrics")
