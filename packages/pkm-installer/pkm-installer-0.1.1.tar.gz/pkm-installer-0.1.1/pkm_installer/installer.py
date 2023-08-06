from pkm_installer import directories, venvs
import importlib_metadata as mtd
import venv
import subprocess
import sys


def _required_version():
    return mtd.version("pkm_installer")


def _installed_version():
    return mtd.version("pkm_main")


def activate():
    data_dir = directories.data_dir()
    venv_dir = data_dir / 'venvs/pkm'
    required_version = _required_version()

    print(f"will install version: {required_version}")

    if venv_dir.exists():
        print("activating pkm environment...")
        venvs.activate(venv_dir)

        installed_version = _installed_version()
        print(f"installed version: {installed_version}")

        if installed_version != required_version:
            _install(required_version)

    else:
        venv_dir.parent.mkdir(parents=True, exist_ok=True)
        venv.create(venv_dir)
        venvs.activate(venv_dir)
        _install(required_version)


def _install(version: str):
    subprocess.check_call([sys.executable, "-m", "pip", "install", f'pkm-main=={version}'])
