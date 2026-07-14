#!/usr/bin/env python3
"""Validate document-corpus lifecycle manifests and archive provenance safely."""

from __future__ import annotations

import argparse
import collections
import collections.abc
import dataclasses
import datetime
import hashlib
import importlib.util
import pathlib
import re
import subprocess
import sys
from typing import Any

import yaml


ROOT = pathlib.Path(__file__).resolve().parents[2]
DEFAULT_PROFILES = ROOT / "docs/99.templates/support/document-metadata-profiles.yaml"
DEFAULT_CONTRACT = ROOT / "docs/99.templates/support/document-corpus-migration-contract.yaml"
METADATA_SCRIPT = ROOT / "scripts/validation/check-document-metadata.py"

MODES = (
    "check-contract",
    "generate-manifest",
    "check-manifest",
    "check-promoted",
    "generate-summary",
    "check-summary",
    "check-impacted",
    "report-duplicates",
    "report-full",
    "check-full",
    "check-archive",
    "check-directory-budget",
    "generate-archive-ledger",
    "check-archive-ledger",
    "generate-snapshot-manifest",
    "check-snapshot-manifest",
)


def _load_metadata_module() -> Any:
    spec = importlib.util.spec_from_file_location(
        "document_metadata_for_corpus_lifecycle", METADATA_SCRIPT
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("metadata validator module is unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


metadata = _load_metadata_module()
Finding = metadata.Finding
Record = metadata.Record
ProfileError = metadata.ProfileError


@dataclasses.dataclass(frozen=True)
class ReviewVerdict:
    specification: str
    quality: str


@dataclasses.dataclass(frozen=True)
class ManifestEvidence:
    commands: tuple[str, ...]
    sources: tuple[str, ...]
    repository_paths: tuple[pathlib.PurePosixPath, ...]
    consumer_scan: tuple[str, ...]
    rollback: tuple[str, ...]


@dataclasses.dataclass(frozen=True)
class MigrationManifestRow:
    source_path: pathlib.PurePosixPath
    target_path: pathlib.PurePosixPath | None
    artifact_id: str | None
    artifact_type: str
    status_before: str | None
    status_after: str | None
    parent_ids: tuple[str, ...]
    disposition: str
    canonical_replacement: str | None
    active_consumers: tuple[pathlib.PurePosixPath, ...]
    partition_plan: pathlib.PurePosixPath | None
    preservation_class: str | None
    evidence: ManifestEvidence
    review_verdict: ReviewVerdict


@dataclasses.dataclass(frozen=True)
class MigrationManifestDocument:
    schema_version: int
    wave: str
    baseline_commit: str
    generated_by: str
    enforcement: str
    entries: tuple[MigrationManifestRow, ...]


@dataclasses.dataclass(frozen=True, order=True)
class DuplicateCandidate:
    left_path: pathlib.PurePosixPath
    right_path: pathlib.PurePosixPath
    artifact_type: str
    signals: tuple[str, ...]


MANIFEST_TOP_LEVEL_FIELDS = (
    "schema_version",
    "wave",
    "baseline_commit",
    "generated_by",
    "enforcement",
    "entries",
)
MANIFEST_ENTRY_FIELDS = (
    "source_path",
    "target_path",
    "artifact_id",
    "artifact_type",
    "status_before",
    "status_after",
    "parent_ids",
    "disposition",
    "canonical_replacement",
    "active_consumers",
    "partition_plan",
    "preservation_class",
    "evidence",
    "review_verdict",
)
EVIDENCE_FIELDS = (
    "commands",
    "sources",
    "repository_paths",
    "consumer_scan",
    "rollback",
)
REVIEW_FIELDS = ("specification", "quality")
DESTRUCTIVE_DISPOSITIONS = frozenset({"merge", "archive", "delete"})
SOURCE_EQUALS_TARGET = frozenset(
    {"migrate", "preserve", "regenerate", "exempt"}
)
TARGET_DISTINCT = frozenset({"move", "merge", "archive"})
REVIEW_VALUES = frozenset({"pending", "pass", "changes-required"})
OBJECT_ID = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})\Z")
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)(?:\s+[^)]*)?\)")
TITLE_PUNCTUATION = re.compile(r"[^a-z0-9]+")
SENSITIVE_PAYLOAD_PATTERNS = (
    re.compile(rb"(?i)(?:password|passwd|credential|secret|token|access[_-]?token|refresh[_-]?token|api[_-]?key)\s*[:=]"),
    re.compile(rb"(?i)(?:auth|authorization)\s*[:=]\s*(?:bearer|basic|[A-Za-z0-9+/]{16,})"),
    re.compile(rb"\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b"),
    re.compile(rb"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(rb"(?i)(?:^|/|\\)\.(?:bash|zsh|sh)_history(?:\s|$)|\bHISTFILE\s*="),
    re.compile(rb"(?m)^\d{4}-\d{2}-\d{2}(?:T|\s).*(?:ERROR|WARN|DEBUG|TRACE)\b"),
    re.compile(rb"(?mi)^(?:TRACE|DEBUG|INFO|WARN|ERROR|FATAL)\b"),
)
SAFETY_CODE_PARTS = (
    "-path-invalid",
    "-commit-invalid",
    "-blob-invalid",
    "-blob-mismatch",
    "-sha256-mismatch",
    "-confidential",
    "archive-snapshot-missing",
    "invalid-archived-",
    "invalid-content-sha256",
    "invalid-snapshot-path",
    "malformed-yaml",
    "duplicate-key",
    "unreadable",
    "parse-",
    "contract-",
    "internal-",
)
KNOWN_FINDING_CODES = frozenset(
    {
        "manifest-source-missing",
        "manifest-source-duplicate",
        "manifest-source-unexpected",
        "manifest-source-path-invalid",
        "manifest-target-path-invalid",
        "manifest-artifact-type-invalid",
        "manifest-artifact-id-invalid",
        "manifest-status-invalid",
        "manifest-baseline-commit-invalid",
        "manifest-wave-mismatch",
        "manifest-enforcement-mismatch",
        "manifest-delete-target-invalid",
        "manifest-move-target-required",
        "manifest-move-target-invalid",
        "manifest-preserve-target-invalid",
        "manifest-destructive-review-required",
        "manifest-destructive-evidence-required",
        "manifest-preservation-required",
        "manifest-replacement-required",
        "manifest-replacement-forbidden",
        "manifest-serialization-stale",
        "directory-budget-warning",
        "directory-budget-blocked",
        "review-age-unavailable",
        "review-due",
        "archive-commit-invalid",
        "archive-blob-invalid",
        "archive-blob-mismatch",
        "archive-snapshot-path-mismatch",
        "archive-content-sha256-mismatch",
        "archive-snapshot-confidential",
        "archive-snapshot-forbidden",
    }
)


def _finding(
    path: str | pathlib.PurePath,
    code: str,
    message: str,
    severity: str = "error",
) -> Finding:
    return Finding(pathlib.PurePosixPath(path).as_posix(), code, message, severity)


def _run_git(
    root: pathlib.Path,
    args: collections.abc.Sequence[str],
    *,
    text: bool = True,
) -> subprocess.CompletedProcess[str] | subprocess.CompletedProcess[bytes]:
    try:
        return subprocess.run(
            ["git", "-C", str(root), *args],
            capture_output=True,
            text=text,
            check=False,
        )
    except OSError as error:
        raise ProfileError("Git executable is unavailable") from error


def _verified_commit(root: pathlib.Path, ref: str) -> str | None:
    result = _run_git(
        root,
        ["rev-parse", "--verify", "--end-of-options", f"{ref}^{{commit}}"],
    )
    value = result.stdout.strip() if result.returncode == 0 else ""
    return value if OBJECT_ID.fullmatch(value) else None


def _git_object_type(root: pathlib.Path, object_id: str) -> str | None:
    result = _run_git(root, ["cat-file", "-t", object_id])
    return result.stdout.strip() if result.returncode == 0 else None


def _safe_path(value: object) -> bool:
    return bool(metadata._safe_repo_path(value)) and isinstance(value, str) and not any(
        marker in value for marker in "*?[]{}"
    )


def _safe_path_text(value: pathlib.PurePosixPath | None) -> str | None:
    return None if value is None else value.as_posix()


def _as_exact_mapping(value: object, fields: tuple[str, ...], label: str) -> dict[str, object]:
    if not isinstance(value, dict) or not all(isinstance(key, str) for key in value):
        raise ProfileError(f"{label} must be a string-keyed mapping")
    if tuple(value) != fields or set(value) != set(fields):
        raise ProfileError(f"{label} must define the exact canonical fields")
    return value


def _as_string(value: object, label: str, *, nullable: bool = False) -> str | None:
    if nullable and value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        raise ProfileError(f"{label} must be a non-empty string")
    return value


def _as_string_tuple(value: object, label: str) -> tuple[str, ...]:
    if not isinstance(value, list) or not all(
        isinstance(item, str) and item.strip() for item in value
    ):
        raise ProfileError(f"{label} must be a list of non-empty strings")
    if len(value) != len(set(value)):
        raise ProfileError(f"{label} must not contain duplicates")
    return tuple(sorted(item.strip() for item in value))


def _as_path_tuple(value: object, label: str) -> tuple[pathlib.PurePosixPath, ...]:
    values = _as_string_tuple(value, label)
    return tuple(pathlib.PurePosixPath(item) for item in values)


def load_migration_contract(path: pathlib.Path) -> dict[str, object]:
    """Load the contract through the canonical metadata validator."""

    return metadata.load_migration_contract(path)


def load_migration_manifest(path: pathlib.Path) -> MigrationManifestDocument:
    """Load an exact, duplicate-key-safe migration manifest."""

    try:
        loaded = metadata._safe_load_unique(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as error:
        raise ProfileError("cannot load migration manifest safely") from error
    top = _as_exact_mapping(loaded, MANIFEST_TOP_LEVEL_FIELDS, "migration manifest")
    if type(top["schema_version"]) is not int or top["schema_version"] != 1:
        raise ProfileError("migration manifest schema_version must be the integer 1")
    entries_value = top["entries"]
    if not isinstance(entries_value, list):
        raise ProfileError("migration manifest entries must be a list")
    entries: list[MigrationManifestRow] = []
    for index, raw_entry in enumerate(entries_value):
        label = f"migration manifest entry {index}"
        entry = _as_exact_mapping(raw_entry, MANIFEST_ENTRY_FIELDS, label)
        evidence_raw = _as_exact_mapping(
            entry["evidence"], EVIDENCE_FIELDS, f"{label} evidence"
        )
        review_raw = _as_exact_mapping(
            entry["review_verdict"], REVIEW_FIELDS, f"{label} review_verdict"
        )
        target = _as_string(entry["target_path"], f"{label} target_path", nullable=True)
        partition = _as_string(
            entry["partition_plan"], f"{label} partition_plan", nullable=True
        )
        review = ReviewVerdict(
            _as_string(review_raw["specification"], f"{label} specification") or "",
            _as_string(review_raw["quality"], f"{label} quality") or "",
        )
        entries.append(
            MigrationManifestRow(
                source_path=pathlib.PurePosixPath(
                    _as_string(entry["source_path"], f"{label} source_path") or ""
                ),
                target_path=pathlib.PurePosixPath(target) if target is not None else None,
                artifact_id=_as_string(
                    entry["artifact_id"], f"{label} artifact_id", nullable=True
                ),
                artifact_type=_as_string(
                    entry["artifact_type"], f"{label} artifact_type"
                )
                or "",
                status_before=_as_string(
                    entry["status_before"], f"{label} status_before", nullable=True
                ),
                status_after=_as_string(
                    entry["status_after"], f"{label} status_after", nullable=True
                ),
                parent_ids=_as_string_tuple(entry["parent_ids"], f"{label} parent_ids"),
                disposition=_as_string(entry["disposition"], f"{label} disposition")
                or "",
                canonical_replacement=_as_string(
                    entry["canonical_replacement"],
                    f"{label} canonical_replacement",
                    nullable=True,
                ),
                active_consumers=_as_path_tuple(
                    entry["active_consumers"], f"{label} active_consumers"
                ),
                partition_plan=pathlib.PurePosixPath(partition)
                if partition is not None
                else None,
                preservation_class=_as_string(
                    entry["preservation_class"],
                    f"{label} preservation_class",
                    nullable=True,
                ),
                evidence=ManifestEvidence(
                    _as_string_tuple(evidence_raw["commands"], f"{label} commands"),
                    _as_string_tuple(evidence_raw["sources"], f"{label} sources"),
                    _as_path_tuple(
                        evidence_raw["repository_paths"],
                        f"{label} repository_paths",
                    ),
                    _as_string_tuple(
                        evidence_raw["consumer_scan"], f"{label} consumer_scan"
                    ),
                    _as_string_tuple(evidence_raw["rollback"], f"{label} rollback"),
                ),
                review_verdict=review,
            )
        )
    return MigrationManifestDocument(
        schema_version=1,
        wave=_as_string(top["wave"], "migration manifest wave") or "",
        baseline_commit=_as_string(
            top["baseline_commit"], "migration manifest baseline_commit"
        )
        or "",
        generated_by=_as_string(top["generated_by"], "migration manifest generated_by")
        or "",
        enforcement=_as_string(top["enforcement"], "migration manifest enforcement")
        or "",
        entries=tuple(sorted(entries, key=lambda row: row.source_path.as_posix())),
    )


def _manifest_mapping(document: MigrationManifestDocument) -> dict[str, object]:
    return {
        "schema_version": document.schema_version,
        "wave": document.wave,
        "baseline_commit": document.baseline_commit,
        "generated_by": document.generated_by,
        "enforcement": document.enforcement,
        "entries": [
            {
                "source_path": row.source_path.as_posix(),
                "target_path": _safe_path_text(row.target_path),
                "artifact_id": row.artifact_id,
                "artifact_type": row.artifact_type,
                "status_before": row.status_before,
                "status_after": row.status_after,
                "parent_ids": sorted(row.parent_ids),
                "disposition": row.disposition,
                "canonical_replacement": row.canonical_replacement,
                "active_consumers": sorted(path.as_posix() for path in row.active_consumers),
                "partition_plan": _safe_path_text(row.partition_plan),
                "preservation_class": row.preservation_class,
                "evidence": {
                    "commands": sorted(row.evidence.commands),
                    "sources": sorted(row.evidence.sources),
                    "repository_paths": sorted(
                        path.as_posix() for path in row.evidence.repository_paths
                    ),
                    "consumer_scan": sorted(row.evidence.consumer_scan),
                    "rollback": sorted(row.evidence.rollback),
                },
                "review_verdict": {
                    "specification": row.review_verdict.specification,
                    "quality": row.review_verdict.quality,
                },
            }
            for row in sorted(document.entries, key=lambda item: item.source_path.as_posix())
        ],
    }


def render_migration_manifest(document: MigrationManifestDocument) -> str:
    """Render a stable LF-only manifest without semantic invention."""

    return yaml.safe_dump(
        _manifest_mapping(document),
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False,
        width=1000,
    )


def _wave_mapping(contract: dict[str, object], wave: str) -> dict[str, object]:
    waves = contract.get("waves")
    value = waves.get(wave) if isinstance(waves, dict) else None
    if not isinstance(value, dict):
        raise ProfileError(f"unknown migration wave: {wave}")
    return value


def generate_manifest_skeleton(
    root: pathlib.Path,
    contract: dict[str, object],
    *,
    wave: str,
    baseline_ref: str,
) -> MigrationManifestDocument:
    """Generate a pending skeleton from exact baseline bytes."""

    baseline_commit = _verified_commit(root, baseline_ref)
    if baseline_commit is None:
        raise ProfileError("baseline_ref must resolve to a commit")
    wave_contract = _wave_mapping(contract, wave)
    source_paths = wave_contract.get("source_paths")
    if not isinstance(source_paths, list) or not all(
        isinstance(item, str) for item in source_paths
    ):
        raise ProfileError("wave source_paths must be a string list")
    rows: list[MigrationManifestRow] = []
    for source_path in source_paths:
        if not _safe_path(source_path):
            raise ProfileError("wave source path is unsafe")
        shown = _run_git(root, ["show", f"{baseline_commit}:{source_path}"], text=False)
        if shown.returncode != 0:
            raise ProfileError("wave source path is not tracked at the baseline")
        try:
            source_text = shown.stdout.decode("utf-8")
            frontmatter = metadata._parse_frontmatter_text(source_text)
        except (UnicodeDecodeError, metadata.FrontmatterError) as error:
            raise ProfileError("wave source frontmatter cannot be parsed") from error
        relative = pathlib.Path(source_path)
        artifact_type = (
            "generated"
            if "generated_by" in frontmatter
            else metadata.infer_artifact_type(relative)
        )
        artifact_id = frontmatter.get("artifact_id")
        status = frontmatter.get("status")
        rows.append(
            MigrationManifestRow(
                source_path=pathlib.PurePosixPath(source_path),
                target_path=pathlib.PurePosixPath(source_path),
                artifact_id=artifact_id if isinstance(artifact_id, str) else None,
                artifact_type=artifact_type,
                status_before=status if isinstance(status, str) else None,
                status_after=status if isinstance(status, str) else None,
                parent_ids=(),
                disposition="preserve",
                canonical_replacement=None,
                active_consumers=(),
                partition_plan=None,
                preservation_class=None,
                evidence=ManifestEvidence((), (), (), (), ()),
                review_verdict=ReviewVerdict("pending", "pending"),
            )
        )
    return MigrationManifestDocument(
        schema_version=1,
        wave=wave,
        baseline_commit=baseline_commit,
        generated_by="check-document-corpus-lifecycle.py",
        enforcement=str(wave_contract.get("enforcement", "advisory")),
        entries=tuple(sorted(rows, key=lambda row: row.source_path.as_posix())),
    )


def _profile_required_fields(
    profiles: dict[str, object], artifact_type: str
) -> set[str]:
    profile_map = profiles.get("profiles")
    profile = profile_map.get(artifact_type) if isinstance(profile_map, dict) else None
    required = profile.get("required") if isinstance(profile, dict) else None
    return set(required) if isinstance(required, list) else set()


def validate_migration_manifest(
    root: pathlib.Path,
    profiles: dict[str, object],
    contract: dict[str, object],
    document: MigrationManifestDocument,
) -> list[Finding]:
    """Return stable manifest findings without changing human dispositions."""

    findings: list[Finding] = []
    path = "manifest"
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
    for row_index, row in enumerate(document.entries):
        source = row.source_path.as_posix()
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
                            else metadata.infer_artifact_type(pathlib.Path(source))
                        )
                        if row.artifact_type != expected_type:
                            findings.append(
                                _finding(
                                    source,
                                    "manifest-artifact-type-mismatch",
                                    "artifact type differs from the canonical path profile",
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
        if row.disposition in {"merge", "archive"} and not row.canonical_replacement:
            findings.append(
                _finding(source, "manifest-replacement-required", "destructive row requires a replacement")
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
        if row.partition_plan is not None:
            partition = row.partition_plan.as_posix()
            if not _safe_path(partition) or not partition.startswith(
                "docs/04.execution/plans/"
            ):
                findings.append(
                    _finding(source, "manifest-partition-plan-invalid", "partition plan path is invalid")
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
    return sorted(set(findings))


def _changed_record_paths(root: pathlib.Path, base_ref: str) -> set[str]:
    baseline = _verified_commit(root, base_ref)
    if baseline is None:
        raise ProfileError("base_ref must resolve to a commit")
    paths: set[str] = set()
    commands = (
        ["diff", "--name-only", "--diff-filter=ACMRTUXB", baseline, "--", "*.md"],
        ["ls-files", "--others", "--exclude-standard", "--", "*.md"],
    )
    for command in commands:
        result = _run_git(root, command)
        if result.returncode != 0:
            raise ProfileError("cannot determine impacted Markdown paths")
        paths.update(line.strip() for line in result.stdout.splitlines() if line.strip())
    return {path for path in paths if _safe_path(path)}


def _added_record_paths(root: pathlib.Path, base_ref: str) -> frozenset[pathlib.PurePosixPath]:
    baseline = _verified_commit(root, base_ref)
    if baseline is None:
        raise ProfileError("base_ref must resolve to a commit")
    paths: set[str] = set()
    commands = (
        ["diff", "--name-only", "--diff-filter=A", baseline, "--", "*.md"],
        ["ls-files", "--others", "--exclude-standard", "--", "*.md"],
    )
    for command in commands:
        result = _run_git(root, command)
        if result.returncode != 0:
            raise ProfileError("cannot determine added Markdown paths")
        paths.update(line.strip() for line in result.stdout.splitlines() if line.strip())
    return frozenset(pathlib.PurePosixPath(path) for path in paths if _safe_path(path))


def _apply_partition_approvals(
    records: collections.abc.Sequence[Record],
    documents: collections.abc.Sequence[MigrationManifestDocument],
) -> tuple[Record, ...]:
    approvals: dict[str, tuple[str, dict[str, str]]] = {}
    for document in documents:
        for row in document.entries:
            if row.partition_plan is None or row.review_verdict != ReviewVerdict("pass", "pass"):
                continue
            target = row.target_path or row.source_path
            approvals[target.as_posix()] = (
                row.partition_plan.as_posix(),
                {"specification": "pass", "quality": "pass"},
            )
    return tuple(
        dataclasses.replace(
            record,
            metadata={
                **record.metadata,
                "partition_plan": approvals[record.path.as_posix()][0],
                "review_verdict": approvals[record.path.as_posix()][1],
            },
        )
        if record.path.as_posix() in approvals
        else record
        for record in records
    )


def _resolved_markdown_links(root: pathlib.Path, record: Record) -> set[str]:
    try:
        text = (root / record.path).read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return set()
    links: set[str] = set()
    for match in MARKDOWN_LINK.finditer(text):
        raw = match.group(1).split("#", 1)[0]
        if not raw or "://" in raw or raw.startswith(("mailto:", "#")):
            continue
        if raw.startswith("/"):
            candidate = pathlib.PurePosixPath(raw.lstrip("/"))
        else:
            candidate = pathlib.PurePosixPath(record.path.parent.as_posix(), raw)
        normalized_parts: list[str] = []
        for part in candidate.parts:
            if part == ".":
                continue
            if part == "..":
                if normalized_parts:
                    normalized_parts.pop()
                continue
            normalized_parts.append(part)
        normalized = pathlib.PurePosixPath(*normalized_parts).as_posix()
        if _safe_path(normalized):
            links.add(normalized)
    return links


def collect_impacted_records(
    root: pathlib.Path,
    records: collections.abc.Sequence[Record],
    profiles: dict[str, object],
    contract: dict[str, object],
    documents: collections.abc.Sequence[MigrationManifestDocument],
    *,
    base_ref: str,
) -> tuple[Record, ...]:
    """Select changed records and direct semantic dependents only."""

    del profiles, contract
    by_path = {record.path.as_posix(): record for record in records}
    by_id = {
        artifact_id: record.path.as_posix()
        for record in records
        if isinstance((artifact_id := record.metadata.get("artifact_id")), str)
    }
    baseline_commit = _verified_commit(root, base_ref)
    if baseline_commit is None:
        raise ProfileError("base_ref must resolve to a commit")
    changed_paths = _changed_record_paths(root, base_ref)
    selected = changed_paths & set(by_path)
    historical_ids: set[str] = set()
    for changed_path in sorted(changed_paths):
        shown = _run_git(root, ["show", f"{baseline_commit}:{changed_path}"], text=False)
        if shown.returncode != 0:
            continue
        try:
            prior_text = shown.stdout.decode("utf-8")
            prior = metadata._record_from_text(pathlib.Path(changed_path), prior_text)
        except UnicodeError:
            continue
        prior_id = prior.metadata.get("artifact_id")
        if isinstance(prior_id, str):
            historical_ids.add(prior_id)
    selected_ids = historical_ids | {
        record.metadata.get("artifact_id")
        for path in selected
        if (record := by_path.get(path)) is not None
        and isinstance(record.metadata.get("artifact_id"), str)
    }
    additions: set[str] = set()
    for path, record in by_path.items():
        parent_ids = record.metadata.get("parent_ids")
        supersedes = record.metadata.get("supersedes")
        relations = set(parent_ids) if isinstance(parent_ids, list) else set()
        if isinstance(supersedes, str):
            relations.add(supersedes)
        if relations & selected_ids:
            additions.add(path)
        if path in selected:
            additions.update(by_id[item] for item in relations if item in by_id)
        if _resolved_markdown_links(root, record) & changed_paths:
            additions.add(path)
    for document in documents:
        for row in document.entries:
            source = row.source_path.as_posix()
            target = _safe_path_text(row.target_path)
            replacement = row.canonical_replacement
            replacement_path = (
                replacement
                if isinstance(replacement, str) and replacement in by_path
                else by_id.get(replacement or "")
            )
            participants = {source}
            if target:
                participants.add(target)
            if replacement_path:
                participants.add(replacement_path)
            consumers = {item.as_posix() for item in row.active_consumers}
            if participants & changed_paths:
                additions.update(consumers | participants)
            if consumers & selected:
                additions.update(participants)
    selected.update(additions & set(by_path))
    return tuple(by_path[path] for path in sorted(selected))


def _safe_archive_value(record: Record, key: str) -> str | None:
    value = record.metadata.get(key)
    return value if isinstance(value, str) and value else None


def validate_archive_provenance(root: pathlib.Path, record: Record) -> list[Finding]:
    """Verify Git and snapshot identity while returning value-free diagnostics."""

    if record.artifact_type != "archive":
        return []
    findings: list[Finding] = []
    path = record.path.as_posix()
    commit = _safe_archive_value(record, "archived_commit")
    blob = _safe_archive_value(record, "archived_blob")
    archived_from = _safe_archive_value(record, "archived_from")
    preservation = _safe_archive_value(record, "preservation_class")
    snapshot_path = _safe_archive_value(record, "snapshot_path")
    content_sha256 = _safe_archive_value(record, "content_sha256")
    snapshot_fields_present = any(
        record.metadata.get(key) is not None
        for key in ("snapshot_path", "content_sha256", "snapshot_reason")
    )
    if preservation == "git-history" and snapshot_fields_present:
        findings.append(
            _finding(path, "archive-snapshot-forbidden", "git-history forbids snapshot fields")
        )
    if preservation is None:
        findings.append(
            _finding(path, "archive-preservation-missing", "archive preservation class is unavailable")
        )
    if commit is None:
        findings.append(
            _finding(path, "archive-commit-missing", "archive commit provenance is unavailable")
        )
        return sorted(set(findings))
    if not OBJECT_ID.fullmatch(commit) or _git_object_type(root, commit) != "commit":
        findings.append(
            _finding(path, "archive-commit-invalid", "archived commit is not a commit object")
        )
        return sorted(set(findings))
    if blob is None:
        findings.append(
            _finding(path, "archive-blob-missing", "archive blob provenance is unavailable")
        )
        return sorted(set(findings))
    if not OBJECT_ID.fullmatch(blob) or _git_object_type(root, blob) != "blob":
        findings.append(
            _finding(path, "archive-blob-invalid", "archived blob is not a blob object")
        )
        return sorted(set(findings))
    if archived_from is None:
        findings.append(
            _finding(path, "archive-source-missing", "archived source path is unavailable")
        )
        return sorted(set(findings))
    if not _safe_path(archived_from):
        findings.append(
            _finding(path, "archive-source-path-invalid", "archived source path is not repository-safe")
        )
        return sorted(set(findings))
    resolved = _run_git(root, ["rev-parse", f"{commit}:{archived_from}"])
    if resolved.returncode != 0 or resolved.stdout.strip() != blob:
        findings.append(
            _finding(path, "archive-blob-mismatch", "commit path does not resolve to archived blob")
        )
        return sorted(set(findings))
    blob_bytes_result = _run_git(root, ["cat-file", "blob", blob], text=False)
    if blob_bytes_result.returncode != 0:
        findings.append(
            _finding(path, "archive-blob-invalid", "archived blob bytes are unavailable")
        )
        return sorted(set(findings))
    blob_sha256 = hashlib.sha256(blob_bytes_result.stdout).hexdigest()
    if preservation == "immutable-snapshot":
        expected_path = (
            f"docs/98.archive/evidence/{content_sha256}.md.snapshot"
            if isinstance(content_sha256, str)
            else None
        )
        if snapshot_path != expected_path or snapshot_path is None or not _safe_path(snapshot_path):
            findings.append(
                _finding(
                    path,
                    "archive-snapshot-path-mismatch",
                    "snapshot path is not the content-addressed canonical path",
                )
            )
            return sorted(set(findings))
        try:
            snapshot_bytes = (root / snapshot_path).read_bytes()
        except OSError:
            findings.append(
                _finding(path, "archive-snapshot-missing", "snapshot bytes are unavailable")
            )
            return sorted(set(findings))
        snapshot_sha256 = hashlib.sha256(snapshot_bytes).hexdigest()
        if (
            not isinstance(content_sha256, str)
            or snapshot_sha256 != content_sha256
            or blob_sha256 != content_sha256
        ):
            findings.append(
                _finding(
                    path,
                    "archive-content-sha256-mismatch",
                    "snapshot and archived blob do not match the declared digest",
                )
            )
        if any(pattern.search(snapshot_bytes) for pattern in SENSITIVE_PAYLOAD_PATTERNS):
            findings.append(
                _finding(
                    path,
                    "archive-snapshot-confidential",
                    "snapshot matches a prohibited confidentiality class",
                )
            )
    return sorted(set(findings))


def _approved_partition(record: Record) -> bool:
    partition = record.metadata.get("partition_plan")
    reviews = record.metadata.get("review_verdict")
    return (
        isinstance(partition, str)
        and _safe_path(partition)
        and partition.startswith("docs/04.execution/plans/")
        and isinstance(reviews, dict)
        and reviews.get("specification") == "pass"
        and reviews.get("quality") == "pass"
    )


def validate_directory_budgets(
    records: collections.abc.Sequence[Record],
    *,
    added_paths: frozenset[pathlib.PurePosixPath],
    warning_at: int,
    block_new_leaf_at: int,
    enforce_all: bool,
) -> list[Finding]:
    """Count only immediate document leaves and block additions at the hard limit."""

    counted = {
        record.path.as_posix(): record
        for record in records
        if record.path.suffix == ".md"
        and record.path.name != "README.md"
        and record.artifact_type not in {"generated", "repo-support", "unsupported"}
    }
    by_directory: dict[str, list[Record]] = collections.defaultdict(list)
    for record in counted.values():
        by_directory[record.path.parent.as_posix()].append(record)
    added = {path.as_posix() for path in added_paths}
    findings: list[Finding] = []
    for directory, members in sorted(by_directory.items()):
        count = len(members)
        if count >= warning_at:
            findings.append(
                _finding(
                    directory,
                    "directory-budget-warning",
                    f"immediate leaf count={count} warning_at={warning_at}",
                    "warning",
                )
            )
        blocking_members = (
            members
            if enforce_all
            else [record for record in members if record.path.as_posix() in added]
        )
        if count >= block_new_leaf_at and any(
            not _approved_partition(record) for record in blocking_members
        ):
            findings.append(
                _finding(
                    directory,
                    "directory-budget-blocked",
                    f"immediate leaf count={count} block_new_leaf_at={block_new_leaf_at}",
                )
            )
    return sorted(set(findings))


def _normalized_title(text: str) -> str | None:
    title = next(
        (line[2:].strip() for line in text.splitlines() if line.startswith("# ")),
        None,
    )
    if not title:
        return None
    normalized = TITLE_PUNCTUATION.sub("", title.casefold())
    return normalized or None


def find_duplicate_candidates(
    root: pathlib.Path,
    records: collections.abc.Sequence[Record],
) -> tuple[DuplicateCandidate, ...]:
    """Return same-type candidate signals without any disposition."""

    inspections: dict[str, tuple[bytes, str | None]] = {}
    for record in records:
        try:
            content = (root / record.path).read_bytes()
            text = content.decode("utf-8")
        except (OSError, UnicodeError):
            continue
        inspections[record.path.as_posix()] = (content, _normalized_title(text))
    candidates: list[DuplicateCandidate] = []
    ordered = sorted(records, key=lambda item: item.path.as_posix())
    for index, left in enumerate(ordered):
        left_inspection = inspections.get(left.path.as_posix())
        if left_inspection is None:
            continue
        for right in ordered[index + 1 :]:
            if left.artifact_type != right.artifact_type:
                continue
            right_inspection = inspections.get(right.path.as_posix())
            if right_inspection is None:
                continue
            signals: list[str] = []
            if left_inspection[0] == right_inspection[0]:
                signals.append("exact-content")
            if left_inspection[1] and left_inspection[1] == right_inspection[1]:
                signals.append("normalized-title")
            if signals:
                candidates.append(
                    DuplicateCandidate(
                        pathlib.PurePosixPath(left.path.as_posix()),
                        pathlib.PurePosixPath(right.path.as_posix()),
                        left.artifact_type,
                        tuple(sorted(signals)),
                    )
                )
    return tuple(sorted(candidates))


def render_archive_ledger(records: collections.abc.Sequence[Record]) -> str:
    """Render safe tombstone metadata only; never archive body bytes."""

    lines = [
        "# Generated Archive Ledger",
        "",
        "| Tombstone | Archived From | Disposition | Preservation | Commit | Blob |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for record in sorted(records, key=lambda item: item.path.as_posix()):
        if record.artifact_type != "archive":
            continue
        values = [
            record.path.as_posix(),
            _safe_archive_value(record, "archived_from") or "",
            _safe_archive_value(record, "archive_disposition") or "",
            _safe_archive_value(record, "preservation_class") or "",
            _safe_archive_value(record, "archived_commit") or "",
            _safe_archive_value(record, "archived_blob") or "",
        ]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines) + "\n"


def render_snapshot_manifest(records: collections.abc.Sequence[Record]) -> str:
    """Render safe immutable-snapshot identities only."""

    lines = [
        "# Generated Snapshot Manifest",
        "",
        "| Tombstone | Snapshot | SHA-256 | Archived Blob |",
        "| --- | --- | --- | --- |",
    ]
    for record in sorted(records, key=lambda item: item.path.as_posix()):
        if (
            record.artifact_type != "archive"
            or record.metadata.get("preservation_class") != "immutable-snapshot"
        ):
            continue
        values = [
            record.path.as_posix(),
            _safe_archive_value(record, "snapshot_path") or "",
            _safe_archive_value(record, "content_sha256") or "",
            _safe_archive_value(record, "archived_blob") or "",
        ]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines) + "\n"


def validate_exceptions(
    path: pathlib.Path,
    *,
    known_codes: frozenset[str],
    today: datetime.date,
) -> list[Finding]:
    """Validate future full-corpus exceptions as bounded, expiring evidence."""

    findings: list[Finding] = []
    label = path.name or "exceptions"
    try:
        loaded = metadata._safe_load_unique(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError):
        return [_finding(label, "exception-schema-invalid", "exception file cannot be parsed safely")]
    if not isinstance(loaded, dict) or set(loaded) != {"schema_version", "exceptions"}:
        return [_finding(label, "exception-schema-invalid", "exception file has invalid top-level fields")]
    if type(loaded.get("schema_version")) is not int or loaded.get("schema_version") != 1:
        findings.append(_finding(label, "exception-schema-invalid", "schema version must be 1"))
    entries = loaded.get("exceptions")
    if not isinstance(entries, list):
        return findings + [_finding(label, "exception-schema-invalid", "exceptions must be a list")]
    expected_field_order = tuple(metadata.EXPECTED_EXCEPTION_SCHEMA["entry_fields"])
    expected_fields = set(expected_field_order)
    previous_key: tuple[str, tuple[str, ...]] | None = None
    for index, entry in enumerate(entries):
        entry_path = f"{label}#{index}"
        if not isinstance(entry, dict):
            findings.append(
                _finding(entry_path, "exception-schema-invalid", "exception entry fields are invalid")
            )
            continue
        missing_fields = expected_fields - set(entry)
        for key, finding_code in (
            ("owner", "exception-owner-required"),
            ("reason", "exception-reason-required"),
            ("exit_condition", "exception-exit-condition-required"),
        ):
            if key in missing_fields:
                findings.append(
                    _finding(entry_path, finding_code, f"{key} must be present and non-empty")
                )
        if missing_fields or set(entry) - expected_fields:
            findings.append(
                _finding(entry_path, "exception-schema-invalid", "exception entry fields are invalid")
            )
            continue
        if tuple(entry) != expected_field_order:
            findings.append(
                _finding(entry_path, "exception-order-invalid", "exception fields are not canonical")
            )
        code = entry.get("finding_code")
        if not isinstance(code, str) or code not in known_codes:
            findings.append(
                _finding(entry_path, "exception-code-unknown", "finding code is not validator-known")
            )
        scopes = entry.get("scope_paths")
        valid_scopes = (
            isinstance(scopes, list)
            and bool(scopes)
            and all(
                isinstance(value, str)
                and _safe_path(value)
                and value not in {".", "all", "global"}
                for value in scopes
            )
            and scopes == sorted(set(scopes))
        )
        if not valid_scopes:
            findings.append(
                _finding(entry_path, "exception-scope-invalid", "scope paths must be bounded and deterministic")
            )
        for key, finding_code in (
            ("owner", "exception-owner-required"),
            ("reason", "exception-reason-required"),
            ("exit_condition", "exception-exit-condition-required"),
        ):
            if not isinstance(entry.get(key), str) or not str(entry.get(key)).strip():
                findings.append(
                    _finding(entry_path, finding_code, f"{key} must be non-empty")
                )
        approved = entry.get("approved_at")
        expires = entry.get("expires_on")
        try:
            approved_date = datetime.date.fromisoformat(approved) if isinstance(approved, str) else None
            expires_date = datetime.date.fromisoformat(expires) if isinstance(expires, str) else None
        except ValueError:
            approved_date = expires_date = None
        if approved_date is None or approved_date > today:
            findings.append(
                _finding(entry_path, "exception-approval-invalid", "approval date is invalid")
            )
        if expires_date is None or expires_date <= today:
            findings.append(
                _finding(entry_path, "exception-expired", "exception is expired or permanent")
            )
        elif approved_date is not None and expires_date <= approved_date:
            findings.append(
                _finding(entry_path, "exception-expiry-invalid", "expiry must be after approval")
            )
        evidence = entry.get("evidence")
        if not (
            isinstance(evidence, list)
            and bool(evidence)
            and evidence == sorted(set(evidence))
            and all(isinstance(value, str) and _safe_path(value) for value in evidence)
        ):
            findings.append(
                _finding(entry_path, "exception-evidence-invalid", "evidence paths are invalid")
            )
        if isinstance(code, str) and valid_scopes:
            order_key = (code, tuple(scopes))
            if previous_key is not None and order_key <= previous_key:
                findings.append(
                    _finding(entry_path, "exception-order-invalid", "exceptions are not uniquely ordered")
                )
            previous_key = order_key
    return sorted(set(findings))


def _review_findings(
    records: collections.abc.Sequence[Record],
    contract: dict[str, object],
    *,
    today: datetime.date,
) -> list[Finding]:
    signals = contract.get("review_signals")
    if not isinstance(signals, dict):
        return [_finding("contract", "contract-review-signals-invalid", "review signals are unavailable")]
    findings: list[Finding] = []
    for record in records:
        status = record.metadata.get("status")
        threshold: int | None = None
        if status == "draft":
            threshold = signals.get("draft_days")  # type: ignore[assignment]
        elif status == "active":
            threshold = signals.get("active_days")  # type: ignore[assignment]
        elif status == "completed" and record.artifact_type in {"plan", "task"}:
            threshold = signals.get("completed_execution_days")  # type: ignore[assignment]
        if not isinstance(threshold, int):
            continue
        reviewed_at = record.metadata.get("reviewed_at")
        if not isinstance(reviewed_at, (str, datetime.date)):
            findings.append(
                _finding(
                    record.path,
                    "review-age-unavailable",
                    "review age is unavailable because no real review evidence exists",
                    "warning",
                )
            )
            continue
        try:
            reviewed = (
                reviewed_at
                if isinstance(reviewed_at, datetime.date)
                else datetime.date.fromisoformat(reviewed_at)
            )
        except ValueError:
            continue
        if (today - reviewed).days >= threshold:
            findings.append(
                _finding(
                    record.path,
                    "review-due",
                    f"review evidence age reached configured threshold={threshold}",
                    "warning",
                )
            )
    return sorted(set(findings))


def _render_summary(document: MigrationManifestDocument) -> str:
    counts = collections.Counter(row.disposition for row in document.entries)
    lines = [
        "# Document Corpus Migration Summary",
        "",
        f"- Wave: `{document.wave}`",
        f"- Baseline commit: `{document.baseline_commit}`",
        f"- Enforcement: `{document.enforcement}`",
        f"- Entries: {len(document.entries)}",
        "",
        "## Dispositions",
        "",
    ]
    lines.extend(f"- `{name}`: {count}" for name, count in sorted(counts.items()))
    lines.extend(
        [
            "",
            "## Reviewed Paths",
            "",
            "| Source | Target | Disposition | Specification | Quality |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for row in sorted(document.entries, key=lambda item: item.source_path.as_posix()):
        lines.append(
            "| "
            + " | ".join(
                (
                    row.source_path.as_posix(),
                    _safe_path_text(row.target_path) or "",
                    row.disposition,
                    row.review_verdict.specification,
                    row.review_verdict.quality,
                )
            )
            + " |"
        )
    return "\n".join(lines) + "\n"


def _write_output(path: pathlib.Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def _check_output(path: pathlib.Path, content: str) -> bool:
    try:
        return path.read_bytes() == content.encode("utf-8")
    except OSError:
        return False


def _rooted(root: pathlib.Path, path: pathlib.Path) -> pathlib.Path:
    return path if path.is_absolute() else root / path


def _collect_records(root: pathlib.Path, profiles: dict[str, object]) -> tuple[Record, ...]:
    return tuple(metadata.collect_records(root, profiles, require_git=True))


def _introduced_metadata_findings(
    root: pathlib.Path,
    records: collections.abc.Sequence[Record],
    impacted: collections.abc.Sequence[Record],
    profiles: dict[str, object],
    *,
    base_ref: str,
) -> list[Finding]:
    baseline = _verified_commit(root, base_ref)
    if baseline is None:
        raise ProfileError("base_ref must resolve to a commit")
    base_records = tuple(metadata.collect_records_at_ref(root, profiles, baseline))
    base_by_path = {record.path.as_posix(): record for record in base_records}
    base_manifest = metadata.build_manifest(base_records)
    current_manifest = metadata.build_manifest(records)
    introduced: list[Finding] = []
    for record in impacted:
        prior = base_by_path.get(record.path.as_posix())
        previous_status = (
            prior.metadata.get("status")
            if prior is not None and isinstance(prior.metadata.get("status"), str)
            else None
        )
        current_record = dataclasses.replace(record, previous_status=previous_status)
        current_findings = metadata.validate_record(current_record, profiles, current_manifest)
        prior_keys = (
            {
                (finding.code, finding.message, finding.severity)
                for finding in metadata.validate_record(prior, profiles, base_manifest)
            }
            if prior is not None
            else set()
        )
        introduced.extend(
            finding
            for finding in current_findings
            if finding.severity == "error"
            and (finding.code, finding.message, finding.severity) not in prior_keys
        )
    return sorted(set(introduced))


def _load_declared_manifests(
    root: pathlib.Path,
    profiles: dict[str, object],
    contract: dict[str, object],
    *,
    promoted_only: bool,
) -> tuple[tuple[MigrationManifestDocument, ...], list[Finding]]:
    documents: list[MigrationManifestDocument] = []
    findings: list[Finding] = []
    waves = contract.get("waves")
    if not isinstance(waves, dict):
        raise ProfileError("contract waves must be a mapping")
    for wave_name, raw_wave in waves.items():
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
        if not absolute.is_file():
            findings.append(
                _finding(manifest_path, "promoted-manifest-missing", "declared manifest does not exist")
            )
            continue
        document = load_migration_manifest(absolute)
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
        findings.extend(validate_migration_manifest(root, profiles, contract, document))
        if not _check_output(absolute, render_migration_manifest(document)):
            findings.append(
                _finding(manifest_path, "manifest-serialization-stale", "manifest bytes are not canonical")
            )
        documents.append(document)
    return tuple(documents), sorted(set(findings))


def _full_findings(
    root: pathlib.Path,
    profiles: dict[str, object],
    contract: dict[str, object],
) -> tuple[tuple[Record, ...], list[Finding]]:
    records = _collect_records(root, profiles)
    manifest = metadata.build_manifest(records)
    findings: list[Finding] = []
    for record in records:
        findings.extend(metadata.validate_record(record, profiles, manifest))
        findings.extend(validate_archive_provenance(root, record))
    budgets = contract.get("directory_budgets")
    if not isinstance(budgets, dict):
        raise ProfileError("directory budget contract is invalid")
    findings.extend(
        validate_directory_budgets(
            records,
            added_paths=frozenset(),
            warning_at=int(budgets["warning_at"]),
            block_new_leaf_at=int(budgets["block_new_leaf_at"]),
            enforce_all=False,
        )
    )
    findings.extend(_review_findings(records, contract, today=datetime.date.today()))
    return records, sorted(set(findings))


def _is_safety_finding(finding: Finding) -> bool:
    return any(part in finding.code for part in SAFETY_CODE_PARTS)


def _print_findings(findings: collections.abc.Sequence[Finding]) -> None:
    for finding in sorted(set(findings)):
        print(f"{finding.code}: {finding.path}: {finding.message}")


def _validate_cli_shape(parser: argparse.ArgumentParser, args: argparse.Namespace) -> None:
    requirements: dict[str, tuple[set[str], set[str]]] = {
        "check-contract": (set(), {"wave", "base_ref", "manifest", "exceptions", "output"}),
        "generate-manifest": ({"wave", "base_ref", "output"}, {"manifest", "exceptions"}),
        "check-manifest": ({"wave", "manifest"}, {"base_ref", "exceptions", "output"}),
        "check-promoted": (set(), {"wave", "base_ref", "manifest", "exceptions", "output"}),
        "generate-summary": ({"manifest", "output"}, {"wave", "base_ref", "exceptions"}),
        "check-summary": ({"manifest", "output"}, {"wave", "base_ref", "exceptions"}),
        "check-impacted": ({"base_ref"}, {"wave", "manifest", "exceptions", "output"}),
        "report-duplicates": ({"output"}, {"wave", "base_ref", "manifest", "exceptions"}),
        "report-full": (set(), {"wave", "base_ref", "manifest", "exceptions", "output"}),
        "check-full": (set(), {"wave", "base_ref", "manifest", "output"}),
        "check-archive": (set(), {"wave", "base_ref", "manifest", "exceptions", "output"}),
        "check-directory-budget": (set(), {"wave", "base_ref", "manifest", "exceptions", "output"}),
        "generate-archive-ledger": ({"output"}, {"wave", "base_ref", "manifest", "exceptions"}),
        "check-archive-ledger": ({"output"}, {"wave", "base_ref", "manifest", "exceptions"}),
        "generate-snapshot-manifest": ({"output"}, {"wave", "base_ref", "manifest", "exceptions"}),
        "check-snapshot-manifest": ({"output"}, {"wave", "base_ref", "manifest", "exceptions"}),
    }
    required, forbidden = requirements[args.mode]
    for name in sorted(required):
        if getattr(args, name) is None:
            parser.error(f"--{name.replace('_', '-')} is required for --mode {args.mode}")
    for name in sorted(forbidden):
        if getattr(args, name) is not None:
            parser.error(f"--{name.replace('_', '-')} is forbidden for --mode {args.mode}")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=pathlib.Path, default=ROOT)
    parser.add_argument("--profiles", type=pathlib.Path, default=DEFAULT_PROFILES)
    parser.add_argument("--contract", type=pathlib.Path, default=DEFAULT_CONTRACT)
    parser.add_argument("--mode", required=True, choices=MODES)
    parser.add_argument("--wave")
    parser.add_argument("--base-ref")
    parser.add_argument("--manifest", type=pathlib.Path)
    parser.add_argument("--exceptions", type=pathlib.Path)
    parser.add_argument("--output", type=pathlib.Path)
    return parser


def main(argv: collections.abc.Sequence[str] | None = None) -> int:
    parser = _parser()
    args = parser.parse_args(argv)
    _validate_cli_shape(parser, args)
    root = args.root.resolve()
    try:
        contract_path = _rooted(root, args.contract).resolve()
        profiles_path = _rooted(root, args.profiles).resolve()
        contract = load_migration_contract(contract_path)
        profiles = metadata.load_profiles(profiles_path, contract_path)
        if args.mode == "check-contract":
            print("document corpus lifecycle contract: violations=0")
            return 0
        if args.mode == "generate-manifest":
            document = generate_manifest_skeleton(
                root, contract, wave=args.wave, baseline_ref=args.base_ref
            )
            _write_output(_rooted(root, args.output), render_migration_manifest(document))
            print(f"manifest generated: entries={len(document.entries)}")
            return 0
        if args.mode == "check-manifest":
            manifest_path = _rooted(root, args.manifest).resolve()
            document = load_migration_manifest(manifest_path)
            findings = validate_migration_manifest(root, profiles, contract, document)
            if document.wave != args.wave:
                findings.append(
                    _finding(args.manifest.as_posix(), "manifest-wave-mismatch", "--wave differs from manifest")
                )
            if not _check_output(manifest_path, render_migration_manifest(document)):
                findings.append(
                    _finding(args.manifest.as_posix(), "manifest-serialization-stale", "manifest bytes are not canonical")
                )
            _print_findings(findings)
            return 3 if any(_is_safety_finding(item) for item in findings) else (1 if findings else 0)
        if args.mode == "check-promoted":
            _, findings = _load_declared_manifests(
                root, profiles, contract, promoted_only=True
            )
            _print_findings(findings)
            print(f"promoted lifecycle manifests: violations={len(findings)}")
            return 3 if any(_is_safety_finding(item) for item in findings) else (1 if findings else 0)
        if args.mode in {"generate-summary", "check-summary"}:
            manifest_path = _rooted(root, args.manifest).resolve()
            document = load_migration_manifest(manifest_path)
            manifest_findings = validate_migration_manifest(root, profiles, contract, document)
            if not _check_output(manifest_path, render_migration_manifest(document)):
                manifest_findings.append(
                    _finding(
                        manifest_path.as_posix(),
                        "manifest-serialization-stale",
                        "manifest bytes are not canonical",
                    )
                )
            if manifest_findings:
                _print_findings(manifest_findings)
                return 3 if any(_is_safety_finding(item) for item in manifest_findings) else 1
            rendered = _render_summary(document)
            output_path = _rooted(root, args.output)
            if args.mode == "generate-summary":
                _write_output(output_path, rendered)
                return 0
            if not _check_output(output_path, rendered):
                print(f"summary-stale: {output_path}")
                return 1
            return 0
        if args.mode == "check-impacted":
            documents, manifest_findings = _load_declared_manifests(
                root, profiles, contract, promoted_only=False
            )
            if manifest_findings:
                _print_findings(manifest_findings)
                return 3 if any(_is_safety_finding(item) for item in manifest_findings) else 1
            records = _collect_records(root, profiles)
            impacted = collect_impacted_records(
                root, records, profiles, contract, documents, base_ref=args.base_ref
            )
            findings = _introduced_metadata_findings(
                root,
                records,
                impacted,
                profiles,
                base_ref=args.base_ref,
            )
            budgets = contract.get("directory_budgets")
            if not isinstance(budgets, dict):
                raise ProfileError("directory budget contract is invalid")
            findings.extend(
                validate_directory_budgets(
                    _apply_partition_approvals(records, documents),
                    added_paths=_added_record_paths(root, args.base_ref),
                    warning_at=int(budgets["warning_at"]),
                    block_new_leaf_at=int(budgets["block_new_leaf_at"]),
                    enforce_all=False,
                )
            )
            _print_findings(findings)
            blocking = [item for item in findings if item.severity == "error"]
            print(f"lifecycle impacted: selected={len(impacted)} violations={len(blocking)}")
            return 3 if any(_is_safety_finding(item) for item in blocking) else (1 if blocking else 0)
        records, full_findings = _full_findings(root, profiles, contract)
        if args.mode == "report-duplicates":
            safety = [item for item in full_findings if _is_safety_finding(item)]
            if safety:
                _print_findings(safety)
                return 3
            candidates = find_duplicate_candidates(root, records)
            rendered = yaml.safe_dump(
                {
                    "schema_version": 1,
                    "candidates": [
                        {
                            "left_path": item.left_path.as_posix(),
                            "right_path": item.right_path.as_posix(),
                            "artifact_type": item.artifact_type,
                            "signals": list(item.signals),
                        }
                        for item in candidates
                    ],
                },
                sort_keys=False,
                width=1000,
            )
            _write_output(_rooted(root, args.output), rendered)
            print(f"duplicate candidates: count={len(candidates)}")
            return 0
        if args.mode in {"generate-archive-ledger", "check-archive-ledger"}:
            archive_paths = {
                record.path.as_posix() for record in records if record.artifact_type == "archive"
            }
            archive_findings = [
                item
                for item in full_findings
                if item.path in archive_paths and item.severity == "error"
            ]
            if archive_findings:
                _print_findings(archive_findings)
                return 3 if any(_is_safety_finding(item) for item in archive_findings) else 1
            rendered = render_archive_ledger(records)
            if args.mode.startswith("generate-"):
                _write_output(_rooted(root, args.output), rendered)
                return 0
            return 0 if _check_output(_rooted(root, args.output), rendered) else 1
        if args.mode in {"generate-snapshot-manifest", "check-snapshot-manifest"}:
            archive_paths = {
                record.path.as_posix() for record in records if record.artifact_type == "archive"
            }
            archive_findings = [
                item
                for item in full_findings
                if item.path in archive_paths and item.severity == "error"
            ]
            if archive_findings:
                _print_findings(archive_findings)
                return 3 if any(_is_safety_finding(item) for item in archive_findings) else 1
            rendered = render_snapshot_manifest(records)
            if args.mode.startswith("generate-"):
                _write_output(_rooted(root, args.output), rendered)
                return 0
            return 0 if _check_output(_rooted(root, args.output), rendered) else 1
        if args.mode == "check-archive":
            findings = [
                finding
                for record in records
                for finding in validate_archive_provenance(root, record)
            ]
        elif args.mode == "check-directory-budget":
            budgets = contract.get("directory_budgets")
            if not isinstance(budgets, dict):
                raise ProfileError("directory budget contract is invalid")
            findings = validate_directory_budgets(
                records,
                added_paths=frozenset(),
                warning_at=int(budgets["warning_at"]),
                block_new_leaf_at=int(budgets["block_new_leaf_at"]),
                enforce_all=True,
            )
        else:
            findings = list(full_findings)
        if args.mode == "check-full":
            budgets = contract.get("directory_budgets")
            if not isinstance(budgets, dict):
                raise ProfileError("directory budget contract is invalid")
            findings = [
                item for item in findings if not item.code.startswith("directory-budget-")
            ]
            findings.extend(
                validate_directory_budgets(
                    records,
                    added_paths=frozenset(),
                    warning_at=int(budgets["warning_at"]),
                    block_new_leaf_at=int(budgets["block_new_leaf_at"]),
                    enforce_all=True,
                )
            )
        if args.mode == "check-full" and args.exceptions is not None:
            known_codes = frozenset({item.code for item in findings}) | KNOWN_FINDING_CODES
            exception_findings = validate_exceptions(
                _rooted(root, args.exceptions).resolve(), known_codes=known_codes, today=datetime.date.today()
            )
            findings.extend(exception_findings)
            if not exception_findings:
                loaded = metadata._safe_load_unique(
                    _rooted(root, args.exceptions).read_text(encoding="utf-8")
                )
                suppressed = {
                    (entry["finding_code"], scope)
                    for entry in loaded["exceptions"]
                    for scope in entry["scope_paths"]
                }
                findings = [
                    item
                    for item in findings
                    if item.code.startswith("exception-")
                    or (item.code, item.path) not in suppressed
                ]
        _print_findings(findings)
        if args.mode == "report-full":
            safety = [item for item in findings if _is_safety_finding(item)]
            print(f"lifecycle full report: findings={len(findings)} safety_failures={len(safety)}")
            return 3 if safety else 0
        blocking = [item for item in findings if item.severity == "error"]
        return 3 if any(_is_safety_finding(item) for item in blocking) else (1 if blocking else 0)
    except ProfileError as error:
        print(f"configuration-error: {error}", file=sys.stderr)
        return 3
    except (OSError, UnicodeError, yaml.YAMLError):
        print("internal-error: lifecycle operation failed safely", file=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
