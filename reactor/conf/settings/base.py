import inspect
import sys
from abc import ABC, abstractmethod


class Settings(ABC):
    @classmethod
    def pre_load(cls):
        pass

    @classmethod
    def post_load(cls):
        pass

    @classmethod
    def load(cls, module_name):
        cls.pre_load()

        instance = cls()
        module = sys.modules[module_name]

        for name, value in inspect.getmembers(instance):
            if not (name.isupper() and not name.startswith("_")):
                continue

            setattr(
                module,
                name,
                value.fget(instance) if isinstance(value, property) else value,
            )

        cls.post_load()

    @classmethod
    @abstractmethod
    def get_urlpatterns(cls):
        pass
