from django.core.handlers.wsgi import WSGIHandler

from reactor.conf import wsgi


def test_application_is_wsgi_handler():
    # Act.
    application = wsgi.application

    # Assert.
    assert isinstance(application, WSGIHandler)
