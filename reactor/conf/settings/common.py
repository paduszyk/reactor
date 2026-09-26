import abc
from pathlib import Path

from environ import Env

from django.utils.translation import pgettext_lazy

from . import base

_env = Env()


class Settings(base.Settings):
    """Settings shared by all application environments.

    Subclasses provide database and storage configurations for the aliases in
    `DATABASE_ALIASES` and `STORAGE_ALIASES`. These configurations are assembled
    into the corresponding Django settings when their properties are evaluated.
    """

    # Paths

    PACKAGE_DIR = Path(__file__).resolve().parents[2]

    BASE_DIR = PACKAGE_DIR.parent

    # Databases

    DATABASE_ALIASES = [
        "default",
    ]

    @abc.abstractmethod
    def get_database_config(self, database_alias):
        """Return the Django database configuration for an alias.

        Args:
            database_alias: An entry from `DATABASE_ALIASES`.

        Returns:
            A configuration dictionary for the alias in `DATABASES`.
        """

    @property
    def DATABASES(self):
        """Return database configurations for the configured aliases."""
        database_aliases = self.DATABASE_ALIASES

        return dict(
            zip(
                database_aliases,
                map(
                    self.get_database_config,
                    database_aliases,
                ),
                strict=True,
            ),
        )

    DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

    # Apps

    INSTALLED_APPS = [
        "django.contrib.admin",
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

    @classmethod
    def get_urlpatterns(cls):
        """Return the URL patterns shared by all application environments."""
        from django.contrib import admin
        from django.urls import include, path

        return [
            path("admin/", admin.site.urls),
            path("i18n/", include("django.conf.urls.i18n")),
        ]

    # Templates

    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [
                PACKAGE_DIR / "templates",
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
        PACKAGE_DIR / "static",
    ]

    # Storages

    STORAGE_ALIASES = [
        "default",
        "staticfiles",
    ]

    @abc.abstractmethod
    def get_storage_config(self, storage_alias):
        """Return the Django storage configuration for an alias.

        Args:
            storage_alias: An entry from `STORAGE_ALIASES`.

        Returns:
            A configuration dictionary for the alias in `STORAGES`, containing
            the backend import path and any backend-specific options.
        """

    @property
    def STORAGES(self):
        """Return storage configurations for the configured aliases."""
        storage_aliases = self.STORAGE_ALIASES

        return dict(
            zip(
                storage_aliases,
                map(
                    self.get_storage_config,
                    storage_aliases,
                ),
                strict=True,
            ),
        )

    # Internationalization

    USE_I18N = True

    LANGUAGES = [
        ("en", pgettext_lazy("language", "English")),
        ("pl", pgettext_lazy("language", "Polish")),
    ]

    LANGUAGE_CODE = _env.str("LANGUAGE_CODE", default="en")

    LOCALE_PATHS = [
        PACKAGE_DIR / "locale",
    ]

    # Time zone

    USE_TZ = True

    TIME_ZONE = _env.str("TIME_ZONE", default="UTC")
