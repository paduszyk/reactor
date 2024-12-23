__all__ = [
    "HumanName",
]

from .base import Parser


class HumanName(Parser):
    def _setup(self, raw_value):
        last, given = map(str.strip, raw_value.split(","))

        self._last = last
        self._given = " ".join(given.split())

    @property
    def last(self):
        return self._last

    @property
    def given(self):
        return self._given

    @property
    def first(self):
        return self.given.split()[0]

    @property
    def middle(self):
        return " ".join(self.given.split()[1:])

    @property
    def full(self):
        return self._get_full(reversed_=False)

    @property
    def full_reversed(self):
        return self._get_full(reversed_=True)

    @property
    def short(self):
        return self._get_short(reversed_=False)

    @property
    def short_reversed(self):
        return self._get_short(reversed_=True)

    @property
    def initials(self):
        return self._get_initials("first", "middle", "last")

    @staticmethod
    def _get_initial(name):
        return f"{name[:1]}." if name else ""

    def _get_initials(self, *attrs):
        initial_list = []

        for attr in attrs:
            attr_parts = getattr(self, attr).split()

            initial_list.append(
                " ".join(
                    "-".join(map(self._get_initial, attr_part.split("-")))
                    for attr_part in attr_parts
                ),
            )

        return " ".join(filter(None, initial_list))

    def _get_full(self, *, reversed_):
        parts = [f"{self.first} {self._get_initials('middle')}".strip(), self.last]

        return " ".join(reversed(parts) if reversed_ else parts)

    def _get_short(self, *, reversed_):
        parts = [self._get_initials("given").strip(), self.last]

        return " ".join(reversed(parts) if reversed_ else parts)
