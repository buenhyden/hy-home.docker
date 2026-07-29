from __future__ import annotations

import argparse
import collections.abc
import dataclasses
import errno
import os
import pathlib
import re
import select
import shutil
import signal
import stat
import subprocess
import sys
import tempfile
import time
from collections.abc import Mapping

try:
    from scripts.validation.ci_gate_contract import (
        GateContractError,
        GateKind,
        GateRegistry,
        expand_gate_ids,
        load_contract_document,
        parse_gate_registry,
        validate_gate_registry,
    )
except ModuleNotFoundError:  # Direct sibling-script execution.
    from ci_gate_contract import (  # type: ignore[no-redef]
        GateContractError,
        GateKind,
        GateRegistry,
        expand_gate_ids,
        load_contract_document,
        parse_gate_registry,
        validate_gate_registry,
    )


_GIT_TIMEOUT_SECONDS = 5
_SHEBANGS = {
    b"#!/usr/bin/env bash": "bash",
    b"#!/usr/bin/env python3": "python",
}
_SECRET_ENV_SHAPE = re.compile(
    r"(?:SECRET|TOKEN|PASSWORD|PASSWD|CREDENTIAL|AUTH|API_KEY|PRIVATE_KEY)",
    re.IGNORECASE,
)
_ADMITTED_ENV_KEYS = frozenset(
    {
        "CI",
        "EVENT_NAME",
        "GITHUB_ACTIONS",
        "GITHUB_STEP_SUMMARY",
        "HEAD_REF",
        "HYHOME_COMPOSE_PROFILES",
        "PR_BASE_SHA",
        "PR_TITLE",
        "PUSH_BEFORE_SHA",
        "SKIP",
        "TEMPLATE_GATE_BASE",
    }
)
_TERMINATION_GRACE_SECONDS = 0.25
_MAX_PROC_PID_ENTRIES = 65_536
_MAX_PROC_STAT_BYTES = 4_096
_PROC_ROOT = pathlib.Path("/proc")


@dataclasses.dataclass(frozen=True, slots=True)
class GateInvocation:
    gate_id: str
    entrypoint: pathlib.PurePosixPath
    argv: tuple[str, ...]
    cwd: pathlib.PurePosixPath
    allowed_env_keys: tuple[str, ...]
    timeout_seconds: int


GateExecutor = collections.abc.Callable[[GateInvocation], int]


@dataclasses.dataclass(slots=True)
class _VerifiedInvocation:
    invocation: GateInvocation
    entrypoint_fd: int
    cwd_fd: int
    interpreter: str


@dataclasses.dataclass(slots=True)
class _ProcessLifecycle:
    process: subprocess.Popen[bytes] | None = None
    pidfd: int | None = None
    group_finalized: bool = False
    reap_started: bool = False
    pidfd_close_attempted: bool = False

    @property
    def pidfd_acquired(self) -> bool:
        return self.pidfd is not None

    def bind_process(self, process: subprocess.Popen[bytes]) -> None:
        self.process = process

    def acquire_pidfd(self) -> None:
        if self.process is None:
            raise _runner_cleanup_error()
        self.pidfd = os.pidfd_open(self.process.pid)

    def mark_group_finalized(self) -> None:
        self.group_finalized = True

    def mark_reap_started(self) -> None:
        self.reap_started = True

    def mark_pidfd_close_attempted(self) -> None:
        self.pidfd_close_attempted = True


class _GateArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise GateContractError(
            "ci-gate-cli-arguments",
            "arguments",
            "the runner arguments do not match the closed grammar",
        )


def build_execution_plan(
    registry: GateRegistry,
    profile: str,
    gate_id: str | None,
    all_roots: bool,
) -> tuple[GateInvocation, ...]:
    node_by_id = {node.gate_id: node for node in registry.nodes}
    gate_ids = expand_gate_ids(registry, profile, gate_id, all_roots)
    invocations: list[GateInvocation] = []
    seen: set[str] = set()
    for selected_id in gate_ids:
        if selected_id in seen:
            continue
        seen.add(selected_id)
        node = node_by_id.get(selected_id)
        if (
            node is None
            or node.kind is GateKind.AGGREGATE
            or node.entrypoint is None
            or node.cwd is None
            or node.timeout_minutes is None
        ):
            raise GateContractError(
                "ci-gate-execution-node",
                selected_id,
                "the selected executable gate is incomplete",
            )
        invocations.append(
            GateInvocation(
                gate_id=node.gate_id,
                entrypoint=node.entrypoint,
                argv=node.argv,
                cwd=node.cwd,
                allowed_env_keys=node.allowed_env_keys,
                timeout_seconds=node.timeout_minutes * 60,
            )
        )
    return tuple(invocations)


def render_execution_plan(
    plan: tuple[GateInvocation, ...],
) -> tuple[str, ...]:
    return tuple(
        f"{invocation.gate_id}\t{invocation.entrypoint.as_posix()}"
        for invocation in plan
    )


def execute_execution_plan(
    root: pathlib.Path,
    plan: tuple[GateInvocation, ...],
    environ: Mapping[str, str],
    executor: GateExecutor | None = None,
) -> int:
    canonical_root = _canonical_root(root)
    path_value = environ.get("PATH", "")
    if not path_value:
        raise GateContractError(
            "ci-gate-environment",
            "PATH",
            "the controller PATH must be nonempty",
        )
    home = pathlib.Path(
        tempfile.mkdtemp(prefix="ci-gate-home-", dir="/tmp")
    )
    try:
        if executor is not None:
            for invocation in plan:
                result = executor(invocation)
                if result != 0:
                    return result
            return 0
        if not pathlib.Path("/proc/self/fd").is_dir():
            raise GateContractError(
                "ci-gate-procfd-unavailable",
                "/proc/self/fd",
                "descriptor execution is unavailable",
            )
        root_fd = _open_root(canonical_root)
        verified: list[_VerifiedInvocation] = []
        try:
            descriptor_root = f"/proc/self/fd/{root_fd}"
            python_bootstrap = _create_python_bootstrap(
                home,
                descriptor_root,
            )
            for invocation in plan:
                verified.append(
                    _verify_invocation(
                        root_fd,
                        invocation,
                        path_value,
                    )
                )
            for item in verified:
                child_environment = _child_environment(
                    root_fd,
                    home,
                    item.invocation,
                    item.interpreter,
                    environ,
                    python_bootstrap=python_bootstrap,
                )
                result = _run_verified_child(
                    root_fd,
                    item,
                    child_environment,
                )
                if result != 0:
                    return result
            return 0
        finally:
            for item in verified:
                _close(item.entrypoint_fd)
                _close(item.cwd_fd)
            _close(root_fd)
    finally:
        _remove_home(home)


def main(argv: list[str] | None = None) -> int:
    parser = _GateArgumentParser(
        description="Execute registered repository CI gates",
        add_help=True,
        exit_on_error=False,
    )
    parser.add_argument("--profile", required=True)
    selection = parser.add_mutually_exclusive_group(required=True)
    selection.add_argument("--gate")
    selection.add_argument("--all", action="store_true")
    selection.add_argument("--list", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    try:
        arguments = parser.parse_args(argv)
        if arguments.list and arguments.dry_run:
            raise GateContractError(
                "ci-gate-cli-arguments",
                "arguments",
                "list and dry-run are distinct modes",
            )
        root_value = os.environ.get("HYHOME_CI_GATE_ROOT")
        root = (
            pathlib.Path(root_value)
            if root_value
            else pathlib.Path(__file__).resolve().parents[2]
        )
        document = load_contract_document(root)
        registry = parse_gate_registry(
            document,
            ".github/workflow-contract.yml",
        )
        findings = validate_gate_registry(root, registry)
        if findings:
            for finding in findings:
                print(
                    f"FAIL [{finding.code}] {finding.path}: {finding.message}",
                    file=sys.stderr,
                )
            return 1
        plan = build_execution_plan(
            registry,
            arguments.profile,
            None if arguments.list or arguments.all else arguments.gate,
            arguments.list or arguments.all,
        )
        if arguments.list or arguments.dry_run:
            for line in render_execution_plan(plan):
                print(line)
            return 0
        return execute_execution_plan(root, plan, os.environ)
    except (GateContractError, argparse.ArgumentError) as error:
        if isinstance(error, GateContractError):
            code = error.code
            path = error.path
            message = error.message
        else:
            code = "ci-gate-cli-arguments"
            path = "arguments"
            message = "the runner arguments do not match the closed grammar"
        print(f"FAIL [{code}] {path}: {message}", file=sys.stderr)
        return 2 if code == "ci-gate-cli-arguments" else 1


def _canonical_root(root: pathlib.Path) -> pathlib.Path:
    candidate = pathlib.Path(root)
    try:
        resolved = candidate.resolve(strict=True)
    except OSError:
        raise GateContractError(
            "ci-gate-root-invalid",
            ".",
            "the repository root is unavailable",
        ) from None
    if (
        not candidate.is_absolute()
        or resolved != candidate
        or candidate.is_symlink()
        or not candidate.is_dir()
    ):
        raise GateContractError(
            "ci-gate-root-invalid",
            ".",
            "the repository root must be a canonical directory",
        )
    return candidate


def _open_root(root: pathlib.Path) -> int:
    try:
        return os.open(
            root,
            os.O_RDONLY | os.O_CLOEXEC | os.O_NOFOLLOW | os.O_DIRECTORY,
        )
    except OSError as error:
        raise GateContractError(
            "ci-gate-root-invalid",
            ".",
            "the repository root could not be opened",
        ) from error


def _canonical_parts(
    path: pathlib.PurePosixPath,
    *,
    dot: bool,
    code: str,
) -> tuple[str, ...]:
    source = path.as_posix()
    if (
        path.is_absolute()
        or ".." in path.parts
        or source != str(path)
        or (source == "." and not dot)
        or (source != "." and any(part in {"", "."} for part in path.parts))
    ):
        raise GateContractError(
            code,
            source,
            "the repository-relative path is invalid",
        )
    return () if source == "." else path.parts


def _open_directory_at(
    root_fd: int,
    path: pathlib.PurePosixPath,
    *,
    code: str,
) -> int:
    parts = _canonical_parts(path, dot=True, code=code)
    current = os.dup(root_fd)
    try:
        for part in parts:
            next_fd = os.open(
                part,
                os.O_RDONLY
                | os.O_CLOEXEC
                | os.O_NOFOLLOW
                | os.O_DIRECTORY,
                dir_fd=current,
            )
            _close(current)
            current = next_fd
        return current
    except OSError as error:
        _close(current)
        raise GateContractError(
            code,
            path.as_posix(),
            "the verified directory is invalid",
        ) from error


def _open_entrypoint_at(
    root_fd: int,
    path: pathlib.PurePosixPath,
) -> int:
    parts = _canonical_parts(
        path,
        dot=False,
        code="ci-gate-entrypoint-invalid",
    )
    parent_fd = os.dup(root_fd)
    try:
        for part in parts[:-1]:
            next_fd = os.open(
                part,
                os.O_RDONLY
                | os.O_CLOEXEC
                | os.O_NOFOLLOW
                | os.O_DIRECTORY,
                dir_fd=parent_fd,
            )
            _close(parent_fd)
            parent_fd = next_fd
        try:
            entrypoint_fd = os.open(
                parts[-1],
                os.O_RDONLY
                | os.O_CLOEXEC
                | os.O_NOFOLLOW
                | os.O_NONBLOCK,
                dir_fd=parent_fd,
            )
        except OSError as error:
            code = (
                "ci-gate-entrypoint-symlink"
                if error.errno in {errno.ELOOP, errno.ENOTDIR}
                else "ci-gate-entrypoint-invalid"
            )
            raise GateContractError(
                code,
                path.as_posix(),
                "the entrypoint path is invalid",
            ) from error
        return entrypoint_fd
    except OSError as error:
        raise GateContractError(
            "ci-gate-entrypoint-symlink",
            path.as_posix(),
            "the entrypoint parent path is invalid",
        ) from error
    finally:
        _close(parent_fd)


def _verify_invocation(
    root_fd: int,
    invocation: GateInvocation,
    path_value: str,
) -> _VerifiedInvocation:
    cwd_fd = _open_directory_at(
        root_fd,
        invocation.cwd,
        code="ci-gate-cwd-invalid",
    )
    entrypoint_fd = -1
    try:
        entrypoint_fd = _open_entrypoint_at(root_fd, invocation.entrypoint)
        metadata = os.fstat(entrypoint_fd)
        if not stat.S_ISREG(metadata.st_mode):
            raise GateContractError(
                "ci-gate-entrypoint-not-regular",
                invocation.entrypoint.as_posix(),
                "the entrypoint must be a regular file",
            )
        first_line = os.pread(entrypoint_fd, 256, 0).split(b"\n", 1)[0]
        interpreter = _SHEBANGS.get(first_line)
        if interpreter is None:
            raise GateContractError(
                "ci-gate-entrypoint-shebang",
                invocation.entrypoint.as_posix(),
                "the entrypoint shebang is not admitted",
            )
        mode, object_id = _tracked_entrypoint(
            root_fd,
            invocation.entrypoint,
            path_value,
        )
        if mode is None:
            raise GateContractError(
                "ci-gate-entrypoint-untracked",
                invocation.entrypoint.as_posix(),
                "the entrypoint must be tracked",
            )
        if mode != "100755":
            raise GateContractError(
                "ci-gate-entrypoint-mode",
                invocation.entrypoint.as_posix(),
                "the tracked entrypoint mode must be executable",
            )
        if not _descriptor_matches_object(
            root_fd,
            entrypoint_fd,
            object_id,
            path_value,
        ):
            raise GateContractError(
                "ci-gate-entrypoint-identity",
                invocation.entrypoint.as_posix(),
                "the entrypoint identity differs from the tracked object",
            )
        return _VerifiedInvocation(
            invocation,
            entrypoint_fd,
            cwd_fd,
            interpreter,
        )
    except BaseException:
        if entrypoint_fd >= 0:
            _close(entrypoint_fd)
        _close(cwd_fd)
        raise


def _git_environment(path_value: str) -> dict[str, str]:
    return {
        "PATH": path_value,
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_GLOBAL": "/dev/null",
    }


def _tracked_entrypoint(
    root_fd: int,
    path: pathlib.PurePosixPath,
    path_value: str,
) -> tuple[str | None, str]:
    try:
        result = subprocess.run(
            [
                "git",
                "--literal-pathspecs",
                "ls-files",
                "--stage",
                "-z",
                "--error-unmatch",
                "--",
                path.as_posix(),
            ],
            cwd=f"/proc/self/fd/{root_fd}",
            env=_git_environment(path_value),
            pass_fds=(root_fd,),
            capture_output=True,
            check=False,
            timeout=_GIT_TIMEOUT_SECONDS,
        )
    except (OSError, subprocess.TimeoutExpired):
        raise GateContractError(
            "ci-gate-entrypoint-provenance",
            path.as_posix(),
            "tracked entrypoint provenance is unavailable",
        ) from None
    if result.returncode != 0 or not result.stdout:
        return None, ""
    records = result.stdout.rstrip(b"\0").split(b"\0")
    if len(records) != 1:
        return None, ""
    try:
        metadata, recorded_path = records[0].split(b"\t", 1)
        mode, object_id, stage = metadata.decode("ascii").split(" ")
        decoded_path = recorded_path.decode("utf-8", errors="strict")
    except (UnicodeDecodeError, ValueError):
        return None, ""
    if stage != "0" or decoded_path != path.as_posix():
        return None, ""
    return mode, object_id


def _descriptor_matches_object(
    root_fd: int,
    entrypoint_fd: int,
    expected_object_id: str,
    path_value: str,
) -> bool:
    duplicate = os.dup(entrypoint_fd)
    try:
        os.lseek(duplicate, 0, os.SEEK_SET)
        with os.fdopen(duplicate, "rb", closefd=True) as source:
            duplicate = -1
            result = subprocess.run(
                ["git", "hash-object", "--stdin"],
                cwd=f"/proc/self/fd/{root_fd}",
                env=_git_environment(path_value),
                stdin=source,
                pass_fds=(root_fd,),
                capture_output=True,
                check=False,
                timeout=_GIT_TIMEOUT_SECONDS,
            )
    except (OSError, subprocess.TimeoutExpired):
        return False
    finally:
        if duplicate >= 0:
            _close(duplicate)
    if result.returncode != 0:
        return False
    try:
        actual = result.stdout.decode("ascii", errors="strict").strip()
    except UnicodeDecodeError:
        return False
    return actual == expected_object_id


def _child_environment(
    root: pathlib.Path | int,
    home: pathlib.Path,
    invocation: GateInvocation,
    interpreter: str,
    environ: Mapping[str, str],
    *,
    python_bootstrap: pathlib.Path | None = None,
) -> dict[str, str]:
    for key in invocation.allowed_env_keys:
        if (
            _SECRET_ENV_SHAPE.search(key)
            or key not in _ADMITTED_ENV_KEYS
        ):
            raise GateContractError(
                "ci-gate-environment",
                invocation.gate_id,
                "the gate environment key is not admitted",
            )
    root_value = (
        f"/proc/self/fd/{root}"
        if isinstance(root, int)
        else str(root)
    )
    admitted: dict[str, str] = {
        "PATH": environ["PATH"],
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "HOME": str(home),
        "TMPDIR": "/tmp",
        "PYTHONNOUSERSITE": "1",
        "PYTHONSAFEPATH": "1",
        "PIP_DISABLE_PIP_VERSION_CHECK": "1",
        "HYHOME_CI_GATE_ROOT": root_value,
    }
    if interpreter == "python":
        if python_bootstrap is None:
            raise GateContractError(
                "ci-gate-python-bootstrap",
                invocation.gate_id,
                "the isolated Python bootstrap is unavailable",
            )
        admitted["PYTHONPATH"] = str(python_bootstrap)
    for key in invocation.allowed_env_keys:
        if key in environ:
            admitted[key] = environ[key]
    return admitted


def _create_python_bootstrap(
    home: pathlib.Path,
    _descriptor_root: str,
) -> pathlib.Path:
    directory = home / "python-bootstrap"
    try:
        directory.mkdir(mode=0o700)
        descriptor = os.open(
            directory / "sitecustomize.py",
            os.O_WRONLY
            | os.O_CREAT
            | os.O_EXCL
            | os.O_CLOEXEC
            | os.O_NOFOLLOW,
            0o600,
        )
        try:
            payload = (
                "import os, sys\n"
                "root = os.environ['HYHOME_CI_GATE_ROOT']\n"
                "sys.path[:0] = [root, root + '/scripts/validation']\n"
            ).encode("utf-8")
            _write_all(descriptor, payload)
            os.fsync(descriptor)
        finally:
            _close(descriptor)
    except OSError:
        raise GateContractError(
            "ci-gate-python-bootstrap",
            "python-bootstrap",
            "the isolated Python bootstrap could not be created",
        ) from None
    return directory


def _run_verified_child(
    root_fd: int,
    item: _VerifiedInvocation,
    environment: Mapping[str, str],
) -> int:
    argv = [
        f"/proc/self/fd/{item.entrypoint_fd}",
        *item.invocation.argv,
    ]
    lifecycle = _ProcessLifecycle()
    process: subprocess.Popen[bytes] | None = None
    try:
        process = subprocess.Popen(
            argv,
            cwd=f"/proc/self/fd/{item.cwd_fd}",
            env=dict(environment),
            pass_fds=tuple(
                sorted(
                    {
                        root_fd,
                        item.cwd_fd,
                        item.entrypoint_fd,
                    }
                )
            ),
            shell=False,
            start_new_session=True,
        )
        lifecycle.bind_process(process)
        lifecycle.acquire_pidfd()
        if lifecycle.pidfd is None:
            raise _runner_cleanup_error()
        leader_ready = _pidfd_ready(
            lifecycle.pidfd,
            item.invocation.timeout_seconds,
        )
        timed_out = not leader_ready
        _finalize_process_group(
            process,
            lifecycle.pidfd,
            leader_ready=leader_ready,
        )
        lifecycle.mark_group_finalized()
        returncode = _bounded_reap(process, lifecycle)
        _close_pidfd_once(lifecycle)
        return 124 if timed_out else returncode
    except BaseException as error:
        _recover_process_lifecycle(
            item.invocation.gate_id,
            process,
            lifecycle,
            error,
        )
        raise AssertionError("process lifecycle recovery must raise")


def _finalize_process_group(
    process: subprocess.Popen[bytes],
    pidfd: int,
    *,
    leader_ready: bool,
) -> None:
    pgid = process.pid
    _signal_process_group(pgid, signal.SIGTERM)
    if not leader_ready:
        leader_ready = _pidfd_ready(
            pidfd,
            _TERMINATION_GRACE_SECONDS,
        )
    members = (
        _same_pgid_members(pgid, process.pid)
        if leader_ready
        else ()
    )
    if not leader_ready or members:
        _signal_process_group(pgid, signal.SIGKILL)
        if not leader_ready:
            leader_ready = _pidfd_ready(
                pidfd,
                _TERMINATION_GRACE_SECONDS,
            )
        if not leader_ready:
            raise GateContractError(
                "ci-gate-runner-pidfd-readiness",
                "pidfd",
                "the adapter leader did not become ready",
            )
        if not _wait_for_nonleader_absence(pgid, process.pid):
            raise GateContractError(
                "ci-gate-runner-proc-members",
                "proc",
                "the adapter process group retained members",
            )


def _recover_process_lifecycle(
    gate_id: str,
    process: subprocess.Popen[bytes] | None,
    lifecycle: _ProcessLifecycle,
    product_error: BaseException,
) -> None:
    if process is None:
        if isinstance(product_error, OSError):
            raise GateContractError(
                "ci-gate-child-exec",
                gate_id,
                "the verified gate could not be executed",
            ) from None
        raise product_error

    if lifecycle.reap_started:
        _finish_post_reap_cleanup(lifecycle)
        raise _runner_cleanup_error()

    if lifecycle.pidfd_acquired:
        cleanup_failed = _recover_with_pidfd(process, lifecycle)
    else:
        cleanup_failed = _recover_without_pidfd(process, lifecycle)
    if cleanup_failed:
        raise _runner_cleanup_error()
    if isinstance(product_error, GateContractError):
        raise product_error
    if not lifecycle.pidfd_acquired and isinstance(product_error, OSError):
        raise GateContractError(
            "ci-gate-runner-pidfd-acquisition",
            "pidfd",
            "the adapter leader identity could not be acquired",
        )
    if isinstance(product_error, Exception):
        raise _runner_cleanup_error()
    raise product_error


def _recover_without_pidfd(
    process: subprocess.Popen[bytes],
    lifecycle: _ProcessLifecycle,
) -> bool:
    cleanup_failed = False
    try:
        _signal_process_group(process.pid, signal.SIGKILL)
    except BaseException:
        cleanup_failed = True
    try:
        _bounded_reap(process, lifecycle)
    except BaseException:
        cleanup_failed = True
    return cleanup_failed


def _recover_with_pidfd(
    process: subprocess.Popen[bytes],
    lifecycle: _ProcessLifecycle,
) -> bool:
    cleanup_failed = False
    leader_ready = lifecycle.group_finalized
    if not lifecycle.group_finalized:
        try:
            _signal_process_group(process.pid, signal.SIGKILL)
        except BaseException:
            cleanup_failed = True
        try:
            if lifecycle.pidfd is None:
                raise _runner_cleanup_error()
            leader_ready = _pidfd_ready(
                lifecycle.pidfd,
                _TERMINATION_GRACE_SECONDS,
            )
        except BaseException:
            cleanup_failed = True
    if not leader_ready:
        cleanup_failed = True
    else:
        try:
            _bounded_reap(process, lifecycle)
        except BaseException:
            cleanup_failed = True
    if not lifecycle.pidfd_close_attempted:
        try:
            _close_pidfd_once(lifecycle)
        except BaseException:
            cleanup_failed = True
    return cleanup_failed


def _finish_post_reap_cleanup(
    lifecycle: _ProcessLifecycle,
) -> None:
    if not lifecycle.pidfd_acquired or lifecycle.pidfd_close_attempted:
        return
    try:
        _close_pidfd_once(lifecycle)
    except BaseException:
        pass


def _bounded_reap(
    process: subprocess.Popen[bytes],
    lifecycle: _ProcessLifecycle,
) -> int:
    if lifecycle.reap_started:
        raise _runner_cleanup_error()
    lifecycle.mark_reap_started()
    return int(process.wait(timeout=_TERMINATION_GRACE_SECONDS))


def _close_pidfd_once(lifecycle: _ProcessLifecycle) -> None:
    if (
        not lifecycle.pidfd_acquired
        or lifecycle.pidfd is None
        or lifecycle.pidfd_close_attempted
    ):
        raise _runner_cleanup_error()
    lifecycle.mark_pidfd_close_attempted()
    os.close(lifecycle.pidfd)


def _signal_process_group(pgid: int, signum: int) -> None:
    try:
        os.killpg(pgid, signum)
    except OSError as error:
        if isinstance(error, ProcessLookupError) or error.errno == errno.ESRCH:
            return
        raise GateContractError(
            "ci-gate-runner-signal",
            "process-group",
            "the adapter process group could not be signaled",
        ) from None


def _pidfd_ready(pidfd: int, timeout_seconds: float) -> bool:
    deadline = time.monotonic() + max(0.0, timeout_seconds)
    poller = select.poll()
    try:
        poller.register(pidfd, select.POLLIN)
    except (OSError, ValueError):
        raise GateContractError(
            "ci-gate-runner-pidfd-readiness",
            "pidfd",
            "the adapter leader readiness could not be observed",
        ) from None
    while True:
        try:
            remaining = max(0.0, deadline - time.monotonic())
            timeout_ms = min(
                2_147_483_647,
                max(0, int(remaining * 1000)),
            )
            events = poller.poll(timeout_ms)
        except OSError as error:
            if error.errno == errno.EINTR and time.monotonic() < deadline:
                continue
            raise GateContractError(
                "ci-gate-runner-pidfd-readiness",
                "pidfd",
                "the adapter leader readiness could not be observed",
            ) from None
        if events:
            for descriptor, event in events:
                if descriptor != pidfd or event & (
                    select.POLLERR | select.POLLNVAL
                ):
                    raise GateContractError(
                        "ci-gate-runner-pidfd-readiness",
                        "pidfd",
                        "the adapter leader readiness could not be observed",
                    )
                if event & select.POLLIN:
                    return True
            raise GateContractError(
                "ci-gate-runner-pidfd-readiness",
                "pidfd",
                "the adapter leader readiness could not be observed",
            )
        if time.monotonic() >= deadline:
            return False


def _wait_for_nonleader_absence(
    pgid: int,
    leader_pid: int,
) -> bool:
    deadline = time.monotonic() + _TERMINATION_GRACE_SECONDS
    while True:
        if not _same_pgid_members(pgid, leader_pid):
            return True
        if time.monotonic() >= deadline:
            return False
        time.sleep(0.01)


def _same_pgid_members(
    pgid: int,
    leader_pid: int,
    *,
    proc_root: pathlib.Path = _PROC_ROOT,
) -> tuple[int, ...]:
    proc_fd = -1
    product_error: BaseException | None = None
    members: list[int] = []
    try:
        proc_fd = os.open(
            proc_root,
            os.O_RDONLY
            | os.O_CLOEXEC
            | os.O_NOFOLLOW
            | os.O_DIRECTORY,
        )
        try:
            numeric_names: list[str] = []
            with os.scandir(proc_fd) as entries:
                for entry in entries:
                    name = entry.name
                    if (
                        not name
                        or not name.isascii()
                        or any(
                            character < "0" or character > "9"
                            for character in name
                        )
                    ):
                        continue
                    numeric_names.append(name)
                    if len(numeric_names) > _MAX_PROC_PID_ENTRIES:
                        raise _proc_scan_error()
        except OSError:
            raise _proc_scan_error() from None
        numeric_entries: list[tuple[int, str]] = []
        for name in numeric_names:
            if len(name) > 20:
                raise _proc_scan_error()
            try:
                pid = int(name, 10)
            except ValueError:
                raise _proc_scan_error() from None
            numeric_entries.append((pid, name))
        numeric_entries.sort()
        for pid, name in numeric_entries:
            if pid == leader_pid:
                continue
            member_pgid = _read_proc_entry_pgid(proc_fd, name, pid)
            if member_pgid == pgid:
                members.append(pid)
    except GateContractError as error:
        product_error = error
    except OSError:
        product_error = _proc_scan_error()
    except BaseException as error:
        product_error = error
    finally:
        cleanup_failed = False
        if proc_fd >= 0:
            try:
                os.close(proc_fd)
            except BaseException:
                cleanup_failed = True
    if cleanup_failed:
        raise _runner_cleanup_error()
    if product_error is not None:
        raise product_error
    return tuple(members)


def _read_proc_entry_pgid(
    proc_fd: int,
    name: str,
    pid: int,
) -> int | None:
    pid_fd = -1
    stat_fd = -1
    vanished = False
    entry_error: GateContractError | None = None
    product_error: BaseException | None = None
    cleanup_failed = False
    pgrp: int | None = None
    try:
        try:
            pid_fd = os.open(
                name,
                os.O_RDONLY
                | os.O_CLOEXEC
                | os.O_NOFOLLOW
                | os.O_DIRECTORY,
                dir_fd=proc_fd,
            )
        except OSError as error:
            if error.errno in {errno.ENOENT, errno.ESRCH}:
                vanished = True
            else:
                entry_error = _proc_scan_error()
        if not vanished and entry_error is None:
            try:
                stat_fd = os.open(
                    "stat",
                    os.O_RDONLY
                    | os.O_CLOEXEC
                    | os.O_NOFOLLOW
                    | os.O_NONBLOCK,
                    dir_fd=pid_fd,
                )
            except OSError as error:
                if error.errno in {errno.ENOENT, errno.ESRCH}:
                    vanished = True
                else:
                    entry_error = _proc_scan_error()
        if not vanished and entry_error is None:
            try:
                payload = _read_proc_stat(stat_fd)
            except OSError as error:
                if error.errno in {errno.ENOENT, errno.ESRCH}:
                    vanished = True
                else:
                    entry_error = _proc_scan_error()
            else:
                try:
                    pgrp = _parse_proc_stat_pgid(payload, pid)
                except ValueError:
                    entry_error = _proc_scan_error()
    except BaseException as error:
        product_error = error
    finally:
        for descriptor in (stat_fd, pid_fd):
            if descriptor < 0:
                continue
            try:
                os.close(descriptor)
            except BaseException:
                cleanup_failed = True
    if cleanup_failed:
        raise _runner_cleanup_error()
    if product_error is not None:
        raise product_error
    if entry_error is not None:
        raise entry_error
    return None if vanished else pgrp


def _read_proc_stat(descriptor: int) -> bytes:
    payload = bytearray()
    while len(payload) <= _MAX_PROC_STAT_BYTES:
        chunk = os.read(
            descriptor,
            _MAX_PROC_STAT_BYTES + 1 - len(payload),
        )
        if not chunk:
            return bytes(payload)
        payload.extend(chunk)
        if len(payload) > _MAX_PROC_STAT_BYTES:
            raise OSError(errno.EFBIG, "proc stat too large")
    raise OSError(errno.EFBIG, "proc stat too large")


def _parse_proc_stat_pgid(payload: bytes, pid: int) -> int:
    if len(payload) > _MAX_PROC_STAT_BYTES or b"\0" in payload:
        raise ValueError
    line = payload[:-1] if payload.endswith(b"\n") else payload
    if not line or b"\n" in line:
        raise ValueError
    prefix = f"{pid} (".encode("ascii")
    if not line.startswith(prefix):
        raise ValueError
    comm_end = line.rfind(b") ")
    if comm_end < len(prefix):
        raise ValueError
    fields = line[comm_end + 2 :].split()
    if (
        len(fields) < 3
        or len(fields[0]) != 1
        or not fields[1].isdigit()
        or not fields[2].isdigit()
    ):
        raise ValueError
    return int(fields[2], 10)


def _proc_scan_error() -> GateContractError:
    return GateContractError(
        "ci-gate-runner-proc-scan",
        "proc",
        "the process-group membership scan failed",
    )


def _runner_cleanup_error() -> GateContractError:
    return GateContractError(
        "ci-gate-runner-cleanup",
        "process-group",
        "the adapter process group could not be cleaned up",
    )


def _remove_home(home: pathlib.Path) -> None:
    for attempt in range(3):
        try:
            shutil.rmtree(home)
            return
        except OSError:
            if attempt < 2:
                time.sleep(0.05)
    raise GateContractError(
        "ci-gate-home-cleanup",
        "HOME",
        "the isolated gate home could not be removed",
    ) from None


def _write_all(descriptor: int, payload: bytes) -> None:
    view = memoryview(payload)
    while view:
        written = os.write(descriptor, view)
        if written <= 0:
            raise OSError(errno.EIO, "short write")
        view = view[written:]


def _close(descriptor: int) -> None:
    if descriptor < 0:
        return
    try:
        os.close(descriptor)
    except OSError:
        pass
