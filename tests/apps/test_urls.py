import pytest

from django.core.exceptions import ImproperlyConfigured

from reactor.apps.urls import AppURLs as BaseFirstPartyAppURLs


def test_app_urls_subclass_accepts_urlpatterns():
    # Arrange.
    class AppURLs(BaseFirstPartyAppURLs):
        urlpatterns = []

    # Act.
    urlpatterns = AppURLs.urlpatterns

    # Assert.
    assert urlpatterns == []


def test_app_urls_subclass_accepts_inherited_urlpatterns():
    # Arrange.
    class ParentAppURLs(BaseFirstPartyAppURLs):
        urlpatterns = []

    # Act.
    class ChildAppURLs(ParentAppURLs):
        pass

    # Assert.
    assert ChildAppURLs.urlpatterns is ParentAppURLs.urlpatterns


def test_app_urls_subclass_rejects_missing_urlpatterns():
    # Act & assert.
    with pytest.raises(ImproperlyConfigured):

        class AppURLs(BaseFirstPartyAppURLs):
            pass
