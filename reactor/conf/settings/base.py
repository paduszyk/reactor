import inspect
import os
import sys
from collections import UserList
from functools import wraps


def _is_setting_name(name):
    return not name.startswith("_") and name.isupper()


class BaseSettings:
    @classmethod
    def pre_load(cls):
        pass

    @classmethod
    def post_load(cls):
        pass

    @classmethod
    def load(cls, module_name):
        cls.pre_load()

        module = sys.modules[module_name]
        instance = cls()

        for name, value in inspect.getmembers(instance):
            if not _is_setting_name(name):
                continue

            setattr(
                module,
                name,
                value.fget(instance) if isinstance(value, property) else value,
            )

        cls.post_load()

    @classmethod
    def get_urlpatterns(cls):
        return []


class PluginRegistry(UserList):
    class Plugin:
        disabled_in_tests = False

        @classmethod
        def is_active(cls):
            return False

    def register(self, plugin):
        if not isinstance(plugin, type) or not issubclass(plugin, self.Plugin):
            msg = (
                f"could not register {plugin!r} as a plugin; plugins must be "
                f"{self.Plugin!r} subclasses"
            )

            raise TypeError(msg)

        if plugin.disabled_in_tests:
            is_active = plugin.is_active

            @wraps(is_active)
            def wrapper(cls, *args, **kwargs):  # noqa: ARG001
                if ("test" in sys.argv) or ("PYTEST_VERSION" in os.environ):
                    return False

                return is_active(*args, **kwargs)

            plugin.is_active = classmethod(wrapper)

        self.append(plugin)

        return plugin

    def get_active_plugins(self):
        yield from (plugin for plugin in self if plugin.is_active())


plugins = PluginRegistry()
