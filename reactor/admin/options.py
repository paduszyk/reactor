__all__ = [
    "ModelAdmin",
]

from django.contrib.admin import options as django_admin_options


class ModelAdmin(django_admin_options.ModelAdmin):
    pass
