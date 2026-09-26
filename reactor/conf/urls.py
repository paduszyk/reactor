from environ import Env

from .settings.base import get_settings_class

_env = Env()

_settings_module_name = _env.str("DJANGO_SETTINGS_MODULE")

_settings_class = get_settings_class(_settings_module_name)

urlpatterns = _settings_class.get_urlpatterns()
