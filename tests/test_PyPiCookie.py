"""Credits: https://github.com/audreyr/cookiecutter-pypackage/blob/master/tests/test_bake_project.py"""

import cookiecutter
import datetime
import os
import shlex
import subprocess

class InsideDir:
    def __init__(self, dir):
        self.dir = dir

    def __enter__(self):
        self.initial_dir = os.getcwd()
        os.chdir(self.dir)

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.chdir(self.initial_dir)

class TempBake:
    def __init__(self, cookies, *args, **kwargs):
        self._cookies = cookies
        self._args = args
        self._kwargs = kwargs

    def __enter__(self):
        self.result = self._cookies.bake(*self._args, **self._kwargs)
        return self.result
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        cookiecutter.utils.rmtree(str(self.result.project))

def run_inside_dir(cmd, dir):
    with InsideDir(dir):
        return subprocess.check_call(shlex.split(cmd))

#################################
            # TESTS #
#################################


def test_default_bake_project(cookies):
    result = cookies.bake()

    assert result.project.basename == 'PyProject'
    assert result.project.isdir()
    assert result.exit_code == 0
    assert result.exception is None

    top_level_files = [f.basename for f in result.project.listdir()]
    for top_level_file in ['docs', 'PyProject', 'tests', '.gitignore', '.readthedocs.yml', '.travis.yml', 'appveyor.yml', 'LICENSE', 'README.md', 'requirements.txt', 'setup.cfg', 'setup.py']:
        assert top_level_file in top_level_files

def test_license_year(cookies):
    with TempBake(cookies) as result:
        license_path = result.project.join('LICENSE')
        now = datetime.datetime.now()
        assert f'Copyright (c) {str(now.year)}' in license_path.read()

def test_run_setup_py(cookies):
    with TempBake(cookies) as result:
        assert result.project.isdir()
        assert run_inside_dir('pip install -rrequirements.txt', str(result.project)) == 0
        for cmd in ['black', 'docs', 'install', 'test']:
            assert run_inside_dir(f'python setup.py {cmd}', str(result.project)) == 0