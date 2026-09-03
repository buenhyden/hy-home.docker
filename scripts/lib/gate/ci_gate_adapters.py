#!/usr/bin/env python3
from __future__ import annotations

import errno
import fcntl
import os
import pathlib
import re
from types import MappingProxyType
import stat
import subprocess
import sys
import threading
import time
from collections.abc import Mapping


SUBCOMMANDS = (
    "verify-metadata-base",
    "check-diff-hygiene",
    "check-shell-syntax",
    "install-python-requirements",
    "run-unittest",
    "run-agent-output-eval",
    "run-npm",
    "check-git-flow",
    "prepare-compose-env",
    "install-playwright",
    "run-zizmor-sarif",
)
_REQUIREMENT_PATHS = {
    "scripts/requirements.txt",
    "scripts/requirements-pre-commit.txt",
}
_NPM_PREFIX = ("--prefix", "projects/storybook/nextjs")
_NPM_SCRIPTS = {"lint", "typecheck", "build", "build-storybook", "coverage"}
# The structural boundary admits only the two authoritative test roots and
# valid nonempty dotted segments. Exact complete argv admission remains owned
# by the runner, so this grammar does not duplicate the library-domain list.
# A `test_` segment is required, so a bare package name is rejected: it is
# shape-valid but runs no tests, and admitting one would let a batch shrink
# silently. Trailing class or method selectors stay admitted; the full-profile
# coverage test compares module strings, so a narrowed selector fails there.
_UNITTEST_MODULE = re.compile(
    r"(?:tests\.validation|tests\.lib)(?:\.[A-Za-z_][A-Za-z0-9_]*)*"
    r"\.test_[A-Za-z0-9_]+(?:\.[A-Za-z_][A-Za-z0-9_]*)*\Z"
)
_FULL_SHA = re.compile(r"[0-9a-f]{40}\Z")
_GIT_OBJECT_ID = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})\Z")
_SECRET_ENV_SHAPE = re.compile(
    r"(?:SECRET|TOKEN|PASSWORD|PASSWD|CREDENTIAL|AUTH|API_KEY|PRIVATE_KEY)",
    re.IGNORECASE,
)
_MAX_CAPTURE_BYTES = 1024 * 1024
_PROC_FD_ROOT = re.compile(r"/proc/self/fd/([0-9]+)\Z")
_CHILD_TERMINATION_SECONDS = 0.25
_CLEANUP_ERROR_CODES = frozenset(
    {
        "ci-gate-adapter-compose-cleanup",
        "ci-gate-adapter-sarif-cleanup",
    }
)


class AdapterError(ValueError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


class _AdoptedRootCleanupError(Exception):
    def __init__(self, owned_root_fd: int) -> None:
        super().__init__()
        self.owned_root_fd = owned_root_fd


def run_adapter(
    root: pathlib.Path,
    argv: tuple[str, ...],
    environ: Mapping[str, str],
) -> int:
    adoption_cleanup_fd: int | None = None
    try:
        canonical_root, owned_root_fd = _adopt_root(root)
    except _AdoptedRootCleanupError as error:
        adoption_cleanup_fd = error.owned_root_fd
    if adoption_cleanup_fd is not None:
        try:
            os.close(adoption_cleanup_fd)
        except BaseException:
            pass
        raise AdapterError(
            "ci-gate-adapter-root-cleanup",
            "the repository root capability could not be cleaned up",
        ) from None
    result: int | None = None
    product_error: BaseException | None = None
    try:
        child_environment = dict(environ)
        child_environment["HYHOME_CI_GATE_ROOT"] = canonical_root.as_posix()
        result = _dispatch_adapter(canonical_root, argv, child_environment)
    except BaseException as error:
        if isinstance(error, AdapterError):
            product_error = error
        elif isinstance(error, Exception):
            product_error = AdapterError(
                "ci-gate-adapter-operation",
                "the adapter operation is unavailable",
            )
        else:
            product_error = error
    root_cleanup_failed = False
    try:
        os.close(owned_root_fd)
    except BaseException:
        root_cleanup_failed = True
    if root_cleanup_failed:
        if (
            isinstance(product_error, AdapterError)
            and product_error.code in _CLEANUP_ERROR_CODES
        ):
            raise product_error
        raise AdapterError(
            "ci-gate-adapter-root-cleanup",
            "the repository root capability could not be cleaned up",
        ) from None
    if product_error is not None:
        try:
            raise product_error
        finally:
            product_error = None
    assert result is not None
    return result


# Admission grammar. The runner asks this module whether an adapter invocation
# is admitted in an execution context, so the gate no longer repeats every test
# module and command tuple. Test coverage is guaranteed separately, by
# comparing the on-disk test modules with the modules the full profile runs.
_ALL_CONTEXTS = frozenset(
    {"local", "pull_request", "push", "push_initial", "workflow_dispatch"}
)
_CI_CONTEXTS = _ALL_CONTEXTS - {"local"}
ADAPTER_CONTEXTS = MappingProxyType(
    {
        "check-diff-hygiene": _ALL_CONTEXTS,
        "check-shell-syntax": _ALL_CONTEXTS,
        "run-agent-output-eval": _ALL_CONTEXTS,
        "run-unittest": _ALL_CONTEXTS,
        "verify-metadata-base": frozenset({"pull_request", "push"}),
        "check-git-flow": frozenset({"pull_request"}),
        "install-playwright": _CI_CONTEXTS,
        "run-npm": _CI_CONTEXTS,
        "run-zizmor-sarif": _CI_CONTEXTS,
        # Workflow setup steps, never admitted as gate leaves.
        "install-python-requirements": frozenset(),
        "prepare-compose-env": frozenset(),
    }
)
_NPM_ARGUMENT_SHAPES = frozenset(
    {("audit", "--audit-level=high"), ("ci",)}
    | {("run", script) for script in _NPM_SCRIPTS}
)


def validate_adapter_argv(argv: tuple[str, ...]) -> None:
    """Raise unless argv is a bounded, well-shaped adapter invocation."""

    if not argv or argv[0] not in SUBCOMMANDS:
        raise AdapterError(
            "ci-gate-adapter-command", "the adapter subcommand is not admitted"
        )
    command, arguments = argv[0], argv[1:]
    if command == "run-unittest":
        if len(arguments) < 2 or arguments[-1] != "-v":
            _argument_error()
        modules = arguments[:-1]
        if len(modules) != len(set(modules)):
            _argument_error()
        for module in modules:
            if not _UNITTEST_MODULE.match(module):
                _argument_error()
        return
    if command == "run-npm":
        if arguments[-len(_NPM_PREFIX) :] != _NPM_PREFIX:
            _argument_error()
        if arguments[: -len(_NPM_PREFIX)] not in _NPM_ARGUMENT_SHAPES:
            _argument_error()
        return
    if command == "install-python-requirements":
        if len(arguments) != 1 or arguments[0] not in _REQUIREMENT_PATHS:
            _argument_error()
        return
    if arguments:
        _argument_error()


def admits_adapter_invocation(argv: tuple[str, ...], context: str) -> bool:
    """Return whether this adapter invocation is admitted in `context`."""

    try:
        validate_adapter_argv(argv)
    except AdapterError:
        return False
    return context in ADAPTER_CONTEXTS.get(argv[0], frozenset())


def _dispatch_adapter(
    canonical_root: pathlib.Path,
    argv: tuple[str, ...],
    environ: Mapping[str, str],
) -> int:
    _validate_environment(environ)
    if not argv or argv[0] not in SUBCOMMANDS:
        raise AdapterError(
            "ci-gate-adapter-command",
            "the adapter subcommand is not admitted",
        )
    command, arguments = argv[0], argv[1:]
    if command == "verify-metadata-base":
        _no_arguments(arguments)
        return _verify_metadata_base(canonical_root, environ)
    if command == "check-diff-hygiene":
        _no_arguments(arguments)
        return _returncode(
            _run_child(
                ("git", "diff", "--check"),
                root=canonical_root,
                environ=_git_environment(environ),
            )
        )
    if command == "check-shell-syntax":
        _no_arguments(arguments)
        return _check_shell_syntax(canonical_root, environ)
    if command == "install-python-requirements":
        if len(arguments) != 1 or arguments[0] not in _REQUIREMENT_PATHS:
            _argument_error()
        return _returncode(
            _run_child(
                (
                    "python3",
                    "-m",
                    "pip",
                    "install",
                    "-r",
                    arguments[0],
                ),
                root=canonical_root,
                environ=environ,
            )
        )
    if command == "run-unittest":
        if (
            len(arguments) < 2
            or arguments[-1] != "-v"
            or any(
                _UNITTEST_MODULE.fullmatch(module) is None for module in arguments[:-1]
            )
        ):
            _argument_error()
        return _returncode(
            _run_child(
                ("python3", "-m", "unittest", *arguments),
                root=canonical_root,
                environ=environ,
            )
        )
    if command == "run-agent-output-eval":
        _no_arguments(arguments)
        return _run_agent_output_eval(canonical_root, environ)
    if command == "run-npm":
        npm_arguments = _npm_arguments(arguments)
        return _returncode(
            _run_child(
                ("npm", *npm_arguments),
                root=canonical_root,
                environ=environ,
            )
        )
    if command == "check-git-flow":
        _no_arguments(arguments)
        _check_git_flow(environ)
        return 0
    if command == "prepare-compose-env":
        _no_arguments(arguments)
        _prepare_compose_env(canonical_root, environ)
        return 0
    if command == "install-playwright":
        _no_arguments(arguments)
        return _returncode(
            _run_child(
                (
                    "npx",
                    "--prefix",
                    "projects/storybook/nextjs",
                    "playwright",
                    "install",
                    "chromium",
                    "--with-deps",
                ),
                root=canonical_root,
                environ=environ,
            )
        )
    if command == "run-zizmor-sarif":
        _no_arguments(arguments)
        return _run_zizmor_sarif(canonical_root, environ)
    raise AssertionError("closed adapter dispatch is incomplete")


def main(argv: list[str] | None = None) -> int:
    arguments = tuple(sys.argv[1:] if argv is None else argv)
    root_value = os.environ.get("HYHOME_CI_GATE_ROOT")
    root = (
        pathlib.Path(root_value)
        if root_value
        else pathlib.Path(__file__).resolve().parents[3]
    )
    try:
        return run_adapter(root, arguments, os.environ)
    except AdapterError as error:
        print(f"FAIL [{error.code}]: {error.message}", file=sys.stderr)
        return 2


def _run_child(
    argv: tuple[str, ...],
    *,
    root: pathlib.Path,
    environ: Mapping[str, str],
    capture_output: bool = False,
    stdout: int | None = None,
) -> subprocess.CompletedProcess[bytes]:
    pass_fds = _root_pass_fds(root)
    if not capture_output and stdout is None:
        try:
            return subprocess.run(
                list(argv),
                cwd=root,
                env=dict(environ),
                shell=False,
                check=False,
                pass_fds=pass_fds,
            )
        except OSError:
            raise AdapterError(
                "ci-gate-adapter-child-exec",
                "the child process is unavailable",
            ) from None
    keyword_arguments: dict[str, object] = {
        "cwd": root,
        "env": dict(environ),
        "shell": False,
        "stdout": subprocess.PIPE,
        "stderr": subprocess.PIPE,
        "pass_fds": pass_fds,
    }
    try:
        process = subprocess.Popen(  # type: ignore[arg-type]
            list(argv),
            **keyword_arguments,
        )
    except OSError:
        raise AdapterError(
            "ci-gate-adapter-child-exec",
            "the child process is unavailable",
        ) from None
    streams = {
        "stdout": process.stdout,
        "stderr": process.stderr,
    }
    captured = {"stdout": bytearray(), "stderr": bytearray()}
    overflow = threading.Event()
    read_error = threading.Event()

    def drain(name: str) -> None:
        stream = streams[name]
        if stream is None:
            return
        try:
            while True:
                chunk = os.read(stream.fileno(), 65536)
                if not chunk:
                    return
                if len(captured[name]) + len(chunk) > _MAX_CAPTURE_BYTES:
                    overflow.set()
                    return
                captured[name].extend(chunk)
        except OSError:
            read_error.set()

    readers = tuple(
        threading.Thread(
            target=drain,
            args=(name,),
            daemon=True,
        )
        for name in streams
    )
    try:
        for reader in readers:
            reader.start()
        while process.poll() is None:
            if overflow.is_set() or read_error.is_set():
                _terminate_child(process)
                break
            time.sleep(0.01)
        for reader in readers:
            reader.join(timeout=_CHILD_TERMINATION_SECONDS)
        if any(reader.is_alive() for reader in readers):
            _terminate_child(process)
            raise AdapterError(
                "ci-gate-adapter-output",
                "the adapter output is invalid",
            )
        if overflow.is_set():
            raise AdapterError(
                "ci-gate-adapter-output",
                "the adapter output is invalid",
            )
        if read_error.is_set():
            raise AdapterError(
                "ci-gate-adapter-child-exec",
                "the child process is unavailable",
            )
        returncode = process.wait()
        stdout_payload = bytes(captured["stdout"])
        stderr_payload = bytes(captured["stderr"])
        if stdout is not None:
            try:
                _write_all(stdout, stdout_payload)
            except OSError:
                raise AdapterError(
                    "ci-gate-adapter-output",
                    "the adapter output is unavailable",
                ) from None
        return subprocess.CompletedProcess(
            argv,
            returncode,
            stdout_payload,
            stderr_payload,
        )
    except OSError:
        _terminate_child(process)
        raise AdapterError(
            "ci-gate-adapter-child-exec",
            "the child process is unavailable",
        ) from None
    finally:
        for stream in streams.values():
            if stream is not None:
                stream.close()


def _terminate_child(process: subprocess.Popen[bytes]) -> None:
    if process.poll() is not None:
        return
    try:
        process.terminate()
    except ProcessLookupError:
        return
    try:
        process.wait(timeout=_CHILD_TERMINATION_SECONDS)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()


def _adopt_root(root: pathlib.Path) -> tuple[pathlib.Path, int]:
    candidate = pathlib.Path(root)
    match = _PROC_FD_ROOT.fullmatch(candidate.as_posix())
    if match is not None:
        inherited_fd = int(match.group(1))
        try:
            metadata = os.fstat(inherited_fd)
        except (OSError, ValueError):
            raise AdapterError(
                "ci-gate-adapter-root",
                "the repository root descriptor is unavailable",
            ) from None
        if not stat.S_ISDIR(metadata.st_mode):
            raise AdapterError(
                "ci-gate-adapter-root",
                "the repository root descriptor is invalid",
            )
        try:
            owned_fd = fcntl.fcntl(
                inherited_fd,
                fcntl.F_DUPFD_CLOEXEC,
                3,
            )
        except OSError:
            raise AdapterError(
                "ci-gate-adapter-root",
                "the repository root descriptor is unavailable",
            ) from None
        inherited_cleanup_failed = False
        try:
            os.close(inherited_fd)
        except BaseException:
            inherited_cleanup_failed = True
        if inherited_cleanup_failed:
            raise _AdoptedRootCleanupError(owned_fd) from None
        return pathlib.Path(f"/proc/self/fd/{owned_fd}"), owned_fd
    try:
        resolved = candidate.resolve(strict=True)
    except OSError:
        raise AdapterError(
            "ci-gate-adapter-root",
            "the repository root is unavailable",
        ) from None
    if (
        not candidate.is_absolute()
        or resolved != candidate
        or candidate.is_symlink()
        or not candidate.is_dir()
    ):
        raise AdapterError(
            "ci-gate-adapter-root",
            "the repository root must be canonical",
        )
    owned_fd = _open_root(candidate)
    return pathlib.Path(f"/proc/self/fd/{owned_fd}"), owned_fd


def _root_pass_fds(root: pathlib.Path) -> tuple[int, ...]:
    match = _PROC_FD_ROOT.fullmatch(pathlib.Path(root).as_posix())
    if match is None:
        return ()
    descriptor = int(match.group(1))
    try:
        metadata = os.fstat(descriptor)
    except OSError:
        raise AdapterError(
            "ci-gate-adapter-root",
            "the repository root descriptor is unavailable",
        ) from None
    if not stat.S_ISDIR(metadata.st_mode):
        raise AdapterError(
            "ci-gate-adapter-root",
            "the repository root descriptor is invalid",
        )
    return (descriptor,)


def _owned_root_descriptor(root: pathlib.Path) -> int:
    descriptors = _root_pass_fds(root)
    if len(descriptors) != 1:
        raise AdapterError(
            "ci-gate-adapter-root",
            "the repository root descriptor is unavailable",
        )
    return descriptors[0]


def _validate_environment(environ: Mapping[str, str]) -> None:
    if not environ.get("PATH"):
        raise AdapterError(
            "ci-gate-adapter-environment",
            "the adapter environment is not admitted",
        )
    if any(_SECRET_ENV_SHAPE.search(key) for key in environ):
        raise AdapterError(
            "ci-gate-adapter-environment",
            "the adapter environment is not admitted",
        )


def _git_environment(environ: Mapping[str, str]) -> dict[str, str]:
    result = {
        key: value for key, value in environ.items() if not key.startswith("GIT_")
    }
    result["GIT_CONFIG_NOSYSTEM"] = "1"
    result["GIT_CONFIG_GLOBAL"] = "/dev/null"
    return result


def _no_arguments(arguments: tuple[str, ...]) -> None:
    if arguments:
        _argument_error()


def _argument_error() -> None:
    raise AdapterError(
        "ci-gate-adapter-arguments",
        "the adapter arguments do not match the closed grammar",
    )


def _returncode(result: subprocess.CompletedProcess[bytes]) -> int:
    return int(result.returncode)


def _verify_metadata_base(
    root: pathlib.Path,
    environ: Mapping[str, str],
) -> int:
    base = environ.get("TEMPLATE_GATE_BASE", "")
    if _FULL_SHA.fullmatch(base) is None:
        raise AdapterError(
            "ci-gate-adapter-metadata-base",
            "the metadata comparison base is invalid",
        )
    git_environment = _git_environment(environ)
    first = _run_child(
        ("git", "cat-file", "-e", f"{base}^{{commit}}"),
        root=root,
        environ=git_environment,
    )
    if first.returncode != 0:
        return int(first.returncode)
    return _returncode(
        _run_child(
            ("git", "merge-base", "HEAD", base),
            root=root,
            environ=git_environment,
        )
    )


def _check_shell_syntax(
    root: pathlib.Path,
    environ: Mapping[str, str],
) -> int:
    result = _run_child(
        (
            "git",
            "ls-files",
            "-z",
            "--",
            "scripts/**/*.sh",
            ".claude/hooks/*.sh",
        ),
        root=root,
        environ=_git_environment(environ),
        capture_output=True,
    )
    if result.returncode != 0:
        return int(result.returncode)
    payload = result.stdout or b""
    if len(payload) > _MAX_CAPTURE_BYTES:
        raise AdapterError(
            "ci-gate-adapter-output",
            "the tracked shell path list is invalid",
        )
    try:
        paths = tuple(
            item.decode("utf-8", errors="strict")
            for item in payload.rstrip(b"\0").split(b"\0")
            if item
        )
    except UnicodeDecodeError:
        raise AdapterError(
            "ci-gate-adapter-output",
            "the tracked shell path list is invalid",
        ) from None
    if any(
        pathlib.PurePosixPath(path).is_absolute()
        or ".." in pathlib.PurePosixPath(path).parts
        or not (
            (path.startswith("scripts/") and path.endswith(".sh"))
            or (path.startswith(".claude/hooks/") and path.endswith(".sh"))
        )
        for path in paths
    ):
        raise AdapterError(
            "ci-gate-adapter-output",
            "the tracked shell path list is invalid",
        )
    if not paths:
        return 0
    return _returncode(
        _run_child(
            ("bash", "-n", *paths),
            root=root,
            environ=environ,
        )
    )


def _run_agent_output_eval(
    root: pathlib.Path,
    environ: Mapping[str, str],
) -> int:
    result = _run_child(
        (
            "bash",
            "scripts/validation/run-agent-output-eval-fixtures.sh",
            "--check-fixtures",
            "--check-regressions",
        ),
        root=root,
        environ=environ,
        capture_output=True,
    )
    if result.returncode != 0:
        return int(result.returncode)
    output = result.stdout or b""
    if (
        len(output) > _MAX_CAPTURE_BYTES
        or b"\0" in output
        or b"fixtures_check=pass" not in output.splitlines()
        or b"regressions_check=pass" not in output.splitlines()
    ):
        raise AdapterError(
            "ci-gate-adapter-eval-output",
            "the eval output markers are incomplete",
        )
    try:
        rendered = output.decode("utf-8", errors="strict")
    except UnicodeDecodeError:
        raise AdapterError(
            "ci-gate-adapter-eval-output",
            "the eval output markers are incomplete",
        ) from None
    sys.stdout.write(rendered)
    return 0


def _npm_arguments(arguments: tuple[str, ...]) -> tuple[str, ...]:
    admitted = {
        ("audit", "--audit-level=high", *_NPM_PREFIX),
        ("ci", *_NPM_PREFIX),
        *{("run", script, *_NPM_PREFIX) for script in _NPM_SCRIPTS},
    }
    if arguments not in admitted:
        _argument_error()
    return arguments


def _check_git_flow(environ: Mapping[str, str]) -> None:
    title = environ.get("PR_TITLE", "")
    branch = environ.get("HEAD_REF", "")
    title_pattern = re.compile(
        r"(?:feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)"
        r"(?:\([A-Za-z0-9._-]+\))?!?: .+\Z"
    )
    branch_pattern = re.compile(
        r"(?:(?:feat|fix|hotfix)/[A-Za-z0-9._-]+-.+|"
        r"(?:docs|style|refactor|perf|test|build|ci|chore|revert)/.+|"
        r"(?:dependabot|codex)/.+)\Z"
    )
    if (
        title_pattern.fullmatch(title) is None
        or branch_pattern.fullmatch(branch) is None
    ):
        raise AdapterError(
            "ci-gate-adapter-git-flow",
            "the pull request identity does not match policy",
        )


def _prepare_compose_env(
    root: pathlib.Path,
    environ: Mapping[str, str],
) -> None:
    root_fd = _owned_root_descriptor(root)
    source_fd = -1
    destination_fd = -1
    created = False
    product_error: BaseException | None = None
    try:
        try:
            source_fd = os.open(
                ".env.example",
                os.O_RDONLY | os.O_CLOEXEC | os.O_NOFOLLOW,
                dir_fd=root_fd,
            )
        except OSError:
            raise AdapterError(
                "ci-gate-adapter-compose-source",
                "the compose example source is invalid",
            ) from None
        try:
            source_metadata = os.fstat(source_fd)
        except OSError:
            raise AdapterError(
                "ci-gate-adapter-compose-source",
                "the compose example source is invalid",
            ) from None
        if (
            not stat.S_ISREG(source_metadata.st_mode)
            or source_metadata.st_size > _MAX_CAPTURE_BYTES
        ):
            raise AdapterError(
                "ci-gate-adapter-compose-source",
                "the compose example source is invalid",
            )
        provenance = _tracked_regular_source(root, environ)
        if provenance is None:
            raise AdapterError(
                "ci-gate-adapter-compose-source",
                "the compose example source is invalid",
            )
        try:
            current_metadata = os.stat(
                ".env.example",
                dir_fd=root_fd,
                follow_symlinks=False,
            )
        except OSError:
            raise AdapterError(
                "ci-gate-adapter-compose-source",
                "the compose example source is invalid",
            ) from None
        if (
            current_metadata.st_dev != source_metadata.st_dev
            or current_metadata.st_ino != source_metadata.st_ino
        ):
            raise AdapterError(
                "ci-gate-adapter-compose-source",
                "the compose example source is invalid",
            )
        try:
            payload = _read_bounded(source_fd)
        except OSError:
            raise AdapterError(
                "ci-gate-adapter-compose-source",
                "the compose example source is invalid",
            ) from None
        tracked_blob = _run_child(
            ("git", "cat-file", "blob", provenance),
            root=root,
            environ=_git_environment(environ),
            capture_output=True,
        )
        if tracked_blob.returncode != 0 or tracked_blob.stdout != payload:
            raise AdapterError(
                "ci-gate-adapter-compose-source",
                "the compose example source is invalid",
            )
        try:
            destination_fd = os.open(
                ".env",
                os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC | os.O_NOFOLLOW,
                0o600,
                dir_fd=root_fd,
            )
            created = True
        except OSError as error:
            if error.errno in {errno.EEXIST, errno.ELOOP}:
                raise AdapterError(
                    "ci-gate-adapter-compose-env-exists",
                    "the compose environment destination already exists",
                ) from None
            raise AdapterError(
                "ci-gate-adapter-compose-output",
                "the compose environment destination is unavailable",
            ) from None
        try:
            _write_all(destination_fd, payload)
            os.fsync(destination_fd)
        except OSError:
            raise AdapterError(
                "ci-gate-adapter-compose-output",
                "the compose environment destination is unavailable",
            ) from None
    except BaseException as error:
        product_error = (
            AdapterError(
                "ci-gate-adapter-compose-output",
                "the compose environment destination is unavailable",
            )
            if isinstance(error, OSError)
            else error
        )

    descriptor_cleanup_failed = False
    for descriptor in (destination_fd, source_fd):
        if descriptor < 0:
            continue
        try:
            os.close(descriptor)
        except OSError:
            descriptor_cleanup_failed = True

    unlink_cleanup_failed = False
    if created and (product_error is not None or descriptor_cleanup_failed):
        try:
            os.unlink(".env", dir_fd=root_fd)
        except OSError:
            unlink_cleanup_failed = True

    if descriptor_cleanup_failed or unlink_cleanup_failed:
        raise AdapterError(
            "ci-gate-adapter-compose-cleanup",
            "the compose environment could not be cleaned up",
        ) from None
    if product_error is not None:
        try:
            raise product_error
        finally:
            product_error = None


def _tracked_regular_source(
    root: pathlib.Path,
    environ: Mapping[str, str],
) -> str | None:
    result = _run_child(
        (
            "git",
            "--literal-pathspecs",
            "ls-files",
            "--stage",
            "-z",
            "--error-unmatch",
            "--",
            ".env.example",
        ),
        root=root,
        environ=_git_environment(environ),
        capture_output=True,
    )
    if result.returncode != 0:
        return None
    records = (result.stdout or b"").rstrip(b"\0").split(b"\0")
    if len(records) != 1:
        return None
    try:
        metadata, path = records[0].split(b"\t", 1)
        mode, object_id, stage = metadata.decode("ascii").split(" ")
    except (UnicodeDecodeError, ValueError):
        return None
    if (
        mode not in {"100644", "100755"}
        or stage != "0"
        or path != b".env.example"
        or _GIT_OBJECT_ID.fullmatch(object_id) is None
    ):
        return None
    return object_id


def _run_zizmor_sarif(
    root: pathlib.Path,
    environ: Mapping[str, str],
) -> int:
    root_fd = _owned_root_descriptor(root)
    output_fd = -1
    created = False
    result_code: int | None = None
    product_error: BaseException | None = None
    try:
        try:
            output_fd = os.open(
                "results.sarif",
                os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC | os.O_NOFOLLOW,
                0o600,
                dir_fd=root_fd,
            )
            created = True
        except OSError:
            raise AdapterError(
                "ci-gate-adapter-sarif-output",
                "the SARIF output is unavailable",
            ) from None
        result = _run_child(
            (
                "uvx",
                "--from",
                "zizmor==1.28.0",
                "zizmor",
                ".",
                "--format",
                "sarif",
                ".",
            ),
            root=root,
            environ=environ,
            stdout=output_fd,
        )
        result_code = int(result.returncode)
    except BaseException as error:
        product_error = (
            AdapterError(
                "ci-gate-adapter-sarif-output",
                "the SARIF output is unavailable",
            )
            if isinstance(error, OSError)
            else error
        )

    output_cleanup_failed = False
    if output_fd >= 0:
        try:
            os.close(output_fd)
        except OSError:
            output_cleanup_failed = True

    unlink_cleanup_failed = False
    if created and (
        product_error is not None or result_code != 0 or output_cleanup_failed
    ):
        try:
            os.unlink("results.sarif", dir_fd=root_fd)
        except OSError:
            unlink_cleanup_failed = True

    if output_cleanup_failed or unlink_cleanup_failed:
        raise AdapterError(
            "ci-gate-adapter-sarif-cleanup",
            "the SARIF output could not be cleaned up",
        ) from None
    if product_error is not None:
        try:
            raise product_error
        finally:
            product_error = None
    assert result_code is not None
    return result_code


def _open_root(root: pathlib.Path) -> int:
    try:
        return os.open(
            root,
            os.O_RDONLY | os.O_CLOEXEC | os.O_NOFOLLOW | os.O_DIRECTORY,
        )
    except OSError:
        raise AdapterError(
            "ci-gate-adapter-root",
            "the repository root could not be opened",
        ) from None


def _read_bounded(descriptor: int) -> bytes:
    os.lseek(descriptor, 0, os.SEEK_SET)
    result = bytearray()
    while True:
        chunk = os.read(descriptor, 65536)
        if not chunk:
            return bytes(result)
        result.extend(chunk)
        if len(result) > _MAX_CAPTURE_BYTES:
            raise OSError(errno.EFBIG, "input too large")


def _write_all(descriptor: int, payload: bytes) -> None:
    view = memoryview(payload)
    while view:
        written = os.write(descriptor, view)
        if written <= 0:
            raise OSError(errno.EIO, "short write")
        view = view[written:]


if __name__ == "__main__":
    raise SystemExit(main())
