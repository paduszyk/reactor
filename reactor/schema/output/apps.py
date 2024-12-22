from django.utils.translation import gettext_lazy as _

from reactor import apps


class OutputConfig(apps.AppConfig):
    name = "reactor.schema.output"
    verbose_name = _("Output")
