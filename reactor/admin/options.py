__all__ = [
    "ModelAdmin",
]

from django.contrib import admin


class ModelAdmin(admin.ModelAdmin):
    """Represent the base for defining admin options for local models."""
