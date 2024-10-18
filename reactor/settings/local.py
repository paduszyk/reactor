from pathlib import Path

from . import debug


class Settings(debug.Settings):
    """Encapsulates settings specific to local development environments."""

    @classmethod
    def pre_load(cls):
        super().pre_load()

        cls.env.read_env(Path.cwd() / ".env", overwrite=True)
