from pathlib import Path

from pkm_installer import directories, venvs
import importlib_metadata as mtd
import venv
import subprocess
import sys


def _required_version():
    return mtd.version("pkm_installer")


def _installed_version():
    try:
        return mtd.version("pkm_main")
    except mtd.PackageNotFoundError:
        return ''


def setup():
    data_dir = directories.data_dir()
    venv_dir = data_dir / 'venvs/pkm'
    required_version = _required_version()

    if venv_dir.exists():
        venvs.activate(venv_dir)

        installed_version = _installed_version()

        if installed_version != required_version:
            _install(venv_dir, required_version)

    else:
        venv_dir.parent.mkdir(parents=True, exist_ok=True)
        venv.create(venv_dir, with_pip=True, prompt="pkm")
        venvs.activate(venv_dir)
        _install(venv_dir, required_version)


def _install(venv: Path, version: str):
    python_executable = str(venv / "bin/python")
    print("Needs to update my environment after upgrade/first-install... ")
    subprocess.check_call([python_executable, "-m", "pip", "install", f'pkm-main=={version}', "-qq"])
    print("Update completed.")
