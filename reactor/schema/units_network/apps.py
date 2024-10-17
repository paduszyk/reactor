from django.utils.translation import gettext_lazy as _

from reactor import apps


class UnitsNetworkConfig(apps.AppConfig):
    name = "reactor.schema.units_network"
    verbose_name = _("Units Network")
