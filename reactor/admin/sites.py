__all__ = [
    "AdminSite",
]

from django.contrib import admin


class AdminSite(admin.AdminSite):
    """Represents the default admin site of the project."""
