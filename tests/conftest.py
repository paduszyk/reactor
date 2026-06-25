from importlib import import_module

import pytest

from django.core.checks.registry import registry as django_check_registry
from django.test.utils import override_settings


@pytest.fixture
def django_settings():
    from django.conf import settings

    with override_settings():
        yield settings


@pytest.fixture
def django_urlpatterns(django_settings):
    urlconf_module = import_module(django_settings.ROOT_URLCONF)
    urlpatterns = urlconf_module.urlpatterns.copy()

    yield urlconf_module.urlpatterns

    urlconf_module.urlpatterns = urlpatterns


@pytest.fixture
def django_checks():
    registered_checks = django_check_registry.registered_checks.copy()

    yield django_check_registry

    django_check_registry.registered_checks = registered_checks
