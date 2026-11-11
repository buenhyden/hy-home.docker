#!/usr/bin/env python3
"""Registry profiles, shared metadata models, and path classification."""

from __future__ import annotations

import collections
import dataclasses
import datetime as dt
import fnmatch
import os
import pathlib
import re
import stat
import sys
from collections.abc import Mapping, Sequence

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

from scripts.lib.agent_governance.agent_governance_contract import (  # noqa: E402
    normalize_repo_relative_path,
)
from scripts.lib.document_governance.frontmatter import (  # noqa: E402
    read_frontmatter_values,
)
from scripts.lib.document_governance.registry import (  # noqa: E402
    DEFAULT_REGISTRY,
    DocumentRegistry,
    RegistryError,
    load_registry,
    normalize_profile_frontmatter,
)
from scripts.lib.document_governance.registry import (  # noqa: E402
    classify_path as classify_registered_path,
)
from scripts.lib.document_governance.taxonomy import (  # noqa: E402
    requirement_package_identity,
)

# Retain the validator's established public parser name while keeping the
# shared implementation imported under its canonical library name.
parse_frontmatter = read_frontmatter_values


def _normalized_document_values(
    path: pathlib.Path,
    values: Mapping[str, object],
    profiles: Mapping[str, object] | None,
) -> dict[str, object]:
    """Apply only the Registry-selected native serialization boundary."""

    registry = profiles.get("_registry") if isinstance(profiles, Mapping) else None
    if not isinstance(registry, DocumentRegistry):
        return dict(values)
    normalized = path.as_posix()
    for role in registry.template_roles.values():
        if role.get("source") == normalized:
            profile_ids = role.get("profiles", ())
            if len(profile_ids) == 1:
                return normalize_profile_frontmatter(
                    values, registry.profiles[profile_ids[0]]
                )
    profile_id = classify_registered_path(normalized, registry)
    if profile_id is None:
        return dict(values)
    return normalize_profile_frontmatter(
        values, registry.profiles[profile_id], normalized
    )


DEFAULT_PROFILES = DEFAULT_REGISTRY
DEFAULT_AGENT_GOVERNANCE_REGISTRY = ROOT / "docs/99.templates/registry.json"
TARGET_SURFACE_CLASSES = (
    "native-platform",
    "generated-output",
    "readme",
    "typed-example",
    "runtime",
    "configuration",
    "executable-script",
    "test-fixture",
    "secret-metadata",
    "content-archive",
    "unsupported-static",
)
TARGET_SURFACE_SOURCE_ROOTS = (
    ".github",
    "archive",
    "examples",
    "infra",
    "projects",
    "scripts",
    "secrets",
    "tests",
)
TARGET_SURFACE_DIRECT_SOURCE_PATHS = (
    ".env.example",
    ".pre-commit-config.yaml",
    ".prettierignore",
    "docs/03.specs/0153-workspace-governance-simplification/tasks/tsk-0004-stage00.md",
    ".agents/governance/documentation-protocol.md",
    ".agents/governance/stage-authoring-matrix.md",
    ".agents/governance/task-checklists.md",
    "docs/01.requirements/005-data-analytics.md",
    "docs/02.architecture/decisions/0015-analytics-engine-selection.md",
    "docs/02.architecture/requirements/0012-data-analytics-architecture.md",
    "docs/03.specs/0005-data-analytics/README.md",
    "docs/03.specs/0005-data-analytics/spec.md",
    "docs/03.specs/README.md",
    "docs/05.operations/guides/04-data/analytics/README.md",  # retired-route-record
    "docs/05.operations/guides/04-data/analytics/influxdb.md",  # retired-route-record
    "docs/05.operations/guides/04-data/lake-and-object/seaweedfs.md",  # retired-route-record
    "docs/05.operations/guides/09-tooling/k6.md",  # retired-route-record
    "docs/05.operations/guides/09-tooling/locust.md",  # retired-route-record
    "docs/05.operations/guides/09-tooling/performance-testing.md",  # retired-route-record
    "docs/05.operations/policies/04-data/analytics/influxdb.md",  # retired-route-record
    "docs/05.operations/policies/04-data/lake-and-object/seaweedfs.md",  # retired-route-record
    "docs/05.operations/policies/09-tooling/k6.md",  # retired-route-record
    "docs/05.operations/policies/09-tooling/locust.md",  # retired-route-record
    "docs/05.operations/policies/09-tooling/performance-testing.md",  # retired-route-record
    "docs/05.operations/runbooks/04-data/analytics/influxdb.md",  # retired-route-record
    "docs/05.operations/runbooks/09-tooling/k6.md",  # retired-route-record
    "docs/05.operations/runbooks/09-tooling/locust.md",  # retired-route-record
    "docs/05.operations/runbooks/09-tooling/performance-testing.md",  # retired-route-record
    "docs/90.references/research/ref-0039-readme.md",
    "docs/90.references/research/ref-0043-automation-pipeline-workflow.md",
    "docs/90.references/research/ref-0044-docker-compose-infrastructure.md",
    "docs/90.references/research/ref-0045-document-metadata-lifecycle.md",
    "docs/90.references/research/ref-0053-quality-ci-formatting.md",
    "docs/90.references/research/ref-0056-security-governance.md",
    "docs/90.references/research/ref-0058-workspace-baseline.md",
    "docs/99.templates/support/README.md",
    "docs/99.templates/support/archive-retention-contract.md",
    "docs/99.templates/support/common-document-contract.md",
    "docs/99.templates/support/corpus-migration-contract.md",
    "docs/99.templates/support/document-corpus-migration-contract.yaml",
    "docs/99.templates/support/document-metadata-profiles.yaml",
    "docs/99.templates/support/frontmatter-contract.md",
    "docs/99.templates/support/readme-profile-contract.md",
    "docs/99.templates/templates/README.md",
    "docs/99.templates/templates/common/README.md",
    "docs/99.templates/templates/common/archive.template.md",
)
EXPECTED_PROFILE_TYPES = {
    "adr",
    "archive",
    "architecture-description",
    "audit",
    "generated",
    "governance",
    "guide",
    "incident",
    "plan",
    "policy",
    "postmortem",
    "prd",
    "readme",
    "reference",
    "repo-support",
    "runbook",
    "srs",
    "spec",
    "task",
    "interface-requirement",
    "template-source",
    "unsupported",
}
EXPECTED_FRONTMATTER_ORDER = (
    "status",
    "artifact_id",
    "artifact_type",
    "parent_ids",
    "created",
    "updated",
    "observed_at",
    "supersedes",
    "completed_at",
    "reviewed_at",
    "next_review_at",
    "occurred_at",
    "resolved_at",
    "generated_by",
    "archived_from",
    "archived_at",
    "archive_reason",
    "archive_disposition",
    "archived_commit",
    "archived_blob",
    "preservation_class",
    "current_replacement",
    "snapshot_path",
    "content_sha256",
    "snapshot_reason",
)
TYPED_EXAMPLE_FIXTURE_PATH = "examples/sample-web-service/service.md"
TYPED_EXAMPLE_FIXTURE_STATUS = "draft"
TYPED_EXAMPLE_FIXTURE_PARENT_IDS = (
    "spec:126-security-supply-chain-remediation",
    "spec:127-deployment-release-engineering-remediation",
)
TRANSITIONAL_UNREGISTERED_TEMPLATE_SOURCES: frozenset[str] = frozenset()
TARGET_MARKDOWN_PREFIXES = (
    ".agents/",
    "labs/",
    "docs/01.requirements/",
    "docs/02.architecture/",
    "docs/03.specs/",
    "docs/05.operations/",
    "docs/90.references/",
    "docs/98.archive/",
    "docs/99.templates/",
)
TARGET_MARKDOWN_FILES = frozenset(
    {
        ".claude/provider.md",
        ".codex/provider.md",
        "tests/fixtures/README.md",
        "tests/fixtures/document_governance/README.md",
        "tests/fixtures/document_governance/operations-moves/README.md",
        "tests/fixtures/opsflow-acceptance/README.md",
    }
)
MARKDOWN_BODY_TOKEN = re.compile(r"{{[A-Z][A-Z0-9_]*}}")
MACHINE_TEMPLATE_TOKEN = re.compile(r"__[A-Z][A-Z0-9_]*__")
TARGET_TEMPLATE_LITERALS = ("<!-- Target:", "> Rules:", "## Template Usage")
MACHINE_TEMPLATE_SUFFIXES = (
    ".template.yaml",
    ".template.yml",
    ".template.graphql",
    ".template.proto",
)
MACHINE_EXAMPLE_VALUE = re.compile(
    r"(?i)(?:"
    r"\bexample(?:\.com)?\b|"
    r"https?://(?!__[A-Z][A-Z0-9_]*__)(?:[a-z0-9-]+\.)+[a-z]{2,}|"
    r"(?::|=)[ \t]*(?:bearer|basic|oauth2?|openidconnect)\b|"
    r"\b(?:bearer|basic|oauth2?|openidconnect)[ \t]+"
    r"(?!__[A-Z][A-Z0-9_]*__)[A-Za-z0-9._~+/-]+|"
    r"\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b"
    r")"
)
OPENAPI_CONCRETE_HOST = re.compile(
    r"(?i)https?://(?!__[A-Z][A-Z0-9_]*__)(?:[a-z0-9-]+\.)+[a-z]{2,}"
)
OPENAPI_BEARER_VALUE = re.compile(
    r"(?i)\b(?:bearer|basic|oauth2?|openidconnect)[ \t]+"
    r"(?!__[A-Z][A-Z0-9_]*__)[A-Za-z0-9._~+/-]+"
)
OPENAPI_JWT_VALUE = re.compile(r"\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b")
OPENAPI_AUTH_SCHEMES = frozenset(
    {"basic", "bearer", "oauth", "oauth2", "openidconnect"}
)
OPENAPI_CREDENTIAL_VALUE_KEYS = frozenset(
    {"default", "example", "examples", "const", "enum"}
)
CREDENTIAL_KEY_NAME = re.compile(
    r"(?:^|_)(?:"
    r"api_?key|password|passwd|secret|client_secret|access_token|refresh_token|"
    r"auth|authentication|authorization|credential|credentials|bearer|jwt|token"
    r")(?:_|$)",
    re.IGNORECASE,
)


class ProfileError(ValueError):
    """Raised when the machine-readable profile contract is invalid."""


class MachineTemplateParseError(ValueError):
    """Raised when a machine template cannot be parsed into its safe shape."""


@dataclasses.dataclass(frozen=True, order=True)
class Finding:
    path: str
    code: str
    message: str
    severity: str = "error"


@dataclasses.dataclass(frozen=True)
class Record:
    path: pathlib.Path
    metadata: dict[str, object]
    artifact_type: str
    previous_status: str | None = None
    parse_error: str | None = None
    parse_error_code: str | None = None
    frontmatter_present: bool = False


@dataclasses.dataclass(frozen=True)
class BaseSelection:
    source: str
    ref: str | None
    merge_base: str | None


@dataclasses.dataclass(frozen=True)
class TransitionOverride:
    path: str
    previous_status: str
    new_status: str
    evidence_task: str
    approval: str
    reason: str


@dataclasses.dataclass(frozen=True)
class OpenApiInspection:
    """Safe, value-free result of inspecting a parsed OpenAPI template."""

    concrete_credential_value: bool
    concrete_format_value: bool


class Manifest(dict[str, pathlib.Path]):
    """Dictionary-compatible ID manifest with deterministic validation context."""

    def __init__(
        self,
        values: dict[str, pathlib.Path],
        duplicates: dict[str, tuple[pathlib.Path, ...]],
        records_by_id: dict[str, Record],
        relation_records_by_id: dict[str, Record] | None = None,
        relation_conflicts: dict[str, tuple[pathlib.Path, ...]] | None = None,
    ) -> None:
        super().__init__(values)
        self.duplicates = duplicates
        self.records_by_id = records_by_id
        self.relation_records_by_id = relation_records_by_id or dict(records_by_id)
        self.relation_conflicts = relation_conflicts or {}


def registered_generated_owner(
    path: pathlib.Path,
    profiles: Mapping[str, object] | None,
) -> str | None:
    """Return the exact registry owner for a generator-owned Markdown output."""

    if not isinstance(profiles, Mapping):
        return None
    common = profiles.get("common")
    generated_outputs = (
        common.get("generated_outputs") if isinstance(common, Mapping) else None
    )
    if not isinstance(generated_outputs, Mapping):
        return None
    owner = generated_outputs.get(path.as_posix())
    return owner if isinstance(owner, str) else None


def _stage00_specialization_entry(
    path: pathlib.Path,
    contract_path: pathlib.Path = DEFAULT_AGENT_GOVERNANCE_REGISTRY,
) -> Mapping[str, object] | None:
    """Return the one Stage 99 profile registered for a canonical governance path."""

    normalized = normalize_repo_relative_path(path)
    try:
        registry = load_registry(contract_path)
    except RegistryError:
        return None
    profile_id = classify_registered_path(normalized, registry)
    if profile_id is None or not normalized.startswith(".agents/"):
        return None
    return registry.profiles.get(profile_id)


def infer_stage00_specialization(
    path: pathlib.Path,
    contract_path: pathlib.Path = DEFAULT_AGENT_GOVERNANCE_REGISTRY,
) -> str | None:
    """Infer the exact Stage 99 profile for a registered canonical governance path."""

    entry = _stage00_specialization_entry(path, contract_path)
    profile_id = entry.get("profile_id") if entry is not None else None
    return profile_id if isinstance(profile_id, str) else None


def infer_artifact_type(
    path: pathlib.Path,
    profiles: Mapping[str, object] | None = None,
) -> str:
    """Infer a supported artifact profile from a repository-relative path."""

    normalized = normalize_repo_relative_path(path)
    if requirement_package_identity(pathlib.PurePosixPath(normalized)) is not None:
        return "requirements-package"
    registry = profiles.get("_registry") if isinstance(profiles, Mapping) else None
    if isinstance(registry, DocumentRegistry):
        registered = classify_registered_path(normalized, registry)
        if registered is not None and registered != "unsupported":
            return registered
        if registered_generated_owner(pathlib.Path(normalized), profiles) is not None:
            return "generated"
        return "unsupported"
    name = pathlib.PurePosixPath(normalized).name
    if registered_generated_owner(pathlib.Path(normalized), profiles) is not None:
        return "generated"
    if name == "README.md":
        return "readme"
    if normalized.startswith("docs/99.templates/templates/") and name.endswith(
        ".template.md"
    ):
        return "template-source"
    if normalized.startswith(".agents/"):
        return "governance"
    if normalized.startswith("docs/99.templates/support/"):
        return "governance"
    if normalized.startswith("docs/98.archive/"):
        return "archive"
    if normalized.startswith("docs/01.requirements/"):
        return "requirements-package"
    if normalized.startswith("docs/02.architecture/descriptions/"):
        return "architecture-description"
    if normalized.startswith("docs/02.architecture/decisions/"):
        return "adr"
    if normalized.startswith("docs/03.specs/"):
        if name == "plan.md":
            return "plan"
        if name.startswith("tsk-"):
            return "task"
        return "spec"
    if normalized.startswith("docs/05.operations/"):
        role = {"guides": "guide", "policies": "policy", "runbooks": "runbook"}.get(
            pathlib.PurePosixPath(normalized).parts[2]
        )
        if role is not None and classify_registered_path(normalized) != role:
            return "unsupported"
        if role is not None:
            return role
    if normalized.startswith("docs/05.operations/incidents/"):
        return "postmortem" if name == "postmortem.md" else "incident"
    if normalized.startswith("docs/90.references/audits/"):
        return "audit"
    if normalized.startswith("docs/90.references/"):
        return "reference"
    return "unsupported"


def build_manifest(records: Sequence[Record]) -> dict[str, pathlib.Path]:
    """Build a deterministic artifact-ID manifest and retain duplicate context."""

    paths_by_id: dict[str, list[pathlib.Path]] = collections.defaultdict(list)
    records_by_id: dict[str, Record] = {}
    for record in sorted(records, key=lambda item: item.path.as_posix()):
        artifact_id = record.metadata.get("artifact_id")
        if not isinstance(artifact_id, str) or not artifact_id.strip():
            continue
        normalized_id = artifact_id.strip()
        paths_by_id[normalized_id].append(record.path)
        records_by_id.setdefault(normalized_id, record)
    values = {
        artifact_id: sorted(paths)[0]
        for artifact_id, paths in sorted(paths_by_id.items())
    }
    duplicates = {
        artifact_id: tuple(sorted(paths))
        for artifact_id, paths in sorted(paths_by_id.items())
        if len(paths) > 1
    }
    relation_candidates: dict[str, list[Record]] = collections.defaultdict(list)
    for record in sorted(records, key=lambda item: item.path.as_posix()):
        artifact_id = record.metadata.get("artifact_id")
        if isinstance(artifact_id, str) and artifact_id.strip():
            relation_candidates[artifact_id.strip()].append(record)

    relation_records_by_id: dict[str, Record] = {}
    relation_conflicts: dict[str, tuple[pathlib.Path, ...]] = {}
    for relation_id, candidates in sorted(relation_candidates.items()):
        unique = {candidate.path.as_posix(): candidate for candidate in candidates}
        if len(unique) == 1:
            relation_records_by_id[relation_id] = next(iter(unique.values()))
        else:
            relation_conflicts[relation_id] = tuple(
                sorted(candidate.path for candidate in unique.values())
            )

    return Manifest(
        values,
        duplicates,
        records_by_id,
        relation_records_by_id,
        relation_conflicts,
    )


def _profile_mapping(
    profiles: dict[str, object],
) -> tuple[dict[str, object], dict[str, object]]:
    common = profiles.get("common", {})
    profile_map = profiles.get("profiles", {})
    if not isinstance(common, dict) or not isinstance(profile_map, dict):
        raise ProfileError("common and profiles must be mappings")
    return common, profile_map


def build_current_manifest(
    root: pathlib.Path, records: Sequence[Record]
) -> dict[str, pathlib.Path]:
    """Current records only: typed references never cite a retired identity."""

    return build_manifest(records)


def _finding(
    record: Record, code: str, message: str, severity: str = "error"
) -> Finding:
    return Finding(record.path.as_posix(), code, message, severity)


def _string_list(value: object) -> list[str] | None:
    if not isinstance(value, list) or not all(
        isinstance(item, str) and item.strip() for item in value
    ):
        return None
    return [item.strip() for item in value]


DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")
DATETIME_RE = re.compile(
    r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})"
)
LOWERCASE_OBJECT_ID_RE = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})")
LOWERCASE_SHA256_RE = re.compile(r"[0-9a-f]{64}")


def _valid_iso_date(value: object) -> bool:
    if isinstance(value, dt.datetime):
        return False
    if isinstance(value, dt.date):
        return True
    if not isinstance(value, str) or DATE_RE.fullmatch(value) is None:
        return False
    try:
        dt.date.fromisoformat(value)
    except ValueError:
        return False
    return True


def _valid_iso_temporal(value: object) -> bool:
    if _valid_iso_date(value):
        return True
    if isinstance(value, dt.datetime):
        return value.tzinfo is not None
    if not isinstance(value, str) or DATETIME_RE.fullmatch(value) is None:
        return False
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None


def _safe_repo_path(value: object, required_prefix: str | None = None) -> bool:
    if not isinstance(value, str) or not value or "\\" in value or "://" in value:
        return False
    pure = pathlib.PurePosixPath(value)
    if (
        pure.is_absolute()
        or value != pure.as_posix()
        or any(part in {"", ".", ".."} for part in pure.parts)
    ):
        return False
    return required_prefix is None or value.startswith(required_prefix)


def _valid_lowercase_object_id(value: object) -> bool:
    return (
        isinstance(value, str) and LOWERCASE_OBJECT_ID_RE.fullmatch(value) is not None
    )


def _valid_lowercase_sha256(value: object) -> bool:
    return isinstance(value, str) and LOWERCASE_SHA256_RE.fullmatch(value) is not None


def _valid_metadata_artifact_id(value: object) -> bool:
    """Apply the canonical metadata validator's artifact-ID value rule."""

    return isinstance(value, str) and bool(value.strip())


def _safe_snapshot_path(value: object) -> bool:
    return (
        _safe_repo_path(value, "docs/98.archive/evidence/")
        and isinstance(value, str)
        and value.endswith(".md.snapshot")
    )


def _condition_members(
    profile: Mapping[str, object],
    group: str,
    field: str,
) -> set[str]:
    conditions = profile.get("conditions", {})
    condition_group = conditions.get(group, {}) if isinstance(conditions, dict) else {}
    values = condition_group.get(field, []) if isinstance(condition_group, dict) else []
    return set(values) if isinstance(values, list) else set()


def _readme_globs_overlap(left: str, right: str) -> bool:
    left_parts = pathlib.PurePosixPath(left).parts
    right_parts = pathlib.PurePosixPath(right).parts
    if len(left_parts) != len(right_parts):
        return False
    return all(
        left_part == right_part or left_part == "*" or right_part == "*"
        for left_part, right_part in zip(left_parts, right_parts, strict=True)
    )


def _readme_glob_matches(path: pathlib.PurePosixPath, pattern: str) -> bool:
    path_parts = path.parts
    pattern_parts = pathlib.PurePosixPath(pattern).parts
    return len(path_parts) == len(pattern_parts) and all(
        pattern_part == "*" or pattern_part == path_part
        for path_part, pattern_part in zip(path_parts, pattern_parts, strict=True)
    )


def _safe_target_glob(value: object) -> bool:
    if not isinstance(value, str) or not value or "\\" in value or "://" in value:
        return False
    pure = pathlib.PurePosixPath(value)
    if pure.is_absolute() or value != pure.as_posix() or not value.endswith(".md"):
        return False
    if any(part in {"", ".", ".."} for part in pure.parts):
        return False
    without_digit_classes = value.replace("[0-9]", "")
    if any(marker in without_digit_classes for marker in "?[]{}"):
        return False
    return all(
        "***" not in part and ("**" not in part or part == "**") for part in pure.parts
    )


def _target_glob_matches(path: pathlib.PurePosixPath, pattern: str) -> bool:
    path_parts = path.parts
    pattern_parts = pathlib.PurePosixPath(pattern).parts

    def matches(path_index: int, pattern_index: int) -> bool:
        if pattern_index == len(pattern_parts):
            return path_index == len(path_parts)
        pattern_part = pattern_parts[pattern_index]
        if pattern_part == "**":
            return any(
                matches(candidate, pattern_index + 1)
                for candidate in range(path_index, len(path_parts) + 1)
            )
        return (
            path_index < len(path_parts)
            and fnmatch.fnmatchcase(path_parts[path_index], pattern_part)
            and matches(path_index + 1, pattern_index + 1)
        )

    return matches(0, 0)


def _target_glob_specificity(pattern: str) -> tuple[int, int, int]:
    parts = pathlib.PurePosixPath(pattern).parts
    literal_characters = sum(len(part.replace("*", "")) for part in parts)
    wildcard_count = sum(part.count("*") for part in parts)
    return literal_characters, -wildcard_count, len(parts)


def _segment_glob_tokens(pattern: str) -> tuple[str | frozenset[str], ...]:
    """Tokenize the bounded segment grammar accepted by `_safe_target_glob`."""

    tokens: list[str | frozenset[str]] = []
    index = 0
    while index < len(pattern):
        if pattern.startswith("[0-9]", index):
            tokens.append(frozenset("0123456789"))
            index += len("[0-9]")
        else:
            tokens.append(pattern[index])
            index += 1
    return tuple(tokens)


def _glob_token_witness(
    left: str | frozenset[str],
    right: str | frozenset[str],
) -> str | None:
    left_values = left if isinstance(left, frozenset) else frozenset({left})
    right_values = right if isinstance(right, frozenset) else frozenset({right})
    common = sorted(left_values & right_values)
    return common[0] if common else None


def _segment_glob_intersection_witness(left: str, right: str) -> str | None:
    """Return one non-empty segment matched by both bounded target globs."""

    left_tokens = _segment_glob_tokens(left)
    right_tokens = _segment_glob_tokens(right)
    queue = collections.deque([(0, 0, "")])
    visited: set[tuple[int, int, bool]] = set()
    while queue:
        left_index, right_index, witness = queue.popleft()
        state = (left_index, right_index, bool(witness))
        if state in visited:
            continue
        visited.add(state)
        if left_index == len(left_tokens) and right_index == len(right_tokens):
            if witness:
                return witness
            continue

        left_star = left_index < len(left_tokens) and left_tokens[left_index] == "*"
        right_star = (
            right_index < len(right_tokens) and right_tokens[right_index] == "*"
        )
        if left_star:
            queue.append((left_index + 1, right_index, witness))
        if right_star:
            queue.append((left_index, right_index + 1, witness))

        if left_index >= len(left_tokens) or right_index >= len(right_tokens):
            continue
        if left_star and right_star:
            queue.append((left_index, right_index, witness + "x"))
        elif left_star:
            right_token = right_tokens[right_index]
            sample = "0" if isinstance(right_token, frozenset) else right_token
            queue.append((left_index, right_index + 1, witness + sample))
        elif right_star:
            left_token = left_tokens[left_index]
            sample = "0" if isinstance(left_token, frozenset) else left_token
            queue.append((left_index + 1, right_index, witness + sample))
        elif (
            sample := _glob_token_witness(
                left_tokens[left_index], right_tokens[right_index]
            )
        ) is not None:
            queue.append((left_index + 1, right_index + 1, witness + sample))
    return None


def _target_glob_intersection_witness(left: str, right: str) -> str | None:
    """Return one path matched by both safe target globs, if one exists."""

    left_parts = pathlib.PurePosixPath(left).parts
    right_parts = pathlib.PurePosixPath(right).parts
    queue = collections.deque([(0, 0, ())])
    visited: set[tuple[int, int]] = set()
    while queue:
        left_index, right_index, witness = queue.popleft()
        state = (left_index, right_index)
        if state in visited:
            continue
        visited.add(state)
        if left_index == len(left_parts) and right_index == len(right_parts):
            return pathlib.PurePosixPath(*witness).as_posix()

        left_globstar = left_index < len(left_parts) and left_parts[left_index] == "**"
        right_globstar = (
            right_index < len(right_parts) and right_parts[right_index] == "**"
        )
        if left_globstar:
            queue.append((left_index + 1, right_index, witness))
        if right_globstar:
            queue.append((left_index, right_index + 1, witness))

        if left_index >= len(left_parts) or right_index >= len(right_parts):
            continue
        segment: str | None = None
        next_left = left_index + 1
        next_right = right_index + 1
        if left_globstar and right_globstar:
            continue
        if left_globstar:
            segment = _segment_glob_intersection_witness("*", right_parts[right_index])
            next_left = left_index
        elif right_globstar:
            segment = _segment_glob_intersection_witness(left_parts[left_index], "*")
            next_right = right_index
        else:
            segment = _segment_glob_intersection_witness(
                left_parts[left_index], right_parts[right_index]
            )
        if segment is not None:
            queue.append((next_left, next_right, (*witness, segment)))
    return None


def matching_template_roles(
    path: pathlib.Path,
    artifact_type: str,
    profiles: dict[str, object],
) -> list[str]:
    """Return sorted template roles matching one target path and profile."""

    normalized = pathlib.PurePosixPath(path.as_posix())
    if normalized.is_absolute() or any(
        part in {"", ".", ".."} for part in normalized.parts
    ):
        return []
    registry = profiles.get("_registry")
    if isinstance(registry, DocumentRegistry):
        registered_profile = classify_registered_path(normalized, registry)
        if registered_profile != artifact_type:
            return []
    common = profiles.get("common", {})
    excluded = common.get("inventory_excludes", []) if isinstance(common, dict) else []
    if normalized.as_posix() in excluded:
        return []
    template_roles = profiles.get("template_roles", {})
    if not isinstance(template_roles, dict):
        return []
    scores: dict[str, tuple[int, int, int]] = {}
    for name, role in template_roles.items():
        if not isinstance(name, str) or not isinstance(role, dict):
            continue
        if role.get("artifact_profile") != artifact_type:
            continue
        patterns = role.get("target_globs", [])
        if not isinstance(patterns, list):
            continue
        matched_scores = [
            _target_glob_specificity(pattern)
            for pattern in patterns
            if isinstance(pattern, str) and _target_glob_matches(normalized, pattern)
        ]
        if matched_scores:
            scores[name] = max(matched_scores)
    if not scores:
        return []
    best = max(scores.values())
    return sorted(name for name, score in scores.items() if score == best)


def classify_template_role(
    path: pathlib.Path,
    artifact_type: str,
    profiles: dict[str, object],
) -> str:
    """Return one role or raise ProfileError for zero or ambiguous matches."""

    matches = matching_template_roles(path, artifact_type, profiles)
    normalized = path.as_posix()
    if not matches:
        raise ProfileError(
            f"template role is unclassified: {normalized}; artifact_profile={artifact_type}"
        )
    if len(matches) > 1:
        raise ProfileError(
            f"template role is ambiguous: {normalized}; roles={','.join(matches)}"
        )
    return matches[0]


NON_TARGET_PROFILE_IDS = frozenset(
    {
        "generated",
        "governance-hook-policy",
        "governance-policy",
        "governance-provider",
        "governance-provider-index",
        "governance-role",
        "governance-sdlc",
        "governance-skill",
        "readme",
        "runtime-projection-claude",
        "runtime-projection-codex",
        "template-source",
        "unsupported",
    }
)


def _typed_target_types(profiles: dict[str, object]) -> set[str]:
    """Registry profiles that own a typed authoring target.

    Canonical governance profiles and the provider-owned runtime projections are
    not SDLC targets: their section contract is enforced from the Registry
    profile directly, whether or not the profile also registers a template.
    """

    registry = profiles.get("_registry")
    if not isinstance(registry, DocumentRegistry):
        return set()
    return {
        profile_id
        for profile_id in registry.profiles
        if profile_id not in NON_TARGET_PROFILE_IDS
    }


def _relation_record(
    manifest: Manifest,
    artifact_id: str,
    referencing_record: Record | None = None,
) -> Record | None:
    """Resolve one exact, unambiguous artifact ID for a relation."""
    if artifact_id in manifest.relation_conflicts:
        return None
    return manifest.relation_records_by_id.get(artifact_id)


def _relation_reference_exists(
    manifest: Manifest,
    artifact_id: str,
    referencing_record: Record | None = None,
) -> bool:
    """Return whether one exact, unambiguous artifact ID is resolvable."""

    return artifact_id not in manifest.relation_conflicts and (
        artifact_id in manifest.relation_records_by_id or artifact_id in manifest
    )


def _relation_ids_for_record(record: Record) -> frozenset[str]:
    relation_ids: set[str] = set()
    artifact_id = record.metadata.get("artifact_id")
    if isinstance(artifact_id, str) and artifact_id.strip():
        relation_ids.add(artifact_id.strip())
    return frozenset(relation_ids)


def _has_parent_cycle(
    record: Record, parent_ids: list[str], manifest: Manifest
) -> bool:
    relation_ids = _relation_ids_for_record(record)
    if not relation_ids:
        return False
    pending = list(parent_ids)
    referrers = [record for _ in parent_ids]
    visited: set[str] = set()
    while pending:
        candidate = pending.pop()
        referrer = referrers.pop()
        if candidate in relation_ids:
            return True
        if candidate in visited:
            continue
        visited.add(candidate)
        parent_record = _relation_record(manifest, candidate, referrer)
        if parent_record is None:
            continue
        nested = _string_list(parent_record.metadata.get("parent_ids"))
        if nested:
            pending.extend(nested)
            referrers.extend(parent_record for _ in nested)
    return False


def _template_placeholder_values(profiles: dict[str, object]) -> dict[str, str]:
    common, _ = _profile_mapping(profiles)
    values = common.get("template_placeholders", {})
    return dict(values) if isinstance(values, dict) else {}


def _template_angle_tokens(profiles: dict[str, object]) -> set[str]:
    return {
        token
        for value in _template_placeholder_values(profiles).values()
        for token in re.findall(r"{{[A-Z][A-Z0-9_]*}}", value)
    }


def _contains_template_placeholder(value: object, angle_tokens: set[str]) -> bool:
    if isinstance(value, str):
        return any(token in value for token in angle_tokens)
    if isinstance(value, list):
        return any(_contains_template_placeholder(item, angle_tokens) for item in value)
    if isinstance(value, dict):
        return any(
            _contains_template_placeholder(item, angle_tokens)
            for item in value.values()
        )
    return False


def _exact_string_list(
    value: object,
    expected: Sequence[str],
    field: str,
) -> list[str]:
    if not isinstance(value, list) or not all(
        isinstance(item, str) and item for item in value
    ):
        raise ProfileError(f"{field} must be a list of non-empty strings")
    if len(value) != len(set(value)):
        raise ProfileError(f"{field} must not contain duplicates")
    if tuple(value) != tuple(expected):
        raise ProfileError(f"{field} must define the exact canonical values")
    return value


def _safe_contract_path(value: object) -> bool:
    return (
        _safe_repo_path(value)
        and isinstance(value, str)
        and not any(marker in value for marker in "*?[]{}")
    )


CANONICAL_PARTITION_PLAN_PATH = re.compile(
    r"docs/03\.specs/[0-9]{4}-[a-z0-9](?:[a-z0-9-]*[a-z0-9])?/plan\.md"
)


def load_profiles(
    path: pathlib.Path = DEFAULT_PROFILES,
) -> Mapping[str, Mapping[str, object]]:
    """Return the Registry profile map. The Registry is the only profile input."""

    if path.suffix.lower() != ".json":
        raise ProfileError("profiles must be the Stage 99 JSON registry")
    try:
        return load_registry(path).profiles
    except RegistryError as error:
        raise ProfileError(str(error)) from error


def _thaw(value: object) -> object:
    """Return a mutable deep copy of a frozen Registry member.

    `load_registry` returns nested `mappingproxy` values, which `copy.deepcopy`
    cannot pickle, and metadata consumers assign into `common` at run time.
    """

    if isinstance(value, Mapping):
        return {str(key): _thaw(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_thaw(item) for item in value]
    return value


def build_registry_profiles(registry: DocumentRegistry) -> dict[str, object]:
    """Project the Registry into the envelope the metadata readers consume.

    The Registry is the only authority here: profiles, template roles, and the
    shared `common` metadata contract all come from `registry.json`.
    """

    common = _thaw(registry.common)
    assert isinstance(common, dict)
    for key in ("typed_keys", "frontmatter_order"):
        values = common.get(key)
        if isinstance(values, list) and "type" not in values:
            common[key] = ["type", *values]
    adapted: dict[str, object] = {"common": common}
    translated: dict[str, object] = {}
    for profile_id, profile in registry.profiles.items():
        lifecycle_id = profile.get("lifecycle_id")
        statuses = (
            list(registry.lifecycles[lifecycle_id])
            if isinstance(lifecycle_id, str) and lifecycle_id in registry.lifecycles
            else []
        )
        initial_status = (
            registry.lifecycle_initial_statuses.get(lifecycle_id)
            if isinstance(lifecycle_id, str)
            else None
        )
        terminal_statuses = (
            list(registry.lifecycle_terminal_statuses.get(lifecycle_id, ()))
            if isinstance(lifecycle_id, str)
            else []
        )
        traceability = profile.get("traceability")
        parents = (
            list(traceability.get("allowed_parent_profiles", ()))
            if isinstance(traceability, Mapping)
            else []
        )
        transitions = (
            {
                status: list(targets)
                for status, targets in registry.transitions.get(profile_id, {}).items()
            }
            if profile_id in registry.transitions
            else {}
        )
        translated[profile_id] = {
            "type": profile.get("type"),
            "frontmatter_values": _thaw(profile.get("frontmatter_values", {})),
            "frontmatter_routes": _thaw(profile.get("frontmatter_routes", {})),
            "required_frontmatter_by_status": _thaw(
                profile.get("required_frontmatter_by_status", {})
            ),
            "required": list(profile.get("required_frontmatter", ())),
            "optional": list(profile.get("optional_frontmatter", ())),
            "forbidden": [],
            "allowed_statuses": statuses,
            "initial_status": initial_status,
            "terminal_statuses": terminal_statuses,
            "allowed_parent_types": parents,
            "allow_empty_parents": (
                # Operations documents may be workspace roots with no parent.
                profile_id
                in {"research", "audit", "data", "guide", "policy", "runbook"}
                or not parents
            ),
            "allow_additional": False,
            "disposition": "registry-canonical",
            # Carried through so a consumer can tell a managed authoring target
            # from a preserved record whose contract was met while it was live.
            "frontmatter_policy": profile.get("frontmatter_policy"),
            "path_pattern": profile.get("path_pattern"),
            "additional_path_patterns": profile.get("additional_path_patterns", ()),
            "additional_paths": profile.get("additional_paths", ()),
            "artifact_id_pattern": profile.get("artifact_id_pattern"),
            "identity_relation": profile.get("identity_relation"),
            "transitions": transitions,
            # Carried through so consumers can see a provider-owned binding.
            "exceptions": profile.get("exceptions", ()),
        }
    adapted["profiles"] = translated
    projected_roles: dict[str, object] = {}
    for role_id, role in registry.template_roles.items():
        profile_ids = role.get("profiles")
        profile_id = (
            profile_ids[0]
            if isinstance(profile_ids, Sequence)
            and not isinstance(profile_ids, (str, bytes, bytearray))
            and profile_ids
            else None
        )
        profile = registry.profiles.get(str(profile_id))
        path_pattern = (
            profile.get("path_pattern") if isinstance(profile, Mapping) else None
        )
        if not isinstance(profile, Mapping) or not isinstance(path_pattern, str):
            continue
        additional_paths = profile.get("additional_paths", ())
        target_patterns = [path_pattern, *profile.get("additional_path_patterns", ())]
        if isinstance(additional_paths, Sequence) and not isinstance(
            additional_paths, (str, bytes, bytearray)
        ):
            target_patterns.extend(
                path for path in additional_paths if isinstance(path, str)
            )
        projected_roles[role_id] = {
            "source": role.get("source"),
            "artifact_profile": profile_id,
            "target_globs": [
                _registry_path_glob(pattern)
                for pattern in dict.fromkeys(target_patterns)
            ],
            "required_headings": [
                f"## {section}" for section in profile.get("required_sections", ())
            ],
            "conditional_headings": [
                f"## {section}" for section in profile.get("optional_sections", ())
            ],
            "forbidden_headings": [],
        }
    adapted["template_roles"] = projected_roles
    adapted["_registry"] = registry
    return adapted


def _registry_path_glob(pattern: str) -> str:
    rendered = re.sub(r"\{[^{}]+:4\}", "[0-9][0-9][0-9][0-9]", pattern)
    return re.sub(
        r"\{(?:slug|domain|stage|hook_slug|category)\}",
        "*",
        rendered.replace("{subpath}", "**"),
    )


def _normalized_target_path(path_text: str) -> pathlib.Path | None:
    if not path_text.endswith(".md") or "\\" in path_text:
        return None
    pure = pathlib.PurePosixPath(path_text)
    if pure.is_absolute() or any(part in {"", ".", ".."} for part in pure.parts):
        return None
    normalized = pure.as_posix()
    runtime_readme = normalized.startswith("infra/") and pure.name == "README.md"
    if (
        not runtime_readme
        and normalized not in TARGET_MARKDOWN_FILES
        and not normalized.startswith(TARGET_MARKDOWN_PREFIXES)
    ):
        return None
    return pathlib.Path(normalized)
