from django.utils.translation import gettext_lazy as _

from reactor import apps


class UnitsConfig(apps.AppConfig):
    name = "reactor.schema.units"
    verbose_name = _("Units")
