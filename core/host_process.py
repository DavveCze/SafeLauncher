"""Environment handling for host tools started by the packaged launcher."""

import os
from typing import Mapping, Optional


_PYTHON_OVERRIDES = (
    "PYTHONHOME",
    "PYTHONPATH",
    "PYTHONEXECUTABLE",
    "PYTHONUSERBASE",
)


def host_process_env(base_env: Optional[Mapping[str, str]] = None) -> dict[str, str]:
    """Return an environment safe for system executables.

    PyInstaller one-file applications temporarily prepend their extraction
    directory to ``LD_LIBRARY_PATH``. Passing that environment to host tools
    such as ``/bin/sh`` or ``umu-run`` can make them load incompatible bundled
    readline/OpenSSL libraries. PyInstaller preserves the caller's original
    value in ``LD_LIBRARY_PATH_ORIG``; restore it before starting host tools.
    """
    env = dict(os.environ if base_env is None else base_env)
    original_library_path = env.pop("LD_LIBRARY_PATH_ORIG", None)
    if original_library_path is None:
        env.pop("LD_LIBRARY_PATH", None)
    else:
        env["LD_LIBRARY_PATH"] = original_library_path

    # These interpreter/loader overrides are meaningful to the bundled app but
    # must not influence the host Python used by umu-run or other system tools.
    env.pop("LD_PRELOAD", None)
    env.pop("LD_AUDIT", None)
    for variable in _PYTHON_OVERRIDES:
        env.pop(variable, None)
    return env
