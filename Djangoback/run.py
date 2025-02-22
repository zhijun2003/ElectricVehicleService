# Djangoback/run.py
import os
import sys

from django.core.management import execute_from_command_line


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoadmin.settings")
    execute_from_command_line([sys.argv[0], "runserver", "0.0.0.0:8000"])


if __name__ == "__main__":
    main()
