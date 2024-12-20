import random
from functools import partialmethod

import pytest
from model_bakery import baker

from django.contrib.contenttypes.models import ContentType

from reactor.schema.output.models import Work
from reactor.schema.units.models import Unit


def _update_unit_kwargs(kwargs):
    if unit := kwargs.pop("unit", None):
        kwargs.setdefault(
            "unit_type",
            ContentType.objects.get_for_model(unit),
        )
        kwargs.setdefault(
            "unit_id",
            unit.pk,
        )
    elif "unit_type" not in kwargs:
        unit_model = random.choice(Unit.__subclasses__())
        unit = baker.make(unit_model)

        kwargs.update(
            unit_type=ContentType.objects.get_for_model(unit),
            unit_id=unit.pk,
        )


def _update_work_kwargs(kwargs):
    if work := kwargs.pop("work", None):
        kwargs.setdefault(
            "work_type",
            ContentType.objects.get_for_model(work),
        )
        kwargs.setdefault(
            "work_id",
            work.pk,
        )
    elif "work_type" not in kwargs:
        work_model = random.choice(Work.__subclasses__())
        work = baker.make(work_model)

        kwargs.update(
            work_type=ContentType.objects.get_for_model(work),
            work_id=work.pk,
        )


def make_hr_contract(**kwargs):
    _update_unit_kwargs(kwargs)

    return baker.make("hr.Contract", **kwargs)


def make_output_contribution(**kwargs):
    _update_work_kwargs(kwargs)

    _fill_optional = kwargs.pop("_fill_optional", [])
    if _fill_optional is True or "unit" in _fill_optional:
        _update_unit_kwargs(kwargs)

    return baker.make("output.Contribution", **kwargs)


class BakerWrapper:
    def _baker_model_method(self, method_name, model, **kwargs):
        app_label, model_name = model.lower().split(".")

        if method_func := globals().get(f"{method_name}_{app_label}_{model_name}"):
            return method_func(**kwargs)

        return getattr(baker, method_name)(model, **kwargs)

    make = partialmethod(_baker_model_method, "make")

    def _baker_recipe_method(self, method_name, *args, **kwargs):
        return getattr(baker, method_name)(*args, **kwargs)

    make_recipe = partialmethod(_baker_recipe_method, "make_recipe")


@pytest.fixture(name="baker")
def _baker():
    return BakerWrapper()
