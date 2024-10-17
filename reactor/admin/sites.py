__all__ = [
    "AdminSite",
]

from django.contrib.admin import sites as django_admin_sites


class AdminSite(django_admin_sites.AdminSite):
    pass
