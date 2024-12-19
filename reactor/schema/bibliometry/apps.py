from django.utils.translation import gettext_lazy as _

from reactor import apps


class BibliometryConfig(apps.AppConfig):
    name = "reactor.schema.bibliometry"
    verbose_name = _("Bibliometry")
