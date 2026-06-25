from reactor.apps.settings import AppSettings
from reactor.apps.urls import AppURLs


class CoreSettings(AppSettings):
    pass


settings = CoreSettings()


class CoreURLs(AppURLs):
    urlpatterns = []


urls = CoreURLs()
