from django.utils.translation import gettext_lazy as _

from reactor import apps


class ScienceClassificationConfig(apps.AppConfig):
    name = "reactor.schema.science_classification"
    verbose_name = _("Science Classification")
