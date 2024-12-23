from abc import ABC, abstractmethod


class Parser(ABC):
    def __init__(self, raw_value):
        self._raw_value = raw_value
        self._setup_exc = None

        try:
            self._setup(raw_value)
        except Exception as e:  # noqa: BLE001
            self._setup_exc = e

    def __getattribute__(self, name):
        if not name.startswith("_") and self._setup_exc is not None:
            return self._raw_value

        return super().__getattribute__(name)

    @abstractmethod
    def _setup(self, raw_value): ...
