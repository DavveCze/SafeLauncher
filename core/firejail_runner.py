import os
import shlex
import shutil
import subprocess
from core.interfaces import ISandboxRunner
from core.host_process import host_process_env

_VALID_MODES = {"umu", "umu_net", "wine", "linux"}


class FirejailSandboxRunner(ISandboxRunner):
    def __init__(self):
        self.proton_path = ""

    def set_proton_path(self, proton_path: str) -> None:
        """Set an optional local Proton/GE-Proton tool directory for UMU."""
        self.proton_path = os.path.realpath(os.path.expanduser(proton_path.strip())) if proton_path.strip() else ""

    @staticmethod
    def check_dependencies() -> dict:
        """Returns dict of system dependencies status."""
        return {
            "firejail": shutil.which("firejail") is not None,
            "umu-run": shutil.which("umu-run") is not None,
            "wine": shutil.which("wine") is not None,
        }

    def launch(self, game_path: str, executable: str, mode: str) -> subprocess.Popen:
        if not game_path or not os.path.exists(game_path):
            raise ValueError(f"Game path does not exist: {game_path}")

        if mode not in _VALID_MODES:
            raise ValueError(f"Unknown launch mode: {mode!r}. Must be one of {sorted(_VALID_MODES)}")

        deps = self.check_dependencies()
        has_firejail = deps["firejail"]

        home_dir = os.path.expanduser('~')
        umu_share = os.path.join(home_dir, '.local', 'share', 'umu')
        umu_cache = os.path.join(home_dir, '.cache', 'umu')

        os.makedirs(umu_share, exist_ok=True)
        os.makedirs(umu_cache, exist_ok=True)

        q_path = shlex.quote(game_path)
        q_exe = shlex.quote(executable)
        q_umu_share = shlex.quote(umu_share)
        q_umu_cache = shlex.quote(umu_cache)
        prefix_path = shlex.quote(os.path.join(game_path, 'prefix'))
        proton_env = f"--env=PROTONPATH={shlex.quote(self.proton_path)} " if self.proton_path else ""
        proton_whitelist = f"--whitelist={shlex.quote(self.proton_path)} " if self.proton_path else ""

        if mode in ("umu", "umu_net"):
            runner_cmd = f"umu-run {q_exe}" if deps["umu-run"] else f"wine {q_exe}"
            if has_firejail:
                net_flag = "--net=none " if mode == "umu" else ""
                cmd = (
                    f"cd {q_path} && exec firejail "
                    # UMU/Proton uses nested bubblewrap namespaces for the
                    # Steam runtime. These compatibility overrides are required
                    # for that runtime to start under Firejail.
                    f"--ignore=noroot --ignore=seccomp --ignore=restrict-namespaces "
                    f"{net_flag}"
                    f"--whitelist={q_path} --whitelist={q_umu_share} --whitelist={q_umu_cache} "
                    f"{proton_whitelist}{proton_env}--env=WINEPREFIX={prefix_path} {runner_cmd}"
                )
            else:
                # Direct unsandboxed execution fallback
                cmd = f"cd {q_path} && export WINEPREFIX={prefix_path} && {runner_cmd}"
        elif mode == "linux":
            full_exe_path = os.path.join(game_path, executable)
            if os.path.exists(full_exe_path):
                if not os.access(full_exe_path, os.X_OK):
                    try:
                        os.chmod(full_exe_path, os.stat(full_exe_path).st_mode | 0o111)
                    except Exception:
                        pass
            if has_firejail:
                cmd = f"cd {q_path} && exec firejail --net=none --whitelist={q_path} ./{q_exe}"
            else:
                cmd = f"cd {q_path} && ./{q_exe}"
        else:  # "wine"
            runner_cmd = f"wine {q_exe}"
            if has_firejail:
                cmd = (
                    f"cd {q_path} && exec firejail --net=none "
                    f"--whitelist={q_path} "
                    f"--env=WINEPREFIX={prefix_path} {runner_cmd}"
                )
            else:
                cmd = f"cd {q_path} && export WINEPREFIX={prefix_path} && {runner_cmd}"

        return subprocess.Popen(
            # Keep the wrapper independent from bash/readline libraries inherited
            # from Proton/Wine environments.  POSIX sh is sufficient for the
            # commands above and avoids errors such as bash's
            # "undefined symbol: rl_print_keybinding".
            ["/bin/sh", "-c", cmd],
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            env=host_process_env(),
        )
