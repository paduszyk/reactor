from django.utils.translation import gettext_lazy as _

from reactor import apps


class EvaluationConfig(apps.AppConfig):
    name = "reactor.schema.evaluation"
    verbose_name = _("Evaluation")
