import json

import pytest

lazy from reactor.conf.settings import common


@pytest.fixture(autouse=True)
def configure_environment(mocker):
    """Configure the environment for common settings tests.

    Other environment variables are cleared for each test. The original process
    environment is restored afterward.
    """
    mocker.patch.dict(
        "os.environ",
        {
            "DEFAULT_DATABASE_URL": (
                "postgresql://postgres:postgres@localhost:5432/postgres"
            ),
            "DEFAULT_STORAGE_JSON": json.dumps(
                {
                    "BACKEND": "django.core.files.storage.InMemoryStorage",
                    "OPTIONS": {
                        "base_url": "/media/default/",
                    },
                },
            ),
        },
        clear=True,
    )


class TestSettings:
    def test_get_database_config_uses_alias_based_env_name(self, mocker):
        # Arrange.
        settings = common.Settings()

        env_db_spy = mocker.spy(common.env, "db")

        # Act.
        settings.get_database_config("default")

        # Assert.
        env_db_spy.assert_called_once_with("DEFAULT_DATABASE_URL")

    def test_get_database_config_returns_empty_config_if_env_missing(self, monkeypatch):
        # Arrange.
        settings = common.Settings()

        monkeypatch.delenv("DEFAULT_DATABASE_URL")

        # Act.
        database_config = settings.get_database_config("default")

        # Assert.
        assert database_config == {}

    def test_get_database_config_rejects_empty_config(self, mocker):
        # Arrange.
        settings = common.Settings()

        mocker.patch.object(common.env, "db", return_value={})

        # Act & assert.
        with (
            pytest.raises(
                ValueError,
                match=(
                    "database configuration for 'default' is empty; "
                    "set DEFAULT_DATABASE_URL to a valid database URL"
                ),
            ),
        ):
            settings.get_database_config("default")

    def test_databases_maps_aliases_to_configs(self, mocker):
        # Arrange.
        expected_databases = {
            "default": object(),
            "replica": object(),
        }

        class Settings(common.Settings):
            DATABASE_ALIASES = [
                "default",
                "replica",
            ]

        settings = Settings()

        mocker.patch.object(
            settings,
            "get_database_config",
            side_effect=expected_databases.__getitem__,
        )

        # Act.
        databases = settings.DATABASES

        # Assert.
        assert databases == expected_databases

    def test_get_storage_config_uses_alias_based_env_name(self, mocker):
        # Arrange.
        settings = common.Settings()

        env_json_spy = mocker.spy(common.env, "json")

        # Act.
        settings.get_storage_config("default")

        # Assert.
        env_json_spy.assert_called_once_with("DEFAULT_STORAGE_JSON")

    def test_get_storage_config_returns_empty_config_if_env_missing(self, monkeypatch):
        # Arrange.
        settings = common.Settings()

        monkeypatch.delenv("DEFAULT_STORAGE_JSON")

        # Act.
        storage_config = settings.get_storage_config("default")

        # Assert.
        assert storage_config == {}

    def test_get_storage_config_rejects_non_object_json(self, monkeypatch):
        # Arrange.
        settings = common.Settings()

        monkeypatch.setenv("DEFAULT_STORAGE_JSON", json.dumps([]))

        # Act & assert.
        with pytest.raises(
            ValueError,
            match=(
                "storage configuration for 'default' is not a non-empty JSON object, "
                "got type 'list'; set DEFAULT_STORAGE_JSON to a non-empty JSON object"
            ),
        ):
            settings.get_storage_config("default")

    def test_storages_maps_aliases_to_configs(self, mocker):
        # Arrange.
        expected_storages = {
            "default": object(),
            "staticfiles": object(),
        }

        class Settings(common.Settings):
            STORAGE_ALIASES = [
                "default",
                "staticfiles",
            ]

        settings = Settings()

        mocker.patch.object(
            settings,
            "get_storage_config",
            side_effect=expected_storages.__getitem__,
        )

        # Act.
        storages = settings.STORAGES

        # Assert.
        assert storages == expected_storages
