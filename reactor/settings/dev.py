import os

if os.getenv("CI"):
    from . import ci as dev
else:
    from . import local as dev


class Settings(dev.Settings):
    """Encapsulates settings specific to development environments."""
