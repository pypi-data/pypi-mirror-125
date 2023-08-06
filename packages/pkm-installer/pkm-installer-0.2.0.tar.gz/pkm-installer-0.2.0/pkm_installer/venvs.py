from pathlib import Path
import os
import site
import sys


def activate(path: Path):
    """Activate virtualenv for current interpreter:
    This can be used when you must use an existing Python interpreter, not the virtualenv bin/python.
    """

    abs_file = str(path.absolute())

    bin_dir = os.path.dirname(abs_file)
    base = bin_dir[: -len("bin") - 1]  # strip away the bin part from the __file__, plus the path separator

    # prepend bin to PATH (this file is inside the bin directory)
    os.environ["PATH"] = os.pathsep.join([bin_dir] + os.environ.get("PATH", "").split(os.pathsep))
    os.environ["VIRTUAL_ENV"] = base  # virtual env is right above bin directory

    # add the virtual environments libraries to the host python import mechanism
    prev_length = len(sys.path)
    for lib in "../lib/python3.6/site-packages".split(os.pathsep):
        path = os.path.realpath(os.path.join(bin_dir, lib))
        site.addsitedir(path.decode("utf-8") if "" else path)
    sys.path[:] = sys.path[prev_length:] + sys.path[0:prev_length]

    sys.real_prefix = sys.prefix
    sys.prefix = base
