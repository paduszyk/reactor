from importlib import metadata

import pytest

lazy from reactor.conf.settings import dev


@pytest.fixture(autouse=True)
def configure_environment(mocker):
    """Configure the environment for development settings tests.

    Other environment variables are cleared for each test. The original process
    environment is restored afterward.
    """
    mocker.patch.dict(
        "os.environ",
        {
            "DEBUG": "true",
            "SECRET_KEY": "secret-key",
        },
        clear=True,
    )


@pytest.fixture
def extension_subclasses(mocker):
    """Wrap `Extension.__subclasses__` for each requesting test.

    The original method is restored afterward; created subclasses are not removed.
    """
    mocker.patch.object(
        dev.Extension,
        "__subclasses__",
        wraps=dev.Extension.__subclasses__,
    )


@pytest.fixture
def base_settings_class():
    """Provide a settings base with empty app, middleware, and URL lists.

    A new base class is created for each test.
    """

    class BaseSettings:
        INSTALLED_APPS = []
        MIDDLEWARE = []

        @classmethod
        def get_urlpatterns(cls):
            return []

    return BaseSettings


@pytest.fixture
def settings_factory(base_settings_class):
    """Provide a factory for settings instances composed from extensions.

    The factory accepts extension classes in settings precedence order.
    Created instances inherit app and middleware lists from the test settings base.
    """

    def _make_settings(*, extensions):
        settings_class = type(
            "Settings",
            (*extensions, base_settings_class),
            {},
        )

        return settings_class()

    return _make_settings


class TestDebugToolbarExtension:
    def test_is_enabled_defaults_true_when_installed(self, mocker, monkeypatch):
        # Arrange.
        monkeypatch.delenv("DEBUG_TOOLBAR_ENABLED", raising=False)

        original_distribution = metadata.distribution

        def distribution_side_effect(name):
            if name == "django-debug-toolbar":
                return object()

            return original_distribution(name)

        mocker.patch.object(
            dev.metadata,
            "distribution",
            side_effect=distribution_side_effect,
        )

        # Act.
        enabled = dev.DebugToolbarExtension.is_enabled()

        # Assert.
        assert enabled is True

    def test_is_enabled_returns_false_when_missing(self, mocker, monkeypatch):
        # Arrange.
        monkeypatch.delenv("DEBUG_TOOLBAR_ENABLED", raising=False)

        original_distribution = metadata.distribution

        def distribution_side_effect(name):
            if name == "django-debug-toolbar":
                raise dev.metadata.PackageNotFoundError(name)

            return original_distribution(name)

        mocker.patch.object(
            dev.metadata,
            "distribution",
            side_effect=distribution_side_effect,
        )

        # Act.
        enabled = dev.DebugToolbarExtension.is_enabled()

        # Assert.
        assert enabled is False

    def test_is_enabled_returns_true_when_env_true(self, mocker, monkeypatch):
        # Arrange.
        monkeypatch.setenv("DEBUG_TOOLBAR_ENABLED", "true")

        original_distribution = metadata.distribution

        def distribution_side_effect(name):
            if name == "django-debug-toolbar":
                return object()

            return original_distribution(name)

        mocker.patch.object(
            dev.metadata,
            "distribution",
            side_effect=distribution_side_effect,
        )

        # Act.
        enabled = dev.DebugToolbarExtension.is_enabled()

        # Assert.
        assert enabled is True

    def test_is_enabled_returns_false_when_env_false(self, mocker, monkeypatch):
        # Arrange.
        monkeypatch.setenv("DEBUG_TOOLBAR_ENABLED", "false")

        original_distribution = metadata.distribution

        def distribution_side_effect(name):
            if name == "django-debug-toolbar":
                return object()

            return original_distribution(name)

        mocker.patch.object(
            dev.metadata,
            "distribution",
            side_effect=distribution_side_effect,
        )

        # Act.
        enabled = dev.DebugToolbarExtension.is_enabled()

        # Assert.
        assert enabled is False

    def test_installed_apps_includes_extension(self, settings_factory):
        # Arrange.
        settings = settings_factory(extensions=(dev.DebugToolbarExtension,))

        # Act.
        installed_apps = settings.INSTALLED_APPS

        # Assert.
        assert "debug_toolbar" in installed_apps

    def test_middleware_includes_extension(self, settings_factory):
        # Arrange.
        settings = settings_factory(extensions=(dev.DebugToolbarExtension,))

        # Act.
        middleware = settings.MIDDLEWARE

        # Assert.
        assert "debug_toolbar.middleware.DebugToolbarMiddleware" in middleware

    def test_get_urlpatterns_adds_extension_route(self, mocker, settings_factory):
        # Arrange.
        settings = settings_factory(extensions=(dev.DebugToolbarExtension,))

        mocker.patch("django.urls.include", return_value=([], None, None))

        # Act.
        urlpatterns = settings.get_urlpatterns()
        routes = [str(urlpattern.pattern) for urlpattern in urlpatterns]

        # Assert.
        assert "__debug__/" in routes

    def test_get_urlpatterns_includes_extension_urls(self, mocker, settings_factory):
        # Arrange.
        settings = settings_factory(extensions=(dev.DebugToolbarExtension,))

        include_mock = mocker.patch(
            "django.urls.include",
            return_value=([], None, None),
        )

        # Act.
        settings.get_urlpatterns()

        # Assert.
        include_mock.assert_called_once_with("debug_toolbar.urls")


class TestBrowserReloadExtension:
    def test_is_enabled_defaults_true_when_installed(self, mocker, monkeypatch):
        # Arrange.
        monkeypatch.delenv("BROWSER_RELOAD_ENABLED", raising=False)

        original_distribution = metadata.distribution

        def distribution_side_effect(name):
            if name == "django-browser-reload":
                return object()

            return original_distribution(name)

        mocker.patch.object(
            dev.metadata,
            "distribution",
            side_effect=distribution_side_effect,
        )

        # Act.
        enabled = dev.BrowserReloadExtension.is_enabled()

        # Assert.
        assert enabled is True

    def test_is_enabled_returns_false_when_missing(self, mocker, monkeypatch):
        # Arrange.
        monkeypatch.delenv("BROWSER_RELOAD_ENABLED", raising=False)

        original_distribution = metadata.distribution

        def distribution_side_effect(name):
            if name == "django-browser-reload":
                raise dev.metadata.PackageNotFoundError(name)

            return original_distribution(name)

        mocker.patch.object(
            dev.metadata,
            "distribution",
            side_effect=distribution_side_effect,
        )

        # Act.
        enabled = dev.BrowserReloadExtension.is_enabled()

        # Assert.
        assert enabled is False

    def test_is_enabled_returns_true_when_env_true(self, mocker, monkeypatch):
        # Arrange.
        monkeypatch.setenv("BROWSER_RELOAD_ENABLED", "true")

        original_distribution = metadata.distribution

        def distribution_side_effect(name):
            if name == "django-browser-reload":
                return object()

            return original_distribution(name)

        mocker.patch.object(
            dev.metadata,
            "distribution",
            side_effect=distribution_side_effect,
        )

        # Act.
        enabled = dev.BrowserReloadExtension.is_enabled()

        # Assert.
        assert enabled is True

    def test_is_enabled_returns_false_when_env_false(self, mocker, monkeypatch):
        # Arrange.
        monkeypatch.setenv("BROWSER_RELOAD_ENABLED", "false")

        original_distribution = metadata.distribution

        def distribution_side_effect(name):
            if name == "django-browser-reload":
                return object()

            return original_distribution(name)

        mocker.patch.object(
            dev.metadata,
            "distribution",
            side_effect=distribution_side_effect,
        )

        # Act.
        enabled = dev.BrowserReloadExtension.is_enabled()

        # Assert.
        assert enabled is False

    def test_installed_apps_includes_extension(self, settings_factory):
        # Arrange.
        settings = settings_factory(
            extensions=(dev.BrowserReloadExtension,),
        )

        # Act.
        installed_apps = settings.INSTALLED_APPS

        # Assert.
        assert "django_browser_reload" in installed_apps

    def test_middleware_includes_extension(self, settings_factory):
        # Arrange.
        settings = settings_factory(
            extensions=(dev.BrowserReloadExtension,),
        )

        # Act.
        middleware = settings.MIDDLEWARE

        # Assert.
        assert "django_browser_reload.middleware.BrowserReloadMiddleware" in middleware

    def test_get_urlpatterns_adds_extension_route(self, mocker, settings_factory):
        # Arrange.
        settings = settings_factory(extensions=(dev.BrowserReloadExtension,))

        mocker.patch("django.urls.include", return_value=([], None, None))

        # Act.
        urlpatterns = settings.get_urlpatterns()
        routes = [str(urlpattern.pattern) for urlpattern in urlpatterns]

        # Assert.
        assert "__reload__/" in routes

    def test_get_urlpatterns_includes_extension_urls(self, mocker, settings_factory):
        # Arrange.
        settings = settings_factory(extensions=(dev.BrowserReloadExtension,))

        include_mock = mocker.patch(
            "django.urls.include",
            return_value=([], None, None),
        )

        # Act.
        settings.get_urlpatterns()

        # Assert.
        include_mock.assert_called_once_with("django_browser_reload.urls")


class TestWatchfilesExtension:
    def test_is_enabled_defaults_true_when_installed(self, mocker, monkeypatch):
        # Arrange.
        monkeypatch.delenv("WATCHFILES_ENABLED", raising=False)

        original_distribution = metadata.distribution

        def distribution_side_effect(name):
            if name == "django-watchfiles":
                return object()

            return original_distribution(name)

        mocker.patch.object(
            dev.metadata,
            "distribution",
            side_effect=distribution_side_effect,
        )

        # Act.
        enabled = dev.WatchfilesExtension.is_enabled()

        # Assert.
        assert enabled is True

    def test_is_enabled_returns_false_when_missing(self, mocker, monkeypatch):
        # Arrange.
        monkeypatch.delenv("WATCHFILES_ENABLED", raising=False)

        original_distribution = metadata.distribution

        def distribution_side_effect(name):
            if name == "django-watchfiles":
                raise dev.metadata.PackageNotFoundError(name)

            return original_distribution(name)

        mocker.patch.object(
            dev.metadata,
            "distribution",
            side_effect=distribution_side_effect,
        )

        # Act.
        enabled = dev.WatchfilesExtension.is_enabled()

        # Assert.
        assert enabled is False

    def test_is_enabled_returns_true_when_env_true(self, mocker, monkeypatch):
        # Arrange.
        monkeypatch.setenv("WATCHFILES_ENABLED", "true")

        original_distribution = metadata.distribution

        def distribution_side_effect(name):
            if name == "django-watchfiles":
                return object()

            return original_distribution(name)

        mocker.patch.object(
            dev.metadata,
            "distribution",
            side_effect=distribution_side_effect,
        )

        # Act.
        enabled = dev.WatchfilesExtension.is_enabled()

        # Assert.
        assert enabled is True

    def test_is_enabled_returns_false_when_env_false(self, mocker, monkeypatch):
        # Arrange.
        monkeypatch.setenv("WATCHFILES_ENABLED", "false")

        original_distribution = metadata.distribution

        def distribution_side_effect(name):
            if name == "django-watchfiles":
                return object()

            return original_distribution(name)

        mocker.patch.object(
            dev.metadata,
            "distribution",
            side_effect=distribution_side_effect,
        )

        # Act.
        enabled = dev.WatchfilesExtension.is_enabled()

        # Assert.
        assert enabled is False

    def test_installed_apps_includes_extension(self, settings_factory):
        # Arrange.
        settings = settings_factory(extensions=(dev.WatchfilesExtension,))

        # Act.
        installed_apps = settings.INSTALLED_APPS

        # Assert.
        assert "django_watchfiles" in installed_apps


@pytest.mark.usefixtures("extension_subclasses")
class TestGetEnabledExtensions:
    def test_get_enabled_extensions_includes_enabled(self):
        # Arrange.
        class EnabledExtension(dev.Extension):
            @classmethod
            def is_enabled(cls):
                return True

        # Act.
        enabled_extensions = dev.get_enabled_extensions()

        # Assert.
        assert EnabledExtension in enabled_extensions

    def test_get_enabled_extensions_excludes_disabled(self):
        # Arrange.
        class DisabledExtension(dev.Extension):
            @classmethod
            def is_enabled(cls):
                return False

        # Act.
        enabled_extensions = dev.get_enabled_extensions()

        # Assert.
        assert DisabledExtension not in enabled_extensions

    def test_get_enabled_extensions_prioritizes_later_defined(self):
        # Arrange.
        class EarlierExtension(dev.Extension):
            @classmethod
            def is_enabled(cls):
                return True

        class LaterExtension(dev.Extension):
            @classmethod
            def is_enabled(cls):
                return True

        # Act.
        enabled_extensions = dev.get_enabled_extensions()

        earlier_index = enabled_extensions.index(EarlierExtension)
        later_index = enabled_extensions.index(LaterExtension)

        # Assert.
        assert later_index < earlier_index


class TestSettings:
    def test_get_storage_config_uses_staticfiles_storage(self):
        # Arrange.
        settings = dev.Settings()

        # Act.
        storage_config = settings.get_storage_config("staticfiles")
        backend_path = storage_config["BACKEND"]

        # Assert.
        assert backend_path.startswith("django.contrib.staticfiles.storage.")

    def test_get_storage_config_uses_core_storage_for_media(self):
        # Arrange.
        settings = dev.Settings()

        # Act.
        storage_config = settings.get_storage_config("default")
        backend_path = storage_config["BACKEND"]

        # Assert.
        assert backend_path.startswith("django.core.files.storage.")

    def test_get_storage_config_uses_alias_for_media_location(self):
        # Arrange.
        settings = dev.Settings()

        # Act.
        storage_config = settings.get_storage_config("default")
        options = storage_config["OPTIONS"]

        # Assert.
        assert options["location"].name == "default"

    def test_get_storage_config_uses_alias_for_media_base_url(self):
        # Arrange.
        settings = dev.Settings()

        # Act.
        storage_config = settings.get_storage_config("default")
        options = storage_config["OPTIONS"]

        # Assert.
        assert options["base_url"].endswith("default/")
