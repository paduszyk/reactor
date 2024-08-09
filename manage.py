#!/usr/bin/env python

__all__ = []

import os
import sys
from contextlib import suppress
from pathlib import Path

CI_RUN = os.getenv("CI") is not None


def main():
    """Configure the environment and run Django."""
    if (source_path := Path(__file__).resolve().parent / "src").exists():
        sys.path.append(source_path.as_posix())

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reactor.conf.settings")
    os.environ.setdefault("DJANGO_CONFIGURATION", "CI" if CI_RUN else "Dev")

    with suppress(ImportError):
        from dotenv import load_dotenv

        load_dotenv(override=True)

    from configurations.management import execute_from_command_line

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
