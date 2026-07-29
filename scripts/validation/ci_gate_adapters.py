#!/usr/bin/env python3
from __future__ import annotations

import errno
import os
import pathlib
import re
import stat
import subprocess
import sys
from collections.abc import Mapping


SUBCOMMANDS = (
    "verify-metadata-base",
    "publish-qa-recommendations",
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
_UNITTEST_MODULE = re.compile(r"tests\.validation\.[A-Za-z0-9_.]+\Z")
_FULL_SHA = re.compile(r"[0-9a-f]{40}\Z")
_SECRET_ENV_SHAPE = re.compile(
    r"(?:SECRET|TOKEN|PASSWORD|PASSWD|CREDENTIAL|AUTH|API_KEY|PRIVATE_KEY)",
    re.IGNORECASE,
)
_MAX_CAPTURE_BYTES = 1024 * 1024


class AdapterError(ValueError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


def run_adapter(
    root: pathlib.Path,
    argv: tuple[str, ...],
    environ: Mapping[str, str],
) -> int:
    canonical_root = _canonical_root(root)
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
    if command == "publish-qa-recommendations":
        _no_arguments(arguments)
        return _publish_qa_recommendations(canonical_root, environ)
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
                _UNITTEST_MODULE.fullmatch(module) is None
                for module in arguments[:-1]
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
        else pathlib.Path(__file__).resolve().parents[2]
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
    keyword_arguments: dict[str, object] = {
        "cwd": root,
        "env": dict(environ),
        "shell": False,
        "check": False,
    }
    if stdout is not None:
        keyword_arguments["stdout"] = stdout
        keyword_arguments["stderr"] = subprocess.PIPE
    elif capture_output:
        keyword_arguments["capture_output"] = True
    return subprocess.run(list(argv), **keyword_arguments)  # type: ignore[arg-type]


def _canonical_root(root: pathlib.Path) -> pathlib.Path:
    candidate = pathlib.Path(root)
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
    return candidate


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
        key: value
        for key, value in environ.items()
        if not key.startswith("GIT_")
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


def _publish_qa_recommendations(
    root: pathlib.Path,
    environ: Mapping[str, str],
) -> int:
    summary_value = environ.get("GITHUB_STEP_SUMMARY", "")
    if not summary_value:
        return 0
    summary_path = pathlib.Path(summary_value)
    try:
        descriptor = os.open(
            summary_path,
            os.O_WRONLY | os.O_APPEND | os.O_CLOEXEC | os.O_NOFOLLOW,
        )
        metadata = os.fstat(descriptor)
        if not stat.S_ISREG(metadata.st_mode):
            raise OSError(errno.EINVAL, "not regular")
    except OSError:
        raise AdapterError(
            "ci-gate-adapter-summary",
            "the summary output is unavailable",
        ) from None
    try:
        base = ""
        event = environ.get("EVENT_NAME", "")
        if event == "pull_request":
            candidate = environ.get("PR_BASE_SHA", "")
            if _FULL_SHA.fullmatch(candidate):
                base = candidate
        elif event == "push":
            candidate = environ.get("PUSH_BEFORE_SHA", "")
            if (
                _FULL_SHA.fullmatch(candidate)
                and candidate != "0" * 40
            ):
                base = candidate
        if not base:
            fallback = _run_child(
                ("git", "rev-parse", "--verify", "--quiet", "HEAD~1"),
                root=root,
                environ=_git_environment(environ),
                capture_output=True,
            )
            if fallback.returncode == 0:
                base = "HEAD~1"
        valid_base = False
        if base:
            valid_base = (
                _run_child(
                    (
                        "git",
                        "rev-parse",
                        "--verify",
                        "--quiet",
                        f"{base}^{{commit}}",
                    ),
                    root=root,
                    environ=_git_environment(environ),
                    capture_output=True,
                ).returncode
                == 0
            )
        command = (
            (
                "bash",
                "scripts/validation/recommend-qa-gates.sh",
                "--base",
                base,
            )
            if valid_base
            else (
                "bash",
                "scripts/validation/recommend-qa-gates.sh",
                "--files",
                ".github/workflows/ci-quality.yml",
            )
        )
        result = _run_child(
            command,
            root=root,
            environ=environ,
            capture_output=True,
        )
        if result.returncode != 0:
            return int(result.returncode)
        output = result.stdout or b""
        if len(output) > _MAX_CAPTURE_BYTES or b"\0" in output:
            raise AdapterError(
                "ci-gate-adapter-output",
                "the adapter output is invalid",
            )
        body = (
            b"## QA gate recommendations\n\n```text\n"
            + output.rstrip(b"\n")
            + b"\n```\n"
        )
        os.write(descriptor, body)
        return 0
    finally:
        os.close(descriptor)


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
            or (
                path.startswith(".claude/hooks/")
                and path.endswith(".sh")
            )
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
    sys.stdout.write(output.decode("utf-8", errors="strict"))
    return 0


def _npm_arguments(arguments: tuple[str, ...]) -> tuple[str, ...]:
    admitted = {
        ("audit", "--audit-level=high", *_NPM_PREFIX),
        ("ci", *_NPM_PREFIX),
        *{
            ("run", script, *_NPM_PREFIX)
            for script in _NPM_SCRIPTS
        },
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
    if title_pattern.fullmatch(title) is None or branch_pattern.fullmatch(branch) is None:
        raise AdapterError(
            "ci-gate-adapter-git-flow",
            "the pull request identity does not match policy",
        )


def _prepare_compose_env(
    root: pathlib.Path,
    environ: Mapping[str, str],
) -> None:
    root_fd = _open_root(root)
    source_fd = -1
    destination_fd = -1
    created = False
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
        if not stat.S_ISREG(os.fstat(source_fd).st_mode):
            raise AdapterError(
                "ci-gate-adapter-compose-source",
                "the compose example source is invalid",
            )
        if not _tracked_regular_source(root, environ):
            raise AdapterError(
                "ci-gate-adapter-compose-source",
                "the compose example source is invalid",
            )
        try:
            destination_fd = os.open(
                ".env",
                os.O_WRONLY
                | os.O_CREAT
                | os.O_EXCL
                | os.O_CLOEXEC
                | os.O_NOFOLLOW,
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
        while True:
            chunk = os.read(source_fd, 65536)
            if not chunk:
                break
            view = memoryview(chunk)
            while view:
                written = os.write(destination_fd, view)
                view = view[written:]
        os.fsync(destination_fd)
    except BaseException:
        if created:
            try:
                os.unlink(".env", dir_fd=root_fd)
            except OSError:
                pass
        raise
    finally:
        for descriptor in (destination_fd, source_fd, root_fd):
            if descriptor >= 0:
                try:
                    os.close(descriptor)
                except OSError:
                    pass


def _tracked_regular_source(
    root: pathlib.Path,
    environ: Mapping[str, str],
) -> bool:
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
        return False
    records = (result.stdout or b"").rstrip(b"\0").split(b"\0")
    if len(records) != 1:
        return False
    try:
        metadata, path = records[0].split(b"\t", 1)
        mode, _object_id, stage = metadata.decode("ascii").split(" ")
    except (UnicodeDecodeError, ValueError):
        return False
    return mode in {"100644", "100755"} and stage == "0" and path == b".env.example"


def _run_zizmor_sarif(
    root: pathlib.Path,
    environ: Mapping[str, str],
) -> int:
    root_fd = _open_root(root)
    output_fd = -1
    created = False
    try:
        try:
            output_fd = os.open(
                "results.sarif",
                os.O_WRONLY
                | os.O_CREAT
                | os.O_EXCL
                | os.O_CLOEXEC
                | os.O_NOFOLLOW,
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
        if result.returncode != 0:
            os.close(output_fd)
            output_fd = -1
            os.unlink("results.sarif", dir_fd=root_fd)
            created = False
        return int(result.returncode)
    finally:
        if output_fd >= 0:
            os.close(output_fd)
        os.close(root_fd)
        if created:
            pass


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


if __name__ == "__main__":
    raise SystemExit(main())
