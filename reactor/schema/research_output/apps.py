from django.utils.translation import gettext_lazy as _

from reactor import apps


class ResearchOutputConfig(apps.AppConfig):
    name = "reactor.schema.research_output"
    verbose_name = _("Research Output")
