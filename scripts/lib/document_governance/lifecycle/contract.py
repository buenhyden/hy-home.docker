#!/usr/bin/env python3
"""Lifecycle contract models, manifest I/O, and bounded repository safety."""

from __future__ import annotations

import collections
import collections.abc
import dataclasses
import hashlib
import os
import pathlib
import re
import shlex
import stat
import subprocess
import sys
from typing import Any

import yaml


_ROOT_ERROR = "FAIL: invalid HYHOME_CI_GATE_ROOT"


def _repository_root() -> pathlib.Path:
    fallback = pathlib.Path(__file__).resolve().parents[4]
    override = os.environ.get("HYHOME_CI_GATE_ROOT")
    if override is None:
        return fallback
    match = re.fullmatch(r"/proc/self/fd/(0|[1-9][0-9]*)", override)
    if match is None:
        raise SystemExit(_ROOT_ERROR)
    try:
        descriptor = os.fstat(int(match.group(1)))
        direct = fallback.stat()
    except (OSError, ValueError, OverflowError):
        raise SystemExit(_ROOT_ERROR) from None
    if not stat.S_ISDIR(descriptor.st_mode) or (
        descriptor.st_dev,
        descriptor.st_ino,
    ) != (direct.st_dev, direct.st_ino):
        raise SystemExit(_ROOT_ERROR)
    return pathlib.Path(override)


ROOT = _repository_root()
_REPOSITORY_DIRECTORY = str(ROOT)
if _REPOSITORY_DIRECTORY not in sys.path:
    sys.path.insert(0, _REPOSITORY_DIRECTORY)
_VALIDATION_DIRECTORY = str(ROOT / "scripts/validation")
if _VALIDATION_DIRECTORY not in sys.path:
    sys.path.insert(0, _VALIDATION_DIRECTORY)

from scripts.lib.document_governance.git_provenance import (  # noqa: E402
    HistoricalDocument,
    resolve_git_provenance,
)
from scripts.lib.document_governance import metadata_contract  # noqa: E402

DEFAULT_PROFILES = ROOT / "docs/99.templates/registry.json"
HISTORICAL_CONTRACT = HistoricalDocument(
    ROOT,
    "494065806794980080b081439298d7b534d10803",
    "docs/99.templates/support/document-corpus-migration-contract.yaml",
)
DEFAULT_CONTRACT = None
SAMPLE_SERVICE_FIXTURE_PATH = "examples/sample-web-service/service.md"
SAMPLE_SERVICE_FIXTURE_METADATA = {
    "status": "draft",
    "artifact_id": "spec:sample-web-service",
    "artifact_type": "spec",
    "parent_ids": [
        "spec:126-security-supply-chain-remediation",
        "spec:127-deployment-release-engineering-remediation",
    ],
}

MODES = (
    "check-public",
    "check-contract",
    "check-promoted",
    "check-recovery",
)

REVIEWED_EVIDENCE_WAVES = frozenset({"foundation"})
FOUNDATION_EVIDENCE_OWNER_PATHS = (
    "docs/03.specs/131-document-corpus-lifecycle-migration-foundation/spec.md",
    "docs/04.execution/plans/2026-07-14-document-corpus-lifecycle-migration-foundation.md",
)
ACTIVE_CONSUMER_PATHS = (
    ":(top,glob)*",
    ":(top,glob).claude/**",
    ":(top,glob).codex/**",
    ":(top,glob).github/**",
    ":(top,glob).rtk/**",
    ":(top,glob)docs/00.agent-governance/**",
    ":(top,glob)docs/01.requirements/**",
    ":(top,glob)docs/02.architecture/**",
    ":(top,glob)docs/03.specs/**",
    ":(top,glob)docs/04.execution/**",
    ":(top,glob)docs/05.operations/**",
    ":(top,glob)docs/99.templates/**",
    ":(top,glob)examples/**",
    ":(top,glob)infra/**",
    ":(top,glob)projects/**",
    ":(top,glob)scripts/**",
    ":(top,glob)secrets/**",
    ":(top,glob)tests/**",
)
ACTIVE_CONSUMER_EXCLUSIONS = (
    ":(top,exclude,literal)docs/03.specs/131-document-corpus-lifecycle-migration-foundation/spec.md",
    ":(top,exclude,literal)docs/04.execution/plans/2026-07-14-document-corpus-lifecycle-migration-foundation.md",
    ":(top,exclude,literal)docs/04.execution/tasks/2026-07-14-document-corpus-lifecycle-migration-foundation.md",
)


class _BootstrapProfileError(ValueError):
    """Used only until the canonical metadata module is loaded safely."""


class _CorpusSafetyError(Exception):
    """Value-free corpus path failure that must cross the CLI safety boundary."""

    def __init__(self, path: str, code: str) -> None:
        super().__init__(code)
        self.path = path if path and _lexically_safe_path(path) else "corpus"
        self.code = code


metadata: Any = metadata_contract
Finding: Any = metadata.Finding
Record: Any = metadata.Record
ProfileError: type[Exception] = metadata.ProfileError

_CORPUS_SNAPSHOT_ROOT: pathlib.Path | None = None
_CORPUS_SNAPSHOT_BYTES: dict[str, bytes] = {}


def _ensure_metadata_loaded() -> Any:
    """Load repository-backed metadata only after CLI-shape validation."""

    global metadata, Finding, Record, ProfileError
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
    artifact_type: str | None
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
    artifact_type_before: str | None = None
    artifact_type_after: str | None = None
    surface_class: str | None = None


@dataclasses.dataclass(frozen=True)
class MigrationManifestDocument:
    schema_version: int
    wave: str
    baseline_commit: str
    generated_by: str
    enforcement: str
    entries: tuple[MigrationManifestRow, ...]


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
MANIFEST_ENTRY_FIELDS_V2 = (
    "source_path",
    "target_path",
    "artifact_id",
    "artifact_type_before",
    "artifact_type_after",
    "surface_class",
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
SOURCE_EQUALS_TARGET = frozenset({"migrate", "preserve", "regenerate", "exempt"})
TARGET_DISTINCT = frozenset({"move", "merge", "archive"})
REVIEW_VALUES = frozenset({"pending", "pass", "changes-required"})
TYPED_SURFACE_CLASSES = frozenset(
    {"content-archive", "generated-output", "readme", "typed-example"}
)
OBJECT_ID = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})\Z")
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)(?:\s+[^)]*)?\)")
SENSITIVE_PAYLOAD_PATTERNS = (
    re.compile(
        rb"(?i)(?:password|passwd|credential|secret|token|access[_-]?token|refresh[_-]?token|api[_-]?key)\s*[:=]"
    ),
    re.compile(
        rb"(?i)(?:auth|authorization)\s*[:=]\s*(?:bearer|basic|[A-Za-z0-9+/]{16,})"
    ),
    re.compile(rb"(?is)\bmachine\s+\S+.{0,512}\blogin\s+\S+.{0,512}\bpassword\s+\S+"),
    re.compile(rb'(?i)"auths?"\s*:\s*\{|"auth"\s*:\s*"[A-Za-z0-9+/=_-]{8,}"'),
    re.compile(rb"\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b"),
    re.compile(rb"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(rb"\bsk-[A-Za-z0-9_-]{12,}\b"),
    re.compile(rb"\bgh[pousr]_[A-Za-z0-9_]{12,}\b"),
    re.compile(rb"\bxox[baprs]-[A-Za-z0-9-]{12,}\b"),
    re.compile(rb"-----BEGIN [A-Z0-9 ]*(?:PRIVATE KEY|PGP PRIVATE KEY BLOCK)-----"),
    re.compile(
        rb"(?i)(?:^|/|\\)(?:\.netrc|\.docker/config\.json|auth\.json|credentials)(?:\s|$)"
    ),
    re.compile(rb"(?i)(?:^|/|\\)\.(?:bash|zsh|sh)_history(?:\s|$)|\bHISTFILE\s*="),
    re.compile(rb"(?m)^\d{4}-\d{2}-\d{2}(?:T|\s).*(?:ERROR|WARN|DEBUG|TRACE)\b"),
    re.compile(rb"(?mi)^(?:TRACE|DEBUG|INFO|WARN|ERROR|FATAL)\b"),
    re.compile(
        rb'(?is)"(?:timestamp|time|ts)"\s*:\s*"[^"]+".{0,512}"level"\s*:\s*"(?:trace|debug|info|warn|error|fatal)"'
    ),
    re.compile(
        rb'(?is)\{.{0,512}"level"\s*:\s*"(?:trace|debug|info|warn|error|fatal)"'
    ),
    re.compile(
        rb"(?m)^(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}\s+\S+\s+\S+(?:\[\d+\])?:"
    ),
)


def _sensitive_value_is_present(value: str) -> bool:
    """Apply one value-free confidentiality classifier to durable and printed data."""

    payload = value.encode("utf-8", errors="replace")
    return any(pattern.search(payload) for pattern in SENSITIVE_PAYLOAD_PATTERNS)


SAFETY_FINDING_CODES = frozenset(
    {
        "manifest-static-invalid",
        "manifest-source-path-invalid",
        "manifest-source-not-at-baseline",
        "manifest-source-mode-invalid",
        "manifest-source-parse-invalid",
        "manifest-target-path-invalid",
        "manifest-target-file-invalid",
        "manifest-target-metadata-forbidden",
        "manifest-consumer-path-invalid",
        "manifest-evidence-path-invalid",
        "manifest-evidence-confidential",
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
        "spec-package-invalid",
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
        "manifest-consumer-scan-invalid",
        "manifest-consumer-evidence-mismatch",
        "manifest-reviewed-evidence-required",
        "manifest-reviewed-source-evidence-invalid",
        "manifest-reviewed-repository-evidence-invalid",
        "manifest-rollback-invalid",
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


def _active_consumer_scan_args(source: str) -> tuple[str, ...]:
    return (
        "grep",
        "-lz",
        "--fixed-strings",
        "--",
        source,
        "--",
        *ACTIVE_CONSUMER_PATHS,
        *ACTIVE_CONSUMER_EXCLUSIONS,
        f":(top,exclude,literal){source}",
    )


def _active_consumer_scan_command(source: str) -> str:
    return shlex.join(("git", *_active_consumer_scan_args(source)))


def _tracked_active_consumers(
    root: pathlib.Path,
    source: str,
) -> tuple[pathlib.PurePosixPath, ...]:
    result = _run_git(root, _active_consumer_scan_args(source), text=False)
    if result.returncode not in {0, 1}:
        raise ProfileError("bounded active-consumer Git scan failed")
    try:
        values = tuple(
            pathlib.PurePosixPath(item.decode("utf-8"))
            for item in result.stdout.split(b"\0")
            if item
        )
    except UnicodeDecodeError as error:
        raise ProfileError(
            "bounded active-consumer Git scan returned invalid UTF-8"
        ) from error
    if any(not _safe_path(item.as_posix()) for item in values):
        raise ProfileError("bounded active-consumer Git scan returned an unsafe path")
    return tuple(sorted(set(values)))


def _reviewed_evidence_findings(
    root: pathlib.Path,
    document: MigrationManifestDocument,
    row: MigrationManifestRow,
) -> list[Finding]:
    if document.wave not in REVIEWED_EVIDENCE_WAVES:
        return []
    evidence = row.evidence
    review_started = (
        document.enforcement == "blocking"
        or row.review_verdict.specification == "pass"
        or row.review_verdict.quality == "pass"
    )
    evidence_present = any(
        (
            evidence.commands,
            evidence.sources,
            evidence.repository_paths,
            evidence.consumer_scan,
            evidence.rollback,
        )
    )
    if not review_started and not evidence_present:
        return []
    source = row.source_path.as_posix()
    if not _safe_path(source):
        return []
    findings: list[Finding] = []
    required_nonempty = (
        evidence.commands,
        evidence.sources,
        evidence.repository_paths,
        evidence.consumer_scan,
    )
    if review_started and any(not values for values in required_nonempty):
        findings.append(
            _finding(
                source,
                "manifest-reviewed-evidence-required",
                "reviewed Foundation evidence requires complete bounded proof",
            )
        )
    expected_sources = tuple(sorted((source, *FOUNDATION_EVIDENCE_OWNER_PATHS)))
    if review_started and evidence.sources != expected_sources:
        findings.append(
            _finding(
                source,
                "manifest-reviewed-source-evidence-invalid",
                "reviewed Foundation sources do not match their canonical owners",
            )
        )
    expected_repository_paths = tuple(
        pathlib.PurePosixPath(path) for path in expected_sources
    )
    if review_started and evidence.repository_paths != expected_repository_paths:
        findings.append(
            _finding(
                source,
                "manifest-reviewed-repository-evidence-invalid",
                "reviewed Foundation repository paths do not match their canonical owners",
            )
        )
    expected_scan = _active_consumer_scan_command(source)
    if expected_scan not in evidence.consumer_scan:
        findings.append(
            _finding(
                source,
                "manifest-consumer-scan-invalid",
                "reviewed evidence requires the canonical bounded active-consumer scan",
            )
        )
    try:
        expected_consumers = _tracked_active_consumers(root, source)
    except ProfileError:
        expected_consumers = ()
        findings.append(
            _finding(
                source,
                "manifest-consumer-scan-invalid",
                "canonical bounded active-consumer scan could not be verified",
            )
        )
    if row.active_consumers != expected_consumers:
        findings.append(
            _finding(
                source,
                "manifest-consumer-evidence-mismatch",
                "active_consumers differs from the canonical bounded Git scan",
            )
        )

    log_pattern = re.compile(
        rf"git log --format=%H ([0-9a-f]{{40}})\.\.([0-9a-f]{{40}}) -- {re.escape(source)}\Z"
    )
    matches = [
        match
        for command in evidence.commands
        if (match := log_pattern.fullmatch(command)) is not None
    ]
    expected_rollback: tuple[str, ...] | None = None
    if len(matches) == 1:
        lower, upper = matches[0].groups()
        if lower == document.baseline_commit and _verified_commit(root, upper) == upper:
            history = _run_git(
                root,
                ["log", "--format=%H", f"{lower}..{upper}", "--", source],
            )
            lines = history.stdout.splitlines()
            commits = tuple(lines)
            if history.returncode == 0 and all(
                OBJECT_ID.fullmatch(line) for line in lines
            ):
                expected_rollback = (
                    ("git revert --no-commit " + " ".join(commits),) if commits else ()
                )
    if (
        expected_rollback is None
        or evidence.rollback != expected_rollback
        or (expected_rollback == () and row.disposition != "preserve")
    ):
        findings.append(
            _finding(
                source,
                "manifest-rollback-invalid",
                "rollback must exactly pin source-changing commits newest-to-oldest",
            )
        )
    return findings


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
    return (
        bool(metadata._safe_repo_path(value))
        and isinstance(value, str)
        and not any(marker in value for marker in "*?[]{}")
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
        os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
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
            record.split(b" ", 1)[0] for record in tracked.stdout.split(b"\0") if record
        }
        if not modes or not modes <= {b"100644", b"100755"}:
            return None
    descriptor = _open_regular_repo_descriptor(root, relative_path)
    if descriptor is None:
        return None
    try:
        before = os.fstat(descriptor)
        limit = 4 * 1024 * 1024
        if before.st_size > limit:
            return None
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = os.read(descriptor, min(65_536, limit + 1 - total))
            if not chunk:
                break
            chunks.append(chunk)
            total += len(chunk)
            if total > limit:
                return None
        after = os.fstat(descriptor)
        if (before.st_size, before.st_mtime_ns, before.st_ctime_ns) != (
            after.st_size,
            after.st_mtime_ns,
            after.st_ctime_ns,
        ):
            return None
        return b"".join(chunks)
    except OSError:
        return None
    finally:
        os.close(descriptor)


def _baseline_regular_blob(root: pathlib.Path, commit: str, path: str) -> bool:
    """Return whether an exact baseline path is a regular Git blob entry."""

    return bool(
        _safe_path(path)
        and resolve_git_provenance(path, commit, repo_root=root).is_regular_blob
    )


def _safe_path_text(value: pathlib.PurePosixPath | None) -> str | None:
    return None if value is None else value.as_posix()


def _as_exact_mapping(
    value: object, fields: tuple[str, ...], label: str
) -> dict[str, object]:
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
    """Read the completed migration's contract for its data, not its shape.

    The file this resolves is absent from the working tree; it is recovered
    from a pinned commit. The 384-line shape assertion that used to guard it
    required a deleted Spec Package's eight named waves to be present in a
    deleted YAML, which is policy about a migration that finished. The modes
    below still read its rows, so the data is loaded and the frozen shape is
    not enforced.
    """

    try:
        loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as error:
        # Never echo the payload. A malformed contract is a configuration
        # error, and its content may carry anything.
        raise ProfileError("migration contract is unreadable") from error
    if not isinstance(loaded, dict):
        raise ProfileError("migration contract must be a mapping")
    for key in ("waves", "manifest", "archive"):
        value = loaded.get(key)
        if value is not None and not isinstance(value, dict):
            raise ProfileError(f"migration contract {key} must be a mapping")
    return loaded


def _load_migration_manifest_text(source: str) -> MigrationManifestDocument:
    try:
        loaded = metadata._safe_load_unique(source)
    except yaml.YAMLError as error:
        raise ProfileError("cannot load migration manifest safely") from error
    top = _as_exact_mapping(loaded, MANIFEST_TOP_LEVEL_FIELDS, "migration manifest")
    schema_version = top["schema_version"]
    if type(schema_version) is not int or schema_version not in {1, 2}:
        raise ProfileError(
            "migration manifest schema_version must be the integer 1 or 2"
        )
    entry_fields = (
        MANIFEST_ENTRY_FIELDS_V2 if schema_version == 2 else MANIFEST_ENTRY_FIELDS
    )
    entries_value = top["entries"]
    if not isinstance(entries_value, list):
        raise ProfileError("migration manifest entries must be a list")
    entries: list[MigrationManifestRow] = []
    for index, raw_entry in enumerate(entries_value):
        label = f"migration manifest entry {index}"
        if schema_version == 2:
            if not isinstance(raw_entry, dict) or set(raw_entry) != set(entry_fields):
                raise ProfileError(f"{label} must define the exact canonical fields")
            entry = {field: raw_entry[field] for field in entry_fields}
        else:
            entry = _as_exact_mapping(raw_entry, entry_fields, label)
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
                target_path=pathlib.PurePosixPath(target)
                if target is not None
                else None,
                artifact_id=_as_string(
                    entry["artifact_id"], f"{label} artifact_id", nullable=True
                ),
                artifact_type=(
                    _as_string(entry["artifact_type"], f"{label} artifact_type") or ""
                    if schema_version == 1
                    else None
                ),
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
                artifact_type_before=(
                    _as_string(
                        entry["artifact_type_before"],
                        f"{label} artifact_type_before",
                        nullable=True,
                    )
                    if schema_version == 2
                    else None
                ),
                artifact_type_after=(
                    _as_string(
                        entry["artifact_type_after"],
                        f"{label} artifact_type_after",
                        nullable=True,
                    )
                    if schema_version == 2
                    else None
                ),
                surface_class=(
                    _as_string(entry["surface_class"], f"{label} surface_class")
                    if schema_version == 2
                    else None
                ),
            )
        )
    return MigrationManifestDocument(
        schema_version=schema_version,
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


def _repo_manifest_matches(
    root: pathlib.Path,
    relative_path: str,
    expected: str,
) -> bool:
    payload = _read_regular_repo_bytes(root, relative_path, require_tracked=True)
    return payload == expected.replace("\r\n", "\n").encode("utf-8")


def _manifest_mapping(document: MigrationManifestDocument) -> dict[str, object]:
    def row_mapping(row: MigrationManifestRow) -> dict[str, object]:
        artifact_fields = (
            {
                "artifact_type_before": row.artifact_type_before,
                "artifact_type_after": row.artifact_type_after,
                "surface_class": row.surface_class,
            }
            if document.schema_version == 2
            else {"artifact_type": row.artifact_type}
        )
        return {
            "source_path": row.source_path.as_posix(),
            "target_path": _safe_path_text(row.target_path),
            "artifact_id": row.artifact_id,
            **artifact_fields,
            "status_before": row.status_before,
            "status_after": row.status_after,
            "parent_ids": sorted(row.parent_ids),
            "disposition": row.disposition,
            "canonical_replacement": row.canonical_replacement,
            "active_consumers": sorted(
                path.as_posix() for path in row.active_consumers
            ),
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

    return {
        "schema_version": document.schema_version,
        "wave": document.wave,
        "baseline_commit": document.baseline_commit,
        "generated_by": document.generated_by,
        "enforcement": document.enforcement,
        "entries": [
            row_mapping(row)
            for row in sorted(
                document.entries, key=lambda item: item.source_path.as_posix()
            )
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


def _baseline_tree_entries(
    root: pathlib.Path,
    commit: str,
    paths: collections.abc.Sequence[str],
    *,
    recursive: bool,
) -> dict[str, str]:
    """Return safe regular baseline paths and modes without reading blob bodies."""

    if not paths:
        return {}
    if any(not _safe_path(path) for path in paths):
        raise ProfileError("wave selection paths must be safe")
    args = ["ls-tree", "-z"]
    if recursive:
        args.append("-r")
    args.extend([commit, "--", *paths])
    result = _run_git(root, args, text=False)
    if result.returncode != 0:
        raise ProfileError("wave baseline tree enumeration failed")
    entries: dict[str, str] = {}
    for raw_entry in result.stdout.split(b"\0"):
        if not raw_entry:
            continue
        try:
            raw_header, raw_path = raw_entry.split(b"\t", 1)
            raw_mode, raw_type, raw_object = raw_header.split()
            mode = raw_mode.decode("ascii")
            object_type = raw_type.decode("ascii")
            object_id = raw_object.decode("ascii")
            path = raw_path.decode("utf-8")
        except (ValueError, UnicodeDecodeError):
            raise ProfileError("wave baseline tree metadata is malformed") from None
        if (
            mode not in {"100644", "100755"}
            or object_type != "blob"
            or not OBJECT_ID.fullmatch(object_id)
            or not _safe_path(path)
        ):
            raise ProfileError("wave selection includes a non-regular or unsafe path")
        if path in entries:
            raise ProfileError("wave baseline tree contains duplicate paths")
        entries[path] = mode
    return entries


def _surface_class(path: str, mode: str, profiles: dict[str, object]) -> str:
    """Classify a baseline path from safe path/mode metadata only."""

    pure = pathlib.PurePosixPath(path)
    name = pure.name
    suffix = pure.suffix.lower()
    if path.startswith("archive/"):
        return "content-archive"
    if path.startswith(".github/"):
        return "native-platform"
    if name == "README.md":
        return "readme"
    if metadata.registered_generated_owner(pathlib.Path(path), profiles) is not None:
        return "generated-output"
    if path.startswith("secrets/"):
        return "secret-metadata"
    if path.startswith("tests/"):
        return "test-fixture"
    if name == "Dockerfile" or name.startswith(("docker-compose", "compose.")):
        return "runtime"
    if suffix in {".container", ".service", ".socket"}:
        return "runtime"
    if suffix == ".md" and (path.startswith("examples/") or path.startswith("docs/")):
        return "typed-example"
    if mode == "100755" or (
        path.startswith("scripts/")
        and suffix in {".sh", ".bash", ".zsh", ".py", ".js", ".mjs", ".ts"}
    ):
        return "executable-script"
    if suffix in {
        ".yaml",
        ".yml",
        ".json",
        ".jsonc",
        ".toml",
        ".ini",
        ".conf",
        ".config",
        ".env",
        ".example",
        ".properties",
    } or name.startswith("."):
        return "configuration"
    return "unsupported-static"


def _typed_baseline_metadata(
    root: pathlib.Path,
    commit: str,
    path: str,
    surface_class: str,
) -> dict[str, object]:
    """Decode only declared Markdown/profile surfaces, never native/binary rows."""

    if surface_class not in {
        "content-archive",
        "generated-output",
        "readme",
        "typed-example",
    }:
        return {}
    shown = _run_git(root, ["show", f"{commit}:{path}"], text=False)
    if shown.returncode != 0:
        raise ProfileError("typed wave source is unavailable at the baseline")
    try:
        source_text = shown.stdout.decode("utf-8")
        return metadata._parse_frontmatter_text(source_text)
    except (UnicodeDecodeError, metadata.FrontmatterError) as error:
        raise ProfileError("typed wave source frontmatter cannot be parsed") from error


def _surface_artifact_types(
    path: str,
    surface_class: str,
    frontmatter: dict[str, object],
    profiles: dict[str, object],
) -> tuple[str | None, str | None]:
    profile_map = profiles.get("profiles")
    registered = set(profile_map) if isinstance(profile_map, dict) else set()
    declared = frontmatter.get("type")
    declared_type = (
        declared if isinstance(declared, str) and declared in registered else None
    )
    if surface_class == "content-archive":
        return ("archive" if declared_type == "archive" else None), "archive"
    if surface_class == "readme":
        return declared_type or "readme", declared_type or "readme"
    if surface_class == "generated-output":
        return "generated", "generated"
    if surface_class == "typed-example":
        inferred = declared_type or metadata.infer_artifact_type(
            pathlib.Path(path), profiles
        )
        inferred = (
            inferred if inferred in registered and inferred != "unsupported" else None
        )
        return inferred, inferred
    return None, None


def _manifest_profiles(
    profiles: dict[str, object] | None,
) -> dict[str, object]:
    """Return the Registry-first adapter required by manifest inference."""

    if profiles is not None and isinstance(profiles.get("profiles"), dict):
        return profiles
    return metadata.build_registry_profiles(metadata.load_registry(DEFAULT_PROFILES))


def _generate_manifest_skeleton(
    root: pathlib.Path,
    contract: dict[str, object],
    *,
    wave: str,
    baseline_ref: str,
    profiles: dict[str, object] | None = None,
) -> MigrationManifestDocument:
    """Generate a pending skeleton from exact baseline bytes."""

    baseline_commit = _verified_commit(root, baseline_ref)
    if baseline_commit is None:
        raise ProfileError("baseline_ref must resolve to a commit")
    wave_contract = _wave_mapping(contract, wave)
    pinned_baseline = wave_contract.get("baseline_commit")
    if pinned_baseline is not None and pinned_baseline != baseline_commit:
        raise ProfileError(
            "baseline_ref must resolve to the wave's pinned baseline_commit"
        )
    active_profiles = _manifest_profiles(profiles)
    source_roots = wave_contract.get("source_roots")
    direct_source_paths = wave_contract.get("direct_source_paths")
    if source_roots is not None or direct_source_paths is not None:
        if not isinstance(source_roots, list) or not all(
            isinstance(item, str) for item in source_roots
        ):
            raise ProfileError("wave source_roots must be a string list")
        if not isinstance(direct_source_paths, list) or not all(
            isinstance(item, str) for item in direct_source_paths
        ):
            raise ProfileError("wave direct_source_paths must be a string list")
        selected = _baseline_tree_entries(
            root, baseline_commit, source_roots, recursive=True
        )
        direct_entries = _baseline_tree_entries(
            root, baseline_commit, direct_source_paths, recursive=False
        )
        if set(direct_entries) != set(direct_source_paths):
            raise ProfileError("wave direct source path is not tracked at the baseline")
        for path, mode in direct_entries.items():
            existing = selected.get(path)
            if existing is not None and existing != mode:
                raise ProfileError("wave source metadata conflicts across selectors")
            selected[path] = mode
        rows: list[MigrationManifestRow] = []
        for source_path, mode in sorted(selected.items()):
            surface_class = _surface_class(source_path, mode, active_profiles)
            frontmatter = _typed_baseline_metadata(
                root, baseline_commit, source_path, surface_class
            )
            artifact_type_before, artifact_type_after = _surface_artifact_types(
                source_path, surface_class, frontmatter, active_profiles
            )
            before_status = frontmatter.get("status")
            status_before = before_status if isinstance(before_status, str) else None
            status_after = (
                "archived" if surface_class == "content-archive" else status_before
            )
            identity_type = artifact_type_after or artifact_type_before or "unsupported"
            parent_ids = frontmatter.get("parent_ids")
            rows.append(
                MigrationManifestRow(
                    source_path=pathlib.PurePosixPath(source_path),
                    target_path=pathlib.PurePosixPath(source_path),
                    artifact_id=_manifest_artifact_id(
                        identity_type, frontmatter.get("artifact_id")
                    ),
                    artifact_type=None,
                    status_before=status_before,
                    status_after=status_after,
                    parent_ids=tuple(sorted(parent_ids))
                    if isinstance(parent_ids, list)
                    and all(isinstance(item, str) for item in parent_ids)
                    else (),
                    disposition="preserve",
                    canonical_replacement=None,
                    active_consumers=(),
                    partition_plan=None,
                    preservation_class=None,
                    evidence=ManifestEvidence((), (), (), (), ()),
                    review_verdict=ReviewVerdict("pending", "pending"),
                    artifact_type_before=artifact_type_before,
                    artifact_type_after=artifact_type_after,
                    surface_class=surface_class,
                )
            )
        return MigrationManifestDocument(
            schema_version=2,
            wave=wave,
            baseline_commit=baseline_commit,
            generated_by="check-document-corpus-lifecycle.py",
            enforcement=str(wave_contract.get("enforcement", "advisory")),
            entries=tuple(rows),
        )

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
            else metadata.infer_artifact_type(relative, active_profiles)
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
                artifact_type_before=artifact_type,
                artifact_type_after=artifact_type,
                surface_class="typed-example",
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


def generate_manifest_skeleton(
    root: pathlib.Path,
    contract: dict[str, object],
    *,
    wave: str,
    baseline_ref: str,
) -> MigrationManifestDocument:
    """Generate a pending skeleton through the fixed public Plan interface."""

    return _generate_manifest_skeleton(
        root,
        contract,
        wave=wave,
        baseline_ref=baseline_ref,
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

    if not _safe_path(path):
        return None
    provenance = resolve_git_provenance(path, commit, repo_root=root)
    return provenance.object_id if provenance.is_regular_blob else None


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
    if disposition == "merge" and (target is None or candidate_path != target):
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
    if candidate.artifact_type in {
        "archive",
        "generated",
        "readme",
        "repo-support",
        "template-source",
        "unsupported",
    } or candidate.metadata.get("status") not in {"active", "completed"}:
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
    declared_owner_type = owner.metadata.get("type")
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
        transitions.get(baseline_status) if isinstance(transitions, dict) else None
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
        candidate for candidate in entries if complete_attestation(candidate)
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
    profiles: dict[str, object],
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
            pathlib.Path(target), text, profiles=profiles
        )
    return (
        tuple(records_by_path[path] for path in sorted(records_by_path)),
        result_payloads,
    )


def _surface_regular_result_exists(root: pathlib.Path, path: str) -> bool:
    """Check one result path without reading or decoding its body."""

    descriptor = _open_regular_repo_descriptor(root, path)
    if descriptor is None:
        return False
    os.close(descriptor)
    return True


def _surface_tracked_regular_mode(root: pathlib.Path, path: str) -> str | None:
    """Return the exact tracked regular-file mode without reading the file body."""

    if not _safe_path(path):
        return None
    tracked = _run_git(
        root,
        ["ls-files", "--stage", "-z", "--", path],
        text=False,
    )
    if tracked.returncode != 0:
        return None
    entries = [entry for entry in tracked.stdout.split(b"\0") if entry]
    if len(entries) != 1 or b"\t" not in entries[0]:
        return None
    header, raw_path = entries[0].split(b"\t", 1)
    fields = header.split()
    try:
        mode = fields[0].decode("ascii") if len(fields) == 3 else ""
        object_id = fields[1].decode("ascii") if len(fields) == 3 else ""
        stage = fields[2].decode("ascii") if len(fields) == 3 else ""
        tracked_path = raw_path.decode("utf-8")
    except UnicodeDecodeError:
        return None
    if (
        mode not in {"100644", "100755"}
        or not OBJECT_ID.fullmatch(object_id)
        or stage != "0"
        or tracked_path != path
    ):
        return None
    descriptor = _open_regular_repo_descriptor(root, path)
    if descriptor is None:
        return None
    os.close(descriptor)
    return mode


def _surface_native_replacement_valid(
    root: pathlib.Path,
    profiles: dict[str, object],
    document: MigrationManifestDocument,
    row: MigrationManifestRow,
    replacement: str,
) -> bool:
    """Validate one selected native replacement using path and mode truth only."""

    native_classes = {"runtime", "configuration"}
    source = row.source_path.as_posix()
    target = _safe_path_text(row.target_path)
    if (
        row.surface_class not in native_classes
        or not _safe_path(replacement)
        or replacement in {source, target}
    ):
        return False
    candidates = [
        candidate
        for candidate in document.entries
        if _safe_path_text(candidate.target_path) == replacement
    ]
    if len(candidates) != 1:
        return False
    candidate = candidates[0]
    mode = _surface_tracked_regular_mode(root, replacement)
    return (
        candidate.disposition != "delete"
        and candidate.surface_class == row.surface_class
        and mode is not None
        and _surface_class(replacement, mode, profiles) == row.surface_class
    )


def _surface_replacement_record(
    root: pathlib.Path,
    profiles: dict[str, object],
    replacement: str,
) -> Record | None:
    """Resolve one typed replacement while leaving selected native bodies opaque."""

    candidate_paths: tuple[str, ...] = ()
    replacement_is_tracked_path = (
        _safe_path(replacement)
        and _read_regular_repo_bytes(root, replacement, require_tracked=True)
        is not None
    )
    replacement_is_artifact_id = (
        not replacement_is_tracked_path
        and metadata._valid_metadata_artifact_id(replacement)
    )
    if replacement_is_tracked_path:
        candidate_paths = (replacement,)
    elif replacement_is_artifact_id:
        result = _run_git(
            root,
            [
                "grep",
                "-lz",
                "--fixed-strings",
                "--",
                f"artifact_id: {replacement}",
                "--",
                ":(top,glob)**/*.md",
                ":(top,glob)*.md",
            ],
            text=False,
        )
        if result.returncode not in {0, 1}:
            return None
        try:
            candidate_paths = tuple(
                sorted(
                    {
                        value.decode("utf-8")
                        for value in result.stdout.split(b"\0")
                        if value
                    }
                )
            )
        except UnicodeDecodeError:
            return None
    else:
        return None

    candidates: list[Record] = []
    for path in candidate_paths:
        if not _safe_path(path):
            continue
        payload = _read_regular_repo_bytes(root, path, require_tracked=True)
        if payload is None:
            continue
        try:
            text = payload.decode("utf-8")
        except UnicodeDecodeError:
            continue
        record = metadata._record_from_text(pathlib.Path(path), text, profiles=profiles)
        if (
            record.parse_error is not None
            or not record.frontmatter_present
            or record.artifact_type
            in {
                "archive",
                "generated",
                "readme",
                "repo-support",
                "template-source",
                "unsupported",
            }
            or record.metadata.get("status") not in {"active", "completed"}
        ):
            continue
        if (
            replacement_is_artifact_id
            and record.metadata.get("artifact_id") != replacement
        ):
            continue
        candidates.append(record)
    return candidates[0] if len(candidates) == 1 else None


def _surface_replacement_findings(
    root: pathlib.Path,
    profiles: dict[str, object],
    document: MigrationManifestDocument,
    row: MigrationManifestRow,
) -> list[Finding]:
    """Apply the common replacement contract without scanning selected bodies."""

    source = row.source_path.as_posix()
    target = _safe_path_text(row.target_path)
    replacement = row.canonical_replacement
    if row.disposition == "merge" and replacement is None:
        return [
            _finding(
                source,
                "manifest-replacement-required",
                "destructive row requires a replacement",
            )
        ]
    if row.disposition in SOURCE_EQUALS_TARGET | {"move"} and replacement is not None:
        return [
            _finding(
                source,
                "manifest-replacement-forbidden",
                "disposition forbids a replacement",
            )
        ]
    if replacement is None:
        return []
    if document.schema_version == 2 and row.surface_class in {
        "runtime",
        "configuration",
    }:
        return (
            []
            if _surface_native_replacement_valid(
                root,
                profiles,
                document,
                row,
                replacement,
            )
            else [
                _finding(
                    source,
                    "manifest-replacement-invalid",
                    "canonical native replacement must resolve uniquely",
                )
            ]
        )
    candidate = _surface_replacement_record(root, profiles, replacement)
    if candidate is None:
        return [
            _finding(
                source,
                "manifest-replacement-invalid",
                "canonical replacement must resolve uniquely",
            )
        ]
    candidate_path = candidate.path.as_posix()
    if row.disposition == "merge":
        valid = target is not None and candidate_path == target
    else:
        valid = candidate_path not in {
            value for value in (source, target) if value is not None
        }
    return (
        []
        if valid
        else [
            _finding(
                source,
                "manifest-replacement-invalid",
                "canonical replacement does not match the selected result",
            )
        ]
    )


def _surface_rollback_valid(root: pathlib.Path, commands: tuple[str, ...]) -> bool:
    """Accept only immutable newest-to-oldest Git revert commands."""

    for command in commands:
        try:
            tokens = shlex.split(command)
        except ValueError:
            return False
        if tokens[:3] != ["git", "revert", "--no-commit"] or len(tokens) < 4:
            return False
        commits = tokens[3:]
        if any(
            not OBJECT_ID.fullmatch(commit) or _verified_commit(root, commit) != commit
            for commit in commits
        ):
            return False
        for newer, older in zip(commits, commits[1:]):
            order = _run_git(root, ["merge-base", "--is-ancestor", older, newer])
            if order.returncode != 0:
                return False
    return True


def _surface_partition_plan_findings(
    root: pathlib.Path,
    profiles: dict[str, object],
    row: MigrationManifestRow,
) -> list[Finding]:
    """Validate the selected canonical Plan; native and binary rows stay opaque."""

    if row.partition_plan is None:
        return []
    source = row.source_path.as_posix()
    partition = row.partition_plan.as_posix()
    if (
        not _safe_path(partition)
        or metadata.infer_artifact_type(pathlib.Path(partition), profiles) != "plan"
    ):
        return [
            _finding(
                source,
                "manifest-partition-plan-invalid",
                "partition plan must be a safe tracked regular canonical Plan",
            )
        ]
    current_records, current_payloads = _canonical_current_snapshot(root, profiles)
    payload = current_payloads.get(partition)
    plan_record = {record.path.as_posix(): record for record in current_records}.get(
        partition
    )
    if payload is None or plan_record is None:
        return [
            _finding(
                source,
                "manifest-partition-plan-invalid",
                "partition plan must be a safe tracked regular canonical Plan",
            )
        ]
    try:
        text = payload.decode("utf-8")
    except UnicodeDecodeError:
        return [
            _finding(
                source,
                "manifest-partition-plan-invalid",
                "partition plan must be a UTF-8 canonical Plan",
            )
        ]
    profile_errors = [
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
        or plan_record.metadata.get("type") != "sdlc/plan"
        or plan_record.metadata.get("status") not in {"active", "completed"}
        or profile_errors
    ):
        return [
            _finding(
                source,
                "manifest-partition-plan-profile-invalid",
                "partition plan does not satisfy the canonical Plan profile",
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


def _sample_service_predecessor_row_valid(
    predecessor_row: MigrationManifestRow,
) -> bool:
    """Keep the predecessor manifest's historical sample row immutable."""

    return (
        predecessor_row.source_path.as_posix() == SAMPLE_SERVICE_FIXTURE_PATH
        and _safe_path_text(predecessor_row.target_path) == SAMPLE_SERVICE_FIXTURE_PATH
        and predecessor_row.artifact_id == "spec:sample-web-service"
        and predecessor_row.artifact_type_before is None
        and predecessor_row.artifact_type_after == "spec"
        and predecessor_row.surface_class == "typed-example"
        and predecessor_row.status_before == "active"
        and predecessor_row.status_after == "active"
        and predecessor_row.parent_ids
        == ("spec:133-target-surface-contract-convergence",)
        and predecessor_row.disposition == "migrate"
        and predecessor_row.canonical_replacement is None
        and not predecessor_row.active_consumers
        and predecessor_row.partition_plan is None
        and predecessor_row.preservation_class is None
        and predecessor_row.evidence == ManifestEvidence((), (), (), (), ())
        and predecessor_row.review_verdict == ReviewVerdict("pass", "pass")
    )


def _sample_service_successor_handoff_valid(
    root: pathlib.Path,
    profiles: dict[str, object],
    target: str,
    target_record: Record,
    predecessor_row: MigrationManifestRow,
) -> bool:
    """Admit the exact successor-owned sample fixture without rewriting history."""

    if (
        target != SAMPLE_SERVICE_FIXTURE_PATH
        or not _sample_service_predecessor_row_valid(predecessor_row)
        or not target_record.frontmatter_present
        or target_record.metadata != SAMPLE_SERVICE_FIXTURE_METADATA
        or metadata.matching_template_roles(
            pathlib.Path(target),
            "spec",
            profiles,
        )
        != ["service"]
    ):
        return False
    return True


def _surface_result_state_findings(
    root: pathlib.Path,
    profiles: dict[str, object],
    contract: dict[str, object],
    document: MigrationManifestDocument,
    row: MigrationManifestRow,
) -> tuple[list[Finding], bool]:
    """Bind v2 result state while decoding only declared typed document targets."""

    findings: list[Finding] = []
    source = row.source_path.as_posix()
    target = _safe_path_text(row.target_path)
    if not _safe_path(source):
        return findings, False
    if row.disposition in {"move", "merge", "archive", "delete"} and os.path.lexists(
        root / source
    ):
        findings.append(
            _finding(
                source,
                "manifest-source-result-present",
                "source path remains present after a removing disposition",
            )
        )
    if row.disposition == "delete":
        return findings, not findings
    if (
        target is None
        or not _safe_path(target)
        or not _surface_regular_result_exists(root, target)
    ):
        findings.append(
            _finding(
                target or source,
                "manifest-target-missing",
                "result target is not a regular in-root file",
            )
        )
        return findings, False
    if row.surface_class not in TYPED_SURFACE_CLASSES:
        if any(
            (
                row.artifact_id is not None,
                row.artifact_type_after is not None,
                row.status_after is not None,
                bool(row.parent_ids),
            )
        ):
            findings.append(
                _finding(
                    target,
                    "manifest-target-metadata-forbidden",
                    "non-document result target cannot declare document metadata",
                )
            )
            return findings, False
        return findings, not findings
    pending_advisory_skeleton = (
        document.enforcement == "advisory"
        and row.disposition == "preserve"
        and row.review_verdict == ReviewVerdict("pending", "pending")
        and row.canonical_replacement is None
        and row.partition_plan is None
        and not any(
            (
                row.evidence.commands,
                row.evidence.sources,
                row.evidence.repository_paths,
                row.evidence.consumer_scan,
                row.evidence.rollback,
            )
        )
    )
    if pending_advisory_skeleton:
        return findings, not findings
    payload = _read_regular_repo_bytes(root, target, require_tracked=False)
    if payload is None:
        findings.append(
            _finding(
                target,
                "manifest-target-file-invalid",
                "typed result target cannot be read safely",
            )
        )
        return findings, False
    try:
        text = payload.decode("utf-8")
        target_record = metadata._record_from_text(
            pathlib.Path(target), text, profiles=profiles
        )
    except UnicodeDecodeError:
        findings.append(
            _finding(
                target,
                "manifest-target-file-invalid",
                "typed result target metadata cannot be parsed safely",
            )
        )
        return findings, False
    if target_record.parse_error:
        findings.append(
            _finding(
                target,
                "manifest-target-file-invalid",
                "typed result target metadata cannot be parsed safely",
            )
        )
        return findings, False
    target_metadata = target_record.metadata
    registered_profiles = profiles.get("profiles")
    registered_types = (
        set(registered_profiles) if isinstance(registered_profiles, dict) else set()
    )
    declared_type = target_metadata.get("type")
    target_artifact_type = (
        declared_type
        if isinstance(declared_type, str)
        and declared_type in registered_types
        and declared_type != "unsupported"
        else target_record.artifact_type
        if target_record.artifact_type in registered_types
        and target_record.artifact_type != "unsupported"
        else None
    )
    target_status = target_metadata.get("status")
    normalized_status = target_status if isinstance(target_status, str) else None
    target_parents = target_metadata.get("parent_ids")
    normalized_parents = (
        tuple(sorted(target_parents))
        if isinstance(target_parents, list)
        and all(isinstance(item, str) for item in target_parents)
        else ()
    )
    sample_successor_handoff = _sample_service_successor_handoff_valid(
        root,
        profiles,
        target,
        target_record,
        row,
    )
    sample_predecessor_status_valid = target != SAMPLE_SERVICE_FIXTURE_PATH or (
        row.status_before,
        row.status_after,
    ) == ("active", "active")
    sample_predecessor_parents_valid = (
        target != SAMPLE_SERVICE_FIXTURE_PATH
        or row.parent_ids == ("spec:133-target-surface-contract-convergence",)
    )
    if target_artifact_type != row.artifact_type_after:
        findings.append(
            _finding(
                target,
                "manifest-target-artifact-type-mismatch",
                "result target type differs from manifest truth",
            )
        )
    target_artifact_id = _manifest_artifact_id(
        target_artifact_type or "unsupported", target_metadata.get("artifact_id")
    )
    if target_artifact_id != row.artifact_id:
        findings.append(
            _finding(
                target,
                "manifest-target-artifact-id-mismatch",
                "result target identity differs from manifest truth",
            )
        )
    if not sample_predecessor_status_valid or (
        normalized_status != row.status_after and not sample_successor_handoff
    ):
        findings.append(
            _finding(
                target,
                "manifest-target-status-mismatch",
                "result target status differs from manifest truth",
            )
        )
    if not sample_predecessor_parents_valid or (
        normalized_parents != row.parent_ids and not sample_successor_handoff
    ):
        findings.append(
            _finding(
                target,
                "manifest-target-parent-ids-mismatch",
                "result target parents differ from manifest truth",
            )
        )
    if row.disposition == "migrate" and not sample_successor_handoff:
        profile_type = row.artifact_type_after
        profile_errors: list[Finding] = []
        if not isinstance(profile_type, str) or profile_type not in registered_types:
            profile_errors.append(
                _finding(
                    target,
                    "manifest-target-profile-invalid",
                    "migrated result target does not select a registered metadata profile",
                )
            )
        else:
            profile_record = dataclasses.replace(
                target_record,
                artifact_type=profile_type,
            )
            context_records = [profile_record]
            for candidate in document.entries:
                if candidate.source_path == row.source_path:
                    continue
                candidate_type = candidate.artifact_type_after
                candidate_id = candidate.artifact_id
                candidate_path = candidate.target_path or candidate.source_path
                if not isinstance(candidate_type, str) or candidate_id is None:
                    continue
                candidate_metadata: dict[str, object] = {
                    "artifact_id": candidate_id,
                    "artifact_type": candidate_type,
                    "parent_ids": list(candidate.parent_ids),
                }
                if candidate.status_after is not None:
                    candidate_metadata["status"] = candidate.status_after
                context_records.append(
                    metadata.Record(
                        pathlib.Path(candidate_path.as_posix()),
                        candidate_metadata,
                        candidate_type,
                    )
                )
            profile_errors.extend(
                finding
                for finding in metadata.validate_record(
                    profile_record,
                    profiles,
                    metadata.build_manifest(tuple(context_records)),
                )
                if finding.severity == "error"
            )
        if profile_errors:
            findings.append(
                _finding(
                    target,
                    "manifest-target-profile-invalid",
                    "migrated result target does not satisfy its canonical metadata profile",
                )
            )
    if row.artifact_type_after == "archive":
        archive_errors = [
            finding
            for finding in metadata.validate_record(
                target_record,
                profiles,
                metadata.build_manifest((target_record,)),
            )
            if finding.severity == "error"
        ]
        if archive_errors:
            findings.append(
                _finding(
                    target,
                    "manifest-archive-target-profile-invalid",
                    "archive result does not satisfy its path-selected profile",
                )
            )
        findings.extend(validate_archive_provenance(root, target_record))
    return findings, not findings


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
        tokens = [
            token.decode("utf-8") for token in changed.stdout.split(b"\0") if token
        ]
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
    if (
        not _safe_path(partition)
        or metadata.infer_artifact_type(pathlib.Path(partition), profiles) != "plan"
    ):
        return [
            _finding(
                source,
                "manifest-partition-plan-invalid",
                "partition plan must be a safe tracked regular canonical Plan",
            )
        ]
    tracked_payload = _read_regular_repo_bytes(root, partition, require_tracked=True)
    if tracked_payload is None:
        return [
            _finding(
                source,
                "manifest-partition-plan-invalid",
                "partition plan must be a safe tracked regular canonical Plan",
            )
        ]
    if records is None or payloads is None:
        current_records, current_payloads = _canonical_current_snapshot(root, profiles)
    else:
        current_records = tuple(records)
        current_payloads = dict(payloads)
    payload = current_payloads.get(partition)
    if payload is None:
        return [
            _finding(
                source,
                "manifest-partition-plan-invalid",
                "partition plan must be a safe tracked regular canonical Plan",
            )
        ]
    try:
        text = payload.decode("utf-8")
    except UnicodeDecodeError:
        return [
            _finding(
                source,
                "manifest-partition-plan-invalid",
                "partition plan must be a safe tracked regular canonical Plan",
            )
        ]
    by_path = {record.path.as_posix(): record for record in current_records}
    plan_record = by_path.get(partition)
    if plan_record is None:
        return [
            _finding(
                source,
                "manifest-partition-plan-invalid",
                "partition plan must be a safe tracked regular canonical Plan",
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
        or values.get("type") != "sdlc/plan"
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
            _finding(
                path,
                "archive-snapshot-forbidden",
                "git-history forbids snapshot fields",
            )
        )
    if preservation is None:
        findings.append(
            _finding(
                path,
                "archive-preservation-missing",
                "archive preservation class is unavailable",
            )
        )
    if commit is None:
        findings.append(
            _finding(
                path,
                "archive-commit-missing",
                "archive commit provenance is unavailable",
            )
        )
        return sorted(set(findings))
    if not OBJECT_ID.fullmatch(commit) or _git_object_type(root, commit) != "commit":
        findings.append(
            _finding(
                path, "archive-commit-invalid", "archived commit is not a commit object"
            )
        )
        return sorted(set(findings))
    if blob is None:
        findings.append(
            _finding(
                path, "archive-blob-missing", "archive blob provenance is unavailable"
            )
        )
        return sorted(set(findings))
    if not OBJECT_ID.fullmatch(blob) or _git_object_type(root, blob) != "blob":
        findings.append(
            _finding(path, "archive-blob-invalid", "archived blob is not a blob object")
        )
        return sorted(set(findings))
    if archived_from is None:
        findings.append(
            _finding(
                path, "archive-source-missing", "archived source path is unavailable"
            )
        )
        return sorted(set(findings))
    if not _safe_path(archived_from):
        findings.append(
            _finding(
                path,
                "archive-source-path-invalid",
                "archived source path is not repository-safe",
            )
        )
        return sorted(set(findings))
    resolved = _run_git(root, ["rev-parse", f"{commit}:{archived_from}"])
    if resolved.returncode != 0 or resolved.stdout.strip() != blob:
        findings.append(
            _finding(
                path,
                "archive-blob-mismatch",
                "commit path does not resolve to archived blob",
            )
        )
        return sorted(set(findings))
    blob_bytes_result = _run_git(root, ["cat-file", "blob", blob], text=False)
    if blob_bytes_result.returncode != 0:
        findings.append(
            _finding(
                path, "archive-blob-invalid", "archived blob bytes are unavailable"
            )
        )
        return sorted(set(findings))
    blob_sha256 = hashlib.sha256(blob_bytes_result.stdout).hexdigest()
    if preservation == "immutable-snapshot":
        expected_path = (
            f"docs/98.archive/evidence/{content_sha256}.md.snapshot"
            if isinstance(content_sha256, str)
            else None
        )
        if (
            snapshot_path != expected_path
            or snapshot_path is None
            or not _safe_path(snapshot_path)
        ):
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
        if any(
            pattern.search(snapshot_bytes) for pattern in SENSITIVE_PAYLOAD_PATTERNS
        ):
            findings.append(
                _finding(
                    path,
                    "archive-snapshot-confidential",
                    "snapshot matches a prohibited confidentiality class",
                )
            )
    return sorted(set(findings))


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
    excluded_values = (
        common.get("inventory_excludes") if isinstance(common, dict) else None
    )
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
            raise _CorpusSafetyError("corpus", "corpus-markdown-path-invalid") from None
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
            raise _CorpusSafetyError("corpus", "corpus-markdown-path-invalid") from None
        index += 1
        path_token: bytes
        if status_code.startswith("R"):
            if index + 1 >= len(tokens):
                raise _CorpusSafetyError("corpus", "corpus-markdown-path-invalid")
            path_token = tokens[index]
            index += 2
        elif status_code.startswith("D"):
            if index >= len(tokens):
                raise _CorpusSafetyError("corpus", "corpus-markdown-path-invalid")
            path_token = tokens[index]
            index += 1
        else:
            raise _CorpusSafetyError("corpus", "corpus-markdown-path-invalid")
        try:
            path = path_token.decode("utf-8")
        except UnicodeDecodeError:
            raise _CorpusSafetyError("corpus", "corpus-markdown-path-invalid") from None
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
    excluded_values = (
        common.get("inventory_excludes") if isinstance(common, dict) else None
    )
    excluded = set(excluded_values) if isinstance(excluded_values, list) else set()
    target_prefixes = tuple(metadata.TARGET_MARKDOWN_PREFIXES)
    candidates: list[str] = []
    for raw_path in result.stdout.split(b"\0"):
        if not raw_path:
            continue
        try:
            path = raw_path.decode("utf-8")
        except UnicodeDecodeError:
            raise _CorpusSafetyError("corpus", "corpus-markdown-path-invalid") from None
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
        payload = _read_regular_repo_bytes(root, path, require_tracked=path in tracked)
        if payload is None:
            raise _CorpusSafetyError(path, "corpus-markdown-file-invalid")
        payloads[path] = payload
    records: list[Record] = []
    for path in paths:
        try:
            text = payloads[path].decode("utf-8")
        except UnicodeDecodeError:
            raise _CorpusSafetyError(path, "corpus-markdown-file-invalid") from None
        records.append(
            metadata._record_from_text(
                pathlib.Path(path),
                text,
                profiles=profiles,
            )
        )
    return tuple(records), payloads
