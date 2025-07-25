from pathlib import Path

import dj_database_url as dj_db_url
from decouple import UndefinedValueError, config

from django.utils.translation import gettext_lazy as _

from .base import Settings as Base


class Settings(Base):
    # Paths

    PROJECT_DIR = Path(__file__).resolve().parents[2]

    BASE_DIR = PROJECT_DIR.parent

    # Databases

    @property
    def DATABASES(self):
        try:
            return {
                "default": config("DJANGO_DATABASE_URL", cast=dj_db_url.parse),
            }
        except UndefinedValueError:
            return {}

    DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

    # Apps

    INSTALLED_APPS = [
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
    ]

    # Middleware

    MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.locale.LocaleMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ]

    # URLs

    ROOT_URLCONF = "reactor.conf.urls"

    @classmethod
    def get_urlpatterns(cls):
        from django.urls import include, path

        return [
            path("i18n/", include("django.conf.urls.i18n")),
        ]

    # Templates

    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [
                PROJECT_DIR / "templates",
            ],
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                ],
            },
        },
    ]

    # Static files

    STATICFILES_DIRS = [
        PROJECT_DIR / "static",
    ]

    # Internationalization

    USE_I18N = True

    LANGUAGES = [
        ("en", _("English")),
        ("pl", _("Polish")),
    ]

    LANGUAGE_CODE = config("DJANGO_LANGUAGE_CODE", default="en")

    LOCALE_PATHS = [
        PROJECT_DIR / "locale",
    ]

    # Time zone

    USE_TZ = True

    TIME_ZONE = config("DJANGO_TIME_ZONE", default="UTC")
