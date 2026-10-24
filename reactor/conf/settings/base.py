"""Base settings and discovery of application settings classes."""

import abc
import sys

from django.core.exceptions import ImproperlyConfigured

_settings_class_registry = {}


class Settings(abc.ABC):
    """Base settings with module discovery and export to Django.

    Each module may define one settings subclass; imported settings classes
    may be used as bases. Concrete subclasses must support construction without
    arguments and provide or inherit an implementation of `get_urlpatterns`.

    Public uppercase attributes, including inherited attributes and properties,
    become module-level Django settings when `export` is called. Other
    attributes may provide helpers without becoming Django settings.
    """

    def __init_subclass__(cls, **kwargs):
        """Register the subclass as its module's settings class.

        Redefining the same class name is allowed to support module reloads.

        Raises:
            TypeError: The module already defines another settings subclass.
        """
        super().__init_subclass__(**kwargs)

        class_name, module_name = cls.__name__, cls.__module__
        module_attrs = sys.modules[module_name].__dict__

        existing_settings_class = module_attrs.get(class_name)

        for attr_name, attr in module_attrs.items():
            if not (
                isinstance(attr, type)
                and issubclass(attr, Settings)
                and attr.__module__ == module_name
            ):
                continue

            # Reloading replaces the previous class; aliases may still reference it.
            if attr is existing_settings_class:
                continue

            msg = (
                f"module {module_name!r} defines multiple subclasses "
                f"of {f'{Settings.__module__}.{Settings.__qualname__}'!r}: "
                f"{attr_name!r} and {class_name!r}; move each settings class "
                f"into a separate module"
            )
            raise TypeError(msg)

        cls._exported = False

        _settings_class_registry[module_name] = cls

    @classmethod
    def export(cls):
        """Publish this class's settings in its defining module.

        Public uppercase properties are evaluated on an instance before any
        settings are assigned to the module. If evaluation fails, no settings
        are exported and a later call may retry. Side effects from property
        evaluation are not rolled back. After a successful export, further calls
        do nothing, including when configuration values have subsequently changed.

        Raises:
            ImproperlyConfigured: A setting cannot be evaluated.
        """
        if cls._exported:
            return

        settings_instance = cls()
        settings_to_export = {}

        for attr_name in dir(settings_instance):
            if attr_name.startswith("_"):
                continue

            if not attr_name.isupper():
                continue

            try:
                setting_value = getattr(settings_instance, attr_name)
            except Exception as exc:
                msg = (
                    f"could not evaluate setting {attr_name!r} on "
                    f"{f'{cls.__module__}.{cls.__qualname__}'!r}; fix the setting "
                    f"using the chained exception for details"
                )
                raise ImproperlyConfigured(msg) from exc

            settings_to_export[attr_name] = setting_value

        settings_module = sys.modules[cls.__module__]

        for setting_name, setting_value in settings_to_export.items():
            setattr(settings_module, setting_name, setting_value)

        cls._exported = True

    @classmethod
    @abc.abstractmethod
    def get_urlpatterns(cls):
        """Return the Django URL patterns for this settings environment.

        Overrides provide a list of URL patterns or resolvers for the root URL
        configuration. Django's apps must be initialized before this method is
        called.
        """


def get_settings_class(module_name):
    """Return the settings class registered for an imported module.

    Args:
        module_name: Fully qualified name of a module defining a settings
            subclass. The module must already have been imported.

    Raises:
        LookupError: No settings class is registered for the module.
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
