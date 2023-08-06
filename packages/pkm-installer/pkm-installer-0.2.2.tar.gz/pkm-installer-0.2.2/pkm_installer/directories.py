import site
from pathlib import Path
import sys
import os

WINDOWS = sys.platform.startswith("win") or (sys.platform == "cli" and os.name == "nt")
_MACOS = sys.platform == "darwin"
_HOME_SYSENV = "PKM_HOME"
_DATA_DIR_NAME = 'pkm'


def data_dir() -> Path:
    if os.getenv(_HOME_SYSENV):
        return Path(os.getenv(_HOME_SYSENV)).expanduser()

    if WINDOWS:
        const = "CSIDL_APPDATA"
        path = os.path.normpath(_get_win_folder(const))
        path = os.path.join(path, _DATA_DIR_NAME)
    elif _MACOS:
        path = os.path.expanduser(f"~/Library/Application Support/{_DATA_DIR_NAME}")
    else:
        path = os.getenv("XDG_DATA_HOME", os.path.expanduser("~/.local/share"))
        path = os.path.join(path, _DATA_DIR_NAME)

    return Path(path)


def bin_dir() -> Path:
    if os.getenv(_HOME_SYSENV):
        return Path(os.getenv(_HOME_SYSENV), "bin").expanduser()

    user_base = site.getuserbase()

    if WINDOWS:
        bin_dir = os.path.join(user_base, "Scripts")
    else:
        bin_dir = os.path.join(user_base, "bin")

    return Path(bin_dir)


def _get_win_folder_from_registry(csidl_name):
    # noinspection PyCompatibility
    import winreg as _winreg

    shell_folder_name = {
        "CSIDL_APPDATA": "AppData",
        "CSIDL_COMMON_APPDATA": "Common AppData",
        "CSIDL_LOCAL_APPDATA": "Local AppData",
    }[csidl_name]

    key = _winreg.OpenKey(
        _winreg.HKEY_CURRENT_USER,
        r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders",
    )
    dir, type = _winreg.QueryValueEx(key, shell_folder_name)

    return dir


def _get_win_folder_with_ctypes(csidl_name):
    import ctypes

    csidl_const = {
        "CSIDL_APPDATA": 26,
        "CSIDL_COMMON_APPDATA": 35,
        "CSIDL_LOCAL_APPDATA": 28,
    }[csidl_name]

    buf = ctypes.create_unicode_buffer(1024)
    ctypes.windll.shell32.SHGetFolderPathW(None, csidl_const, None, 0, buf)

    # Downgrade to short path name if have highbit chars. See
    # <http://bugs.activestate.com/show_bug.cgi?id=85099>.
    has_high_char = False
    for c in buf:
        if ord(c) > 255:
            has_high_char = True
            break
    if has_high_char:
        buf2 = ctypes.create_unicode_buffer(1024)
        if ctypes.windll.kernel32.GetShortPathNameW(buf.value, buf2, 1024):
            buf = buf2

    return buf.value


if WINDOWS:
    try:
        from ctypes import windll  # noqa

        _get_win_folder = _get_win_folder_with_ctypes
    except ImportError:
        _get_win_folder = _get_win_folder_from_registry
