#!/usr/bin/env python

import os
import sys
from contextlib import suppress


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reactor.conf.settings.dev")

    from django.core.management import execute_from_command_line

    with suppress(ImportError, IndexError):
        import django_extensions  # noqa: F401

        if sys.argv[1] == "shell":
            sys.argv[1] = "shell_plus"

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
