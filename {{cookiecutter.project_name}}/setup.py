#!/usr/bin/env python
import distutils
import os
import setuptools
import shlex
import shutil
import subprocess
import threading
import time

from pip._internal.req import parse_requirements
from watchdog import observers
from watchdog import events


class BlackCommand(distutils.cmd.Command):
    """A custom command to format python code"""

    description = "run Black on Python source files"
    user_options = []

    def initialize_options(self):
        """Set default values for options."""
        pass

    def finalize_options(self):
        """Post-process options."""
        pass

    def run(self):
        """Run command."""
        command = f"python -mblack setup.py {self.distribution.get_name()} tests"

        self.announce(f"Running command: {command}", level=distutils.log.INFO)
        subprocess.check_call(shlex.split(command))


class DocsCommand(distutils.cmd.Command):
    """A custom command to format python code"""

    description = "generate documentation"
    user_options = []

    def initialize_options(self):
        """Set default values for options."""
        pass

    def finalize_options(self):
        """Post-process options."""
        pass

    def run(self):
        """Run command."""
        command = "make html"

        if os.path.exists("docs/_build") and os.path.isdir("docs/_build"):
            self.announce(f"Removing build directory", level=distutils.log.INFO)
            shutil.rmtree("docs/_build")

        self.announce(f"Running command: {command}", level=distutils.log.INFO)
        if os.name == "nt":
            subprocess.check_call(shlex.split(command), cwd="docs", shell=True)
        else:
            subprocess.check_call(shlex.split(command), cwd="docs")


class PipWatch(events.PatternMatchingEventHandler):
    def on_any_event(self, event):
        subprocess.check_call(shlex.split("pip install ."))


class WatchCommand(distutils.cmd.Command):
    """A custom command to format python code"""

    description = "watch install"
    user_options = []

    def initialize_options(self):
        """Set default values for options."""
        pass

    def finalize_options(self):
        """Post-process options."""
        pass

    def run(self):
        event_handler = PipWatch("*.py")
        observer = observers.Observer()
        observer.schedule(event_handler, self.distribution.get_name(), recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(5)
        except KeyboardInterrupt:
            observer.stop()

setuptools.setup(
    name="{{cookiecutter.project_name}}",
    version="{{cookiecutter.project_version}}",
    author="{{cookiecutter.project_authors}}",
    packages=setuptools.find_packages(),
    entry_points={"console_scripts": ["{{cookiecutter.project_name}}={{cookiecutter.project_name}}.__main__:cli"]},
    cmdclass={
        "black": BlackCommand,
        "docs": DocsCommand,
        "watch": WatchCommand,
    },
    install_requires=[str(i.req) for i in parse_requirements('requirements.txt', session='hack')],
)
