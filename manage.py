#!/usr/bin/env python

if __name__ == "__main__":
    import os
    import sys

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reactor.conf.settings.dev")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
