__all__ = [
    "CI",
    "Dev",
]

from pathlib import Path

from configurations import Configuration, values

from django.urls import include, path
from django.utils.translation import gettext_lazy as _

# Django settings
# https://docs.djangoproject.com/en/dev/ref/settings/

# Django configurations
# https://django-configurations.readthedocs.io/


class Common(Configuration):
    """Encapsulates settings common to all environments."""

    # Paths

    PROJECT_DIR = Path(__file__).resolve().parents[1]

    BASE_DIR = PROJECT_DIR.parent

    # Databases

    DATABASES = values.DatabaseURLValue()

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

    # Template engines

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

    LANGUAGE_CODE = "en"

    LOCALE_PATHS = [
        PROJECT_DIR / "locale",
    ]

    # Time zones

    USE_TZ = True

    TIME_ZONE = "Europe/Warsaw"

    # Static files

    STATICFILES_DIRS = [
        PROJECT_DIR / "static",
    ]

    STATIC_URL = "static/"

    STATIC_ROOT = BASE_DIR / "staticfiles"

    # Fixtures

    FIXTURE_DIRS = [
        PROJECT_DIR / "fixtures",
    ]

    @classmethod
    def get_urlpatterns(cls):
        from django.contrib import admin

        return [
            path("admin/", admin.site.urls),
            path("i18n/", include("django.conf.urls.i18n")),
        ]


class Debug(Common):
    """Encapsulates settings specific to debugging environments."""

    # Debugging mode

    DEBUG = True

    # Security

    SECRET_KEY = values.Value("django-insecure-secret-key", environ=False)

    ALLOWED_HOSTS = ["*"]

    # Media

    MEDIA_URL = "media/"

    MEDIA_ROOT = Common.BASE_DIR / "media"

    @classmethod
    def get_urlpatterns(cls):
        from django.conf.urls.static import static

        return super().get_urlpatterns() + static(
            cls.MEDIA_URL,
            document_root=cls.MEDIA_ROOT,
        )


class Dev(Debug):
    """Encapsulates settings specific to local development environments."""

    # Security

    INTERNAL_IPS = [
        "127.0.0.1",
    ]

    # Apps

    INSTALLED_APPS = Debug.INSTALLED_APPS + [
        "debug_toolbar",
        "django_extensions",
        "schema_graph",
        "xlsx_serializer",
    ]

    # Middleware

    MIDDLEWARE = Debug.MIDDLEWARE + [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ]

    # Extensions

    SHELL_PLUS = "ipython"

    @classmethod
    def get_urlpatterns(cls):
        import debug_toolbar
        from schema_graph.views import Schema

        return super().get_urlpatterns() + [
            path("debug/", include(debug_toolbar.urls)),
            path("schema/", Schema.as_view()),
        ]


class CI(Debug):
    """Encapsulates settings specific to CI environments."""
