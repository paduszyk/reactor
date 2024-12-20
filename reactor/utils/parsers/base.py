from abc import ABC, abstractmethod


class Parser(ABC):
    def __init__(self, raw_value):
        self._raw_value = raw_value
        self._setup_failed = False

        try:
            self.setup(raw_value)
        except Exception:  # noqa: BLE001
            self._setup_failed = True

    def __getattribute__(self, name):
        accessible_attrs = {
            "parsed",
            "setup_failed",
        }

        if (
            not name.startswith("_")
            and name not in accessible_attrs
            and self._setup_failed
        ):
            return self._raw_value

        return super().__getattribute__(name)

    @abstractmethod
    def setup(self, raw_value): ...

    @property
    def setup_failed(self):
        return self._setup_failed
