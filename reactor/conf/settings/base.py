import abc
import sys

_settings_class_registry = {}


class Settings(abc.ABC):
    """Base configuration for class-based Django settings.

    Each subclass is registered under its defining module's name when created.
    A module may define one settings subclass; subclasses imported from other
    modules are allowed. Redefining the same class name supports module reloads.

    Concrete subclasses must support construction without arguments and provide
    URL patterns. Calling `export()` publishes their public uppercase attributes,
    including inherited attributes and evaluated properties, as module settings.
    """

    ROOT_URLCONF = "reactor.conf.urls"

    def __init_subclass__(cls, **kwargs):
        """Register a settings subclass in its defining module.

        Args:
            **kwargs: Class-creation options forwarded to the superclass hook.

        Raises:
            TypeError: The module already contains a locally defined `Settings`
                subclass bound to a different name.
        """
        super().__init_subclass__(**kwargs)

        cls._exported = False

        class_name = cls.__name__
        module_name = cls.__module__

        module = sys.modules[module_name]

        for attr_name, attr in module.__dict__.items():
            if not (
                isinstance(attr, type)
                and issubclass(attr, Settings)
                and attr.__module__ == module_name
            ):
                continue

            if attr_name == class_name:
                continue

            msg = (
                f"module {module_name!r} must define only one "
                f"{f'{Settings.__module__}.{Settings.__qualname__}'!r} subclass, "
                f"got {attr_name!r} and {class_name!r}; move each subclass "
                f"into a separate module"
            )
            raise TypeError(msg)

        _settings_class_registry[module_name] = cls

    @classmethod
    def export(cls):
        """Publish evaluated settings to the subclass's defining module once.

        The subclass is instantiated without arguments. Attributes whose names
        are uppercase and do not start with an underscore are evaluated before
        any module attributes are assigned. Existing module values with matching
        names are replaced; unrelated module attributes are preserved.

        Properties are evaluated before their values are exported. After
        a successful export, subsequent calls for the same class do nothing,
        even if its attributes have changed.
        """
        if cls._exported:
            return

        instance = cls()
        settings_exports = {}

        for attr_name in dir(instance):
            if attr_name.startswith("_"):
                continue

            if not attr_name.isupper():
                continue

            settings_exports[attr_name] = getattr(instance, attr_name)

        settings_module = sys.modules[cls.__module__]

        for setting_name, setting_value in settings_exports.items():
            setattr(settings_module, setting_name, setting_value)

        cls._exported = True

    @classmethod
    @abc.abstractmethod
    def get_urlpatterns(cls):
        """Return the URL patterns for the application's root URL configuration.

        Returns:
            A list of Django URL patterns and URL resolvers.
        """


def get_settings_class(module_name):
    """Return the settings subclass registered for a module.

    Registration occurs when a subclass is created, independently of `export()`.
    This function does not import the module or instantiate the returned class.

    Args:
        module_name: Fully qualified name of an already imported settings module.

    Returns:
        The `Settings` subclass registered under the given module name, which may
        still be abstract.

    Raises:
        LookupError: No subclass is registered for the module.
    """
    try:
        settings_class = _settings_class_registry[module_name]
    except KeyError as exc:
        msg = (
            f"no {f'{Settings.__module__}.{Settings.__qualname__}'!r} subclass "
            f"registered for module {module_name!r}; ensure the module defines "
            f"such a subclass and has been imported before accessing the registry"
        )
        raise LookupError(msg) from exc

    return settings_class
