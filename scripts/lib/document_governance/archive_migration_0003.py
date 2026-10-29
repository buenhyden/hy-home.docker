"""Migration 0003 cutover proof, kept apart from general Stage 98 integrity.

Migration 0003 is a completed, preserved cutover. Its frozen digest, approved
commit, and the Task 10 row selection prove that the preserved record still
matches what was approved. These readers stay because the documentation
protocol keeps proof readers for preserved bytes, but they live here so the
general archive module holds no value that belongs to one past migration.
"""

from __future__ import annotations

import collections
import copy
import hashlib
import pathlib
import re
from collections.abc import Iterable, Mapping
from typing import Any

import yaml

from scripts.lib.document_governance import archive
from scripts.lib.document_governance.git_provenance import (
    HistoricalDocument,
    read_archived_metadata_batch,
    recovery_commit_is_valid,
    verify_recovery_blobs_batch,
)

FROZEN_MIGRATION_SHA256 = (
    "271f21c50cf4ab765422ee552de244a4340c160e53149231eb6be45f03476ab9"
)
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


def _migration_path(root: pathlib.Path) -> pathlib.Path:
    return (
        root / "docs/98.archive/migrations/0003-workspace-governance-simplification.md"
    )


def validate_compacted_migration(document: object) -> None:
    """Validate the durable schema independently of pending execution evidence."""

    if not isinstance(document, dict) or set(document) != {
        "schema_version",
        "migration_id",
        "rows",
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
        source = archive._safe_path(row["source_path"])
        target = row["target_path"]
        if source is None or (
            target is not None and archive._safe_path(target) is None
        ):
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
        document = archive._load_archive_yaml(payload)
    except (yaml.YAMLError, ValueError) as error:
        raise ValueError(
            "Migration 0003 YAML is invalid or has duplicate keys"
        ) from error
    if not isinstance(document, dict) or document.get("migration_id") != "mig-0003":
        raise ValueError("Migration 0003 execution ledger is invalid")
    rows = document.get("rows")
    if not isinstance(rows, list) or not rows or len(rows) > 2048:
        raise ValueError("Migration 0003 rows are invalid")
    return document


def _approved_migration_document(root: pathlib.Path) -> dict[str, Any]:
    """Read the reviewed execution selection, never current policy, from Git."""

    raw = HistoricalDocument(
        root,
        APPROVED_MIGRATION_COMMIT,
        "docs/98.archive/migrations/0003-workspace-governance-simplification.md",
    ).read_bytes()
    if hashlib.sha256(raw).hexdigest() != FROZEN_MIGRATION_SHA256:
        raise ValueError("Migration 0003 approved frozen digest is invalid")
    return _parse_migration_document(raw)


def _mapping_selection(document: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            key: row[key]
            for key in ("source_path", "target_path", "artifact_id", "action")
        }
        for row in document["rows"]
    ]


def _compact_mapping_selection(document: Mapping[str, Any]) -> list[dict[str, Any]]:
    """Project reviewed routes, omitting three superseded unexecuted plans."""

    selected = _mapping_selection(document)
    task_targets = {
        "docs/03.specs/0123-agentic-engineering-audit-remediation/task.md": "docs/03.specs/0123-agentic-engineering-audit-remediation/tasks/"
        "tsk-0001-research-pack-extension.md",
        "docs/03.specs/0134-agent-governance-canonical-convergence/task.md": "docs/03.specs/0134-agent-governance-canonical-convergence/tasks/"
        "tsk-0001-canonical-convergence.md",
        "docs/03.specs/0135-target-surface-delta-convergence/task.md": "docs/03.specs/0135-target-surface-delta-convergence/tasks/"
        "tsk-0001-delta-convergence.md",
        "docs/03.specs/0136-sdlc-taxonomy-convergence/task.md": "docs/03.specs/0136-sdlc-taxonomy-convergence/tasks/"
        "tsk-0001-taxonomy-convergence.md",
        "docs/03.specs/0152-deleted-reference-leaf-disposition/task.md": "docs/03.specs/0152-deleted-reference-leaf-disposition/tasks/"
        "tsk-0001-reference-disposition.md",
    }
    row_ids = {f"mig-0003-r{number:04d}" for number in (233, 239, 242, 245, 248)}
    for original, row in zip(document["rows"], selected, strict=True):
        if original["row_id"] in row_ids:
            row["target_path"] = task_targets[row["target_path"]]
    # Approved 2026-09-10. Emptying the Stage 90 data category moved the
    # `DATA-0067` payload under `docs/98.archive/retired/`. The bytes are
    # unchanged, so the recovery comparison still proves the same equality; only
    # the path the frozen row names moved, and the owner approved that rewrite.
    retired_targets = {
        "docs/90.references/data/0067-foundation/data.yaml": (
            "docs/98.archive/retired/90.references/data/0067-foundation/data.yaml"
        ),
    }
    for row in selected:
        moved = retired_targets.get(row.get("target_path"))
        if moved is not None:
            row["target_path"] = moved

    omitted = {"mig-0003-r0842", "mig-0003-r0848", "mig-0003-r0852"}
    return [
        row
        for original, row in zip(document["rows"], selected, strict=True)
        if original["row_id"] not in omitted
    ]


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

    document = _parse_migration_document(archive._read_regular(_migration_path(root)))
    approved = _approved_migration_document(root)
    recoveries: list[tuple[str, str]] = []
    if document.get("schema_version") == 3:
        validate_compacted_migration(document)
        additions = [
            {
                "source_path": path,
                "target_path": None,
                "artifact_id": None,
                "action": "delete",
            }
            for path in ONE_TIME_VERIFIER_PATHS
        ]
        additions.extend(
            {
                "source_path": path,
                "target_path": None,
                "artifact_id": identity,
                "action": "delete",
            }
            for path, identity in HISTORICAL_SESSION_SPECS.items()
        )
        if _mapping_selection(document) != [
            *_compact_mapping_selection(approved),
            *additions,
        ]:
            raise ValueError(
                "Migration 0003 compact selection differs from approved frozen digest"
            )
        if any(
            row["recovery_commit"] != APPROVED_MIGRATION_COMMIT
            for row in document["rows"][-len(additions) :]
        ):
            raise ValueError(
                "terminal addition recovery must use its approved existing commit"
            )
        recoveries = [
            (row["source_path"], row["recovery_commit"]) for row in document["rows"]
        ]
    else:
        if (
            type(document.get("schema_version")) is not int
            or document["schema_version"] != 2
            or set(document) != archive._MIGRATION_FIELDS
            or _execution_selection(document) != _execution_selection(approved)
        ):
            raise ValueError(
                "Migration 0003 execution selection differs from approved frozen digest"
            )
        for row in document["rows"]:
            if row["status"] == "planned" and row["recovery_commit"] is None:
                continue
            if row["status"] != "completed" or not recovery_commit_is_valid(
                row["recovery_commit"]
            ):
                raise ValueError("Migration 0003 completed row requires recovery")
            recoveries.append((row["source_path"], row["recovery_commit"]))
    for offset in range(0, len(recoveries), 512):
        proofs = verify_recovery_blobs_batch(
            recoveries[offset : offset + 512], repo_root=root
        )
        if not all(proof.is_regular_blob for proof in proofs):
            raise ValueError(
                "Migration 0003 recovery must resolve to an existing regular Git blob"
            )
    return document


def migration_rows_for_task(
    root: pathlib.Path, task: int
) -> tuple[dict[str, Any], ...]:
    """Select native rows using the reviewed historical ownership, not invented fields."""

    document = _migration_document(root)
    approved = _approved_migration_document(root)
    sources = {
        row["source_path"] for row in approved["rows"] if row["owner_task"] == task
    }
    return tuple(row for row in document["rows"] if row["source_path"] in sources)


def task10_rows(root: pathlib.Path) -> tuple[dict[str, Any], ...]:
    rows = migration_rows_for_task(root, 10)
    if rows and "row_id" not in rows[0]:
        # Native compact fields were checked against the approved mapping and
        # every recovery blob by the shared loader; no execution fields invented.
        if len(rows) != 275:
            raise ValueError("Task 10 compact selection is incomplete")
        return rows
    expected_row_ids = tuple(f"mig-0003-r{number:04d}" for number in range(566, 841))
    if (
        len(rows) != 275
        or tuple(row.get("row_id") for row in rows) != expected_row_ids
        or rows[0].get("row_id") != TASK10_FIRST_ROW
        or rows[-1].get("row_id") != TASK10_LAST_ROW
    ):
        raise ValueError(
            "Task 10 Migration row range is not the approved 275-row selection"
        )
    for row in rows:
        source = archive._safe_path(row.get("source_path"))
        target_value = row.get("target_path")
        target = None if target_value is None else archive._safe_path(target_value)
        action = row.get("action")
        consumers = row.get("active_consumers")
        if (
            source is None
            or not source.as_posix().startswith("docs/98.archive/")
            or action not in {"rename", "delete"}
            or (action == "rename" and target is None)
            or (action == "delete" and target_value is not None)
            or (
                target is not None
                and not target.as_posix().startswith("docs/98.archive/")
            )
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
            or any(archive._safe_path(consumer) is None for consumer in consumers)
            or (
                row.get("artifact_id") is not None
                and (
                    not isinstance(row.get("artifact_id"), str)
                    or not row.get("artifact_id")
                )
            )
            or row.get("status") not in {"planned", "completed"}
        ):
            raise ValueError("Task 10 Migration row semantics are invalid")
    return rows


def _legacy_change_recoveries(
    root: pathlib.Path,
    sources: Iterable[pathlib.PurePosixPath],
) -> dict[pathlib.PurePosixPath, archive.RecoveryReference]:
    selected = tuple(sources)
    metadata = {
        item.source: archive.RecoveryReference(item.archived_commit, item.archived_from)
        for item in read_archived_metadata_batch(
            selected,
            TASK10_BASELINE_COMMIT,
            repo_root=root,
        )
    }
    missing = set(selected) - set(metadata)
    if missing != archive.APPROVED_BASELINE_RECOVERY_PATHS:
        unexpected = ", ".join(path.as_posix() for path in sorted(missing))
        raise ValueError(f"unapproved missing legacy recovery metadata: {unexpected}")
    return {
        source: metadata.get(
            source, archive.RecoveryReference(TASK10_BASELINE_COMMIT, source)
        )
        for source in selected
    }


def load_task10_recovery_references(
    root: pathlib.Path,
) -> tuple[archive.RecoveryReference, ...]:
    change_rows = [
        row
        for row in task10_rows(root)
        if row.get("action") == "delete"
        and str(row.get("source_path", "")).startswith("docs/98.archive/changes/")
    ]
    sources = tuple(
        pathlib.PurePosixPath(str(row["source_path"])) for row in change_rows
    )
    recoveries = _legacy_change_recoveries(root, sources)
    references = [recoveries[source] for source in sources]
    inventory = archive.load_archive(root / "docs/98.archive")
    references.extend(
        item.recovery for item in inventory.tombstones if item.recovery is not None
    )
    return tuple(references)


def load_task10_preservation_decisions(
    root: pathlib.Path,
) -> tuple[archive.PreservationDecision, ...]:
    change_rows = [
        row
        for row in task10_rows(root)
        if row.get("action") == "delete"
        and str(row.get("source_path", "")).startswith("docs/98.archive/changes/")
    ]
    sources = tuple(
        pathlib.PurePosixPath(str(row["source_path"])) for row in change_rows
    )
    recoveries = _legacy_change_recoveries(root, sources)
    grouped: dict[pathlib.PurePosixPath, list[archive.RecoveryReference]] = (
        collections.defaultdict(list)
    )
    for source in sources:
        grouped[source.parent].append(recoveries[source])
    decisions = [
        archive.PreservationDecision(
            "git-only",
            packet,
            None,
            "Completed change evidence is recovered from Git; no active body copy is retained.",
            sorted(recoveries)[0],
            "approved",
        )
        for packet, recoveries in sorted(grouped.items())
    ]
    for tombstone in archive.load_archive(root / "docs/98.archive").tombstones:
        if tombstone.recovery is None:
            # A route-shape Tombstone records a route, not a preservation decision.
            continue
        decisions.append(
            archive.PreservationDecision(
                "minimal-tombstone",
                tombstone.path,
                tombstone.replacement,
                tombstone.reason,
                tombstone.recovery,
                "approved",
            )
        )
    return tuple(decisions)
