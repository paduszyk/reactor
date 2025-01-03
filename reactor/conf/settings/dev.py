import os

if os.environ.get("CI"):
    from . import ci as dev
else:
    from . import local as dev


class Settings(dev.Settings):
    load = True
