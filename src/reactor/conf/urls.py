from . import get_configuration_class

__all__ = ["urlpatterns"]

Configuration = get_configuration_class()

urlpatterns = Configuration.get_urlpatterns()
