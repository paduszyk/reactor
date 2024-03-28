from django.utils.translation import gettext_lazy as _

from reactor import apps

__all__ = ["UnitsNetworkConfig"]


class UnitsNetworkConfig(apps.AppConfig):
    """Represents the `units_network` app and its configuration."""

    name = "units_network"
    verbose_name = _("Units Network")
