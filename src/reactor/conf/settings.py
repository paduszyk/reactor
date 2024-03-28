import os
from functools import reduce
from operator import add
from pathlib import Path

from configurations import Configuration, values

from django.urls import include, path
from django.utils.translation import gettext_lazy as _

__all__ = ["CI", "Local"]


class Common(Configuration):
    """Represents settings common to all environments."""

    # Paths

    PROJECT_DIR = Path(__file__).resolve().parents[1]

    BASE_DIR = PROJECT_DIR.parents[1]

    # Databases

    DATABASES = values.DatabaseURLValue()

    DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

    # Apps

    DJANGO_APPS = [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
    ]

    THIRD_PARTY_APPS = []

    FIRST_PARTY_APPS = [
        "reactor.apps",
        "reactor.db",
        "reactor.core",
    ]

    LOCAL_APPS = [
        "bibliometrics",
        "contracts",
        "personal_data",
        "publishing_media",
        "research_works",
        "science_evaluation",
        "units_network",
        "work_contributions",
    ]

    # URLs

    ROOT_URLCONF = "reactor.conf.urls"

    # Middleware

    MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ]

    # Templates

    TEMPLATE_DIRS = [
        PROJECT_DIR / "templates",
    ]

    CONTEXT_PROCESSORS = [
        "django.template.context_processors.debug",
        "django.template.context_processors.request",
        "django.contrib.auth.context_processors.auth",
        "django.contrib.messages.context_processors.messages",
    ]

    TEMPLATE_TAG_LIBRARIES = {}

    # Internationalization

    USE_I18N = True

    LANGUAGE_CODE = "en"

    LANGUAGES = [
        ("en", _("English")),
        ("pl", _("Polish")),
    ]

    LOCALE_PATHS = [
        PROJECT_DIR / "locale",
    ]

    # Timezone

    USE_TZ = True

    TIME_ZONE = "Europe/Warsaw"

    # Fixtures

    FIXTURE_DIRS = [
        PROJECT_DIR / "fixtures",
    ]

    # Static files

    STATICFILES_DIRS = [
        PROJECT_DIR / "static",
    ]

    STATIC_URL = "static/"

    STATIC_ROOT = BASE_DIR / "staticfiles"

    # Media

    MEDIA_URL = "media/"

    MEDIA_ROOT = BASE_DIR / "media"

    @property
    def PROJECT_APPS(self):
        return self.FIRST_PARTY_APPS + self.LOCAL_APPS

    @property
    def INSTALLED_APPS(self):
        return self.DJANGO_APPS + self.THIRD_PARTY_APPS + self.PROJECT_APPS

    @property
    def TEMPLATES(self):
        return [
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "DIRS": self.TEMPLATE_DIRS,
                "APP_DIRS": True,
                "OPTIONS": {
                    "context_processors": self.CONTEXT_PROCESSORS,
                    "libraries": self.TEMPLATE_TAG_LIBRARIES,
                },
            },
        ]

    @classmethod
    def get_urlpatterns(cls):
        from django.conf import settings
        from django.conf.urls.static import static
        from django.contrib import admin

        # Internationalization

        i18n_urls = [
            path("i18n/", include("django.conf.urls.i18n")),
        ]

        # Static files & media

        static_urls = static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

        media_urls = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

        # Apps

        django_apps_urls = [
            path("admin/", admin.site.urls),
        ]

        third_party_apps_urls = []

        first_party_apps_urls = []

        local_apps_urls = []

        # All URLs combined and exposed for the export

        return reduce(
            add,
            [
                i18n_urls,
                static_urls,
                media_urls,
                django_apps_urls,
                third_party_apps_urls,
                first_party_apps_urls,
                local_apps_urls,
            ],
        )


class Debug(Common):
    """Represents settings common to all environments using the debugging mode."""

    # Debugging mode

    DEBUG = True

    # Security

    SECRET_KEY = "django-insecure-secret-key"

    ALLOWED_HOSTS = ["*"]

    @classmethod
    def pre_setup(cls):
        super().pre_setup()

        DATABASE_ENGINE = os.environ["DJANGO_DATABASE_ENGINE"].upper()

        cls.DATABASES = values.DatabaseURLValue(
            environ_name=f"DJANGO_DATABASE_{DATABASE_ENGINE}"
        )


class Local(Debug):
    """Represents settings specific to local development environments."""

    # Environment variables

    DOTENV = Debug.BASE_DIR / ".env"

    @property
    def THIRD_PARTY_APPS(self):
        return super().THIRD_PARTY_APPS + [
            "schema_graph",
        ]

    @classmethod
    def get_urlpatterns(cls):
        from schema_graph.views import Schema

        return super().get_urlpatterns() + [
            path("schema/", Schema.as_view()),
        ]


class CI(Debug):
    """Represents settings specific to continuous integration environments."""
