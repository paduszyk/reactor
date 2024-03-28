from django.utils.translation import gettext_lazy as _

from reactor import apps

__all__ = ["PersonalDataConfig"]


class PersonalDataConfig(apps.AppConfig):
    """Represents the `personal_data` app and its configuration."""

    name = "personal_data"
    verbose_name = _("Personal Data")
