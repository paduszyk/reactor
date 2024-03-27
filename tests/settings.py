import os

from reactor.conf.settings import CI, Local

__all__ = ["Tests"]

# Inherit from 'CI' if running in CI, otherwise from 'Local'. CI is detected by the
# presence of the 'CI' environment variable.

TestsBase = CI if os.getenv("CI") else Local


class Tests(TestsBase):
    """Represents settings specific to environments running tests."""
