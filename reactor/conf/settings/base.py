import inspect
import sys


class Settings:
    @classmethod
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
    def get_urlpatterns(cls):
        return []
