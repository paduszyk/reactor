"""Application management command entry point."""

import sys
from pathlib import Path

from environ import Env


def main():
    """Run the management command specified by the process arguments.

    Defaults from the project `.env` file are loaded before Django initializes.
    Existing process environment variables take precedence.
    """
    Env.read_env(env_file=Path(__file__).resolve().parent / ".env")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
