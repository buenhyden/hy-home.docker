"""Gated, bounded shell execution used by the existing work dispatcher."""

from __future__ import annotations

import contextlib
import fcntl
import ipaddress
import json
import os
import re
import select
import shutil
import signal
import stat
import subprocess
import sys
import time
import uuid
from pathlib import Path

from scripts.lib.ops.environment_admission import (
    AdmissionError,
    _private_directory,
    process_identity,
    process_status,
)

TICK = 0.05
CONTROLLER_CPUS = 0.25
CONTROLLER_MEMORY_BYTES = 512 * 1024**2
CONTROLLER_DISK_BYTES = 4 * 1024**2


class ProcessError(ValueError):
    """A shell execution that cannot establish the requested boundary."""


def _argv(value):
    return (
        isinstance(value, list)
        and bool(value)
        and all(isinstance(part, str) and "\0" not in part for part in value)
    )


def _kill(process: subprocess.Popen) -> None:
    """Stop the worker's whole process group, then reap the worker."""
    for sig in (signal.SIGTERM, signal.SIGKILL):
        try:
            os.killpg(process.pid, sig)
        except ProcessLookupError:
            break
        time.sleep(0.5)
    process.wait()


def _write_record(path, record):
    temporary = path.with_name(path.name + "." + uuid.uuid4().hex)
    with open(temporary, "x", encoding="utf-8") as handle:
        os.chmod(temporary, 0o600)
        json.dump(record, handle)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)
    descriptor = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _budget(value, timeout):
    result = {
        "cpus": 1.0,
        "memory_bytes": 512 * 1024**2,
        "disk_bytes": 256 * 1024**2,
        "runtime_seconds": timeout,
    }
    if value is not None:
        if not isinstance(value, dict) or set(value) - set(result):
            raise ProcessError("invalid resource_budget")
        result.update(value)
    for amount in result.values():
        if type(amount) not in (int, float) or not 0 < amount < float("inf"):
            raise ProcessError("resource_budget values must be positive and finite")
    if result["runtime_seconds"] > 600 or timeout > result["runtime_seconds"]:
        raise ProcessError("timeout must fit resource_budget runtime at most600s")
    return result


def _controller_environment(environment):
    allowed = (
        "HOME",
        "XDG_RUNTIME_DIR",
        "DBUS_SESSION_BUS_ADDRESS",
        "HY_TASK",
        "HY_BRIEF_REVISION",
        "HY_WORK_UNIT",
        "HY_FENCE",
    )
    result = {
        "PATH": "/usr/bin:/bin",
        "LC_ALL": "C.UTF-8",
        **{key: environment[key] for key in allowed if key in environment},
    }
    result.setdefault("XDG_RUNTIME_DIR", f"/run/user/{os.getuid()}")
    result.setdefault(
        "DBUS_SESSION_BUS_ADDRESS", "unix:path=" + result["XDG_RUNTIME_DIR"] + "/bus"
    )
    return result


def _git_view(gitdir, tree, base, directory, disk_bytes):
    """Minimal readonly inspection metadata; never expose the common config."""

    def git(*args, data=None):
        return subprocess.run(
            [
                "git",
                "-C",
                str(tree),
                "--git-dir=" + str(gitdir),
                "--work-tree=" + str(tree),
                *args,
            ],
            check=True,
            capture_output=True,
            input=data,
        ).stdout

    current = git("write-tree").strip()
    heads = (base.encode(), current)
    objects = {base.encode(), current}
    for head in heads:
        objects.add(git("rev-parse", head.decode() + "^{tree}").strip())
        objects.update(
            row.split(b"\t", 1)[0].split()[2]
            for row in git("ls-tree", "-r", "-t", "-z", head.decode()).split(b"\0")
            if row
        )
    listing = b"\n".join(sorted(objects)) + b"\n"
    sizes = git("cat-file", "--batch-check=%(objectsize)", data=listing)
    if sum(int(size) for size in sizes.splitlines()) * 2 > disk_bytes:
        raise ProcessError("snapshot exceeds scratch disk reservation")
    (directory / "objects/pack").mkdir(parents=True)
    (directory / "refs").mkdir()
    git("pack-objects", str(directory / "objects/pack/pack"), data=listing)
    (directory / "HEAD").write_text(base + "\n")
    (directory / "shallow").write_text(base + "\n")
    (directory / "config").write_text("[core]\nrepositoryformatversion=0\nbare=false\n")
    shutil.copyfile(Path(gitdir) / "index", directory / "index")
    return directory


def _bounded_command(command, token, budget, *, cwd, env, git_view=None, provider=None):
    """Bubblewrap with a read-only root and only the worktree writable.

    A provider profile adds the network, its own read-only binds and its
    environment; nothing else of the host becomes visible.
    """
    boundary = [
        "/usr/bin/bwrap",
        "--unshare-all",
        "--die-with-parent",
        "--new-session",
        "--cap-drop",
        "ALL",
        "--clearenv",
        "--setenv",
        "PATH",
        "/usr/bin:/bin",
        "--setenv",
        "HOME",
        "/tmp",
        "--setenv",
        "LC_ALL",
        "C.UTF-8",
    ]
    for path in ("/usr", "/bin", "/lib", "/lib64", "/etc/ld.so.cache"):
        if Path(path).exists():
            boundary += ["--ro-bind", path, path]
    for name in ("HY_TASK", "HY_BRIEF_REVISION", "HY_WORK_UNIT", "HY_FENCE"):
        if name in env:
            boundary += ["--setenv", name, env[name]]
    directory = str(Path(cwd).resolve(strict=True))
    boundary += [
        "--proc",
        "/proc",
        "--dev",
        "/dev",
        "--size",
        str(int(budget["disk_bytes"])),
        "--tmpfs",
        "/tmp",
        "--size",
        "1048576",
        "--tmpfs",
        "/run",
    ]
    if provider is not None:
        boundary.append("--share-net")
        for source, target in provider["binds"]:
            boundary += ["--ro-bind", source, target]
        for name, value in provider["env"].items():
            boundary += ["--setenv", name, value]
    if git_view is not None:
        boundary += [
            "--ro-bind",
            str(git_view),
            "/hy-home-git",
            "--setenv",
            "GIT_DIR",
            "/hy-home-git",
            "--setenv",
            "GIT_WORK_TREE",
            directory,
            "--setenv",
            "GIT_OPTIONAL_LOCKS",
            "0",
            "--setenv",
            "GIT_CONFIG_NOSYSTEM",
            "1",
            "--setenv",
            "GIT_CONFIG_GLOBAL",
            "/dev/null",
        ]
    boundary += [
        "--bind",
        directory,
        directory,
        "--chdir",
        directory,
        "--remount-ro",
        "/",
    ]
    boundary = [*boundary, "--", *command]
    if provider is not None and provider.get("egress") == "public":
        boundary = _egress_limited(boundary, provider["dns"])
    return _scope_command(boundary, token, budget)


# Ranges an egress-limited worker must never reach: the host's own bridges and
# services, the LAN, carrier-grade NAT and link-local metadata addresses.
PRIVATE_RANGES = (
    "10.0.0.0/8",
    "172.16.0.0/12",
    "192.168.0.0/16",
    "100.64.0.0/10",
    "169.254.0.0/16",
)
# Run as root of pasta's own user namespace, before bubblewrap drops every
# capability: cut the private ranges, then hand the resolver to bubblewrap.
EGRESS_SETUP = (
    "set -e; for net in "
    + " ".join(PRIVATE_RANGES)
    + '; do /usr/sbin/ip route add unreachable "$net"; done; '
    + 'dns="$1"; shift; exec "$@" 3<<EOF\nnameserver $dns\nEOF\n'
)


def _egress_limited(boundary, dns):
    """Wrap bubblewrap in a pasta network namespace with public egress only.

    pasta forwards no port either way and does not map its gateway to the
    host, the namespace uses 198.18.0.0/24 so no private route is needed, and
    bubblewrap shares that namespace without any capability to change it.
    """
    if not ipaddress.ip_address(dns).is_global:
        raise ValueError("the egress resolver must be a public address")
    bwrap = boundary.index("--share-net")
    inner = [
        *boundary[:bwrap],
        "--ro-bind-data",
        "3",
        "/etc/resolv.conf",
        *boundary[bwrap:],
    ]
    return [
        "/usr/bin/pasta",
        "--config-net",
        "--quiet",
        "-4",
        "--no-map-gw",
        "-T", "none", "-U", "none", "-t", "none", "-u", "none",
        "-a", "198.18.0.2", "-n", "24", "-g", "198.18.0.1",
        "-D", dns,
        "--",
        "/bin/sh", "-c", EGRESS_SETUP, "sh", dns,
        *inner,
    ]  # fmt: skip


def _scope_command(command, token, budget):
    scope = "hy-home-worker-" + token + ".scope"
    return (
        [
            "/usr/bin/systemd-run",
            "--user",
            "--scope",
            "--quiet",
            "--unit=" + scope,
            "--property=Description=hy-home-worker:" + token,
            "--property=CPUQuota=" + str(budget["cpus"] * 100) + "%",
            "--property=MemoryMax=" + str(int(budget["memory_bytes"])),
            "--property=TasksMax=256",
            "--property=KillMode=control-group",
            "--property=RuntimeMaxSec=" + str(budget["runtime_seconds"]),
            "--",
            *command,
        ],
        scope,
    )


def _registered_command(command, token, budget, **kwargs):
    if (
        _argv(command)
        and command[:4]
        == ["/usr/bin/docker", "--host", "unix:///var/run/docker.sock", "wait"]
        and len(command) == 5
        and re.fullmatch(r"[0-9a-f]{12,64}", command[4])
    ):
        return _scope_command(command, token, budget)
    if (
        not _argv(command)
        or command[:4]
        != ["/usr/bin/docker", "--host", "unix:///var/run/docker.sock", "compose"]
        or sum(part in ("up", "down", "stop") for part in command[4:]) != 1
        or any(
            part in ("exec", "run", "build", "pull", "config", "--context", "-H")
            for part in command[4:]
        )
    ):
        raise ProcessError("unregistered Docker operation")
    return _scope_command(command, token, budget)


def _registered_target(command, record):
    if command[3] == "wait":
        return (
            "wait"  # Caller verifies its read-only job ID using project/token labels.
        )
    projects = []
    for index, part in enumerate(command[4:], 4):
        if part in ("-p", "--project-name"):
            if index + 1 == len(command):
                raise ProcessError("Compose project is missing")
            projects.append(command[index + 1])
        elif part.startswith("--project-name="):
            projects.append(part.split("=", 1)[1])
        elif part.startswith("-p") and len(part) > 2:
            projects.append(part[2:])
    if not record.get("project") or projects != [record["project"]]:
        raise ProcessError("Compose project does not match its reservation")
    return next(part for part in command[4:] if part in ("up", "down", "stop"))


def _scope_absent(scope, token, *, stop=False):
    if scope is None:
        return True  # Only injected local process fixtures omit a scope.
    if scope != "hy-home-worker-" + token + ".scope":
        return False
    try:

        def state():
            found = subprocess.run(
                [
                    "/usr/bin/systemctl",
                    "--user",
                    "show",
                    scope,
                    "--property=LoadState,ActiveState,Description",
                ],
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )
            return dict(
                line.split("=", 1) for line in found.stdout.splitlines() if "=" in line
            )

        current = state()
        if current.get("LoadState") == "not-found":
            return True
        if current.get("Description") != "hy-home-worker:" + token:
            return False
        if stop:
            subprocess.run(
                ["/usr/bin/systemctl", "--user", "stop", scope],
                capture_output=True,
                timeout=10,
                check=False,
            )
        return state().get("ActiveState") in ("inactive", "failed")
    except (OSError, subprocess.TimeoutExpired):
        return False


def _group_absent(identity):
    try:
        os.killpg(identity["pgid"], 0)
    except ProcessLookupError:
        return True
    except (PermissionError, KeyError, TypeError):
        pass
    return False


def _disk_problem(paths, budget):
    """Inspect owned inode metadata only; never follow a worker's symlink."""
    total, count = 0, 0
    try:
        for path in paths:
            descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
            stack = [descriptor]
            try:
                while stack:
                    current = stack.pop()
                    try:
                        found = os.fstat(current)
                        space = os.fstatvfs(current)
                        if (
                            space.f_bavail * space.f_frsize
                            < space.f_blocks * space.f_frsize / 10
                        ):
                            return "host disk headroom below10percent"
                        if stat.S_ISDIR(found.st_mode):
                            with os.scandir(current) as entries:
                                for entry in entries:
                                    count += 1
                                    if count > 100000:
                                        return "owned disk inventory limit exceeded"
                                    info = os.stat(
                                        entry.name,
                                        dir_fd=current,
                                        follow_symlinks=False,
                                    )
                                    if stat.S_ISDIR(info.st_mode):
                                        stack.append(
                                            os.open(
                                                entry.name,
                                                os.O_RDONLY
                                                | os.O_DIRECTORY
                                                | os.O_NOFOLLOW,
                                                dir_fd=current,
                                            )
                                        )
                                    elif stat.S_ISREG(info.st_mode) or stat.S_ISLNK(
                                        info.st_mode
                                    ):
                                        total += info.st_size
                                    else:
                                        return "unsupported owned disk object"
                        elif stat.S_ISREG(found.st_mode):
                            total += found.st_size
                        else:
                            return "unsupported owned disk root"
                        if total > budget:
                            return "disk budget exceeded"
                    finally:
                        os.close(current)
            finally:
                for descriptor in stack:
                    os.close(descriptor)
        return None
    except OSError:
        return "owned disk usage unavailable"


def _bootstrap(path, control_fd, ack_fd):
    record = json.loads(Path(path).read_text())
    record = {**record, "identity": process_identity(), "state": "ready"}
    _write_record(Path(path), record)
    os.write(ack_fd, b"R")
    os.close(ack_fd)
    with os.fdopen(control_fd, "rb", buffering=0) as control:
        message = control.readline(1024 * 1024)
        if not message.endswith(b"\n"):
            return 125
        command = json.loads(message)
        if not _argv(command):
            return 125
        child = subprocess.Popen(command, stdin=subprocess.DEVNULL)
        while child.poll() is None:
            if select.select([control], [], [], TICK)[0] and not control.read(1):
                _scope_absent(record["scope"], record["token"], stop=True)
                os.killpg(os.getpgrp(), signal.SIGKILL)
        # Keep the leader alive while removing its session's background children.
        for candidate in Path("/proc").iterdir():
            if candidate.name.isdigit() and int(candidate.name) != os.getpid():
                try:
                    descriptor = os.pidfd_open(int(candidate.name))
                    try:
                        if os.getpgid(int(candidate.name)) == os.getpgrp():
                            signal.pidfd_send_signal(descriptor, signal.SIGKILL)
                    finally:
                        os.close(descriptor)
                except (ProcessLookupError, PermissionError):
                    pass
        return child.returncode


def _spawn(
    command,
    *,
    root,
    name,
    cwd,
    env,
    stdout,
    admission,
    budget,
    kind,
    reservation=None,
    git_view=None,
    register=True,
    trusted_docker=False,
    disk_paths=None,
    provider=None,
):
    record = reservation or admission.admit(services=(), budget=budget, kind=kind)
    token = record["token"]
    disk_paths = tuple(Path(path) for path in (disk_paths or (cwd,)))
    builder = _registered_command if trusted_docker else _bounded_command
    path = root / (name + ".process.json")
    process = None
    scope = None
    descriptors = []
    try:
        extra = {"provider": provider} if provider is not None else {}
        command, scope = builder(
            command, token, budget, cwd=cwd, env=env, git_view=git_view, **extra
        )
        _write_record(
            path,
            {"token": token, "state": "intent", "identity": None, "scope": scope},
        )
        if register:
            admission.update(
                token, process_file=str(path), run_id=root.name, scope=scope
            )
        control_r, control_w = os.pipe()
        descriptors.extend((control_r, control_w))
        ack_r, ack_w = os.pipe()
        descriptors.extend((ack_r, ack_w))
        environment = _controller_environment(env)
        if trusted_docker:
            environment.update(
                {key: value for key, value in env.items() if key.startswith("LAB_")}
            )
        process = subprocess.Popen(
            [
                sys.executable,
                str(
                    Path(__file__).resolve().parents[2] / "operations/work_dispatch.py"
                ),
                "--bootstrap",
                str(path),
                str(control_r),
                str(ack_w),
            ],
            cwd=cwd,
            env=environment,
            stdout=stdout,
            stderr=subprocess.STDOUT,
            stdin=subprocess.DEVNULL,
            start_new_session=True,
            pass_fds=(control_r, ack_w),
        )
        os.close(control_r)
        os.close(ack_w)
        if not select.select([ack_r], [], [], 5)[0] or os.read(ack_r, 1) != b"R":
            raise OSError("worker ownership handshake failed")
        saved = json.loads(path.read_text())
        if saved["token"] != token or process_status(saved["identity"]) != "alive":
            raise OSError("worker ownership changed before release")
        problem = _disk_problem(disk_paths, budget["disk_bytes"])
        if problem:
            raise ProcessError(problem)
        if register:
            admission.attach(
                token,
                saved["identity"],
                process_file=str(path),
                run_id=root.name,
                scope=scope,
            )
        os.write(control_w, json.dumps(command).encode() + b"\n")
        (root / (name + ".pgid")).write_text(str(process.pid))
        return {
            "process": process,
            "control": control_w,
            "identity": saved["identity"],
            "environment_token": token,
            "process_file": path,
            "scope": scope,
            "disk_paths": disk_paths,
            "disk_budget": budget["disk_bytes"],
        }
    except BaseException:
        if process is not None:
            identity = process_identity(process.pid)
            _kill(process)
            absent = _scope_absent(scope, token, stop=True)
            if register and identity is not None:
                if admission.release(
                    token, verify=lambda _: absent and _group_absent(identity)
                ):
                    path.unlink(missing_ok=True)
        elif register:
            try:
                scope_absent = scope is None or _scope_absent(scope, token, stop=True)
                if path.exists():
                    saved = json.loads(path.read_text())
                    intent_matches = saved == {
                        "token": token,
                        "state": "intent",
                        "identity": None,
                        "scope": scope,
                    }
                else:
                    intent_matches = True
                released = (
                    scope_absent
                    and intent_matches
                    and admission.release(
                        token,
                        verify=lambda current: (
                            current["owner"] == record["owner"]
                            and current["kind"] == kind
                            and current["state"] == "intent"
                            and current["identity"] is None
                            and current["budget"] == record["budget"]
                            and current["metadata"].get("process_file")
                            in (None, str(path))
                            and current["metadata"].get("scope") in (None, scope)
                        ),
                    )
                )
                if released:
                    path.unlink(missing_ok=True)
            except (OSError, ValueError, KeyError, AdmissionError, StopIteration):
                pass
        for descriptor in descriptors:
            try:
                os.close(descriptor)
            except OSError:
                pass
        raise
    finally:
        if len(descriptors) >= 3:
            try:
                os.close(descriptors[2])
            except OSError:
                pass


def _finish_environment(job, admission):
    os.close(job["control"])
    absent = _scope_absent(job["scope"], job["environment_token"], stop=True)
    released = admission.release(
        job["environment_token"],
        verify=lambda _: absent and _group_absent(job["identity"]),
    )
    if released:
        job["process_file"].unlink(missing_ok=True)
    return released


def prepare_registered_docker(admission, token):
    """Prebind a private operation directory before the first Docker effect."""
    directory = admission.path.parent / "operations" / token
    record = next((row for row in admission.records() if row["token"] == token), None)
    if record is None:
        raise ProcessError("unknown Docker operation token")
    previous = record["metadata"].get("docker_operation_dir")
    if previous is not None:
        if Path(previous) != directory or not (directory / "operation.json").is_file():
            raise ProcessError("existing Docker operation proof unavailable")
        with _operation_lock(directory):
            journal = json.loads((directory / "operation.json").read_text())
            if journal.get("claim_token") != token:
                raise ProcessError("foreign Docker operation proof")
        return directory
    admission.update(token, docker_operation_dir=str(directory))
    _private_directory(directory)
    marker = directory / "operation.json"
    with _operation_lock(directory):
        if not marker.exists():
            _write_record(marker, {"claim_token": token, "state": "prepared"})
    return directory


@contextlib.contextmanager
def _operation_lock(directory):
    found = directory.lstat()
    if (
        not stat.S_ISDIR(found.st_mode)
        or found.st_uid != os.getuid()
        or stat.S_IMODE(found.st_mode) & 0o077
        or directory.resolve() != directory
    ):
        raise ProcessError("unsafe Docker operation directory")
    descriptor = os.open(
        directory / "operation.lock", os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o600
    )
    try:
        found = os.fstat(descriptor)
        if (
            not stat.S_ISREG(found.st_mode)
            or found.st_uid != os.getuid()
            or found.st_mode & 0o077
        ):
            raise ProcessError("unsafe Docker operation lock")
        fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
        yield
    except BlockingIOError:
        raise ProcessError("Docker operation already active") from None
    finally:
        os.close(descriptor)


def _operation_directory(record):
    directory = Path(record["metadata"]["docker_operation_dir"])
    if (
        directory.name != record["token"]
        or directory.parent.name != "operations"
        or not directory.is_absolute()
    ):
        raise ProcessError("unbound Docker operation directory")
    return directory


def _verify_operation(record, directory, *, stop=False):
    marker = directory / "operation.json"
    journal = json.loads(marker.read_text())
    if journal.get("claim_token") != record["token"]:
        return False
    if journal.get("state") == "prepared":
        return True
    if journal.get("state") != "intent":
        return False
    token = journal["operation_token"]
    recorded_token = record["metadata"].get("docker_operation_token")
    if recorded_token not in (None, token):
        return False
    process_file = directory / "controller.process.json"
    if not process_file.is_file():
        return _scope_absent("hy-home-worker-" + token + ".scope", token, stop=stop)
    saved = json.loads(process_file.read_text())
    if (
        saved["token"] != token
        or saved["scope"] != "hy-home-worker-" + token + ".scope"
    ):
        return False
    absent = _scope_absent(saved["scope"], token, stop=stop)
    deadline = time.monotonic() + (2 if stop else 0)
    while process_status(saved["identity"]) == "alive" and time.monotonic() < deadline:
        time.sleep(TICK)
    return (
        absent
        and process_status(saved["identity"]) == "absent"
        and _group_absent(saved["identity"])
    )


def verify_registered_docker_absent(record, *, stop=False):
    """Observe a prebound operation; lost or unknown state is not absence."""
    try:
        directory = _operation_directory(record)
        with _operation_lock(directory):
            return _verify_operation(record, directory, stop=stop)
    except (OSError, ValueError, KeyError, AdmissionError):
        return False


def cleanup_unstarted_registered_docker(record, *, owner_may_be_live=False):
    """Remove only a token-owned partial pre-spawn directory with no controller token."""
    try:
        from scripts.lib.ops.environment_admission import process_identity

        owner_status = process_status(record["owner"])
        if owner_may_be_live:
            if process_identity(record["owner"]["pid"]) != record["owner"]:
                return False
        elif owner_status != "absent":
            return False
        metadata = record["metadata"]
        if metadata.get("docker_operation_token"):
            return False
        raw = metadata.get("docker_operation_dir")
        if raw is None:
            return True
        directory = Path(raw)
        if (
            not directory.is_absolute()
            or directory.name != record["token"]
            or directory.parent.name != "operations"
        ):
            return False
        if not directory.exists():
            return True
        with _operation_lock(directory):
            names = {path.name for path in directory.iterdir()}
            allowed = {"operation.lock", "operation.json"}
            allowed.update(
                name
                for name in names
                if re.fullmatch(r"operation\.json\.[0-9a-f]{32}", name)
            )
            if names - allowed:
                return False
            marker = directory / "operation.json"
            if marker.exists():
                journal = json.loads(marker.read_text())
                if journal.get("claim_token") != record["token"]:
                    return False
                if journal.get("state") == "prepared":
                    pass
                elif journal.get("state") == "intent":
                    operation_token = journal.get("operation_token")
                    if (
                        not isinstance(operation_token, str)
                        or not re.fullmatch(r"[0-9a-f]{32}", operation_token)
                        or (directory / "controller.process.json").exists()
                        or (directory / "controller.pgid").exists()
                        or not _scope_absent(
                            "hy-home-worker-" + operation_token + ".scope",
                            operation_token,
                        )
                    ):
                        return False
                else:
                    return False
            for path in directory.iterdir():
                found = path.lstat()
                if (
                    not stat.S_ISREG(found.st_mode)
                    or found.st_uid != os.getuid()
                    or found.st_mode & 0o077
                ):
                    return False
            for path in directory.iterdir():
                path.unlink()
            directory.rmdir()
        return True
    except (OSError, ValueError, KeyError, AdmissionError):
        return False


def cleanup_registered_docker(record):
    """Remove only the closed claim's known operation files after caller release."""
    try:
        directory = _operation_directory(record)
        with _operation_lock(directory):
            if not _verify_operation(record, directory):
                return False
            names = {
                "operation.json",
                "operation.lock",
                "controller.process.json",
                "controller.pgid",
            }
            if {path.name for path in directory.iterdir()} - names:
                return False
            for path in directory.iterdir():
                if not path.is_file() or path.is_symlink():
                    return False
            for path in directory.iterdir():
                path.unlink()
            directory.rmdir()
        return True
    except (OSError, ValueError, KeyError, AdmissionError):
        return False


def run_registered_docker(argv, *, cwd, timeout, admission, token, env=None):
    """Only generated local Docker lifecycle commands use this trusted lane."""
    record = next((row for row in admission.records() if row["token"] == token), None)
    if (
        record is None
        or record["workspace_id"] != admission.workspace_id
        or record["daemon_id"] != admission.daemon_id
    ):
        raise ProcessError("foreign Docker operation token")
    directory = _operation_directory(record)
    controller = {
        "cpus": CONTROLLER_CPUS,
        "memory_bytes": CONTROLLER_MEMORY_BYTES,
        "disk_bytes": CONTROLLER_DISK_BYTES,
    }
    if any(record["budget"][key] < amount for key, amount in controller.items()):
        raise ProcessError("controller budget was not reserved")
    budget = _budget(controller, timeout)
    # Validate before replacing an earlier operation's ownership witness.
    _registered_command(argv, "validation", budget)
    operation = _registered_target(argv, record)
    with _operation_lock(directory):
        if not _verify_operation(record, directory):
            raise ProcessError("prior Docker operation is live or unobserved")
        if not any(row["token"] == token for row in admission.records()):
            raise ProcessError("closed Docker operation token")
        operation_token = uuid.uuid4().hex
        _write_record(
            directory / "operation.json",
            {
                "claim_token": token,
                "operation_token": operation_token,
                "state": "intent",
            },
        )
        if record["kind"] == "compose-start":
            admission.update(token, docker_operation_token=operation_token)
        execution = _spawn(
            argv,
            root=directory,
            name="controller",
            cwd=cwd,
            env=os.environ if env is None else env,
            stdout=subprocess.DEVNULL,
            admission=None,
            budget=budget,
            kind="docker-controller",
            reservation={**record, "token": operation_token},
            register=False,
            trusted_docker=True,
            disk_paths=(directory,),
        )
        try:
            try:
                code = execution["process"].wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                _kill(execution["process"])
                code = 124
        finally:
            if execution["process"].returncode is None:
                _kill(execution["process"])
            os.close(execution["control"])
            if not _verify_operation(record, directory, stop=True):
                raise ProcessError("Docker controller cleanup unverified")
        # Raw controller output can contain interpolated data or environment values.
        # Successful wait callers obtain the numeric job status by bounded inspect.
        diagnostic = (
            "" if code == 0 else f"Docker controller {operation} failed (exit={code})."
        )
        return subprocess.CompletedProcess(
            argv, code, stdout="", stderr=diagnostic[:128]
        )
