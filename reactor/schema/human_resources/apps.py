from django.utils.translation import gettext_lazy as _

from reactor import apps


class HumanResourcesConfig(apps.AppConfig):
    """Represents the `human_resources` app and its configuration."""

    name = "reactor.schema.human_resources"
    verbose_name = _("Human Resources")
