"""Minimal Stage 98 inventory and fail-closed Git recovery authority."""

from __future__ import annotations

import collections
import copy
import dataclasses
import hashlib
import os
import pathlib
import re
import stat
from collections.abc import Iterable, Mapping
from typing import Any

import yaml

from scripts.lib.document_governance.frontmatter import safe_load_unique
from scripts.lib.document_governance.git_provenance import (
    HistoricalDocument,
    read_archived_metadata_batch,
    recovery_commit_is_valid,
    verify_recovery_blobs_batch,
)


FROZEN_MIGRATION_SHA256 = "271f21c50cf4ab765422ee552de244a4340c160e53149231eb6be45f03476ab9"
APPROVED_MIGRATION_COMMIT = "494065806794980080b081439298d7b534d10803"
ONE_TIME_VERIFIER_PATHS = (
    "scripts/validation/check-task4-migration.py",
    "tests/validation/test_task4_migration_verifier.py",
)
HISTORICAL_SESSION_SPECS = {
    "docs/03.specs/0090-workspace-audit-2026-05/spec.md": "SPEC-0090",
    "docs/03.specs/0091-workspace-doc-consistency-2026-05/spec.md": "SPEC-0091",
    "docs/03.specs/0092-workspace-consistency-2026-05b/spec.md": "SPEC-0092",
}
TASK10_BASELINE_COMMIT = "f259c139fb7da166609029cdd3657de87e639f6b"
TASK10_FIRST_ROW = "mig-0003-r0566"
TASK10_LAST_ROW = "mig-0003-r0840"
MAX_DOCUMENT_BYTES = 1_048_576
MAX_ARCHIVE_ENTRIES = 512
MAX_ARCHIVE_BYTES = 32 * 1024 * 1024
MAX_ROOT_ENTRIES = 8
MAX_MIGRATION_ENTRIES = 16
MAX_TOMBSTONE_PARTITIONS = 16
MAX_TOMBSTONES_PER_PARTITION = 256
_MIGRATION_NAME = re.compile(r"[0-9]{4}-[a-z0-9]+(?:-[a-z0-9]+)*\.md\Z")
_TOMBSTONE_NAME = re.compile(r"(?P<number>[0-9]{4})-[a-z0-9]+(?:-[a-z0-9]+)*\.md\Z")
_STAGE = re.compile(r"(?:00|01|02|03|05|90|98|99)\.[a-z0-9]+(?:-[a-z0-9]+)*\Z")
_RECOVERY_FIELDS = frozenset({"status", "recovery_commit", "original_path"})
_MIGRATION_FIELDS = frozenset(
    {
        "schema_version",
        "migration_id",
        "baseline_commit",
        "approval",
        "consumer_policy",
        "final_compaction",
        "planned_creations",
        "rows",
    }
)
_TASK10_ROW_FIELDS = frozenset(
    {
        "row_id",
        "source_path",
        "target_path",
        "artifact_id",
        "action",
        "owner_task",
        "source_kind",
        "source_owner_task",
        "active_consumers",
        "recovery_commit",
        "status",
    }
)
_TOMBSTONE_FIELDS = frozenset(
    {"profile_id", "status", "artifact_id", "artifact_type", "parent_ids", "created", "updated"}
)
APPROVED_BASELINE_RECOVERY_PATHS = frozenset(
    pathlib.PurePosixPath(path)
    for path in (
        "docs/98.archive/changes/chg-0069-agentic-engineering-implementation-audit-pack/plan.md",
        "docs/98.archive/changes/chg-0069-agentic-engineering-implementation-audit-pack/task.md",
        "docs/98.archive/changes/chg-0070-agentic-research-pack-refresh/plan.md",
        "docs/98.archive/changes/chg-0070-agentic-research-pack-refresh/task.md",
        "docs/98.archive/changes/chg-0088-agentic-research-pack-consolidation/plan.md",
        "docs/98.archive/changes/chg-0088-agentic-research-pack-consolidation/task.md",
        "docs/98.archive/changes/chg-0089-agentic-engineering-audit-remediation/plan.md",
        "docs/98.archive/changes/chg-0089-agentic-engineering-audit-remediation/task.md",
        "docs/98.archive/changes/chg-0095-document-contract-canonicalization/plan.md",
        "docs/98.archive/changes/chg-0095-document-contract-canonicalization/task.md",
        "docs/98.archive/changes/chg-0098-agent-governance-harness-convergence/plan.md",
        "docs/98.archive/changes/chg-0098-agent-governance-harness-convergence/task.md",
        "docs/98.archive/changes/chg-0099-target-surface-contract-convergence/plan.md",
        "docs/98.archive/changes/chg-0099-target-surface-contract-convergence/task.md",
    )
)


@dataclasses.dataclass(frozen=True, order=True)
class ArchiveFinding:
    code: str
    path: str
    detail: str = ""


@dataclasses.dataclass(frozen=True, order=True)
class RecoveryReference:
    commit: str
    original_path: pathlib.PurePosixPath


@dataclasses.dataclass(frozen=True, order=True)
class PreservationDecision:
    disposition: str
    stable_path: pathlib.PurePosixPath
    replacement: pathlib.PurePosixPath | None
    reason: str
    recovery: RecoveryReference
    reviewer_decision: str


@dataclasses.dataclass(frozen=True, order=True)
class TombstoneRecord:
    path: pathlib.PurePosixPath
    retired_path: pathlib.PurePosixPath
    replacement: pathlib.PurePosixPath | None
    reason: str
    recovery: RecoveryReference
    is_minimal: bool


@dataclasses.dataclass(frozen=True)
class ArchiveInventory:
    root_entries: tuple[str, ...]
    migrations: tuple[pathlib.PurePosixPath, ...]
    tombstones: tuple[TombstoneRecord, ...]


def _safe_path(value: object) -> pathlib.PurePosixPath | None:
    if not isinstance(value, str) or not value or value.startswith("-"):
        return None
    path = pathlib.PurePosixPath(value)
    if path.is_absolute() or not path.parts:
        return None
    if any(
        part in {"", ".", ".."}
        or part.startswith("-")
        or "\\" in part
        or any(ord(character) < 32 or ord(character) == 127 for character in part)
        for part in path.parts
    ):
        return None
    return path


def _directory_flags() -> int:
    return (
        os.O_RDONLY
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_DIRECTORY", 0)
        | getattr(os, "O_NOFOLLOW", 0)
    )


def _snapshot(metadata: os.stat_result) -> tuple[int, int, int, int, int, int]:
    return (
        metadata.st_dev,
        metadata.st_ino,
        metadata.st_mode,
        metadata.st_size,
        metadata.st_mtime_ns,
        metadata.st_ctime_ns,
    )


def _open_directory_at(parent: int, name: str, label: str) -> tuple[int, tuple[int, ...]]:
    descriptor: int | None = None
    try:
        before = os.stat(name, dir_fd=parent, follow_symlinks=False)
        if stat.S_ISLNK(before.st_mode) or not stat.S_ISDIR(before.st_mode):
            raise ValueError(f"{label} must be a non-symlink directory")
        descriptor = os.open(name, _directory_flags(), dir_fd=parent)
        opened = os.fstat(descriptor)
    except OSError as error:
        if descriptor is not None:
            os.close(descriptor)
        raise ValueError(f"cannot open {label}: {error}") from error
    assert descriptor is not None
    if _snapshot(opened) != _snapshot(before):
        os.close(descriptor)
        raise ValueError(f"{label} changed while opening")
    return descriptor, _snapshot(opened)


def _open_directory_path(path: pathlib.Path, label: str) -> tuple[int, int, str, tuple[int, ...]]:
    absolute = pathlib.Path(os.path.abspath(path))
    if not absolute.is_absolute() or len(absolute.parts) < 2:
        raise ValueError(f"{label} must be an absolute contained path")
    parent = os.open(os.path.sep, _directory_flags())
    try:
        for part in absolute.parts[1:-1]:
            if part in {"", ".", ".."}:
                raise ValueError(f"{label} contains an unsafe component")
            child, _ = _open_directory_at(parent, part, f"{label} parent")
            os.close(parent)
            parent = child
        name = absolute.parts[-1]
        descriptor, snapshot = _open_directory_at(parent, name, label)
        return parent, descriptor, name, snapshot
    except BaseException:
        os.close(parent)
        raise


def _verify_directory(
    parent: int,
    name: str,
    descriptor: int,
    snapshot: tuple[int, ...],
    label: str,
) -> None:
    try:
        linked = os.stat(name, dir_fd=parent, follow_symlinks=False)
        opened = os.fstat(descriptor)
    except OSError as error:
        raise ValueError(f"{label} changed while loading: {error}") from error
    if stat.S_ISLNK(linked.st_mode) or _snapshot(linked) != snapshot or _snapshot(opened) != snapshot:
        raise ValueError(f"{label} changed while loading")


def _bounded_entries(
    descriptor: int,
    *,
    label: str,
    limit: int,
) -> tuple[tuple[str, os.stat_result], ...]:
    entries: list[tuple[str, os.stat_result]] = []
    try:
        with os.scandir(descriptor) as iterator:
            for entry in iterator:
                if len(entries) >= limit:
                    raise ValueError(f"{label} entry limit exceeded")
                entries.append((entry.name, entry.stat(follow_symlinks=False)))
    except OSError as error:
        raise ValueError(f"cannot enumerate {label}: {error}") from error
    return tuple(sorted(entries, key=lambda item: item[0]))


def _read_regular_at(
    parent: int,
    name: str,
    label: str,
    *,
    expected: os.stat_result | None = None,
) -> bytes:
    try:
        before = expected or os.stat(name, dir_fd=parent, follow_symlinks=False)
    except OSError as error:
        raise ValueError(f"cannot stat {label}: {error}") from error
    if stat.S_ISLNK(before.st_mode) or not stat.S_ISREG(before.st_mode):
        raise ValueError(f"document is not a bounded regular file: {label}")
    if before.st_size > MAX_DOCUMENT_BYTES:
        raise ValueError(f"document exceeds the byte limit: {label}")
    try:
        descriptor = os.open(
            name,
            os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0) | os.O_NONBLOCK,
            dir_fd=parent,
        )
    except OSError as error:
        raise ValueError(f"cannot open {label}: {error}") from error
    try:
        opened = os.fstat(descriptor)
        if _snapshot(opened) != _snapshot(before):
            raise ValueError(f"document changed while opening: {label}")
        chunks: list[bytes] = []
        remaining = before.st_size
        while remaining:
            chunk = os.read(descriptor, min(65_536, remaining))
            if not chunk:
                raise ValueError(f"document ended before its snapshotted size: {label}")
            chunks.append(chunk)
            remaining -= len(chunk)
        if os.read(descriptor, 1):
            raise ValueError(f"document grew during its bounded read: {label}")
        after = os.fstat(descriptor)
        linked = os.stat(name, dir_fd=parent, follow_symlinks=False)
        if _snapshot(after) != _snapshot(before) or _snapshot(linked) != _snapshot(before):
            raise ValueError(f"document changed during its bounded read: {label}")
        return b"".join(chunks)
    finally:
        os.close(descriptor)


def _read_regular(path: pathlib.Path) -> bytes:
    parent, descriptor, name, snapshot = _open_directory_path(path.parent, f"{path} parent")
    try:
        entries = dict(_bounded_entries(descriptor, label=f"{path} parent", limit=MAX_ARCHIVE_ENTRIES))
        if path.name not in entries:
            raise ValueError(f"document is missing: {path}")
        raw = _read_regular_at(descriptor, path.name, str(path), expected=entries[path.name])
        _verify_directory(parent, name, descriptor, snapshot, f"{path} parent")
        return raw
    finally:
        os.close(descriptor)
        os.close(parent)


def _decode_document(path: pathlib.Path) -> str:
    try:
        return _read_regular(path).decode("utf-8")
    except UnicodeDecodeError as error:
        raise ValueError(f"document is not UTF-8: {path}") from error


def _frontmatter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---\n"):
        raise ValueError("frontmatter is required")
    marker = text.find("\n---\n", 4)
    if marker < 0:
        raise ValueError("frontmatter is unterminated")
    try:
        loaded = _load_archive_yaml(text[4:marker])
    except (yaml.YAMLError, ValueError) as error:
        raise ValueError("frontmatter YAML is invalid or has duplicate keys") from error
    if not isinstance(loaded, dict) or any(not isinstance(key, str) for key in loaded):
        raise ValueError("frontmatter must be a string-key mapping")
    return loaded, text[marker + 5 :]


def _load_archive_yaml(source: str) -> object:
    """Load strict Archive YAML without aliases or merge-key indirection."""

    root = yaml.compose(source, Loader=yaml.SafeLoader)
    seen: set[int] = set()

    def visit(node: yaml.nodes.Node | None) -> None:
        if node is None:
            return
        identity = id(node)
        if identity in seen:
            raise ValueError("Archive YAML aliases are not supported")
        seen.add(identity)
        if isinstance(node, yaml.nodes.MappingNode):
            for key, value in node.value:
                if key.tag == "tag:yaml.org,2002:merge":
                    raise ValueError("Archive YAML merge keys are not supported")
                visit(key)
                visit(value)
        elif isinstance(node, yaml.nodes.SequenceNode):
            for value in node.value:
                visit(value)

    visit(root)
    return safe_load_unique(source)


def _migration_path(root: pathlib.Path) -> pathlib.Path:
    return root / "docs/98.archive/migrations/0003-workspace-governance-simplification.md"


def validate_compacted_migration(document: object) -> None:
    """Validate the durable schema independently of pending execution evidence."""

    if not isinstance(document, dict) or set(document) != {
        "schema_version", "migration_id", "rows"
    }:
        raise ValueError("compacted Migration top-level fields are invalid")
    if type(document["schema_version"]) is not int or document["schema_version"] != 3:
        raise ValueError("compacted Migration schema must be version 3")
    if document["migration_id"] != "mig-0003":
        raise ValueError("compacted Migration identity is invalid")
    rows = document["rows"]
    if not isinstance(rows, list) or not rows or len(rows) > 2048:
        raise ValueError("compacted Migration rows must be nonempty")
    fields = {"source_path", "target_path", "artifact_id", "action", "recovery_commit"}
    sources: set[str] = set()
    for row in rows:
        if not isinstance(row, dict) or set(row) != fields:
            raise ValueError("compacted Migration row fields are invalid")
        source = _safe_path(row["source_path"])
        target = row["target_path"]
        if source is None or (target is not None and _safe_path(target) is None):
            raise ValueError("compacted Migration path is invalid")
        if source.as_posix() in sources:
            raise ValueError("compacted Migration source is duplicated")
        sources.add(source.as_posix())
        artifact = row["artifact_id"]
        if artifact is not None and (not isinstance(artifact, str) or not artifact):
            raise ValueError("compacted Migration artifact identity is invalid")
        action = row["action"]
        if action not in {"rename", "merge", "delete"}:
            raise ValueError("compacted Migration action is invalid")
        if (action == "delete") != (target is None):
            raise ValueError("compacted Migration action and target disagree")
        if not recovery_commit_is_valid(row["recovery_commit"]):
            raise ValueError("compacted Migration recovery commit is required")


def _parse_migration_document(raw: bytes) -> dict[str, Any]:
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ValueError("Migration 0003 is not UTF-8") from error
    blocks = re.findall(r"^```yaml\n(.*?)^```[ \t]*$", text, re.MULTILINE | re.DOTALL)
    if len(blocks) != 1 or text.count("```yaml\n") != 1:
        raise ValueError("Migration 0003 requires exactly one closed fenced ledger")
    payload = blocks[0]
    try:
        document = _load_archive_yaml(payload)
    except (yaml.YAMLError, ValueError) as error:
        raise ValueError("Migration 0003 YAML is invalid or has duplicate keys") from error
    if not isinstance(document, dict) or document.get("migration_id") != "mig-0003":
        raise ValueError("Migration 0003 execution ledger is invalid")
    rows = document.get("rows")
    if not isinstance(rows, list) or not rows or len(rows) > 2048:
        raise ValueError("Migration 0003 rows are invalid")
    return document


def _approved_migration_document(root: pathlib.Path) -> dict[str, Any]:
    """Read the reviewed execution selection, never current policy, from Git."""

    raw = HistoricalDocument(
        root, APPROVED_MIGRATION_COMMIT,
        "docs/98.archive/migrations/0003-workspace-governance-simplification.md",
    ).read_bytes()
    if hashlib.sha256(raw).hexdigest() != FROZEN_MIGRATION_SHA256:
        raise ValueError("Migration 0003 approved frozen digest is invalid")
    return _parse_migration_document(raw)


def _mapping_selection(document: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {key: row[key] for key in ("source_path", "target_path", "artifact_id", "action")}
        for row in document["rows"]
    ]


def _compact_mapping_selection(document: Mapping[str, Any]) -> list[dict[str, Any]]:
    """Project reviewed routes, omitting three superseded unexecuted plans."""

    from scripts.lib.document_governance.spec_packages import _SINGULAR_TASK_FINALS

    selected = _mapping_selection(document)
    row_ids = {f"mig-0003-r{number:04d}" for number in (233, 239, 242, 245, 248)}
    for original, row in zip(document["rows"], selected, strict=True):
        if original["row_id"] in row_ids:
            row["target_path"] = _SINGULAR_TASK_FINALS[row["target_path"]]
    omitted = {"mig-0003-r0842", "mig-0003-r0848", "mig-0003-r0852"}
    return [row for original, row in zip(document["rows"], selected, strict=True)
            if original["row_id"] not in omitted]


def _execution_selection(document: dict[str, Any]) -> dict[str, Any]:
    selection = copy.deepcopy(document)
    for row in selection["rows"]:
        if not isinstance(row, dict) or set(row) != _TASK10_ROW_FIELDS:
            raise ValueError("Migration 0003 execution row fields are invalid")
        del row["status"]
        del row["recovery_commit"]
    return selection


def _migration_document(root: pathlib.Path) -> dict[str, Any]:
    """Read a native execution or compact state with the frozen selection proof."""

    document = _parse_migration_document(_read_regular(_migration_path(root)))
    approved = _approved_migration_document(root)
    recoveries: list[tuple[str, str]] = []
    if document.get("schema_version") == 3:
        validate_compacted_migration(document)
        additions = [
            {"source_path": path, "target_path": None, "artifact_id": None, "action": "delete"}
            for path in ONE_TIME_VERIFIER_PATHS
        ]
        additions.extend(
            {"source_path": path, "target_path": None, "artifact_id": identity, "action": "delete"}
            for path, identity in HISTORICAL_SESSION_SPECS.items()
        )
        if _mapping_selection(document) != [*_compact_mapping_selection(approved), *additions]:
            raise ValueError("Migration 0003 compact selection differs from approved frozen digest")
        if any(row["recovery_commit"] != APPROVED_MIGRATION_COMMIT for row in document["rows"][-len(additions):]):
            raise ValueError("terminal addition recovery must use its approved existing commit")
        recoveries = [(row["source_path"], row["recovery_commit"]) for row in document["rows"]]
    else:
        if (
            type(document.get("schema_version")) is not int
            or document["schema_version"] != 2
            or set(document) != _MIGRATION_FIELDS
            or _execution_selection(document) != _execution_selection(approved)
        ):
            raise ValueError("Migration 0003 execution selection differs from approved frozen digest")
        for row in document["rows"]:
            if row["status"] == "planned" and row["recovery_commit"] is None:
                continue
            if row["status"] != "completed" or not recovery_commit_is_valid(row["recovery_commit"]):
                raise ValueError("Migration 0003 completed row requires recovery")
            recoveries.append((row["source_path"], row["recovery_commit"]))
    for offset in range(0, len(recoveries), 512):
        proofs = verify_recovery_blobs_batch(recoveries[offset:offset + 512], repo_root=root)
        if not all(proof.is_regular_blob for proof in proofs):
            raise ValueError("Migration 0003 recovery must resolve to an existing regular Git blob")
    return document


def migration_rows_for_task(root: pathlib.Path, task: int) -> tuple[dict[str, Any], ...]:
    """Select native rows using the reviewed historical ownership, not invented fields."""

    document = _migration_document(root)
    approved = _approved_migration_document(root)
    sources = {row["source_path"] for row in approved["rows"] if row["owner_task"] == task}
    return tuple(row for row in document["rows"] if row["source_path"] in sources)


def task10_rows(root: pathlib.Path) -> tuple[dict[str, Any], ...]:
    rows = migration_rows_for_task(root, 10)
    if rows and "row_id" not in rows[0]:
        # Native compact fields were checked against the approved mapping and
        # every recovery blob by the shared loader; no execution fields invented.
        if len(rows) != 275:
            raise ValueError("Task 10 compact selection is incomplete")
        return rows
    expected_row_ids = tuple(
        f"mig-0003-r{number:04d}"
        for number in range(566, 841)
    )
    if (
        len(rows) != 275
        or tuple(row.get("row_id") for row in rows) != expected_row_ids
        or rows[0].get("row_id") != TASK10_FIRST_ROW
        or rows[-1].get("row_id") != TASK10_LAST_ROW
    ):
        raise ValueError("Task 10 Migration row range is not the approved 275-row selection")
    for row in rows:
        source = _safe_path(row.get("source_path"))
        target_value = row.get("target_path")
        target = None if target_value is None else _safe_path(target_value)
        action = row.get("action")
        consumers = row.get("active_consumers")
        if (
            source is None
            or not source.as_posix().startswith("docs/98.archive/")
            or action not in {"rename", "delete"}
            or (action == "rename" and target is None)
            or (action == "delete" and target_value is not None)
            or (target is not None and not target.as_posix().startswith("docs/98.archive/"))
            or row.get("owner_task") != 10
            or row.get("source_kind") not in {"tracked", "planned-output"}
            or (
                row.get("source_kind") == "tracked"
                and row.get("source_owner_task") is not None
            )
            or (
                row.get("source_kind") == "planned-output"
                and row.get("source_owner_task") != 1
            )
            or not isinstance(consumers, list)
            or any(_safe_path(consumer) is None for consumer in consumers)
            or row.get("artifact_id") is not None
            and (not isinstance(row.get("artifact_id"), str) or not row.get("artifact_id"))
            or row.get("status") not in {"planned", "completed"}
        ):
            raise ValueError("Task 10 Migration row semantics are invalid")
    return rows


def _legacy_change_recoveries(
    root: pathlib.Path,
    sources: Iterable[pathlib.PurePosixPath],
) -> dict[pathlib.PurePosixPath, RecoveryReference]:
    selected = tuple(sources)
    metadata = {
        item.source: RecoveryReference(item.archived_commit, item.archived_from)
        for item in read_archived_metadata_batch(
            selected,
            TASK10_BASELINE_COMMIT,
            repo_root=root,
        )
    }
    missing = set(selected) - set(metadata)
    if missing != APPROVED_BASELINE_RECOVERY_PATHS:
        unexpected = ", ".join(path.as_posix() for path in sorted(missing))
        raise ValueError(f"unapproved missing legacy recovery metadata: {unexpected}")
    return {
        source: metadata.get(source, RecoveryReference(TASK10_BASELINE_COMMIT, source))
        for source in selected
    }


def _section(body: str, heading: str) -> str:
    match = re.search(
        rf"(?ms)^## {re.escape(heading)}\s*$\n(.*?)(?=^## |\Z)",
        body,
    )
    if match is None:
        raise ValueError(f"missing tombstone section: {heading}")
    return match.group(1).strip()


def _code_value(value: str) -> str:
    match = re.fullmatch(r"`([^`]+)`", value.strip())
    if match is None:
        raise ValueError("tombstone value must be one code span")
    return match.group(1)


def _parse_tombstone_text(
    text: str,
    relative: pathlib.PurePosixPath,
    filename: str,
) -> TombstoneRecord:
    metadata, body = _frontmatter(text)
    retired = _safe_path(_code_value(_section(body, "Retired Path")))
    replacement_text = _section(body, "Replacement")
    replacement = None if replacement_text == "none" else _safe_path(_code_value(replacement_text))
    reason = _section(body, "Reason")
    commit = _code_value(_section(body, "Recovery Commit"))
    traceability = _section(body, "Traceability")
    headings = tuple(re.findall(r"(?m)^## ([^\n]+)$", body))
    number_match = _TOMBSTONE_NAME.fullmatch(filename)
    number = number_match.group("number") if number_match else ""
    minimal = bool(
        set(metadata) == _TOMBSTONE_FIELDS
        and metadata.get("profile_id") == "tombstone"
        and metadata.get("status") == "completed"
        and metadata.get("artifact_id") == f"tombstone-{number}"
        and metadata.get("artifact_type") == "tombstone"
        and isinstance(metadata.get("parent_ids"), list)
        and headings == ("Retired Path", "Replacement", "Reason", "Recovery Commit", "Traceability")
        and retired is not None
        and (replacement_text == "none" or replacement is not None)
        and bool(reason)
        and recovery_commit_is_valid(commit)
        and (
            "../../README.md" in traceability
            or "../../migrations/" in traceability
            or "98.archive/README.md" in traceability
            or "98.archive/migrations/" in traceability
        )
        and not re.search(r"(?i)archived_blob|snapshot(?:_path|_count)|line[-_ ]sha", text)
    )
    if retired is None or not recovery_commit_is_valid(commit):
        raise ValueError(f"invalid tombstone recovery identity: {relative}")
    if not minimal:
        raise ValueError(f"tombstone does not satisfy the minimal contract: {relative}")
    return TombstoneRecord(
        relative,
        retired,
        replacement,
        reason,
        RecoveryReference(commit, retired),
        minimal,
    )


def _parse_tombstone(path: pathlib.Path, archive_root: pathlib.Path) -> TombstoneRecord:
    relative = pathlib.PurePosixPath(path.relative_to(archive_root.parent.parent).as_posix())
    return _parse_tombstone_text(_decode_document(path), relative, path.name)


def load_archive(archive_root: pathlib.Path) -> ArchiveInventory:
    parent, root_fd, root_name, root_snapshot = _open_directory_path(archive_root, "Stage 98")
    migrations_fd: int | None = None
    tombstones_fd: int | None = None
    try:
        root_rows = _bounded_entries(root_fd, label="Stage 98", limit=MAX_ROOT_ENTRIES)
        entries = tuple(name for name, _ in root_rows)
        if entries != ("README.md", "migrations", "tombstones"):
            raise ValueError("Stage 98 root must contain only README.md, migrations/, and tombstones/")
        root_metadata = dict(root_rows)
        if not stat.S_ISREG(root_metadata["README.md"].st_mode):
            raise ValueError("Stage 98 README.md must be a regular file")
        migrations_fd, migrations_snapshot = _open_directory_at(
            root_fd, "migrations", "Stage 98 migrations"
        )
        migration_rows = _bounded_entries(
            migrations_fd,
            label="Stage 98 migrations",
            limit=MAX_MIGRATION_ENTRIES,
        )
        migrations: list[pathlib.PurePosixPath] = []
        total_entries = len(root_rows) + len(migration_rows)
        total_bytes = 0
        for filename, metadata in migration_rows:
            if (
                stat.S_ISLNK(metadata.st_mode)
                or not stat.S_ISREG(metadata.st_mode)
                or _MIGRATION_NAME.fullmatch(filename) is None
            ):
                raise ValueError("Stage 98 migrations must be prefixless numbered Markdown files")
            raw = _read_regular_at(
                migrations_fd,
                filename,
                f"Stage 98 migrations/{filename}",
                expected=metadata,
            )
            total_bytes += len(raw)
            migrations.append(pathlib.PurePosixPath(f"docs/98.archive/migrations/{filename}"))
        _verify_directory(
            root_fd, "migrations", migrations_fd, migrations_snapshot, "Stage 98 migrations"
        )

        tombstones_fd, tombstones_snapshot = _open_directory_at(
            root_fd, "tombstones", "Stage 98 tombstones"
        )
        stage_rows = _bounded_entries(
            tombstones_fd,
            label="Stage 98 tombstones",
            limit=MAX_TOMBSTONE_PARTITIONS,
        )
        total_entries += len(stage_rows)
        tombstones: list[TombstoneRecord] = []
        for stage_name, stage_metadata in stage_rows:
            if (
                stat.S_ISLNK(stage_metadata.st_mode)
                or not stat.S_ISDIR(stage_metadata.st_mode)
                or _STAGE.fullmatch(stage_name) is None
            ):
                raise ValueError(f"invalid Stage 98 tombstone partition: {stage_name}")
            stage_fd, stage_snapshot = _open_directory_at(
                tombstones_fd,
                stage_name,
                f"Stage 98 tombstones/{stage_name}",
            )
            try:
                file_rows = _bounded_entries(
                    stage_fd,
                    label=f"Stage 98 tombstones/{stage_name}",
                    limit=MAX_TOMBSTONES_PER_PARTITION,
                )
                total_entries += len(file_rows)
                if total_entries > MAX_ARCHIVE_ENTRIES:
                    raise ValueError("Stage 98 aggregate entry limit exceeded")
                for filename, metadata in file_rows:
                    if (
                        stat.S_ISLNK(metadata.st_mode)
                        or not stat.S_ISREG(metadata.st_mode)
                        or _TOMBSTONE_NAME.fullmatch(filename) is None
                    ):
                        raise ValueError(
                            f"invalid Stage 98 tombstone path: {stage_name}/{filename}"
                        )
                    raw = _read_regular_at(
                        stage_fd,
                        filename,
                        f"Stage 98 tombstones/{stage_name}/{filename}",
                        expected=metadata,
                    )
                    total_bytes += len(raw)
                    if total_bytes > MAX_ARCHIVE_BYTES:
                        raise ValueError("Stage 98 aggregate byte limit exceeded")
                    try:
                        text = raw.decode("utf-8")
                    except UnicodeDecodeError as error:
                        raise ValueError("Stage 98 tombstone must be UTF-8") from error
                    relative = pathlib.PurePosixPath(
                        f"docs/98.archive/tombstones/{stage_name}/{filename}"
                    )
                    tombstones.append(_parse_tombstone_text(text, relative, filename))
                _verify_directory(
                    tombstones_fd,
                    stage_name,
                    stage_fd,
                    stage_snapshot,
                    f"Stage 98 tombstones/{stage_name}",
                )
            finally:
                os.close(stage_fd)
        _verify_directory(
            root_fd, "tombstones", tombstones_fd, tombstones_snapshot, "Stage 98 tombstones"
        )
        _verify_directory(parent, root_name, root_fd, root_snapshot, "Stage 98")
        return ArchiveInventory(entries, tuple(migrations), tuple(tombstones))
    finally:
        if migrations_fd is not None:
            os.close(migrations_fd)
        if tombstones_fd is not None:
            os.close(tombstones_fd)
        os.close(root_fd)
        os.close(parent)


def load_task10_recovery_references(root: pathlib.Path) -> tuple[RecoveryReference, ...]:
    change_rows = [
        row for row in task10_rows(root)
        if row.get("action") == "delete" and str(row.get("source_path", "")).startswith("docs/98.archive/changes/")
    ]
    sources = tuple(pathlib.PurePosixPath(str(row["source_path"])) for row in change_rows)
    recoveries = _legacy_change_recoveries(root, sources)
    references = [recoveries[source] for source in sources]
    archive = load_archive(root / "docs/98.archive")
    references.extend(item.recovery for item in archive.tombstones)
    if len(references) != 272:
        raise ValueError("Task 10 must expose exactly 272 artifact recovery tuples")
    return tuple(references)


def load_task10_preservation_decisions(root: pathlib.Path) -> tuple[PreservationDecision, ...]:
    change_rows = [
        row for row in task10_rows(root)
        if row.get("action") == "delete" and str(row.get("source_path", "")).startswith("docs/98.archive/changes/")
    ]
    sources = tuple(pathlib.PurePosixPath(str(row["source_path"])) for row in change_rows)
    recoveries = _legacy_change_recoveries(root, sources)
    grouped: dict[pathlib.PurePosixPath, list[RecoveryReference]] = collections.defaultdict(list)
    for source in sources:
        grouped[source.parent].append(recoveries[source])
    decisions = [
        PreservationDecision(
            "git-only",
            packet,
            None,
            "Completed change evidence is recovered from Git; no active body copy is retained.",
            sorted(recoveries)[0],
            "approved",
        )
        for packet, recoveries in sorted(grouped.items())
    ]
    for tombstone in load_archive(root / "docs/98.archive").tombstones:
        decisions.append(
            PreservationDecision(
                "minimal-tombstone",
                tombstone.path,
                tombstone.replacement,
                tombstone.reason,
                tombstone.recovery,
                "approved",
            )
        )
    return tuple(decisions)


def parse_recovery_row(row: Mapping[str, object]) -> RecoveryReference:
    if set(row) != _RECOVERY_FIELDS or row.get("status") != "completed":
        raise ValueError("recovery row must use the exact completed recovery shape")
    commit = row.get("recovery_commit")
    original = _safe_path(row.get("original_path"))
    if not recovery_commit_is_valid(commit) or original is None:
        raise ValueError("recovery row identity is invalid")
    return RecoveryReference(commit, original)


def validate_recovery_rows(
    rows: Iterable[RecoveryReference],
    root: pathlib.Path,
) -> tuple[ArchiveFinding, ...]:
    findings: list[ArchiveFinding] = []
    selected = tuple(rows)
    if len(selected) > 512:
        return (ArchiveFinding("recovery-row-count-exceeded", "docs/98.archive"),)
    valid: list[RecoveryReference] = []
    for row in selected:
        if not recovery_commit_is_valid(row.commit):
            findings.append(ArchiveFinding("recovery-commit-invalid", row.original_path.as_posix()))
            continue
        if _safe_path(row.original_path.as_posix()) is None:
            findings.append(ArchiveFinding("recovery-path-invalid", row.original_path.as_posix()))
            continue
        valid.append(row)
    try:
        proofs = verify_recovery_blobs_batch(
            ((row.original_path, row.commit) for row in valid),
            repo_root=root,
        )
    except ValueError as error:
        findings.append(
            ArchiveFinding("recovery-validator-internal-error", "docs/98.archive", str(error))
        )
        return tuple(sorted(set(findings)))
    for row, proof in zip(valid, proofs, strict=True):
        if proof.is_regular_blob:
            continue
        if not proof.exists:
            findings.append(ArchiveFinding("recovery-object-missing", row.original_path.as_posix()))
        else:
            findings.append(
                ArchiveFinding("recovery-object-not-regular-blob", row.original_path.as_posix())
            )
    return tuple(sorted(set(findings)))


def sha256_file(path: pathlib.Path) -> str:
    return hashlib.sha256(_read_regular(path)).hexdigest()
