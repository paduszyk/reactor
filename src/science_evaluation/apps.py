from django.utils.translation import gettext_lazy as _

from reactor import apps

__all__ = ["ScienceEvaluationConfig"]


class ScienceEvaluationConfig(apps.AppConfig):
    """Represents the `science_evaluation` app and its configuration."""

    name = "science_evaluation"
    verbose_name = _("Science Evaluation")
