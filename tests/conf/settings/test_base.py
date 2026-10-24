import importlib
import textwrap
from types import ModuleType

import pytest

from django.core.exceptions import ImproperlyConfigured

from reactor.conf.settings import base


@pytest.fixture
def settings_module(mocker):
    """Provide a temporary module for defining and exporting test settings."""
    module = ModuleType(name="settings")

    mocker.patch.dict("sys.modules", {module.__name__: module})

    return module


@pytest.fixture
def settings_class_factory(settings_module):
    """Provide a factory for concrete settings subclasses.

    The factory accepts a class name, target module, and extra attributes.
    Created classes belong to the target module and default to no URL patterns.
    """

    def _make_settings_class(
        *,
        class_name="Settings",
        module=settings_module,
        extra_attrs=None,
    ):
        settings_class = type(
            class_name,
            (base.Settings,),
            {
                "__module__": module.__name__,
                "get_urlpatterns": classmethod(lambda _: []),
                **(extra_attrs if extra_attrs is not None else {}),
            },
        )

        setattr(module, class_name, settings_class)

        return settings_class

    return _make_settings_class


@pytest.fixture
def module_writer(mocker, monkeypatch, tmp_path):
    """Provide a writer for temporary, importable Python modules.

    The writer accepts a module name and source text, removing common leading
    indentation. The module registry and import search path are restored after
    the test; changes within existing modules are not undone.
    """

    def _write_module(module_name, source):
        (tmp_path / f"{module_name}.py").write_text(textwrap.dedent(source))

    monkeypatch.syspath_prepend(tmp_path)
    mocker.patch.dict("sys.modules")

    return _write_module


class TestSettings:
    def test_init_subclass_allows_single_local_subclass(self, module_writer):
        # Arrange.
        module_writer(
            module_name="settings",
            source="""
                from reactor.conf.settings import base

                class Settings(base.Settings):
                    pass
            """,
        )

        # Act & assert.
        importlib.import_module("settings")

    def test_init_subclass_allows_imported_subclass(self, module_writer):
        # Arrange.
        module_writer(
            module_name="imported_settings",
            source="""
                from reactor.conf.settings import base

                class ImportedSettings(base.Settings):
                    pass
            """,
        )
        module_writer(
            module_name="settings",
            source="""
                from imported_settings import ImportedSettings

                class Settings(ImportedSettings):
                    pass
            """,
        )

        # Act & assert.
        importlib.import_module("settings")

    def test_init_subclass_allows_module_reload(self, module_writer):
        # Arrange.
        module_writer(
            module_name="settings",
            source="""
                from reactor.conf.settings import base

                class Settings(base.Settings):
                    pass
            """,
        )

        settings_module = importlib.import_module("settings")

        # Act & assert.
        importlib.reload(settings_module)

    def test_init_subclass_allows_module_reload_with_aliases(self, module_writer):
        # Arrange.
        module_writer(
            module_name="settings",
            source="""
                from reactor.conf.settings import base

                class Settings(base.Settings):
                    pass

                SettingsAlias = Settings
            """,
        )

        settings_module = importlib.import_module("settings")

        # Act & assert.
        importlib.reload(settings_module)

    def test_init_subclass_rejects_multiple_local_subclasses(self, module_writer):
        # Arrange.
        module_writer(
            module_name="settings",
            source="""
                from reactor.conf.settings import base

                class FirstSettings(base.Settings):
                    pass

                class SecondSettings(base.Settings):
                    pass
            """,
        )

        # Act & assert.
        with pytest.raises(
            TypeError,
            match=(
                r"module 'settings' defines multiple subclasses "
                r"of '(?:\w+\.)+Settings': 'FirstSettings' and 'SecondSettings'; "
                r"move each settings class into a separate module"
            ),
        ):
            importlib.import_module("settings")

    def test_export_exports_uppercase_attribute(
        self,
        settings_class_factory,
        settings_module,
    ):
        # Arrange.
        expected_value = object()

        settings_class = settings_class_factory(
            module=settings_module,
            extra_attrs={
                "SETTING": expected_value,
            },
        )

        # Act.
        settings_class.export()

        # Assert.
        assert settings_module.SETTING is expected_value

    def test_export_evaluates_uppercase_property(
        self,
        settings_class_factory,
        settings_module,
    ):
        # Arrange.
        expected_value = object()

        settings_class = settings_class_factory(
            module=settings_module,
            extra_attrs={
                "SETTING": property(lambda _: expected_value),
            },
        )

        # Act.
        settings_class.export()

        # Assert.
        assert settings_module.SETTING is expected_value

    @pytest.mark.parametrize(
        "attr_name",
        [
            pytest.param("_SETTING", id="uppercase"),
            pytest.param("_setting", id="lowercase"),
            pytest.param("_Setting", id="title case"),
            pytest.param("_SeTtInG", id="mixed case"),
        ],
    )
    def test_export_skips_private_attribute(
        self,
        attr_name,
        settings_class_factory,
        settings_module,
    ):
        # Arrange.
        settings_class = settings_class_factory(
            module=settings_module,
            extra_attrs={
                attr_name: object(),
            },
        )

        # Act.
        settings_class.export()

        # Assert.
        assert not hasattr(settings_module, attr_name)

    @pytest.mark.parametrize(
        "attr_name",
        [
            pytest.param("setting", id="lowercase"),
            pytest.param("Setting", id="title case"),
            pytest.param("SeTtInG", id="mixed case"),
        ],
    )
    def test_export_skips_non_uppercase_attribute(
        self,
        attr_name,
        settings_class_factory,
        settings_module,
    ):
        # Arrange.
        settings_class = settings_class_factory(
            module=settings_module,
            extra_attrs={
                attr_name: object(),
            },
        )

        # Act.
        settings_class.export()

        # Assert.
        assert not hasattr(settings_module, attr_name)

    def test_export_wraps_evaluation_error(self, settings_class_factory):
        # Arrange.
        class EvaluationError(Exception):
            pass

        evaluation_error = EvaluationError()

        def evaluate_setting(_):
            raise evaluation_error

        settings_class = settings_class_factory(
            extra_attrs={"SETTING": property(evaluate_setting)},
        )

        # Act & assert.
        with pytest.raises(
            ImproperlyConfigured,
            match=(
                r"could not evaluate setting 'SETTING' on 'settings\.Settings'; "
                r"fix the setting using the chained exception for details"
            ),
        ) as exc_info:
            settings_class.export()

        exc_cause = exc_info.value.__cause__

        assert exc_cause is evaluation_error

    def test_export_preserves_module_on_evaluation_error(
        self,
        mocker,
        settings_class_factory,
        settings_module,
    ):
        # Arrange.
        class EvaluationError(Exception):
            pass

        def raise_evaluation_error():
            raise EvaluationError

        settings_class = settings_class_factory(
            module=settings_module,
            extra_attrs={
                "PASSING_SETTING": object(),
                "FAILING_SETTING": property(lambda _: raise_evaluation_error()),
            },
        )

        module_dict_before = settings_module.__dict__.copy()

        def dir_side_effect(obj):
            if isinstance(obj, settings_class):
                return [
                    "PASSING_SETTING",
                    "FAILING_SETTING",
                ]

            return dir(obj)

        # Evaluate a valid setting first to detect partial exports on failure.
        mocker.patch.object(base, "dir", side_effect=dir_side_effect)

        # Act & assert.
        with pytest.raises(ImproperlyConfigured):
            settings_class.export()

        module_dict_after = settings_module.__dict__

        assert module_dict_after == module_dict_before

    def test_export_is_idempotent(self, mocker, settings_class_factory):
        # Arrange.
        settings_class = settings_class_factory(
            extra_attrs={
                "evaluate_setting": staticmethod(lambda: None),
                "SETTING": property(lambda self: self.evaluate_setting()),
            },
        )

        evaluate_setting_spy = mocker.spy(settings_class, "evaluate_setting")

        # Act.
        settings_class.export()
        settings_class.export()

        # Assert.
        evaluate_setting_spy.assert_called_once()


class TestGetSettingsClass:
    def test_returns_registered_class(self, settings_class_factory, settings_module):
        # Arrange.
        expected_settings_class = settings_class_factory(module=settings_module)

        # Act.
        settings_class = base.get_settings_class(module_name=settings_module.__name__)

        # Assert.
        assert settings_class is expected_settings_class

    def test_rejects_unregistered_module(self, settings_class_registry):
        # Arrange.
        settings_class_registry.pop("settings", None)

        # Act & assert.
        with pytest.raises(
            LookupError,
            match=(
                r"no '(?:\w+\.)+Settings' subclass registered for module 'settings'; "
                r"ensure the module defines such a subclass and has been imported "
                r"before accessing the registry"
            ),
        ) as exc_info:
            base.get_settings_class(module_name="settings")

        exc_cause = exc_info.value.__cause__

        assert isinstance(exc_cause, KeyError)
        assert exc_cause.args == ("settings",)
