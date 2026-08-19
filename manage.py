#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

import os
import sys
import webbrowser
import time
from threading import Thread


def open_browser():
    # Wait for Django to finish starting
    time.sleep(8)
    webbrowser.open_new("http://127.0.0.1:8000/")


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "risk_project.settings")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable?"
        ) from exc

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    if "runserver" in sys.argv and "--noreload" in sys.argv:
        Thread(target=open_browser, daemon=True).start()

    main()