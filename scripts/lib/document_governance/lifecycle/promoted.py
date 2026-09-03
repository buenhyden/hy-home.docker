"""Promoted lifecycle manifest semantics and historical reconciliation."""

from __future__ import annotations

import collections.abc
import hashlib
import os
import pathlib
import re

from scripts.lib.document_governance import archive as archive_authority
from scripts.lib.document_governance.git_provenance import HistoricalDocument
from scripts.lib.document_governance.lifecycle.contract import (
    DESTRUCTIVE_DISPOSITIONS,
    OBJECT_ID,
    REVIEW_VALUES,
    SOURCE_EQUALS_TARGET,
    TARGET_DISTINCT,
    TYPED_SURFACE_CLASSES,
    Finding,
    MigrationManifestDocument,
    ProfileError,
    Record,
    ReviewVerdict,
    _baseline_merge_owner_findings,
    _baseline_regular_blob,
    _blob_at_commit_path,
    _canonical_current_snapshot,
    _canonical_replacement_findings,
    _finding,
    _generate_manifest_skeleton,
    _held_result_snapshot,
    _load_migration_manifest_text,
    _load_repo_migration_manifest,
    _manifest_artifact_id,
    _manifest_mapping,
    _partition_plan_findings,
    _profile_required_fields,
    _read_regular_repo_bytes,
    _repo_manifest_matches,
    _resolve_canonical_replacement,
    _reviewed_evidence_findings,
    _run_git,
    _safe_path,
    _safe_path_text,
    _sensitive_value_is_present,
    _surface_partition_plan_findings,
    _surface_replacement_findings,
    _surface_result_state_findings,
    _surface_rollback_valid,
    _tracked_active_consumers,
    _verified_commit,
    _wave_mapping,
    metadata,
    render_migration_manifest,
    validate_archive_provenance,
)

TASK5_MIGRATION_LEDGER = pathlib.PurePosixPath(
    "docs/98.archive/migrations/0001-sdlc-taxonomy-convergence.md"
)
# Retained deliberately against SPEC-0158 Task 7 Step 6, which asks to remove
# persistent digest and count ledgers. These maps describe frozen Migration
# evidence, not a living corpus, so they never drift with legitimate change.
# Until 2026-09-02 they were also the only integrity control on Migrations 0001
# and 0002; `test_archive` now digest-pins all three, which makes these a second
# layer rather than the sole one. They are kept because an action-count
# mismatch names which action class changed, while a digest only says the file
# differs.
TASK5_LEDGER_ACTION_COUNTS = {
    "archive": 28,
    "delete": 38,
    "merge": 8,
    "move": 262,
    "rewrite": 1,
}
TASK5_STAGE_PREFIXES = (
    "docs/03.specs/",
    "docs/04.execution/",
    "docs/98.archive/03.specs/",
)
TASK5_OPERATIONS_EXCEPTION = (
    "docs/05.operations/policies/00-workspace/"  # retired-route-record
    "infra-service-optimization-catalog.md"
)
TASK5_RELATIVE_LINK = re.compile(r"(?<!!)\[[^\]\n]+\]\(([^)\n]+)\)")
TASK7_LEDGER_ACTION_COUNTS = {
    "archive": 38,
    "delete": 16,
    "move": 75,
    "rewrite": 40,
}
TASK7_ALL_LEDGER_ACTION_COUNTS = {
    "archive": 38,
    "delete": 38,
    "merge": 63,
    "move": 613,
    "rewrite": 47,
}
TASK7_EXTENSION_IDENTITIES = (
    (
        "archive/Windows-Network-IP.md",
        "docs/98.archive/tombstones/05.operations/ref-0095-windows-network-ip.md",
        "ref-0095",
        "archive",
        "32c40e11747bc0bd03789c24861d2e5d60c0e999",
    ),
    (
        "docs/90.references/research/0001-agentic-research-pack-refresh/github-actions-platform.md",
        "docs/90.references/research/0084-github-actions-platform/README.md",
        "ref-0084",
        "move",
        "f2f8f8a441b5977d55e516ba59ea7865c06d6c55",
    ),
    (
        "docs/90.references/research/0001-agentic-research-pack-refresh/verification-validation.md",
        "docs/90.references/research/ref-0085-verification-validation.md",
        "ref-0085",
        "move",
        "9c927a0e187a4214358453f4826dc758a72611b5",
    ),
)
TASK7_LEDGER_FIELDS = {
    "legacy_path",
    "stable_path",
    "artifact_id",
    "action",
    "replacement",
    "source_commit",
    "reason",
}
TASK7_DATE_COMPONENT = re.compile(r"^\d{4}-\d{2}-\d{2}(?:-|$)")
TASK7_YEAR_COMPONENT = re.compile(r"^\d{4}$")
TASK7_IMMUTABLE_MANIFEST = (
    "docs/90.references/data/0069-target-surface-convergence/data.yaml"
)
TASK7_IMMUTABLE_MANIFEST_SHA256 = (
    "4c061d2a4d9bb494db97318280d451f9cdcc7748bfcbbe021fb1436fe6398a67"
)


def _task5_migration_rows(root: pathlib.Path) -> dict[str, dict[str, object]]:
    """Load only the frozen ledger fields needed for promoted reconciliation."""

    payload = _read_regular_repo_bytes(
        root,
        TASK5_MIGRATION_LEDGER.as_posix(),
        require_tracked=True,
    )
    if payload is None:
        return {}
    try:
        text = payload.decode("utf-8")
        fenced = text.split("## Archive Ledger", 1)[1].split("```yaml", 1)[1].split(
            "```", 1
        )[0]
        document = metadata._safe_load_unique(fenced)
    except (
        IndexError,
        UnicodeDecodeError,
        metadata.FrontmatterError,
        metadata.ProfileError,
    ):
        return {}
    if not isinstance(document, dict) or document.get("migration_id") != "mig-0001":
        return {}
    records = document.get("records")
    if not isinstance(records, list):
        return {}
    rows: dict[str, dict[str, object]] = {}
    for row in records:
        if not isinstance(row, dict):
            return {}
        legacy = row.get("legacy_path")
        if not isinstance(legacy, str) or not _safe_path(legacy) or legacy in rows:
            return {}
        rows[legacy] = row
    return rows


def _task5_selected_rows(
    rows: dict[str, dict[str, object]],
) -> dict[str, dict[str, object]]:
    """Select the frozen Stage 03/04 wave plus its one approved Ops exception."""

    return {
        legacy: row
        for legacy, row in rows.items()
        if legacy.startswith(TASK5_STAGE_PREFIXES)
        or legacy == TASK5_OPERATIONS_EXCEPTION
    }


def _task7_ledger_groups(
    root: pathlib.Path,
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    """Load the immutable baseline and exact Task 7 post-baseline extension."""

    payload = _read_regular_repo_bytes(
        root,
        TASK5_MIGRATION_LEDGER.as_posix(),
        require_tracked=True,
    )
    if payload is None:
        return [], []
    try:
        text = payload.decode("utf-8")
        fenced = text.split("## Archive Ledger", 1)[1].split("```yaml", 1)[1].split(
            "```", 1
        )[0]
        document = metadata._safe_load_unique(fenced)
    except (
        IndexError,
        UnicodeDecodeError,
        metadata.FrontmatterError,
        metadata.ProfileError,
    ):
        return [], []
    if not isinstance(document, dict) or document.get("migration_id") != "mig-0001":
        return [], []
    baseline = document.get("records")
    extension = document.get("post_baseline_records")
    if not isinstance(baseline, list) or not isinstance(extension, list):
        return [], []
    if len(baseline) != 796 or len(extension) != 3:
        return [], []
    values = [*baseline, *extension]
    if any(not isinstance(row, dict) or set(row) != TASK7_LEDGER_FIELDS for row in values):
        return [], []
    typed_rows = [row for row in values if isinstance(row, dict)]
    legacy_paths = [row.get("legacy_path") for row in typed_rows]
    if (
        any(not isinstance(path, str) or not _safe_path(path) for path in legacy_paths)
        or len(legacy_paths) != len(set(legacy_paths))
    ):
        return [], []
    actual_extension = tuple(
        (
            row.get("legacy_path"),
            row.get("stable_path"),
            row.get("artifact_id"),
            row.get("action"),
            row.get("source_commit"),
        )
        for row in extension
        if isinstance(row, dict)
    )
    if actual_extension != TASK7_EXTENSION_IDENTITIES:
        return [], []
    return (
        [row for row in baseline if isinstance(row, dict)],
        [row for row in extension if isinstance(row, dict)],
    )


def _task7_all_migration_rows(root: pathlib.Path) -> dict[str, dict[str, object]]:
    baseline, extension = _task7_ledger_groups(root)
    return {
        str(row["legacy_path"]): row
        for row in [*baseline, *extension]
    }


def _task7_migration_rows(root: pathlib.Path) -> dict[str, dict[str, object]]:
    """Select the exact Stage 90, Stage 98, and root archive Task 7 rows."""

    return {
        legacy: row
        for legacy, row in _task7_all_migration_rows(root).items()
        if legacy.startswith(("docs/90.references/", "docs/98.archive/"))
        or legacy == "archive/Windows-Network-IP.md"
    }


def _task7_dispositions_executed(
    root: pathlib.Path,
    rows: dict[str, dict[str, object]],
) -> bool:
    """Prove path-changing rewrites and all other ledger actions from Git blobs."""

    by_commit: dict[str, list[str]] = collections.defaultdict(list)
    for legacy, row in rows.items():
        action = row.get("action")
        stable = row.get("stable_path")
        replacement = row.get("replacement")
        source_commit = row.get("source_commit")
        if (
            not _safe_path(legacy)
            or action not in TASK7_ALL_LEDGER_ACTION_COUNTS
            or not isinstance(source_commit, str)
            or OBJECT_ID.fullmatch(source_commit) is None
        ):
            return False
        by_commit[source_commit].append(legacy)
        destination = replacement if action == "delete" else stable
        if action == "merge":
            destination = replacement or stable
        if not isinstance(destination, str) or not _safe_path(destination):
            return False
        if action == "rewrite" and destination == legacy:
            if not (root / legacy).is_file():
                return False
            continue
        if (root / legacy).exists() or not (root / destination).is_file():
            return False
    for source_commit, paths in by_commit.items():
        result = _run_git(
            root,
            ["ls-tree", "-r", "-z", source_commit, "--", *sorted(paths)],
            text=False,
        )
        if result.returncode != 0:
            return False
        regular: set[str] = set()
        for entry in (item for item in result.stdout.split(b"\0") if item):
            if b"\t" not in entry:
                return False
            header, raw_path = entry.split(b"\t", 1)
            fields = header.split()
            try:
                path = raw_path.decode("utf-8")
            except UnicodeDecodeError:
                return False
            if len(fields) == 3 and fields[0] in {b"100644", b"100755"} and fields[1] == b"blob":
                regular.add(path)
        if regular != set(paths):
            return False
    return True


def _task7_current_links_resolve(root: pathlib.Path) -> bool:
    """Resolve current Markdown links while treating Stage 98 as history."""

    result = _run_git(root, ["ls-files", "-z", "--", "*.md"], text=False)
    if result.returncode != 0:
        return False
    try:
        paths = tuple(item.decode("utf-8") for item in result.stdout.split(b"\0") if item)
    except UnicodeDecodeError:
        return False
    resolved_root = root.resolve()
    for path in paths:
        if not _safe_path(path) or path.startswith("docs/98.archive/"):
            continue
        payload = _read_regular_repo_bytes(root, path, require_tracked=True)
        if payload is None:
            return False
        try:
            lines = payload.decode("utf-8").splitlines()
        except UnicodeDecodeError:
            return False
        in_fence = False
        document = root / path
        for line in lines:
            stripped = line.lstrip()
            if stripped.startswith(("```", "~~~")):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            for match in TASK5_RELATIVE_LINK.finditer(line):
                raw = match.group(1).strip()
                href = (
                    raw[1 : raw.index(">")]
                    if raw.startswith("<") and ">" in raw
                    else raw.split()[0]
                )
                if (
                    not href
                    or href.startswith("#")
                    or href.endswith("...")
                    or re.match(r"^[a-z][a-z0-9+.-]*:", href, flags=re.I)
                ):
                    continue
                relative = href.split("#", 1)[0]
                target = (
                    resolved_root / relative.lstrip("/")
                    if relative.startswith("/")
                    else document.parent / relative
                ).resolve()
                try:
                    target.relative_to(resolved_root)
                except ValueError:
                    return False
                if not target.exists():
                    return False
    return True


def _task7_reconciliation_ready(
    root: pathlib.Path,
    contract: dict[str, object],
) -> bool:
    """Require the exact completed migration through Task 7."""

    waves = contract.get("waves")
    wave = waves.get("sdlc-taxonomy-convergence") if isinstance(waves, dict) else None
    all_rows = _task7_all_migration_rows(root)
    selected = _task7_migration_rows(root)
    selected_targets = [
        row.get("stable_path") for row in selected.values() if row.get("stable_path") is not None
    ]
    selected_ids = [
        row.get("artifact_id") for row in selected.values() if row.get("artifact_id") is not None
    ]
    tracked = _run_git(
        root,
        ["ls-files", "-z", "--", "docs/90.references", "docs/98.archive", "archive"],
        text=False,
    )
    try:
        tracked_paths = tuple(
            item.decode("utf-8") for item in tracked.stdout.split(b"\0") if item
        )
    except UnicodeDecodeError:
        return False
    dated = any(
        any(
            TASK7_YEAR_COMPONENT.fullmatch(component)
            or TASK7_DATE_COMPONENT.match(component)
            for component in pathlib.PurePosixPath(path).parts
        )
        for path in tracked_paths
        if path.startswith(("docs/90.references/", "docs/98.archive/"))
    )
    return (
        isinstance(wave, dict)
        and wave.get("scope_state") == "approved"
        and len(all_rows) == 799
        and dict(collections.Counter(row.get("action") for row in all_rows.values()))
        == TASK7_ALL_LEDGER_ACTION_COUNTS
        and len(selected) == 169
        and dict(collections.Counter(row.get("action") for row in selected.values()))
        == TASK7_LEDGER_ACTION_COUNTS
        and len(selected_targets) == len(set(selected_targets))
        and len(selected_ids) == len(set(selected_ids))
        and _task7_dispositions_executed(root, all_rows)
        and not dated
        and not any(path.startswith("archive/") for path in tracked_paths)
        and not (root / "archive").exists()
        and _task7_current_links_resolve(root)
    )


def _task7_consumer_evidence_is_reconciled(
    root: pathlib.Path,
    document: MigrationManifestDocument,
    source: str,
    rows: dict[str, dict[str, object]],
) -> bool:
    """Admit only real tracked consumer drift after the exact ledger executes."""

    row = next(
        (item for item in document.entries if item.source_path.as_posix() == source),
        None,
    )
    if row is None or len(rows) != 169:
        return False
    try:
        current = _tracked_active_consumers(root, source)
    except ProfileError:
        return False
    difference = set(row.active_consumers) ^ set(current)
    allowed = {
        pathlib.PurePosixPath(path)
        for legacy, ledger_row in rows.items()
        for path in (legacy, ledger_row.get("stable_path"))
        if isinstance(path, str) and _safe_path(path)
    }
    return bool(difference) and difference <= allowed


def _task7_target_missing_is_reconciled(
    root: pathlib.Path,
    source: str,
    rows: dict[str, dict[str, object]],
) -> bool:
    """Prove an exact Task 7 retired target through its ledger destination."""

    row = rows.get(source)
    if row is None:
        return False
    action = row.get("action")
    destination = row.get("replacement") if action == "delete" else row.get("stable_path")
    return (
        action in TASK7_LEDGER_ACTION_COUNTS
        and not (root / source).exists()
        and isinstance(destination, str)
        and _safe_path(destination)
        and (root / destination).is_file()
    )


def _task7_registered_manifest_matches(
    root: pathlib.Path,
    contract: dict[str, object],
    document: MigrationManifestDocument,
    candidate_manifest_path: str | None,
) -> bool:
    """Bind reconciliation to the registered path and immutable ref-0069 bytes."""

    waves = contract.get("waves")
    registered_wave = waves.get(document.wave) if isinstance(waves, dict) else None
    registered_manifest = (
        registered_wave.get("manifest_path")
        if isinstance(registered_wave, dict)
        else None
    )
    if (
        document.wave != "target-surface-convergence"
        or registered_manifest != TASK7_IMMUTABLE_MANIFEST
        or candidate_manifest_path != TASK7_IMMUTABLE_MANIFEST
    ):
        return False
    baseline, extension = _task7_ledger_groups(root)
    if len(baseline) != 796 or len(extension) != 3:
        return False
    payload = _read_regular_repo_bytes(
        root,
        TASK7_IMMUTABLE_MANIFEST,
        require_tracked=True,
    )
    return (
        payload is not None
        and hashlib.sha256(payload).hexdigest() == TASK7_IMMUTABLE_MANIFEST_SHA256
        and _repo_manifest_matches(
            root,
            TASK7_IMMUTABLE_MANIFEST,
            render_migration_manifest(document),
        )
    )


def _task7_immutable_expected_document(
    root: pathlib.Path,
    contract: dict[str, object],
    wave: str,
) -> MigrationManifestDocument | None:
    """Load hash-pinned baseline selection after its legacy roots are removed."""

    if wave != "target-surface-convergence":
        return None
    waves = contract.get("waves")
    registered = waves.get(wave) if isinstance(waves, dict) else None
    if (
        not isinstance(registered, dict)
        or registered.get("manifest_path") != TASK7_IMMUTABLE_MANIFEST
    ):
        return None
    baseline, extension = _task7_ledger_groups(root)
    all_rows = {
        str(row["legacy_path"]): row
        for row in [*baseline, *extension]
    }
    owner = next(
        (
            row
            for row in all_rows.values()
            if row.get("stable_path") == TASK7_IMMUTABLE_MANIFEST
        ),
        None,
    )
    payload = _read_regular_repo_bytes(
        root,
        TASK7_IMMUTABLE_MANIFEST,
        require_tracked=True,
    )
    if (
        len(baseline) != 796
        or len(extension) != 3
        or not isinstance(owner, dict)
        or payload is None
        or hashlib.sha256(payload).hexdigest() != TASK7_IMMUTABLE_MANIFEST_SHA256
    ):
        return None
    source_commit = owner.get("source_commit")
    legacy_path = owner.get("legacy_path")
    if (
        not isinstance(source_commit, str)
        or not isinstance(legacy_path, str)
        or _verified_commit(root, source_commit) != source_commit
        or not _baseline_regular_blob(root, source_commit, legacy_path)
    ):
        return None
    try:
        document = _load_repo_migration_manifest(root, TASK7_IMMUTABLE_MANIFEST)
    except ProfileError:
        return None
    return document if document.wave == wave else None


def _task5_dispositions_executed(
    root: pathlib.Path,
    rows: dict[str, dict[str, object]],
) -> bool:
    """Prove each selected ledger row against the current repository topology."""

    for legacy, row in rows.items():
        action = row.get("action")
        stable = row.get("stable_path")
        replacement = row.get("replacement")
        source_commit = row.get("source_commit")
        if (
            not _safe_path(legacy)
            or action not in TASK5_LEDGER_ACTION_COUNTS
            or not isinstance(source_commit, str)
            or OBJECT_ID.fullmatch(source_commit) is None
        ):
            return False
        try:
            source_is_commit = _verified_commit(root, source_commit) == source_commit
            source_has_legacy_blob = _baseline_regular_blob(root, source_commit, legacy)
        except ProfileError:
            return False
        if not source_is_commit or not source_has_legacy_blob:
            return False
        destination = replacement if action == "delete" else stable
        if action == "merge":
            destination = replacement or stable
        if not isinstance(destination, str) or not _safe_path(destination):
            return False
        if action == "rewrite":
            if destination != legacy or not (root / legacy).is_file():
                return False
            continue
        if (root / legacy).exists() or not (root / destination).is_file():
            return False
    return True


def _task5_current_links_resolve(root: pathlib.Path) -> bool:
    """Resolve tracked current-surface and Task 5 change-packet Markdown links."""

    result = _run_git(root, ["ls-files", "-z", "--", "*.md"], text=False)
    if result.returncode != 0:
        return False
    try:
        paths = tuple(
            item.decode("utf-8") for item in result.stdout.split(b"\0") if item
        )
    except UnicodeDecodeError:
        return False
    resolved_root = root.resolve()
    for path in paths:
        if not _safe_path(path):
            return False
        if path.startswith("docs/98.archive/") and not path.startswith(
            "docs/98.archive/changes/"
        ):
            continue
        payload = _read_regular_repo_bytes(root, path, require_tracked=True)
        if payload is None:
            return False
        try:
            lines = payload.decode("utf-8").splitlines()
        except UnicodeDecodeError:
            return False
        in_fence = False
        document = root / path
        for line in lines:
            stripped = line.lstrip()
            if stripped.startswith(("```", "~~~")):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            for match in TASK5_RELATIVE_LINK.finditer(line):
                raw = match.group(1).strip()
                href = (
                    raw[1 : raw.index(">")]
                    if raw.startswith("<") and ">" in raw
                    else raw.split()[0]
                )
                if (
                    not href
                    or href.startswith("#")
                    or href.endswith("...")
                    or re.match(r"^[a-z][a-z0-9+.-]*:", href, flags=re.I)
                ):
                    continue
                relative = href.split("#", 1)[0]
                target = (
                    resolved_root / relative.lstrip("/")
                    if relative.startswith("/")
                    else document.parent / relative
                ).resolve()
                try:
                    target.relative_to(resolved_root)
                except ValueError:
                    return False
                if not target.exists():
                    return False
    return True


def _task5_reconciliation_ready(
    root: pathlib.Path,
    contract: dict[str, object],
) -> bool:
    """Require the completed Task 5 topology before reconciling old manifests."""

    waves = contract.get("waves")
    wave = waves.get("sdlc-taxonomy-convergence") if isinstance(waves, dict) else None
    stage03 = root / "docs/03.specs"
    rows = _task5_selected_rows(_task5_migration_rows(root))
    actions = collections.Counter(row.get("action") for row in rows.values())
    return (
        isinstance(wave, dict)
        and wave.get("scope_state") == "approved"
        and not (root / "docs/04.execution").exists()
        and stage03.is_dir()
        and all(
            not child.is_dir() or child.name.startswith("spec-")
            for child in stage03.iterdir()
        )
        and len(rows) == 337
        and dict(actions) == TASK5_LEDGER_ACTION_COUNTS
        and _task5_dispositions_executed(root, rows)
        and _task5_current_links_resolve(root)
    )


def _task5_target_missing_is_reconciled(
    root: pathlib.Path,
    path: str,
    rows: dict[str, dict[str, object]],
) -> bool:
    """Prove one retired Stage 03/04 target through the frozen Task 5 ledger."""

    if not path.startswith(("docs/03.specs/", "docs/04.execution/")):
        return False
    row = rows.get(path)
    if row is not None:
        action = row.get("action")
        destination = row.get("stable_path") or row.get("replacement")
        return (
            action in {"move", "merge", "delete", "archive"}
            and not (root / path).exists()
            and isinstance(destination, str)
            and _safe_path(destination)
            and (root / destination).is_file()
        )
    match = re.fullmatch(r"docs/03\.specs/(\d{3})-([^/]+)/spec\.md", path)
    if match is None:
        return False
    stable = f"docs/03.specs/spec-0{match.group(1)}-{match.group(2)}/spec.md"
    stable_id = f"spec-0{match.group(1)}"
    proving_rows = [
        row
        for row in rows.values()
        if row.get("action") == "move"
        and row.get("stable_path") == stable
        and row.get("artifact_id") == stable_id
    ]
    return (
        len(proving_rows) == 1
        and not (root / path).exists()
        and (root / stable).is_file()
    )


def _reconcile_task5_promoted_findings(
    root: pathlib.Path,
    contract: dict[str, object],
    document: MigrationManifestDocument,
    findings: collections.abc.Iterable[Finding],
    *,
    manifest_path: str | None = None,
) -> list[Finding]:
    """Keep historical manifests immutable while honoring the executed Task 5 wave."""

    values = list(findings)
    waves = contract.get("waves")
    task7_candidate_is_registered = _task7_registered_manifest_matches(
        root, contract, document, manifest_path
    )
    task5_ready = _task5_reconciliation_ready(root, contract)
    task7_ready = (
        task7_candidate_is_registered
        and _task7_reconciliation_ready(root, contract)
    )
    if not task5_ready and not task7_ready:
        return sorted(set(values))
    task5_rows = _task5_migration_rows(root)
    task7_rows = _task7_migration_rows(root)
    foundation = waves.get("foundation") if isinstance(waves, dict) else None
    source_paths = foundation.get("source_paths") if isinstance(foundation, dict) else []
    foundation_sources = {
        path for path in source_paths if isinstance(path, str) and _safe_path(path)
    }
    reconciled: list[Finding] = []
    for finding in values:
        if (
            task5_ready
            and document.wave == "foundation"
            and finding.code == "manifest-consumer-evidence-mismatch"
            and finding.path in foundation_sources
        ):
            # Foundation active_consumers is point-in-time evidence. Task 5 owns
            # the current consumer graph through mig-0001 and the zero-link gate.
            continue
        if (
            task7_ready
            and document.wave in {"foundation", "target-surface-convergence"}
            and finding.code == "manifest-consumer-evidence-mismatch"
            and _task7_consumer_evidence_is_reconciled(
                root, document, finding.path, task7_rows
            )
        ):
            # The manifests retain point-in-time consumer paths. The exact
            # completed ledger and current-link proof own present topology.
            continue
        if (
            task7_ready
            and document.wave == "target-surface-convergence"
            and finding.code == "manifest-target-missing"
            and _task7_target_missing_is_reconciled(
                root, finding.path, task7_rows
            )
        ):
            continue
        if (
            task7_ready
            and document.wave == "target-surface-convergence"
            and finding.path == "archive/Windows-Network-IP.md"
            and finding.code == "manifest-transition-invalid"
            and _task7_target_missing_is_reconciled(
                root, finding.path, task7_rows
            )
        ):
            continue
        if (
            task7_ready
            and document.wave == "target-surface-convergence"
            and finding.path == "manifest"
            and finding.code == "manifest-baseline-commit-invalid"
        ):
            # The immutable baseline cannot be regenerated after the exact
            # migration removes its selected legacy roots. mig-0001 and the
            # current topology checks provide the post-execution proof.
            continue
        if (
            document.wave in {"foundation", "target-surface-convergence"}
            and finding.code == "manifest-target-missing"
            and _task5_target_missing_is_reconciled(
                root, finding.path, task5_rows
            )
        ):
            continue
        reconciled.append(finding)
    return sorted(set(reconciled))



def _validate_surface_manifest_semantics(
    root: pathlib.Path,
    profiles: dict[str, object],
    contract: dict[str, object],
    document: MigrationManifestDocument,
) -> list[Finding]:
    """Apply v1-compatible semantic and safety gates to a schema-v2 wave."""

    findings: list[Finding] = []
    common = profiles.get("common")
    transitions = common.get("transitions") if isinstance(common, dict) else {}
    for row in document.entries:
        source = row.source_path.as_posix()
        result_findings, result_valid = _surface_result_state_findings(
            root, profiles, contract, document, row
        )
        findings.extend(result_findings)
        transition_valid = row.status_before == row.status_after
        if (
            not transition_valid
            and isinstance(row.status_before, str)
            and isinstance(row.status_after, str)
            and isinstance(transitions, dict)
        ):
            next_statuses = transitions.get(row.status_before)
            transition_valid = (
                isinstance(next_statuses, list) and row.status_after in next_statuses
            )
        if row.disposition == "archive":
            transition_valid = (
                result_valid
                and row.review_verdict == ReviewVerdict("pass", "pass")
            )
        if (
            not transition_valid
            and row.surface_class == "content-archive"
            and row.status_after == "archived"
        ):
            transition_valid = (
                document.enforcement == "advisory"
                and row.disposition == "preserve"
                and row.review_verdict == ReviewVerdict("pending", "pending")
            ) or (
                result_valid
                and row.review_verdict == ReviewVerdict("pass", "pass")
            )
        if not transition_valid:
            findings.append(
                _finding(
                    source,
                    "manifest-transition-invalid",
                    "status transition is not canonical",
                )
            )
        findings.extend(
            _surface_replacement_findings(root, profiles, document, row)
        )
        rollback_invalid = (
            row.disposition in DESTRUCTIVE_DISPOSITIONS
            and not row.evidence.rollback
        ) or (
            bool(row.evidence.rollback)
            and not _surface_rollback_valid(root, row.evidence.rollback)
        )
        if rollback_invalid:
            findings.append(
                _finding(
                    source,
                    "manifest-rollback-invalid",
                    "rollback must pin immutable commits newest-to-oldest",
                )
            )
        findings.extend(_surface_partition_plan_findings(root, profiles, row))
        for consumer in row.active_consumers:
            if not _safe_path(consumer.as_posix()):
                findings.append(
                    _finding(
                        source,
                        "manifest-consumer-path-invalid",
                        "consumer path is not repository-safe",
                    )
                )
        for repository_path in row.evidence.repository_paths:
            if not _safe_path(repository_path.as_posix()):
                findings.append(
                    _finding(
                        source,
                        "manifest-evidence-path-invalid",
                        "evidence path is not repository-safe",
                    )
                )
        evidence_values = (
            *row.evidence.commands,
            *row.evidence.sources,
            *(path.as_posix() for path in row.evidence.repository_paths),
            *row.evidence.consumer_scan,
            *row.evidence.rollback,
        )
        if any(_sensitive_value_is_present(value) for value in evidence_values):
            findings.append(
                _finding(
                    source,
                    "manifest-evidence-confidential",
                    "manifest evidence contains prohibited confidential data",
                )
            )
        if row.disposition in DESTRUCTIVE_DISPOSITIONS:
            if row.preservation_class is None:
                findings.append(
                    _finding(
                        source,
                        "manifest-preservation-required",
                        "destructive row requires preservation",
                    )
                )
            evidence_lists = (
                row.evidence.commands,
                row.evidence.sources,
                row.evidence.repository_paths,
                row.evidence.consumer_scan,
                row.evidence.rollback,
            )
            if any(not values for values in evidence_lists):
                findings.append(
                    _finding(
                        source,
                        "manifest-destructive-evidence-required",
                        "destructive row requires complete bounded evidence",
                    )
                )
            if row.review_verdict != ReviewVerdict("pass", "pass"):
                findings.append(
                    _finding(
                        source,
                        "manifest-destructive-review-required",
                        "destructive row requires independent passing reviews",
                    )
                )
    return sorted(set(findings))


def _validate_surface_manifest(
    root: pathlib.Path,
    profiles: dict[str, object],
    contract: dict[str, object],
    document: MigrationManifestDocument,
) -> list[Finding]:
    """Validate v2 coverage and baseline truth without decoding native blobs."""

    findings: list[Finding] = []
    try:
        metadata.validate_static_migration_manifest(
            _manifest_mapping(document), contract, profiles
        )
    except ProfileError:
        findings.append(
            _finding(
                "manifest",
                "manifest-static-invalid",
                "manifest violates the canonical static contract",
            )
        )
    try:
        wave = _wave_mapping(contract, document.wave)
    except ProfileError:
        return [_finding("manifest", "manifest-wave-invalid", "manifest wave is not declared")]
    if document.schema_version != 2:
        findings.append(_finding("manifest", "manifest-schema-invalid", "schema version must be 2"))
    if document.enforcement not in {"advisory", "blocking"}:
        findings.append(
            _finding("manifest", "manifest-enforcement-invalid", "enforcement is not registered")
        )
    if document.enforcement != wave.get("enforcement"):
        findings.append(
            _finding(
                "manifest",
                "manifest-enforcement-mismatch",
                "manifest enforcement differs from its wave registry",
            )
        )
    if document.baseline_commit != wave.get("baseline_commit"):
        findings.append(
            _finding(
                "manifest",
                "manifest-baseline-commit-invalid",
                "baseline_commit differs from the pinned wave baseline",
            )
        )
        return sorted(set(findings))
    try:
        expected_document = _generate_manifest_skeleton(
            root,
            contract,
            wave=document.wave,
            baseline_ref=document.baseline_commit,
            profiles=profiles,
        )
    except ProfileError:
        expected_document = _task7_immutable_expected_document(
            root, contract, document.wave
        )
        if expected_document is None:
            findings.append(
                _finding(
                    "manifest",
                    "manifest-baseline-commit-invalid",
                    "pinned baseline selection cannot be established",
                )
            )
            return sorted(set(findings))
    expected_by_path = {
        row.source_path.as_posix(): row for row in expected_document.entries
    }
    counts = collections.Counter(row.source_path.as_posix() for row in document.entries)
    for source in sorted(set(expected_by_path) - set(counts)):
        findings.append(_finding(source, "manifest-source-missing", "selected source has no manifest row"))
    for source, count in sorted(counts.items()):
        display = source if _safe_path(source) else "manifest"
        if count > 1:
            findings.append(
                _finding(display, "manifest-source-duplicate", "selected source has multiple rows")
            )
        if source not in expected_by_path:
            findings.append(
                _finding(display, "manifest-source-unexpected", "row is outside selected wave scope")
            )
    for row in document.entries:
        source = row.source_path.as_posix()
        expected = expected_by_path.get(source)
        if expected is None:
            continue
        if row.surface_class != expected.surface_class:
            findings.append(
                _finding(source, "manifest-surface-class-mismatch", "surface class differs from baseline path/mode truth")
            )
        if row.artifact_type_before != expected.artifact_type_before:
            findings.append(
                _finding(source, "manifest-artifact-type-mismatch", "artifact_type_before differs from typed baseline truth")
            )
        target_metadata_owned = (
            row.disposition == "migrate"
            and row.surface_class in TYPED_SURFACE_CLASSES
            and row.surface_class != "content-archive"
        )
        expected_after = None if row.disposition == "delete" else (
            "archive"
            if row.surface_class == "content-archive"
            else row.artifact_type_before
        )
        if not target_metadata_owned and row.artifact_type_after != expected_after:
            findings.append(
                _finding(source, "manifest-artifact-transition-invalid", "artifact type transition is not admitted")
            )
        if row.status_before != expected.status_before:
            findings.append(
                _finding(source, "manifest-baseline-status-mismatch", "status_before differs from baseline truth")
            )
        target_identity_owned = row.surface_class == "content-archive" or (
            row.disposition == "migrate"
            and row.surface_class in TYPED_SURFACE_CLASSES
        )
        if not target_identity_owned and row.artifact_id != expected.artifact_id:
            findings.append(
                _finding(source, "manifest-baseline-artifact-id-mismatch", "artifact identity differs from baseline truth")
            )
    entry_order = [row.source_path.as_posix() for row in document.entries]
    if entry_order != sorted(entry_order):
        findings.append(
            _finding("manifest", "manifest-order-invalid", "entries are not ordered by source_path")
        )
    findings.extend(
        _validate_surface_manifest_semantics(root, profiles, contract, document)
    )
    return sorted(set(findings))


def validate_migration_manifest(
    root: pathlib.Path,
    profiles: dict[str, object],
    contract: dict[str, object],
    document: MigrationManifestDocument,
    *,
    manifest_path: str | None = None,
) -> list[Finding]:
    """Return stable manifest findings without changing human dispositions."""

    if document.schema_version == 2:
        return _reconcile_task5_promoted_findings(
            root,
            contract,
            document,
            _validate_surface_manifest(root, profiles, contract, document),
            manifest_path=manifest_path,
        )

    findings: list[Finding] = []
    path = "manifest"
    try:
        metadata.validate_static_migration_manifest(
            _manifest_mapping(document), contract, profiles
        )
    except ProfileError:
        findings.append(
            _finding(
                path,
                "manifest-static-invalid",
                "manifest violates the canonical static contract",
            )
        )
    try:
        wave = _wave_mapping(contract, document.wave)
    except ProfileError:
        return [_finding(path, "manifest-wave-invalid", "manifest wave is not declared")]
    if document.schema_version != 1:
        findings.append(_finding(path, "manifest-schema-invalid", "schema version must be 1"))
    if not document.generated_by.strip():
        findings.append(
            _finding(path, "manifest-generated-by-invalid", "generated_by must be non-empty")
        )
    entry_order = [row.source_path.as_posix() for row in document.entries]
    if entry_order != sorted(entry_order):
        findings.append(
            _finding(path, "manifest-order-invalid", "entries are not ordered by source_path")
        )
    if document.enforcement not in {"advisory", "blocking"}:
        findings.append(
            _finding(path, "manifest-enforcement-invalid", "enforcement is not registered")
        )
    registry_enforcement = wave.get("enforcement")
    if document.enforcement != registry_enforcement:
        findings.append(
            _finding(
                path,
                "manifest-enforcement-mismatch",
                "manifest enforcement differs from its wave registry",
            )
        )
    baseline = (
        _verified_commit(root, document.baseline_commit)
        if OBJECT_ID.fullmatch(document.baseline_commit)
        else None
    )
    if baseline != document.baseline_commit:
        findings.append(
            _finding(
                path,
                "manifest-baseline-commit-invalid",
                "baseline_commit does not resolve to the exact commit object",
            )
        )
    expected_paths = wave.get("source_paths")
    expected = set(expected_paths) if isinstance(expected_paths, list) else set()
    counts = collections.Counter(row.source_path.as_posix() for row in document.entries)
    for source in sorted(expected - set(counts)):
        findings.append(
            _finding(source, "manifest-source-missing", "selected source has no manifest row")
        )
    for source, count in sorted(counts.items()):
        display_source = source if _safe_path(source) else "manifest"
        if count > 1:
            findings.append(
                _finding(display_source, "manifest-source-duplicate", "selected source has multiple rows")
            )
        if source not in expected:
            findings.append(
                _finding(display_source, "manifest-source-unexpected", "row is outside selected wave scope")
            )

    common = profiles.get("common")
    allowed_statuses = set(common.get("allowed_statuses", [])) if isinstance(common, dict) else set()
    profile_map = profiles.get("profiles")
    registered_types = set(profile_map) if isinstance(profile_map, dict) else set()
    dispositions = set(contract.get("manifest", {}).get("dispositions", []))  # type: ignore[union-attr]
    preservation_classes = set(contract.get("archive", {}).get("preservation_classes", []))  # type: ignore[union-attr]
    needs_canonical_snapshot = any(
        row.disposition == "archive" or row.canonical_replacement is not None
        for row in document.entries
    )
    if needs_canonical_snapshot:
        canonical_records, canonical_payloads = _canonical_current_snapshot(
            root, profiles
        )
        baseline_records = (
            metadata.collect_records_at_ref(root, profiles, baseline)
            if baseline is not None
            else ()
        )
    else:
        canonical_records, canonical_payloads = (), {}
        baseline_records = ()
    result_records, result_payloads = _held_result_snapshot(
        root,
        profiles,
        document,
        canonical_records,
        canonical_payloads,
    )
    result_records_by_path = {
        record.path.as_posix(): record for record in result_records
    }
    result_manifest = metadata.build_manifest(result_records)
    for row_index, row in enumerate(document.entries):
        source = row.source_path.as_posix()
        archive_disposition: str | None = None
        if not _safe_path(source):
            findings.append(
                _finding(
                    f"manifest#entry-{row_index}",
                    "manifest-source-path-invalid",
                    "source path is not repository-safe",
                )
            )
            continue
        if baseline is not None:
            tracked = _run_git(root, ["cat-file", "-e", f"{baseline}:{source}"])
            if tracked.returncode != 0:
                findings.append(
                    _finding(
                        source,
                        "manifest-source-not-at-baseline",
                        "source is not tracked at baseline_commit",
                    )
                )
            elif not _baseline_regular_blob(root, baseline, source):
                findings.append(
                    _finding(
                        source,
                        "manifest-source-mode-invalid",
                        "baseline source is not a regular tracked blob",
                    )
                )
            else:
                shown = _run_git(root, ["show", f"{baseline}:{source}"])
                if shown.returncode == 0:
                    try:
                        baseline_metadata = metadata._parse_frontmatter_text(shown.stdout)
                    except metadata.FrontmatterError:
                        findings.append(
                            _finding(
                                source,
                                "manifest-source-parse-invalid",
                                "baseline source frontmatter cannot be parsed safely",
                            )
                        )
                    else:
                        expected_type = (
                            "generated"
                            if "generated_by" in baseline_metadata
                            else metadata.infer_artifact_type(pathlib.Path(source), profiles)
                        )
                        if row.artifact_type != expected_type:
                            findings.append(
                                _finding(
                                    source,
                                    "manifest-artifact-type-mismatch",
                                    "artifact type differs from the canonical path profile",
                                )
                            )
                        expected_artifact_id = _manifest_artifact_id(
                            expected_type, baseline_metadata.get("artifact_id")
                        )
                        if row.artifact_id != expected_artifact_id:
                            findings.append(
                                _finding(
                                    source,
                                    "manifest-baseline-artifact-id-mismatch",
                                    "artifact identity differs from baseline truth",
                                )
                            )
                        baseline_status = baseline_metadata.get("status")
                        expected_status = (
                            baseline_status if isinstance(baseline_status, str) else None
                        )
                        if row.status_before != expected_status:
                            findings.append(
                                _finding(
                                    source,
                                    "manifest-baseline-status-mismatch",
                                    "status_before differs from baseline truth",
                                )
                            )
        target = _safe_path_text(row.target_path)
        if target is not None and not _safe_path(target):
            findings.append(
                _finding(source, "manifest-target-path-invalid", "target path is not repository-safe")
            )
        if row.artifact_type not in registered_types:
            findings.append(
                _finding(source, "manifest-artifact-type-invalid", "artifact type is not registered")
            )
        common_transitions = common.get("transitions") if isinstance(common, dict) else None
        transition_valid = row.status_before == row.status_after
        if (
            not transition_valid
            and isinstance(row.status_before, str)
            and isinstance(row.status_after, str)
            and isinstance(common_transitions, dict)
        ):
            allowed_next = common_transitions.get(row.status_before)
            transition_valid = (
                isinstance(allowed_next, list) and row.status_after in allowed_next
            )
        archive_result_valid = False
        required = _profile_required_fields(profiles, row.artifact_type)
        if "artifact_id" in required and not metadata._valid_metadata_artifact_id(row.artifact_id):
            findings.append(
                _finding(source, "manifest-artifact-id-invalid", "selected profile requires artifact identity")
            )
        elif row.artifact_id is not None and not metadata._valid_metadata_artifact_id(row.artifact_id):
            findings.append(
                _finding(source, "manifest-artifact-id-invalid", "artifact identity is invalid")
            )
        for label, status in (("before", row.status_before), ("after", row.status_after)):
            if ("status" in required and status is None) or (
                status is not None and status not in allowed_statuses
            ):
                findings.append(
                    _finding(
                        source,
                        "manifest-status-invalid",
                        f"status_{label} does not satisfy the selected profile",
                    )
                )
        if row.disposition not in dispositions:
            findings.append(
                _finding(source, "manifest-disposition-invalid", "disposition is not registered")
            )
            continue
        if row.disposition == "delete" and target is not None:
            findings.append(
                _finding(source, "manifest-delete-target-invalid", "delete requires a null target")
            )
        elif row.disposition in TARGET_DISTINCT:
            if target is None:
                findings.append(
                    _finding(
                        source,
                        f"manifest-{row.disposition}-target-required",
                        "disposition requires a target",
                    )
                )
            elif target == source:
                findings.append(
                    _finding(
                        source,
                        f"manifest-{row.disposition}-target-invalid",
                        "disposition requires a distinct target",
                    )
                )
        elif row.disposition in SOURCE_EQUALS_TARGET and target != source:
            findings.append(
                _finding(
                    source,
                    f"manifest-{row.disposition}-target-invalid",
                    "disposition requires source and target equality",
                )
            )
        merge_replacement: Record | None = None
        if row.disposition == "merge" and row.canonical_replacement is not None:
            merge_replacement, replacement_findings = _resolve_canonical_replacement(
                profiles,
                source=source,
                target=target,
                replacement=row.canonical_replacement,
                disposition=row.disposition,
                records=canonical_records,
                payloads=canonical_payloads,
            )
            findings.extend(replacement_findings)
            if merge_replacement is not None and baseline is not None and target is not None:
                findings.extend(
                    _baseline_merge_owner_findings(
                        root=root,
                        profiles=profiles,
                        baseline=baseline,
                        row=row,
                        target=target,
                        replacement=merge_replacement,
                        baseline_records=baseline_records,
                        entries=document.entries,
                    )
                )
        removes_source = row.disposition in {"move", "merge", "archive", "delete"}
        if removes_source and os.path.lexists(root / source):
            findings.append(
                _finding(
                    source,
                    "manifest-source-result-present",
                    "source path remains present after a removing disposition",
                )
            )
        if row.disposition != "delete" and target is not None and _safe_path(target):
            target_bytes = result_payloads.get(target)
            if target_bytes is None:
                findings.append(
                    _finding(
                        target,
                        "manifest-target-missing",
                        "result target is not a regular in-root file",
                    )
                )
            else:
                try:
                    target_text = target_bytes.decode("utf-8")
                    target_metadata = metadata._parse_frontmatter_text(target_text)
                except (UnicodeDecodeError, metadata.FrontmatterError):
                    findings.append(
                        _finding(
                            target,
                            "manifest-target-file-invalid",
                            "result target metadata cannot be parsed safely",
                        )
                    )
                else:
                    target_record = result_records_by_path.get(target)
                    if target_record is None:
                        target_record = metadata._record_from_text(
                            pathlib.Path(target), target_text, profiles=profiles
                        )
                    target_type = target_record.artifact_type
                    expected_target_type = (
                        "archive" if row.disposition == "archive" else row.artifact_type
                    )
                    if target_type != expected_target_type:
                        findings.append(
                            _finding(
                                target,
                                "manifest-target-artifact-type-mismatch",
                                "result target type differs from manifest truth",
                            )
                        )
                    expected_target_id = _manifest_artifact_id(
                        target_type, target_metadata.get("artifact_id")
                    )
                    merge_target_value = (
                        merge_replacement.metadata.get("artifact_id")
                        if merge_replacement is not None
                        else None
                    )
                    manifest_target_id = (
                        merge_target_value
                        if row.disposition == "merge"
                        and isinstance(merge_target_value, str)
                        else row.artifact_id
                    )
                    if (
                        row.disposition != "merge" or merge_replacement is not None
                    ) and expected_target_id != manifest_target_id:
                        findings.append(
                            _finding(
                                target,
                                "manifest-target-artifact-id-mismatch",
                                "result target identity differs from manifest truth",
                            )
                        )
                    target_status = target_metadata.get("status")
                    expected_target_status = (
                        target_status if isinstance(target_status, str) else None
                    )
                    if expected_target_status != row.status_after:
                        findings.append(
                            _finding(
                                target,
                                "manifest-target-status-mismatch",
                                "result target status differs from manifest truth",
                            )
                        )
                    target_parents = target_metadata.get("parent_ids")
                    expected_target_parents = (
                        tuple(sorted(target_parents))
                        if isinstance(target_parents, list)
                        and all(isinstance(item, str) for item in target_parents)
                        else ()
                    )
                    if expected_target_parents != row.parent_ids:
                        findings.append(
                            _finding(
                                target,
                                "manifest-target-parent-ids-mismatch",
                                "result target parents differ from manifest truth",
                            )
                        )
                    if row.disposition == "archive":
                        archive_findings: list[Finding] = []
                        archive_disposition_value = target_metadata.get(
                            "archive_disposition"
                        )
                        archive_disposition = (
                            archive_disposition_value
                            if isinstance(archive_disposition_value, str)
                            else None
                        )
                        required_archive = _profile_required_fields(
                            profiles, "archive"
                        )
                        if (
                            target_type != "archive"
                            or target_metadata.get("type") != "archive/migration"
                            or any(
                                key not in target_metadata
                                or target_metadata.get(key) in (None, "")
                                for key in required_archive
                            )
                        ):
                            archive_findings.append(
                                _finding(
                                    target,
                                    "manifest-archive-target-profile-invalid",
                                    "archive result does not satisfy the canonical archive profile",
                                )
                            )
                        if (
                            row.status_after != "archived"
                            or target_metadata.get("status") != "archived"
                        ):
                            archive_findings.append(
                                _finding(
                                    target,
                                    "manifest-archive-status-invalid",
                                    "archive result requires archived status",
                                )
                            )
                        if target_metadata.get("archived_from") != source:
                            archive_findings.append(
                                _finding(
                                    target,
                                    "manifest-archive-source-mismatch",
                                    "archive result does not bind the baseline source path",
                                )
                            )
                        if (
                            target_metadata.get("current_replacement")
                            != row.canonical_replacement
                        ):
                            archive_findings.append(
                                _finding(
                                    target,
                                    "manifest-archive-replacement-mismatch",
                                    "archive replacement differs from manifest truth",
                                )
                            )
                        if (
                            target_metadata.get("preservation_class")
                            != row.preservation_class
                        ):
                            archive_findings.append(
                                _finding(
                                    target,
                                    "manifest-archive-preservation-mismatch",
                                    "archive preservation differs from manifest truth",
                                )
                            )
                        intrinsic = [
                            item
                            for item in metadata.validate_record(
                                target_record, profiles, result_manifest
                            )
                            if item.severity == "error"
                        ]
                        if intrinsic:
                            archive_findings.extend(intrinsic)
                            archive_findings.append(
                                _finding(
                                    target,
                                    "manifest-archive-target-profile-invalid",
                                    "archive result does not satisfy the canonical archive profile",
                                )
                            )
                        archive_findings.extend(
                            validate_archive_provenance(root, target_record)
                        )
                        archived_blob = target_metadata.get("archived_blob")
                        baseline_blob = (
                            _blob_at_commit_path(root, baseline, source)
                            if baseline is not None
                            else None
                        )
                        if (
                            baseline_blob is None
                            or archived_blob != baseline_blob
                        ):
                            archive_findings.append(
                                _finding(
                                    target,
                                    "manifest-archive-baseline-blob-mismatch",
                                    "archive provenance does not preserve the manifest baseline blob",
                                )
                            )
                        required_replacement_dispositions = {
                            "superseded",
                            "duplicate",
                            "conflict",
                        }
                        if (
                            archive_disposition in required_replacement_dispositions
                            and row.canonical_replacement is None
                        ):
                            archive_findings.append(
                                _finding(
                                    source,
                                    "manifest-replacement-required",
                                    "archive disposition requires a canonical replacement",
                                )
                            )
                        if (
                            archive_disposition == "withdrawn"
                            and row.canonical_replacement is not None
                        ):
                            archive_findings.append(
                                _finding(
                                    source,
                                    "manifest-replacement-forbidden",
                                    "withdrawn archive forbids a canonical replacement",
                                )
                            )
                        if row.canonical_replacement is not None:
                            archive_findings.extend(
                                _canonical_replacement_findings(
                                    profiles,
                                    source=source,
                                    target=target,
                                    replacement=row.canonical_replacement,
                                    disposition=row.disposition,
                                    artifact_id=row.artifact_id,
                                    records=canonical_records,
                                    payloads=canonical_payloads,
                                )
                            )
                        findings.extend(archive_findings)
                        evidence_complete = all(
                            values
                            for values in (
                                row.evidence.commands,
                                row.evidence.sources,
                                row.evidence.repository_paths,
                                row.evidence.consumer_scan,
                                row.evidence.rollback,
                            )
                        )
                        archive_result_valid = (
                            not archive_findings
                            and expected_target_id == row.artifact_id
                            and expected_target_parents == row.parent_ids
                            and row.review_verdict == ReviewVerdict("pass", "pass")
                            and row.preservation_class is not None
                            and evidence_complete
                        )
        if row.disposition == "archive":
            transition_valid = archive_result_valid
        if not transition_valid:
            findings.append(
                _finding(
                    source,
                    "manifest-transition-invalid",
                    "status transition is not canonical",
                )
            )
        if row.disposition == "merge" and not row.canonical_replacement:
            findings.append(
                _finding(source, "manifest-replacement-required", "destructive row requires a replacement")
            )
        if (
            row.disposition == "delete"
            and row.canonical_replacement is not None
        ):
            findings.extend(
                _canonical_replacement_findings(
                    profiles,
                    source=source,
                    target=target,
                    replacement=row.canonical_replacement,
                    disposition=row.disposition,
                    artifact_id=row.artifact_id,
                    records=canonical_records,
                    payloads=canonical_payloads,
                )
            )
        if row.disposition in SOURCE_EQUALS_TARGET | {"move"} and row.canonical_replacement is not None:
            findings.append(
                _finding(source, "manifest-replacement-forbidden", "disposition forbids a replacement")
            )
        if row.preservation_class is not None and row.preservation_class not in preservation_classes:
            findings.append(
                _finding(source, "manifest-preservation-invalid", "preservation class is not registered")
            )
        for consumer in row.active_consumers:
            if not _safe_path(consumer.as_posix()):
                findings.append(
                    _finding(source, "manifest-consumer-path-invalid", "consumer path is not repository-safe")
                )
        for repository_path in row.evidence.repository_paths:
            if not _safe_path(repository_path.as_posix()):
                findings.append(
                    _finding(source, "manifest-evidence-path-invalid", "evidence path is not repository-safe")
                )
        evidence_values = (
            *row.evidence.commands,
            *row.evidence.sources,
            *(path.as_posix() for path in row.evidence.repository_paths),
            *row.evidence.consumer_scan,
            *row.evidence.rollback,
        )
        if any(_sensitive_value_is_present(value) for value in evidence_values):
            findings.append(
                _finding(
                    source,
                    "manifest-evidence-confidential",
                    "manifest evidence contains prohibited confidential data",
                )
            )
        findings.extend(_reviewed_evidence_findings(root, document, row))
        if row.partition_plan is not None:
            findings.extend(
                _partition_plan_findings(
                    root,
                    profiles,
                    row,
                    records=canonical_records if canonical_payloads else None,
                    payloads=canonical_payloads if canonical_payloads else None,
                )
            )
        deterministic_lists: tuple[tuple[object, ...], ...] = (
            row.parent_ids,
            row.active_consumers,
            row.evidence.commands,
            row.evidence.sources,
            row.evidence.repository_paths,
            row.evidence.consumer_scan,
            row.evidence.rollback,
        )
        if any(values != tuple(sorted(values)) or len(values) != len(set(values)) for values in deterministic_lists):
            findings.append(
                _finding(
                    source,
                    "manifest-order-invalid",
                    "manifest list values must be unique and deterministically ordered",
                )
            )
        if row.canonical_replacement is not None and not row.canonical_replacement.strip():
            findings.append(
                _finding(
                    source,
                    "manifest-replacement-invalid",
                    "canonical replacement must be non-empty when present",
                )
            )
        if row.review_verdict.specification not in REVIEW_VALUES or row.review_verdict.quality not in REVIEW_VALUES:
            findings.append(
                _finding(source, "manifest-review-verdict-invalid", "review verdict is not registered")
            )
        if row.disposition in DESTRUCTIVE_DISPOSITIONS:
            if row.preservation_class is None:
                findings.append(
                    _finding(source, "manifest-preservation-required", "destructive row requires preservation")
                )
            evidence_lists = (
                row.evidence.commands,
                row.evidence.sources,
                row.evidence.repository_paths,
                row.evidence.consumer_scan,
                row.evidence.rollback,
            )
            if any(not values for values in evidence_lists):
                findings.append(
                    _finding(
                        source,
                        "manifest-destructive-evidence-required",
                        "destructive row requires complete bounded evidence",
                    )
                )
            if row.review_verdict != ReviewVerdict("pass", "pass"):
                findings.append(
                    _finding(
                        source,
                        "manifest-destructive-review-required",
                        "destructive row requires independent passing reviews",
                    )
                )
    return _reconcile_task5_promoted_findings(
        root,
        contract,
        document,
        findings,
        manifest_path=manifest_path,
    )



def _load_declared_manifests(
    root: pathlib.Path,
    profiles: dict[str, object],
    contract: dict[str, object],
    *,
    promoted_only: bool,
    selected_wave: str | None = None,
) -> tuple[tuple[MigrationManifestDocument, ...], list[Finding]]:
    documents: list[MigrationManifestDocument] = []
    findings: list[Finding] = []
    waves = contract.get("waves")
    if not isinstance(waves, dict):
        raise ProfileError("contract waves must be a mapping")
    if selected_wave is not None and selected_wave not in waves:
        raise ProfileError(f"unknown migration wave: {selected_wave}")
    for wave_name, raw_wave in waves.items():
        if selected_wave is not None and wave_name != selected_wave:
            continue
        if not isinstance(wave_name, str) or not isinstance(raw_wave, dict):
            raise ProfileError("contract wave entry is invalid")
        enforcement = raw_wave.get("enforcement")
        manifest_path = raw_wave.get("manifest_path")
        if manifest_path is None:
            if promoted_only and enforcement == "blocking":
                findings.append(
                    _finding(
                        wave_name,
                        "promoted-manifest-path-required",
                        "blocking wave requires a manifest path",
                    )
                )
            continue
        if not isinstance(manifest_path, str) or not _safe_path(manifest_path):
            findings.append(
                _finding(wave_name, "promoted-manifest-path-invalid", "manifest path is unsafe")
            )
            continue
        absolute = root / manifest_path
        if not os.path.lexists(absolute):
            findings.append(
                _finding(manifest_path, "promoted-manifest-missing", "declared manifest does not exist")
            )
            continue
        try:
            document = _load_repo_migration_manifest(root, manifest_path)
        except ProfileError:
            if (
                wave_name == "sdlc-taxonomy-convergence"
                and enforcement == "advisory"
                and raw_wave.get("scope_state") == "approved"
                and manifest_path
                == "docs/99.templates/support/document-corpus-migration-contract.yaml"
                and (
                    _task5_reconciliation_ready(root, contract)
                    or _task7_reconciliation_ready(root, contract)
                )
            ):
                # The approved SDLC registry is the bounded migration owner,
                # not a serialized lifecycle-manifest document. mig-0001 owns
                # its executed rows after Task 5 completes.
                continue
            findings.append(
                _finding(
                    manifest_path,
                    "promoted-manifest-file-invalid",
                    "declared manifest must be a tracked regular canonical file",
                )
            )
            continue
        if document.wave != wave_name:
            findings.append(
                _finding(manifest_path, "promoted-wave-mismatch", "manifest wave differs from registry")
            )
        if document.enforcement != enforcement:
            findings.append(
                _finding(
                    manifest_path,
                    "promoted-enforcement-mismatch",
                    "manifest enforcement differs from registry",
                )
            )
        findings.extend(
            validate_migration_manifest(
                root,
                profiles,
                contract,
                document,
                manifest_path=manifest_path,
            )
        )
        if not _repo_manifest_matches(
            root,
            manifest_path,
            render_migration_manifest(document),
        ):
            findings.append(
                _finding(manifest_path, "manifest-serialization-stale", "manifest bytes are not canonical")
            )
        documents.append(document)
    return tuple(documents), sorted(set(findings))



def _historical_promoted_findings(root: pathlib.Path) -> list[Finding]:
    """Check immutable promoted evidence against exact approved recovery blobs.

    Historical manifest target names describe their execution snapshot, not the
    current corpus. Migration 0003 maps those evidence files to current Data
    packages; Stage 99 and current lifecycle readers validate today's documents.
    """

    findings: list[Finding] = []
    migration = archive_authority._migration_document(root)
    selected = [row for row in migration["rows"] if row.get("artifact_id") in {"DATA-0067", "DATA-0069"}]
    if len(selected) != 2 or {row["artifact_id"] for row in selected} != {"DATA-0067", "DATA-0069"}:
        raise ProfileError("promoted historical evidence mappings are incomplete")
    for row in selected:
        target = row["target_path"]
        recovery = row["recovery_commit"] if row["recovery_commit"] is not None else migration["baseline_commit"]
        historical = HistoricalDocument(root, recovery, row["source_path"])
        expected = historical.read_bytes()
        # Parse exact historical shape, rejecting duplicate keys and unsafe paths.
        _load_migration_manifest_text(expected.decode("utf-8"))
        observed = _read_regular_repo_bytes(root, target, require_tracked=True)
        if observed != expected:
            findings.append(_finding(target, "historical-manifest-drift", "historical evidence differs from its verified recovery blob"))
    return findings
