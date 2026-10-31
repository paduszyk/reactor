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
