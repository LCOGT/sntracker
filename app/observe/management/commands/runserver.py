import os
import platform
import sys

import django
from django.conf import settings
from django.contrib.staticfiles.management.commands import runserver
from django.core.management.commands.runserver import BaseRunserverCommand
from django.contrib.staticfiles.handlers import StaticFilesHandler
from django.db import connection
from django.http import Http404
from django.utils.termcolors import colorize
from django.views.static import serve

def banner():

    # The raw banner split into lines.
    lines = ("""
 ____
/ ___| _   _ _ __   ___ _ __ _ __   _____   ____ _
\___ \| | | | '_ \ / _ \ '__| '_ \ / _ \ \ / / _` |
 ___) | |_| | |_) |  __/ |  | | | | (_) \ V / (_| |
|____/ \__,_| .__/ \___|_|  |_| |_|\___/ \_/ \__,_|
            |_|
 _____               _
|_   _| __ __ _  ___| | _____ _ __
  | || '__/ _` |/ __| |/ / _ \ '__|
  | || | | (_| | (__|   <  __/ |
  |_||_|  \__,_|\___|_|\_\___|_|   
* Django %(django_version)s
* Python %(python_version)s
* %(os_name)s %(os_version)s
* AsteroidDay %(astday_version)s

""" % {
        "django_version": django.get_version(),
        "python_version": sys.version.split(" ", 1)[0],
        "os_name": platform.system(),
        "os_version": platform.release(),
        "astday_version" : settings.VERSION,
    }).splitlines()

    return "\n".join(lines)


class Command(BaseRunserverCommand):
    """
    Overrides runserver to display an ODIN banner
    """

    def inner_run(self, *args, **kwargs):
        # Show the funky ODIN banner in the terminal. There
        # aren't really any exceptions to catch here, but we do
        # so blanketly since such a trivial thing like the banner
        # shouldn't be able to crash the development server.

        try:
            self.stdout.write(banner())
        except Exception, e:
            print e
            pass
        super(Command, self).inner_run(*args, **kwargs)
