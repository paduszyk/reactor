from django.utils.translation import gettext_lazy as _

from reactor import apps

__all__ = ["ResearchWorksConfig"]


class ResearchWorksConfig(apps.AppConfig):
    """Represents the `research_works` app and its configuration."""

    name = "research_works"
    verbose_name = _("Research Works")
