from reactor.conf.settings import get_settings

Settings = get_settings()

urlpatterns = Settings.get_urlpatterns()
