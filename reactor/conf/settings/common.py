"""Application settings shared across deployment environments."""

from pathlib import Path

from django.utils.translation import pgettext_lazy

from reactor.conf import env

from . import base


class Settings(base.Settings):
    """Settings shared by all application environments."""

    # Paths

    PACKAGE_DIR = Path(__file__).resolve().parents[2]

    BASE_DIR = PACKAGE_DIR.parent

    # Databases

    DATABASE_ALIASES = [
        "default",
    ]

    def get_database_config(self, database_alias):
        """Return the Django database configuration for an alias.

        The URL comes from `<ALIAS>_DATABASE_URL`, with the alias uppercased.
        An unset variable returns an empty dictionary, allowing commands that
        need no database access to run without database configuration.

        Raises:
            ValueError: The supplied URL produces an empty configuration or
                contains invalid connection values.
        """
        database_url_env_name = f"{database_alias.upper()}_DATABASE_URL"

        if database_url_env_name not in env:
            return {}

        database_config = env.db(database_url_env_name)

        if not database_config:
            msg = (
                f"database configuration for {database_alias!r} is empty; set "
                f"{database_url_env_name} to a valid database URL"
            )
            raise ValueError(msg)

        return database_config

    @property
    def DATABASES(self):
        """Return database configurations for `DATABASE_ALIASES`.

        `DATABASE_ALIASES` selects the entries in the returned mapping.
        Subclasses can customize each entry through `get_database_config`.
        """
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

    ROOT_URLCONF = "reactor.conf.urls"

    @classmethod
    def get_urlpatterns(cls):
        """Return the shared application URL patterns."""
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

    def get_storage_config(self, storage_alias):
        """Return the Django storage configuration for an alias.

        The configuration comes from `<ALIAS>_STORAGE_JSON`, with the alias
        uppercased. An unset variable returns an empty dictionary. A supplied
        value must be a non-empty JSON object containing Django storage settings,
        such as `BACKEND` and optional `OPTIONS`; backend options are not validated
        here.

        Raises:
            ValueError: The value is invalid JSON or is not a non-empty object.
        """
        storage_json_env_name = f"{storage_alias.upper()}_STORAGE_JSON"

        if storage_json_env_name not in env:
            return {}

        storage_config = env.json(storage_json_env_name)

        if not (isinstance(storage_config, dict) and storage_config):
            msg = (
                f"storage configuration for {storage_alias!r} is not a non-empty "
                f"JSON object, got type {type(storage_config).__name__!r}; set "
                f"{storage_json_env_name} to a non-empty JSON object"
            )
            raise ValueError(msg)

        return storage_config

    @property
    def STORAGES(self):
        """Return storage configurations for `STORAGE_ALIASES`.

        `STORAGE_ALIASES` selects the entries in the returned mapping.
        Subclasses can customize each entry through `get_storage_config`.
        """
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

    LANGUAGE_CODE = env.str("LANGUAGE_CODE", default="en")

    LOCALE_PATHS = [
        PACKAGE_DIR / "locale",
    ]

    # Time zone

    USE_TZ = True

    TIME_ZONE = env.str("TIME_ZONE", default="UTC")
