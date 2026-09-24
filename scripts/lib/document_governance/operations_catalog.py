"""Bounded current-tree validation for Stage 05 Operations."""

from __future__ import annotations

import dataclasses
import datetime as dt
import errno
import json
import os
import pathlib
import posixpath
import re
import selectors
import signal
import stat
import subprocess
import time
from collections import Counter
from collections.abc import Mapping, Sequence

import yaml
from markdown_it import MarkdownIt

from scripts.lib.document_governance.frontmatter import (
    FrontmatterError,
    parse_frontmatter_text,
)
from scripts.lib.document_governance.registry import (
    RegistryError,
    document_type,
    load_registry_document,
    path_matches_pattern,
)
from scripts.lib.document_governance.registry import (
    validate_registry as validate_canonical_registry,
)

REGISTRY_PATH = pathlib.PurePosixPath("docs/99.templates/registry.json")
OPERATIONS_ROOT = pathlib.PurePosixPath("docs/05.operations")
MAX_FILE_BYTES = 10_000_000
MAX_TRACKED_FILES = 10_000
MAX_CATALOG_ENTRIES = 1_000
MAX_DIRECTORY_ENTRIES = 10_000
MAX_OPERATIONS_ROOT_ENTRIES = 16
MAX_DOMAIN_ENTRIES = 512
MAX_SUBJECT_ENTRIES = 8
MAX_INCIDENT_ENTRIES = 512
MAX_INCIDENT_YEAR_ENTRIES = 1_000
MAX_INCIDENT_PACKET_ENTRIES = 4
MAX_GIT_SECONDS = 30.0
MAX_GIT_STDOUT_BYTES = 10_000_000
MAX_GIT_STDERR_BYTES = 1_000_000
MAX_GIT_TOTAL_BYTES = 11_000_000
_DOMAIN = re.compile(r"[0-9]{2}-[a-z0-9][a-z0-9-]*")
_SUBJECT = re.compile(r"(?P<number>[0-9]{4})-(?P<slug>[a-z0-9][a-z0-9-]*)")
_YEAR = re.compile(r"[0-9]{4}")
_INCIDENT = re.compile(r"inc-(?P<number>[0-9]{4})-[a-z0-9][a-z0-9-]*")
_ROLE_FILE = {"guide.md": "guide", "policy.md": "policy", "runbook.md": "runbook"}
_OPERATIONS_PROFILE_IDS = ("guide", "policy", "runbook", "incident", "postmortem")
_ROLE_SECTION_ALIASES = {
    "guide": {
        "Purpose": {"Purpose", "Overview", "Usage"},
        "Audience": {"Audience", "Audience and Prerequisites", "Usage"},
        "Prerequisites": {"Prerequisites", "Audience and Prerequisites", "Usage"},
        "Usage": {"Usage"},
        "Troubleshooting": {"Troubleshooting", "Common Checks", "Runbook Handoff"},
        "Verification": {"Verification", "Common Checks"},
        "Traceability": {"Traceability", "Related Documents"},
    },
    "policy": {
        "Purpose": {"Purpose", "Overview"},
        "Scope": {"Scope", "Policy Scope"},
        "Policy Statements": {"Policy Statements", "Controls"},
        "Enforcement": {"Enforcement", "Controls", "Verification"},
        "Exceptions": {"Exceptions"},
        "Verification": {"Verification"},
        "Traceability": {"Traceability", "Related Documents"},
    },
    "runbook": {
        "Purpose": {"Purpose", "Overview", "When to Use"},
        "Trigger": {"Trigger", "When to Use"},
        "Prerequisites": {"Prerequisites", "When to Use", "Procedure"},
        "Procedure": {"Procedure"},
        "Verification": {
            "Verification",
            "Evidence",
            "Verification Steps",
            "Verification Record",
        },
        "Rollback": {"Rollback", "Rollback or Recovery"},
        "Escalation": {"Escalation"},
        "Traceability": {"Traceability", "Related Documents"},
    },
}
_ACTIVE_ROUTE_PATTERNS = (
    re.compile(r"docs/05\.operations/[^\s`)'\"]+/ops-(?:#{4}|\*|[0-9]{4})(?:[-/])"),
    re.compile(
        r"docs/05\.operations/(?:\{(?:guides[|,]policies[|,]runbooks)(?:[|,]incidents)?\}|guides|policies|runbooks)(?:[/}`]|$)"
    ),
)
_RELEASE_ROLE_PATTERN = re.compile(
    r"(?:(?:guide|policy|runbook|incident|postmortem)(?:\s*,\s*|\s+and\s+)release\b|Release (?:document )?role)",
    re.IGNORECASE,
)
_RELEASE_NEGATIONS = (
    "no release",
    "not maintain",
    "does not maintain",
    "without a release",
    "release absence",
    "release is absent",
    "release role and route are unnecessary",
    "no separate release",
    "remove release",
    "retired release",
    "a separate release document role",
)


class OperationsAuthorityError(ValueError):
    def __init__(self, code: str, message: str) -> None:
        self.code = code
        super().__init__(message)


ManifestError = OperationsAuthorityError


@dataclasses.dataclass(frozen=True, order=True)
class CatalogFinding:
    code: str
    path: str
    message: str


@dataclasses.dataclass(frozen=True)
class GitCommandResult:
    returncode: int
    stdout: bytes
    stderr: bytes


@dataclasses.dataclass(frozen=True, order=True)
class BoundedDirectoryEntry:
    name: str
    mode: int

    @property
    def is_directory(self) -> bool:
        return stat.S_ISDIR(self.mode)

    @property
    def is_regular(self) -> bool:
        return stat.S_ISREG(self.mode)

    @property
    def is_symlink(self) -> bool:
        return stat.S_ISLNK(self.mode)


def _finding(code: str, path: object, message: str) -> CatalogFinding:
    return CatalogFinding(code, str(path), message)


def _safe_relative(value: object, label: str) -> pathlib.PurePosixPath:
    if not isinstance(value, str) or not value:
        raise OperationsAuthorityError("path-invalid", f"{label} must be nonempty")
    path = pathlib.PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or path.as_posix() != value:
        raise OperationsAuthorityError("path-invalid", f"unsafe {label}: {value}")
    return path


def _has_symlink_component(root: pathlib.Path, relative: pathlib.PurePosixPath) -> bool:
    current = root
    for part in relative.parts:
        current /= part
        try:
            if stat.S_ISLNK(current.lstat().st_mode):
                return True
        except FileNotFoundError:
            return False
    return False


def _kill_and_reap(process: subprocess.Popen[bytes]) -> None:
    if process.poll() is None:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except (OSError, ProcessLookupError):
            try:
                process.kill()
            except OSError:
                pass
    try:
        process.wait(timeout=1)
    except subprocess.TimeoutExpired:
        try:
            process.kill()
        except OSError:
            pass
        process.wait()


def _run_git_bounded(
    root: pathlib.Path,
    arguments: Sequence[str],
    *,
    timeout_seconds: float = MAX_GIT_SECONDS,
    max_stdout: int = MAX_GIT_STDOUT_BYTES,
    max_stderr: int = MAX_GIT_STDERR_BYTES,
) -> GitCommandResult:
    """Run Git with simultaneous bounded pipe draining and hard cleanup."""

    if not arguments or any(
        not isinstance(item, str) or "\0" in item for item in arguments
    ):
        raise OperationsAuthorityError(
            "git-arguments-invalid", "Git arguments must be nonempty text"
        )
    if timeout_seconds <= 0 or max_stdout < 1 or max_stderr < 1:
        raise OperationsAuthorityError("bounds-invalid", "Git bounds must be positive")
    deadline_seconds = min(float(timeout_seconds), MAX_GIT_SECONDS)
    stdout_limit = min(max_stdout, MAX_GIT_STDOUT_BYTES)
    stderr_limit = min(max_stderr, MAX_GIT_STDERR_BYTES)
    try:
        process = subprocess.Popen(
            ["git", *arguments],
            cwd=root,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            start_new_session=True,
            close_fds=True,
        )
    except OSError as error:
        raise OperationsAuthorityError("git-start-failed", str(error)) from error
    assert process.stdout is not None and process.stderr is not None
    streams = {
        process.stdout: ("stdout", stdout_limit),
        process.stderr: ("stderr", stderr_limit),
    }
    output = {"stdout": bytearray(), "stderr": bytearray()}
    selector = selectors.DefaultSelector()
    failure: OperationsAuthorityError | None = None
    started = time.monotonic()
    try:
        for stream in streams:
            os.set_blocking(stream.fileno(), False)
            selector.register(stream, selectors.EVENT_READ)
        while selector.get_map():
            remaining = deadline_seconds - (time.monotonic() - started)
            if remaining <= 0:
                failure = OperationsAuthorityError(
                    "git-deadline", "Git deadline exceeded"
                )
                break
            for key, _ in selector.select(min(remaining, 0.1)):
                stream = key.fileobj
                label, limit = streams[stream]
                try:
                    chunk = os.read(stream.fileno(), 65_536)
                except BlockingIOError:
                    continue
                if not chunk:
                    selector.unregister(stream)
                    stream.close()
                    continue
                output[label].extend(chunk)
                if len(output[label]) > limit:
                    failure = OperationsAuthorityError(
                        f"git-{label}-bounds", f"Git {label} bound exceeded"
                    )
                    break
                if len(output["stdout"]) + len(output["stderr"]) > MAX_GIT_TOTAL_BYTES:
                    failure = OperationsAuthorityError(
                        "git-output-bounds", "Git output bound exceeded"
                    )
                    break
            if failure is not None:
                break
        if failure is not None:
            _kill_and_reap(process)
            raise failure
        remaining = deadline_seconds - (time.monotonic() - started)
        if remaining <= 0:
            _kill_and_reap(process)
            raise OperationsAuthorityError("git-deadline", "Git deadline exceeded")
        try:
            returncode = process.wait(timeout=remaining)
        except subprocess.TimeoutExpired as error:
            _kill_and_reap(process)
            raise OperationsAuthorityError(
                "git-deadline", "Git deadline exceeded"
            ) from error
        return GitCommandResult(
            returncode, bytes(output["stdout"]), bytes(output["stderr"])
        )
    finally:
        for stream in streams:
            try:
                selector.unregister(stream)
            except (KeyError, ValueError):
                pass
            if not stream.closed:
                stream.close()
        selector.close()
        if process.poll() is None:
            _kill_and_reap(process)


def _open_anchored_regular(
    root: pathlib.Path, relative: pathlib.PurePosixPath
) -> tuple[int, int, os.stat_result]:
    """Open and identify a regular file relative to an anchored root descriptor."""

    relative = _safe_relative(relative.as_posix(), "input path")
    directory_flags = (
        os.O_RDONLY
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_DIRECTORY", 0)
        | getattr(os, "O_NOFOLLOW", 0)
    )
    file_flags = (
        os.O_RDONLY
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NOFOLLOW", 0)
        | getattr(os, "O_NONBLOCK", 0)
    )
    directory_descriptor: int | None = None
    descriptor: int | None = None
    try:
        held_root = re.fullmatch(r"/proc/self/fd/(0|[1-9][0-9]*)", root.as_posix())
        if held_root is None:
            directory_descriptor = os.open(root, directory_flags)
        else:
            # The gate owns this already-open root. Duplicate its descriptor;
            # never resolve the proc link or relax no-follow for child paths.
            directory_descriptor = os.dup(int(held_root[1]))
            if not stat.S_ISDIR(os.fstat(directory_descriptor).st_mode):
                raise OperationsAuthorityError(
                    "root-invalid", "held root is not a directory"
                )
        for part in relative.parts[:-1]:
            component = os.stat(
                part, dir_fd=directory_descriptor, follow_symlinks=False
            )
            if stat.S_ISLNK(component.st_mode):
                raise OperationsAuthorityError(
                    "symlink-invalid", f"symlink input: {relative}"
                )
            if not stat.S_ISDIR(component.st_mode):
                raise OperationsAuthorityError(
                    "file-not-regular", f"non-directory component: {relative}"
                )
            next_descriptor = os.open(
                part, directory_flags, dir_fd=directory_descriptor
            )
            opened = os.fstat(next_descriptor)
            if (component.st_dev, component.st_ino) != (opened.st_dev, opened.st_ino):
                os.close(next_descriptor)
                raise OperationsAuthorityError(
                    "file-raced", f"changed before read: {relative}"
                )
            os.close(directory_descriptor)
            directory_descriptor = next_descriptor
        path_stat = os.stat(
            relative.name, dir_fd=directory_descriptor, follow_symlinks=False
        )
        if stat.S_ISLNK(path_stat.st_mode):
            raise OperationsAuthorityError(
                "symlink-invalid", f"symlink input: {relative}"
            )
        if not stat.S_ISREG(path_stat.st_mode):
            raise OperationsAuthorityError(
                "file-not-regular", f"not regular: {relative}"
            )
        descriptor = os.open(relative.name, file_flags, dir_fd=directory_descriptor)
        opened = os.fstat(descriptor)
        if not stat.S_ISREG(opened.st_mode) or (opened.st_dev, opened.st_ino) != (
            path_stat.st_dev,
            path_stat.st_ino,
        ):
            raise OperationsAuthorityError(
                "file-raced", f"changed before read: {relative}"
            )
        return directory_descriptor, descriptor, opened
    except OperationsAuthorityError:
        if descriptor is not None:
            os.close(descriptor)
        if directory_descriptor is not None:
            os.close(directory_descriptor)
        raise
    except OSError as error:
        if descriptor is not None:
            os.close(descriptor)
        if directory_descriptor is not None:
            os.close(directory_descriptor)
        code = "symlink-invalid" if error.errno in {errno.ELOOP} else "file-unreadable"
        raise OperationsAuthorityError(code, f"{relative}: {error}") from error


def _directory_entries_bounded(
    root: pathlib.Path,
    relative: pathlib.PurePosixPath,
    *,
    max_entries: int,
) -> tuple[BoundedDirectoryEntry, ...]:
    """Stream one directory through anchored descriptors and reject identity races."""

    if (
        isinstance(max_entries, bool)
        or not isinstance(max_entries, int)
        or max_entries < 1
    ):
        raise OperationsAuthorityError(
            "bounds-invalid", "max_entries must be a positive integer"
        )
    effective_limit = min(max_entries, MAX_DIRECTORY_ENTRIES)
    relative = _safe_relative(relative.as_posix(), "directory path")
    if not relative.parts:
        raise OperationsAuthorityError(
            "path-invalid", "directory path must be nonempty"
        )
    directory_flags = (
        os.O_RDONLY
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_DIRECTORY", 0)
        | getattr(os, "O_NOFOLLOW", 0)
    )
    parent_descriptor: int | None = None
    directory_descriptor: int | None = None
    try:
        parent_descriptor = os.open(root, directory_flags)
        path_stat: os.stat_result | None = None
        for index, part in enumerate(relative.parts):
            path_stat = os.stat(part, dir_fd=parent_descriptor, follow_symlinks=False)
            if stat.S_ISLNK(path_stat.st_mode) or not stat.S_ISDIR(path_stat.st_mode):
                raise OperationsAuthorityError(
                    "directory-not-regular", f"not a real directory: {relative}"
                )
            opened_descriptor = os.open(part, directory_flags, dir_fd=parent_descriptor)
            opened = os.fstat(opened_descriptor)
            if (path_stat.st_dev, path_stat.st_ino) != (opened.st_dev, opened.st_ino):
                os.close(opened_descriptor)
                raise OperationsAuthorityError(
                    "directory-raced",
                    f"directory changed before enumeration: {relative}",
                )
            if index == len(relative.parts) - 1:
                directory_descriptor = opened_descriptor
                before = opened
                break
            os.close(parent_descriptor)
            parent_descriptor = opened_descriptor
        assert directory_descriptor is not None and path_stat is not None
        entries: list[BoundedDirectoryEntry] = []
        scan_descriptor = os.dup(directory_descriptor)
        try:
            with os.scandir(scan_descriptor) as iterator:
                for entry in iterator:
                    if len(entries) >= effective_limit:
                        raise OperationsAuthorityError(
                            "directory-bounds", f"entry bound exceeded: {relative}"
                        )
                    metadata = entry.stat(follow_symlinks=False)
                    entries.append(BoundedDirectoryEntry(entry.name, metadata.st_mode))
        finally:
            try:
                os.close(scan_descriptor)
            except OSError as error:
                if error.errno != errno.EBADF:
                    raise
        after = os.fstat(directory_descriptor)
        path_after = os.stat(
            relative.name,
            dir_fd=parent_descriptor,
            follow_symlinks=False,
        )
        identity = (before.st_dev, before.st_ino)
        if (
            identity != (after.st_dev, after.st_ino)
            or identity != (path_after.st_dev, path_after.st_ino)
            or before.st_mtime_ns != after.st_mtime_ns
            or stat.S_ISLNK(path_after.st_mode)
            or not stat.S_ISDIR(path_after.st_mode)
        ):
            raise OperationsAuthorityError(
                "directory-raced", f"directory changed during enumeration: {relative}"
            )
        return tuple(sorted(entries))
    except OperationsAuthorityError:
        raise
    except (NotImplementedError, OSError) as error:
        raise OperationsAuthorityError(
            "directory-unreadable", f"cannot enumerate {relative}: {error}"
        ) from error
    finally:
        if directory_descriptor is not None:
            os.close(directory_descriptor)
        if parent_descriptor is not None:
            os.close(parent_descriptor)


def read_bounded_regular(
    root: pathlib.Path,
    relative: pathlib.PurePosixPath,
    *,
    max_bytes: int = MAX_FILE_BYTES,
) -> bytes:
    """Read one regular file without following symlinks or accepting races."""
    if isinstance(max_bytes, bool) or not isinstance(max_bytes, int) or max_bytes < 1:
        raise OperationsAuthorityError(
            "bounds-invalid", "max_bytes must be a positive integer"
        )
    effective_max_bytes = min(max_bytes, MAX_FILE_BYTES)
    relative = _safe_relative(relative.as_posix(), "input path")
    directory_descriptor, descriptor, before = _open_anchored_regular(root, relative)
    try:
        identity = (before.st_dev, before.st_ino)
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = os.read(descriptor, min(65_536, effective_max_bytes + 1 - total))
            if not chunk:
                break
            chunks.append(chunk)
            total += len(chunk)
            if total > effective_max_bytes:
                raise OperationsAuthorityError(
                    "file-too-large", f"bound exceeded: {relative}"
                )
        after = os.fstat(descriptor)
        if (
            identity != (after.st_dev, after.st_ino)
            or before.st_size != after.st_size
            or before.st_mtime_ns != after.st_mtime_ns
        ):
            raise OperationsAuthorityError(
                "file-raced", f"changed during read: {relative}"
            )
        return b"".join(chunks)
    finally:
        os.close(descriptor)
        os.close(directory_descriptor)


def _read_text(root: pathlib.Path, relative: pathlib.PurePosixPath) -> str:
    try:
        return read_bounded_regular(root, relative).decode("utf-8")
    except UnicodeDecodeError as error:
        raise OperationsAuthorityError(
            "utf8-invalid", f"invalid UTF-8: {relative}"
        ) from error


def _tracked_paths(
    root: pathlib.Path, max_files: int
) -> tuple[pathlib.PurePosixPath, ...]:
    effective_max_files = min(max_files, MAX_TRACKED_FILES)
    result = _run_git_bounded(
        root,
        ["ls-files", "-z"],
        max_stdout=MAX_GIT_STDOUT_BYTES,
    )
    if result.returncode:
        raise OperationsAuthorityError("git-scan-failed", "git ls-files failed")
    raw = result.stdout.split(b"\0")
    if raw and raw[-1] == b"":
        raw.pop()
    if len(raw) > effective_max_files:
        raise OperationsAuthorityError(
            "tracked-file-bounds", "tracked file bound exceeded"
        )
    try:
        return tuple(_safe_relative(item.decode(), "tracked path") for item in raw)
    except UnicodeDecodeError as error:
        raise OperationsAuthorityError(
            "tracked-path-utf8", "tracked path is not UTF-8"
        ) from error


def tracked_paths(root: pathlib.Path) -> tuple[pathlib.PurePosixPath, ...]:
    """Expose the bounded tracked-path scan to other document validators."""

    return _tracked_paths(root, MAX_TRACKED_FILES)


def _excluded(path: pathlib.PurePosixPath) -> bool:
    value = path.as_posix()
    return value.startswith(
        ("docs/90.references/", "docs/98.archive/", "graphify-out/")
    )


_RETIRED_ROUTE_RECORD_MARKER = "retired-route-record"


def _active_reference_scan_excluded(path: pathlib.PurePosixPath) -> bool:
    value = path.as_posix()
    spec_execution_body = value.startswith("docs/03.specs/") and (
        path.name == "plan.md" or "tasks" in path.parts
    )
    return (
        _excluded(path)
        or spec_execution_body
        or value.startswith(("tests/", ".superpowers/"))
    )


def validate_active_operations_references(
    root: pathlib.Path,
) -> tuple[CatalogFinding, ...]:
    """Reject generic predecessor routes on bounded active text surfaces."""

    findings: list[CatalogFinding] = []
    for path in _tracked_paths(root, MAX_TRACKED_FILES):
        suffix = path.suffix.lower()
        if suffix not in {
            ".md",
            ".py",
            ".sh",
            ".yaml",
            ".yml",
            ".json",
            ".toml",
        } or _active_reference_scan_excluded(path):
            continue
        try:
            (root / path).lstat()
        except FileNotFoundError:
            continue
        except OSError as error:
            raise OperationsAuthorityError(
                "tracked-file-invalid", f"{path}: {error}"
            ) from error
        try:
            text = read_bounded_regular(root, path).decode("utf-8")
        except UnicodeDecodeError:
            continue
        text = text.replace("\r\n", "\n").replace("\r", "\n")
        value = path.as_posix()
        if value.startswith("docs/03.specs/") and path.name == "spec.md":
            try:
                metadata = parse_frontmatter_text(text)
            except FrontmatterError:
                metadata = {}
            if metadata.get("status") in {"superseded", "retired"}:
                continue
        release_table_lines: set[int] = set()
        if suffix == ".md" and "release" in text.lower():
            in_table = False
            for token in MarkdownIt("commonmark").enable("table").parse(text):
                if token.type == "table_open":
                    in_table = True
                elif token.type == "table_close":
                    in_table = False
                elif (
                    in_table
                    and token.type == "inline"
                    and token.content.strip().lower() == "release"
                    and token.map
                ):
                    release_table_lines.add(token.map[0] + 1)
        for line_number, line in enumerate(text.split("\n"), 1):
            if _RETIRED_ROUTE_RECORD_MARKER in line:
                # A line whose purpose is to record a retired route is not an
                # active reference to it. Sixteen such lines used to satisfy
                # this scan by splitting the path across adjacent string
                # literals, so the check was met by typography and any
                # reformatting broke it. The marker states the exemption.
                continue
            old_route = any(pattern.search(line) for pattern in _ACTIVE_ROUTE_PATTERNS)
            release_role = (
                suffix == ".md"
                and (
                    line_number in release_table_lines
                    or _RELEASE_ROLE_PATTERN.search(line)
                )
                and not any(token in line.lower() for token in _RELEASE_NEGATIONS)
            )
            if old_route or release_role:
                findings.append(
                    _finding(
                        "active-operations-reference-invalid",
                        f"{path}:{line_number}",
                        "generic predecessor route or Release document role",
                    )
                )
    return tuple(sorted(set(findings)))


COMPOSE_ROOT = pathlib.PurePosixPath("docker-compose.yml")
PROFILE_VOCABULARY_POLICY = pathlib.PurePosixPath(
    "docs/05.operations/catalog/00-workspace/0078-compose-profile-vocabulary/policy.md"
)
_COMPOSE_FILE_NAME = re.compile(r"(?:docker-)?compose[^/]*\.ya?ml")
# A profile row is a table row whose first cell is exactly one backticked name.
# The mutually exclusive pairs table never matches, because its first cells
# carry more than a single name.
_PROFILE_ROW = re.compile(r"\| `(?P<name>[A-Za-z0-9][A-Za-z0-9_.-]*)` \|(?P<rest>.*)\|")
_PROFILE_MEMBER = re.compile(r"`([A-Za-z0-9][A-Za-z0-9_.-]*)`")
_PROFILE_CATEGORIES = frozenset(
    {"baseline", "domain", "capability", "role", "topology", "lifecycle", "automation"}
)
_HOME_FORBIDDEN_CATEGORIES = frozenset({"automation", "lifecycle", "topology"})
_HOME_FORBIDDEN_SERVICE_CATEGORIES = frozenset({"automation", "lifecycle"})
_REQUIRED_HOME_PROFILES = frozenset(
    {
        "core",
        "mng",
        "ai",
        "workflow",
        "obs-core",
        "obs-host",
        "availability",
        "logs",
        "alerting",
        "storage",
    }
)
_FIXED_PROFILE_CATEGORIES = {
    "core": "baseline",
    "local": "baseline",
    "dev": "baseline",
    "dependency-update": "automation",
    "testing": "automation",
    "iac": "automation",
    "legacy-vault": "lifecycle",
    "couchdb": "topology",
    "dedicated-valkey": "topology",
    "messaging-cluster": "topology",
    "mongodb": "topology",
    "nginx": "topology",
    "opensearch": "topology",
    "opensearch-cluster": "topology",
    "postgres-ha": "topology",
    "valkey-cluster": "topology",
}


@dataclasses.dataclass(frozen=True)
class _ProfilePolicyRow:
    category: str
    members: frozenset[str] | None
    count: int | None
    line_number: int


def _is_infra_compose_file(path: str | pathlib.PurePosixPath) -> bool:
    candidate = pathlib.PurePosixPath(path)
    return (
        not candidate.is_absolute()
        and ".." not in candidate.parts
        and len(candidate.parts) >= 2
        and candidate.parts[0] == "infra"
        and _COMPOSE_FILE_NAME.fullmatch(candidate.name) is not None
    )


def _parse_backticked_names(value: str) -> tuple[tuple[str, ...], str | None]:
    if not value:
        return (), "is empty"
    names = tuple(_PROFILE_MEMBER.findall(value))
    if value != ", ".join(f"`{name}`" for name in names):
        return names, "is malformed"
    duplicate = next(
        (name for index, name in enumerate(names) if name in names[:index]), None
    )
    if duplicate is not None:
        return names, f"duplicates {duplicate}"
    return names, None


def _required_compose_dependencies(service: object) -> frozenset[str]:
    if not isinstance(service, Mapping):
        return frozenset()
    depends_on = service.get("depends_on")
    if isinstance(depends_on, Mapping):
        return frozenset(
            str(name)
            for name, condition in depends_on.items()
            if not (
                isinstance(condition, Mapping) and condition.get("required") is False
            )
        )
    return frozenset(_string_items(depends_on))


class _ComposeLoader(yaml.SafeLoader):
    """Safe loader that also reads the merge tags Compose defines."""


def _construct_compose_tag(loader: yaml.SafeLoader, node: yaml.Node) -> object:
    # Only plain data comes back, so the loader stays as safe as SafeLoader.
    if isinstance(node, yaml.MappingNode):
        return loader.construct_mapping(node)
    if isinstance(node, yaml.SequenceNode):
        return loader.construct_sequence(node)
    if isinstance(node, yaml.ScalarNode):
        return loader.construct_scalar(node)
    return None


for _compose_tag in ("!reset", "!override"):
    _ComposeLoader.add_constructor(_compose_tag, _construct_compose_tag)


def _compose_mapping(
    root: pathlib.Path, path: pathlib.PurePosixPath
) -> Mapping[str, object]:
    try:
        value = yaml.load(_read_text(root, path), Loader=_ComposeLoader)
    except yaml.YAMLError as error:
        raise OperationsAuthorityError(
            "compose-yaml-invalid", f"{path}: {error}"
        ) from error
    if value is None:
        return {}
    if not isinstance(value, Mapping):
        raise OperationsAuthorityError(
            "compose-yaml-invalid", f"{path}: top level is not a mapping"
        )
    return value


def _include_paths(include: object) -> set[str]:
    """Read string and `path:` mapping include entries as normalized paths."""

    if not isinstance(include, Sequence) or isinstance(include, (str, bytes)):
        return set()
    paths: set[str] = set()
    for item in include:
        value = item.get("path") if isinstance(item, Mapping) else item
        entries = (value,) if isinstance(value, str) else _string_items(value)
        paths.update(posixpath.normpath(entry) for entry in entries)
    return paths


def validate_compose_profile_vocabulary(
    root: pathlib.Path,
) -> tuple[CatalogFinding, ...]:
    """Hold POL-0078 profile membership and HOME selection to Compose."""

    compose_files = tuple(
        path
        for path in _tracked_paths(root, MAX_TRACKED_FILES)
        if _is_infra_compose_file(path)
    )
    tracked = {path.as_posix() for path in compose_files}
    included = _include_paths(_compose_mapping(root, COMPOSE_ROOT).get("include"))
    findings = [
        _finding(
            "compose-include-drift",
            COMPOSE_ROOT,
            f"{path} is tracked and not included",
        )
        for path in sorted(tracked - included)
    ] + [
        _finding(
            "compose-include-drift",
            COMPOSE_ROOT,
            f"{path} is included and is not a tracked Compose file under infra/",
        )
        for path in sorted(included - tracked)
    ]

    declared: dict[str, frozenset[str]] = {}
    service_definitions: dict[str, object] = {}
    for path in compose_files:
        services = _compose_mapping(root, path).get("services")
        items = services.items() if isinstance(services, Mapping) else ()
        for name, service in items:
            service_name = str(name)
            profiles = frozenset(
                _string_items(
                    service.get("profiles") if isinstance(service, Mapping) else None
                )
            )
            if not profiles:
                findings.append(
                    _finding(
                        "compose-service-profile-missing",
                        path,
                        f"service {service_name} declares no profile, "
                        "so it starts when none is selected",
                    )
                )
            service_definitions = {**service_definitions, service_name: service}
            for profile in profiles:
                declared = {
                    **declared,
                    profile: declared.get(profile, frozenset()) | {service_name},
                }

    rows: dict[str, _ProfilePolicyRow] = {}
    policy_text = _read_text(root, PROFILE_VOCABULARY_POLICY)
    header: list[str] = []
    home_profiles: tuple[str, ...] | None = None
    home_forbidden: tuple[str, ...] | None = None
    for line_number, line in enumerate(policy_text.splitlines(), 1):
        stripped = line.strip()
        if not stripped.startswith("|"):
            header = []
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        first = cells[0].lower() if cells else ""
        if first in {"profile", "named selection"}:
            header = [cell.lower() for cell in cells]
            if first == "profile" and "selected services" not in header:
                findings.append(
                    _finding(
                        "compose-profile-vocabulary-drift",
                        f"{PROFILE_VOCABULARY_POLICY}:{line_number}",
                        "profile table has no Selected services column",
                    )
                )
            continue
        if first == "home" and header and header[0] == "named selection":
            location = f"{PROFILE_VOCABULARY_POLICY}:{line_number}"
            fields = dict(zip(header, cells, strict=False))
            if len(cells) != len(header):
                findings.append(
                    _finding(
                        "compose-profile-vocabulary-drift",
                        location,
                        "HOME row does not match its table header",
                    )
                )
            home_profiles, profiles_error = _parse_backticked_names(
                fields.get("profiles", "")
            )
            home_forbidden, categories_error = _parse_backticked_names(
                fields.get("forbidden categories", "")
            )
            for field, error in (
                ("Profiles", profiles_error),
                ("Forbidden categories", categories_error),
            ):
                if error is not None:
                    findings.append(
                        _finding(
                            "compose-profile-vocabulary-drift",
                            location,
                            f"HOME {field} {error}",
                        )
                    )
            continue
        match = _PROFILE_ROW.fullmatch(stripped)
        if match is None or not header or header[0] != "profile":
            continue
        name, location = match["name"], f"{PROFILE_VOCABULARY_POLICY}:{line_number}"
        if name in rows:
            findings.append(
                _finding(
                    "compose-profile-vocabulary-drift",
                    location,
                    f"profile {name} has more than one row; "
                    f"the first is line {rows[name].line_number}",
                )
            )
            continue
        count: int | None = None
        messages: list[str] = []
        if len(cells) != len(header):
            messages.append(f"profile {name} row does not match its table header")
        fields = dict(zip(header, cells, strict=False))
        category = fields.get("category", "")
        if category not in _PROFILE_CATEGORIES:
            messages.append(f"profile {name} row has no valid category")
        if not fields.get("purpose", "").strip():
            messages.append(f"profile {name} row has no purpose")
        members: frozenset[str] | None = None
        if "selected services" in header:
            member_names, member_error = _parse_backticked_names(
                fields.get("selected services", "")
            )
            if member_error is not None:
                if member_error == "is empty":
                    messages.append(f"profile {name} has empty Selected services")
                elif member_error == "is malformed":
                    messages.append(f"profile {name} has malformed Selected services")
                else:
                    detail = member_error.replace("duplicates ", "duplicates service ")
                    messages.append(f"profile {name} Selected services {detail}")
            if member_error is None or member_error.startswith("duplicates "):
                members = frozenset(member_names)
        count_key = next((key for key in ("서비스", "services") if key in header), None)
        if count_key is not None:
            raw_count = fields.get(count_key, "")
            if not (raw_count.isascii() and raw_count.isdigit()):
                count = -1
                messages.append(f"profile {name} row has no integer service count")
            else:
                count = int(raw_count)
        rows = {
            **rows,
            name: _ProfilePolicyRow(
                category=category,
                members=members,
                count=count,
                line_number=line_number,
            ),
        }
        findings.extend(
            _finding("compose-profile-vocabulary-drift", location, message)
            for message in messages
        )
    for name in sorted(declared.keys() - rows.keys()):
        findings.append(
            _finding(
                "compose-profile-vocabulary-drift",
                PROFILE_VOCABULARY_POLICY,
                f"profile {name} is declared by {len(declared[name])} service(s) "
                "and has no row",
            )
        )
    for name in sorted(declared):
        if name.casefold() == "home":
            findings.append(
                _finding(
                    "compose-profile-vocabulary-drift",
                    PROFILE_VOCABULARY_POLICY,
                    f"profile {name} uses reserved HOME name; "
                    "HOME is a named selection, not a Compose profile",
                )
            )
    for name, row in sorted(rows.items()):
        location = f"{PROFILE_VOCABULARY_POLICY}:{row.line_number}"
        if name not in declared:
            message = (
                f"profile {name} has a row and no tracked Compose service declares it"
            )
            findings.append(
                _finding("compose-profile-vocabulary-drift", location, message)
            )
            continue
        if (
            row.count is not None
            and row.count >= 0
            and row.count != len(declared[name])
        ):
            message = (
                f"profile {name} row counts {row.count} service(s); "
                f"Compose declares {len(declared[name])}"
            )
            findings.append(
                _finding("compose-profile-vocabulary-drift", location, message)
            )
        if row.members is None:
            continue
        missing = declared[name] - row.members
        extra = row.members - declared[name]
        for label, members in (
            ("missing from policy", missing),
            ("unknown or extra", extra),
        ):
            if members:
                findings.append(
                    _finding(
                        "compose-profile-vocabulary-drift",
                        location,
                        f"profile {name} Selected services {label}: "
                        + ", ".join(sorted(members)),
                    )
                )

    for name, expected in _FIXED_PROFILE_CATEGORIES.items():
        row = rows.get(name)
        if row is not None and row.category != expected:
            findings.append(
                _finding(
                    "compose-profile-vocabulary-drift",
                    f"{PROFILE_VOCABULARY_POLICY}:{row.line_number}",
                    f"profile {name} must use safety category {expected}, "
                    f"found {row.category or '<empty>'}",
                )
            )

    tooling = declared.get("tooling", frozenset())
    for profile, row in sorted(rows.items()):
        if row.category not in _HOME_FORBIDDEN_SERVICE_CATEGORIES:
            continue
        overlap = tooling & declared.get(profile, frozenset())
        if overlap:
            findings.append(
                _finding(
                    "compose-profile-vocabulary-drift",
                    PROFILE_VOCABULARY_POLICY,
                    f"tooling overlaps automation/lifecycle profile {profile}: "
                    + ", ".join(sorted(overlap)),
                )
            )

    if home_profiles is None or home_forbidden is None:
        findings.append(
            _finding(
                "compose-profile-vocabulary-drift",
                PROFILE_VOCABULARY_POLICY,
                "named selection table has no valid HOME row",
            )
        )
        return tuple(findings)
    if frozenset(home_forbidden) != _HOME_FORBIDDEN_CATEGORIES:
        findings.append(
            _finding(
                "compose-profile-vocabulary-drift",
                PROFILE_VOCABULARY_POLICY,
                "HOME Forbidden categories must be automation, lifecycle, topology",
            )
        )
    missing_required = _REQUIRED_HOME_PROFILES - frozenset(home_profiles)
    if missing_required:
        findings.append(
            _finding(
                "compose-profile-vocabulary-drift",
                PROFILE_VOCABULARY_POLICY,
                "HOME is missing required profiles: "
                + ", ".join(sorted(missing_required)),
            )
        )
    unknown_home = frozenset(home_profiles) - declared.keys()
    if unknown_home:
        findings.append(
            _finding(
                "compose-profile-vocabulary-drift",
                PROFILE_VOCABULARY_POLICY,
                "HOME names unknown profiles: " + ", ".join(sorted(unknown_home)),
            )
        )
    forbidden_profiles = frozenset(
        name
        for name in home_profiles
        if name in rows and rows[name].category in _HOME_FORBIDDEN_CATEGORIES
    )
    if forbidden_profiles:
        findings.append(
            _finding(
                "compose-profile-vocabulary-drift",
                PROFILE_VOCABULARY_POLICY,
                "HOME includes forbidden profiles: "
                + ", ".join(sorted(forbidden_profiles)),
            )
        )
    home_services = frozenset().union(
        *(declared.get(name, frozenset()) for name in home_profiles)
    )
    forbidden_services = frozenset().union(
        *(
            declared.get(name, frozenset())
            for name, row in rows.items()
            if row.category in _HOME_FORBIDDEN_SERVICE_CATEGORIES
        )
    )
    unsafe_overlap = home_services & forbidden_services
    if unsafe_overlap:
        findings.append(
            _finding(
                "compose-profile-vocabulary-drift",
                PROFILE_VOCABULARY_POLICY,
                "HOME services overlap forbidden profile services: "
                + ", ".join(sorted(unsafe_overlap)),
            )
        )
    for service_name in sorted(home_services):
        for dependency in sorted(
            _required_compose_dependencies(service_definitions.get(service_name))
            - home_services
        ):
            findings.append(
                _finding(
                    "compose-profile-vocabulary-drift",
                    PROFILE_VOCABULARY_POLICY,
                    f"HOME service {service_name} has required dependency "
                    f"{dependency} outside HOME",
                )
            )
    return tuple(findings)


def _frontmatter(text: str, path: pathlib.PurePosixPath) -> Mapping[str, object]:
    if not text.startswith("---\n"):
        raise OperationsAuthorityError("frontmatter-missing", str(path))
    try:
        value = parse_frontmatter_text(text)
    except FrontmatterError as error:
        raise OperationsAuthorityError("frontmatter-invalid", str(path)) from error
    return value


def _load_registry(root: pathlib.Path) -> Mapping[str, object]:
    try:
        value = load_registry_document(root / REGISTRY_PATH)
    except RegistryError as error:
        raise OperationsAuthorityError("registry-invalid", str(error)) from error
    return value


def _validate_registry(registry: Mapping[str, object]) -> list[CatalogFinding]:
    profiles = registry.get("profiles")
    roles = registry.get("template_roles")
    if not isinstance(profiles, list) or not isinstance(roles, Mapping):
        return [
            _finding(
                "registry-invalid",
                REGISTRY_PATH,
                "profile/template collections invalid",
            )
        ]
    profile_ids = [
        item.get("id")
        for item in profiles
        if isinstance(item, Mapping) and isinstance(item.get("id"), str)
    ]
    release_template_present = any(
        isinstance(definition, Mapping)
        and "release.template" in str(definition.get("source", ""))
        for definition in roles.values()
    )
    canonical_findings = validate_canonical_registry(registry)
    findings: list[CatalogFinding] = [
        _finding(
            "registry-canonical-invalid", REGISTRY_PATH, f"{item.code}:{item.path}"
        )
        for item in canonical_findings
    ]
    if (
        "release" in profile_ids
        or "operations/release" in roles
        or "operation/release" in roles
        or release_template_present
    ):
        findings.append(
            _finding(
                "release-authority-present", REGISTRY_PATH, "Release remains registered"
            )
        )
    if any(item.code == "schema-invalid" for item in canonical_findings):
        return findings
    duplicates = {
        item
        for item in profile_ids
        if isinstance(item, str) and profile_ids.count(item) > 1
    }
    if duplicates:
        findings.append(
            _finding(
                "registry-profile-duplicate", REGISTRY_PATH, str(sorted(duplicates))
            )
        )
    by_id = {item.get("id"): item for item in profiles if isinstance(item, Mapping)}
    lifecycles = registry.get("lifecycles")
    for profile_id in _OPERATIONS_PROFILE_IDS:
        profile = by_id.get(profile_id)
        if not isinstance(profile, Mapping):
            findings.append(
                _finding(
                    "registry-operations-profile-invalid", REGISTRY_PATH, profile_id
                )
            )
            continue
        required_frontmatter = profile.get("required_frontmatter")
        required_sections = profile.get("required_sections")
        lifecycle_id = profile.get("lifecycle_id")
        lifecycle = (
            lifecycles.get(lifecycle_id) if isinstance(lifecycles, Mapping) else None
        )
        statuses = lifecycle.get("statuses") if isinstance(lifecycle, Mapping) else None
        if (
            profile.get("frontmatter_policy") != "required"
            or not isinstance(profile.get("artifact_id_pattern"), str)
            or not isinstance(required_frontmatter, list)
            or not all(isinstance(item, str) and item for item in required_frontmatter)
            or not {"title", "type", "layer", "status", "owner", "artifact_id"}
            <= set(required_frontmatter)
            or not isinstance(required_sections, list)
            or not required_sections
            or not all(isinstance(item, str) and item for item in required_sections)
        ):
            findings.append(
                _finding(
                    "registry-operations-profile-invalid", REGISTRY_PATH, profile_id
                )
            )
        if (
            not isinstance(statuses, list)
            or not statuses
            or not all(isinstance(status, str) and status for status in statuses)
        ):
            findings.append(
                _finding(
                    "registry-operations-lifecycle-invalid",
                    REGISTRY_PATH,
                    str(lifecycle_id),
                )
            )
        template_id = profile.get("template_id")
        role = roles.get(template_id) if isinstance(template_id, str) else None
        if not isinstance(role, Mapping) or profile_id not in role.get("profiles", ()):
            findings.append(
                _finding(
                    "registry-operations-profile-invalid",
                    REGISTRY_PATH,
                    f"{profile_id}.template_id",
                )
            )
    role_sections = [
        tuple(by_id[role].get("required_sections", ()))
        for role in ("guide", "policy", "runbook")
        if isinstance(by_id.get(role), Mapping)
    ]
    if len(role_sections) != len(set(role_sections)):
        findings.append(
            _finding(
                "registry-role-purpose-duplicate",
                REGISTRY_PATH,
                "role sections must differ",
            )
        )
    return findings


def _registry_profiles(
    registry: Mapping[str, object],
) -> dict[str, Mapping[str, object]]:
    profiles = registry.get("profiles")
    if not isinstance(profiles, list):
        return {}
    return {
        str(profile["id"]): profile
        for profile in profiles
        if isinstance(profile, Mapping) and isinstance(profile.get("id"), str)
    }


def _profile_statuses(
    registry: Mapping[str, object], profile: Mapping[str, object]
) -> frozenset[str]:
    lifecycles = registry.get("lifecycles")
    lifecycle_id = profile.get("lifecycle_id")
    lifecycle = (
        lifecycles.get(lifecycle_id)
        if isinstance(lifecycles, Mapping) and isinstance(lifecycle_id, str)
        else None
    )
    statuses = lifecycle.get("statuses") if isinstance(lifecycle, Mapping) else None
    if not isinstance(statuses, list):
        return frozenset()
    return frozenset(status for status in statuses if isinstance(status, str))


def _string_items(value: object) -> tuple[str, ...]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes, bytearray)):
        return ()
    return tuple(item for item in value if isinstance(item, str))


def _headings(text: str) -> set[str]:
    return {
        match.group(1).strip()
        for line in text.splitlines()
        if (match := re.fullmatch(r" {0,3}##\s+(.+?)\s*#*", line))
    }


def _matches_artifact_pattern(pattern: object, value: object) -> bool:
    if not isinstance(pattern, str) or not isinstance(value, str):
        return False
    expression = re.escape(pattern).replace(
        re.escape("{number:4}"),
        r"[0-9]{4}",
    )
    return re.fullmatch(expression, value) is not None


def _date_time(value: object) -> dt.datetime | None:
    if isinstance(value, dt.datetime):
        parsed = value
    elif isinstance(value, dt.date):
        parsed = dt.datetime.combine(value, dt.time.min)
    elif isinstance(value, str):
        try:
            parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return None
    else:
        return None
    if parsed.tzinfo is not None:
        parsed = parsed.astimezone(dt.UTC).replace(tzinfo=None)
    return parsed


def validate_current_operations(root: pathlib.Path) -> tuple[CatalogFinding, ...]:
    """Validate the bounded current Stage 05 tree against Stage 99 profiles."""
    try:
        registry = _load_registry(root)
    except OperationsAuthorityError as error:
        return (_finding(error.code, "authority", str(error)),)
    findings = _validate_registry(registry)
    if any(finding.code == "registry-invalid" for finding in findings):
        return tuple(sorted(set(findings)))
    profiles = _registry_profiles(registry)
    try:
        tracked_paths = set(_tracked_paths(root, MAX_TRACKED_FILES))
    except OperationsAuthorityError as error:
        return tuple(sorted({*findings, _finding(error.code, "authority", str(error))}))

    def require_tracked(path: pathlib.PurePosixPath) -> None:
        if path not in tracked_paths:
            findings.append(
                _finding(
                    "untracked-operations-path",
                    path,
                    "current Operations files must be Git tracked",
                )
            )

    try:
        operations_entries = _directory_entries_bounded(
            root,
            OPERATIONS_ROOT,
            max_entries=MAX_OPERATIONS_ROOT_ENTRIES,
        )
    except OperationsAuthorityError as error:
        code = (
            "operations-root-bounds"
            if error.code == "directory-bounds"
            else "operations-root-invalid"
        )
        return (_finding(code, OPERATIONS_ROOT, str(error)),)
    root_entry_names = {entry.name for entry in operations_entries}
    root_by_name = {entry.name: entry for entry in operations_entries}
    if root_entry_names != {"README.md", "catalog", "incidents"}:
        findings.append(
            _finding(
                "operations-root-contents-invalid",
                OPERATIONS_ROOT,
                str(sorted(root_entry_names)),
            )
        )
    for retired in ("releases", "guides", "policies", "runbooks"):
        if retired in root_entry_names:
            findings.append(
                _finding(
                    "retired-root-present", OPERATIONS_ROOT / retired, "must be absent"
                )
            )
    root_readme = root_by_name.get("README.md")
    if root_readme is None or not root_readme.is_regular:
        findings.append(
            _finding(
                "operations-root-index-invalid",
                OPERATIONS_ROOT / "README.md",
                "regular README required",
            )
        )
    else:
        require_tracked(OPERATIONS_ROOT / "README.md")
    template = root / "docs/99.templates/templates/operations/release.template.md"
    if template.exists() or template.is_symlink():
        findings.append(
            _finding(
                "release-template-present", template.relative_to(root), "must be absent"
            )
        )

    catalog_relative = OPERATIONS_ROOT / "catalog"
    try:
        catalog_entries = _directory_entries_bounded(
            root,
            catalog_relative,
            max_entries=MAX_CATALOG_ENTRIES,
        )
    except OperationsAuthorityError as error:
        code = (
            "catalog-bounds"
            if error.code == "directory-bounds"
            else "catalog-root-invalid"
        )
        findings.append(_finding(code, catalog_relative, str(error)))
        catalog_entries = ()
    seen_numbers: dict[str, pathlib.PurePosixPath] = {}
    seen_artifacts: dict[str, pathlib.PurePosixPath] = {}
    catalog_by_name = {entry.name: entry for entry in catalog_entries}
    catalog_readme = catalog_by_name.get("README.md")
    if catalog_readme is None or not catalog_readme.is_regular:
        findings.append(
            _finding(
                "catalog-index-invalid",
                catalog_relative / "README.md",
                "regular README required",
            )
        )
    else:
        require_tracked(catalog_relative / "README.md")
    for domain_entry in sorted(catalog_entries, key=lambda item: item.name):
        if domain_entry.name == "README.md":
            continue
        domain_relative = catalog_relative / domain_entry.name
        if (
            not domain_entry.is_directory
            or _DOMAIN.fullmatch(domain_entry.name) is None
        ):
            findings.append(
                _finding(
                    "domain-path-invalid",
                    domain_relative,
                    "must be a two-digit slug directory",
                )
            )
            continue
        try:
            domain_entries = _directory_entries_bounded(
                root,
                domain_relative,
                max_entries=MAX_DOMAIN_ENTRIES,
            )
        except OperationsAuthorityError as error:
            code = (
                "domain-bounds"
                if error.code == "directory-bounds"
                else "domain-invalid"
            )
            findings.append(_finding(code, domain_relative, str(error)))
            continue
        domain_by_name = {entry.name: entry for entry in domain_entries}
        domain_readme = domain_by_name.get("README.md")
        if domain_readme is None or not domain_readme.is_regular:
            findings.append(
                _finding(
                    "domain-index-invalid",
                    domain_relative / "README.md",
                    "regular README required",
                )
            )
        else:
            require_tracked(domain_relative / "README.md")
        for subject_entry in sorted(domain_entries, key=lambda item: item.name):
            if subject_entry.name == "README.md":
                continue
            subject_relative = domain_relative / subject_entry.name
            match = _SUBJECT.fullmatch(subject_entry.name)
            if not subject_entry.is_directory or match is None:
                findings.append(
                    _finding(
                        "subject-path-invalid",
                        subject_relative,
                        "must be prefixless four-digit slug",
                    )
                )
                continue
            try:
                subject_entries = _directory_entries_bounded(
                    root,
                    subject_relative,
                    max_entries=MAX_SUBJECT_ENTRIES,
                )
            except OperationsAuthorityError as error:
                code = (
                    "subject-bounds"
                    if error.code == "directory-bounds"
                    else "subject-symlink-invalid"
                )
                findings.append(_finding(code, subject_relative, str(error)))
                continue
            number = match.group("number")
            previous = seen_numbers.setdefault(number, subject_relative)
            if previous != subject_relative:
                findings.append(
                    _finding(
                        "subject-identity-duplicate", subject_relative, str(previous)
                    )
                )
            entries_by_name = {entry.name: entry for entry in subject_entries}
            entries = set(entries_by_name)
            if not entries or not entries <= set(_ROLE_FILE):
                findings.append(
                    _finding(
                        "subject-role-membership-invalid",
                        subject_relative,
                        "one or more guide.md, policy.md, or runbook.md files required",
                    )
                )
            for filename in sorted(entries & set(_ROLE_FILE)):
                role_relative = subject_relative / filename
                require_tracked(role_relative)
                if not entries_by_name[filename].is_regular:
                    findings.append(
                        _finding(
                            "role-file-invalid",
                            role_relative,
                            "must be regular and symlink-free",
                        )
                    )
                    continue
                try:
                    role_text = _read_text(root, role_relative)
                    metadata = _frontmatter(role_text, role_relative)
                except OperationsAuthorityError as error:
                    findings.append(_finding(error.code, role_relative, str(error)))
                    continue
                role = _ROLE_FILE[filename]
                artifact = metadata.get("artifact_id")
                profile = profiles.get(role)
                if not isinstance(profile, Mapping):
                    findings.append(
                        _finding("role-profile-invalid", role_relative, role)
                    )
                    continue
                if not path_matches_pattern(role_relative, profile.get("path_pattern")):
                    findings.append(
                        _finding(
                            "role-path-profile-mismatch",
                            role_relative,
                            role,
                        )
                    )
                if profile.get("identity_relation") != "subject-member":
                    findings.append(
                        _finding(
                            "role-identity-relation-invalid",
                            role_relative,
                            str(profile.get("identity_relation")),
                        )
                    )
                if not _matches_artifact_pattern(
                    profile.get("artifact_id_pattern"), artifact
                ) or metadata.get("type") != document_type(role):
                    findings.append(
                        _finding("role-identity-invalid", role_relative, str(artifact))
                    )
                required_metadata = set(
                    _string_items(profile.get("required_frontmatter"))
                )
                if not required_metadata <= set(metadata):
                    findings.append(
                        _finding(
                            "role-profile-invalid",
                            role_relative,
                            "required metadata missing",
                        )
                    )
                allowed_statuses = _profile_statuses(registry, profile)
                if metadata.get("status") not in allowed_statuses:
                    findings.append(
                        _finding(
                            "role-status-invalid",
                            role_relative,
                            str(metadata.get("status")),
                        )
                    )
                headings = _headings(role_text)
                missing_sections = [
                    section
                    for section in _string_items(profile.get("required_sections"))
                    if not headings
                    & _ROLE_SECTION_ALIASES.get(role, {}).get(section, {section})
                ]
                if missing_sections:
                    findings.append(
                        _finding(
                            "role-sections-invalid",
                            role_relative,
                            ",".join(missing_sections),
                        )
                    )
                if isinstance(artifact, str):
                    previous_artifact = seen_artifacts.setdefault(
                        artifact, role_relative
                    )
                    if previous_artifact != role_relative:
                        findings.append(
                            _finding(
                                "role-identity-duplicate",
                                role_relative,
                                str(previous_artifact),
                            )
                        )

    incidents_relative = OPERATIONS_ROOT / "incidents"
    try:
        incident_entries = _directory_entries_bounded(
            root,
            incidents_relative,
            max_entries=MAX_INCIDENT_ENTRIES,
        )
    except OperationsAuthorityError as error:
        code = (
            "incident-bounds"
            if error.code == "directory-bounds"
            else "incident-root-invalid"
        )
        findings.append(_finding(code, incidents_relative, str(error)))
    else:
        incident_by_name = {entry.name: entry for entry in incident_entries}
        incident_readme = incident_by_name.get("README.md")
        if incident_readme is None or not incident_readme.is_regular:
            findings.append(
                _finding(
                    "incident-index-invalid",
                    incidents_relative / "README.md",
                    "regular README required",
                )
            )
        else:
            require_tracked(incidents_relative / "README.md")
        for year_entry in incident_entries:
            if year_entry.name == "README.md":
                continue
            year_relative = incidents_relative / year_entry.name
            if _YEAR.fullmatch(year_entry.name) is None or not year_entry.is_directory:
                findings.append(
                    _finding(
                        "incident-year-invalid",
                        year_relative,
                        "year is the only date exception",
                    )
                )
                continue
            try:
                year_entries = _directory_entries_bounded(
                    root,
                    year_relative,
                    max_entries=MAX_INCIDENT_YEAR_ENTRIES,
                )
            except OperationsAuthorityError as error:
                code = (
                    "incident-bounds"
                    if error.code == "directory-bounds"
                    else "incident-year-invalid"
                )
                findings.append(_finding(code, year_relative, str(error)))
                continue
            for packet_entry in year_entries:
                packet_relative = year_relative / packet_entry.name
                packet_match = _INCIDENT.fullmatch(packet_entry.name)
                if packet_match is None or not packet_entry.is_directory:
                    findings.append(
                        _finding(
                            "incident-packet-invalid", packet_relative, "invalid packet"
                        )
                    )
                    continue
                try:
                    packet_entries = _directory_entries_bounded(
                        root,
                        packet_relative,
                        max_entries=MAX_INCIDENT_PACKET_ENTRIES,
                    )
                except OperationsAuthorityError as error:
                    code = (
                        "incident-bounds"
                        if error.code == "directory-bounds"
                        else "incident-packet-invalid"
                    )
                    findings.append(_finding(code, packet_relative, str(error)))
                    continue
                entries = {entry.name for entry in packet_entries}
                if "incident.md" not in entries or not entries <= {
                    "incident.md",
                    "postmortem.md",
                }:
                    findings.append(
                        _finding(
                            "incident-roles-invalid",
                            packet_relative,
                            "incident required; postmortem optional",
                        )
                    )
                for child_entry in packet_entries:
                    child_relative = packet_relative / child_entry.name
                    require_tracked(child_relative)
                    if not child_entry.is_regular:
                        findings.append(
                            _finding(
                                "incident-role-file-invalid",
                                child_relative,
                                "must be regular",
                            )
                        )
                        continue
                    if child_entry.name not in {"incident.md", "postmortem.md"}:
                        continue
                    role = pathlib.PurePosixPath(child_entry.name).stem
                    try:
                        child_text = _read_text(root, child_relative)
                        metadata = _frontmatter(child_text, child_relative)
                    except OperationsAuthorityError as error:
                        findings.append(
                            _finding(error.code, child_relative, str(error))
                        )
                        continue
                    profile = profiles.get(role)
                    if not isinstance(profile, Mapping):
                        findings.append(
                            _finding("incident-profile-invalid", child_relative, role)
                        )
                        continue
                    if not path_matches_pattern(
                        child_relative, profile.get("path_pattern")
                    ):
                        findings.append(
                            _finding(
                                "incident-path-profile-mismatch",
                                child_relative,
                                role,
                            )
                        )
                    expected_relation = (
                        "direct" if role == "incident" else "package-member"
                    )
                    if profile.get("identity_relation") != expected_relation:
                        findings.append(
                            _finding(
                                "incident-identity-relation-invalid",
                                child_relative,
                                str(profile.get("identity_relation")),
                            )
                        )
                    required_metadata = set(
                        _string_items(profile.get("required_frontmatter"))
                    )
                    if not required_metadata <= set(metadata) or metadata.get(
                        "type"
                    ) != document_type(role):
                        findings.append(
                            _finding("incident-profile-invalid", child_relative, role)
                        )
                    allowed_statuses = _profile_statuses(registry, profile)
                    if metadata.get("status") not in allowed_statuses:
                        findings.append(
                            _finding(
                                "incident-status-invalid",
                                child_relative,
                                str(metadata.get("status")),
                            )
                        )
                    number = packet_match.group("number")
                    artifact_pattern = profile.get("artifact_id_pattern")
                    expected_id = (
                        artifact_pattern.replace("{number:4}", number).replace(
                            "{year:4}", child_relative.parts[3]
                        )
                        if isinstance(artifact_pattern, str)
                        else ""
                    )
                    if metadata.get("artifact_id") != expected_id:
                        findings.append(
                            _finding(
                                "incident-identity-invalid", child_relative, expected_id
                            )
                        )
                    parent_ids = metadata.get("parent_ids")
                    incident_profile = profiles.get("incident")
                    incident_pattern = (
                        incident_profile.get("artifact_id_pattern")
                        if isinstance(incident_profile, Mapping)
                        else None
                    )
                    expected_parent = (
                        incident_pattern.replace("{number:4}", number).replace(
                            "{year:4}", child_relative.parts[3]
                        )
                        if isinstance(incident_pattern, str)
                        else ""
                    )
                    if role == "postmortem" and (
                        not isinstance(parent_ids, list)
                        or expected_parent not in parent_ids
                    ):
                        findings.append(
                            _finding(
                                "incident-identity-invalid",
                                child_relative,
                                "incident parent required",
                            )
                        )
                    headings = _headings(child_text)
                    missing_sections = (
                        set(_string_items(profile.get("required_sections"))) - headings
                    )
                    if missing_sections:
                        findings.append(
                            _finding(
                                "incident-sections-invalid",
                                child_relative,
                                ",".join(sorted(missing_sections)),
                            )
                        )
                    created = _date_time(metadata.get("created"))
                    updated = _date_time(metadata.get("updated"))
                    if created is None or updated is None or updated < created:
                        findings.append(
                            _finding(
                                "incident-date-order-invalid",
                                child_relative,
                                "created/updated",
                            )
                        )
                    if role == "incident":
                        occurred = _date_time(metadata.get("occurred_at"))
                        resolved = _date_time(metadata.get("resolved_at"))
                        if occurred is None or str(occurred.year) != year_entry.name:
                            findings.append(
                                _finding(
                                    "incident-year-date-invalid",
                                    child_relative,
                                    year_entry.name,
                                )
                            )
                        if (
                            resolved is not None
                            and occurred is not None
                            and resolved < occurred
                        ):
                            findings.append(
                                _finding(
                                    "incident-date-order-invalid",
                                    child_relative,
                                    "resolved before occurred",
                                )
                            )
    return tuple(sorted(set(findings)))


# Current service inventory is a joined source projection, not another authority.
SERVICE_INVENTORY_PATH = pathlib.PurePosixPath(
    "docs/90.references/research/0002-agentic-engineering-research-pack/"
    "m0021-local-docker-service-consolidation.md"
)
SERVICE_INVENTORY_COLUMNS = (
    "Domain",
    "Component",
    "Compose path",
    "Service",
    "Profiles",
    "Runtime classification",
    "Consumer",
    "Dependencies",
    "Network",
    "Ports",
    "Persistence",
    "Env",
    "Secret metadata",
    "Resources",
    "Security",
    "Backup",
    "Operations docs",
    "Runtime version authority",
    "Update owner",
    "Disposition",
)
_INVENTORY_START = "<!-- current-service-inventory:start -->"
_INVENTORY_END = "<!-- current-service-inventory:end -->"
_INVENTORY_CLASSES = frozenset({"HOME", "DEV", "OPTIONAL", "LAB", "REMOVE", "MIGRATE"})


def _service_inventory_rows(text: str) -> list[dict[str, str]]:
    if text.count(_INVENTORY_START) != 1 or text.count(_INVENTORY_END) != 1:
        raise OperationsAuthorityError(
            "service-inventory-shape", "current inventory requires one bounded table"
        )
    section = text.split(_INVENTORY_START, 1)[1].split(_INVENTORY_END, 1)[0]
    lines = [line for line in section.splitlines() if line.startswith("|")]
    cells = [
        [cell.strip() for cell in line.strip().strip("|").split("|")] for line in lines
    ]
    if len(cells) < 2 or tuple(cells[0]) != SERVICE_INVENTORY_COLUMNS:
        raise OperationsAuthorityError(
            "service-inventory-shape",
            "current inventory requires all twenty named columns",
        )
    if any(len(row) != len(SERVICE_INVENTORY_COLUMNS) for row in cells[2:]):
        raise OperationsAuthorityError(
            "service-inventory-shape", "inventory row has wrong column count"
        )
    return [dict(zip(SERVICE_INVENTORY_COLUMNS, row, strict=True)) for row in cells[2:]]


def _inventory_cell(value: object) -> str:
    # Source expressions stay portable; never interpolate private instance values.
    if value in (None, {}, [], ()):
        return "none"
    return json.dumps(
        value, sort_keys=True, ensure_ascii=False, separators=(",", ":")
    ).replace("|", "&#124;")


def _inventory_link(path: pathlib.PurePosixPath, label: str | None = None) -> str:
    relative = posixpath.relpath(str(path), str(SERVICE_INVENTORY_PATH.parent))
    return f"[{label or path.as_posix()}]({relative})"


def _inventory_sources(
    root: pathlib.Path, paths: tuple[pathlib.PurePosixPath, ...]
) -> dict[tuple[str, str], Mapping[str, object]]:
    return {
        (str(path), str(name)): service
        for path in paths
        if _is_infra_compose_file(path)
        for name, service in _compose_mapping(root, path).get("services", {}).items()
        if isinstance(service, Mapping)
    }


def _inventory_inherited(
    root: pathlib.Path,
    path: pathlib.PurePosixPath,
    service: Mapping[str, object],
    tracked: frozenset[pathlib.PurePosixPath],
    chain: tuple[tuple[str, str], ...] = (),
) -> Mapping[str, object]:
    """Resolve scalar template defaults only; do not impersonate Compose rendering.

    Inventory topology/env/mount cells describe leaf source declarations. Resource
    scalars and security controls additionally identify inherited declarations.
    These fields do not require private environment or Docker daemon access.
    """
    extends = service.get("extends")
    if not isinstance(extends, Mapping):
        return service
    target = _safe_relative(
        posixpath.normpath(str(path.parent / str(extends.get("file", path.name)))),
        "extends source",
    )
    name = str(extends.get("service", ""))
    identity = (str(target), name)
    if target not in tracked or identity in chain or len(chain) >= 16:
        raise OperationsAuthorityError(
            "service-inventory-source", "untracked or cyclic extends source"
        )
    base = _compose_mapping(root, target).get("services", {}).get(name)
    if not isinstance(base, Mapping):
        raise OperationsAuthorityError(
            "service-inventory-source", "missing inherited service"
        )
    inherited = _inventory_inherited(root, target, base, tracked, (*chain, identity))
    return {**inherited, **service}


def _inventory_source_links(text: str, guide: pathlib.PurePosixPath) -> frozenset[str]:
    links = (
        token.attrGet("href")
        for block in MarkdownIt("commonmark").parse(text)
        for token in block.children or ()
        if token.type == "link_open"
    )
    return frozenset(
        posixpath.normpath(str(guide.parent / href.split("#", 1)[0]))
        for href in links
        if href and not re.match(r"[a-z]+://", href)
    )


def _inventory_bindings(
    root: pathlib.Path,
    paths: tuple[pathlib.PurePosixPath, ...],
    services: Mapping[tuple[str, str], object],
) -> tuple[dict[tuple[str, str], pathlib.PurePosixPath], list[CatalogFinding]]:
    owners: dict[tuple[str, str], pathlib.PurePosixPath] = {}
    findings: list[CatalogFinding] = []
    tracked = frozenset(paths)
    for guide in paths:
        if not (
            str(guide).startswith("docs/05.operations/catalog/")
            and guide.name == "guide.md"
        ):
            continue
        text = _read_text(root, guide)
        metadata = _frontmatter(text, guide)
        bindings = metadata.get("implementation_services")
        if bindings is None:
            continue
        if not isinstance(bindings, Mapping) or not bindings:
            findings.append(
                _finding(
                    "service-operations-owner",
                    guide,
                    "implementation_services must be a nonempty mapping",
                )
            )
            continue
        for compose, names in bindings.items():
            if (
                not isinstance(compose, str)
                or not _is_infra_compose_file(compose)
                or pathlib.PurePosixPath(compose) not in tracked
            ):
                findings.append(
                    _finding(
                        "service-operations-removed",
                        guide,
                        "binding source is not tracked current Compose",
                    )
                )
                continue
            links = _inventory_source_links(text, guide)
            if compose not in links or not (root / compose).is_file():
                findings.append(
                    _finding(
                        "service-guide-source",
                        guide,
                        f"Guide must link its existing Compose source: {compose}",
                    )
                )
            if (
                not isinstance(names, list)
                or not names
                or any(not isinstance(name, str) or not name for name in names)
            ):
                findings.append(
                    _finding(
                        "service-operations-owner",
                        guide,
                        "binding service list must be nonempty names",
                    )
                )
                continue
            for name in names:
                identity = (compose, name)
                if identity not in services:
                    findings.append(
                        _finding(
                            "service-operations-removed",
                            guide,
                            f"current Guide binds removed service {compose}#{name}",
                        )
                    )
                elif identity in owners:
                    findings.append(
                        _finding(
                            "service-operations-duplicate",
                            guide,
                            f"duplicate Guide binding for {compose}#{name}",
                        )
                    )
                else:
                    owners[identity] = guide
        for filename, kind in _ROLE_FILE.items():
            member = guide.parent / filename
            try:
                frontmatter = _frontmatter(_read_text(root, member), member)
                valid = frontmatter.get(
                    "type"
                ) == f"operation/{kind}" and frontmatter.get("status") in {
                    "active",
                    "draft",
                }
            except OperationsAuthorityError:
                valid = False
            if member not in tracked or not valid:
                findings.append(
                    _finding(
                        "service-operations-owner",
                        member,
                        "service ownership requires a current Guide/Policy/Runbook triplet",
                    )
                )
    for compose, name in sorted(set(services) - set(owners)):
        findings.append(
            _finding(
                "service-operations-missing",
                compose,
                f"service {name} has no current Guide binding",
            )
        )
    return owners, findings


def _inventory_version_authority(
    path: pathlib.PurePosixPath,
    service: Mapping[str, object],
    tracked: frozenset[pathlib.PurePosixPath],
) -> str:
    authority = [_inventory_link(path)]
    build = service.get("build")
    if isinstance(build, str):
        build = {"context": build}
    if isinstance(build, Mapping) and "dockerfile_inline" in build:
        authority.append("inline Dockerfile in Compose")
    elif isinstance(build, Mapping):
        context = posixpath.normpath(str(path.parent / str(build.get("context", "."))))
        dockerfile_value = str(build.get("dockerfile", "Dockerfile"))
        default = re.fullmatch(
            r"\$\{[A-Za-z_][A-Za-z_0-9]*:?-([^}]+)\}", dockerfile_value
        )
        if default:
            authority.append(
                "Dockerfile selector=" + dockerfile_value + " (declared default below)"
            )
            dockerfile_value = default.group(1)
        dockerfile = _safe_relative(
            posixpath.normpath(context + "/" + dockerfile_value), "build Dockerfile"
        )
        if dockerfile not in tracked:
            raise OperationsAuthorityError(
                "service-inventory-source",
                f"untracked build Dockerfile for {path}",
            )
        authority.append(_inventory_link(dockerfile))
    return "; ".join(authority)


def _inventory_persistence(
    root: pathlib.Path, path: pathlib.PurePosixPath, service: Mapping[str, object]
) -> str:
    source = _compose_mapping(root, path)
    volumes = service.get("volumes", [])
    declared_volumes = source.get("volumes", {})
    referenced = {
        str(item.get("source", ""))
        if isinstance(item, Mapping)
        else next(
            (
                str(name)
                for name in declared_volumes
                if str(item).startswith(str(name) + ":")
            ),
            "",
        )
        for item in volumes
    }
    mounts = {
        "mounts": volumes,
        "volume_sources": {
            name: value
            for name, value in declared_volumes.items()
            if name in referenced
        },
    }
    return _inventory_cell(mounts)


def _inventory_projection(
    root: pathlib.Path,
    identity: tuple[str, str],
    service: Mapping[str, object],
    owners: Mapping[tuple[str, str], pathlib.PurePosixPath],
    tracked: frozenset[pathlib.PurePosixPath],
) -> dict[str, str]:
    compose, name = identity
    path = pathlib.PurePosixPath(compose)
    inherited = _inventory_inherited(root, path, service, tracked)
    template = service.get("extends", {})
    security_keys = (
        "user",
        "privileged",
        "read_only",
        "security_opt",
        "cap_add",
        "cap_drop",
        "network_mode",
        "pid",
        "devices",
        "gpus",
    )
    security = {key: service[key] for key in security_keys if key in service}
    inherited_security = {
        key: inherited[key]
        for key in security_keys
        if key not in service and key in inherited
    }
    resources = {
        key: inherited[key]
        for key in ("cpus", "mem_limit", "mem_reservation", "pids_limit", "shm_size")
        if key in inherited
    }
    deploy = inherited.get("deploy")
    if isinstance(deploy, Mapping):
        resources["deploy"] = {
            **(
                deploy.get("resources", {})
                if isinstance(deploy.get("resources", {}), Mapping)
                else {}
            ),
            **({"replicas": deploy["replicas"]} if "replicas" in deploy else {}),
        }
    environment = service.get("environment", {})
    env_keys = sorted(
        environment
        if isinstance(environment, Mapping)
        else [str(item).split("=", 1)[0] for item in environment]
    )
    secrets = sorted(
        str(item.get("source", "")) if isinstance(item, Mapping) else str(item)
        for item in service.get("secrets", [])
    )
    guide = owners.get(identity)
    security["authentication_env_keys"] = [
        key for key in env_keys if re.search(r"AUTH|OIDC|SSO|COOKIE", key)
    ]
    labels = service.get("labels", {})
    if isinstance(labels, Mapping):
        security["router_middlewares"] = {
            key: value
            for key, value in labels.items()
            if str(key).endswith(".middlewares")
        }
    operations = (
        "; ".join(
            _inventory_link(guide.parent / member, member.removesuffix(".md"))
            for member in _ROLE_FILE
        )
        if guide
        else "unowned"
    )
    return {
        "Domain": path.parts[1],
        "Component": path.parent.name if len(path.parts) > 3 else name,
        "Compose path": compose,
        "Service": name,
        "Profiles": _inventory_cell(sorted(service.get("profiles", []))),
        "Dependencies": _inventory_cell(service.get("depends_on", {})),
        "Network": _inventory_cell(
            service.get("networks", service.get("network_mode", "default"))
        ),
        "Ports": _inventory_cell(
            {
                "published": service.get("ports", []),
                "exposed": service.get("expose", []),
            }
        ),
        "Persistence": _inventory_persistence(root, path, service),
        "Env": _inventory_cell(env_keys),
        "Secret metadata": _inventory_cell(secrets),
        "Resources": _inventory_cell(resources),
        "Security": "leaf="
        + _inventory_cell(security)
        + "; inherited-defaults="
        + _inventory_cell(inherited_security)
        + "; extends="
        + _inventory_cell(template)
        + "; runtime unverified; "
        + (
            _inventory_link(guide.parent / "policy.md", "Policy")
            if guide
            else "unowned"
        ),
        "Operations docs": operations,
        "Runtime version authority": _inventory_version_authority(
            path, service, tracked
        ),
        "Update owner": "Renovate; "
        + _inventory_link(pathlib.PurePosixPath("renovate.json5"))
        + "; POL-0086",
    }


def _inventory_consumer(
    row: Mapping[str, str], services: Mapping[tuple[str, str], Mapping[str, object]]
) -> str:
    names = sorted(
        name
        for (_, name), service in services.items()
        if row["Service"] in service.get("depends_on", {})
    )
    declared = "declared reverse edges=" + (",".join(names) or "none")
    value = row["Consumer"]
    if re.search(r"declared reverse edges=[^;]+", value):
        return re.sub(r"declared reverse edges=[^;]+", declared, value)
    return value + "; " + declared


def render_service_inventory(root: pathlib.Path) -> str:
    """Return a refreshed table, preserving authored evidence and disposition."""
    paths = _tracked_paths(root, MAX_TRACKED_FILES)
    services = _inventory_sources(root, paths)
    owners, _ = _inventory_bindings(root, paths, services)
    rows = _service_inventory_rows(_read_text(root, SERVICE_INVENTORY_PATH))
    identities = [(row["Compose path"], row["Service"]) for row in rows]
    if len(set(identities)) != len(identities) or set(identities) != set(services):
        raise OperationsAuthorityError(
            "service-inventory-membership",
            "author missing/extra/duplicate service rows before rendering",
        )
    output = [
        _INVENTORY_START,
        "| " + " | ".join(SERVICE_INVENTORY_COLUMNS) + " |",
        "| " + " | ".join("---" for _ in SERVICE_INVENTORY_COLUMNS) + " |",
    ]
    for row in rows:
        identity = (row["Compose path"], row["Service"])
        projected = {
            **row,
            **_inventory_projection(
                root, identity, services[identity], owners, frozenset(paths)
            ),
        }
        projected = {**projected, "Consumer": _inventory_consumer(row, services)}
        output.append(
            "| "
            + " | ".join(projected[column] for column in SERVICE_INVENTORY_COLUMNS)
            + " |"
        )
    return "\n".join((*output, _INVENTORY_END)) + "\n"


def validate_service_inventory(root: pathlib.Path) -> tuple[CatalogFinding, ...]:
    paths = _tracked_paths(root, MAX_TRACKED_FILES)
    services = _inventory_sources(root, paths)
    owners, findings = _inventory_bindings(root, paths, services)
    try:
        rows = _service_inventory_rows(_read_text(root, SERVICE_INVENTORY_PATH))
    except OperationsAuthorityError as error:
        return tuple(
            (*findings, _finding(error.code, SERVICE_INVENTORY_PATH, str(error)))
        )
    identities = [(row["Compose path"], row["Service"]) for row in rows]
    for identity, count in Counter(identities).items():
        if count > 1:
            findings.append(
                _finding(
                    "service-inventory-duplicate",
                    SERVICE_INVENTORY_PATH,
                    f"duplicate service identity {identity}",
                )
            )
    for identity in sorted(set(services) ^ set(identities)):
        findings.append(
            _finding(
                "service-inventory-membership",
                SERVICE_INVENTORY_PATH,
                f"missing or extra service {identity}",
            )
        )
    for row in rows:
        identity = (row["Compose path"], row["Service"])
        for column in SERVICE_INVENTORY_COLUMNS:
            if not row[column]:
                findings.append(
                    _finding(
                        "service-inventory-field",
                        SERVICE_INVENTORY_PATH,
                        f"{identity}: missing {column}",
                    )
                )
        if row["Runtime classification"] not in _INVENTORY_CLASSES:
            findings.append(
                _finding(
                    "service-inventory-classification",
                    SERVICE_INVENTORY_PATH,
                    f"{identity}: invalid classification",
                )
            )
        if identity not in services:
            continue
        expected = _inventory_projection(
            root, identity, services[identity], owners, frozenset(paths)
        )
        expected = {**expected, "Consumer": _inventory_consumer(row, services)}
        for column, value in expected.items():
            if row[column] != value:
                findings.append(
                    _finding(
                        "service-inventory-drift",
                        SERVICE_INVENTORY_PATH,
                        f"{identity}: stale {column}",
                    )
                )
    return tuple(findings)
