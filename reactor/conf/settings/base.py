import inspect
import sys
from abc import ABC, abstractmethod


class Settings(ABC):
    load = False

    def __init_subclass__(cls):
        super().__init_subclass__()

        if cls.load:
            cls._load()

    @classmethod
    @abstractmethod
    def pre_load(cls): ...

    @classmethod
    def _load(cls):
        cls.pre_load()

        instance = cls()
        module = sys.modules[cls.__module__]

        for name, value in inspect.getmembers(instance):
            if not (name.isupper() and not name.startswith("_")):
                continue

            if isinstance(value, property):
                value = value.fget(instance)  # noqa: PLW2901

            setattr(module, name, value)

    @classmethod
    @abstractmethod
    def get_urlpatterns(cls): ...
