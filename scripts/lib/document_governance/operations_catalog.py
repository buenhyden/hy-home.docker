"""Bounded current-authority validation for Stage 05 Operations.

Registry + Migration 0003 own current structure. Migration 0002 is read only
for body-derived witnesses of its two already-executed role merges.
"""

from __future__ import annotations

import dataclasses
import datetime as dt
import errno
import hashlib
import json
import os
import pathlib
import re
import selectors
import signal
import stat
import subprocess
import time
from collections import Counter, defaultdict
from collections.abc import Mapping, Sequence

import yaml

from scripts.lib.document_governance.frontmatter import FrontmatterError, parse_frontmatter_text
from scripts.lib.document_governance.registry import validate_registry as validate_canonical_registry


TASK8_ROW_IDS = tuple(f"mig-0003-r{number:04d}" for number in range(257, 450))
EXPECTED_DOMAINS = (
    "00-workspace", "01-gateway", "02-auth", "03-security", "04-data",
    "05-messaging", "06-observability", "07-workflow", "08-ai",
    "09-tooling", "10-communication", "11-laboratory", "12-infra-net",
)
EXPECTED_ROLE_COUNTS = {"guide": 66, "policy": 64, "runbook": 62}
MIGRATION_PATH = pathlib.PurePosixPath(
    "docs/98.archive/migrations/mig-0003-workspace-governance-simplification.md"
)
SEMANTIC_WITNESS_PATH = pathlib.PurePosixPath(
    "docs/98.archive/migrations/mig-0002-operations-catalog-convergence.md"
)
REGISTRY_PATH = pathlib.PurePosixPath("docs/99.templates/registry.json")
OPERATIONS_ROOT = pathlib.PurePosixPath("docs/05.operations")
MAX_FILE_BYTES = 10_000_000
MAX_TRACKED_FILES = 10_000
MAX_TRACKED_BYTES = 300_000_000
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
MIGRATION_SHA256 = "271f21c50cf4ab765422ee552de244a4340c160e53149231eb6be45f03476ab9"
_EXPECTED_DELETED_TRACKED_PATHS = frozenset({
    pathlib.PurePosixPath("docs/05.operations/releases/README.md"),
    pathlib.PurePosixPath("docs/99.templates/templates/operations/release.template.md"),
})
_ACTIVE_REFERENCE_HISTORY_EXCLUSIONS = frozenset({
    # This support ledger pins the pre-convergence Task 1 source set.
    pathlib.PurePosixPath(
        "docs/99.templates/support/document-corpus-migration-contract.yaml"
    ),
})

_ROW_FIELDS = frozenset({
    "row_id", "source_path", "target_path", "artifact_id", "action",
    "owner_task", "source_kind", "source_owner_task", "active_consumers",
    "recovery_commit", "status",
})
_SUBJECT = re.compile(r"(?P<number>[0-9]{4})-(?P<slug>[a-z0-9][a-z0-9-]*)")
_YEAR = re.compile(r"[0-9]{4}")
_INCIDENT = re.compile(r"inc-(?P<number>[0-9]{4})-[a-z0-9][a-z0-9-]*")
_ROLE_FILE = {"guide.md": "guide", "policy.md": "policy", "runbook.md": "runbook"}
_OPERATIONS_PROFILE_CONTRACT = {
    "guide": {
        "profile_id": "guide",
        "frontmatter_policy": "required",
        "path_pattern": "docs/05.operations/catalog/{domain}/{subject_number:4}-{slug}/guide.md",
        "artifact_id_pattern": "guide-{number:4}",
        "identity_relation": "subject-member",
        "template_id": "operations/guide",
        "required_frontmatter": ("profile_id", "status", "artifact_id", "artifact_type", "parent_ids", "created", "updated"),
        "optional_frontmatter": ("reviewed_at", "next_review_at", "supersedes", "superseded_by"),
        "lifecycle_id": "living",
        "traceability": {
            "allowed_parent_profiles": ("spec", "policy", "runbook"),
            "membership_authority": "operations-migration-manifest",
        },
        "required_sections": ("Purpose", "Audience", "Prerequisites", "Usage", "Troubleshooting", "Verification", "Traceability"),
        "optional_sections": ("Examples",),
        "exceptions": (),
    },
    "policy": {
        "profile_id": "policy",
        "frontmatter_policy": "required",
        "path_pattern": "docs/05.operations/catalog/{domain}/{subject_number:4}-{slug}/policy.md",
        "artifact_id_pattern": "policy-{number:4}",
        "identity_relation": "subject-member",
        "template_id": "operations/policy",
        "required_frontmatter": ("profile_id", "status", "artifact_id", "artifact_type", "parent_ids", "created", "updated"),
        "optional_frontmatter": ("reviewed_at", "next_review_at", "supersedes", "superseded_by"),
        "lifecycle_id": "living",
        "traceability": {
            "allowed_parent_profiles": ("requirements-package", "architecture-description", "adr", "spec"),
            "membership_authority": "operations-migration-manifest",
        },
        "required_sections": ("Purpose", "Scope", "Policy Statements", "Enforcement", "Exceptions", "Verification", "Traceability"),
        "optional_sections": ("Definitions",),
        "exceptions": (),
    },
    "runbook": {
        "profile_id": "runbook",
        "frontmatter_policy": "required",
        "path_pattern": "docs/05.operations/catalog/{domain}/{subject_number:4}-{slug}/runbook.md",
        "artifact_id_pattern": "runbook-{number:4}",
        "identity_relation": "subject-member",
        "template_id": "operations/runbook",
        "required_frontmatter": ("profile_id", "status", "artifact_id", "artifact_type", "parent_ids", "created", "updated"),
        "optional_frontmatter": ("reviewed_at", "next_review_at", "supersedes", "superseded_by"),
        "lifecycle_id": "living",
        "traceability": {
            "allowed_parent_profiles": ("spec", "guide", "policy", "task"),
            "membership_authority": "operations-migration-manifest",
        },
        "required_sections": ("Purpose", "Trigger", "Prerequisites", "Procedure", "Verification", "Rollback", "Escalation", "Traceability"),
        "optional_sections": ("Automation",),
        "exceptions": (),
    },
    "incident": {
        "profile_id": "incident",
        "frontmatter_policy": "required",
        "path_pattern": "docs/05.operations/incidents/{year:4}/inc-{number:4}-{slug}/incident.md",
        "artifact_id_pattern": "inc-{number:4}",
        "identity_relation": "direct",
        "template_id": "operations/incident",
        "required_frontmatter": ("profile_id", "status", "artifact_id", "artifact_type", "parent_ids", "created", "updated", "occurred_at"),
        "optional_frontmatter": ("resolved_at",),
        "lifecycle_id": "incident",
        "traceability": {"allowed_parent_profiles": ("runbook",)},
        "required_sections": ("Summary", "Impact", "Coordination", "Timeline", "Mitigation", "Current Status", "Corrective Actions", "Traceability"),
        "optional_sections": ("Communications",),
        "exceptions": ({"kind": "year-directory"},),
    },
    "postmortem": {
        "profile_id": "postmortem",
        "frontmatter_policy": "required",
        "path_pattern": "docs/05.operations/incidents/{year:4}/inc-{number:4}-{slug}/postmortem.md",
        "artifact_id_pattern": "postmortem-{number:4}",
        "identity_relation": "package-member",
        "template_id": "operations/postmortem",
        "required_frontmatter": ("profile_id", "status", "artifact_id", "artifact_type", "parent_ids", "created", "updated", "reviewed_at"),
        "optional_frontmatter": ("supersedes", "superseded_by"),
        "lifecycle_id": "point-in-time",
        "traceability": {"allowed_parent_profiles": ("incident",)},
        "required_sections": ("Summary", "Impact", "Timeline", "Root Cause", "Contributing Factors", "Detection and Response", "Corrective Actions", "Learning", "Traceability"),
        "optional_sections": ("Follow-up Review",),
        "exceptions": ({"kind": "year-directory"},),
    },
}
_OPERATIONS_LIFECYCLE_CONTRACT = {
    "living": {
        "statuses": ("draft", "active", "superseded", "retired"),
        "transitions": {
            "draft": ("active", "retired"),
            "active": ("superseded", "retired"),
            "superseded": (),
            "retired": (),
        },
    },
    "incident": {
        "statuses": ("open", "mitigated", "closed"),
        "transitions": {
            "open": ("mitigated", "closed"),
            "mitigated": ("closed",),
            "closed": (),
        },
    },
    "point-in-time": {
        "statuses": ("draft", "active", "superseded", "retired"),
        "transitions": {
            "draft": ("active", "retired"),
            "active": ("superseded", "retired"),
            "superseded": (),
            "retired": (),
        },
    },
}
_OPERATIONS_LIFECYCLE_STATUSES = {
    lifecycle_id: tuple(contract["statuses"])
    for lifecycle_id, contract in _OPERATIONS_LIFECYCLE_CONTRACT.items()
}
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
        "Verification": {"Verification", "Evidence", "Verification Steps", "Verification Record"},
        "Rollback": {"Rollback", "Rollback or Recovery"},
        "Escalation": {"Escalation"},
        "Traceability": {"Traceability", "Related Documents"},
    },
}
_SEMANTIC_MERGE_IDENTITIES = (
    (
        "docs/05.operations/" "00-workspace/ops-0005-harness-agent-first-engineering-validation/runbook.md",
        "6f2703d8d245cf4e3576bece0bf247dd516b2bf3",
        "d3da293e44cfc19e47af7169bdd146ae381202a8",
        "runbook",
        "docs/05.operations/" "catalog/00-workspace/ops-0005-harness-agent-first-engineering-validation/runbook.md",
        "docs/05.operations/" "catalog/00-workspace/ops-0004-harness-agent-first-engineering/runbook.md",
        "docs/05.operations/" "catalog/00-workspace/ops-0004-harness-agent-first-engineering/runbook.md",
        "docs/05.operations/catalog/00-workspace/0004-harness-agent-first-engineering/runbook.md",
    ),
    (
        "docs/05.operations/" "07-workflow/ops-0052-dag-deployment/policy.md",
        "6f2703d8d245cf4e3576bece0bf247dd516b2bf3",
        "2ef693b98a0cd0ff7fd9aba08adf2163bb486063",
        "policy",
        "docs/05.operations/" "catalog/07-workflow/ops-0052-dag-deployment/policy.md",
        "docs/05.operations/" "catalog/07-workflow/ops-0051-airflow-dag-lifecycle/policy.md",
        "docs/05.operations/" "catalog/07-workflow/ops-0051-airflow-dag-lifecycle/policy.md",
        "docs/05.operations/catalog/07-workflow/0051-airflow-dag-lifecycle/policy.md",
    ),
)
MAX_SEMANTIC_WITNESS_BYTES = 4_096
_ACTIVE_ROUTE_PATTERNS = (
    re.compile(r"docs/05\.operations/[^\s`)'\"]+/ops-(?:#{4}|\*|[0-9]{4})(?:[-/])"),
    re.compile(
        r"docs/05\.operations/(?:\{(?:guides[|,]policies[|,]runbooks)(?:[|,]incidents)?\}|guides|policies|runbooks)(?:[/}`]|$)"
    ),
)
_RELEASE_ROLE_PATTERN = re.compile(
    r"(?:\|\s*Release\s*\||(?:guide|policy|runbook|incident|postmortem)(?:\s*,\s*|\s+and\s+)release\b|Release (?:document )?role)",
    re.IGNORECASE,
)
_RELEASE_NEGATIONS = (
    "no release", "not maintain", "does not maintain", "without a release",
    "release absence", "release is absent", "release role and route are unnecessary",
    "no separate release", "remove release", "retired release",
    "a separate release document role",
)
_SPEC_IMPLEMENTATION_EVIDENCE_EXCLUSIONS = frozenset(
    {
        pathlib.PurePosixPath("docs/03.specs/0136-sdlc-taxonomy-convergence/spec.md"),
        pathlib.PurePosixPath("docs/03.specs/0136-sdlc-taxonomy-convergence/plan.md"),
        pathlib.PurePosixPath(
            "docs/03.specs/0136-sdlc-taxonomy-convergence/tasks/tsk-0001-taxonomy-convergence.md"
        ),
        pathlib.PurePosixPath(
            "docs/03.specs/0153-workspace-governance-simplification/spec.md"
        ),
        pathlib.PurePosixPath(
            "docs/03.specs/0153-workspace-governance-simplification/plan.md"
        ),
    }
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
class MigrationRow:
    row_id: str
    source_path: pathlib.PurePosixPath
    target_path: pathlib.PurePosixPath | None
    artifact_id: str | None
    action: str
    owner_task: int
    source_kind: str
    source_owner_task: int | None
    active_consumers: tuple[pathlib.PurePosixPath, ...]
    recovery_commit: str | None
    status: str


@dataclasses.dataclass(frozen=True)
class Task8Migration:
    rows: tuple[MigrationRow, ...]
    all_rows: tuple[MigrationRow, ...]


@dataclasses.dataclass(frozen=True)
class ConsumerInventory:
    declared_raw: tuple[pathlib.PurePosixPath, ...]
    declared_current: tuple[pathlib.PurePosixPath, ...]
    live: tuple[pathlib.PurePosixPath, ...]
    live_only: tuple[pathlib.PurePosixPath, ...]
    union: tuple[pathlib.PurePosixPath, ...]
    excluded: tuple[pathlib.PurePosixPath, ...]
    tracked_files: int
    tracked_bytes: int


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

    if not arguments or any(not isinstance(item, str) or "\0" in item for item in arguments):
        raise OperationsAuthorityError("git-arguments-invalid", "Git arguments must be nonempty text")
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
    streams = {process.stdout: ("stdout", stdout_limit), process.stderr: ("stderr", stderr_limit)}
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
                failure = OperationsAuthorityError("git-deadline", "Git deadline exceeded")
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
                    failure = OperationsAuthorityError("git-output-bounds", "Git output bound exceeded")
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
            raise OperationsAuthorityError("git-deadline", "Git deadline exceeded") from error
        return GitCommandResult(returncode, bytes(output["stdout"]), bytes(output["stderr"]))
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
        directory_descriptor = os.open(root, directory_flags)
        for part in relative.parts[:-1]:
            component = os.stat(part, dir_fd=directory_descriptor, follow_symlinks=False)
            if stat.S_ISLNK(component.st_mode):
                raise OperationsAuthorityError("symlink-invalid", f"symlink input: {relative}")
            if not stat.S_ISDIR(component.st_mode):
                raise OperationsAuthorityError("file-not-regular", f"non-directory component: {relative}")
            next_descriptor = os.open(part, directory_flags, dir_fd=directory_descriptor)
            opened = os.fstat(next_descriptor)
            if (component.st_dev, component.st_ino) != (opened.st_dev, opened.st_ino):
                os.close(next_descriptor)
                raise OperationsAuthorityError("file-raced", f"changed before read: {relative}")
            os.close(directory_descriptor)
            directory_descriptor = next_descriptor
        path_stat = os.stat(relative.name, dir_fd=directory_descriptor, follow_symlinks=False)
        if stat.S_ISLNK(path_stat.st_mode):
            raise OperationsAuthorityError("symlink-invalid", f"symlink input: {relative}")
        if not stat.S_ISREG(path_stat.st_mode):
            raise OperationsAuthorityError("file-not-regular", f"not regular: {relative}")
        descriptor = os.open(relative.name, file_flags, dir_fd=directory_descriptor)
        opened = os.fstat(descriptor)
        if (
            not stat.S_ISREG(opened.st_mode)
            or (opened.st_dev, opened.st_ino) != (path_stat.st_dev, path_stat.st_ino)
        ):
            raise OperationsAuthorityError("file-raced", f"changed before read: {relative}")
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


def _regular_file_size(root: pathlib.Path, relative: pathlib.PurePosixPath) -> int:
    directory_descriptor, descriptor, opened = _open_anchored_regular(root, relative)
    try:
        return opened.st_size
    finally:
        os.close(descriptor)
        os.close(directory_descriptor)


def _directory_entries_bounded(
    root: pathlib.Path,
    relative: pathlib.PurePosixPath,
    *,
    max_entries: int,
) -> tuple[BoundedDirectoryEntry, ...]:
    """Stream one directory through anchored descriptors and reject identity races."""

    if isinstance(max_entries, bool) or not isinstance(max_entries, int) or max_entries < 1:
        raise OperationsAuthorityError("bounds-invalid", "max_entries must be a positive integer")
    effective_limit = min(max_entries, MAX_DIRECTORY_ENTRIES)
    relative = _safe_relative(relative.as_posix(), "directory path")
    if not relative.parts:
        raise OperationsAuthorityError("path-invalid", "directory path must be nonempty")
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
                    "directory-raced", f"directory changed before enumeration: {relative}"
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
        raise OperationsAuthorityError("bounds-invalid", "max_bytes must be a positive integer")
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
                raise OperationsAuthorityError("file-too-large", f"bound exceeded: {relative}")
        after = os.fstat(descriptor)
        if (
            identity != (after.st_dev, after.st_ino)
            or before.st_size != after.st_size
            or before.st_mtime_ns != after.st_mtime_ns
        ):
            raise OperationsAuthorityError("file-raced", f"changed during read: {relative}")
        return b"".join(chunks)
    finally:
        os.close(descriptor)
        os.close(directory_descriptor)


def _read_text(root: pathlib.Path, relative: pathlib.PurePosixPath) -> str:
    try:
        return read_bounded_regular(root, relative).decode("utf-8")
    except UnicodeDecodeError as error:
        raise OperationsAuthorityError("utf8-invalid", f"invalid UTF-8: {relative}") from error


class _UniqueKeyLoader(yaml.SafeLoader):
    pass


def _construct_unique_mapping(
    loader: _UniqueKeyLoader,
    node: yaml.MappingNode,
    deep: bool = False,
) -> dict[object, object]:
    result: dict[object, object] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                f"duplicate YAML key: {key}",
                key_node.start_mark,
            )
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


_UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_unique_mapping,
)


def _fenced_yaml(text: str, heading: str) -> Mapping[str, object]:
    try:
        value = yaml.load(
            text.split(heading, 1)[1].split("```yaml", 1)[1].split("```", 1)[0],
            Loader=_UniqueKeyLoader,
        )
    except (IndexError, yaml.YAMLError) as error:
        raise OperationsAuthorityError(
            "migration-invalid", f"invalid {heading} YAML: {error}"
        ) from error
    if not isinstance(value, Mapping):
        raise OperationsAuthorityError("migration-invalid", "migration body is not a mapping")
    return value


def _parse_row(value: object) -> MigrationRow:
    if not isinstance(value, Mapping) or set(value) != _ROW_FIELDS:
        raise OperationsAuthorityError("migration-row-invalid", "row fields are not exact")
    consumers_value = value["active_consumers"]
    if not isinstance(consumers_value, list):
        raise OperationsAuthorityError("migration-row-invalid", "consumers must be a list")
    consumers = tuple(_safe_relative(item, "consumer") for item in consumers_value)
    if consumers != tuple(sorted(set(consumers))):
        raise OperationsAuthorityError("migration-row-invalid", "consumers must be sorted and unique")
    target_value = value["target_path"]
    artifact = value["artifact_id"]
    if artifact is not None and (not isinstance(artifact, str) or not artifact):
        raise OperationsAuthorityError("migration-row-invalid", "artifact_id must be text or null")
    row_id = value["row_id"]
    action = value["action"]
    owner_task = value["owner_task"]
    source_kind = value["source_kind"]
    source_owner_task = value["source_owner_task"]
    recovery_commit = value["recovery_commit"]
    status_value = value["status"]
    if not isinstance(row_id, str) or not isinstance(action, str):
        raise OperationsAuthorityError("migration-row-invalid", "row identity/action must be text")
    if action not in {"rename", "delete"}:
        raise OperationsAuthorityError("migration-row-invalid", f"action invalid: {row_id}")
    if (action == "rename") != (target_value is not None):
        raise OperationsAuthorityError("migration-row-invalid", f"target_path/action invalid: {row_id}")
    if isinstance(owner_task, bool) or not isinstance(owner_task, int) or owner_task < 1:
        raise OperationsAuthorityError("migration-row-invalid", f"owner_task invalid: {row_id}")
    if source_kind not in {"tracked", "planned-output"}:
        raise OperationsAuthorityError("migration-row-invalid", f"source_kind invalid: {row_id}")
    if source_kind == "tracked" and source_owner_task is not None:
        raise OperationsAuthorityError("migration-row-invalid", f"source_owner_task invalid: {row_id}")
    if source_kind == "planned-output" and (
        isinstance(source_owner_task, bool)
        or not isinstance(source_owner_task, int)
        or source_owner_task < 1
    ):
        raise OperationsAuthorityError("migration-row-invalid", f"source_kind owner invalid: {row_id}")
    if recovery_commit is not None:
        raise OperationsAuthorityError("migration-row-invalid", f"recovery_commit invalid: {row_id}")
    if status_value != "planned":
        raise OperationsAuthorityError("migration-row-invalid", f"status invalid: {row_id}")
    return MigrationRow(
        row_id=row_id,
        source_path=_safe_relative(value["source_path"], "source_path"),
        target_path=None if target_value is None else _safe_relative(target_value, "target_path"),
        artifact_id=artifact,
        action=action,
        owner_task=owner_task,
        source_kind=source_kind,
        source_owner_task=source_owner_task,
        active_consumers=consumers,
        recovery_commit=recovery_commit,
        status=status_value,
    )


def load_task8_migration(
    root: pathlib.Path,
    relative: pathlib.PurePosixPath = MIGRATION_PATH,
) -> Task8Migration:
    if relative != MIGRATION_PATH:
        raise OperationsAuthorityError(
            "structural-authority-invalid", "current structure must use Migration 0003"
        )
    migration_bytes = read_bounded_regular(root, relative)
    try:
        migration_text = migration_bytes.decode("utf-8")
    except UnicodeDecodeError as error:
        raise OperationsAuthorityError("utf8-invalid", f"invalid UTF-8: {relative}") from error
    ledger = _fenced_yaml(migration_text, "## Archive Ledger")
    if ledger.get("schema_version") != 2 or ledger.get("migration_id") != "mig-0003":
        raise OperationsAuthorityError("structural-authority-invalid", "unexpected migration authority")
    raw_rows = ledger.get("rows")
    if not isinstance(raw_rows, list) or len(raw_rows) != 903:
        raise OperationsAuthorityError("migration-bounds", "row bound exceeded")
    all_rows = tuple(_parse_row(value) for value in raw_rows)
    expected_all_ids = tuple(f"mig-0003-r{number:04d}" for number in range(1, 904))
    if tuple(row.row_id for row in all_rows) != expected_all_ids:
        raise OperationsAuthorityError("migration-row-invalid", "full row order is not exact")
    sources = tuple(row.source_path for row in all_rows)
    targets = tuple(row.target_path for row in all_rows if row.target_path is not None)
    if len(set(sources)) != len(sources):
        raise OperationsAuthorityError("migration-row-invalid", "source_path values are not unique")
    if len(set(targets)) != len(targets):
        raise OperationsAuthorityError("migration-row-invalid", "target_path values are not unique")
    rows_by_id = {row.row_id: row for row in all_rows}
    if len(rows_by_id) != len(all_rows):
        raise OperationsAuthorityError("migration-row-invalid", "duplicate row_id")
    try:
        rows = tuple(rows_by_id[row_id] for row_id in TASK8_ROW_IDS)
    except KeyError as error:
        raise OperationsAuthorityError("task8-rows-invalid", f"missing row: {error}") from error
    selected = tuple(row.row_id for row in all_rows if row.row_id in set(TASK8_ROW_IDS))
    if selected != TASK8_ROW_IDS:
        raise OperationsAuthorityError("task8-rows-invalid", "Task 8 rows are not exact and ordered")
    if Counter(row.action for row in rows) != Counter({"rename": 192, "delete": 1}):
        raise OperationsAuthorityError("task8-actions-invalid", "expected 192 rename and one delete")
    if tuple(row.action for row in rows) != ("rename",) * 192 + ("delete",):
        raise OperationsAuthorityError("task8-actions-invalid", "Task 8 actions are not ordered")
    for row in rows:
        if (
            row.owner_task != 8
            or row.source_kind != "tracked"
            or row.source_owner_task is not None
            or row.recovery_commit is not None
            or row.status != "planned"
        ):
            raise OperationsAuthorityError("task8-row-invalid", f"owner_task/source/status: {row.row_id}")
        if row.action == "rename":
            if row.target_path is None or row.source_path.name != row.target_path.name:
                raise OperationsAuthorityError("task8-row-invalid", row.row_id)
            if not row.source_path.parent.name.startswith("ops-") or (
                row.target_path.parent.name != row.source_path.parent.name[4:]
            ):
                raise OperationsAuthorityError("task8-row-invalid", row.row_id)
        elif (
            row.source_path.as_posix() != "docs/05.operations/releases/README.md"
            or row.target_path is not None
        ):
            raise OperationsAuthorityError("task8-row-invalid", row.row_id)
    if hashlib.sha256(migration_bytes).hexdigest() != MIGRATION_SHA256:
        raise OperationsAuthorityError("migration-digest-invalid", "frozen digest mismatch")
    return Task8Migration(rows=rows, all_rows=all_rows)


def _tracked_paths(root: pathlib.Path, max_files: int) -> tuple[pathlib.PurePosixPath, ...]:
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
        raise OperationsAuthorityError("tracked-file-bounds", "tracked file bound exceeded")
    try:
        return tuple(_safe_relative(item.decode(), "tracked path") for item in raw)
    except UnicodeDecodeError as error:
        raise OperationsAuthorityError("tracked-path-utf8", "tracked path is not UTF-8") from error


def _excluded(path: pathlib.PurePosixPath) -> bool:
    value = path.as_posix()
    return value.startswith((
        "docs/98.archive/", "graphify-out/", "docs/90.references/research/",
        "docs/90.references/audits/", "docs/90.references/llm-wiki/",
        "docs/90.references/data/knowledge/", "docs/90.references/data/security/",
        "docs/90.references/data/governance/document-corpus-lifecycle/",
    ))


def _current_route(
    root: pathlib.Path,
    path: pathlib.PurePosixPath,
    rows_by_source: Mapping[pathlib.PurePosixPath, MigrationRow],
) -> pathlib.PurePosixPath | None:
    seen: set[pathlib.PurePosixPath] = set()
    current = path
    while current not in seen:
        seen.add(current)
        target = root / current
        if target.is_file() and not target.is_symlink() and not _has_symlink_component(root, current):
            return current
        row = rows_by_source.get(current)
        if row is None or row.target_path is None:
            return None
        current = row.target_path
    raise OperationsAuthorityError("consumer-route-cycle", str(path))


def extract_task8_consumers(
    root: pathlib.Path,
    migration: Task8Migration,
    *,
    max_files: int = MAX_TRACKED_FILES,
    max_bytes: int = MAX_TRACKED_BYTES,
) -> ConsumerInventory:
    """Return the bounded declared/live Task 8 consumer union."""
    if max_files < 1 or max_bytes < 1:
        raise OperationsAuthorityError("bounds-invalid", "consumer bounds must be positive")
    effective_max_files = min(max_files, MAX_TRACKED_FILES)
    effective_max_bytes = min(max_bytes, MAX_TRACKED_BYTES)
    tracked = _tracked_paths(root, effective_max_files)
    routes = {row.source_path: row for row in migration.all_rows}
    declared_raw = tuple(sorted({item for row in migration.rows for item in row.active_consumers}))
    declared_current: set[pathlib.PurePosixPath] = set()
    excluded: set[pathlib.PurePosixPath] = set()
    for path in declared_raw:
        current = _current_route(root, path, routes)
        if current is None or _excluded(current):
            excluded.add(path)
        else:
            declared_current.add(current)
    tokens = {row.source_path.as_posix() for row in migration.rows}
    tokens.update(
        f"{row.source_path.parent.name}/{row.source_path.name}"
        for row in migration.rows if row.action == "rename"
    )

    tokens.add("docs/05.operations/releases/")
    live: set[pathlib.PurePosixPath] = set()
    total = 0
    for path in tracked:
        if path in _EXPECTED_DELETED_TRACKED_PATHS:
            continue
        total += _regular_file_size(root, path)
        if total > effective_max_bytes:
            raise OperationsAuthorityError("tracked-byte-bounds", "tracked byte bound exceeded")
        if _excluded(path):
            continue
        data = read_bounded_regular(root, path, max_bytes=min(MAX_FILE_BYTES, effective_max_bytes))
        try:
            text = data.decode()
        except UnicodeDecodeError:
            continue
        if any(token in text for token in tokens):
            live.add(path)
    return ConsumerInventory(
        declared_raw=declared_raw,
        declared_current=tuple(sorted(declared_current)),
        live=tuple(sorted(live)),
        live_only=tuple(sorted(live - declared_current)),
        union=tuple(sorted(live | declared_current)),
        excluded=tuple(sorted(excluded)),
        tracked_files=len(tracked),
        tracked_bytes=total,
    )


def _active_reference_scan_excluded(path: pathlib.PurePosixPath) -> bool:
    value = path.as_posix()
    return (
        _excluded(path)
        or value.startswith("docs/90.references/")
        or path in _EXPECTED_DELETED_TRACKED_PATHS
        or path in _ACTIVE_REFERENCE_HISTORY_EXCLUSIONS
        or path in _SPEC_IMPLEMENTATION_EVIDENCE_EXCLUSIONS
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
            text = read_bounded_regular(root, path).decode("utf-8")
        except UnicodeDecodeError:
            continue
        for line_number, line in enumerate(text.splitlines(), 1):
            old_route = any(pattern.search(line) for pattern in _ACTIVE_ROUTE_PATTERNS)
            release_role = suffix == ".md" and _RELEASE_ROLE_PATTERN.search(line) and not any(
                token in line.lower() for token in _RELEASE_NEGATIONS
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


def _frontmatter(text: str, path: pathlib.PurePosixPath) -> Mapping[str, object]:
    if not text.startswith("---\n"):
        raise OperationsAuthorityError("frontmatter-missing", str(path))
    try:
        value = parse_frontmatter_text(text)
    except FrontmatterError as error:
        raise OperationsAuthorityError("frontmatter-invalid", str(path)) from error
    return value


def _load_registry(root: pathlib.Path) -> Mapping[str, object]:
    def unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
        result: dict[str, object] = {}
        for key, value in pairs:
            if key in result:
                raise OperationsAuthorityError("registry-invalid", f"duplicate JSON member: {key}")
            result[key] = value
        return result

    try:
        value = json.loads(_read_text(root, REGISTRY_PATH), object_pairs_hook=unique_object)
    except json.JSONDecodeError as error:
        raise OperationsAuthorityError("registry-invalid", str(error)) from error
    if not isinstance(value, Mapping):
        raise OperationsAuthorityError("registry-invalid", "Registry must be an object")
    return value


def _validate_registry(registry: Mapping[str, object]) -> list[CatalogFinding]:
    profiles = registry.get("profiles")
    roles = registry.get("template_roles")
    if not isinstance(profiles, list) or not isinstance(roles, Mapping):
        return [_finding("registry-invalid", REGISTRY_PATH, "profile/template collections invalid")]
    findings: list[CatalogFinding] = [
        _finding("registry-canonical-invalid", REGISTRY_PATH, f"{item.code}:{item.path}")
        for item in validate_canonical_registry(registry)
    ]
    profile_ids = [item.get("profile_id") for item in profiles if isinstance(item, Mapping)]
    duplicates = {item for item in profile_ids if isinstance(item, str) and profile_ids.count(item) > 1}
    if duplicates:
        findings.append(_finding("registry-profile-duplicate", REGISTRY_PATH, str(sorted(duplicates))))
    by_id = {item.get("profile_id"): item for item in profiles if isinstance(item, Mapping)}
    for profile_id, contract in _OPERATIONS_PROFILE_CONTRACT.items():
        profile = by_id.get(profile_id)
        if not isinstance(profile, Mapping):
            findings.append(_finding("registry-operations-profile-invalid", REGISTRY_PATH, profile_id))
            continue
        if set(profile) != set(contract):
            findings.append(
                _finding("registry-operations-profile-invalid", REGISTRY_PATH, f"{profile_id}.fields")
            )
        for key, expected in contract.items():
            actual = profile.get(key)
            if _contract_value(actual) != _contract_value(expected):
                findings.append(
                    _finding("registry-operations-profile-invalid", REGISTRY_PATH, f"{profile_id}.{key}")
                )
        role = roles.get(f"operations/{profile_id}")
        expected_role = {
            "source": f"docs/99.templates/templates/operations/{profile_id}.template.md",
            "profile_id": profile_id,
        }
        if role != expected_role:
            findings.append(
                _finding("registry-operations-profile-invalid", REGISTRY_PATH, f"operations/{profile_id}")
            )
    role_sections = [
        tuple(by_id[role].get("required_sections", ()))
        for role in ("guide", "policy", "runbook")
        if isinstance(by_id.get(role), Mapping)
    ]
    if len(role_sections) != len(set(role_sections)):
        findings.append(
            _finding("registry-role-purpose-duplicate", REGISTRY_PATH, "role sections must differ")
        )
    if "release" in by_id or "operations/release" in roles or "release.template" in json.dumps(registry):
        findings.append(_finding("release-authority-present", REGISTRY_PATH, "Release remains registered"))
    lifecycles = registry.get("lifecycles")
    for lifecycle_id, expected_lifecycle in _OPERATIONS_LIFECYCLE_CONTRACT.items():
        lifecycle = lifecycles.get(lifecycle_id) if isinstance(lifecycles, Mapping) else None
        if _contract_value(lifecycle) != _contract_value(expected_lifecycle):
            findings.append(
                _finding(
                    "registry-operations-lifecycle-invalid",
                    REGISTRY_PATH,
                    lifecycle_id,
                )
            )
    return findings


def _contract_value(value: object) -> object:
    if isinstance(value, Mapping):
        return tuple(sorted((str(key), _contract_value(item)) for key, item in value.items()))
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return tuple(_contract_value(item) for item in value)
    return value


def _headings(text: str) -> set[str]:
    return {
        match.group(1).strip()
        for line in text.splitlines()
        if (match := re.fullmatch(r" {0,3}##\s+(.+?)\s*#*", line))
    }


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


def _prefixless(path: pathlib.PurePosixPath) -> pathlib.PurePosixPath:
    parts = list(path.parts)
    if len(parts) > 4 and parts[4].startswith("ops-"):
        parts[4] = parts[4][4:]
    return pathlib.PurePosixPath(*parts)


def _markdown_body_text(text: str) -> str:
    """Return Markdown prose excluding YAML frontmatter and heading lines."""

    lines = text.splitlines()
    if lines and lines[0] == "---":
        try:
            end = lines.index("---", 1)
        except ValueError:
            return ""
        lines = lines[end + 1 :]
    return "\n".join(line for line in lines if re.match(r"^ {0,3}#{1,6}(?:\s|$)", line) is None)


def _git_blob_id(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def _validate_semantic_witnesses(root: pathlib.Path) -> list[CatalogFinding]:
    """Use Migration 0002 only to prove its two body-derived merge witnesses."""
    ledger = _fenced_yaml(_read_text(root, SEMANTIC_WITNESS_PATH), "## Archive Ledger")
    raw_files = ledger.get("files")
    if not isinstance(raw_files, list):
        return [_finding("semantic-witness-invalid", SEMANTIC_WITNESS_PATH, "files missing")]
    rows = [row for row in raw_files if isinstance(row, Mapping) and row.get("semantic_action") == "merge"]
    if len(rows) != 2:
        return [_finding("semantic-witness-invalid", SEMANTIC_WITNESS_PATH, "expected two role merges")]
    identities: list[tuple[object, ...]] = []
    for row in rows:
        identities.append(
            (
                row.get("legacy_path"),
                row.get("source_commit"),
                row.get("source_blob"),
                row.get("role"),
                row.get("catalog_path"),
                row.get("final_path"),
                row.get("canonical_role_owner"),
            )
        )
    expected_identities = tuple(item[:7] for item in _SEMANTIC_MERGE_IDENTITIES)
    if tuple(identities) != expected_identities:
        return [
            _finding(
                "semantic-witness-row-invalid",
                SEMANTIC_WITNESS_PATH,
                "merge identities and paths are not exact",
            )
        ]
    findings: list[CatalogFinding] = []
    for row, expected in zip(rows, _SEMANTIC_MERGE_IDENTITIES, strict=True):
        legacy = _safe_relative(row.get("legacy_path"), "legacy_path")
        final = pathlib.PurePosixPath(expected[7])
        preserved = row.get("preserved_semantics")
        if not isinstance(preserved, list):
            findings.append(_finding("semantic-witness-invalid", legacy, "witness list invalid"))
            continue
        witnesses: list[str] = []
        invalid_witness = False
        for value in preserved:
            if isinstance(value, Mapping) and any(str(key).startswith("text:") for key in value):
                invalid_witness = True
                continue
            if not isinstance(value, str) or not value.startswith("text:"):
                continue
            parts = value.split(":", 2)
            if len(parts) != 3:
                invalid_witness = True
                continue
            witness = parts[2]
            if (
                not witness.strip()
                or witness != witness.strip()
                or len(witness.encode("utf-8")) > MAX_SEMANTIC_WITNESS_BYTES
            ):
                invalid_witness = True
                continue
            witnesses.append(witness)
        if invalid_witness or not witnesses:
            findings.append(_finding("semantic-witness-invalid", legacy, "no body-derived witness"))
            continue
        result = _run_git_bounded(
            root,
            ["show", f"{row.get('source_commit')}:{legacy.as_posix()}"],
            max_stdout=MAX_FILE_BYTES,
        )
        try:
            current = _read_text(root, final)
        except OperationsAuthorityError as error:
            findings.append(_finding(error.code, final, str(error)))
            continue
        if result.returncode:
            findings.append(_finding("semantic-witness-source-invalid", legacy, "pinned source unavailable"))
            continue
        if _git_blob_id(result.stdout) != row.get("source_blob"):
            findings.append(_finding("semantic-witness-source-invalid", legacy, "source blob mismatch"))
            continue
        try:
            source_text = result.stdout.decode("utf-8")
        except UnicodeDecodeError:
            findings.append(_finding("semantic-witness-source-invalid", legacy, "source is not UTF-8"))
            continue
        source_body = _markdown_body_text(source_text)
        current_body = _markdown_body_text(current)
        for witness in witnesses:
            if witness not in source_body:
                findings.append(_finding("semantic-witness-not-body-derived", legacy, witness))
            if witness not in current_body:
                findings.append(_finding("semantic-witness-missing", final, witness))
    return findings


def validate_current_operations(
    root: pathlib.Path,
    *,
    include_semantic_witnesses: bool = True,
) -> tuple[CatalogFinding, ...]:
    """Validate exact final topology against Registry + Migration 0003."""
    try:
        migration = load_task8_migration(root)
        registry = _load_registry(root)
    except OperationsAuthorityError as error:
        return (_finding(error.code, "authority", str(error)),)
    findings = _validate_registry(registry)
    expected_files = {row.target_path: row for row in migration.rows if row.action == "rename"}
    expected_subjects = {path.parent for path in expected_files if path is not None}
    expected_by_domain: dict[str, set[str]] = defaultdict(set)
    expected_roles: dict[pathlib.PurePosixPath, set[str]] = defaultdict(set)
    for path in expected_files:
        assert path is not None
        expected_by_domain[path.parts[3]].add(path.parts[4])
        expected_roles[path.parent].add(path.name)
    if len(expected_subjects) != 75:
        findings.append(_finding("subject-count-invalid", "migration", str(len(expected_subjects))))
    role_counts = Counter(_ROLE_FILE[path.name] for path in expected_files if path is not None)
    if dict(role_counts) != EXPECTED_ROLE_COUNTS:
        findings.append(_finding("role-count-invalid", "migration", str(dict(role_counts))))

    try:
        operations_entries = _directory_entries_bounded(
            root,
            OPERATIONS_ROOT,
            max_entries=MAX_OPERATIONS_ROOT_ENTRIES,
        )
    except OperationsAuthorityError as error:
        code = "operations-root-bounds" if error.code == "directory-bounds" else "operations-root-invalid"
        return (_finding(code, OPERATIONS_ROOT, str(error)),)
    root_entry_names = {entry.name for entry in operations_entries}
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
            findings.append(_finding("retired-root-present", OPERATIONS_ROOT / retired, "must be absent"))
    template = root / "docs/99.templates/templates/operations/release.template.md"
    if template.exists() or template.is_symlink():
        findings.append(_finding("release-template-present", template.relative_to(root), "must be absent"))

    catalog_relative = OPERATIONS_ROOT / "catalog"
    try:
        catalog_entries = _directory_entries_bounded(
            root,
            catalog_relative,
            max_entries=MAX_CATALOG_ENTRIES,
        )
    except OperationsAuthorityError as error:
        code = "catalog-bounds" if error.code == "directory-bounds" else "catalog-root-invalid"
        findings.append(_finding(code, catalog_relative, str(error)))
        catalog_entries = ()
    actual_domains = {entry.name for entry in catalog_entries if entry.name != "README.md"}
    if actual_domains != set(EXPECTED_DOMAINS):
        findings.append(_finding("domain-set-invalid", catalog_relative, str(sorted(actual_domains))))
    seen_numbers: dict[str, pathlib.PurePosixPath] = {}
    seen_artifacts: dict[str, pathlib.PurePosixPath] = {}
    for domain in EXPECTED_DOMAINS:
        domain_relative = catalog_relative / domain
        try:
            domain_entries = _directory_entries_bounded(
                root,
                domain_relative,
                max_entries=MAX_DOMAIN_ENTRIES,
            )
        except OperationsAuthorityError as error:
            code = "domain-bounds" if error.code == "directory-bounds" else "domain-invalid"
            findings.append(_finding(code, domain_relative, str(error)))
            continue
        actual = {entry.name for entry in domain_entries}
        expected = {"README.md", *expected_by_domain[domain]}
        if actual != expected:
            findings.append(_finding("domain-ownership-invalid", domain_relative, f"expected {sorted(expected)}"))
        for subject_name in sorted(actual - {"README.md"}):
            subject_relative = domain_relative / subject_name
            match = _SUBJECT.fullmatch(subject_name)
            if subject_name.startswith("ops-") or match is None:
                findings.append(_finding("subject-path-invalid", subject_relative, "must be prefixless four-digit slug"))
                continue
            try:
                subject_entries = _directory_entries_bounded(
                    root,
                    subject_relative,
                    max_entries=MAX_SUBJECT_ENTRIES,
                )
            except OperationsAuthorityError as error:
                code = "subject-bounds" if error.code == "directory-bounds" else "subject-symlink-invalid"
                findings.append(_finding(code, subject_relative, str(error)))
                continue
            number = match.group("number")
            previous = seen_numbers.setdefault(number, subject_relative)
            if previous != subject_relative:
                findings.append(_finding("subject-identity-duplicate", subject_relative, str(previous)))
            entries_by_name = {entry.name: entry for entry in subject_entries}
            entries = set(entries_by_name)
            role_set = expected_roles.get(subject_relative, set())
            if entries != role_set:
                findings.append(_finding("subject-role-membership-invalid", subject_relative, f"expected {sorted(role_set)}"))
            for filename in sorted(entries & set(_ROLE_FILE)):
                role_relative = subject_relative / filename
                if not entries_by_name[filename].is_regular:
                    findings.append(_finding("role-file-invalid", role_relative, "must be regular and symlink-free"))
                    continue
                try:
                    role_text = _read_text(root, role_relative)
                    metadata = _frontmatter(role_text, role_relative)
                except OperationsAuthorityError as error:
                    findings.append(_finding(error.code, role_relative, str(error)))
                    continue
                row = expected_files.get(role_relative)
                role = _ROLE_FILE[filename]
                artifact = metadata.get("artifact_id")
                if row is None or artifact != row.artifact_id or metadata.get("artifact_type") != role:
                    findings.append(_finding("role-identity-invalid", role_relative, f"expected {row.artifact_id if row else None}"))
                if metadata.get("profile_id") != role:
                    findings.append(_finding("role-profile-invalid", role_relative, role))
                profile = _OPERATIONS_PROFILE_CONTRACT[role]
                required_metadata = set(profile["required_frontmatter"])
                if not required_metadata <= set(metadata):
                    findings.append(_finding("role-profile-invalid", role_relative, "required metadata missing"))
                allowed_statuses = _OPERATIONS_LIFECYCLE_STATUSES[str(profile["lifecycle_id"])]
                if metadata.get("status") not in allowed_statuses:
                    findings.append(_finding("role-status-invalid", role_relative, str(metadata.get("status"))))
                headings = _headings(role_text)
                missing_sections = [
                    section
                    for section in profile["required_sections"]
                    if not headings & _ROLE_SECTION_ALIASES[role][section]
                ]
                if missing_sections:
                    findings.append(
                        _finding("role-sections-invalid", role_relative, ",".join(missing_sections))
                    )
                if isinstance(artifact, str):
                    previous_artifact = seen_artifacts.setdefault(artifact, role_relative)
                    if previous_artifact != role_relative:
                        findings.append(_finding("role-identity-duplicate", role_relative, str(previous_artifact)))

    incidents_relative = OPERATIONS_ROOT / "incidents"
    try:
        incident_entries = _directory_entries_bounded(
            root,
            incidents_relative,
            max_entries=MAX_INCIDENT_ENTRIES,
        )
    except OperationsAuthorityError as error:
        code = "incident-bounds" if error.code == "directory-bounds" else "incident-root-invalid"
        findings.append(_finding(code, incidents_relative, str(error)))
    else:
        for year_entry in incident_entries:
            if year_entry.name == "README.md":
                continue
            year_relative = incidents_relative / year_entry.name
            if _YEAR.fullmatch(year_entry.name) is None or not year_entry.is_directory:
                findings.append(_finding("incident-year-invalid", year_relative, "year is the only date exception"))
                continue
            try:
                year_entries = _directory_entries_bounded(
                    root,
                    year_relative,
                    max_entries=MAX_INCIDENT_YEAR_ENTRIES,
                )
            except OperationsAuthorityError as error:
                code = "incident-bounds" if error.code == "directory-bounds" else "incident-year-invalid"
                findings.append(_finding(code, year_relative, str(error)))
                continue
            for packet_entry in year_entries:
                packet_relative = year_relative / packet_entry.name
                packet_match = _INCIDENT.fullmatch(packet_entry.name)
                if packet_match is None or not packet_entry.is_directory:
                    findings.append(_finding("incident-packet-invalid", packet_relative, "invalid packet"))
                    continue
                try:
                    packet_entries = _directory_entries_bounded(
                        root,
                        packet_relative,
                        max_entries=MAX_INCIDENT_PACKET_ENTRIES,
                    )
                except OperationsAuthorityError as error:
                    code = "incident-bounds" if error.code == "directory-bounds" else "incident-packet-invalid"
                    findings.append(_finding(code, packet_relative, str(error)))
                    continue
                entries = {entry.name for entry in packet_entries}
                if "incident.md" not in entries or not entries <= {"incident.md", "postmortem.md"}:
                    findings.append(_finding("incident-roles-invalid", packet_relative, "incident required; postmortem optional"))
                for child_entry in packet_entries:
                    if not child_entry.is_regular:
                        findings.append(_finding("incident-role-file-invalid", packet_relative / child_entry.name, "must be regular"))
                        continue
                    if child_entry.name not in {"incident.md", "postmortem.md"}:
                        continue
                    child_relative = packet_relative / child_entry.name
                    role = pathlib.PurePosixPath(child_entry.name).stem
                    try:
                        child_text = _read_text(root, child_relative)
                        metadata = _frontmatter(child_text, child_relative)
                    except OperationsAuthorityError as error:
                        findings.append(_finding(error.code, child_relative, str(error)))
                        continue
                    profile = _OPERATIONS_PROFILE_CONTRACT[role]
                    required_metadata = set(profile["required_frontmatter"])
                    if (
                        not required_metadata <= set(metadata)
                        or metadata.get("profile_id") != role
                        or metadata.get("artifact_type") != role
                    ):
                        findings.append(_finding("incident-profile-invalid", child_relative, role))
                    allowed_statuses = _OPERATIONS_LIFECYCLE_STATUSES[str(profile["lifecycle_id"])]
                    if metadata.get("status") not in allowed_statuses:
                        findings.append(
                            _finding(
                                "incident-status-invalid",
                                child_relative,
                                str(metadata.get("status")),
                            )
                        )
                    number = packet_match.group("number")
                    expected_id = f"inc-{number}" if role == "incident" else f"postmortem-{number}"
                    if metadata.get("artifact_id") != expected_id:
                        findings.append(_finding("incident-identity-invalid", child_relative, expected_id))
                    parent_ids = metadata.get("parent_ids")
                    if role == "postmortem" and (
                        not isinstance(parent_ids, list) or f"inc-{number}" not in parent_ids
                    ):
                        findings.append(
                            _finding("incident-identity-invalid", child_relative, "incident parent required")
                        )
                    headings = _headings(child_text)
                    missing_sections = set(profile["required_sections"]) - headings
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
                            _finding("incident-date-order-invalid", child_relative, "created/updated")
                        )
                    if role == "incident":
                        occurred = _date_time(metadata.get("occurred_at"))
                        resolved = _date_time(metadata.get("resolved_at"))
                        if occurred is None or str(occurred.year) != year_entry.name:
                            findings.append(
                                _finding("incident-year-date-invalid", child_relative, year_entry.name)
                            )
                        if resolved is not None and occurred is not None and resolved < occurred:
                            findings.append(
                                _finding("incident-date-order-invalid", child_relative, "resolved before occurred")
                            )
    if include_semantic_witnesses:
        try:
            findings.extend(_validate_semantic_witnesses(root))
        except OperationsAuthorityError as error:
            findings.append(_finding(error.code, SEMANTIC_WITNESS_PATH, str(error)))
    return tuple(sorted(set(findings)))


def consumer_inventory_json(inventory: ConsumerInventory) -> str:
    return json.dumps(
        {
            "declared_raw": [str(path) for path in inventory.declared_raw],
            "declared_current": [str(path) for path in inventory.declared_current],
            "live": [str(path) for path in inventory.live],
            "live_only": [str(path) for path in inventory.live_only],
            "union": [str(path) for path in inventory.union],
            "excluded": [str(path) for path in inventory.excluded],
            "tracked_files": inventory.tracked_files,
            "tracked_bytes": inventory.tracked_bytes,
        }, indent=2, sort_keys=True,
    )
