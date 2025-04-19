from .common import Settings as Common


class Settings(Common):
    # Debugging

    DEBUG = True

    # Security

    SECRET_KEY = "django-insecure-secret-key"  # noqa: S105

    # Storages

    STATIC_URL = "static/"

    STATIC_ROOT = Common.BASE_DIR / "staticfiles"


Settings.load(__name__)
