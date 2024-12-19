from django.utils.translation import gettext_lazy as _

from reactor import apps


class PublishersConfig(apps.AppConfig):
    name = "reactor.schema.publishers"
    verbose_name = _("Publishers")
