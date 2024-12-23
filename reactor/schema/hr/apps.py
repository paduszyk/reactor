from django.utils.translation import gettext_lazy as _

from reactor import apps


class HrConfig(apps.AppConfig):
    name = "reactor.schema.hr"
    verbose_name = _("HR")
