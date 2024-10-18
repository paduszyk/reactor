from pathlib import Path

from django.urls import include, path
from django.utils.translation import gettext_lazy as _

from . import base


class Settings(base.Settings):
    """Encapsulates settings common to all environments."""

    # Paths

    PROJECT_DIR = Path(__file__).resolve().parents[1]

    BASE_DIR = PROJECT_DIR.parent

    # Databases

    @property
    def DATABASES(self):
        return (
            {"default": self.env.db_url_config(DATABASE_URL)}
            if (DATABASE_URL := self.env.get_value("DATABASE_URL", default=None))
            else {}
        )

    DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

    # Apps

    INSTALLED_APPS = [
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        #
        # Project-level apps
        "reactor.admin",
        "reactor.apps",
        "reactor.db",
        #
        # Database schema apps
        "reactor.schema.bibliometrics",
        "reactor.schema.human_resources",
        "reactor.schema.publishers",
        "reactor.schema.research_output",
        "reactor.schema.science_classification",
        "reactor.schema.units_network",
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

    ROOT_URLCONF = "reactor.urls"

    @classmethod
    def get_urlpatterns(cls):
        from django.contrib import admin

        return [
            *super().get_urlpatterns(),
            path("admin/", admin.site.urls),
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

    # Internationalization

    USE_I18N = True

    LANGUAGES = [
        ("en", _("English")),
        ("pl", _("Polish")),
    ]

    LOCALE_PATHS = [
        PROJECT_DIR / "locale",
    ]

    # Time zone

    USE_TZ = True

    TIME_ZONE = "Europe/Warsaw"

    # Static files

    STATICFILES_DIRS = [
        PROJECT_DIR / "static",
    ]

    # Fixtures

    FIXTURE_DIRS = [
        PROJECT_DIR / "fixtures",
    ]
