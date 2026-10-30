import pytest

from reactor.conf.settings import base


@pytest.fixture(autouse=True)
def settings_class_registry(mocker):
    """Provide the settings class registry with changes restored after each test."""
    return mocker.patch.dict(f"{base.__name__}._settings_class_registry")
