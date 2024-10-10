import os

if os.getenv("CI"):
    from . import ci as dev
else:
    from . import local as dev


Settings = type("Settings", (dev.Settings,), {})
