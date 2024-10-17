from pathlib import Path

from . import debug


class Settings(debug.Settings):
    @classmethod
    def pre_load(cls):
        super().pre_load()

        cls.env.read_env(Path.cwd() / ".env", overwrite=True)
