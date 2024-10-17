import inspect
import sys

import environ


class Settings:
    def __init_subclass__(cls):
        cls.load()

    @classmethod
    def pre_load(cls):
        cls.env = environ.Env()

    @classmethod
    def load(cls):
        cls.pre_load()

        settings = cls()
        module = sys.modules[cls.__module__]

        for name, value in inspect.getmembers(settings):
            if not (name.isupper() and not name.startswith("_")):
                continue

            if isinstance(value, property):
                value = value.fget(settings)  # noqa: PLW2901

            setattr(module, name, value)

    @classmethod
    def get_urlpatterns(cls):
        return []
