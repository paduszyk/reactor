import importlib
import textwrap
import types

import pytest

from reactor.conf.settings import base


@pytest.fixture
def settings_module(mocker):
    module = types.ModuleType(name="settings")

    mocker.patch.dict("sys.modules", {module.__name__: module})

    return module


@pytest.fixture
def settings_class_factory(settings_module):
    def make_settings_class(*, module=None, class_name="Settings", extra_attrs=None):
        module = module if module is not None else settings_module

        method_stubs = {
            "get_urlpatterns": classmethod(lambda _: []),
            "get_database_config": lambda _: {},
            "get_storage_config": lambda _: {},
        }

        attrs = {
            "__module__": module.__name__,
            **method_stubs,
            **(extra_attrs if extra_attrs is not None else {}),
        }

        settings_class = type(class_name, (base.Settings,), attrs)

        setattr(module, class_name, settings_class)

        return settings_class

    return make_settings_class


@pytest.fixture(autouse=True)
def settings_class_registry(mocker):
    return mocker.patch.dict(f"{base.__name__}._settings_class_registry")


@pytest.fixture
def write_tmp_module(mocker, monkeypatch, tmp_path):
    def write_tmp_module(module_name, source):
        module_path = tmp_path / f"{module_name}.py"

        module_path.write_text(textwrap.dedent(source))

    monkeypatch.syspath_prepend(tmp_path)
    mocker.patch.dict("sys.modules")

    return write_tmp_module


class TestSettings:
    def test_init_subclass_allows_imported_subclass(self, write_tmp_module):
        # Arrange.
        write_tmp_module(
            module_name="imported_settings",
            source="""
                from reactor.conf.settings import base

                class ImportedSettings(base.Settings):
                    pass
            """,
        )
        write_tmp_module(
            module_name="settings",
            source="""
                from imported_settings import ImportedSettings

                class Settings(ImportedSettings):
                    pass
            """,
        )

        # Act & assert.
        importlib.import_module("settings")

    def test_init_subclass_allows_module_reload(self, write_tmp_module):
        # Arrange.
        write_tmp_module(
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

    def test_init_subclass_rejects_second_subclass_in_module(self, write_tmp_module):
        # Arrange.
        write_tmp_module(
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
                r"module 'settings' must define only one '(?:\w+\.)+Settings' "
                r"subclass, got 'FirstSettings' and 'SecondSettings'"
            ),
        ):
            importlib.import_module("settings")

    def test_export_sets_uppercase_attribute_on_module(
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

    def test_export_evaluates_uppercase_property(self, mocker, settings_class_factory):
        # Arrange.
        settings_class = settings_class_factory(
            extra_attrs={
                "evaluate_setting": staticmethod(lambda: None),
                "SETTING": property(lambda self: self.evaluate_setting()),
            },
        )

        # Spy.
        evaluate_setting_spy = mocker.spy(settings_class, "evaluate_setting")

        # Act.
        settings_class.export()

        # Assert.
        evaluate_setting_spy.assert_called()

    def test_export_skips_repeated_evaluation(self, mocker, settings_class_factory):
        # Arrange.
        settings_class = settings_class_factory(
            extra_attrs={
                "evaluate_setting": staticmethod(lambda: None),
                "SETTING": property(lambda self: self.evaluate_setting()),
            },
        )

        # Spy.
        evaluate_setting_spy = mocker.spy(settings_class, "evaluate_setting")

        # Act.
        settings_class.export()
        settings_class.export()

        # Assert.
        evaluate_setting_spy.assert_called_once()

    @pytest.mark.parametrize(
        "transform_case",
        [
            pytest.param(str.upper, id="uppercase"),
            pytest.param(str.lower, id="lowercase"),
            pytest.param(str.title, id="title-case"),
            pytest.param(str.swapcase, id="mixed-case"),
        ],
    )
    def test_export_skips_private_attribute(
        self,
        settings_class_factory,
        settings_module,
        transform_case,
    ):
        # Arrange.
        attr_name = transform_case("_Setting")

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
        "transform_case",
        [
            pytest.param(str.lower, id="lowercase"),
            pytest.param(str.title, id="title-case"),
            pytest.param(str.swapcase, id="mixed-case"),
        ],
    )
    def test_export_skips_non_uppercase_attribute(
        self,
        settings_class_factory,
        settings_module,
        transform_case,
    ):
        # Arrange.
        attr_name = transform_case("Setting")

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

        # Mock.
        def dir_side_effect(obj):
            if isinstance(obj, settings_class):
                return [
                    "PASSING_SETTING",
                    "FAILING_SETTING",
                ]

            return dir(obj)

        mocker.patch.object(base, "dir", side_effect=dir_side_effect)

        # Act & assert.
        with pytest.raises(EvaluationError):
            settings_class.export()

        assert settings_module.__dict__ == module_dict_before


class TestGetSettingsClass:
    def test_returns_registered_class(self, settings_class_factory, settings_module):
        # Arrange.
        expected_settings_class = settings_class_factory(module=settings_module)

        # Act.
        settings_class = base.get_settings_class(settings_module.__name__)

        # Assert.
        assert settings_class is expected_settings_class

    def test_rejects_unregistered_module(self, settings_class_registry):
        # Arrange.
        settings_class_registry.pop("settings", None)

        # Act & assert.
        with pytest.raises(
            LookupError,
            match=r"no '(?:\w+\.)+Settings' subclass registered for module 'settings'",
        ) as exc_info:
            base.get_settings_class("settings")

        exc_cause = exc_info.value.__cause__

        assert isinstance(exc_cause, KeyError)
        assert exc_cause.args == ("settings",)
