import json

import pytest

lazy from reactor.conf.settings import prod


@pytest.fixture(autouse=True)
def configure_environment(mocker):
    """Configure the environment for production settings tests.

    Other environment variables are cleared for each test. The original process
    environment is restored afterward.
    """
    mocker.patch.dict(
        "os.environ",
        {
            "SECRET_KEY": "secret-key",
            "ALLOWED_HOSTS": "*",
            "CSRF_TRUSTED_ORIGINS": "https://*",
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
    def test_get_database_config_rejects_missing_env(self, monkeypatch):
        # Arrange.
        settings = prod.Settings()

        monkeypatch.delenv("DEFAULT_DATABASE_URL")

        # Act & assert.
        with pytest.raises(
            ValueError,
            match=(
                "required production database configuration for 'default' is missing; "
                "set DEFAULT_DATABASE_URL to a valid database URL"
            ),
        ):
            settings.get_database_config("default")

    def test_middleware_places_whitenoise_after_security(self):
        # Arrange.
        settings = prod.Settings()

        # Act.
        middleware = settings.MIDDLEWARE

        security_middleware_index = middleware.index(
            "django.middleware.security.SecurityMiddleware",
        )
        whitenoise_middleware_index = middleware.index(
            "whitenoise.middleware.WhiteNoiseMiddleware",
        )

        # Assert.
        assert whitenoise_middleware_index == security_middleware_index + 1

    def test_get_storage_config_uses_whitenoise_for_staticfiles(self):
        # Arrange.
        settings = prod.Settings()

        # Act.
        storage_config = settings.get_storage_config("staticfiles")
        backend_path = storage_config["BACKEND"]

        # Assert.
        assert backend_path.startswith("whitenoise.storage.")

    def test_get_storage_config_rejects_missing_env(self, monkeypatch):
        # Arrange.
        settings = prod.Settings()

        monkeypatch.delenv("DEFAULT_STORAGE_JSON")

        # Act & assert.
        with pytest.raises(
            ValueError,
            match=(
                "required production storage configuration for 'default' is missing; "
                "set DEFAULT_STORAGE_JSON to a non-empty JSON object"
            ),
        ):
            settings.get_storage_config("default")
