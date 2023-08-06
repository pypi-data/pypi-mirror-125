import os
import sys
from pathlib import Path
from typing import Callable, NoReturn

from pkm_installer import directories, venvs
import importlib_metadata as mtd
from virtualenv import cli_run as venv_create
import subprocess

from pkm_installer.directories import WINDOWS

_VERSION_FILE = "etc/pkm/version"
_PYTHON_EXECUTABLE = "bin/python"
_PKM_EXECUTABLE = "bin/rp" if not WINDOWS else "bin/rp.exe"
EXECUTOR_T = Callable[[], NoReturn]


def _required_version():
    return mtd.version("pkm-installer")


def _installed_version(venv: Path) -> str:
    vfile = venv / _VERSION_FILE
    if not vfile.exists():
        return ''
    return vfile.read_text()


def install() -> EXECUTOR_T:
    data_dir = directories.data_dir()
    venv_dir = data_dir / 'venvs/pkm'
    required_version = _required_version()

    if venv_dir.exists():
        installed_version = _installed_version(venv_dir)
        print(f"installed version: {installed_version}")

        if installed_version != required_version:
            _install(venv_dir, required_version)

    else:
        venv_dir.parent.mkdir(parents=True, exist_ok=True)
        venv_create([str(venv_dir)])
        _install(venv_dir, required_version)

    def execute() -> NoReturn:
        os.execve(str(venv_dir / _PKM_EXECUTABLE), sys.argv, os.environ)

    return execute


def _install(venv: Path, version: str):
    python_executable = str(venv / _PYTHON_EXECUTABLE)
    print("Needs to setup my own virtual environment after upgrade/first-install... ")
    subprocess.check_call([python_executable, "-m", "pip", "install", 'pip', '-U'])
    subprocess.check_call([python_executable, "-m", "pip", "install", f'pkm-main=={version}'])
    version_file = venv / _VERSION_FILE
    version_file.parent.mkdir(parents=True, exist_ok=True)
    version_file.write_text(version)
    print("Setup completed.")
