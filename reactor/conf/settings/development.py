from dotenv import load_dotenv

from .common import Settings as Common


class Settings(Common):
    @classmethod
    def pre_load(cls):
        super().pre_load()

        load_dotenv()

    # Debugging

    DEBUG = True

    # Security

    SECRET_KEY = "django-insecure-secret-key"  # noqa: S105


Settings.load(__name__)
