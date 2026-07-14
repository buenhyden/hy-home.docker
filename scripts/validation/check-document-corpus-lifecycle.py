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
import os
import pathlib
import re
import secrets
import stat
import subprocess
import sys
import unicodedata
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


class _BootstrapProfileError(ValueError):
    """Used only until the canonical metadata module is loaded safely."""


class _CorpusSafetyError(Exception):
    """Value-free corpus path failure that must cross the CLI safety boundary."""

    def __init__(self, path: str, code: str) -> None:
        super().__init__(code)
        self.path = path if path and _lexically_safe_path(path) else "corpus"
        self.code = code


metadata: Any = None
Finding: Any = None
Record: Any = None
ProfileError: type[Exception] = _BootstrapProfileError

_CORPUS_SNAPSHOT_ROOT: pathlib.Path | None = None
_CORPUS_SNAPSHOT_BYTES: dict[str, bytes] = {}


def _ensure_metadata_loaded() -> Any:
    """Load repository-backed metadata only after CLI-shape validation."""

    global metadata, Finding, Record, ProfileError
    if metadata is None:
        metadata = _load_metadata_module()
        Finding = metadata.Finding
        Record = metadata.Record
        ProfileError = metadata.ProfileError
    return metadata


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
SENSITIVE_PAYLOAD_PATTERNS = (
    re.compile(rb"(?i)(?:password|passwd|credential|secret|token|access[_-]?token|refresh[_-]?token|api[_-]?key)\s*[:=]"),
    re.compile(rb"(?i)(?:auth|authorization)\s*[:=]\s*(?:bearer|basic|[A-Za-z0-9+/]{16,})"),
    re.compile(rb"(?is)\bmachine\s+\S+.{0,512}\blogin\s+\S+.{0,512}\bpassword\s+\S+"),
    re.compile(rb'(?i)"auths?"\s*:\s*\{|"auth"\s*:\s*"[A-Za-z0-9+/=_-]{8,}"'),
    re.compile(rb"\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b"),
    re.compile(rb"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(rb"\bsk-[A-Za-z0-9_-]{12,}\b"),
    re.compile(rb"\bgh[pousr]_[A-Za-z0-9_]{12,}\b"),
    re.compile(rb"\bxox[baprs]-[A-Za-z0-9-]{12,}\b"),
    re.compile(rb"-----BEGIN [A-Z0-9 ]*(?:PRIVATE KEY|PGP PRIVATE KEY BLOCK)-----"),
    re.compile(rb"(?i)(?:^|/|\\)\.(?:bash|zsh|sh)_history(?:\s|$)|\bHISTFILE\s*="),
    re.compile(rb"(?m)^\d{4}-\d{2}-\d{2}(?:T|\s).*(?:ERROR|WARN|DEBUG|TRACE)\b"),
    re.compile(rb"(?mi)^(?:TRACE|DEBUG|INFO|WARN|ERROR|FATAL)\b"),
    re.compile(rb'(?is)"(?:timestamp|time|ts)"\s*:\s*"[^"]+".{0,512}"level"\s*:\s*"(?:trace|debug|info|warn|error|fatal)"'),
    re.compile(rb'(?is)\{.{0,512}"level"\s*:\s*"(?:trace|debug|info|warn|error|fatal)"'),
    re.compile(rb"(?m)^(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}\s+\S+\s+\S+(?:\[\d+\])?:"),
)
SAFETY_FINDING_CODES = frozenset(
    {
        "manifest-static-invalid",
        "manifest-source-path-invalid",
        "manifest-source-not-at-baseline",
        "manifest-source-mode-invalid",
        "manifest-source-parse-invalid",
        "manifest-target-path-invalid",
        "manifest-target-file-invalid",
        "manifest-consumer-path-invalid",
        "manifest-evidence-path-invalid",
        "manifest-partition-plan-invalid",
        "corpus-markdown-path-invalid",
        "corpus-markdown-mode-invalid",
        "corpus-markdown-file-invalid",
        "manifest-baseline-commit-invalid",
        "manifest-serialization-stale",
        "promoted-manifest-path-invalid",
        "promoted-manifest-file-invalid",
        "archive-commit-invalid",
        "archive-blob-invalid",
        "archive-blob-mismatch",
        "archive-source-path-invalid",
        "archive-snapshot-path-mismatch",
        "archive-snapshot-file-invalid",
        "archive-snapshot-missing",
        "archive-content-sha256-mismatch",
        "archive-snapshot-confidential",
        "archive-snapshot-forbidden",
        "invalid-archived-commit",
        "invalid-archived-blob",
        "invalid-snapshot-path",
        "invalid-content-sha256",
        "archive-snapshot-disposition-forbidden",
        "manifest-archive-baseline-blob-mismatch",
        "frontmatter-malformed-yaml",
        "frontmatter-duplicate-key",
        "exception-schema-invalid",
        "exception-order-invalid",
        "exception-code-unknown",
        "exception-scope-invalid",
        "exception-owner-required",
        "exception-reason-required",
        "exception-exit-condition-required",
        "exception-approval-invalid",
        "exception-expired",
        "exception-expiry-invalid",
        "exception-evidence-invalid",
        "exception-static-invalid",
        "exception-safety-code-forbidden",
        "contract-invalid",
        "diagnostic-redaction-unsafe",
        "internal-error",
    }
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
        "manifest-replacement-invalid",
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


def _lexically_safe_path(value: object) -> bool:
    if (
        not isinstance(value, str)
        or not value
        or "\\" in value
        or "|" in value
        or any(ord(character) < 32 or ord(character) == 127 for character in value)
    ):
        return False
    path = pathlib.PurePosixPath(value)
    return (
        not path.is_absolute()
        and bool(path.parts)
        and all(part not in {"", ".", ".."} for part in path.parts)
    )


def _open_regular_repo_descriptor(root: pathlib.Path, relative_path: str) -> int | None:
    """Open one in-root regular file without following any path component."""

    if not _lexically_safe_path(relative_path):
        return None
    parts = pathlib.PurePosixPath(relative_path).parts
    directory_flags = (
        os.O_RDONLY
        | getattr(os, "O_DIRECTORY", 0)
        | getattr(os, "O_NOFOLLOW", 0)
    )
    file_flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    parent_descriptor: int | None = None
    descriptor: int | None = None
    try:
        parent_descriptor = os.open(root.resolve(), directory_flags)
        for part in parts[:-1]:
            child_descriptor = os.open(
                part,
                directory_flags,
                dir_fd=parent_descriptor,
            )
            os.close(parent_descriptor)
            parent_descriptor = child_descriptor
        descriptor = os.open(parts[-1], file_flags, dir_fd=parent_descriptor)
        opened = os.fstat(descriptor)
        if not stat.S_ISREG(opened.st_mode):
            os.close(descriptor)
            descriptor = None
        return descriptor
    except OSError:
        if descriptor is not None:
            os.close(descriptor)
        return None
    finally:
        if parent_descriptor is not None:
            os.close(parent_descriptor)


def _read_regular_repo_bytes(
    root: pathlib.Path,
    relative_path: str,
    *,
    require_tracked: bool,
) -> bytes | None:
    """Read a regular in-root file through a no-follow directory-fd chain."""

    if not _safe_path(relative_path):
        return None
    if require_tracked:
        tracked = _run_git(
            root,
            ["ls-files", "--stage", "-z", "--", relative_path],
            text=False,
        )
        if tracked.returncode != 0 or not tracked.stdout:
            return None
        modes = {
            record.split(b" ", 1)[0]
            for record in tracked.stdout.split(b"\0")
            if record
        }
        if not modes or not modes <= {b"100644", b"100755"}:
            return None
    descriptor = _open_regular_repo_descriptor(root, relative_path)
    if descriptor is None:
        return None
    try:
        chunks: list[bytes] = []
        while True:
            chunk = os.read(descriptor, 1024 * 1024)
            if not chunk:
                break
            chunks.append(chunk)
        return b"".join(chunks)
    except OSError:
        return None
    finally:
        os.close(descriptor)


def _baseline_regular_blob(root: pathlib.Path, commit: str, path: str) -> bool:
    """Return whether an exact baseline path is a regular Git blob entry."""

    if not _safe_path(path):
        return False
    result = _run_git(root, ["ls-tree", "-z", commit, "--", path], text=False)
    if result.returncode != 0 or not result.stdout:
        return False
    entries = [entry for entry in result.stdout.split(b"\0") if entry]
    if len(entries) != 1 or b"\t" not in entries[0]:
        return False
    raw_header, raw_path = entries[0].split(b"\t", 1)
    header = raw_header.split()
    try:
        entry_path = raw_path.decode("utf-8")
        object_id = header[2].decode("ascii") if len(header) == 3 else ""
    except UnicodeDecodeError:
        return False
    return (
        len(header) == 3
        and header[0] in {b"100644", b"100755"}
        and header[1] == b"blob"
        and entry_path == path
        and bool(OBJECT_ID.fullmatch(object_id))
        and _git_object_type(root, object_id) == "blob"
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


def _load_migration_manifest_text(source: str) -> MigrationManifestDocument:
    try:
        loaded = metadata._safe_load_unique(source)
    except yaml.YAMLError as error:
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


def load_migration_manifest(path: pathlib.Path) -> MigrationManifestDocument:
    """Load an exact, duplicate-key-safe migration manifest."""

    try:
        source = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise ProfileError("cannot load migration manifest safely") from error
    return _load_migration_manifest_text(source)


def _load_repo_migration_manifest(
    root: pathlib.Path,
    relative_path: str,
) -> MigrationManifestDocument:
    payload = _read_regular_repo_bytes(root, relative_path, require_tracked=True)
    if payload is None:
        raise ProfileError("repository manifest must be a tracked regular in-root file")
    try:
        source = payload.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ProfileError("repository manifest must be UTF-8") from error
    return _load_migration_manifest_text(source)


def _load_candidate_migration_manifest(
    root: pathlib.Path,
    relative_path: str,
) -> MigrationManifestDocument:
    """Load a safe in-root candidate without requiring prior Git staging."""

    payload = _read_regular_repo_bytes(root, relative_path, require_tracked=False)
    if payload is None:
        raise ProfileError("candidate manifest must be a regular in-root file")
    try:
        source = payload.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ProfileError("candidate manifest must be UTF-8") from error
    return _load_migration_manifest_text(source)


def _repo_manifest_path(root: pathlib.Path, path: pathlib.Path) -> str:
    """Return a safe repository-relative manifest path without resolving links."""

    resolved_root = root.resolve()
    if any(part == ".." for part in path.parts):
        raise ProfileError("manifest path must not traverse parent directories")
    candidate = path if path.is_absolute() else resolved_root / path
    try:
        relative = candidate.relative_to(resolved_root).as_posix()
    except ValueError as error:
        raise ProfileError("manifest path must remain inside the repository") from error
    if not _safe_path(relative):
        raise ProfileError("manifest path must be repository-safe")
    return relative


def _repo_manifest_matches(
    root: pathlib.Path,
    relative_path: str,
    expected: str,
) -> bool:
    payload = _read_regular_repo_bytes(root, relative_path, require_tracked=True)
    return payload == expected.replace("\r\n", "\n").encode("utf-8")


def _candidate_manifest_matches(
    root: pathlib.Path,
    relative_path: str,
    expected: str,
) -> bool:
    """Compare canonical bytes for a safe candidate before it is staged."""

    payload = _read_regular_repo_bytes(root, relative_path, require_tracked=False)
    return payload == expected.replace("\r\n", "\n").encode("utf-8")


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


def _manifest_artifact_id(artifact_type: str, value: object) -> str | None:
    """Project template placeholders to null without hiding concrete identities."""

    if artifact_type == "template-source" and value == "<artifact-id>":
        return None
    return value if isinstance(value, str) else None


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
        status = frontmatter.get("status")
        rows.append(
            MigrationManifestRow(
                source_path=pathlib.PurePosixPath(source_path),
                target_path=pathlib.PurePosixPath(source_path),
                artifact_id=_manifest_artifact_id(
                    artifact_type, frontmatter.get("artifact_id")
                ),
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


def _blob_at_commit_path(root: pathlib.Path, commit: str, path: str) -> str | None:
    """Resolve one verified regular blob identity without reading its payload."""

    if not _safe_path(path) or not _baseline_regular_blob(root, commit, path):
        return None
    result = _run_git(root, ["rev-parse", f"{commit}:{path}"])
    object_id = result.stdout.strip() if result.returncode == 0 else ""
    return object_id if OBJECT_ID.fullmatch(object_id) else None


def _canonical_current_snapshot(
    root: pathlib.Path,
    profiles: dict[str, object],
) -> tuple[tuple[Record, ...], dict[str, bytes]]:
    """Return one tracked, no-follow corpus snapshot for canonical proofs."""

    return _safe_corpus_snapshot(root, profiles, include_untracked=False)


def _resolve_canonical_replacement(
    profiles: dict[str, object],
    *,
    source: str,
    target: str | None,
    replacement: str,
    disposition: str,
    records: collections.abc.Sequence[Record],
    payloads: collections.abc.Mapping[str, bytes],
) -> tuple[Record | None, list[Finding]]:
    """Resolve one unique current canonical replacement from held corpus bytes."""

    candidates: list[Record] = []
    by_path = {record.path.as_posix(): record for record in records}
    path_candidate = by_path.get(replacement) if _safe_path(replacement) else None
    if path_candidate is not None:
        candidates = [path_candidate]
    else:
        candidates = [
            record
            for record in records
            if record.metadata.get("artifact_id") == replacement
        ]
    if len(candidates) != 1:
        return None, [
            _finding(
                source,
                "manifest-replacement-invalid",
                "canonical replacement must resolve uniquely",
            )
        ]
    candidate = candidates[0]
    candidate_path = candidate.path.as_posix()
    if disposition == "merge" and (
        target is None
        or candidate_path != target
    ):
        return None, [
            _finding(
                source,
                "manifest-replacement-invalid",
                "merge replacement must be the selected canonical result",
            )
        ]
    if disposition != "merge" and candidate_path in {
        value for value in (source, target) if value is not None
    }:
        return None, [
            _finding(
                source,
                "manifest-replacement-invalid",
                "canonical replacement must be distinct from the removed source and archive target",
            )
        ]
    if (
        candidate.artifact_type
        in {"archive", "generated", "readme", "repo-support", "template-source", "unsupported"}
        or candidate.metadata.get("status") not in {"active", "completed"}
    ):
        return None, [
            _finding(
                source,
                "manifest-replacement-invalid",
                "canonical replacement is not an eligible current document",
            )
        ]
    payload = payloads.get(candidate_path)
    if payload is None:
        return None, [
            _finding(
                source,
                "manifest-replacement-invalid",
                "canonical replacement is not in the held tracked corpus",
            )
        ]
    try:
        text = payload.decode("utf-8")
    except UnicodeDecodeError:
        return None, [
            _finding(
                source,
                "manifest-replacement-invalid",
                "canonical replacement is not valid UTF-8",
            )
        ]
    manifest = metadata.build_manifest(records)
    errors = [
        finding
        for finding in (
            *metadata.validate_record(candidate, profiles, manifest),
            *metadata.validate_body_contract(candidate, text, profiles, True),
        )
        if finding.severity == "error"
    ]
    if errors:
        return None, [
            _finding(
                source,
                "manifest-replacement-invalid",
                "canonical replacement fails its metadata or body contract",
            )
        ]
    return candidate, []


def _canonical_replacement_findings(
    profiles: dict[str, object],
    *,
    source: str,
    target: str | None,
    replacement: str,
    disposition: str,
    artifact_id: str | None,
    records: collections.abc.Sequence[Record],
    payloads: collections.abc.Mapping[str, bytes],
) -> list[Finding]:
    """Return canonical replacement findings while preserving the fixed helper call shape."""

    del artifact_id
    _, findings = _resolve_canonical_replacement(
        profiles,
        source=source,
        target=target,
        replacement=replacement,
        disposition=disposition,
        records=records,
        payloads=payloads,
    )
    return findings


def _baseline_merge_owner_findings(
    *,
    root: pathlib.Path,
    profiles: dict[str, object],
    baseline: str,
    row: MigrationManifestRow,
    target: str,
    replacement: Record,
    baseline_records: collections.abc.Sequence[Record],
    entries: collections.abc.Sequence[MigrationManifestRow],
) -> list[Finding]:
    """Bind a distinct merge replacement identity to one baseline owner."""

    replacement_id = replacement.metadata.get("artifact_id")
    if not isinstance(replacement_id, str) or replacement_id == row.artifact_id:
        return []
    owners = [
        record
        for record in baseline_records
        if record.metadata.get("artifact_id") == replacement_id
    ]
    if len(owners) != 1:
        return [
            _finding(
                target,
                "manifest-replacement-invalid",
                "merge replacement identity must have one baseline owner",
            )
        ]
    owner = owners[0]
    owner_path = owner.path.as_posix()
    if not _baseline_regular_blob(root, baseline, owner_path):
        return [
            _finding(
                target,
                "manifest-replacement-invalid",
                "merge replacement baseline owner is not a regular tracked blob",
            )
        ]
    declared_owner_type = owner.metadata.get("artifact_type")
    baseline_status = owner.metadata.get("status")
    current_status = replacement.metadata.get("status")
    if (
        declared_owner_type != owner.artifact_type
        or owner.artifact_type != replacement.artifact_type
        or not isinstance(baseline_status, str)
        or not isinstance(current_status, str)
    ):
        return [
            _finding(
                target,
                "manifest-replacement-invalid",
                "merge replacement baseline owner differs in type or lifecycle truth",
            )
        ]
    if owner_path == target:
        if baseline_status == current_status:
            return []

    common = profiles.get("common")
    transitions = common.get("transitions") if isinstance(common, dict) else None
    allowed_next = (
        transitions.get(baseline_status)
        if isinstance(transitions, dict)
        else None
    )
    transition_valid = baseline_status == current_status or (
        isinstance(allowed_next, list) and current_status in allowed_next
    )

    def complete_attestation(candidate: MigrationManifestRow) -> bool:
        evidence_complete = all(
            values
            for values in (
                candidate.evidence.commands,
                candidate.evidence.sources,
                candidate.evidence.repository_paths,
                candidate.evidence.consumer_scan,
                candidate.evidence.rollback,
            )
        )
        if owner_path == target:
            disposition_valid = candidate.disposition == "migrate"
        else:
            disposition_valid = candidate.disposition in {"move", "merge"}
        return (
            candidate.source_path.as_posix() == owner_path
            and candidate.target_path is not None
            and candidate.target_path.as_posix() == target
            and candidate.artifact_id == replacement_id
            and candidate.artifact_type == owner.artifact_type
            and candidate.status_before == baseline_status
            and candidate.status_after == current_status
            and candidate.canonical_replacement is None
            and disposition_valid
            and transition_valid
            and evidence_complete
            and candidate.review_verdict == ReviewVerdict("pass", "pass")
        )

    attestations = [
        candidate
        for candidate in entries
        if complete_attestation(candidate)
    ]
    if len(attestations) == 1:
        return []
    return [
        _finding(
            target,
            "manifest-replacement-invalid",
            "merge replacement baseline owner is not uniquely attested to the selected result",
        )
    ]


def _held_result_snapshot(
    root: pathlib.Path,
    document: MigrationManifestDocument,
    records: collections.abc.Sequence[Record],
    payloads: collections.abc.Mapping[str, bytes],
) -> tuple[tuple[Record, ...], dict[str, bytes]]:
    """Add every safe manifest result target to one held current snapshot."""

    records_by_path = {record.path.as_posix(): record for record in records}
    result_payloads = dict(payloads)
    for row in document.entries:
        target = _safe_path_text(row.target_path)
        if target is None or not _safe_path(target) or target in result_payloads:
            continue
        payload = _read_regular_repo_bytes(root, target, require_tracked=False)
        if payload is None:
            if os.path.lexists(root / target):
                raise _CorpusSafetyError(target, "corpus-markdown-file-invalid")
            continue
        try:
            text = payload.decode("utf-8")
        except UnicodeDecodeError:
            continue
        result_payloads[target] = payload
        records_by_path[target] = metadata._record_from_text(
            pathlib.Path(target), text
        )
    return (
        tuple(records_by_path[path] for path in sorted(records_by_path)),
        result_payloads,
    )


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
                            pathlib.Path(target), target_text
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
                            or target_metadata.get("artifact_type") != "archive"
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
    return sorted(set(findings))


def _changed_path_sets(root: pathlib.Path, base_ref: str) -> tuple[set[str], set[str]]:
    """Return current changed paths and all relation-trigger paths NUL-safely."""

    baseline = _verified_commit(root, base_ref)
    if baseline is None:
        raise ProfileError("base_ref must resolve to a commit")
    changed = _run_git(
        root,
        [
            "diff",
            "--name-status",
            "-z",
            "--find-renames",
            baseline,
            "--",
            "*.md",
        ],
        text=False,
    )
    untracked = _run_git(
        root,
        ["ls-files", "-z", "--others", "--exclude-standard", "--", "*.md"],
        text=False,
    )
    if changed.returncode != 0 or untracked.returncode != 0:
        raise ProfileError("cannot determine impacted Markdown paths")
    try:
        tokens = [token.decode("utf-8") for token in changed.stdout.split(b"\0") if token]
        untracked_paths = [
            token.decode("utf-8") for token in untracked.stdout.split(b"\0") if token
        ]
    except UnicodeDecodeError as error:
        raise ProfileError("impacted Markdown paths are not UTF-8") from error
    current_paths: set[str] = set()
    trigger_paths: set[str] = set()
    index = 0
    while index < len(tokens):
        status_code = tokens[index]
        index += 1
        if status_code.startswith(("R", "C")):
            if index + 1 >= len(tokens):
                raise ProfileError("Git rename record is incomplete")
            old_path, new_path = tokens[index], tokens[index + 1]
            index += 2
            trigger_paths.update((old_path, new_path))
            current_paths.add(new_path)
        else:
            if index >= len(tokens):
                raise ProfileError("Git path record is incomplete")
            path = tokens[index]
            index += 1
            trigger_paths.add(path)
            if not status_code.startswith("D"):
                current_paths.add(path)
    current_paths.update(untracked_paths)
    trigger_paths.update(untracked_paths)
    return (
        {path for path in current_paths if _safe_path(path)},
        {path for path in trigger_paths if _safe_path(path)},
    )


def _changed_record_paths(root: pathlib.Path, base_ref: str) -> set[str]:
    return _changed_path_sets(root, base_ref)[1]


def _added_record_paths(root: pathlib.Path, base_ref: str) -> frozenset[pathlib.PurePosixPath]:
    baseline = _verified_commit(root, base_ref)
    if baseline is None:
        raise ProfileError("base_ref must resolve to a commit")
    paths: set[str] = set()
    commands = (
        ["diff", "--name-only", "-z", "--diff-filter=A", baseline, "--", "*.md"],
        ["ls-files", "-z", "--others", "--exclude-standard", "--", "*.md"],
    )
    for command in commands:
        result = _run_git(root, command, text=False)
        if result.returncode != 0:
            raise ProfileError("cannot determine added Markdown paths")
        try:
            paths.update(
                token.decode("utf-8")
                for token in result.stdout.split(b"\0")
                if token
            )
        except UnicodeDecodeError as error:
            raise ProfileError("added Markdown paths are not UTF-8") from error
    return frozenset(pathlib.PurePosixPath(path) for path in paths if _safe_path(path))


def _partition_plan_findings(
    root: pathlib.Path,
    profiles: dict[str, object],
    row: MigrationManifestRow,
    *,
    records: collections.abc.Sequence[Record] | None = None,
    payloads: collections.abc.Mapping[str, bytes] | None = None,
) -> list[Finding]:
    """Prove a partition approval against a tracked canonical Plan."""

    if row.partition_plan is None:
        return []
    source = row.source_path.as_posix()
    partition = row.partition_plan.as_posix()
    if not _safe_path(partition) or not partition.startswith(
        "docs/04.execution/plans/"
    ):
        return [
            _finding(
                source,
                "manifest-partition-plan-invalid",
                "partition plan must be a safe tracked regular Stage 04 Plan",
            )
        ]
    tracked_payload = _read_regular_repo_bytes(
        root, partition, require_tracked=True
    )
    if tracked_payload is None:
        return [
            _finding(
                source,
                "manifest-partition-plan-invalid",
                "partition plan must be a safe tracked regular Stage 04 Plan",
            )
        ]
    if records is None or payloads is None:
        current_records, current_payloads = _canonical_current_snapshot(
            root, profiles
        )
    else:
        current_records = tuple(records)
        current_payloads = dict(payloads)
    payload = current_payloads.get(partition)
    if payload is None:
        return [
            _finding(
                source,
                "manifest-partition-plan-invalid",
                "partition plan must be a safe tracked regular Stage 04 Plan",
            )
        ]
    try:
        text = payload.decode("utf-8")
    except UnicodeDecodeError:
        return [
            _finding(
                source,
                "manifest-partition-plan-invalid",
                "partition plan must be a safe tracked regular Stage 04 Plan",
            )
        ]
    by_path = {record.path.as_posix(): record for record in current_records}
    plan_record = by_path.get(partition)
    if plan_record is None:
        return [
            _finding(
                source,
                "manifest-partition-plan-invalid",
                "partition plan must be a safe tracked regular Stage 04 Plan",
            )
        ]
    values = plan_record.metadata
    plan_errors = [
        finding
        for finding in (
            *metadata.validate_record(
                plan_record,
                profiles,
                metadata.build_manifest(current_records),
            ),
            *metadata.validate_body_contract(plan_record, text, profiles, True),
        )
        if finding.severity == "error"
    ]
    if (
        plan_record.parse_error is not None
        or not plan_record.frontmatter_present
        or plan_record.artifact_type != "plan"
        or values.get("artifact_type") != "plan"
        or plan_errors
    ):
        return [
            _finding(
                source,
                "manifest-partition-plan-profile-invalid",
                "partition plan does not satisfy the canonical Plan profile",
            )
        ]
    if values.get("status") not in {"active", "completed"}:
        return [
            _finding(
                source,
                "manifest-partition-plan-status-invalid",
                "partition plan must have active or completed approval status",
            )
        ]
    if row.review_verdict != ReviewVerdict("pass", "pass"):
        return [
            _finding(
                source,
                "manifest-partition-plan-review-required",
                "partition approval requires independent passing manifest reviews",
            )
        ]
    return []


def _apply_partition_approvals(
    records: collections.abc.Sequence[Record],
    documents: collections.abc.Sequence[MigrationManifestDocument],
    *,
    root: pathlib.Path,
    profiles: dict[str, object],
) -> tuple[Record, ...]:
    approvals: dict[str, tuple[str, dict[str, str]]] = {}
    for document in documents:
        for row in document.entries:
            if row.partition_plan is None or _partition_plan_findings(
                root, profiles, row
            ):
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


def _record_body_bytes(root: pathlib.Path, record: Record) -> bytes | None:
    """Return snapshot bytes, or perform one bounded no-follow library read."""

    relative = record.path.as_posix()
    if (
        _CORPUS_SNAPSHOT_ROOT == root.resolve()
        and relative in _CORPUS_SNAPSHOT_BYTES
    ):
        return _CORPUS_SNAPSHOT_BYTES[relative]
    return _read_regular_repo_bytes(root, relative, require_tracked=False)


def _resolved_markdown_links(root: pathlib.Path, record: Record) -> set[str]:
    payload = _record_body_bytes(root, record)
    if payload is None:
        return set()
    try:
        text = payload.decode("utf-8")
    except UnicodeDecodeError:
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
    current_changed_paths, trigger_paths = _changed_path_sets(root, base_ref)
    selected = current_changed_paths & set(by_path)
    historical_ids: set[str] = set()
    historical_relation_ids: set[str] = set()
    for changed_path in sorted(trigger_paths):
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
        prior_parents = prior.metadata.get("parent_ids")
        if isinstance(prior_parents, list):
            historical_relation_ids.update(
                item for item in prior_parents if isinstance(item, str)
            )
        prior_supersedes = prior.metadata.get("supersedes")
        if isinstance(prior_supersedes, str):
            historical_relation_ids.add(prior_supersedes)
    selected_ids = historical_ids | {
        record.metadata.get("artifact_id")
        for path in selected
        if (record := by_path.get(path)) is not None
        and isinstance(record.metadata.get("artifact_id"), str)
    }
    additions: set[str] = set()
    additions.update(
        by_id[artifact_id]
        for artifact_id in historical_relation_ids
        if artifact_id in by_id
    )
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
        if _resolved_markdown_links(root, record) & trigger_paths:
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
            if participants & trigger_paths:
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
        snapshot_bytes = _read_regular_repo_bytes(
            root,
            snapshot_path,
            require_tracked=True,
        )
        if snapshot_bytes is None:
            findings.append(
                _finding(
                    path,
                    "archive-snapshot-file-invalid",
                    "snapshot must be a tracked regular in-root file",
                )
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
    normalized = "".join(
        character
        for character in unicodedata.normalize("NFKC", title).casefold()
        if character.isalnum()
    )
    return normalized or None


def find_duplicate_candidates(
    root: pathlib.Path,
    records: collections.abc.Sequence[Record],
) -> tuple[DuplicateCandidate, ...]:
    """Return same-type candidate signals without any disposition."""

    inspections: dict[str, tuple[bytes, str | None]] = {}
    for record in records:
        content = _record_body_bytes(root, record)
        if content is None:
            continue
        try:
            text = content.decode("utf-8")
        except UnicodeError:
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
        lines.append("| " + " | ".join(_escape_markdown_cell(value) for value in values) + " |")
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
        lines.append("| " + " | ".join(_escape_markdown_cell(value) for value in values) + " |")
    return "\n".join(lines) + "\n"


def _escape_markdown_cell(value: object) -> str:
    """Escape deterministic generated-table content without admitting row injection."""

    text = str(value)
    text = "".join(" " if ord(character) < 32 or ord(character) == 127 else character for character in text)
    return text.replace("|", "\\|")


def _exception_failure_code(
    document: object,
    known_codes: frozenset[str],
    today: datetime.date,
) -> str:
    """Map a canonical validation failure to a stable, value-free code."""

    if not isinstance(document, dict) or set(document) != {"schema_version", "exceptions"}:
        return "exception-schema-invalid"
    entries = document.get("exceptions")
    if type(document.get("schema_version")) is not int or document.get("schema_version") != 1:
        return "exception-schema-invalid"
    if not isinstance(entries, list):
        return "exception-schema-invalid"
    expected_fields = set(metadata.EXPECTED_EXCEPTION_SCHEMA["entry_fields"])
    ordering: list[tuple[str, tuple[str, ...]]] = []
    for entry in entries:
        if not isinstance(entry, dict):
            return "exception-schema-invalid"
        missing = expected_fields - set(entry)
        for field, code in (
            ("owner", "exception-owner-required"),
            ("reason", "exception-reason-required"),
            ("exit_condition", "exception-exit-condition-required"),
        ):
            if field in missing:
                return code
        if missing or set(entry) - expected_fields:
            return "exception-schema-invalid"
        finding_code = entry.get("finding_code")
        if isinstance(finding_code, str) and finding_code in SAFETY_FINDING_CODES:
            return "exception-safety-code-forbidden"
        if not isinstance(finding_code, str) or finding_code not in known_codes:
            return "exception-code-unknown"
        scopes = entry.get("scope_paths")
        if not (
            isinstance(scopes, list)
            and bool(scopes)
            and all(
                isinstance(scope, str)
                and _safe_path(scope)
                and scope.casefold() not in {"*", "**", ".", "all", "global"}
                for scope in scopes
            )
            and scopes == sorted(scopes)
            and len(scopes) == len(set(scopes))
        ):
            return "exception-scope-invalid"
        for field, code in (
            ("owner", "exception-owner-required"),
            ("reason", "exception-reason-required"),
            ("exit_condition", "exception-exit-condition-required"),
        ):
            value = entry.get(field)
            if not isinstance(value, str) or not value.strip():
                return code
        approved = entry.get("approved_at")
        expires = entry.get("expires_on")
        try:
            approved_date = (
                datetime.date.fromisoformat(approved)
                if isinstance(approved, str)
                else None
            )
            expiry_date = (
                datetime.date.fromisoformat(expires)
                if isinstance(expires, str)
                else None
            )
        except ValueError:
            approved_date = expiry_date = None
        if approved_date is None or approved_date > today:
            return "exception-approval-invalid"
        if expiry_date is None or expiry_date <= today:
            return "exception-expired"
        if expiry_date <= approved_date:
            return "exception-expiry-invalid"
        evidence = entry.get("evidence")
        if not (
            isinstance(evidence, list)
            and bool(evidence)
            and all(isinstance(value, str) and _safe_path(value) for value in evidence)
            and evidence == sorted(evidence)
            and len(evidence) == len(set(evidence))
        ):
            return "exception-evidence-invalid"
        ordering.append((finding_code, tuple(scopes)))
    if ordering != sorted(ordering) or len(ordering) != len(set(ordering)):
        return "exception-order-invalid"
    return "exception-static-invalid"


def _load_exception_document(path: pathlib.Path) -> object:
    try:
        return metadata._safe_load_unique(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as error:
        raise ProfileError("exception document cannot be loaded safely") from error


def validate_exceptions(
    path: pathlib.Path,
    *,
    known_codes: frozenset[str],
    today: datetime.date,
) -> list[Finding]:
    """Delegate bounded exception semantics to the canonical static validator."""

    label = path.name or "exceptions"
    try:
        loaded = _load_exception_document(path)
    except ProfileError:
        return [
            _finding(
                label,
                "exception-schema-invalid",
                "exception document cannot be parsed safely",
            )
        ]
    try:
        metadata.validate_static_exception_document(
            loaded,
            {"exception_schema": metadata.EXPECTED_EXCEPTION_SCHEMA},
            known_codes - SAFETY_FINDING_CODES,
            today,
        )
    except ProfileError:
        code = _exception_failure_code(loaded, known_codes, today)
        return [
            _finding(
                label,
                code,
                "exception document violates the canonical bounded contract",
            )
        ]
    return []


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
                _escape_markdown_cell(value)
                for value in (
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


def _output_path_components(path: pathlib.Path) -> tuple[tuple[str, ...], str]:
    """Return absolute parent components and a final name without resolving links."""

    if not path.is_absolute() or len(path.parts) < 2:
        raise _CorpusSafetyError("output", "output-path-unsafe")
    components = tuple(path.parts[1:])
    if any(part in {"", ".", ".."} for part in components):
        raise _CorpusSafetyError("output", "output-path-unsafe")
    return components[:-1], components[-1]


def _open_output_parent_descriptor(
    path: pathlib.Path,
    *,
    create: bool,
) -> tuple[int | None, str]:
    """Hold an absolute output parent through a component-wise no-follow chain."""

    parent_parts, final_name = _output_path_components(path)
    directory_flags = (
        os.O_RDONLY
        | getattr(os, "O_DIRECTORY", 0)
        | getattr(os, "O_NOFOLLOW", 0)
    )
    descriptor: int | None = None
    try:
        descriptor = os.open(path.anchor, directory_flags)
        for part in parent_parts:
            try:
                child = os.open(part, directory_flags, dir_fd=descriptor)
            except FileNotFoundError:
                if not create:
                    return None, final_name
                try:
                    os.mkdir(part, mode=0o755, dir_fd=descriptor)
                except FileExistsError:
                    pass
                try:
                    child = os.open(part, directory_flags, dir_fd=descriptor)
                except OSError as error:
                    raise _CorpusSafetyError(
                        "output", "output-path-unsafe"
                    ) from error
            except OSError as error:
                raise _CorpusSafetyError("output", "output-path-unsafe") from error
            os.close(descriptor)
            descriptor = child
        held = descriptor
        descriptor = None
        return held, final_name
    except _CorpusSafetyError:
        raise
    except OSError as error:
        raise _CorpusSafetyError("output", "output-path-unsafe") from error
    finally:
        if descriptor is not None:
            os.close(descriptor)


def _require_regular_output_entry(parent_descriptor: int, name: str) -> bool:
    """Return existence while rejecting a symlink or any non-regular entry."""

    try:
        details = os.stat(
            name,
            dir_fd=parent_descriptor,
            follow_symlinks=False,
        )
    except FileNotFoundError:
        return False
    except OSError as error:
        raise _CorpusSafetyError("output", "output-path-unsafe") from error
    if not stat.S_ISREG(details.st_mode):
        raise _CorpusSafetyError("output", "output-path-unsafe")
    return True


def _write_output(path: pathlib.Path, content: str) -> None:
    """Publish deterministic bytes atomically through a held no-follow parent."""

    _assert_safe_generated_output(content)
    payload = content.encode("utf-8")
    parent_descriptor, final_name = _open_output_parent_descriptor(path, create=True)
    if parent_descriptor is None:
        raise _CorpusSafetyError("output", "output-path-unsafe")
    temporary_name: str | None = None
    temporary_descriptor: int | None = None
    try:
        _require_regular_output_entry(parent_descriptor, final_name)
        for _ in range(16):
            candidate = (
                f".lifecycle-output-{os.getpid()}-{secrets.token_hex(8)}.tmp"
            )
            try:
                temporary_descriptor = os.open(
                    candidate,
                    os.O_WRONLY
                    | os.O_CREAT
                    | os.O_EXCL
                    | getattr(os, "O_NOFOLLOW", 0),
                    0o666,
                    dir_fd=parent_descriptor,
                )
            except FileExistsError:
                continue
            temporary_name = candidate
            break
        if temporary_descriptor is None or temporary_name is None:
            raise _CorpusSafetyError("output", "output-path-unsafe")
        view = memoryview(payload)
        while view:
            written = os.write(temporary_descriptor, view)
            if written <= 0:
                raise OSError("short output write")
            view = view[written:]
        os.fsync(temporary_descriptor)
        os.close(temporary_descriptor)
        temporary_descriptor = None

        # Reject a final link/non-regular swap observed before publication.
        # A later swap is still safe because replace(2) replaces the directory
        # entry itself and never follows it to a victim.
        _require_regular_output_entry(parent_descriptor, final_name)
        os.replace(
            temporary_name,
            final_name,
            src_dir_fd=parent_descriptor,
            dst_dir_fd=parent_descriptor,
        )
        temporary_name = None
        os.fsync(parent_descriptor)
    finally:
        if temporary_descriptor is not None:
            os.close(temporary_descriptor)
        if temporary_name is not None:
            try:
                os.unlink(temporary_name, dir_fd=parent_descriptor)
            except FileNotFoundError:
                pass
        os.close(parent_descriptor)


def _check_output(path: pathlib.Path, content: str) -> bool:
    """Compare canonical bytes from one held regular no-follow descriptor."""

    _assert_safe_generated_output(content)
    parent_descriptor, final_name = _open_output_parent_descriptor(path, create=False)
    if parent_descriptor is None:
        return False
    descriptor: int | None = None
    try:
        if not _require_regular_output_entry(parent_descriptor, final_name):
            return False
        try:
            descriptor = os.open(
                final_name,
                os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0),
                dir_fd=parent_descriptor,
            )
        except FileNotFoundError:
            return False
        except OSError as error:
            raise _CorpusSafetyError("output", "output-path-unsafe") from error
        if not stat.S_ISREG(os.fstat(descriptor).st_mode):
            raise _CorpusSafetyError("output", "output-path-unsafe")
        chunks: list[bytes] = []
        while True:
            chunk = os.read(descriptor, 1024 * 1024)
            if not chunk:
                break
            chunks.append(chunk)
        return b"".join(chunks) == content.encode("utf-8")
    finally:
        if descriptor is not None:
            os.close(descriptor)
        os.close(parent_descriptor)


def _rooted(root: pathlib.Path, path: pathlib.Path) -> pathlib.Path:
    return path if path.is_absolute() else root / path


def _tracked_corpus_paths(
    root: pathlib.Path,
    profiles: dict[str, object],
    *,
    allow_worktree_deletions: bool = False,
) -> tuple[str, ...]:
    """Discover and preflight every tracked lifecycle Markdown path safely."""

    result = _run_git(
        root,
        ["ls-files", "--stage", "-z", "--", "*.md"],
        text=False,
    )
    if result.returncode != 0:
        raise _CorpusSafetyError("corpus", "corpus-markdown-path-invalid")
    common = profiles.get("common")
    excluded_values = common.get("inventory_excludes") if isinstance(common, dict) else None
    excluded = set(excluded_values) if isinstance(excluded_values, list) else set()
    candidates: list[str] = []
    seen: set[str] = set()
    target_prefixes = tuple(metadata.TARGET_MARKDOWN_PREFIXES)
    for raw_entry in result.stdout.split(b"\0"):
        if not raw_entry:
            continue
        try:
            raw_header, raw_path = raw_entry.split(b"\t", 1)
            mode, _object_id, stage = raw_header.split()
            path = raw_path.decode("utf-8")
        except (ValueError, UnicodeDecodeError):
            raise _CorpusSafetyError(
                "corpus", "corpus-markdown-path-invalid"
            ) from None
        if not path.endswith(".md") or not path.startswith(target_prefixes):
            continue
        if not _safe_path(path):
            raise _CorpusSafetyError(path, "corpus-markdown-path-invalid")
        if stage != b"0" or mode not in {b"100644", b"100755"} or path in seen:
            raise _CorpusSafetyError(path, "corpus-markdown-mode-invalid")
        seen.add(path)
        candidates.append(path)

    allowed_missing = (
        _worktree_removed_markdown_paths(root)
        if allow_worktree_deletions
        else frozenset()
    )

    # Validate every worktree path before reading any Markdown body. This
    # catches final and intermediate symlinks even when the index mode is a
    # regular blob. The subsequent open repeats the same no-follow boundary,
    # so a swap between preflight and read still cannot expose outside bytes.
    for path in sorted(candidates):
        descriptor = _open_regular_repo_descriptor(root, path)
        if descriptor is None:
            if path in allowed_missing:
                try:
                    os.lstat(root / path)
                except FileNotFoundError:
                    continue
                except OSError:
                    pass
            raise _CorpusSafetyError(path, "corpus-markdown-file-invalid")
        os.close(descriptor)
    return tuple(
        path
        for path in sorted(candidates)
        if path not in excluded and path not in allowed_missing
    )


def _worktree_removed_markdown_paths(root: pathlib.Path) -> frozenset[str]:
    """Return only index-owned Markdown paths absent by a current D/R state."""

    result = _run_git(
        root,
        [
            "diff",
            "--name-status",
            "-z",
            "--find-renames",
            "--diff-filter=DR",
            "--",
            "*.md",
        ],
        text=False,
    )
    if result.returncode != 0:
        raise _CorpusSafetyError("corpus", "corpus-markdown-path-invalid")
    tokens = [token for token in result.stdout.split(b"\0") if token]
    removed: set[str] = set()
    index = 0
    while index < len(tokens):
        try:
            status_code = tokens[index].decode("ascii")
        except UnicodeDecodeError:
            raise _CorpusSafetyError(
                "corpus", "corpus-markdown-path-invalid"
            ) from None
        index += 1
        path_token: bytes
        if status_code.startswith("R"):
            if index + 1 >= len(tokens):
                raise _CorpusSafetyError(
                    "corpus", "corpus-markdown-path-invalid"
                )
            path_token = tokens[index]
            index += 2
        elif status_code.startswith("D"):
            if index >= len(tokens):
                raise _CorpusSafetyError(
                    "corpus", "corpus-markdown-path-invalid"
                )
            path_token = tokens[index]
            index += 1
        else:
            raise _CorpusSafetyError(
                "corpus", "corpus-markdown-path-invalid"
            )
        try:
            path = path_token.decode("utf-8")
        except UnicodeDecodeError:
            raise _CorpusSafetyError(
                "corpus", "corpus-markdown-path-invalid"
            ) from None
        if not _safe_path(path):
            raise _CorpusSafetyError(path, "corpus-markdown-path-invalid")
        removed.add(path)
    return frozenset(removed)


def _untracked_corpus_paths(
    root: pathlib.Path,
    profiles: dict[str, object],
) -> tuple[str, ...]:
    """Discover safe untracked Markdown and reject untracked symlink boundaries."""

    result = _run_git(
        root,
        ["ls-files", "-z", "--others", "--exclude-standard"],
        text=False,
    )
    if result.returncode != 0:
        raise _CorpusSafetyError("corpus", "corpus-markdown-path-invalid")
    common = profiles.get("common")
    excluded_values = common.get("inventory_excludes") if isinstance(common, dict) else None
    excluded = set(excluded_values) if isinstance(excluded_values, list) else set()
    target_prefixes = tuple(metadata.TARGET_MARKDOWN_PREFIXES)
    candidates: list[str] = []
    for raw_path in result.stdout.split(b"\0"):
        if not raw_path:
            continue
        try:
            path = raw_path.decode("utf-8")
        except UnicodeDecodeError:
            raise _CorpusSafetyError(
                "corpus", "corpus-markdown-path-invalid"
            ) from None
        if not path.startswith(target_prefixes):
            continue
        if not _safe_path(path):
            raise _CorpusSafetyError(path, "corpus-markdown-path-invalid")
        try:
            mode = os.lstat(root / path).st_mode
        except OSError:
            raise _CorpusSafetyError(path, "corpus-markdown-file-invalid") from None
        # Git reports an untracked intermediate symlink as the symlink entry,
        # not the Markdown file beyond it. Reject the boundary before any read.
        if stat.S_ISLNK(mode):
            raise _CorpusSafetyError(path, "corpus-markdown-file-invalid")
        if path.endswith(".md") and path not in excluded:
            candidates.append(path)
    for path in sorted(candidates):
        descriptor = _open_regular_repo_descriptor(root, path)
        if descriptor is None:
            raise _CorpusSafetyError(path, "corpus-markdown-file-invalid")
        os.close(descriptor)
    return tuple(sorted(set(candidates)))


def _safe_corpus_snapshot(
    root: pathlib.Path,
    profiles: dict[str, object],
    *,
    include_untracked: bool = False,
    allow_worktree_deletions: bool = False,
) -> tuple[tuple[Record, ...], dict[str, bytes]]:
    """Read one no-follow corpus snapshot, then parse only held safe bytes."""

    tracked_paths = _tracked_corpus_paths(
        root,
        profiles,
        allow_worktree_deletions=allow_worktree_deletions,
    )
    untracked_paths = (
        _untracked_corpus_paths(root, profiles) if include_untracked else ()
    )
    tracked = set(tracked_paths)
    paths = tuple(sorted(tracked | set(untracked_paths)))
    payloads: dict[str, bytes] = {}
    for path in paths:
        payload = _read_regular_repo_bytes(
            root, path, require_tracked=path in tracked
        )
        if payload is None:
            raise _CorpusSafetyError(path, "corpus-markdown-file-invalid")
        payloads[path] = payload
    records: list[Record] = []
    for path in paths:
        try:
            text = payloads[path].decode("utf-8")
        except UnicodeDecodeError:
            raise _CorpusSafetyError(path, "corpus-markdown-file-invalid") from None
        records.append(metadata._record_from_text(pathlib.Path(path), text))
    return tuple(records), payloads


def _collect_records(
    root: pathlib.Path,
    profiles: dict[str, object],
    *,
    include_untracked: bool = False,
    allow_worktree_deletions: bool = False,
) -> tuple[Record, ...]:
    global _CORPUS_SNAPSHOT_ROOT, _CORPUS_SNAPSHOT_BYTES
    _CORPUS_SNAPSHOT_ROOT = None
    _CORPUS_SNAPSHOT_BYTES = {}
    records, payloads = _safe_corpus_snapshot(
        root,
        profiles,
        include_untracked=include_untracked,
        allow_worktree_deletions=allow_worktree_deletions,
    )
    _CORPUS_SNAPSHOT_ROOT = root.resolve()
    _CORPUS_SNAPSHOT_BYTES = payloads
    return records


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
        if not os.path.lexists(absolute):
            findings.append(
                _finding(manifest_path, "promoted-manifest-missing", "declared manifest does not exist")
            )
            continue
        try:
            document = _load_repo_migration_manifest(root, manifest_path)
        except ProfileError:
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
        findings.extend(validate_migration_manifest(root, profiles, contract, document))
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
    return finding.code in SAFETY_FINDING_CODES


def _diagnostic_payload_is_sensitive(value: str) -> bool:
    payload = value.encode("utf-8", errors="replace")
    return any(pattern.search(payload) for pattern in SENSITIVE_PAYLOAD_PATTERNS)


def _safe_diagnostic_path(value: object) -> str:
    path = value if isinstance(value, str) else "corpus"
    if (
        len(path.encode("utf-8", errors="replace")) > 512
        or not _lexically_safe_path(path)
        or _diagnostic_payload_is_sensitive(path)
    ):
        return "corpus"
    return path


def _assert_safe_generated_output(content: str) -> None:
    if _diagnostic_payload_is_sensitive(content):
        raise _CorpusSafetyError("output", "diagnostic-redaction-unsafe")


def _print_findings(findings: collections.abc.Sequence[Finding]) -> None:
    ordered = sorted(set(findings))
    for finding in ordered:
        if _diagnostic_payload_is_sensitive(
            f"{finding.path}\n{finding.message}"
        ):
            raise _CorpusSafetyError(
                _safe_diagnostic_path(finding.path),
                "diagnostic-redaction-unsafe",
            )
    for finding in ordered:
        print(
            f"{finding.code}: {_safe_diagnostic_path(finding.path)}: "
            "validation rule is not satisfied"
        )


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
    try:
        _ensure_metadata_loaded()
        root = args.root.resolve()
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
            manifest_relative = _repo_manifest_path(root, args.manifest)
            document = _load_candidate_migration_manifest(root, manifest_relative)
            findings = validate_migration_manifest(root, profiles, contract, document)
            if document.wave != args.wave:
                findings.append(
                    _finding(args.manifest.as_posix(), "manifest-wave-mismatch", "--wave differs from manifest")
                )
            if not _candidate_manifest_matches(
                root,
                manifest_relative,
                render_migration_manifest(document),
            ):
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
            manifest_relative = _repo_manifest_path(root, args.manifest)
            document = _load_candidate_migration_manifest(root, manifest_relative)
            manifest_findings = validate_migration_manifest(root, profiles, contract, document)
            if not _candidate_manifest_matches(
                root,
                manifest_relative,
                render_migration_manifest(document),
            ):
                manifest_findings.append(
                    _finding(
                        manifest_relative,
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
                print("summary-stale: output: generated summary differs from canonical bytes")
                return 1
            return 0
        if args.mode == "check-impacted":
            documents, manifest_findings = _load_declared_manifests(
                root, profiles, contract, promoted_only=False
            )
            if manifest_findings:
                _print_findings(manifest_findings)
                return 3 if any(_is_safety_finding(item) for item in manifest_findings) else 1
            records = _collect_records(
                root,
                profiles,
                include_untracked=True,
                allow_worktree_deletions=True,
            )
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
                    _apply_partition_approvals(
                        records,
                        documents,
                        root=root,
                        profiles=profiles,
                    ),
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
            known_codes = (
                frozenset({item.code for item in findings}) | KNOWN_FINDING_CODES
            ) - SAFETY_FINDING_CODES
            exception_path = _rooted(root, args.exceptions).resolve()
            exception_findings = validate_exceptions(
                exception_path,
                known_codes=known_codes,
                today=datetime.date.today(),
            )
            findings.extend(exception_findings)
            if not exception_findings:
                loaded = _load_exception_document(exception_path)
                suppressed = {
                    (entry["finding_code"], scope)
                    for entry in loaded["exceptions"]
                    for scope in entry["scope_paths"]
                }
                findings = [
                    item
                    for item in findings
                    if _is_safety_finding(item)
                    or item.code.startswith("exception-")
                    or (item.code, item.path) not in suppressed
                ]
        _print_findings(findings)
        if args.mode == "report-full":
            safety = [item for item in findings if _is_safety_finding(item)]
            print(f"lifecycle full report: findings={len(findings)} safety_failures={len(safety)}")
            return 3 if safety else 0
        if args.mode == "check-full":
            return 3 if any(_is_safety_finding(item) for item in findings) else (1 if findings else 0)
        blocking = [item for item in findings if item.severity == "error"]
        return 3 if any(_is_safety_finding(item) for item in blocking) else (1 if blocking else 0)
    except _CorpusSafetyError as error:
        print(
            f"{error.code}: {_safe_diagnostic_path(error.path)}: "
            "selected lifecycle path is unsafe",
            file=sys.stderr,
        )
        return 3
    except ProfileError:
        print("configuration-error: repository lifecycle input is invalid", file=sys.stderr)
        return 3
    except (OSError, UnicodeError, yaml.YAMLError):
        print("internal-error: lifecycle operation failed safely", file=sys.stderr)
        return 3
    except Exception:
        print("internal-error: lifecycle operation failed safely", file=sys.stderr)
        return 3


if __name__ != "__main__":
    _ensure_metadata_loaded()


if __name__ == "__main__":
    raise SystemExit(main())
