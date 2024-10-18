from django.contrib.admin import apps


class AdminConfig(apps.AdminConfig):
    """Represents the `admin` app and its configuration."""

    default_site = "reactor.admin.sites.AdminSite"
