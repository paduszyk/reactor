import importlib

import pytest

from reactor.conf.settings import base


@pytest.fixture
def urls_module(mocker):
    """Provide the root URL module and restore its configuration after the test."""
    from reactor.conf import urls

    yield urls

    mocker.stopall()
    importlib.reload(urls)


def test_urlpatterns_use_settings_class(mocker, urls_module):
    # Arrange.
    expected_urlpatterns = object()

    class Settings:
        @classmethod
        def get_urlpatterns(cls):
            return expected_urlpatterns

    mocker.patch.object(base, "get_settings_class", return_value=Settings)

    # Act.
    importlib.reload(urls_module)
    urlpatterns = urls_module.urlpatterns

    # Assert.
    assert urlpatterns is expected_urlpatterns
