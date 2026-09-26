# ruff: noqa: SLF001

from reactor.conf.settings import dev


class TestSettings:
    def test_get_database_config_uses_alias_based_env_name(self, mocker):
        # Arrange.
        settings = dev.Settings()

        # Mock.
        mocker.patch.dict("os.environ", {"DEFAULT_DATABASE_URL": "default-url"})
        env_db_mock = mocker.patch.object(dev._env, "db")

        # Act.
        settings.get_database_config("default")

        # Assert.
        env_db_mock.assert_called_once_with("DEFAULT_DATABASE_URL")

    def test_get_database_config_returns_env_result(self, mocker):
        # Arrange.
        expected_database_config = object()

        settings = dev.Settings()

        # Mock.
        mocker.patch.dict("os.environ", {"DEFAULT_DATABASE_URL": "default-url"})
        mocker.patch.object(dev._env, "db", return_value=expected_database_config)

        # Act.
        database_config = settings.get_database_config("default")

        # Assert.
        assert database_config is expected_database_config

    def test_get_database_config_returns_empty_when_env_var_missing(self, monkeypatch):
        # Arrange.
        settings = dev.Settings()

        # Mock.
        monkeypatch.delenv("DEFAULT_DATABASE_URL", raising=False)

        # Act.
        database_config = settings.get_database_config("default")

        # Assert.
        assert database_config == {}
