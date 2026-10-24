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
