"""Bounded immutable parsing for canonical Stage 03 Spec Packages."""

from __future__ import annotations

import dataclasses
import datetime
import os
import pathlib
import re
import selectors
import stat
import subprocess
import time
from collections.abc import Mapping, Sequence

from scripts.lib.document_governance.frontmatter import (
    FrontmatterError,
    frontmatter_record_from_text,
)
from scripts.lib.document_governance.registry import (
    DocumentRegistry,
    RegistryError,
    document_type,
    load_registry,
    load_registry_at_revision,
    load_registry_document_at_revision,
    validate_registry,
    validate_registry_at_revision,
)

MAX_SPEC_FILE_BYTES = 4 * 1024 * 1024
MAX_SPEC_PACKAGES = 256
MAX_PACKAGE_ENTRIES = 256
MAX_PACKAGE_TASKS = 128
MAX_PACKAGE_CONTRACTS = 3
MAX_TOTAL_ENTRIES = 4096
MAX_TOTAL_FILE_BYTES = 64 * 1024 * 1024
GIT_COMMAND_TIMEOUT_SECONDS = 30.0
GIT_REAP_TIMEOUT_SECONDS = 1.0
GIT_STREAM_CHUNK_BYTES = 64 * 1024

_PACKAGE_PATH = re.compile(r"(?P<number>[0-9]{4})-(?P<slug>[a-z0-9][a-z0-9-]*)")
_TASK_PATH = re.compile(r"tsk-(?P<number>[0-9]{4})-(?P<slug>[a-z0-9][a-z0-9-]*)\.md")
_SPEC_ID = re.compile(r"SPEC-[0-9]{4}")
_PLAN_ID = re.compile(r"SPEC-[0-9]{4}-PLAN-[0-9]{4}")
_TASK_ID = re.compile(r"SPEC-[0-9]{4}-TSK-[0-9]{4}")
_EXTERNAL_PARENT_ID = re.compile(r"(?:REQ|AD|ADR|SPEC)-[0-9]{4}")
_RECOVERY_COMMIT = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})")
_FORBIDDEN_PACKAGE_ROLES = frozenset({"design.md", "tests.md", "task.md"})
_CONTRACT_PROFILES = {
    "openapi.yaml": "openapi-contract",
    "schema.graphql": "graphql-contract",
    "service.proto": "proto-contract",
}
_EXPECTED_PROFILES = {
    "spec": (
        "docs/03.specs/{number:4}-{slug}/spec.md",
        "SPEC-{number:4}",
        "direct",
        "spec",
    ),
    "plan": (
        "docs/03.specs/{package_number:4}-{slug}/plan.md",
        "SPEC-{package_number:4}-PLAN-{member_number:4}",
        "package-member",
        "plan",
    ),
    "task": (
        "docs/03.specs/{package_number:4}-{slug}/tasks/tsk-{task_number:4}-{slug}.md",
        "SPEC-{package_number:4}-TSK-{task_number:4}",
        "package-member",
        "task",
    ),
}


class SpecPackageError(ValueError):
    """Raised when the Stage 03 package surface cannot be trusted."""


@dataclasses.dataclass(frozen=True)
class BranchIntegrationReceipt:
    """One typed handoff for an exact divergent historical package."""

    source_commit: str
    source_package_path: pathlib.PurePosixPath
    source_artifact_id: str
    preserved_package_path: pathlib.PurePosixPath
    target_package_path: pathlib.PurePosixPath
    target_artifact_id: str
    disposition: str


@dataclasses.dataclass(frozen=True)
class SpecDocument:
    """One immutable registered Markdown member of a Spec Package."""

    path: pathlib.PurePosixPath
    profile_id: str
    artifact_id: str
    status: str
    parent_ids: tuple[str, ...]
    body: str = ""
    branch_integration_receipts: tuple[BranchIntegrationReceipt, ...] = ()
    cancellation: object = None
    source_text: str = ""


@dataclasses.dataclass(frozen=True)
class SpecPackage:
    """One canonical prefixless Stage 03 package."""

    path: pathlib.Path
    number: str
    slug: str
    spec: SpecDocument
    plan: SpecDocument | None
    tasks: tuple[SpecDocument, ...]
    contracts: tuple[pathlib.PurePosixPath, ...]


@dataclasses.dataclass(frozen=True, order=True)
class SpecPackageFinding:
    """One deterministic Stage 03 lifecycle finding."""

    code: str
    path: str
    message: str


@dataclasses.dataclass(frozen=True)
class SpecPackageLifecycleValidation:
    """Repository findings plus exact transitions proved by current Task rows."""

    findings: tuple[SpecPackageFinding, ...]
    actual_transitions: frozenset[tuple[str, str, str]]
    actual_normalizations: frozenset[tuple[str, str, str]] = frozenset()
    generation_source: str | None = None


@dataclasses.dataclass(frozen=True)
class _LifecycleEvent:
    artifact_id: str
    source: str
    target: str
    evidence: str
    host_path: pathlib.PurePosixPath


@dataclasses.dataclass(frozen=True)
class _MigrationProof:
    source_revision: str
    host_path: pathlib.PurePosixPath


@dataclasses.dataclass(frozen=True)
class _GenerationIntegration:
    """The exact first-parent merge that joined the new contract to main."""

    revision: str
    main_revision: str


@dataclasses.dataclass(frozen=True)
class _LoadBudget:
    entries: int = 0
    file_bytes: int = 0


@dataclasses.dataclass(frozen=True)
class _ReceiptCarrier:
    receipt: BranchIntegrationReceipt
    task: SpecDocument
    package: SpecPackage
    completed_archive: bool = False


def _path_identity(metadata: os.stat_result) -> tuple[int, int]:
    """Return what a symlink swap cannot forge.

    The stat-then-open check exists to prove the descriptor refers to the
    object that was stat'd. Only device and inode carry that. Link count and
    timestamps move whenever anything else writes into the directory, which on
    a shared parent such as /tmp happens continuously and proves nothing; an
    attacker who swaps a directory can match a timestamp with utimensat but
    cannot match an inode. Content that must not move while a load runs is
    guarded separately by the fuller snapshot below.
    """

    return (metadata.st_dev, metadata.st_ino)


def _directory_snapshot(
    metadata: os.stat_result,
) -> tuple[int, int, int, int, int, int]:
    return (
        metadata.st_dev,
        metadata.st_ino,
        metadata.st_mode,
        metadata.st_nlink,
        metadata.st_mtime_ns,
        metadata.st_ctime_ns,
    )


def _open_directory_at(
    parent_descriptor: int,
    name: str,
    label: str,
) -> tuple[int, tuple[int, int, int, int, int, int]]:
    try:
        metadata = os.stat(name, dir_fd=parent_descriptor, follow_symlinks=False)
    except OSError as error:
        raise SpecPackageError(f"cannot stat {label}: {error}") from error
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
        raise SpecPackageError(f"{label} must be a regular non-symlink directory")
    flags = (
        os.O_RDONLY
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_DIRECTORY", 0)
        | getattr(os, "O_NOFOLLOW", 0)
    )
    try:
        descriptor = os.open(name, flags, dir_fd=parent_descriptor)
    except OSError as error:
        raise SpecPackageError(f"cannot open {label}: {error}") from error
    opened = os.fstat(descriptor)
    if not stat.S_ISDIR(opened.st_mode) or _path_identity(opened) != _path_identity(
        metadata
    ):
        os.close(descriptor)
        raise SpecPackageError(f"{label} changed while opening")
    return descriptor, _directory_snapshot(opened)


def _open_directory_path(
    path: pathlib.Path,
    label: str,
) -> tuple[int, int, str, tuple[int, int, int, int, int, int]]:
    absolute = pathlib.Path(os.path.abspath(path))
    parts = absolute.parts
    if not parts or parts[0] != os.path.sep or len(parts) < 2:
        raise SpecPackageError(f"{label} path must be an absolute contained path")
    flags = (
        os.O_RDONLY
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_DIRECTORY", 0)
        | getattr(os, "O_NOFOLLOW", 0)
    )
    parent_descriptor = os.open(os.path.sep, flags)
    try:
        for component in parts[1:-1]:
            if component in {"", ".", ".."}:
                raise SpecPackageError(f"{label} path contains an unsafe component")
            child_descriptor, _ = _open_directory_at(
                parent_descriptor,
                component,
                f"{label} parent",
            )
            os.close(parent_descriptor)
            parent_descriptor = child_descriptor
        name = parts[-1]
        descriptor, snapshot = _open_directory_at(parent_descriptor, name, label)
        return parent_descriptor, descriptor, name, snapshot
    except BaseException:
        os.close(parent_descriptor)
        raise


def _verify_directory_entry(
    parent_descriptor: int,
    name: str,
    descriptor: int,
    snapshot: tuple[int, int, int, int, int, int],
    label: str,
) -> None:
    try:
        final = os.stat(name, dir_fd=parent_descriptor, follow_symlinks=False)
        opened = os.fstat(descriptor)
    except OSError as error:
        raise SpecPackageError(f"{label} changed while loading: {error}") from error
    if (
        stat.S_ISLNK(final.st_mode)
        or not stat.S_ISDIR(final.st_mode)
        or _directory_snapshot(final) != snapshot
        or _directory_snapshot(opened) != snapshot
    ):
        raise SpecPackageError(f"{label} changed or became a symlink while loading")


def _bounded_directory_names(
    descriptor: int,
    *,
    label: str,
    limit: int,
    limit_message: str,
    budget: _LoadBudget,
) -> tuple[tuple[str, ...], _LoadBudget]:
    before = _directory_snapshot(os.fstat(descriptor))
    names: list[str] = []
    current = budget
    try:
        with os.scandir(descriptor) as iterator:
            for entry in iterator:
                if len(names) >= limit:
                    raise SpecPackageError(limit_message)
                if current.entries >= MAX_TOTAL_ENTRIES:
                    raise SpecPackageError(
                        "Stage 03 exceeds the aggregate entry budget"
                    )
                if entry.name in {"", ".", ".."}:
                    raise SpecPackageError(f"{label} contains an unsafe entry")
                names.append(entry.name)
                current = dataclasses.replace(
                    current,
                    entries=current.entries + 1,
                )
    except SpecPackageError:
        raise
    except OSError as error:
        raise SpecPackageError(f"cannot enumerate {label}: {error}") from error
    after = _directory_snapshot(os.fstat(descriptor))
    if after != before:
        raise SpecPackageError(f"{label} changed while enumerating")
    return tuple(sorted(names)), current


def _file_snapshot(metadata: os.stat_result) -> tuple[int, int, int, int, int, int]:
    return (
        metadata.st_dev,
        metadata.st_ino,
        metadata.st_mode,
        metadata.st_size,
        metadata.st_mtime_ns,
        metadata.st_ctime_ns,
    )


def _read_regular_utf8_at(
    parent_descriptor: int,
    name: str,
    label: str,
    budget: _LoadBudget,
) -> tuple[str, _LoadBudget]:
    try:
        metadata = os.stat(name, dir_fd=parent_descriptor, follow_symlinks=False)
    except OSError as error:
        raise SpecPackageError(f"cannot stat {label}: {error}") from error
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode):
        raise SpecPackageError(f"{label} must be a regular non-symlink file")
    if metadata.st_size > MAX_SPEC_FILE_BYTES:
        raise SpecPackageError(f"{label} exceeds the byte limit")
    flags = (
        os.O_RDONLY
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NOFOLLOW", 0)
        | os.O_NONBLOCK
    )
    try:
        descriptor = os.open(name, flags, dir_fd=parent_descriptor)
        try:
            opened = os.fstat(descriptor)
            if not stat.S_ISREG(opened.st_mode):
                raise SpecPackageError(f"{label} changed to a non-regular file")
            if _file_snapshot(opened) != _file_snapshot(metadata):
                raise SpecPackageError(f"{label} changed while opening")
            if opened.st_size > MAX_SPEC_FILE_BYTES:
                raise SpecPackageError(f"{label} exceeds the byte limit")
            if budget.file_bytes + opened.st_size > MAX_TOTAL_FILE_BYTES:
                raise SpecPackageError("Stage 03 exceeds the aggregate byte budget")
            chunks: list[bytes] = []
            length = 0
            while True:
                chunk = os.read(
                    descriptor,
                    min(64 * 1024, MAX_SPEC_FILE_BYTES + 1 - length),
                )
                if not chunk:
                    break
                chunks.append(chunk)
                length += len(chunk)
                if length > MAX_SPEC_FILE_BYTES:
                    raise SpecPackageError(f"{label} exceeds the byte limit")
            verified = os.fstat(descriptor)
            if (
                _file_snapshot(verified) != _file_snapshot(opened)
                or length != opened.st_size
            ):
                raise SpecPackageError(
                    f"{label} changed while reading or produced a short read"
                )
            final = os.stat(name, dir_fd=parent_descriptor, follow_symlinks=False)
            if stat.S_ISLNK(final.st_mode) or _file_snapshot(final) != _file_snapshot(
                opened
            ):
                raise SpecPackageError(
                    f"{label} changed or became a symlink while reading"
                )
        finally:
            os.close(descriptor)
    except SpecPackageError:
        raise
    except OSError as error:
        raise SpecPackageError(f"cannot read {label}: {error}") from error
    try:
        text = b"".join(chunks).decode("utf-8")
    except UnicodeDecodeError as error:
        raise SpecPackageError(f"{label} must be UTF-8") from error
    return text, dataclasses.replace(
        budget,
        file_bytes=budget.file_bytes + len(b"".join(chunks)),
    )


def _validate_registry_contract(registry: DocumentRegistry) -> None:
    for profile_id, expected in _EXPECTED_PROFILES.items():
        profile = registry.profiles.get(profile_id)
        if not isinstance(profile, Mapping):
            raise SpecPackageError(f"Stage 99 profile is missing: {profile_id}")
        path_pattern, artifact_pattern, identity_relation, lifecycle_id = expected
        if (
            profile.get("path_pattern") != path_pattern
            or profile.get("artifact_id_pattern") != artifact_pattern
            or profile.get("identity_relation") != identity_relation
            or profile.get("lifecycle_id") != lifecycle_id
        ):
            raise SpecPackageError(
                f"Stage 99 Spec Package profile is not canonical: {profile_id}"
            )
        lifecycle = registry.lifecycles.get(lifecycle_id)
        if not isinstance(lifecycle, tuple):
            raise SpecPackageError(f"Stage 99 lifecycle is missing: {lifecycle_id}")
    for filename, profile_id in _CONTRACT_PROFILES.items():
        profile = registry.profiles.get(profile_id)
        expected_path = "docs/03.specs/{package_number:4}-{slug}/contracts/" + filename
        if (
            not isinstance(profile, Mapping)
            or profile.get("path_pattern") != expected_path
            or profile.get("frontmatter_policy") != "absent"
        ):
            raise SpecPackageError(
                f"Stage 99 executable contract profile is not canonical: {profile_id}"
            )


def _string_tuple(value: object, field: str) -> tuple[str, ...]:
    if not isinstance(value, tuple) or not all(
        isinstance(item, str) and item for item in value
    ):
        raise SpecPackageError(
            f"Spec Package frontmatter {field} must be a string list"
        )
    if len(value) != len(set(value)):
        raise SpecPackageError(
            f"Spec Package frontmatter {field} contains duplicate identities"
        )
    return value


_RECEIPT_FIELDS = frozenset(
    {
        "source_commit",
        "source_package_path",
        "source_artifact_id",
        "preserved_package_path",
        "target_package_path",
        "target_artifact_id",
        "disposition",
    }
)


def _branch_integration_receipts(
    value: object,
) -> tuple[BranchIntegrationReceipt, ...]:
    if value is None:
        return ()
    if not isinstance(value, tuple) or not value:
        raise SpecPackageError(
            "branch_integration_receipts must be a non-empty receipt list"
        )
    receipts: list[BranchIntegrationReceipt] = []
    for item in value:
        if not isinstance(item, Mapping) or set(item) != _RECEIPT_FIELDS:
            raise SpecPackageError("branch integration receipt shape is invalid")
        if not all(isinstance(item[field], str) and item[field] for field in item):
            raise SpecPackageError("branch integration receipt values must be strings")
        if _RECOVERY_COMMIT.fullmatch(item["source_commit"]) is None:
            raise SpecPackageError(
                "branch integration receipt source_commit must be a full object ID"
            )
        if any(
            not _safe_repository_path(item[field])
            for field in (
                "source_package_path",
                "preserved_package_path",
                "target_package_path",
            )
        ):
            raise SpecPackageError("branch integration receipt path is unsafe")
        if item["disposition"] != "historical-superseded":
            raise SpecPackageError("branch integration receipt disposition is invalid")
        receipt = BranchIntegrationReceipt(
            source_commit=item["source_commit"],
            source_package_path=pathlib.PurePosixPath(item["source_package_path"]),
            source_artifact_id=item["source_artifact_id"],
            preserved_package_path=pathlib.PurePosixPath(
                item["preserved_package_path"]
            ),
            target_package_path=pathlib.PurePosixPath(item["target_package_path"]),
            target_artifact_id=item["target_artifact_id"],
            disposition=item["disposition"],
        )
        if receipt in receipts:
            raise SpecPackageError("branch integration receipt is duplicated")
        receipts.append(receipt)
    return tuple(receipts)


def _allowed_statuses(
    registry: DocumentRegistry,
    profile_id: str,
) -> tuple[str, ...]:
    lifecycle_id = _EXPECTED_PROFILES[profile_id][3]
    statuses = registry.lifecycles.get(lifecycle_id)
    if not isinstance(statuses, tuple):
        raise SpecPackageError(f"Stage 99 lifecycle is missing: {lifecycle_id}")
    if not all(isinstance(status, str) for status in statuses):
        raise SpecPackageError(
            f"Stage 99 lifecycle statuses are malformed: {lifecycle_id}"
        )
    return statuses


def _parse_document(
    parent_descriptor: int,
    name: str,
    display_path: pathlib.Path,
    relative: pathlib.PurePosixPath,
    *,
    profile_id: str,
    expected_artifact_id: str,
    registry: DocumentRegistry,
    budget: _LoadBudget,
) -> tuple[SpecDocument, _LoadBudget]:
    text, current = _read_regular_utf8_at(
        parent_descriptor,
        name,
        f"Stage 03 {profile_id}",
        budget,
    )
    try:
        record = frontmatter_record_from_text(display_path, text)
    except FrontmatterError as error:
        raise SpecPackageError(str(error)) from error
    if record.metadata.get("type") != document_type(profile_id):
        raise SpecPackageError(
            f"{relative} must declare type: {document_type(profile_id)}"
        )
    artifact_id = record.metadata.get("artifact_id")
    if artifact_id != expected_artifact_id:
        raise SpecPackageError(
            f"{relative} must own {expected_artifact_id}, found {artifact_id!r}"
        )
    status = record.metadata.get("status")
    if not isinstance(status, str) or status not in _allowed_statuses(
        registry, profile_id
    ):
        raise SpecPackageError(
            f"{relative} status is outside the {profile_id} lifecycle: {status!r}"
        )
    parent_ids = _string_tuple(record.metadata.get("parent_ids"), "parent_ids")
    receipts = (
        _branch_integration_receipts(record.metadata.get("branch_integration_receipts"))
        if profile_id == "task"
        else ()
    )
    return (
        SpecDocument(
            relative,
            profile_id,
            artifact_id,
            status,
            parent_ids,
            body=record.body,
            branch_integration_receipts=receipts,
            cancellation=record.metadata.get("cancellation"),
            source_text=text,
        ),
        current,
    )


def _validate_spec_parents(document: SpecDocument) -> None:
    if any(
        _EXTERNAL_PARENT_ID.fullmatch(parent) is None for parent in document.parent_ids
    ):
        raise SpecPackageError(
            f"{document.path} Spec parents must use canonical uppercase stable IDs"
        )
    if document.artifact_id in document.parent_ids:
        raise SpecPackageError(f"{document.path} may not parent itself")


def _validate_plan_parents(document: SpecDocument, spec_id: str) -> None:
    if document.parent_ids != (spec_id,):
        raise SpecPackageError(
            f"{document.path} plan parent must be exactly its owning {spec_id}"
        )


def _validate_task_parents(
    document: SpecDocument,
    *,
    spec_id: str,
    plan_id: str | None,
    current_contracts: bool,
    task_ids: frozenset[str] = frozenset(),
) -> None:
    if current_contracts:
        valid = plan_id is not None and document.parent_ids == (plan_id,)
    else:
        required = (spec_id, plan_id) if plan_id is not None else (spec_id,)
        valid = (plan_id is not None and document.parent_ids == (plan_id,)) or (
            document.parent_ids[: len(required)] == required
            and all(
                parent in task_ids and parent != document.artifact_id
                for parent in document.parent_ids[len(required) :]
            )
        )
    if not valid:
        raise SpecPackageError(
            f"{document.path} task parent must match its owning Plan contract"
        )


def _validate_execution_states(
    spec: SpecDocument,
    plan: SpecDocument | None,
    tasks: tuple[SpecDocument, ...],
) -> None:
    if plan is None:
        return
    task_terminal = {"completed", "cancelled"}
    parent_terminal = {"completed", "cancelled", "superseded"}
    if spec.status in {"cancelled", "superseded"}:
        if plan.status not in parent_terminal or any(
            task.status not in task_terminal for task in tasks
        ):
            raise SpecPackageError(
                f"{plan.path} terminal package contains an active Plan or Task"
            )
        return
    if spec.status != plan.status:
        raise SpecPackageError(
            f"{plan.path} Spec and Plan must share one status projection"
        )
    if not tasks:
        if spec.status not in {
            "draft",
            "in-review",
            "approved",
            "in-progress",
            "blocked",
        }:
            raise SpecPackageError(
                f"{plan.path} empty package has an invalid status projection"
            )
        return
    remaining = tuple(task for task in tasks if task.status not in task_terminal)
    if spec.status in {"draft", "in-review"}:
        if any(task.status != "draft" for task in remaining):
            raise SpecPackageError(
                f"{plan.path} pre-execution package contains an active Task"
            )
        return
    if not remaining:
        if spec.status not in {"approved", "in-progress", "blocked", "completed"}:
            raise SpecPackageError(
                f"{plan.path} terminal-only package has an invalid status projection"
            )
        return
    if any(task.status == "in-progress" for task in remaining):
        expected = "in-progress"
    elif all(task.status == "blocked" for task in remaining):
        expected = "blocked"
    else:
        if spec.status not in {"approved", "in-progress", "blocked"}:
            raise SpecPackageError(
                f"{plan.path} fallback package has an invalid status projection"
            )
        return
    if spec.status != expected:
        raise SpecPackageError(
            f"{plan.path} parent status projection must be {expected}"
        )


def _completion_visible_lines(body: str) -> list[str]:
    """Exclude fenced examples and HTML comments without mixing their states."""
    visible: list[str] = []
    fence: str | None = None
    comment = False
    for line in body.splitlines():
        if fence is not None:
            if re.fullmatch(
                rf" {{0,3}}{re.escape(fence[0])}{{{len(fence)},}}[ \t]*", line
            ):
                fence = None
            continue
        opening = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if not comment and opening and not (opening[1][0] == "`" and "`" in opening[2]):
            fence = opening[1]
            continue
        parts: list[str] = []
        for token in re.split(r"(<!--|--!?>)", line):
            if comment:
                if re.fullmatch(r"--!?>", token):
                    comment = False
            elif token == "<!--":
                comment = True
                parts.append(" ")
            else:
                parts.append(token)
        visible.append("".join(parts))
    return visible


def _contract_section(body: str, heading: str) -> list[str]:
    lines = _completion_visible_lines(body)
    marker = "## " + heading
    starts = [index for index, line in enumerate(lines) if line == marker]
    if len(starts) != 1:
        raise SpecPackageError(f"completion requires one {marker}")
    start = starts[0] + 1
    end = next(
        (index for index in range(start, len(lines)) if lines[index].startswith("## ")),
        len(lines),
    )
    return lines[start:end]


def acceptance_criterion_numbers(spec_body: str, heading: str) -> tuple[int, ...]:
    """Read visible numbered criteria from the registered acceptance section."""
    return tuple(
        int(value)
        for value in re.findall(
            r"^([1-9][0-9]*)\. \S",
            "\n".join(_contract_section(spec_body, heading)),
            re.M,
        )
    )


def task_cancellation_findings(
    task_id: str,
    cancellation: object,
    criteria: frozenset[int],
    task_statuses: Mapping[str, str],
    *,
    generation: int = 4,
    references: frozenset[str] = frozenset(),
) -> tuple[str, ...]:
    """Judge cancellation without changing metadata or exempting completion."""
    if not isinstance(cancellation, Mapping):
        return ("cancellation must be an object",)
    if generation >= 5:
        expected = {"reason", "authorization_ref", "criteria_disposition"}
        if set(cancellation) != expected:
            return (
                "cancellation requires exactly reason, authorization_ref, and criteria_disposition",
            )
        for field in ("reason", "authorization_ref"):
            value = cancellation.get(field)
            if not isinstance(value, str) or not value.strip():
                return (f"cancellation {field} must be a nonempty string",)
        if cancellation["authorization_ref"] not in references:
            return (
                "cancellation authorization_ref must resolve to one unique same-Task heading",
            )
        entries = cancellation.get("criteria_disposition")
        if not isinstance(entries, (list, tuple)):
            return ("cancellation criteria_disposition must be a list",)
        seen_criteria: set[int] = set()
        for entry in entries:
            if not isinstance(entry, Mapping):
                return ("cancellation criteria disposition must be an object",)
            criterion = entry.get("criterion")
            if type(criterion) is not int or criterion not in criteria:
                return ("cancellation criterion must name a Spec acceptance criterion",)
            if criterion in seen_criteria:
                return ("cancellation criterion must occur only once",)
            seen_criteria.add(criterion)
            alternatives = {"successor", "withdrawal_ref"} & set(entry)
            if set(entry) != {"criterion", *alternatives} or len(alternatives) != 1:
                return (
                    "cancellation criterion needs exactly one successor or approved withdrawal reference",
                )
            if "withdrawal_ref" in entry:
                reference = entry["withdrawal_ref"]
                if not isinstance(reference, str) or not reference.strip():
                    return ("cancellation withdrawal_ref must be nonempty",)
                if reference not in references:
                    return (
                        "cancellation withdrawal_ref must resolve to one unique same-Task heading",
                    )
                continue
            target = entry["successor"]
            if (
                not isinstance(target, str)
                or target == task_id
                or target not in task_statuses
                or task_statuses[target] == "cancelled"
            ):
                return (
                    "cancellation successor must name another non-cancelled package Task",
                )
        return ()
    for field in ("reason", "approved_by"):
        value = cancellation.get(field)
        if not isinstance(value, str) or not value.strip():
            return (f"cancellation {field} must be a nonempty string",)
    approved_at = cancellation.get("approved_at")
    if (
        not isinstance(approved_at, str)
        or re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", approved_at) is None
    ):
        return ("cancellation approved_at must be a YYYY-MM-DD date",)
    try:
        datetime.date.fromisoformat(approved_at)
    except ValueError:
        return ("cancellation approved_at must be a valid date",)
    entries = cancellation.get("criteria")
    if not isinstance(entries, (list, tuple)):
        return ("cancellation criteria must be a list",)
    seen_criteria: set[int] = set()
    for entry in entries:
        if not isinstance(entry, Mapping):
            return ("cancellation criteria entry must be an object",)
        criterion = entry.get("criterion")
        if type(criterion) is not int or criterion not in criteria:
            return ("cancellation criterion must name a Spec acceptance criterion",)
        if criterion in seen_criteria:
            return ("cancellation criterion must occur only once",)
        seen_criteria.add(criterion)
        if ("reassigned_to" in entry) == ("withdrawn" in entry):
            return (
                "cancellation criterion needs exactly one of reassigned_to or withdrawn",
            )
        if "withdrawn" in entry:
            if (
                not isinstance(entry["withdrawn"], str)
                or not entry["withdrawn"].strip()
            ):
                return ("cancellation withdrawn must be a nonempty reason",)
        else:
            target = entry["reassigned_to"]
            if (
                not isinstance(target, str)
                or target == task_id
                or target not in task_statuses
                or task_statuses[target] == "cancelled"
            ):
                return (
                    "cancellation reassigned_to must name another non-cancelled package Task",
                )
    return ()


def _v5_cancellation_findings(
    document: SpecDocument,
    criteria: frozenset[int],
    statuses: Mapping[str, str],
) -> tuple[str, ...]:
    findings = task_cancellation_findings(
        document.artifact_id,
        document.cancellation,
        criteria,
        statuses,
        generation=5,
        references=_document_anchor_references(document.source_text),
    )
    if findings:
        return findings
    assert isinstance(document.cancellation, Mapping)
    entries = document.cancellation["criteria_disposition"]
    assert isinstance(entries, (list, tuple))
    disposed = {entry["criterion"] for entry in entries if isinstance(entry, Mapping)}
    if disposed != set(criteria):
        return ("cancellation criteria disposition must match assigned criteria",)
    return ()


def _document_anchor_references(source_text: str) -> frozenset[str]:
    anchors = [
        "#" + _heading_anchor(match.group(1))
        for line in _completion_visible_lines(source_text)
        if (match := re.fullmatch(r"#{1,6} +(.+?) *#*", line)) is not None
    ]
    return frozenset(anchor for anchor in anchors if anchors.count(anchor) == 1)


def _registered_table_rows(
    lines: Sequence[str],
    headers: tuple[str, ...],
    *,
    allowed_headers: frozenset[tuple[str, ...]] = frozenset(),
    strict_contiguity: bool = False,
) -> tuple[tuple[str, ...], ...]:
    def is_visible_pipe_row(line: str) -> bool:
        content = line.lstrip(" ")
        return len(line) - len(content) <= 3 and content.startswith("|")

    matches: list[int] = []
    for index, line in enumerate(lines):
        if not line.startswith("|"):
            continue
        cells = tuple(cell.strip() for cell in line.strip().strip("|").split("|"))
        if cells == headers:
            matches.append(index)
        elif cells and cells[0] == headers[0] and cells not in allowed_headers:
            raise SpecPackageError("registered evidence table has malformed headers")
    if not matches:
        if strict_contiguity and any(is_visible_pipe_row(line) for line in lines):
            raise SpecPackageError("registered evidence table must be contiguous")
        return ()
    if len(matches) != 1:
        raise SpecPackageError("registered evidence table must occur only once")
    index = matches[0]
    if (
        index + 1 >= len(lines)
        or re.fullmatch(rf"\|(?: *:?-+:? *\|){{{len(headers)}}}", lines[index + 1])
        is None
    ):
        raise SpecPackageError(
            f"registered evidence requires a {len(headers)}-column table"
        )
    rows: list[tuple[str, ...]] = []
    table_end = index + 2
    for line in lines[table_end:]:
        if not line.startswith("|"):
            break
        values = tuple(cell.strip() for cell in line.strip().strip("|").split("|"))
        if len(values) != len(headers) or any(not value for value in values):
            raise SpecPackageError("registered evidence table has malformed columns")
        rows.append(values)
        table_end += 1
    if not rows:
        raise SpecPackageError("registered evidence table requires at least one row")
    if strict_contiguity and (
        any(is_visible_pipe_row(line) for line in lines[:index])
        or any(is_visible_pipe_row(line) for line in lines[table_end:])
    ):
        raise SpecPackageError("registered evidence table must be contiguous")
    return tuple(rows)


def _completion_rows(
    task: SpecDocument,
    contract: Mapping[str, object],
) -> tuple[tuple[str, tuple[tuple[str, ...], ...]], ...]:
    lines = _contract_section(task.body, str(contract["task_section"]))
    registered: list[tuple[str, tuple[str, ...]]] = []
    for key in ("table_headers", "item_table_headers"):
        raw_headers = contract.get(key)
        if key == "item_table_headers" and raw_headers is None:
            continue
        if not isinstance(raw_headers, (list, tuple)) or not all(
            isinstance(header, str) and header for header in raw_headers
        ):
            raise SpecPackageError(f"completion evidence {key} is malformed")
        registered.append((key, tuple(raw_headers)))
    allowed = frozenset(headers for _, headers in registered)
    tables: list[tuple[str, tuple[tuple[str, ...], ...]]] = []
    for key, headers in registered:
        try:
            rows = _registered_table_rows(
                lines,
                headers,
                allowed_headers=allowed,
            )
        except SpecPackageError as error:
            raise SpecPackageError(f"completion evidence: {error}") from error
        if rows:
            tables.append((key, rows))
    if len(tables) > 1:
        raise SpecPackageError("Task must use one registered completion table shape")
    return tuple(tables)


def _review_rows(
    task: SpecDocument,
    registry: DocumentRegistry,
) -> tuple[tuple[str, str, str], ...]:
    contract = registry.common.get("review_evidence")
    if not isinstance(contract, Mapping):
        raise SpecPackageError("review evidence contract is missing from Registry")
    section_name = contract.get("section")
    raw_headers = contract.get("table_headers")
    if not isinstance(section_name, str) or not isinstance(raw_headers, (list, tuple)):
        raise SpecPackageError("review evidence contract is malformed")
    headers = tuple(raw_headers)
    if len(headers) != 3 or not all(
        isinstance(header, str) and header for header in headers
    ):
        raise SpecPackageError("review evidence table headers are malformed")
    try:
        rows = _registered_table_rows(
            _contract_section(task.body, section_name),
            headers,
        )
    except SpecPackageError as error:
        raise SpecPackageError(f"review evidence: {error}") from error
    return tuple(
        (criterion, acceptance, evidence) for criterion, acceptance, evidence in rows
    )


def _task_result_value(result: str, allowed: frozenset[str]) -> str:
    if result not in allowed:
        raise SpecPackageError("Task result is outside the registered result values")
    return result


def _registered_common_values(
    registry: DocumentRegistry, key: str, expected_length: int | None = None
) -> tuple[str, ...]:
    values = registry.common.get(key)
    if (
        not isinstance(values, (list, tuple))
        or not all(isinstance(value, str) and value for value in values)
        or len(values) != len(set(values))
        or (expected_length is not None and len(values) != expected_length)
    ):
        raise SpecPackageError(f"{key} is missing or malformed in Registry")
    return tuple(values)


def _registered_common_section(registry: DocumentRegistry, key: str) -> str:
    value = registry.common.get(key)
    if not isinstance(value, str) or not value:
        raise SpecPackageError(f"{key} is missing or malformed in Registry")
    return value


def _cell_references(value: str, label: str) -> tuple[str, ...]:
    references = tuple(item.strip() for item in value.split(","))
    if not references or any(not item for item in references):
        raise SpecPackageError(f"{label} references are malformed")
    return references


def _work_references(value: str) -> tuple[str, ...]:
    if value == "None":
        return ()
    references: list[str] = []
    for item in _cell_references(value, "Plan Dependencies"):
        match = re.fullmatch(r"W([1-9][0-9]*)[–-]W([1-9][0-9]*)", item)
        if match is None:
            references.append(item)
            continue
        start, end = map(int, match.groups())
        if start >= end:
            raise SpecPackageError("Plan dependency range is malformed")
        references.extend(f"W{number}" for number in range(start, end + 1))
    if any(re.fullmatch(r"W[1-9][0-9]*", item) is None for item in references):
        raise SpecPackageError("Plan Dependencies must reference Work Unit identities")
    return tuple(references)


def _v5_plan_rows(
    plan: SpecDocument, registry: DocumentRegistry
) -> tuple[tuple[str, ...], ...]:
    headers = _registered_common_values(registry, "plan_columns", 6)
    if headers != (
        "Work Unit",
        "Criteria",
        "Work",
        "Dependencies",
        "Task",
        "Verification",
    ):
        raise SpecPackageError("generation 5 Plan columns are not canonical")
    return _registered_table_rows(
        _contract_section(
            plan.body, _registered_common_section(registry, "plan_section")
        ),
        headers,
        strict_contiguity=True,
    )


def _v5_evidence_rows(
    task: SpecDocument, registry: DocumentRegistry
) -> tuple[tuple[str, ...], ...]:
    headers = _registered_common_values(registry, "evidence_columns", 8)
    if headers != (
        "Evidence",
        "Criteria",
        "Work Unit",
        "Check",
        "Input",
        "Result",
        "Location",
        "Acceptance",
    ):
        raise SpecPackageError("generation 5 Evidence columns are not canonical")
    return _registered_table_rows(
        _contract_section(
            task.body, _registered_common_section(registry, "task_section")
        ),
        headers,
        strict_contiguity=True,
    )


def _v5_evidence_contract(
    spec: SpecDocument,
    plan: SpecDocument | None,
    tasks: tuple[SpecDocument, ...],
    registry: DocumentRegistry,
    historical_tasks: frozenset[pathlib.PurePosixPath] = frozenset(),
    historical_completed_pairs: Mapping[
        pathlib.PurePosixPath, frozenset[tuple[str, str]]
    ]
    | None = None,
) -> tuple[
    frozenset[str],
    frozenset[str],
    frozenset[tuple[str, str]],
    frozenset[tuple[str, str]],
]:
    criterion_numbers = tuple(
        str(number)
        for number in acceptance_criterion_numbers(
            spec.body, _registered_common_section(registry, "spec_section")
        )
    )
    if not criterion_numbers or len(criterion_numbers) != len(set(criterion_numbers)):
        raise SpecPackageError(
            "generation 5 evidence requires unique numbered Spec criteria"
        )
    criteria = frozenset(criterion_numbers)
    if plan is None:
        if tasks:
            raise SpecPackageError("generation 5 Task evidence requires a Plan")
        return criteria, frozenset(), frozenset(), frozenset()
    plan_rows = _v5_plan_rows(plan, registry)
    work: set[str] = set()
    planned_pairs: set[tuple[str, str]] = set()
    assignments: dict[tuple[str, str], frozenset[str]] = {}
    task_references = {
        reference: task.artifact_id
        for task in tasks
        for reference in (
            task.artifact_id,
            task.artifact_id.rsplit("-", 2)[-2]
            + "-"
            + task.artifact_id.rsplit("-", 1)[-1],
        )
    }
    for unit, raw_criteria, _, dependencies, raw_tasks, _ in plan_rows:
        if re.fullmatch(r"W[1-9][0-9]*", unit) is None or unit in work:
            raise SpecPackageError("Plan Work Unit identities must be unique W labels")
        if any(reference not in work for reference in _work_references(dependencies)):
            raise SpecPackageError(
                "Plan Dependencies must reference earlier Work Units"
            )
        work.add(unit)
        assigned = _cell_references(raw_tasks, "Plan Task")
        if any(reference not in task_references for reference in assigned):
            raise SpecPackageError("Plan Task must name a same-package Task")
        assigned_ids = frozenset(task_references[reference] for reference in assigned)
        for criterion in _cell_references(raw_criteria, "Plan Criteria"):
            if criterion not in criteria:
                raise SpecPackageError("Plan row references an unknown criterion")
            pair = (criterion, unit)
            planned_pairs.add(pair)
            assignments[pair] = assigned_ids
    results = frozenset(_registered_common_values(registry, "result_domain"))
    acceptance = frozenset(_registered_common_values(registry, "acceptance_domain"))
    if results != {"NOT_RUN", "PASS", "FAIL", "DEFER", "NOT_APPLICABLE"}:
        raise SpecPackageError("generation 5 result domain is not canonical")
    if acceptance != {"pending", "accepted", "rejected", "not-required"}:
        raise SpecPackageError("generation 5 acceptance domain is not canonical")
    completed_pairs: set[tuple[str, str]] = set()
    for task in tasks:
        assigned = {
            pair
            for pair, assigned_tasks in assignments.items()
            if task.artifact_id in assigned_tasks
        }
        if task.path in historical_tasks:
            admitted = (historical_completed_pairs or {}).get(task.path, frozenset())
            completed_pairs.update(assigned & admitted)
            continue
        if task.status == "cancelled":
            cancellation = task.cancellation
            entries = (
                cancellation.get("criteria_disposition", ())
                if isinstance(cancellation, Mapping)
                else ()
            )
            disposed = {
                str(entry.get("criterion"))
                for entry in entries
                if isinstance(entry, Mapping)
            }
            assigned_criteria = {criterion for criterion, _ in assigned}
            if disposed != assigned_criteria:
                raise SpecPackageError(
                    "cancelled Task criteria disposition must match its Plan assignment"
                )
            successors = {
                str(entry.get("criterion")): entry.get("successor")
                for entry in entries
                if isinstance(entry, Mapping) and "successor" in entry
            }
            for pair in assigned:
                successor = successors.get(pair[0])
                if successor is None:
                    continue
                successor_id = (
                    task_references.get(successor)
                    if isinstance(successor, str)
                    else None
                )
                if successor_id is None or successor_id not in assignments[pair]:
                    raise SpecPackageError(
                        "cancellation successor must be assigned the disposed Plan work"
                    )
        rows = _v5_evidence_rows(task, registry)
        task_completed_pairs: set[tuple[str, str]] = set()
        for _evidence, raw_criteria, unit, _, _, result, _, disposition in rows:
            if unit not in work:
                raise SpecPackageError("Evidence row references an unknown Work Unit")
            row_criteria = _cell_references(raw_criteria, "Evidence Criteria")
            if any(
                (criterion, unit) not in planned_pairs for criterion in row_criteria
            ):
                raise SpecPackageError(
                    "Evidence row references an unknown criterion/Work Unit pair"
                )
            if any(
                task.artifact_id not in assignments[(criterion, unit)]
                for criterion in row_criteria
            ):
                raise SpecPackageError(
                    f"{task.path}: Evidence row is outside the Plan Task assignment"
                )
            if result not in results:
                raise SpecPackageError(
                    "Evidence Result is outside the registered result domain"
                )
            if disposition not in acceptance:
                raise SpecPackageError(
                    "Evidence Acceptance is outside the registered acceptance domain"
                )
            if result == "PASS" and disposition == "accepted":
                row_pairs = {(criterion, unit) for criterion in row_criteria}
                task_completed_pairs.update(row_pairs)
        if task.status == "completed":
            completed_pairs.update(task_completed_pairs)
            if not assigned <= task_completed_pairs:
                raise SpecPackageError(
                    "completed Task requires PASS and accepted evidence"
                )
    return (
        criteria,
        frozenset(work),
        frozenset(planned_pairs),
        frozenset(completed_pairs),
    )


def _item_status_summary(
    statuses: Sequence[str], terminal_statuses: frozenset[str]
) -> str:
    if "blocked" in statuses:
        return "blocked"
    terminal = [status in terminal_statuses for status in statuses]
    if "in-progress" in statuses or (any(terminal) and not all(terminal)):
        return "in-progress"
    if "ready" in statuses:
        return "ready"
    if "draft" in statuses:
        return "draft"
    if all(status == "cancelled" for status in statuses):
        return "cancelled"
    return "completed"


def _validate_task_item_evidence(
    spec: SpecDocument,
    plan: SpecDocument | None,
    tasks: tuple[SpecDocument, ...],
    registry: DocumentRegistry,
    historical_tasks: frozenset[pathlib.PurePosixPath] = frozenset(),
    historical_completed_pairs: Mapping[
        pathlib.PurePosixPath, frozenset[tuple[str, str]]
    ]
    | None = None,
) -> None:
    if registry.common.get("lifecycle_generation") == 5:
        _v5_evidence_contract(
            spec,
            plan,
            tasks,
            registry,
            historical_tasks,
            historical_completed_pairs,
        )
        return
    contract = registry.common.get("spec_completion_evidence")
    if not isinstance(contract, Mapping):
        raise SpecPackageError("completion evidence contract is missing from Registry")
    raw_result_values = contract.get("task_result_values")
    if not isinstance(raw_result_values, (list, tuple)) or not all(
        isinstance(value, str) and value for value in raw_result_values
    ):
        raise SpecPackageError("Task result values are missing from Registry")
    result_values = frozenset(raw_result_values)
    review_contract = registry.common.get("review_evidence")
    allowed_acceptance = (
        review_contract.get("acceptance_values")
        if isinstance(review_contract, Mapping)
        else None
    )
    if not isinstance(allowed_acceptance, (list, tuple)) or not all(
        isinstance(value, str) and value for value in allowed_acceptance
    ):
        raise SpecPackageError("review acceptance values are missing from Registry")
    acceptance_values = frozenset(allowed_acceptance)
    tables = tuple((task, _completion_rows(task, contract)) for task in tasks)
    terminal_statuses = frozenset(registry.lifecycle_terminal_statuses["task"])
    legacy_tables = tuple(
        (task, rows)
        for task, task_tables in tables
        for key, rows in task_tables
        if key == "table_headers"
    )
    if any(
        len(rows) > 1 and task.status not in terminal_statuses
        for task, rows in legacy_tables
    ):
        raise SpecPackageError("multi-row completion evidence requires item statuses")
    evidence_tables = tuple(
        (task, key, rows) for task, task_tables in tables for key, rows in task_tables
    )
    if not evidence_tables:
        return
    if plan is None:
        raise SpecPackageError("item evidence requires a Plan")
    criteria = frozenset(
        str(number)
        for number in acceptance_criterion_numbers(
            spec.body, str(contract["spec_section"])
        )
    )
    work = frozenset(
        re.findall(
            r"^[1-9][0-9]*\. (?:\*\*)?(W[1-9][0-9]*)(?:\*\*)?: \S",
            "\n".join(_contract_section(plan.body, str(contract["plan_section"]))),
            re.M,
        )
    )
    if not criteria or not work:
        raise SpecPackageError(
            "item evidence requires criterion and Plan work identities"
        )
    allowed_statuses = frozenset(registry.lifecycles["task"])
    task_statuses = {task.artifact_id: task.status for task in tasks}
    pairs: set[tuple[str, str]] = set()
    for task, key, raw_rows in evidence_tables:
        rows = tuple(
            (
                criterion,
                unit,
                task.status,
                result,
                owner,
            )
            if key == "table_headers"
            else (criterion, unit, status, result, owner)
            for criterion, unit, *tail in raw_rows
            for status, result, owner in (
                (task.status, tail[0], tail[1])
                if key == "table_headers"
                else (tail[0], tail[1], tail[2]),
            )
        )
        statuses: list[str] = []
        reviews = _review_rows(task, registry)
        legacy_terminal_without_review = (
            key == "table_headers" and task.status in terminal_statuses and not reviews
        )
        if legacy_terminal_without_review:
            for criterion, unit, _, _ in raw_rows:
                pair = (criterion, unit)
                if pair in pairs:
                    raise SpecPackageError(
                        f"{task.path}: item evidence duplicates a criterion/work pair: "
                        f"{criterion}/{unit}"
                    )
                pairs.add(pair)
            continue
        if not reviews and not legacy_terminal_without_review:
            raise SpecPackageError(f"{task.path}: Review Evidence table is required")
        review_by_criterion: dict[str, str] = {}
        for criterion, acceptance, _ in reviews:
            if criterion in review_by_criterion:
                raise SpecPackageError("review evidence duplicates acceptance criteria")
            if acceptance not in acceptance_values:
                raise SpecPackageError(
                    "review evidence acceptance is outside the registered values"
                )
            review_by_criterion[criterion] = acceptance
        cancelled_criteria: frozenset[int] = frozenset()
        if any(row[2] == "cancelled" for row in rows):
            findings = task_cancellation_findings(
                task.artifact_id,
                task.cancellation,
                frozenset(int(criterion) for criterion in criteria),
                task_statuses,
            )
            if findings:
                raise SpecPackageError(f"{task.path}: {findings[0]}")
            assert isinstance(task.cancellation, Mapping)
            cancelled_criteria = frozenset(
                entry["criterion"]
                for entry in task.cancellation["criteria"]
                if isinstance(entry, Mapping)
            )
        for criterion, unit, status, result, owner in rows:
            if criterion not in criteria or unit not in work:
                raise SpecPackageError(
                    "item evidence has an unknown criterion or Plan work unit"
                )
            pair = (criterion, unit)
            if pair in pairs:
                raise SpecPackageError(
                    f"{task.path}: item evidence duplicates a criterion/work pair: "
                    f"{criterion}/{unit}"
                )
            pairs.add(pair)
            if status not in allowed_statuses:
                raise SpecPackageError(
                    "item evidence status is outside the Task lifecycle"
                )
            if status == "cancelled" and int(criterion) not in cancelled_criteria:
                raise SpecPackageError(
                    "cancelled item requires its acceptance criterion disposition"
                )
            result_value = _task_result_value(result, result_values)
            if status == "completed":
                if result_value != "PASS":
                    raise SpecPackageError("completed item needs PASS evidence")
                if re.fullmatch(r"N/A: \S.*|\[[^]\n]+\]\([^()\s]+\)", owner) is None:
                    raise SpecPackageError(
                        "completed item needs a durable owner link or N/A reason"
                    )
            statuses.append(status)
        assigned = {criterion for criterion, *_ in rows}
        if not legacy_terminal_without_review and set(review_by_criterion) != assigned:
            raise SpecPackageError(
                "review evidence criteria must match the Task item criteria"
            )
        if (
            task.status == "completed"
            and not legacy_terminal_without_review
            and any(
                review_by_criterion[criterion] != "accepted" for criterion in assigned
            )
        ):
            raise SpecPackageError("completed Task requires accepted review evidence")
        if key == "item_table_headers" and task.status != _item_status_summary(
            statuses, terminal_statuses
        ):
            raise SpecPackageError(
                f"{task.path} frontmatter does not match its item status summary"
            )


def _legacy_completed_task_pairs(
    spec: SpecDocument,
    plan: SpecDocument | None,
    tasks: tuple[SpecDocument, ...],
    registry: DocumentRegistry,
) -> dict[pathlib.PurePosixPath, frozenset[tuple[str, str]]]:
    """Return only completion pairs admitted by the exact source contract."""

    _validate_task_item_evidence(spec, plan, tasks, registry)
    contract = registry.common.get("spec_completion_evidence")
    if not isinstance(contract, Mapping):
        raise SpecPackageError("completion evidence contract is missing from Registry")
    result_values = frozenset(contract.get("task_result_values", ()))
    completed: dict[pathlib.PurePosixPath, frozenset[tuple[str, str]]] = {}
    for task in tasks:
        if task.status != "completed":
            continue
        reviews = {
            criterion: acceptance
            for criterion, acceptance, _ in _review_rows(task, registry)
        }
        if not reviews:
            completed[task.path] = frozenset()
            continue
        admitted: set[tuple[str, str]] = set()
        for key, raw_rows in _completion_rows(task, contract):
            for criterion, unit, *tail in raw_rows:
                status, result = (
                    (task.status, tail[0]) if key == "table_headers" else tail[:2]
                )
                if (
                    status == "completed"
                    and _task_result_value(result, result_values) == "PASS"
                    and reviews.get(criterion) == "accepted"
                ):
                    admitted.add((criterion, unit))
        completed[task.path] = frozenset(admitted)
    return completed


def _generation_three_completed_task_pairs(
    package: SpecPackage,
    registry: DocumentRegistry,
    admitted_paths: frozenset[pathlib.PurePosixPath],
) -> dict[pathlib.PurePosixPath, frozenset[tuple[str, str]]]:
    """Read exact PASS pairs from source-bound generation-three receipts."""

    contract = registry.common.get("spec_completion_evidence")
    if not isinstance(contract, Mapping):
        raise SpecPackageError("completion evidence contract is missing from Registry")
    completed: dict[pathlib.PurePosixPath, frozenset[tuple[str, str]]] = {}
    for task in package.tasks:
        if task.path not in admitted_paths or task.status != "completed":
            continue
        pairs: set[tuple[str, str]] = set()
        for key, rows in _completion_rows(task, contract):
            if key != "table_headers":
                continue
            for criterion, unit, result, _owner in rows:
                if re.fullmatch(r"PASS(?:: \S.*)?", result) is None:
                    raise SpecPackageError(
                        f"{task.path}: historical completed Task requires PASS evidence"
                    )
                pair = (criterion, unit)
                if pair in pairs:
                    raise SpecPackageError(
                        f"{task.path}: historical evidence duplicates {criterion}/{unit}"
                    )
                pairs.add(pair)
        if not pairs:
            raise SpecPackageError(
                f"{task.path}: historical completed Task requires evidence"
            )
        completed[task.path] = frozenset(pairs)
    return completed


def _validate_completion_evidence(
    spec: SpecDocument,
    plan: SpecDocument | None,
    tasks: tuple[SpecDocument, ...],
    registry: DocumentRegistry,
    *,
    current_contracts: bool = True,
    historical_tasks: frozenset[pathlib.PurePosixPath] = frozenset(),
    historical_completed_pairs: Mapping[
        pathlib.PurePosixPath, frozenset[tuple[str, str]]
    ]
    | None = None,
    source_criteria: frozenset[str] | None = None,
    source_work: frozenset[str] | None = None,
    source_closed_pairs: frozenset[tuple[str, str]] | None = None,
) -> None:
    """Check structural coverage only; reported results are not execution proof."""
    if spec.status != "completed":
        return
    if registry.common.get("lifecycle_generation") == 5:
        if plan is None or plan.status != "completed" or not tasks:
            raise SpecPackageError(
                "completion requires a completed Plan and Task evidence"
            )
        if any(task.status not in {"completed", "cancelled"} for task in tasks):
            raise SpecPackageError(
                "completion requires every remaining Task to be terminal"
            )
        criteria, work, planned_pairs, completed_pairs = _v5_evidence_contract(
            spec,
            plan,
            tasks,
            registry,
            historical_tasks,
            historical_completed_pairs,
        )
        if (
            source_criteria is not None
            and source_work is not None
            and (criteria != source_criteria or work != source_work)
        ):
            raise SpecPackageError(
                "completed migrated package must preserve source criteria and work identities"
            )
        if source_closed_pairs is not None and planned_pairs != source_closed_pairs:
            raise SpecPackageError(
                "completed historical package Plan pairs must match source closure evidence"
            )
        if (
            {criterion for criterion, _ in completed_pairs} != criteria
            or {unit for _, unit in completed_pairs} != work
            or not planned_pairs <= completed_pairs
        ):
            raise SpecPackageError(
                "completion evidence must cover every acceptance criterion and Plan work unit"
            )
        return
    contract = registry.common.get("spec_completion_evidence")
    if not isinstance(contract, Mapping):
        raise SpecPackageError("completion evidence contract is missing from Registry")
    if plan is None or plan.status != "completed" or not tasks:
        raise SpecPackageError("completion requires a completed Plan and Task evidence")

    if any(
        task.status not in registry.lifecycle_terminal_statuses["task"]
        for task in tasks
    ):
        raise SpecPackageError(
            "completion requires every remaining Task to be terminal"
        )

    def section(document: SpecDocument, key: str) -> list[str]:
        return _contract_section(document.body, str(contract[key]))

    criteria = tuple(
        str(number)
        for number in acceptance_criterion_numbers(
            spec.body, str(contract["spec_section"])
        )
    )
    work = re.findall(
        r"^[1-9][0-9]*\. (?:\*\*)?(W[1-9][0-9]*)(?:\*\*)?: \S",
        "\n".join(section(plan, "plan_section")),
        re.M,
    )
    if (
        not criteria
        or len(criteria) != len(set(criteria))
        or not work
        or len(work) != len(set(work))
    ):
        raise SpecPackageError(
            "completion requires unique numbered criteria and Plan work units"
        )
    covered: set[str] = set()
    pairs: set[tuple[str, str]] = set()
    completed_pairs: set[tuple[str, str]] = set()
    for task in tasks:
        reviews = (
            {
                criterion: acceptance
                for criterion, acceptance, _ in _review_rows(task, registry)
            }
            if current_contracts
            else {}
        )
        for key, rows in _completion_rows(task, contract):
            if key == "table_headers" and task.status != "completed":
                raise SpecPackageError("completion receipt Task must be completed")
            for values in rows:
                if key == "table_headers":
                    criterion, unit, result, owner = values
                    row_status = task.status
                else:
                    criterion, unit, row_status, result, owner = values
                if criterion not in criteria or unit not in work:
                    raise SpecPackageError(
                        "completion receipt has an unknown criterion or Plan work unit"
                    )
                if (criterion, unit) in pairs:
                    raise SpecPackageError(
                        "completion receipt duplicates a criterion/work pair"
                    )
                pairs.add((criterion, unit))
                if row_status != "completed":
                    continue
                result_is_pass = (
                    _task_result_value(
                        result,
                        frozenset(contract["task_result_values"]),
                    )
                    == "PASS"
                    if current_contracts
                    else re.fullmatch(r"PASS: \S.*", result) is not None
                )
                if not result_is_pass:
                    raise SpecPackageError(
                        "completion result needs PASS evidence; SKIP does not satisfy acceptance"
                    )
                if re.fullmatch(r"N/A: \S.*|\[[^]\n]+\]\([^()\s]+\)", owner) is None:
                    raise SpecPackageError(
                        "completion needs a durable owner link or N/A reason"
                    )
                if not current_contracts or reviews.get(criterion) == "accepted":
                    completed_pairs.add((criterion, unit))
                    covered.add(criterion)
    if covered != set(criteria) or {unit for _, unit in completed_pairs} != set(work):
        raise SpecPackageError(
            "completion evidence must cover every acceptance criterion and Plan work unit"
        )


def _load_contracts(
    package_descriptor: int,
    package_path: pathlib.Path,
    relative_package: pathlib.PurePosixPath,
    budget: _LoadBudget,
) -> tuple[tuple[pathlib.PurePosixPath, ...], _LoadBudget]:
    descriptor, snapshot = _open_directory_at(
        package_descriptor,
        "contracts",
        "Stage 03 contracts",
    )
    try:
        entries, current = _bounded_directory_names(
            descriptor,
            label="Stage 03 contracts",
            limit=MAX_PACKAGE_CONTRACTS,
            limit_message="Stage 03 package contains too many executable contracts",
            budget=budget,
        )
        contracts: list[pathlib.PurePosixPath] = []
        for name in entries:
            if name not in _CONTRACT_PROFILES:
                raise SpecPackageError(f"unregistered Stage 03 contract path: {name}")
            _, current = _read_regular_utf8_at(
                descriptor,
                name,
                "Stage 03 executable contract",
                current,
            )
            contracts.append(relative_package / "contracts" / name)
        _verify_directory_entry(
            package_descriptor,
            "contracts",
            descriptor,
            snapshot,
            "Stage 03 contracts",
        )
        return tuple(contracts), current
    finally:
        os.close(descriptor)


def _load_tasks(
    package_descriptor: int,
    package_path: pathlib.Path,
    relative_package: pathlib.PurePosixPath,
    *,
    package_number: str,
    registry: DocumentRegistry,
    budget: _LoadBudget,
) -> tuple[tuple[SpecDocument, ...], _LoadBudget]:
    descriptor, snapshot = _open_directory_at(
        package_descriptor,
        "tasks",
        "Stage 03 tasks",
    )
    try:
        entries, current = _bounded_directory_names(
            descriptor,
            label="Stage 03 tasks",
            limit=MAX_PACKAGE_TASKS,
            limit_message="Stage 03 package contains too many Task records",
            budget=budget,
        )
        tasks: list[SpecDocument] = []
        seen_numbers: set[str] = set()
        for name in entries:
            match = _TASK_PATH.fullmatch(name)
            if match is None:
                raise SpecPackageError(f"unregistered Stage 03 task path: {name}")
            task_number = match.group("number")
            if task_number in seen_numbers:
                raise SpecPackageError(
                    f"duplicate Task number in Stage 03 package: {task_number}"
                )
            seen_numbers.add(task_number)
            relative = relative_package / "tasks" / name
            task, current = _parse_document(
                descriptor,
                name,
                package_path / "tasks" / name,
                relative,
                profile_id="task",
                expected_artifact_id=f"SPEC-{package_number}-TSK-{task_number}",
                registry=registry,
                budget=current,
            )
            tasks.append(task)
        _verify_directory_entry(
            package_descriptor,
            "tasks",
            descriptor,
            snapshot,
            "Stage 03 tasks",
        )
        return tuple(tasks), current
    finally:
        os.close(descriptor)


def _load_package(
    stage_descriptor: int,
    package: pathlib.Path,
    match: re.Match[str],
    *,
    registry: DocumentRegistry,
    budget: _LoadBudget,
    completion_evidence: bool,
    current_contracts: bool,
) -> tuple[SpecPackage, _LoadBudget]:
    descriptor, snapshot = _open_directory_at(
        stage_descriptor,
        package.name,
        "Stage 03 package",
    )
    number = match.group("number")
    slug = match.group("slug")
    relative_package = pathlib.PurePosixPath("docs/03.specs", package.name)
    try:
        entries, current = _bounded_directory_names(
            descriptor,
            label="Stage 03 package",
            limit=MAX_PACKAGE_ENTRIES,
            limit_message="Stage 03 package contains too many entries",
            budget=budget,
        )
        allowed = {"README.md", "spec.md", "plan.md", "tasks", "contracts"}
        for name in entries:
            if name in _FORBIDDEN_PACKAGE_ROLES:
                raise SpecPackageError(f"forbidden Stage 03 package role: {name}")
            if name not in allowed:
                raise SpecPackageError(f"unregistered Stage 03 package entry: {name}")
        if "README.md" in entries:
            _, current = _read_regular_utf8_at(
                descriptor,
                "README.md",
                "Stage 03 package README",
                current,
            )
        if "spec.md" not in entries:
            raise SpecPackageError(f"{relative_package} must retain spec.md")
        spec, current = _parse_document(
            descriptor,
            "spec.md",
            package / "spec.md",
            relative_package / "spec.md",
            profile_id="spec",
            expected_artifact_id=f"SPEC-{number}",
            registry=registry,
            budget=current,
        )
        _validate_spec_parents(spec)
        plan: SpecDocument | None = None
        if "plan.md" in entries:
            plan, current = _parse_document(
                descriptor,
                "plan.md",
                package / "plan.md",
                relative_package / "plan.md",
                profile_id="plan",
                expected_artifact_id=f"SPEC-{number}-PLAN-0001",
                registry=registry,
                budget=current,
            )
            _validate_plan_parents(plan, spec.artifact_id)
        tasks: tuple[SpecDocument, ...] = ()
        if "tasks" in entries:
            tasks, current = _load_tasks(
                descriptor,
                package,
                relative_package,
                package_number=number,
                registry=registry,
                budget=current,
            )
        task_ids = frozenset(task.artifact_id for task in tasks)
        if len(task_ids) != len(tasks):
            raise SpecPackageError(f"duplicate Task identity in {relative_package}")
        for task in tasks:
            _validate_task_parents(
                task,
                spec_id=spec.artifact_id,
                plan_id=None if plan is None else plan.artifact_id,
                current_contracts=current_contracts,
                task_ids=task_ids,
            )
        if current_contracts:
            _validate_execution_states(spec, plan, tasks)
        if completion_evidence:
            task_statuses = {task.artifact_id: task.status for task in tasks}
            for task in tasks:
                if task.status != "cancelled":
                    continue
                generation = int(registry.common.get("lifecycle_generation", 4))
                heading = (
                    _registered_common_section(registry, "spec_section")
                    if generation >= 5
                    else str(
                        registry.common["spec_completion_evidence"]["spec_section"]
                    )
                )
                findings = task_cancellation_findings(
                    task.artifact_id,
                    task.cancellation,
                    frozenset(acceptance_criterion_numbers(spec.body, heading)),
                    task_statuses,
                    generation=generation,
                    references=_document_anchor_references(task.source_text),
                )
                if findings:
                    raise SpecPackageError(f"{task.path}: {findings[0]}")
            _validate_task_item_evidence(spec, plan, tasks, registry)
            _validate_completion_evidence(
                spec,
                plan,
                tasks,
                registry,
                current_contracts=current_contracts,
            )
        contracts: tuple[pathlib.PurePosixPath, ...] = ()
        if "contracts" in entries:
            contracts, current = _load_contracts(
                descriptor,
                package,
                relative_package,
                current,
            )
        _verify_directory_entry(
            stage_descriptor,
            package.name,
            descriptor,
            snapshot,
            "Stage 03 package",
        )
        return SpecPackage(package, number, slug, spec, plan, tasks, contracts), current
    finally:
        os.close(descriptor)


def load_spec_packages(
    stage_root: pathlib.Path,
    *,
    registry: DocumentRegistry | None = None,
    _completion_evidence: bool = True,
    _current_contracts: bool = True,
) -> tuple[SpecPackage, ...]:
    """Load and validate the complete canonical Stage 03 package surface."""

    stage_root = pathlib.Path(stage_root)
    active_registry = load_registry() if registry is None else registry
    _validate_registry_contract(active_registry)
    defer_v5_evidence = (
        _completion_evidence
        and _current_contracts
        and active_registry.common.get("lifecycle_generation") == 5
    )
    parent_descriptor, descriptor, stage_name, snapshot = _open_directory_path(
        stage_root,
        "Stage 03",
    )
    try:
        try:
            stage04 = os.stat(
                "04.execution",
                dir_fd=parent_descriptor,
                follow_symlinks=False,
            )
        except FileNotFoundError:
            stage04 = None
        except OSError as error:
            raise SpecPackageError(f"cannot inspect Stage 04: {error}") from error
        if stage04 is not None:
            raise SpecPackageError(
                "Stage 04 must not exist after Spec Package convergence"
            )
        entries, budget = _bounded_directory_names(
            descriptor,
            label="Stage 03",
            limit=MAX_SPEC_PACKAGES + 1,
            limit_message="Stage 03 exceeds the package count limit",
            budget=_LoadBudget(),
        )
        packages: list[SpecPackage] = []
        seen_numbers: set[str] = set()
        for name in entries:
            if name == "README.md":
                _, budget = _read_regular_utf8_at(
                    descriptor,
                    name,
                    "Stage 03 README",
                    budget,
                )
                continue
            match = _PACKAGE_PATH.fullmatch(name)
            if match is None:
                raise SpecPackageError(
                    f"Stage 03 package path is not canonical: {name}"
                )
            if len(packages) >= MAX_SPEC_PACKAGES:
                raise SpecPackageError("Stage 03 exceeds the package count limit")
            number = match.group("number")
            if number in seen_numbers:
                raise SpecPackageError(
                    f"duplicate Stage 03 package identity: SPEC-{number}"
                )
            seen_numbers.add(number)
            package, budget = _load_package(
                descriptor,
                stage_root / name,
                match,
                registry=active_registry,
                budget=budget,
                completion_evidence=_completion_evidence and not defer_v5_evidence,
                current_contracts=_current_contracts,
            )
            packages.append(package)
        artifact_ids = tuple(package.spec.artifact_id for package in packages)
        if len(artifact_ids) != len(set(artifact_ids)):
            raise SpecPackageError("duplicate Stage 03 Spec identity")
        if defer_v5_evidence:
            proof = _migration_proof(
                packages,
                active_registry,
                root=stage_root.parent.parent,
                target_generation=5,
            )
            source_registry = load_registry_document_at_revision(
                proof.source_revision,
                root=stage_root.parent.parent,
            )
            if validate_registry_at_revision(
                proof.source_revision, root=stage_root.parent.parent
            ):
                raise SpecPackageError("generation 5 source Registry is invalid")
            source_common = source_registry.get("common")
            if (
                not isinstance(source_common, Mapping)
                or source_common.get("lifecycle_generation") != 4
            ):
                raise SpecPackageError(
                    "generation 5 migration source must be lifecycle generation 4"
                )
            source_packages = _load_base_spec_packages(
                stage_root.parent.parent,
                base_ref=proof.source_revision,
            )
            source_contract = load_registry_at_revision(
                proof.source_revision,
                root=stage_root.parent.parent,
            )
            integration = _generation_integration(
                stage_root.parent.parent,
                proof,
                target_generation=5,
            )
            main_packages = _load_base_spec_packages(
                stage_root.parent.parent,
                base_ref=integration.main_revision,
            )
            integrated_packages = _load_base_spec_packages(
                stage_root.parent.parent,
                base_ref=integration.revision,
            )
            mainline_historical_tasks = _mainline_historical_terminal_tasks(
                source_packages,
                main_packages,
                integrated_packages,
                packages,
            )
            source_tasks = {
                task.path: task for package in source_packages for task in package.tasks
            }
            historical_tasks = frozenset(
                {
                    task.path
                    for package in packages
                    for task in package.tasks
                    if task.status in {"completed", "cancelled"}
                    and task.path in source_tasks
                    and source_tasks[task.path].status in {"completed", "cancelled"}
                    and task.source_text == source_tasks[task.path].source_text
                }
                | set(mainline_historical_tasks)
            )
            historical_completed_pairs: dict[
                pathlib.PurePosixPath, frozenset[tuple[str, str]]
            ] = {}
            source_semantics: dict[
                str,
                tuple[
                    frozenset[str],
                    frozenset[str],
                    frozenset[tuple[str, str]] | None,
                ],
            ] = {}
            source_completion = source_contract.common.get("spec_completion_evidence")
            if not isinstance(source_completion, Mapping):
                raise SpecPackageError(
                    "generation 5 source completion contract is missing"
                )
            for source_package in source_packages:
                admitted = _legacy_completed_task_pairs(
                    source_package.spec,
                    source_package.plan,
                    source_package.tasks,
                    source_contract,
                )
                historical_completed_pairs.update(
                    {
                        path: pairs
                        for path, pairs in admitted.items()
                        if path in historical_tasks
                    }
                )
                source_criteria = frozenset(
                    str(number)
                    for number in acceptance_criterion_numbers(
                        source_package.spec.body,
                        str(source_completion["spec_section"]),
                    )
                )
                source_work = (
                    frozenset(
                        re.findall(
                            r"^[1-9][0-9]*\. (?:\*\*)?(W[1-9][0-9]*)(?:\*\*)?: \S",
                            "\n".join(
                                _contract_section(
                                    source_package.plan.body,
                                    str(source_completion["plan_section"]),
                                )
                            ),
                            re.M,
                        )
                    )
                    if source_package.plan is not None
                    else frozenset()
                )
                source_closed_pairs = None
                if (
                    source_package.spec.status == "completed"
                    and source_package.plan is not None
                    and source_package.plan.status == "completed"
                ):
                    _validate_completion_evidence(
                        source_package.spec,
                        source_package.plan,
                        source_package.tasks,
                        source_contract,
                        current_contracts=True,
                    )
                    source_closed_pairs = frozenset(
                        pair for pairs in admitted.values() for pair in pairs
                    )
                source_semantics[source_package.spec.artifact_id] = (
                    source_criteria,
                    source_work,
                    source_closed_pairs,
                )
            main_contract = load_registry_at_revision(
                integration.main_revision,
                root=stage_root.parent.parent,
            )
            for main_package in main_packages:
                admitted = _generation_three_completed_task_pairs(
                    main_package,
                    main_contract,
                    mainline_historical_tasks,
                )
                historical_completed_pairs.update(admitted)
            spec_statuses = {
                package.spec.artifact_id: package.spec.status for package in packages
            }
            plan_statuses = {
                package.plan.artifact_id: package.plan.status
                for package in packages
                if package.plan is not None
            }
            for package in packages:
                if package.spec.status == "cancelled":
                    numbers = acceptance_criterion_numbers(
                        package.spec.body,
                        _registered_common_section(active_registry, "spec_section"),
                    )
                    if len(numbers) != len(set(numbers)):
                        raise SpecPackageError(
                            f"{package.spec.path}: cancellation criteria must be unique"
                        )
                    findings = _v5_cancellation_findings(
                        package.spec, frozenset(numbers), spec_statuses
                    )
                    if findings:
                        raise SpecPackageError(f"{package.spec.path}: {findings[0]}")
                if package.plan is not None and package.plan.status == "cancelled":
                    spec_criteria = frozenset(
                        str(number)
                        for number in acceptance_criterion_numbers(
                            package.spec.body,
                            _registered_common_section(active_registry, "spec_section"),
                        )
                    )
                    raw_plan_criteria = tuple(
                        criterion
                        for row in _v5_plan_rows(package.plan, active_registry)
                        for criterion in _cell_references(row[1], "Plan Criteria")
                    )
                    if any(
                        criterion not in spec_criteria
                        for criterion in raw_plan_criteria
                    ):
                        raise SpecPackageError(
                            f"{package.plan.path}: Plan row references an unknown criterion"
                        )
                    plan_criteria = frozenset(map(int, raw_plan_criteria))
                    findings = _v5_cancellation_findings(
                        package.plan, plan_criteria, plan_statuses
                    )
                    if findings:
                        raise SpecPackageError(f"{package.plan.path}: {findings[0]}")
                task_statuses = {
                    task.artifact_id: task.status for task in package.tasks
                }
                cancelled = tuple(
                    task
                    for task in package.tasks
                    if task.status == "cancelled" and task.path not in historical_tasks
                )
                if cancelled:
                    criteria = frozenset(
                        acceptance_criterion_numbers(
                            package.spec.body,
                            _registered_common_section(active_registry, "spec_section"),
                        )
                    )
                for task in cancelled:
                    findings = task_cancellation_findings(
                        task.artifact_id,
                        task.cancellation,
                        criteria,
                        task_statuses,
                        generation=5,
                        references=_document_anchor_references(task.source_text),
                    )
                    if findings:
                        raise SpecPackageError(f"{task.path}: {findings[0]}")
                _validate_task_item_evidence(
                    package.spec,
                    package.plan,
                    package.tasks,
                    active_registry,
                    historical_tasks,
                    historical_completed_pairs,
                )
                source_semantic = source_semantics.get(package.spec.artifact_id)
                _validate_completion_evidence(
                    package.spec,
                    package.plan,
                    package.tasks,
                    active_registry,
                    historical_tasks=historical_tasks,
                    historical_completed_pairs=historical_completed_pairs,
                    source_criteria=(
                        source_semantic[0] if source_semantic is not None else None
                    ),
                    source_work=(
                        source_semantic[1] if source_semantic is not None else None
                    ),
                    source_closed_pairs=(
                        source_semantic[2] if source_semantic is not None else None
                    ),
                )
        _verify_directory_entry(
            parent_descriptor,
            stage_name,
            descriptor,
            snapshot,
            "Stage 03",
        )
        return tuple(packages)
    finally:
        os.close(descriptor)
        os.close(parent_descriptor)


def _documents(
    packages: Sequence[SpecPackage],
) -> dict[pathlib.PurePosixPath, SpecDocument]:
    result: dict[pathlib.PurePosixPath, SpecDocument] = {}
    for package in packages:
        members = [package.spec, *package.tasks]
        if package.plan is not None:
            members.append(package.plan)
        for member in members:
            if member.path in result:
                raise SpecPackageError(
                    f"duplicate Spec Package member path: {member.path}"
                )
            result[member.path] = member
    return result


def _with_missing_historical_tasks(
    primary: Sequence[SpecPackage],
    fallback: Sequence[SpecPackage],
    admitted_paths: frozenset[pathlib.PurePosixPath],
) -> tuple[SpecPackage, ...]:
    """Add only Git-bound Task paths absent from the generation snapshot."""

    fallback_by_name = {package.spec.path.parts[2]: package for package in fallback}
    merged: list[SpecPackage] = []
    for package in primary:
        name = package.spec.path.parts[2]
        supplement = fallback_by_name.get(name)
        existing = {task.path for task in package.tasks}
        additional = (
            tuple(
                task
                for task in supplement.tasks
                if task.path in admitted_paths and task.path not in existing
            )
            if supplement is not None
            else ()
        )
        tasks = tuple(
            sorted(
                (*package.tasks, *additional),
                key=lambda task: task.path.as_posix(),
            )
        )
        merged.append(dataclasses.replace(package, tasks=tasks))
    return tuple(merged)


def disposition_entry_statuses(
    profile_id: str, registry: DocumentRegistry | None = None
) -> frozenset[str]:
    """Read disposition states separately from lifecycle terminal states."""
    active = registry if registry is not None else load_registry()
    contract = active.common.get("archive_retention", {})
    statuses = contract.get("disposition_entry_statuses", {}).get(profile_id)
    if not isinstance(statuses, (list, tuple)) or not all(
        isinstance(status, str) for status in statuses
    ):
        raise SpecPackageError(f"disposition entry statuses missing for {profile_id}")
    return frozenset(statuses)


def validate_spec_package_lifecycle(
    previous: Sequence[SpecPackage],
    current: Sequence[SpecPackage],
    *,
    retired_paths: frozenset[pathlib.PurePosixPath] = frozenset(),
    preserved_paths: frozenset[pathlib.PurePosixPath] = frozenset(),
    registry: DocumentRegistry | None = None,
) -> tuple[SpecPackageFinding, ...]:
    """Enforce the canonical retention contract on Spec Package removals.

    A retained package keeps its non-terminal members. A package that leaves
    Stage 03 is either preserved or retired, and the two are not the same
    event: preservation moves a finished package to the archive and keeps every
    document, while retirement withdraws one and records a Tombstone saying
    why. A Tombstone is required for the second, and asking for one after a
    completion would record a withdrawal that never happened.

    The Spec's terminal status is an authoring obligation recorded in the
    Tombstone's `Reason`, not a predicate here: the comparison base is the
    branch point, so a package that is `active` there can never be observed as
    terminal by the change that retires it.
    """

    active_registry = registry if registry is not None else load_registry()
    previous_documents = _documents(previous)
    current_documents = _documents(current)
    retained_packages = frozenset(package.spec.path.parts[2] for package in current)
    findings: list[SpecPackageFinding] = []
    retired_packages: dict[str, SpecPackage] = {}
    for package in previous:
        if package.spec.path.parts[2] in retained_packages:
            continue
        retired_packages[package.spec.path.parts[2]] = package
    for path, document in sorted(previous_documents.items()):
        if path in current_documents or path.parts[2] not in retained_packages:
            continue
        if document.status not in disposition_entry_statuses(
            document.profile_id, active_registry
        ):
            findings.append(
                SpecPackageFinding(
                    "execution-evidence-deletion-forbidden",
                    path.as_posix(),
                    "a retained package keeps non-terminal Spec Package members",
                )
            )
    for name, package in sorted(retired_packages.items()):
        if package.spec.path in preserved_paths:
            continue
        if package.spec.path not in retired_paths:
            findings.append(
                SpecPackageFinding(
                    "package-retirement-unrecorded",
                    f"docs/03.specs/{name}",
                    "retirement requires one Stage 98 Tombstone",
                )
            )
    return tuple(findings)


def _bounded_git(
    root: pathlib.Path,
    *arguments: str,
    byte_limit: int,
) -> bytes:
    if type(byte_limit) is not int or byte_limit < 0:
        raise SpecPackageError("Spec Package Git snapshot byte budget is invalid")
    process: subprocess.Popen[bytes] | None = None
    selector = selectors.DefaultSelector()
    streams: list[object] = []

    def reap() -> None:
        if process is None or process.poll() is not None:
            return
        process.kill()
        try:
            process.wait(timeout=GIT_REAP_TIMEOUT_SECONDS)
        except subprocess.TimeoutExpired as error:
            raise SpecPackageError(
                "cannot reap Spec Package Git snapshot process"
            ) from error

    try:
        process = subprocess.Popen(
            ["git", *arguments],
            cwd=root,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=0,
        )
        if process.stdout is None or process.stderr is None:
            raise SpecPackageError("cannot open Spec Package Git snapshot streams")
        streams = [process.stdout, process.stderr]
        for stream in streams:
            os.set_blocking(stream.fileno(), False)
            selector.register(stream, selectors.EVENT_READ, stream is process.stdout)

        deadline = time.monotonic() + GIT_COMMAND_TIMEOUT_SECONDS
        total = 0
        stdout_chunks: list[bytes] = []
        while selector.get_map():
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise SpecPackageError(
                    "Spec Package Git snapshot exceeded its deadline"
                )
            events = selector.select(remaining)
            if not events:
                if time.monotonic() >= deadline:
                    raise SpecPackageError(
                        "Spec Package Git snapshot exceeded its deadline"
                    )
                continue
            for key, _ in events:
                try:
                    chunk = os.read(
                        key.fd,
                        min(GIT_STREAM_CHUNK_BYTES, byte_limit + 1 - total),
                    )
                except BlockingIOError:
                    continue
                if not chunk:
                    selector.unregister(key.fileobj)
                    continue
                total += len(chunk)
                if total > byte_limit:
                    raise SpecPackageError(
                        "Spec Package Git snapshot exceeds the byte budget"
                    )
                if key.data:
                    stdout_chunks.append(chunk)

        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise SpecPackageError("Spec Package Git snapshot exceeded its deadline")
        try:
            return_code = process.wait(timeout=remaining)
        except subprocess.TimeoutExpired as error:
            raise SpecPackageError(
                "Spec Package Git snapshot exceeded its deadline"
            ) from error
        if return_code != 0:
            raise SpecPackageError("cannot read Spec Package Git snapshot")
        return b"".join(stdout_chunks)
    except SpecPackageError:
        reap()
        raise
    except OSError as error:
        reap()
        raise SpecPackageError(
            f"cannot read Spec Package Git snapshot: {error}"
        ) from error
    finally:
        selector.close()
        for stream in streams:
            stream.close()


def _safe_repository_path(value: str) -> bool:
    path = pathlib.PurePosixPath(value)
    return (
        bool(value)
        and not value.startswith("-")
        and not path.is_absolute()
        and all(
            part not in {"", ".", ".."}
            and not part.startswith("-")
            and "\\" not in part
            and not any(
                ord(character) < 32 or ord(character) == 127 for character in part
            )
            for part in path.parts
        )
        and path.as_posix() == value
    )


def _canonical_package_path(path: pathlib.PurePosixPath) -> bool:
    return (
        len(path.parts) == 3
        and path.parts[:2] == ("docs", "03.specs")
        and _PACKAGE_PATH.fullmatch(path.parts[2]) is not None
        and _safe_repository_path(path.as_posix())
    )


def _filesystem_package_tree(
    root: pathlib.Path,
    package_path: pathlib.PurePosixPath,
) -> Mapping[pathlib.PurePosixPath, bytes]:
    if not _safe_repository_path(package_path.as_posix()):
        raise SpecPackageError("preserved package path is unsafe")
    absolute = pathlib.Path(root) / package_path.as_posix()
    parent, descriptor, name, snapshot = _open_directory_path(
        absolute,
        "preserved Spec Package",
    )
    files: dict[pathlib.PurePosixPath, bytes] = {}
    budget = _LoadBudget()

    def visit(
        directory_descriptor: int,
        relative: pathlib.PurePosixPath,
        depth: int,
    ) -> None:
        nonlocal budget
        if depth > 3:
            raise SpecPackageError("preserved Spec Package nesting is too deep")
        entries, budget = _bounded_directory_names(
            directory_descriptor,
            label="preserved Spec Package",
            limit=MAX_PACKAGE_ENTRIES,
            limit_message="preserved Spec Package contains too many entries",
            budget=budget,
        )
        for entry in entries:
            entry_path = relative / entry
            try:
                metadata = os.stat(
                    entry,
                    dir_fd=directory_descriptor,
                    follow_symlinks=False,
                )
            except OSError as error:
                raise SpecPackageError(
                    f"cannot stat preserved Spec Package entry: {error}"
                ) from error
            if stat.S_ISDIR(metadata.st_mode) and not stat.S_ISLNK(metadata.st_mode):
                child, child_snapshot = _open_directory_at(
                    directory_descriptor,
                    entry,
                    "preserved Spec Package directory",
                )
                try:
                    visit(child, entry_path, depth + 1)
                    _verify_directory_entry(
                        directory_descriptor,
                        entry,
                        child,
                        child_snapshot,
                        "preserved Spec Package directory",
                    )
                finally:
                    os.close(child)
                continue
            if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode):
                raise SpecPackageError(
                    "preserved Spec Package entries must be regular files or directories"
                )
            text, budget = _read_regular_utf8_at(
                directory_descriptor,
                entry,
                "preserved Spec Package file",
                budget,
            )
            files[entry_path] = text.encode("utf-8")
            if len(files) > MAX_PACKAGE_ENTRIES:
                raise SpecPackageError("preserved Spec Package file limit exceeded")

    try:
        visit(descriptor, pathlib.PurePosixPath(), 0)
        _verify_directory_entry(
            parent,
            name,
            descriptor,
            snapshot,
            "preserved Spec Package",
        )
    finally:
        os.close(descriptor)
        os.close(parent)
    return files


def _git_package_tree(
    root: pathlib.Path,
    commit: str,
    package_path: pathlib.PurePosixPath,
) -> Mapping[pathlib.PurePosixPath, bytes]:
    if not _canonical_package_path(package_path):
        raise SpecPackageError("source package path is not canonical")
    tree = _bounded_git(
        root,
        "ls-tree",
        "-r",
        "-z",
        commit,
        "--",
        package_path.as_posix(),
        byte_limit=4 * 1024 * 1024,
    )
    files: dict[pathlib.PurePosixPath, bytes] = {}
    total_bytes = 0
    prefix = package_path.as_posix() + "/"
    for raw in tree.split(b"\0"):
        if not raw:
            continue
        try:
            metadata, raw_path = raw.split(b"\t", 1)
            mode, object_type, _ = metadata.split(b" ", 2)
            source = raw_path.decode("utf-8")
        except (ValueError, UnicodeDecodeError) as error:
            raise SpecPackageError("source package Git tree is malformed") from error
        if mode not in {b"100644", b"100755"} or object_type != b"blob":
            raise SpecPackageError("source package contains a non-regular Git object")
        if not source.startswith(prefix) or not _safe_repository_path(source):
            raise SpecPackageError("source package Git path is unsafe")
        relative = pathlib.PurePosixPath(source[len(prefix) :])
        if not relative.parts or relative in files:
            raise SpecPackageError("source package Git path is duplicated")
        payload = _bounded_git(
            root,
            "show",
            f"{commit}:{source}",
            byte_limit=MAX_SPEC_FILE_BYTES,
        )
        total_bytes += len(payload)
        if total_bytes > MAX_TOTAL_FILE_BYTES:
            raise SpecPackageError("source package exceeds the aggregate byte limit")
        files[relative] = payload
        if len(files) > MAX_PACKAGE_ENTRIES:
            raise SpecPackageError("source package file limit exceeded")
    if pathlib.PurePosixPath("spec.md") not in files:
        raise SpecPackageError("source package has no spec.md")
    return files


def _matches_existing_regular_blob(
    root: pathlib.Path,
    path: pathlib.PurePosixPath,
    payload: bytes,
) -> bool:
    """Match an archive body only against an already committed lineage."""

    for reference in ("HEAD", "MERGE_HEAD"):
        try:
            commit = (
                _bounded_git(
                    root,
                    "rev-parse",
                    "--verify",
                    "--end-of-options",
                    f"{reference}^{{commit}}",
                    byte_limit=256,
                )
                .decode("ascii")
                .strip()
            )
            if _RECOVERY_COMMIT.fullmatch(commit) is None:
                continue
            listing = _bounded_git(
                root,
                "ls-tree",
                "-z",
                commit,
                "--",
                path.as_posix(),
                byte_limit=512,
            )
        except (SpecPackageError, UnicodeDecodeError):
            continue
        rows = tuple(row for row in listing.split(b"\0") if row)
        if len(rows) != 1:
            continue
        try:
            metadata, raw_path = rows[0].split(b"\t", 1)
            mode, object_type, object_id = metadata.split(b" ", 2)
            listed_path = raw_path.decode("utf-8")
            object_name = object_id.decode("ascii")
        except (ValueError, UnicodeDecodeError):
            continue
        if (
            mode not in {b"100644", b"100755"}
            or object_type != b"blob"
            or listed_path != path.as_posix()
            or _RECOVERY_COMMIT.fullmatch(object_name) is None
        ):
            continue
        try:
            size_text = (
                _bounded_git(
                    root,
                    "cat-file",
                    "-s",
                    object_name,
                    byte_limit=64,
                )
                .decode("ascii")
                .strip()
            )
            if not size_text.isdigit() or int(size_text) != len(payload):
                continue
            committed = _bounded_git(
                root,
                "cat-file",
                "blob",
                object_name,
                byte_limit=MAX_SPEC_FILE_BYTES,
            )
        except (SpecPackageError, UnicodeDecodeError):
            continue
        if committed == payload:
            return True
    return False


def _snapshot_document(
    path: pathlib.PurePosixPath,
    text: str,
) -> SpecDocument | None:
    package_match = (
        _PACKAGE_PATH.fullmatch(path.parts[2]) if len(path.parts) >= 4 else None
    )
    if path.parts[:2] != ("docs", "03.specs") or package_match is None:
        return None
    number = package_match.group("number")
    profile_id: str
    artifact_id: str
    if len(path.parts) == 4 and path.name == "spec.md":
        profile_id = "spec"
        artifact_id = f"SPEC-{number}"
    elif len(path.parts) == 4 and path.name == "plan.md":
        profile_id = "plan"
        artifact_id = f"SPEC-{number}-PLAN-0001"
    elif len(path.parts) == 5 and path.parts[3] == "tasks":
        match = _TASK_PATH.fullmatch(path.name)
        if match is None:
            raise SpecPackageError(f"base Task path is not canonical: {path}")
        profile_id = "task"
        artifact_id = f"SPEC-{number}-TSK-{match.group('number')}"
    else:
        return None
    try:
        record = frontmatter_record_from_text(pathlib.Path(path.as_posix()), text)
    except FrontmatterError as error:
        raise SpecPackageError(
            f"cannot parse base Spec Package member: {path}"
        ) from error
    status = record.metadata.get("status")
    parents = record.metadata.get("parent_ids")
    if (
        record.metadata.get("artifact_id") != artifact_id
        or not isinstance(status, str)
        or not isinstance(parents, tuple)
    ):
        raise SpecPackageError(f"base Spec Package metadata is malformed: {path}")
    parent_ids = tuple(parent for parent in parents if isinstance(parent, str))
    if len(parent_ids) != len(parents):
        raise SpecPackageError(f"base Spec Package parents are malformed: {path}")
    receipts = (
        _branch_integration_receipts(record.metadata.get("branch_integration_receipts"))
        if profile_id == "task"
        else ()
    )
    return SpecDocument(
        path,
        profile_id,
        artifact_id,
        status,
        parent_ids,
        body=record.body,
        branch_integration_receipts=receipts,
        cancellation=record.metadata.get("cancellation"),
        source_text=text,
    )


def _load_base_spec_packages(
    root: pathlib.Path,
    *,
    base_ref: str,
) -> tuple[SpecPackage, ...]:
    commit = (
        _bounded_git(
            root,
            "rev-parse",
            "--verify",
            f"{base_ref}^{{commit}}",
            byte_limit=256,
        )
        .decode("ascii")
        .strip()
    )
    if _RECOVERY_COMMIT.fullmatch(commit) is None:
        raise SpecPackageError("Spec Package base ref did not resolve to a commit")
    tree = _bounded_git(
        root,
        "ls-tree",
        "-r",
        "-z",
        commit,
        "--",
        "docs/03.specs",
        "docs/04.execution",
        byte_limit=4 * 1024 * 1024,
    )
    documents: dict[pathlib.PurePosixPath, SpecDocument] = {}
    total_bytes = 0
    for raw in tree.split(b"\0"):
        if not raw:
            continue
        try:
            metadata, raw_path = raw.split(b"\t", 1)
            mode = metadata.split(b" ", 1)[0]
            source = raw_path.decode("utf-8")
        except (ValueError, UnicodeDecodeError) as error:
            raise SpecPackageError("Spec Package base tree is malformed") from error
        path = pathlib.PurePosixPath(source)
        if not (
            len(path.parts) >= 4
            and path.parts[:2] == ("docs", "03.specs")
            and _PACKAGE_PATH.fullmatch(path.parts[2]) is not None
            and (
                path.name in {"spec.md", "plan.md"}
                or (len(path.parts) == 5 and path.parts[3] == "tasks")
            )
        ):
            continue
        if mode not in {b"100644", b"100755"}:
            raise SpecPackageError(
                f"base Spec Package member is not a regular blob: {source}"
            )
        payload = _bounded_git(
            root,
            "show",
            f"{commit}:{source}",
            byte_limit=MAX_SPEC_FILE_BYTES,
        )
        if len(payload) > MAX_SPEC_FILE_BYTES:
            raise SpecPackageError(
                f"base Spec Package member exceeds the byte limit: {source}"
            )
        total_bytes += len(payload)
        if total_bytes > MAX_TOTAL_FILE_BYTES:
            raise SpecPackageError("base Spec Package snapshot exceeds aggregate bytes")
        try:
            text = payload.decode("utf-8")
        except UnicodeDecodeError as error:
            raise SpecPackageError(
                f"base Spec Package member is not UTF-8: {source}"
            ) from error
        document = _snapshot_document(path, text)
        if document is not None:
            if path in documents:
                raise SpecPackageError(f"duplicate base Spec Package member: {path}")
            documents[path] = document
        if len(documents) > MAX_TOTAL_ENTRIES:
            raise SpecPackageError(
                "base Spec Package snapshot exceeds aggregate entries"
            )
    grouped: dict[str, list[SpecDocument]] = {}
    for document in documents.values():
        grouped.setdefault(document.path.parts[2], []).append(document)
    packages: list[SpecPackage] = []
    for package_name, members in sorted(grouped.items()):
        match = _PACKAGE_PATH.fullmatch(package_name)
        assert match is not None
        specs = [member for member in members if member.profile_id == "spec"]
        plans = [member for member in members if member.profile_id == "plan"]
        tasks = tuple(
            sorted(
                (member for member in members if member.profile_id == "task"),
                key=lambda member: member.path.as_posix(),
            )
        )
        if len(specs) != 1 or len(plans) > 1:
            raise SpecPackageError(
                f"base Spec Package ownership is incomplete: {package_name}"
            )
        packages.append(
            SpecPackage(
                root / "docs/03.specs" / package_name,
                match.group("number"),
                match.group("slug"),
                specs[0],
                plans[0] if plans else None,
                tasks,
                (),
            )
        )
    return tuple(packages)


def _heading_anchor(heading: str) -> str:
    normalized = re.sub(r"[^a-z0-9 -]", "", heading.lower()).strip()
    return re.sub(r"-+", "-", re.sub(r"[ ]+", "-", normalized))


def _migration_proof(
    current: Sequence[SpecPackage],
    registry: DocumentRegistry,
    *,
    root: pathlib.Path | None = None,
    target_generation: int | None = None,
) -> _MigrationProof:
    events_contract = registry.common.get("task_lifecycle_events")
    migration = (
        events_contract.get("migration")
        if isinstance(events_contract, Mapping)
        else None
    )
    section_name = (
        events_contract.get("section") if isinstance(events_contract, Mapping) else None
    )
    if not isinstance(migration, Mapping) or not isinstance(section_name, str):
        raise SpecPackageError("lifecycle generation migration contract is missing")
    subsection = migration.get("subsection")
    raw_headers = migration.get("table_headers")
    if (
        not isinstance(subsection, str)
        or not isinstance(raw_headers, (list, tuple))
        or len(raw_headers) != 3
        or not all(isinstance(header, str) and header for header in raw_headers)
    ):
        raise SpecPackageError("lifecycle generation migration contract is malformed")
    proofs: list[_MigrationProof] = []
    for package in current:
        for task in package.tasks:
            section = _contract_section(task.body, section_name)
            marker = "### " + subsection
            starts = [index for index, line in enumerate(section) if line == marker]
            if not starts:
                continue
            if len(starts) != 1:
                raise SpecPackageError("Contract Migration subsection must occur once")
            start = starts[0] + 1
            end = next(
                (
                    index
                    for index in range(start, len(section))
                    if section[index].startswith("### ")
                ),
                len(section),
            )
            rows = _registered_table_rows(section[start:end], tuple(raw_headers))
            if len(rows) != 1:
                raise SpecPackageError(
                    "Contract Migration requires exactly one proof row"
                )
            date, revision, evidence = rows[0]
            try:
                datetime.date.fromisoformat(date)
            except ValueError as error:
                raise SpecPackageError("Contract Migration date is invalid") from error
            if _RECOVERY_COMMIT.fullmatch(revision) is None:
                raise SpecPackageError(
                    "Contract Migration source revision must be a full object ID"
                )
            evidence_match = re.fullmatch(
                r"#(?P<anchor>[a-z0-9][a-z0-9-]*): \S.*", evidence
            )
            if evidence_match is None:
                raise SpecPackageError(
                    "Contract Migration evidence must name one same-Task anchor"
                )
            anchor = evidence_match.group("anchor")
            visible = _completion_visible_lines(task.body)
            anchor_count = sum(
                line == f'<a id="{anchor}"></a>'
                or (
                    (match := re.fullmatch(r"#{1,6} +(.+?) *#*", line)) is not None
                    and _heading_anchor(match.group(1)) == anchor
                )
                for line in visible
            )
            if anchor == _heading_anchor(subsection) or anchor_count != 1:
                raise SpecPackageError(
                    "Contract Migration evidence must name one unique same-Task anchor"
                )
            proofs.append(_MigrationProof(revision, task.path))
    if root is not None and target_generation is not None:
        expected_source_generation = (
            target_generation - 1 if target_generation > 4 else None
        )
        matching: list[_MigrationProof] = []
        for proof in proofs:
            raw = load_registry_document_at_revision(proof.source_revision, root=root)
            common = raw.get("common")
            source_generation = (
                common.get("lifecycle_generation")
                if isinstance(common, Mapping)
                else None
            )
            if source_generation == expected_source_generation:
                matching.append(proof)
        proofs = matching
    if len(proofs) != 1:
        raise SpecPackageError("lifecycle generation migration requires one proof")
    return proofs[0]


def resolve_contract_migration_source(
    root: pathlib.Path,
    current: Sequence[SpecPackage],
    registry: DocumentRegistry,
    *,
    target_generation: int = 5,
) -> str:
    """Resolve proven historical type provenance without changing lifecycle baselines."""

    if (
        target_generation != 5
        or registry.common.get("lifecycle_generation") != target_generation
    ):
        raise SpecPackageError("historical type source requires lifecycle generation 5")
    try:
        proof = _migration_proof(
            current, registry, root=root, target_generation=target_generation
        )
        source_registry = load_registry_document_at_revision(
            proof.source_revision, root=root
        )
        _validate_source_registry(
            source_registry,
            target_generation,
            source_revision=proof.source_revision,
            root=root,
        )
    except RegistryError as error:
        raise SpecPackageError(str(error)) from error
    ancestor = (
        _bounded_git(root, "merge-base", proof.source_revision, "HEAD", byte_limit=256)
        .decode("ascii")
        .strip()
    )
    if ancestor != proof.source_revision:
        raise SpecPackageError(
            "Contract Migration source revision is not a current ancestor"
        )
    _generation_integration(root, proof, target_generation=target_generation)
    return proof.source_revision


def _generation_integration(
    root: pathlib.Path,
    proof: _MigrationProof,
    *,
    target_generation: int,
) -> _GenerationIntegration:
    """Find the one first-parent merge that admitted the typed migration.

    The migration Task binds the generation-4 source, while a local integration
    can also bring a terminal generation-3 Task from main.  The merge is usable
    only when its non-main parent descends from that exact source and its tree
    contains the target Registry generation.  This avoids treating an
    arbitrary current revision as a historical source.
    """

    raw_revisions = _bounded_git(
        root,
        "rev-list",
        "--first-parent",
        "--merges",
        "HEAD",
        byte_limit=MAX_TOTAL_ENTRIES * 41,
    )
    revisions = tuple(raw_revisions.decode("ascii").splitlines())
    if len(revisions) > MAX_TOTAL_ENTRIES or any(
        _RECOVERY_COMMIT.fullmatch(revision) is None for revision in revisions
    ):
        raise SpecPackageError("generation integration history is malformed")
    matches: list[_GenerationIntegration] = []
    for revision in revisions:
        parent_line = (
            _bounded_git(
                root,
                "rev-list",
                "--parents",
                "-n",
                "1",
                revision,
                byte_limit=256,
            )
            .decode("ascii")
            .strip()
            .split()
        )
        if len(parent_line) != 3 or parent_line[0] != revision:
            continue
        main_parent, migration_parent = parent_line[1:]
        try:
            current_registry = load_registry_document_at_revision(revision, root=root)
        except RegistryError:
            continue
        current_common = current_registry.get("common")
        if (
            not isinstance(current_common, Mapping)
            or current_common.get("lifecycle_generation") != target_generation
        ):
            continue
        try:
            main_registry = load_registry_document_at_revision(main_parent, root=root)
        except RegistryError:
            continue
        main_common = main_registry.get("common")
        if (
            isinstance(main_common, Mapping)
            and main_common.get("lifecycle_generation") == target_generation
        ):
            continue
        ancestor = (
            _bounded_git(
                root,
                "merge-base",
                proof.source_revision,
                migration_parent,
                byte_limit=256,
            )
            .decode("ascii")
            .strip()
        )
        if ancestor == proof.source_revision:
            matches.append(_GenerationIntegration(revision, main_parent))
    if len(matches) != 1:
        raise SpecPackageError(
            "lifecycle generation migration requires one main integration"
        )
    return matches[0]


def _validate_source_registry(
    raw: Mapping[str, object],
    target_generation: int = 4,
    *,
    source_revision: str | None = None,
    root: pathlib.Path = pathlib.Path("."),
) -> None:
    findings = (
        validate_registry_at_revision(source_revision, root=root)
        if source_revision is not None
        else validate_registry(raw)
    )
    if findings:
        raise SpecPackageError("migration source Registry is invalid")
    common = raw.get("common")
    if not isinstance(common, Mapping):
        raise SpecPackageError("migration source Registry common contract is missing")
    if target_generation == 5:
        if common.get("lifecycle_generation") != 4:
            raise SpecPackageError(
                "generation 5 migration source must be lifecycle generation 4"
            )
        return
    if "lifecycle_generation" in common:
        raise SpecPackageError(
            "migration source must be the original lifecycle generation"
        )
    expected_lifecycles = {
        "spec": (
            "draft",
            "review",
            "approved",
            "active",
            "completed",
            "cancelled",
            "superseded",
        ),
        "plan": ("draft", "approved", "active", "completed", "cancelled"),
        "task": ("draft", "ready", "in-progress", "blocked", "completed", "cancelled"),
    }
    lifecycles = raw.get("lifecycles")
    if not isinstance(lifecycles, Mapping):
        raise SpecPackageError("migration source lifecycle contracts are missing")
    for name, expected in expected_lifecycles.items():
        contract = lifecycles.get(name)
        if (
            not isinstance(contract, Mapping)
            or tuple(contract.get("statuses", ())) != expected
        ):
            raise SpecPackageError(
                f"migration source {name} lifecycle is not canonical"
            )
    profiles = raw.get("profiles")
    by_id = (
        {
            profile.get("id"): profile
            for profile in profiles
            if isinstance(profile, Mapping)
        }
        if isinstance(profiles, list)
        else {}
    )
    expected_parents = {"plan": ("spec",), "task": ("spec", "plan", "task")}
    for profile_id, expected in expected_parents.items():
        traceability = by_id.get(profile_id, {}).get("traceability")
        if (
            not isinstance(traceability, Mapping)
            or tuple(traceability.get("allowed_parent_profiles", ())) != expected
            or "parent_count" in traceability
        ):
            raise SpecPackageError(
                f"migration source {profile_id} traceability is not canonical"
            )


def _generation_normalizations(
    source: Sequence[SpecPackage],
    current: Sequence[SpecPackage],
    registry: DocumentRegistry,
) -> frozenset[tuple[str, str, str]]:
    source_documents = _documents(source)
    current_documents = _documents(current)
    source_tasks = {
        path: document
        for path, document in source_documents.items()
        if document.profile_id == "task"
    }
    appended_by_artifact: dict[str, list[_LifecycleEvent]] = {}
    for task in (
        document
        for document in current_documents.values()
        if document.profile_id == "task"
    ):
        before = source_tasks.get(task.path)
        current_rows = _lifecycle_event_rows(task, registry)
        source_rows = _lifecycle_event_rows(before, registry) if before else ()
        if current_rows[: len(source_rows)] != source_rows:
            raise SpecPackageError(
                "existing lifecycle event rows must remain an exact prefix"
            )
        for event in current_rows[len(source_rows) :]:
            appended_by_artifact.setdefault(event.artifact_id, []).append(event)
    normalizations: set[tuple[str, str, str]] = set()
    for path, document in current_documents.items():
        before = source_documents.get(path)
        if before is None or before.status == document.status:
            continue
        if document.profile_id not in {"spec", "plan"}:
            continue
        if before.status != "active":
            raise SpecPackageError(
                f"unsupported lifecycle generation normalization: {path}"
            )
        target = document.status
        if target not in {"approved", "in-progress", "blocked"}:
            events = appended_by_artifact.get(document.artifact_id, ())
            target = events[0].source if events else ""
            if target not in {"approved", "in-progress", "blocked"}:
                raise SpecPackageError(
                    f"unsupported lifecycle generation normalization: {path}"
                )
        normalizations.add((path.as_posix(), before.status, target))
    return frozenset(normalizations)


def _validate_terminal_task_migration(
    source: Sequence[SpecPackage], current: Sequence[SpecPackage]
) -> None:
    current_documents = _documents(current)
    current_packages = {package.spec.path.parts[2] for package in current}
    for path, before in _documents(source).items():
        if before.profile_id != "task" or before.status not in {
            "completed",
            "cancelled",
        }:
            continue
        task = current_documents.get(path)
        if task is None:
            if path.parts[2] not in current_packages:
                continue
            raise SpecPackageError(
                f"terminal Task removed during contract migration: {path}"
            )
        if not _terminal_task_migration_matches(before, task):
            raise SpecPackageError(f"terminal Task body or identity changed: {path}")


def _terminal_task_migration_matches(before: SpecDocument, task: SpecDocument) -> bool:
    """Match a terminal Task while allowing only the approved envelope move."""

    if (
        before.path != task.path
        or before.profile_id != "task"
        or task.profile_id != "task"
        or before.artifact_id != task.artifact_id
        or before.status not in {"completed", "cancelled"}
        or before.status != task.status
        or not before.source_text
        or not task.source_text
    ):
        return False
    try:
        before_record = frontmatter_record_from_text(
            pathlib.Path(before.path.as_posix()), before.source_text
        )
        current_record = frontmatter_record_from_text(
            pathlib.Path(task.path.as_posix()), task.source_text
        )
    except FrontmatterError:
        return False
    before_metadata = {
        key: value
        for key, value in before_record.metadata.items()
        if key not in {"parent_ids", "updated"}
    }
    current_metadata = {
        key: value
        for key, value in current_record.metadata.items()
        if key not in {"parent_ids", "updated"}
    }
    return (
        before_record.body == current_record.body
        and before_metadata == current_metadata
    )


def _mainline_historical_terminal_tasks(
    generation_source: Sequence[SpecPackage],
    main_source: Sequence[SpecPackage],
    integration: Sequence[SpecPackage],
    current: Sequence[SpecPackage],
) -> frozenset[pathlib.PurePosixPath]:
    """Admit terminal Tasks added on main before the typed migration merge.

    A candidate must be absent from the Task-declared generation source,
    already terminal on the merge's main parent, preserve its body and identity
    through that merge, and remain byte-for-byte identical to the merge blob in
    the current tree. UTF-8 decoding is lossless here, so newline changes remain
    observable in the complete source-text comparison.
    """

    generation_paths = set(_documents(generation_source))
    integration_documents = _documents(integration)
    current_documents = _documents(current)
    admitted: set[pathlib.PurePosixPath] = set()
    for path, before in _documents(main_source).items():
        if (
            path in generation_paths
            or before.profile_id != "task"
            or before.status not in {"completed", "cancelled"}
        ):
            continue
        merged = integration_documents.get(path)
        task = current_documents.get(path)
        if (
            merged is None
            or task is None
            or not _terminal_task_migration_matches(before, merged)
            or merged.path != task.path
            or merged.profile_id != task.profile_id
            or merged.artifact_id != task.artifact_id
            or merged.status != task.status
            or not merged.source_text
            or merged.source_text != task.source_text
        ):
            continue
        admitted.add(path)
    return frozenset(admitted)


def _lifecycle_event_rows(
    task: SpecDocument,
    registry: DocumentRegistry,
) -> tuple[_LifecycleEvent, ...]:
    contract = registry.common.get("task_lifecycle_events")
    if contract is None:
        return ()
    if not isinstance(contract, Mapping):
        raise SpecPackageError("Task lifecycle event contract is malformed")
    section_name = contract.get("section")
    subsection_name = contract.get("subsection")
    raw_headers = contract.get("table_headers")
    if (
        not isinstance(section_name, str)
        or not isinstance(subsection_name, str)
        or not isinstance(raw_headers, (list, tuple))
        or not all(isinstance(header, str) and header for header in raw_headers)
    ):
        raise SpecPackageError("Task lifecycle event contract is malformed")
    section = _contract_section(task.body, section_name)
    marker = "### " + subsection_name
    starts = [index for index, line in enumerate(section) if line == marker]
    if not starts:
        return ()
    if len(starts) != 1:
        raise SpecPackageError(f"Task lifecycle evidence requires one {marker}")
    start = starts[0] + 1
    end = next(
        (
            index
            for index in range(start, len(section))
            if section[index].startswith("### ")
        ),
        len(section),
    )
    rows = _registered_table_rows(section[start:end], tuple(raw_headers))
    if not rows:
        return ()
    anchor_counts: dict[str, int] = {}
    for line in _completion_visible_lines(task.body):
        match = re.fullmatch(r"#{1,6} +(.+?) *#*", line)
        if match is None:
            continue
        anchor = _heading_anchor(match.group(1))
        anchor_counts[anchor] = anchor_counts.get(anchor, 0) + 1
    events: list[_LifecycleEvent] = []
    for artifact_id, source, target, evidence in rows:
        if (
            re.fullmatch(r"#[a-z0-9][a-z0-9-]*", evidence) is None
            or evidence == "#" + _heading_anchor(subsection_name)
            or anchor_counts.get(evidence[1:]) != 1
        ):
            raise SpecPackageError(
                "Task lifecycle event evidence must be one unique same-Task heading anchor"
            )
        events.append(
            _LifecycleEvent(
                artifact_id,
                source,
                target,
                evidence,
                task.path,
            )
        )
    return tuple(events)


def _event_finding(path: pathlib.PurePosixPath, message: str) -> SpecPackageFinding:
    return SpecPackageFinding(
        "task-lifecycle-events-invalid",
        path.as_posix(),
        message,
    )


def _validate_task_lifecycle_events(
    previous: Sequence[SpecPackage],
    current: Sequence[SpecPackage],
    registry: DocumentRegistry,
    *,
    prefix_previous: Sequence[SpecPackage] | None = None,
    normalizations: frozenset[tuple[str, str, str]] = frozenset(),
    source_registry: Mapping[str, object] | None = None,
) -> tuple[tuple[SpecPackageFinding, ...], frozenset[tuple[str, str, str]]]:
    previous_by_name = {package.spec.path.parts[2]: package for package in previous}
    prefix_by_name = {
        package.spec.path.parts[2]: package
        for package in (prefix_previous if prefix_previous is not None else previous)
    }
    normalization_by_path = {
        pathlib.PurePosixPath(path): (source, target)
        for path, source, target in normalizations
    }
    historical_transitions: Mapping[str, object] = {}
    if isinstance(source_registry, Mapping):
        raw_lifecycles = source_registry.get("lifecycles")
        if isinstance(raw_lifecycles, Mapping):
            historical_transitions = raw_lifecycles
    findings: list[SpecPackageFinding] = []
    actual: set[tuple[str, str, str]] = set()
    for package in current:
        prior = previous_by_name.get(package.spec.path.parts[2])
        prior_tasks = {task.path: task for task in prior.tasks} if prior else {}
        prefix = prefix_by_name.get(package.spec.path.parts[2])
        prefix_tasks = {task.path: task for task in prefix.tasks} if prefix else {}
        historical_suffix: list[_LifecycleEvent] = []
        current_suffix: list[_LifecycleEvent] = []
        for task in package.tasks:
            try:
                current_rows = _lifecycle_event_rows(task, registry)
                previous_rows = (
                    _lifecycle_event_rows(prefix_tasks[task.path], registry)
                    if task.path in prefix_tasks
                    else ()
                )
            except SpecPackageError as error:
                findings.append(_event_finding(task.path, str(error)))
                continue
            if current_rows[: len(previous_rows)] != previous_rows:
                findings.append(
                    _event_finding(
                        task.path,
                        "existing lifecycle event rows must remain an exact prefix",
                    )
                )
                continue
            base_rows = (
                _lifecycle_event_rows(prior_tasks[task.path], registry)
                if task.path in prior_tasks
                else ()
            )
            if current_rows[: len(base_rows)] != base_rows:
                findings.append(
                    _event_finding(
                        task.path,
                        "base lifecycle event rows must remain an exact prefix",
                    )
                )
                continue
            if task.path in prefix_tasks:
                historical_suffix.extend(previous_rows[len(base_rows) :])
                current_suffix.extend(current_rows[len(previous_rows) :])
            else:
                current_suffix.extend(current_rows[len(base_rows) :])

        members = [package.spec, *package.tasks]
        if package.plan is not None:
            members.append(package.plan)
        by_artifact = {member.artifact_id: member for member in members}
        previous_members = _documents((prior,)) if prior is not None else {}
        historical_grouped: dict[str, list[_LifecycleEvent]] = {}
        grouped: dict[str, list[_LifecycleEvent]] = {}
        for event, historical in (
            *((event, True) for event in historical_suffix),
            *((event, False) for event in current_suffix),
        ):
            document = by_artifact.get(event.artifact_id)
            if document is None:
                findings.append(
                    _event_finding(
                        event.host_path,
                        "lifecycle event Artifact must name a current member of the same package",
                    )
                )
                continue
            lifecycle = historical_transitions.get(document.profile_id)
            transitions = (
                lifecycle.get("transitions", {})
                if historical and isinstance(lifecycle, Mapping)
                else registry.transitions.get(document.profile_id, {})
            )
            if event.target not in transitions.get(event.source, ()):
                findings.append(
                    _event_finding(
                        event.host_path,
                        f"lifecycle event is not a registered direct edge: {event.source} -> {event.target}",
                    )
                )
                continue
            target = historical_grouped if historical else grouped
            target.setdefault(event.artifact_id, []).append(event)

        for document in members:
            previous_document = previous_members.get(document.path)
            prefix_document = (
                _documents((prefix,)).get(document.path) if prefix is not None else None
            )
            historical_baseline = (
                previous_document.status
                if previous_document is not None
                else (
                    historical_transitions.get(document.profile_id, {}).get(
                        "initial_status"
                    )
                    if isinstance(
                        historical_transitions.get(document.profile_id), Mapping
                    )
                    else registry.lifecycle_initial_statuses[document.profile_id]
                )
            )
            historical_events = historical_grouped.get(document.artifact_id, [])
            historical_target = (
                prefix_document.status
                if prefix_document is not None
                else historical_baseline
            )
            expected = historical_baseline
            historical_lifecycle = historical_transitions.get(document.profile_id)
            historical_edges = (
                historical_lifecycle.get("transitions", {})
                if isinstance(historical_lifecycle, Mapping)
                else {}
            )
            for event in historical_events:
                if event.source != expected:
                    findings.append(
                        _event_finding(
                            event.host_path,
                            f"lifecycle event chain expected {expected}, found {event.source}",
                        )
                    )
                    break
                expected = event.target
            else:
                historical_direct = historical_target in historical_edges.get(
                    historical_baseline, ()
                )
                if expected != historical_target and not (
                    not historical_events and historical_direct
                ):
                    findings.append(
                        _event_finding(
                            document.path,
                            "checkpoint lifecycle event chain does not match its status",
                        )
                    )

            normalization = normalization_by_path.get(document.path)
            baseline = (
                normalization[1]
                if normalization is not None
                else (
                    prefix_document.status
                    if prefix_document is not None
                    else (
                        previous_document.status
                        if previous_document is not None
                        else registry.lifecycle_initial_statuses[document.profile_id]
                    )
                )
            )
            events = grouped.get(document.artifact_id, [])
            transitions = registry.transitions.get(document.profile_id, {})
            direct = document.status in transitions.get(baseline, ())
            if not events:
                if baseline != document.status and (
                    prefix_document is not None or not direct
                ):
                    findings.append(
                        _event_finding(
                            document.path,
                            f"lifecycle event chain is required for {baseline} -> {document.status}",
                        )
                    )
                elif prefix_document is not None and normalization is None:
                    actual.add(
                        (
                            document.path.as_posix(),
                            historical_baseline,
                            document.status,
                        )
                    )
                continue
            expected = baseline
            for event in events:
                if event.source != expected:
                    findings.append(
                        _event_finding(
                            event.host_path,
                            f"lifecycle event chain expected {expected}, found {event.source}",
                        )
                    )
                    break
                expected = event.target
            else:
                if expected != document.status:
                    findings.append(
                        _event_finding(
                            events[-1].host_path,
                            f"lifecycle event chain ends at {expected}, not {document.status}",
                        )
                    )
                else:
                    if prefix_document is None or normalization is not None:
                        actual.add(
                            (
                                document.path.as_posix(),
                                historical_baseline
                                if prefix_document is not None
                                else baseline,
                                document.status,
                            )
                        )
            if (
                prefix_document is not None
                and normalization is None
                and not any(
                    finding.path == document.path.as_posix() for finding in findings
                )
            ):
                actual.add(
                    (
                        document.path.as_posix(),
                        historical_baseline,
                        document.status,
                    )
                )
    if findings:
        return tuple(sorted(set(findings))), frozenset()
    return (), frozenset(actual)


def _validate_legacy_multirow_receipts(
    previous: Sequence[SpecPackage],
    current: Sequence[SpecPackage],
    registry: DocumentRegistry,
    *,
    migration_source: Sequence[SpecPackage] | None = None,
) -> tuple[SpecPackageFinding, ...]:
    contract = registry.common.get("spec_completion_evidence")
    if not isinstance(contract, Mapping):
        return ()
    previous_documents = _documents(previous)
    migration_documents = (
        _documents(migration_source) if migration_source is not None else {}
    )
    findings: list[SpecPackageFinding] = []
    for package in current:
        for task in package.tasks:
            legacy_section = contract.get("task_section")
            if not isinstance(legacy_section, str) or (
                f"## {legacy_section}" not in task.body.splitlines()
            ):
                continue
            legacy_rows = next(
                (
                    rows
                    for key, rows in _completion_rows(task, contract)
                    if key == "table_headers"
                ),
                (),
            )
            missing_review = not _review_rows(task, registry)
            if len(legacy_rows) <= 1 and not missing_review:
                continue
            before = migration_documents.get(task.path) or previous_documents.get(
                task.path
            )
            if (
                before is not None
                and before.status == task.status == "completed"
                and bool(before.source_text)
                and (
                    before.source_text == task.source_text
                    or (migration_source is not None and before.body == task.body)
                )
            ):
                continue
            findings.append(
                SpecPackageFinding(
                    "task-completion-items-invalid",
                    task.path.as_posix(),
                    "new or changed legacy completion evidence requires item statuses "
                    "and Review Evidence",
                )
            )
    return tuple(findings)


def _standard_preserved_package_path(
    disposition: str,
    origin: pathlib.PurePosixPath,
) -> pathlib.PurePosixPath:
    if not _canonical_package_path(origin):
        raise SpecPackageError("preserved origin package path is not canonical")
    return pathlib.PurePosixPath("docs/98.archive", disposition, *origin.parts[1:])


def _load_preserved_spec_packages(
    root: pathlib.Path,
    disposition: str,
    registry: DocumentRegistry,
) -> tuple[SpecPackage, ...]:
    stage = root / f"docs/98.archive/{disposition}/03.specs"
    try:
        metadata = os.lstat(stage)
    except FileNotFoundError:
        return ()
    except OSError as error:
        raise SpecPackageError(
            f"cannot inspect {disposition} Spec archive: {error}"
        ) from error
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
        raise SpecPackageError(
            f"{disposition} Spec archive must be a non-symlink directory"
        )
    # Historical archives include records created before completion receipts
    # became mandatory; current packages still enforce that authoring gate.
    return load_spec_packages(
        stage,
        registry=registry,
        _completion_evidence=False,
        _current_contracts=False,
    )


def _archive_receipt_carriers(
    completed: Sequence[SpecPackage],
) -> tuple[_ReceiptCarrier, ...]:
    return tuple(
        _ReceiptCarrier(receipt, task, package, completed_archive=True)
        for package in completed
        for task in package.tasks
        for receipt in task.branch_integration_receipts
    )


def _current_receipt_carriers(
    current: Sequence[SpecPackage],
) -> tuple[_ReceiptCarrier, ...]:
    return tuple(
        _ReceiptCarrier(receipt, task, package)
        for package in current
        for task in package.tasks
        for receipt in task.branch_integration_receipts
    )


def _ordinary_preserved_paths(
    root: pathlib.Path,
    previous: Sequence[SpecPackage],
    current: Sequence[SpecPackage],
    completed: Sequence[SpecPackage],
    registry: DocumentRegistry,
) -> frozenset[pathlib.PurePosixPath]:
    current_names = {package.spec.path.parts[2] for package in current}
    preserved: set[pathlib.PurePosixPath] = set()
    for source in previous:
        if source.spec.path.parts[2] in current_names:
            continue
        for disposition, packages, required_status in (
            ("completed", completed, "completed"),
            ("superseded", (), "superseded"),
        ):
            if _preserved_package_is_terminal(
                root,
                source,
                disposition,
                packages,
                required_status,
                registry,
            ):
                preserved.add(source.spec.path)
                break
    return frozenset(preserved)


def _preserved_package_is_terminal(
    root: pathlib.Path,
    source: SpecPackage,
    disposition: str,
    packages: Sequence[SpecPackage],
    required_status: str,
    registry: DocumentRegistry,
) -> bool:
    source_members = {
        member.path.relative_to(source.spec.path.parent)
        for member in (
            source.spec,
            *source.tasks,
            *((source.plan,) if source.plan else ()),
        )
    }
    package = next(
        (item for item in packages if item.spec.path.parent == source.spec.path.parent),
        None,
    )
    if package is not None:
        spec = package.spec
        members = [package.spec, *package.tasks]
        if package.plan is not None:
            members.append(package.plan)
        try:
            _validate_completion_evidence(
                package.spec,
                package.plan,
                package.tasks,
                registry,
                current_contracts=False,
            )
        except SpecPackageError:
            return False
    else:
        try:
            tree = _filesystem_package_tree(
                root,
                _standard_preserved_package_path(disposition, source.spec.path.parent),
            )
            members = [
                document
                for relative, payload in tree.items()
                if (
                    document := _snapshot_document(
                        source.spec.path.parent / relative,
                        payload.decode("utf-8"),
                    )
                )
                is not None
            ]
            spec = next(
                (member for member in members if member.profile_id == "spec"),
                None,
            )
        except (FileNotFoundError, SpecPackageError, UnicodeDecodeError):
            return False
        if spec is None:
            return False
    return (
        spec.artifact_id == source.spec.artifact_id
        and spec.status == required_status
        and source_members
        <= {member.path.relative_to(source.spec.path.parent) for member in members}
        and all(
            member.status in disposition_entry_statuses(member.profile_id, registry)
            for member in members
        )
    )


def _invalid_receipt(
    carrier: _ReceiptCarrier,
    message: str,
) -> SpecPackageFinding:
    return SpecPackageFinding(
        "branch-integration-receipt-invalid",
        carrier.task.path.as_posix(),
        message,
    )


def _validate_receipt_carrier(
    root: pathlib.Path,
    base_commit: str,
    source: SpecPackage,
    current: Sequence[SpecPackage],
    completed_packages: Sequence[SpecPackage],
    carrier: _ReceiptCarrier,
    registry: DocumentRegistry,
) -> SpecPackageFinding | None:
    receipt = carrier.receipt
    origin = source.spec.path.parent
    current_by_path = {package.spec.path.parent: package for package in current}
    if receipt.source_commit != base_commit:
        return _invalid_receipt(carrier, "source_commit is not the lifecycle base")
    if not _canonical_package_path(receipt.source_package_path):
        return _invalid_receipt(carrier, "source_package_path is not canonical")
    if receipt.source_package_path != origin:
        return _invalid_receipt(carrier, "source_package_path does not name the source")
    if receipt.source_artifact_id != source.spec.artifact_id:
        return _invalid_receipt(carrier, "source_artifact_id does not match Git source")
    if origin in current_by_path:
        return _invalid_receipt(carrier, "source package remains in current Stage 03")
    expected_preserved = _standard_preserved_package_path("superseded", origin)
    if receipt.preserved_package_path != expected_preserved:
        return _invalid_receipt(
            carrier, "preserved_package_path is not the exact handoff path"
        )
    if not _canonical_package_path(receipt.target_package_path):
        return _invalid_receipt(carrier, "target_package_path is not canonical")
    if receipt.target_artifact_id == receipt.source_artifact_id:
        return _invalid_receipt(
            carrier, "source and target artifact identities must differ"
        )
    if carrier.package.spec.path.parent != receipt.target_package_path:
        return _invalid_receipt(carrier, "receipt is hosted outside its target package")
    if carrier.package.spec.artifact_id != receipt.target_artifact_id:
        return _invalid_receipt(
            carrier, "target_artifact_id does not match its package"
        )
    if not carrier.completed_archive:
        if carrier.package.spec.status not in {
            "active",
            "in-progress",
            "blocked",
        } or carrier.task.status not in {
            "in-progress",
            "blocked",
        }:
            return _invalid_receipt(
                carrier,
                "current carrier requires an active target Spec and in-progress or blocked Task",
            )
    else:
        members = [carrier.package.spec, *carrier.package.tasks]
        if carrier.package.plan is not None:
            members.append(carrier.package.plan)
        if (
            carrier.package.plan is None
            or not carrier.package.tasks
            or any(member.status != "completed" for member in members)
        ):
            return _invalid_receipt(
                carrier,
                "archived carrier requires one full completed target package",
            )
        try:
            _validate_completion_evidence(
                carrier.package.spec,
                carrier.package.plan,
                carrier.package.tasks,
                registry,
                current_contracts=False,
            )
        except SpecPackageError:
            return _invalid_receipt(
                carrier,
                "archived carrier requires valid completion evidence",
            )
    try:
        source_tree = _git_package_tree(root, base_commit, origin)
        preserved_tree = _filesystem_package_tree(
            root,
            receipt.preserved_package_path,
        )
    except (FileNotFoundError, SpecPackageError) as error:
        return _invalid_receipt(carrier, str(error))
    completed_matches = tuple(
        package
        for package in completed_packages
        if package.spec.artifact_id == receipt.source_artifact_id
    )
    if len(completed_matches) != 1:
        return _invalid_receipt(
            carrier, "same-identity completed record is missing or ambiguous"
        )
    completed = completed_matches[0]
    completed_path = _standard_preserved_package_path(
        "completed", completed.spec.path.parent
    )
    try:
        completed_spec_bytes = _filesystem_package_tree(root, completed_path)[
            pathlib.PurePosixPath("spec.md")
        ]
    except (KeyError, FileNotFoundError, SpecPackageError) as error:
        return _invalid_receipt(carrier, str(error))
    if not _matches_existing_regular_blob(
        root,
        completed_path / "spec.md",
        completed_spec_bytes,
    ):
        return _invalid_receipt(
            carrier,
            "completed Spec must match an existing regular Git blob",
        )
    completed_members = [completed.spec, *completed.tasks]
    if completed.plan is not None:
        completed_members.append(completed.plan)
    if (
        completed.spec.artifact_id != receipt.source_artifact_id
        or completed.spec.status != "completed"
        or any(
            member.status not in disposition_entry_statuses(member.profile_id, registry)
            for member in completed_members
        )
    ):
        return _invalid_receipt(
            carrier,
            "same-identity immutable completed record is missing or invalid",
        )
    if source_tree != preserved_tree:
        return _invalid_receipt(
            carrier,
            "preserved package file set or bytes differ from the Git source",
        )
    return None


def _validate_branch_integration_receipts(
    root: pathlib.Path,
    base_commit: str,
    previous: Sequence[SpecPackage],
    current: Sequence[SpecPackage],
    completed: Sequence[SpecPackage],
    ordinary_preserved: frozenset[pathlib.PurePosixPath],
    registry: DocumentRegistry,
) -> tuple[frozenset[pathlib.PurePosixPath], tuple[SpecPackageFinding, ...]]:
    removed = {
        package.spec.path.parent: package
        for package in previous
        if package.spec.path.parts[2]
        not in {item.spec.path.parts[2] for item in current}
    }
    carriers = (
        *_current_receipt_carriers(current),
        *_archive_receipt_carriers(completed),
    )
    relevant = tuple(
        carrier
        for carrier in carriers
        if carrier.receipt.source_package_path in removed
        or carrier.receipt.source_commit == base_commit
    )
    findings: list[SpecPackageFinding] = []
    accepted: set[pathlib.PurePosixPath] = set()
    for source_path, source in sorted(removed.items(), key=lambda item: item[0]):
        matching = [
            carrier
            for carrier in relevant
            if carrier.receipt.source_package_path == source_path
        ]
        if len(matching) > 1:
            findings.append(
                SpecPackageFinding(
                    "branch-integration-receipt-duplicate",
                    source_path.as_posix(),
                    "exactly one current or completed Task may carry the receipt",
                )
            )
            continue
        if not matching:
            archived = (
                root
                / _standard_preserved_package_path("superseded", source_path).as_posix()
            )
            try:
                present = os.lstat(archived) is not None
            except FileNotFoundError:
                present = False
            except OSError:
                present = True
            if present:
                if _preserved_package_is_terminal(
                    root,
                    source,
                    "superseded",
                    (),
                    "superseded",
                    registry,
                ):
                    continue
                findings.append(
                    SpecPackageFinding(
                        "branch-integration-receipt-required",
                        source_path.as_posix(),
                        "a non-lifecycle branch preservation requires one typed Task receipt",
                    )
                )
            elif source.spec.path in ordinary_preserved:
                continue
            continue
        failure = _validate_receipt_carrier(
            root,
            base_commit,
            source,
            current,
            completed,
            matching[0],
            registry,
        )
        if failure is None:
            accepted.add(source.spec.path)
        else:
            findings.append(failure)
    for carrier in relevant:
        if carrier.receipt.source_package_path not in removed:
            findings.append(
                _invalid_receipt(
                    carrier,
                    "source_package_path does not name a package removed from the base",
                )
            )
    return frozenset(accepted), tuple(findings)


def validate_repository_spec_package_lifecycle_details(
    root: pathlib.Path,
    current: Sequence[SpecPackage],
    *,
    base_ref: str | None = None,
    registry: DocumentRegistry | None = None,
) -> SpecPackageLifecycleValidation:
    """Validate current package lifecycle and return exact observed transitions."""

    root = pathlib.Path(root)
    base_commit = resolve_lifecycle_base(root, base_ref)
    previous = _load_base_spec_packages(
        root,
        base_ref=base_commit,
    )
    registry = registry if registry is not None else load_registry()
    generation = registry.common.get("lifecycle_generation")
    current_surface = any(
        package.plan is not None
        and any(
            task.parent_ids == (package.plan.artifact_id,) for task in package.tasks
        )
        for package in current
    )
    source_registry: Mapping[str, object] | None = None
    source_registry_contract: DocumentRegistry | None = None
    source_packages: tuple[SpecPackage, ...] | None = None
    mainline_historical_tasks: frozenset[pathlib.PurePosixPath] = frozenset()
    normalizations: frozenset[tuple[str, str, str]] = frozenset()
    generation_source: str | None = None
    if current_surface:
        if generation not in {4, 5}:
            raise SpecPackageError("current lifecycle generation must be 4 or 5")
        try:
            base_registry = load_registry_document_at_revision(
                base_commit,
                root=root,
            )
        except RegistryError as error:
            if previous:
                raise SpecPackageError(str(error)) from error
            base_registry = {}
        base_common = base_registry.get("common")
        base_generation = (
            base_common.get("lifecycle_generation")
            if isinstance(base_common, Mapping)
            else None
        )
        if previous and base_generation != generation:
            proof = _migration_proof(
                current,
                registry,
                root=root,
                target_generation=int(generation),
            )
            generation_source = proof.source_revision
            head = (
                _bounded_git(
                    root,
                    "rev-parse",
                    "--verify",
                    "HEAD^{commit}",
                    byte_limit=256,
                )
                .decode("ascii")
                .strip()
            )
            ancestor = (
                _bounded_git(
                    root,
                    "merge-base",
                    generation_source,
                    head,
                    byte_limit=256,
                )
                .decode("ascii")
                .strip()
            )
            if ancestor != generation_source:
                raise SpecPackageError(
                    "Contract Migration source revision is not a current ancestor"
                )
            try:
                source_registry = load_registry_document_at_revision(
                    generation_source,
                    root=root,
                )
            except RegistryError as error:
                raise SpecPackageError(str(error)) from error
            _validate_source_registry(
                source_registry,
                int(generation),
                source_revision=generation_source,
                root=root,
            )
            source_registry_contract = load_registry_at_revision(
                generation_source,
                root=root,
            )
            source_packages = _load_base_spec_packages(
                root,
                base_ref=generation_source,
            )
            integration = _generation_integration(
                root,
                proof,
                target_generation=int(generation),
            )
            if base_commit == integration.main_revision:
                integrated_packages = _load_base_spec_packages(
                    root,
                    base_ref=integration.revision,
                )
                mainline_historical_tasks = _mainline_historical_terminal_tasks(
                    source_packages,
                    previous,
                    integrated_packages,
                    current,
                )
            normalizations = _generation_normalizations(
                source_packages, current, registry
            )
            _validate_terminal_task_migration(source_packages, current)
        elif previous:
            _validate_terminal_task_migration(previous, current)
    event_baseline = (
        _with_missing_historical_tasks(
            source_packages,
            previous,
            mainline_historical_tasks,
        )
        if generation == 5 and source_packages is not None
        else previous
    )
    event_findings, actual_transitions = _validate_task_lifecycle_events(
        event_baseline,
        current,
        registry,
        prefix_previous=source_packages if generation == 4 else None,
        normalizations=normalizations,
        source_registry=source_registry if generation == 4 else None,
    )
    receipt_shape_findings = _validate_legacy_multirow_receipts(
        previous,
        current,
        source_registry_contract or registry,
        migration_source=source_packages,
    )
    completed = _load_preserved_spec_packages(root, "completed", registry)
    ordinary_preserved = _ordinary_preserved_paths(
        root,
        previous,
        current,
        completed,
        registry,
    )
    branch_preserved, receipt_findings = _validate_branch_integration_receipts(
        root,
        base_commit,
        previous,
        current,
        completed,
        ordinary_preserved,
        registry,
    )
    lifecycle_findings = validate_spec_package_lifecycle(
        previous,
        current,
        retired_paths=_recorded_retirements(root),
        preserved_paths=ordinary_preserved | branch_preserved,
        registry=registry,
    )
    return SpecPackageLifecycleValidation(
        tuple(
            sorted(
                (
                    *event_findings,
                    *receipt_shape_findings,
                    *receipt_findings,
                    *lifecycle_findings,
                )
            )
        ),
        actual_transitions,
        normalizations,
        generation_source,
    )


def validate_repository_spec_package_lifecycle(
    root: pathlib.Path,
    current: Sequence[SpecPackage],
    *,
    base_ref: str | None = None,
) -> tuple[SpecPackageFinding, ...]:
    """Validate current removals and lifecycle events against bounded Git."""

    return validate_repository_spec_package_lifecycle_details(
        root,
        current,
        base_ref=base_ref,
    ).findings


def _recorded_retirements(root: pathlib.Path) -> frozenset[pathlib.PurePosixPath]:
    """Stage 98 withdrawal records are the tracked record of an approved retirement.

    A sealed Tombstone records a withdrawal. Once the archive disposition model
    is adopted, a Retention Catalog row for a `retired/` unit records one too,
    and a route-shape Tombstone, which names only a route, records none.
    """

    from scripts.lib.document_governance.archive import (
        load_archive,
        retention_catalog_retirements,
    )
    from scripts.lib.document_governance.registry import (
        ARCHIVE_MODEL_ADOPTED,
        archive_disposition_model,
    )

    root = pathlib.Path(root)
    try:
        inventory = load_archive(root / "docs/98.archive")
    except (OSError, ValueError):
        # Stage 98 has its own gate. An unreadable archive grants no exemption:
        # every removal is judged as unrecorded until the archive is valid.
        return frozenset()
    recorded = frozenset(
        record.retired_path
        for record in inventory.tombstones
        if record.recovery is not None
    )
    if archive_disposition_model(root) != ARCHIVE_MODEL_ADOPTED:
        return recorded
    try:
        return recorded | retention_catalog_retirements(root)
    except (OSError, ValueError):
        # The archive gate reports the unsafe catalog; it grants no exemption.
        return frozenset()


def resolve_lifecycle_base(root: pathlib.Path, explicit: str | None = None) -> str:
    """Pin the explicit/CI base; local no-base compares HEAD to working bytes."""

    selected = (
        explicit if explicit is not None else os.environ.get("TEMPLATE_GATE_BASE")
    )
    if selected is None:
        if os.environ.get("EVENT_NAME") in {"pull_request", "push"}:
            raise SpecPackageError("CI lifecycle comparison requires a trusted base")
        selected = "HEAD"
    if (
        not selected
        or selected.startswith("-")
        or any(ord(character) < 32 for character in selected)
    ):
        raise SpecPackageError("lifecycle comparison base is invalid")
    commit = (
        _bounded_git(
            root,
            "rev-parse",
            "--verify",
            "--end-of-options",
            f"{selected}^{{commit}}",
            byte_limit=256,
        )
        .decode("ascii")
        .strip()
    )
    if _RECOVERY_COMMIT.fullmatch(commit) is None:
        raise SpecPackageError("lifecycle comparison base is not a commit")
    return commit
