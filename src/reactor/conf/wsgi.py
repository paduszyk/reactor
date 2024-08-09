__all__ = [
    "application",
]

from configurations.wsgi import get_wsgi_application

application = get_wsgi_application()
