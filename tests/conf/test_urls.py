import importlib

import pytest

from reactor.conf.settings import base


@pytest.fixture
def urls(mocker):
    from reactor.conf import urls

    yield urls

    mocker.stopall()
    importlib.reload(urls)


def test_urlpatterns_come_from_settings_class(mocker, urls):
    # Arrange.
    expected_urlpatterns = object()

    class Settings:
        @classmethod
        def get_urlpatterns(cls):
            return expected_urlpatterns

    # Mock.
    mocker.patch.object(base, "get_settings_class", return_value=Settings)

    # Act.
    importlib.reload(urls)
    urlpatterns = urls.urlpatterns

    # Assert.
    assert urlpatterns is expected_urlpatterns
