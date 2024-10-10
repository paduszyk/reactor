import inspect
import sys

import environ


class Settings:
    def __init_subclass__(cls):
        super().__init_subclass__()

        cls._load()

    @classmethod
    def pre_load(cls):
        env = environ.Env()
        env.prefix = "DJANGO_"

        cls.env = env

    @classmethod
    def get_urlpatterns(cls):
        return []

    @classmethod
    def _load(cls):
        cls.pre_load()

        settings = cls()
        module = sys.modules[cls.__module__]

        for name, value in inspect.getmembers(settings):
            if name.isupper() and not name.startswith("_"):
                setattr(
                    module,
                    name,
                    value.fget(settings)
                    if value and isinstance(value, property)
                    else value,
                )
