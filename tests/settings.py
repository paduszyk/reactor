__all__ = [
    "Test",
]

import os
from contextlib import suppress

from reactor.conf.settings import CI, Dev

CI_RUN = os.getenv("CI") is not None

TestBase = CI if CI_RUN else Dev


class Test(TestBase):
    """Encapsulates settings specific to test environments."""

    # Apps

    INSTALLED_APPS = TestBase.INSTALLED_APPS + ["tests"]

    @classmethod
    def pre_setup(cls):
        with suppress(ImportError):
            from dotenv import load_dotenv

            load_dotenv(override=True)

        super().pre_setup()
