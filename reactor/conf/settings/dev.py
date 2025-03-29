from decouple import config

from .common import Settings as Common


class Settings(Common):
    # Debugging

    DEBUG = config("DJANGO_DEBUG", cast=bool, default=True)

    # Security

    SECRET_KEY = config("DJANGO_SECRET_KEY", default="django-insecure-secret-key")


Settings.load(__name__)
