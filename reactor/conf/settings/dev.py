"""Django settings for application development environments."""

import abc
from importlib import metadata

from reactor.conf import env

from . import common


class Extension(abc.ABC):
    """Optional mixin for development settings.

    Extensions group settings and behavior for optional integrations. Direct
    subclasses must implement `is_enabled` and be defined or imported before
    `Settings` is defined below. Enabled extensions precede the common
    settings base in reverse definition order, so later extensions take
    precedence. Attributes defined on development settings take precedence
    over extensions.

    Extensions can provide uppercase settings or override properties and methods.
    Overrides can use `super()` to build on the next extension or the settings
    class. Mutable settings should be copied before modification to avoid
    changing inherited values.
    """

    @classmethod
    @abc.abstractmethod
    def is_enabled(cls):
        """Return whether this extension should be applied."""


class DebugToolbarExtension(Extension):
    """Optional `django-debug-toolbar` integration for development settings."""

    @classmethod
    def is_enabled(cls):
        """Return whether `django-debug-toolbar` is installed and enabled.

        The extension is disabled if the package is not installed. Otherwise,
        `DEBUG_TOOLBAR_ENABLED` controls enablement and defaults to `True`.
        """
        try:
            metadata.distribution("django-debug-toolbar")
        except metadata.PackageNotFoundError:
            return False

        return env.bool("DEBUG_TOOLBAR_ENABLED", default=True)

    # Security

    INTERNAL_IPS = [
        "127.0.0.1",
    ]

    # Apps

    @property
    def INSTALLED_APPS(self):
        """Return inherited apps with `django-debug-toolbar` appended."""
        installed_apps = super().INSTALLED_APPS.copy()

        installed_apps += [
            "debug_toolbar",
        ]

        return installed_apps

    # Middleware

    @property
    def MIDDLEWARE(self):
        """Return inherited middleware with `django-debug-toolbar` appended."""
        middleware = super().MIDDLEWARE.copy()

        middleware += [
            "debug_toolbar.middleware.DebugToolbarMiddleware",
        ]

        return middleware

    # URLs

    @classmethod
    def get_urlpatterns(cls):
        """Return inherited routes with `django-debug-toolbar` routes appended."""
        urlpatterns = super().get_urlpatterns()

        from django.urls import include, path

        urlpatterns += [
            path("__debug__/", include("debug_toolbar.urls")),
        ]

        return urlpatterns


class BrowserReloadExtension(Extension):
    """Optional `django-browser-reload` integration for development settings."""

    @classmethod
    def is_enabled(cls):
        """Return whether `django-browser-reload` is installed and enabled.

        The extension is disabled if the package is not installed. Otherwise,
        `BROWSER_RELOAD_ENABLED` controls enablement and defaults to `True`.
        """
        try:
            metadata.distribution("django-browser-reload")
        except metadata.PackageNotFoundError:
            return False

        return env.bool("BROWSER_RELOAD_ENABLED", default=True)

    # Apps

    @property
    def INSTALLED_APPS(self):
        """Return inherited apps with `django-browser-reload` appended."""
        installed_apps = super().INSTALLED_APPS.copy()

        installed_apps += [
            "django_browser_reload",
        ]

        return installed_apps

    # Middleware

    @property
    def MIDDLEWARE(self):
        """Return inherited middleware with `django-browser-reload` appended."""
        middleware = super().MIDDLEWARE.copy()

        middleware += [
            "django_browser_reload.middleware.BrowserReloadMiddleware",
        ]

        return middleware

    # URLs

    @classmethod
    def get_urlpatterns(cls):
        """Return inherited routes with `django-browser-reload` routes appended."""
        urlpatterns = super().get_urlpatterns()

        from django.urls import include, path

        urlpatterns += [
            path("__reload__/", include("django_browser_reload.urls")),
        ]

        return urlpatterns


class WatchfilesExtension(Extension):
    """Optional `django-watchfiles` integration for development settings."""

    @classmethod
    def is_enabled(cls):
        """Return whether `django-watchfiles` is installed and enabled.

        The extension is disabled if the package is not installed. Otherwise,
        `WATCHFILES_ENABLED` controls enablement and defaults to `True`.
        """
        try:
            metadata.distribution("django-watchfiles")
        except metadata.PackageNotFoundError:
            return False

        return env.bool("WATCHFILES_ENABLED", default=True)

    # Apps

    @property
    def INSTALLED_APPS(self):
        """Return inherited apps with `django-watchfiles` appended."""
        installed_apps = super().INSTALLED_APPS.copy()

        installed_apps += [
            "django_watchfiles",
        ]

        return installed_apps


def get_enabled_extensions():
    """Return enabled extension classes in settings precedence order.

    Only direct subclasses of `Extension` already defined or imported are
    considered. The returned list contains classes whose `is_enabled` method
    returns a truthy value, with later-defined classes first so they take
    precedence when used as settings bases.
    """
    extensions = reversed(Extension.__subclasses__())

    return [extension for extension in extensions if extension.is_enabled()]


enabled_extensions = get_enabled_extensions()


class Settings(*enabled_extensions, common.Settings):
    """Settings for application development environments."""

    # Debugging

    DEBUG = env.bool("DEBUG", default=True)

    # Security

    SECRET_KEY = env.str("SECRET_KEY", default="secret-key")

    # URLs

    @classmethod
    def get_urlpatterns(cls):
        """Return shared routes with local media serving when debugging is enabled."""
        urlpatterns = super().get_urlpatterns()

        from django.conf import settings
        from django.conf.urls.static import static

        urlpatterns += [
            *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
        ]

        return urlpatterns

    # Storages

    def get_storage_config(self, storage_alias):
        """Return local file storage settings for the requested alias.

        The `staticfiles` alias uses Django's development static file storage.
        Other aliases store uploads in separate subdirectories of `MEDIA_ROOT`,
        with matching URL prefixes under `MEDIA_URL`. Environment storage
        configuration is not used.
        """
        if storage_alias == "staticfiles":
            return {
                "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
            }

        return {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
            "OPTIONS": {
                "location": self.MEDIA_ROOT / storage_alias,
                "base_url": self.MEDIA_URL + storage_alias + "/",
            },
        }

    STATIC_ROOT = common.Settings.BASE_DIR / "staticfiles"

    STATIC_URL = "/static/"

    MEDIA_ROOT = common.Settings.BASE_DIR / "media"

    MEDIA_URL = "/media/"


Settings.export()
