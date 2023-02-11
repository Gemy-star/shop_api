#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import signal


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                          "config.settings.development")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    if sys.argv[1] == "runserver":
        execute_from_command_line([sys.argv[0], "migrate"])
        from django.contrib.auth.models import Group
        if Group.objects.all().count() == 0:
            Group.objects.create('Manager')
            Group.objects.create('Delivery Crew')
        from apps.scheduler.cluster import QCluster
        global q_cluster
        q_cluster = QCluster()
        signal.signal(signal.SIGINT, sigint_handler)

    execute_from_command_line(sys.argv)


def sigint_handler(signal, frame):
    global q_cluster
    q_cluster.stop()
    sys.exit(0)


if __name__ == "__main__":
    main()
