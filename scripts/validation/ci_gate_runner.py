from __future__ import annotations

import argparse
import collections.abc
import dataclasses
import errno
import os
import pathlib
import re
import shutil
import stat
import subprocess
import sys
import tempfile
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
                    canonical_root,
                    home,
                    item.invocation,
                    item.interpreter,
                    environ,
                )
                try:
                    result = subprocess.run(
                        [
                            f"/proc/self/fd/{item.entrypoint_fd}",
                            *item.invocation.argv,
                        ],
                        cwd=f"/proc/self/fd/{item.cwd_fd}",
                        env=child_environment,
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
                        check=False,
                        timeout=item.invocation.timeout_seconds,
                    )
                except subprocess.TimeoutExpired:
                    return 124
                except OSError as error:
                    raise GateContractError(
                        "ci-gate-child-exec",
                        item.invocation.gate_id,
                        "the verified gate could not be executed",
                    ) from error
                if result.returncode != 0:
                    return result.returncode
            return 0
        finally:
            for item in verified:
                _close(item.entrypoint_fd)
                _close(item.cwd_fd)
            _close(root_fd)
    finally:
        shutil.rmtree(home, ignore_errors=True)


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
    root: pathlib.Path,
    home: pathlib.Path,
    invocation: GateInvocation,
    interpreter: str,
    environ: Mapping[str, str],
) -> dict[str, str]:
    admitted: dict[str, str] = {
        "PATH": environ["PATH"],
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "HOME": str(home),
        "TMPDIR": "/tmp",
        "PYTHONNOUSERSITE": "1",
        "PYTHONSAFEPATH": "1",
        "PIP_DISABLE_PIP_VERSION_CHECK": "1",
        "HYHOME_CI_GATE_ROOT": str(root),
    }
    if interpreter == "python":
        admitted["PYTHONPATH"] = os.pathsep.join(
            (str(root), str(root / "scripts/validation"))
        )
    for key in invocation.allowed_env_keys:
        if _SECRET_ENV_SHAPE.search(key):
            raise GateContractError(
                "ci-gate-environment",
                invocation.gate_id,
                "the gate environment key is not admitted",
            )
        if key in environ:
            admitted[key] = environ[key]
    return admitted


def _close(descriptor: int) -> None:
    if descriptor < 0:
        return
    try:
        os.close(descriptor)
    except OSError:
        pass
