"""Django settings for application development environments."""

import abc

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
