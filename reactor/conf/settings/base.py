import inspect
import sys
from abc import ABC, abstractmethod


class Settings(ABC):
    @classmethod  # noqa: B027
    def pre_load(cls):
        pass

    @classmethod
    def load(cls, module_name):
        cls.pre_load()

        instance = cls()
        module = sys.modules[module_name]

        for name, value in inspect.getmembers(instance):
            if name.startswith("_") or not name.isupper():
                continue

            setattr(
                module,
                name,
                value.fget(instance) if isinstance(value, property) else value,
            )

    @classmethod
    @abstractmethod
    def get_urlpatterns(cls):
        pass
