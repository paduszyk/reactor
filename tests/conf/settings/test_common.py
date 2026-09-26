from reactor.conf.settings import common


class TestSettings:
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

            def get_database_config(self):
                return {}

            def get_storage_config(self):
                return {}

        settings = Settings()

        # Mock.
        mocker.patch.object(
            Settings,
            "get_database_config",
            side_effect=expected_databases.__getitem__,
        )

        # Act.
        databases = settings.DATABASES

        # Assert.
        assert databases == expected_databases

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

            def get_database_config(self):
                return {}

            def get_storage_config(self):
                return {}

        settings = Settings()

        # Mock.
        mocker.patch.object(
            Settings,
            "get_storage_config",
            side_effect=expected_storages.__getitem__,
        )

        # Act.
        storages = settings.STORAGES

        # Assert.
        assert storages == expected_storages
