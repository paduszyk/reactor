import os
import sys

__all__ = []


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reactor.conf.settings")
    os.environ.setdefault("DJANGO_CONFIGURATION", "CI" if os.getenv("CI") else "Local")

    from configurations.management import execute_from_command_line

    execute_from_command_line(sys.argv)
