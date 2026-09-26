import os
import sys
from pathlib import Path

from environ import Env


def main():
    """Run a Django management command for local development.

    Development settings are selected before loading `.env`, so the file cannot
    choose another settings module. Use `--settings` or explicitly set the
    `DJANGO_SETTINGS_MODULE` environment variable to select different settings.
    The `--settings` option takes precedence over the environment variable.
    """
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reactor.conf.settings.dev")

    Env.read_env(env_file=Path(__file__).resolve().parent / ".env")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
