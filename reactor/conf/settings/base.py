import inspect
import sys
from abc import ABC, abstractmethod


class Settings(ABC):
    @classmethod
    @abstractmethod
    def get_urlpatterns(cls):
        pass

    @staticmethod
    def is_setting(name):
        return name.isupper()

    @classmethod  # noqa: B027
    def pre_load(cls):
        pass

    @classmethod
    def load(cls, module_name):
        cls.pre_load()

        instance = cls()
        module = sys.modules[module_name]

        for name, value in inspect.getmembers(instance):
            if not cls.is_setting(name):
                continue

            if isinstance(value, property):
                value = value.fget(instance)  # noqa: PLW2901

            setattr(module, name, value)
