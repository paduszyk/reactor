from django.utils.translation import gettext_lazy as _

from reactor import apps

__all__ = ["ContractsConfig"]


class ContractsConfig(apps.AppConfig):
    """Represents the `contracts` app and its configuration."""

    name = "contracts"
    verbose_name = _("Contracts")
