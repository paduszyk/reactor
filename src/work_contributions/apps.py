from django.utils.translation import gettext_lazy as _

from reactor import apps

__all__ = ["WorkContributionsConfig"]


class WorkContributionsConfig(apps.AppConfig):
    """Represents the `work_contributions` app and its configuration."""

    name = "work_contributions"
    verbose_name = _("Work Contributions")
