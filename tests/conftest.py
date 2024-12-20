from functools import partialmethod

import pytest
from model_bakery import baker


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
