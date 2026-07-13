#!/usr/bin/env python3
"""Validate typed Markdown metadata and render an advisory inventory."""

from __future__ import annotations

import argparse
import collections
import dataclasses
import datetime as dt
import fnmatch
import os
import pathlib
import re
import subprocess
import sys
from collections.abc import Mapping, Sequence
from typing import Any

import yaml


ROOT = pathlib.Path(__file__).resolve().parents[2]
DEFAULT_PROFILES = ROOT / "docs/99.templates/support/document-metadata-profiles.yaml"
EXPECTED_PROFILE_TYPES = {
    "adr",
    "archive",
    "ard",
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
    "release",
    "repo-support",
    "runbook",
    "spec",
    "task",
    "template-source",
    "unsupported",
}
EXPECTED_FRONTMATTER_ORDER = (
    "status",
    "artifact_id",
    "artifact_type",
    "parent_ids",
    "supersedes",
    "reviewed_at",
    "review_cycle",
    "generated_by",
    "archived_from",
    "archived_on",
    "archive_reason",
    "current_replacement",
)
EXPECTED_DOCUMENT_FAMILIES = {
    "sdlc": (
        "prd",
        "ard",
        "adr",
        "spec",
        "plan",
        "task",
        "guide",
        "policy",
        "runbook",
        "incident",
        "postmortem",
        "release",
    ),
    "common": (
        "reference",
        "audit",
        "archive",
        "readme",
        "governance",
        "generated",
        "template-source",
        "repo-support",
        "unsupported",
    ),
}
README_PROFILE_KEYS = frozenset(
    {
        "path_globs",
        "frontmatter",
        "frontmatter_consumer",
        "allowed_frontmatter_keys",
        "required_headings",
        "optional_headings",
        "forbidden_headings",
        "allowed_local_content_role",
        "canonical_shared_rule_owner",
    }
)
README_FRONTMATTER_ALLOWED_KEYS = frozenset({"status", "layer", "generated_by", "runtime"})
TEMPLATE_ROLE_KEYS = frozenset(
    {
        "source",
        "artifact_profile",
        "target_globs",
        "required_headings",
        "conditional_headings",
        "forbidden_headings",
    }
)
EXPECTED_TEMPLATE_ROLE_NAMES = frozenset(
    {
        "adr",
        "agent-design",
        "api-spec",
        "archive",
        "ard",
        "audit",
        "data-model",
        "guide",
        "incident",
        "memory",
        "plan",
        "policy",
        "postmortem",
        "prd",
        "progress",
        "readme",
        "reference",
        "release",
        "runbook",
        "service",
        "spec",
        "task",
        "tests",
    }
)
TRANSITIONAL_UNREGISTERED_TEMPLATE_SOURCES: frozenset[str] = frozenset()
TARGET_MARKDOWN_PREFIXES = (
    "docs/00.agent-governance/",
    "docs/01.requirements/",
    "docs/02.architecture/",
    "docs/03.specs/",
    "docs/04.execution/",
    "docs/05.operations/",
    "docs/90.references/",
    "docs/98.archive/",
    "docs/99.templates/",
)
MIGRATION_TYPED_KEYS = frozenset(
    {"artifact_id", "artifact_type", "parent_ids", "supersedes", "reviewed_at", "review_cycle"}
)
APPROVED_MIGRATION_PATHS = frozenset(
    {
        "docs/03.specs/123-agentic-engineering-audit-remediation/README.md",
        "docs/03.specs/123-agentic-engineering-audit-remediation/spec.md",
        "docs/04.execution/plans/2026-07-11-agentic-engineering-audit-remediation.md",
        "docs/04.execution/tasks/2026-07-11-agentic-engineering-audit-remediation.md",
        "docs/90.references/research/2026-07-05-agentic-research-pack-refresh/README.md",
        "docs/90.references/research/2026-07-05-agentic-research-pack-refresh/document-metadata-lifecycle.md",
        "docs/90.references/research/2026-07-05-agentic-research-pack-refresh/agent-instructions-vibe-coding.md",
        "docs/90.references/research/2026-07-05-agentic-research-pack-refresh/workspace-baseline.md",
        "docs/90.references/research/2026-07-05-agentic-research-pack-refresh/harness-engineering.md",
        "docs/90.references/research/2026-07-05-agentic-research-pack-refresh/loop-engineering.md",
        "docs/90.references/research/2026-07-05-agentic-research-pack-refresh/provider-implementation-comparison.md",
        "docs/90.references/research/2026-07-05-agentic-research-pack-refresh/provider-model-landscape.md",
        "docs/90.references/research/2026-07-05-agentic-research-pack-refresh/agent-model-selection.md",
        "docs/90.references/research/2026-07-05-agentic-research-pack-refresh/ai-agent-catalogs.md",
        "docs/90.references/research/2026-07-05-agentic-research-pack-refresh/spec-driven-sdlc.md",
        "docs/90.references/research/2026-07-05-agentic-research-pack-refresh/sdlc-document-roles.md",
        "docs/90.references/research/2026-07-05-agentic-research-pack-refresh/quality-ci-formatting.md",
        "docs/90.references/research/2026-07-05-agentic-research-pack-refresh/docker-compose-infrastructure.md",
        "docs/90.references/research/2026-07-05-agentic-research-pack-refresh/security-governance.md",
        "docs/90.references/research/2026-07-05-agentic-research-pack-refresh/automation-pipeline-workflow.md",
        "docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/README.md",
        "docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/implementation-overview.md",
        "docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/harness-engineering-implementation.md",
        "docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/loop-engineering-implementation.md",
        "docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/provider-harness-loop-implementation.md",
        "docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/workspace-rules-environment-implementation.md",
        "docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/sdlc-document-contracts-implementation.md",
        "docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/frontmatter-template-readme-implementation.md",
        "docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/sdlc-quality-formatting-implementation.md",
        "docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md",
        "docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/compose-infrastructure-operations-readiness.md",
        "docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/security-framework-maturity.md",
        "docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/agent-instructions-catalog-vibe-models.md",
        "docs/99.templates/templates/sdlc/prd.template.md",
        "docs/99.templates/templates/sdlc/ard.template.md",
        "docs/99.templates/templates/sdlc/adr.template.md",
        "docs/99.templates/templates/sdlc/spec.template.md",
        "docs/99.templates/templates/sdlc/plan.template.md",
        "docs/99.templates/templates/sdlc/task.template.md",
        "docs/99.templates/templates/operations/guide.template.md",
        "docs/99.templates/templates/operations/policy.template.md",
        "docs/99.templates/templates/operations/runbook.template.md",
        "docs/99.templates/templates/operations/incident.template.md",
        "docs/99.templates/templates/operations/postmortem.template.md",
        "docs/99.templates/templates/common/reference.template.md",
        "docs/99.templates/templates/common/readme.template.md",
        "docs/99.templates/templates/common/archive.template.md",
    }
)
LEGACY_EXCEPTION_CODES = frozenset(
    {"missing-required-key", "replacement-free-supersession", "stale-active"}
)
EXPECTED_TEMPLATE_PLACEHOLDER_KEYS = frozenset(
    {
        "artifact_id",
        "parent_id",
        "reviewed_at",
        "review_cycle",
        "archived_from",
        "archived_on",
        "archive_reason",
        "current_replacement",
    }
)


class FrontmatterError(ValueError):
    """Raised when a Markdown frontmatter block cannot be parsed safely."""

    def __init__(self, message: str, code: str = "malformed-yaml") -> None:
        self.code = code
        super().__init__(message)


class ProfileError(ValueError):
    """Raised when the machine-readable profile contract is invalid."""


class UniqueKeyLoader(yaml.SafeLoader):
    """PyYAML safe loader that rejects duplicate mapping keys."""


def _construct_unique_mapping(
    loader: UniqueKeyLoader,
    node: yaml.nodes.MappingNode,
    deep: bool = False,
) -> dict[object, object]:
    mapping: dict[object, object] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            duplicate = key in mapping
        except TypeError as error:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                "mapping key must be a hashable scalar",
                key_node.start_mark,
            ) from error
        if duplicate:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                f"duplicate key: {key!r}",
                key_node.start_mark,
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_unique_mapping,
)


def _safe_load_unique(source: str) -> object:
    """Apply duplicate-key rejection, then parse with PyYAML safe_load."""

    yaml.load(source, Loader=UniqueKeyLoader)
    return yaml.safe_load(source)


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


class Manifest(dict[str, pathlib.Path]):
    """Dictionary-compatible ID manifest with deterministic validation context."""

    def __init__(
        self,
        values: dict[str, pathlib.Path],
        duplicates: dict[str, tuple[pathlib.Path, ...]],
        records_by_id: dict[str, Record],
    ) -> None:
        super().__init__(values)
        self.duplicates = duplicates
        self.records_by_id = records_by_id


def _parse_frontmatter_text(text: str) -> dict[str, object]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    closing = next((index for index in range(1, len(lines)) if lines[index].strip() == "---"), None)
    if closing is None:
        raise FrontmatterError("opening frontmatter fence has no closing fence")
    source = "\n".join(lines[1:closing])
    try:
        loaded = _safe_load_unique(source)
    except yaml.YAMLError as error:
        summary = str(error).splitlines()[0]
        code = "duplicate-key" if getattr(error, "problem", "").startswith("duplicate key:") else "malformed-yaml"
        raise FrontmatterError(f"invalid YAML frontmatter: {summary}", code=code) from error
    if loaded is None:
        return {}
    if not isinstance(loaded, dict) or not all(isinstance(key, str) for key in loaded):
        raise FrontmatterError("frontmatter must be a string-keyed YAML mapping", code="malformed-yaml")
    return dict(loaded)


def parse_frontmatter(path: pathlib.Path) -> dict[str, object]:
    """Return top-of-file YAML frontmatter, or an empty mapping when absent."""

    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise FrontmatterError(f"cannot read UTF-8 Markdown: {error}") from error
    return _parse_frontmatter_text(text)


def infer_artifact_type(path: pathlib.Path) -> str:
    """Infer a supported artifact profile from a repository-relative path."""

    normalized = path.as_posix().lstrip("./")
    name = pathlib.PurePosixPath(normalized).name
    if name == "README.md":
        return "readme"
    if normalized.startswith("docs/99.templates/templates/") and name.endswith(".template.md"):
        return "template-source"
    if normalized.startswith("docs/00.agent-governance/"):
        return "governance"
    if normalized.startswith("docs/99.templates/support/"):
        return "governance"
    if normalized.startswith("docs/98.archive/"):
        return "archive"
    if normalized.startswith("docs/01.requirements/"):
        return "prd"
    if normalized.startswith("docs/02.architecture/requirements/"):
        return "ard"
    if normalized.startswith("docs/02.architecture/decisions/"):
        return "adr"
    if normalized.startswith("docs/03.specs/"):
        return "spec"
    if normalized.startswith("docs/04.execution/plans/"):
        return "plan"
    if normalized.startswith("docs/04.execution/tasks/"):
        return "task"
    if normalized.startswith("docs/05.operations/guides/"):
        return "guide"
    if normalized.startswith("docs/05.operations/policies/"):
        return "policy"
    if normalized.startswith("docs/05.operations/runbooks/"):
        return "runbook"
    if normalized.startswith("docs/05.operations/incidents/"):
        return "postmortem" if name == "postmortem.md" else "incident"
    if normalized.startswith("docs/05.operations/releases/"):
        return "release"
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
    values = {artifact_id: sorted(paths)[0] for artifact_id, paths in sorted(paths_by_id.items())}
    duplicates = {
        artifact_id: tuple(sorted(paths))
        for artifact_id, paths in sorted(paths_by_id.items())
        if len(paths) > 1
    }
    return Manifest(values, duplicates, records_by_id)


def _profile_mapping(profiles: dict[str, object]) -> tuple[dict[str, object], dict[str, object]]:
    common = profiles.get("common", {})
    profile_map = profiles.get("profiles", {})
    if not isinstance(common, dict) or not isinstance(profile_map, dict):
        raise ProfileError("common and profiles must be mappings")
    return common, profile_map


def _finding(record: Record, code: str, message: str, severity: str = "error") -> Finding:
    return Finding(record.path.as_posix(), code, message, severity)


def _string_list(value: object) -> list[str] | None:
    if not isinstance(value, list) or not all(isinstance(item, str) and item.strip() for item in value):
        return None
    return [item.strip() for item in value]


DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")
DATETIME_RE = re.compile(
    r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})"
)


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
    if pure.is_absolute() or value != pure.as_posix() or any(part in {"", ".", ".."} for part in pure.parts):
        return False
    return required_prefix is None or value.startswith(required_prefix)


def _safe_readme_glob(value: object) -> bool:
    if not isinstance(value, str) or not value or "\\" in value or "://" in value:
        return False
    pure = pathlib.PurePosixPath(value)
    if pure.is_absolute() or value != pure.as_posix() or pure.name != "README.md":
        return False
    if any(part in {"", ".", "..", "**"} for part in pure.parts):
        return False
    return all(part == "*" or not any(marker in part for marker in "?[]*") for part in pure.parts)


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
    if any(marker in value for marker in "?[]{}"):
        return False
    return all("***" not in part and ("**" not in part or part == "**") for part in pure.parts)


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


def _segment_glob_intersection_witness(left: str, right: str) -> str | None:
    """Return one non-empty segment matched by both supported `*` globs."""

    queue = collections.deque([(0, 0, "")])
    visited: set[tuple[int, int, bool]] = set()
    while queue:
        left_index, right_index, witness = queue.popleft()
        state = (left_index, right_index, bool(witness))
        if state in visited:
            continue
        visited.add(state)
        if left_index == len(left) and right_index == len(right):
            if witness:
                return witness
            continue

        left_star = left_index < len(left) and left[left_index] == "*"
        right_star = right_index < len(right) and right[right_index] == "*"
        if left_star:
            queue.append((left_index + 1, right_index, witness))
        if right_star:
            queue.append((left_index, right_index + 1, witness))

        if left_index >= len(left) or right_index >= len(right):
            continue
        if left_star and right_star:
            queue.append((left_index, right_index, witness + "x"))
        elif left_star:
            queue.append((left_index, right_index + 1, witness + right[right_index]))
        elif right_star:
            queue.append((left_index + 1, right_index, witness + left[left_index]))
        elif left[left_index] == right[right_index]:
            queue.append((left_index + 1, right_index + 1, witness + left[left_index]))
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
        right_globstar = right_index < len(right_parts) and right_parts[right_index] == "**"
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
            queue.append((next_left, next_right, witness + (segment,)))
    return None


def matching_template_roles(
    path: pathlib.Path,
    artifact_type: str,
    profiles: dict[str, object],
) -> list[str]:
    """Return sorted template roles matching one target path and profile."""

    normalized = pathlib.PurePosixPath(path.as_posix())
    if normalized.is_absolute() or any(part in {"", ".", ".."} for part in normalized.parts):
        return []
    common = profiles.get("common", {})
    excluded = common.get("inventory_excludes", []) if isinstance(common, dict) else []
    if normalized.as_posix() in excluded:
        return []
    if artifact_type == "readme":
        try:
            classify_readme_profile(path, profiles)
        except ProfileError:
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


def matching_readme_profiles(path: pathlib.Path, profiles: dict[str, object]) -> list[str]:
    """Return every declared README profile matching a repository-relative path."""

    normalized = pathlib.PurePosixPath(path.as_posix())
    if normalized.is_absolute() or normalized.name != "README.md" or any(
        part in {"", ".", ".."} for part in normalized.parts
    ):
        return []
    readme_profiles = profiles.get("readme_profiles", {})
    if not isinstance(readme_profiles, dict):
        return []
    matches: list[str] = []
    for name, raw_profile in sorted(readme_profiles.items()):
        if not isinstance(name, str) or not isinstance(raw_profile, dict):
            continue
        patterns = raw_profile.get("path_globs", [])
        if isinstance(patterns, list) and any(
            isinstance(pattern, str) and _readme_glob_matches(normalized, pattern)
            for pattern in patterns
        ):
            matches.append(name)
    return matches


def classify_readme_profile(path: pathlib.Path, profiles: dict[str, object]) -> str:
    """Classify one README path, failing deterministically on zero or many owners."""

    matches = matching_readme_profiles(path, profiles)
    normalized = path.as_posix()
    if not matches:
        raise ProfileError(f"README path is unclassified: {normalized}")
    if len(matches) > 1:
        raise ProfileError(f"README path is ambiguous: {normalized}; profiles={','.join(matches)}")
    return matches[0]


def readme_frontmatter_consumer(path: pathlib.Path, profiles: dict[str, object]) -> str | None:
    """Return the profile-declared consumer; metadata content never infers one."""

    profile_name = classify_readme_profile(path, profiles)
    readme_profiles = profiles.get("readme_profiles", {})
    raw_profile = readme_profiles.get(profile_name, {}) if isinstance(readme_profiles, dict) else {}
    if not isinstance(raw_profile, dict) or raw_profile.get("frontmatter") != "optional":
        return None
    consumer = raw_profile.get("frontmatter_consumer")
    return consumer if isinstance(consumer, str) and consumer else None


def _typed_target_types(profiles: dict[str, object]) -> set[str]:
    families = profiles.get("document_families", {})
    if not isinstance(families, dict):
        return set()
    excluded = {"readme", "governance", "generated", "template-source", "repo-support", "unsupported"}
    return {
        item
        for members in families.values()
        if isinstance(members, list)
        for item in members
        if isinstance(item, str) and item not in excluded
    }


def _has_parent_cycle(record: Record, parent_ids: list[str], manifest: Manifest) -> bool:
    artifact_id = record.metadata.get("artifact_id")
    if not isinstance(artifact_id, str) or not artifact_id.strip():
        return False
    target = artifact_id.strip()
    pending = list(parent_ids)
    visited: set[str] = set()
    while pending:
        candidate = pending.pop()
        if candidate == target:
            return True
        if candidate in visited:
            continue
        visited.add(candidate)
        parent_record = manifest.records_by_id.get(candidate)
        if parent_record is None:
            continue
        nested = _string_list(parent_record.metadata.get("parent_ids"))
        if nested:
            pending.extend(nested)
    return False


def _template_placeholder_values(profiles: dict[str, object]) -> dict[str, str]:
    common, _ = _profile_mapping(profiles)
    values = common.get("template_placeholders", {})
    return dict(values) if isinstance(values, dict) else {}


def _template_angle_tokens(profiles: dict[str, object]) -> set[str]:
    return {
        token
        for value in _template_placeholder_values(profiles).values()
        for token in re.findall(r"<[^<>]+>", value)
    }


def _contains_template_placeholder(value: object, angle_tokens: set[str]) -> bool:
    if isinstance(value, str):
        return any(token in value for token in angle_tokens)
    if isinstance(value, list):
        return any(_contains_template_placeholder(item, angle_tokens) for item in value)
    if isinstance(value, dict):
        return any(_contains_template_placeholder(item, angle_tokens) for item in value.values())
    return False


def _validate_template_source(
    record: Record,
    profiles: dict[str, object],
) -> list[Finding] | None:
    template_roles = profiles.get("template_roles", {})
    if not isinstance(template_roles, dict):
        return None
    matching_roles = [
        (name, role)
        for name, role in template_roles.items()
        if isinstance(name, str)
        and isinstance(role, dict)
        and role.get("source") == record.path.as_posix()
    ]
    if not matching_roles:
        return None
    role_name, role = matching_roles[0]
    target_type = role.get("artifact_profile")
    if not isinstance(target_type, str):
        return [_finding(record, "unknown-template-target", "template role has no artifact profile")]
    if role_name == "readme":
        return (
            []
            if record.metadata == {"status": "draft"}
            else [_finding(record, "invalid-template-metadata", "README source metadata must be exactly status: draft")]
        )
    if role_name in {"memory", "progress"}:
        expected = {"layer": "agentic", "status": "draft"}
        return (
            []
            if record.metadata == expected
            else [
                _finding(
                    record,
                    "invalid-template-metadata",
                    f"{role_name} source metadata must be exactly layer: agentic plus status: draft",
                )
            ]
        )
    _, profile_map = _profile_mapping(profiles)
    target_profile = profile_map.get(target_type)
    if not isinstance(target_profile, dict):
        return [_finding(record, "unknown-template-target", f"template target profile is unknown: {target_type}")]
    placeholders = _template_placeholder_values(profiles)
    findings: list[Finding] = []
    required = set(target_profile.get("required", []))
    optional = set(target_profile.get("optional", []))
    forbidden = set(target_profile.get("forbidden", []))
    allowed_template_keys = required | optional | {"status"}
    for key in sorted(required - set(record.metadata)):
        findings.append(_finding(record, "missing-template-key", f"target-profile key is missing: {key}"))
    for key in sorted(set(record.metadata) & forbidden):
        findings.append(_finding(record, "forbidden-template-key", f"key is forbidden for {target_type}: {key}"))
    for key in sorted(set(record.metadata) - allowed_template_keys):
        findings.append(_finding(record, "type-inappropriate-key", f"key is not declared for target {target_type}: {key}"))
    if record.metadata.get("status") != "draft":
        findings.append(_finding(record, "invalid-template-status", "template sources must keep status: draft"))
    if record.metadata.get("artifact_type") != target_type:
        findings.append(
            _finding(record, "artifact-type-mismatch", f"template must declare target artifact_type {target_type}")
        )
    if record.metadata.get("artifact_id") != placeholders.get("artifact_id"):
        findings.append(_finding(record, "invalid-template-placeholder", "artifact_id must use the Stage 99 placeholder"))
    parents = _string_list(record.metadata.get("parent_ids"))
    parent_placeholder = placeholders.get("parent_id")
    if parents is None:
        findings.append(_finding(record, "invalid-template-placeholder", "parent_ids must be a placeholder list"))
    elif not parents and not target_profile.get("allow_empty_parents", False):
        findings.append(_finding(record, "missing-parent", f"{target_type} template requires a direct parent placeholder"))
    elif any(parent != parent_placeholder for parent in parents):
        findings.append(_finding(record, "invalid-template-placeholder", "parent_ids contains a noncanonical placeholder"))
    placeholder_keys = {
        "reviewed_at": "reviewed_at",
        "review_cycle": "review_cycle",
        "archived_from": "archived_from",
        "archived_on": "archived_on",
        "archive_reason": "archive_reason",
        "current_replacement": "current_replacement",
    }
    for key, placeholder_key in placeholder_keys.items():
        if key in required and record.metadata.get(key) != placeholders.get(placeholder_key):
            findings.append(_finding(record, "invalid-template-placeholder", f"{key} must use the Stage 99 placeholder"))
    return sorted(set(findings))


def validate_record(
    record: Record,
    profiles: dict[str, object],
    manifest: dict[str, pathlib.Path],
    transition_overrides: Mapping[tuple[str, str, str], TransitionOverride] | None = None,
) -> list[Finding]:
    """Validate one record against its typed profile and the global manifest."""

    common, profile_map = _profile_mapping(profiles)
    raw_profile = profile_map.get(record.artifact_type)
    if not isinstance(raw_profile, dict):
        return [_finding(record, "unknown-profile", f"profile is not configured: {record.artifact_type}")]
    typed_manifest = manifest if isinstance(manifest, Manifest) else Manifest(dict(manifest), {}, {})
    findings: list[Finding] = []
    if record.parse_error:
        parse_code = record.parse_error_code or "malformed-yaml"
        findings.append(_finding(record, f"frontmatter-{parse_code}", record.parse_error))
        return findings
    template_findings = _validate_template_source(record, profiles)
    if template_findings is not None:
        return template_findings
    if record.artifact_type == "unsupported":
        findings.append(
            _finding(
                record,
                "unsupported-profile",
                "path is outside the typed document corpus",
                severity="warning",
            )
        )

    if record.artifact_type == "readme":
        try:
            readme_profile_name = classify_readme_profile(record.path, profiles)
        except ProfileError as error:
            findings.append(_finding(record, "readme-profile", str(error)))
        else:
            readme_profiles = profiles.get("readme_profiles", {})
            readme_profile = (
                readme_profiles.get(readme_profile_name, {}) if isinstance(readme_profiles, dict) else {}
            )
            behavior = readme_profile.get("frontmatter") if isinstance(readme_profile, dict) else None
            allowed_readme_keys = (
                set(readme_profile.get("allowed_frontmatter_keys", []))
                if isinstance(readme_profile, dict)
                else set()
            )
            if record.frontmatter_present and behavior == "forbidden":
                findings.append(
                    _finding(
                        record,
                        "readme-frontmatter-forbidden",
                        f"README profile {readme_profile_name} forbids frontmatter",
                    )
                )
            elif record.metadata and readme_frontmatter_consumer(record.path, profiles) is None:
                findings.append(
                    _finding(
                        record,
                        "readme-consumer-missing",
                        f"README profile {readme_profile_name} has no declared frontmatter consumer",
                    )
                )
            for key in sorted(set(record.metadata) - allowed_readme_keys):
                findings.append(
                    _finding(
                        record,
                        "readme-frontmatter-key",
                        f"README profile {readme_profile_name} does not allow frontmatter key: {key}",
                    )
                )

    if record.artifact_type in _typed_target_types(profiles):
        frontmatter_order = common.get("frontmatter_order", [])
        if isinstance(frontmatter_order, list):
            order_index = {key: index for index, key in enumerate(frontmatter_order)}
            present_keys = [key for key in record.metadata if key in order_index]
            expected_keys = sorted(present_keys, key=order_index.__getitem__)
            if present_keys != expected_keys:
                findings.append(
                    _finding(
                        record,
                        "frontmatter-order",
                        "frontmatter keys do not follow deterministic canonical serialization order",
                    )
                )

    placeholder_values = _template_angle_tokens(profiles)
    if record.artifact_type != "template-source" and any(
        _contains_template_placeholder(value, placeholder_values) for value in record.metadata.values()
    ):
        findings.append(
            _finding(
                record,
                "template-placeholder-in-target",
                "Stage 99 template placeholders must be replaced in instantiated documents",
            )
        )

    required = set(raw_profile.get("required", []))
    optional = set(raw_profile.get("optional", []))
    forbidden = set(raw_profile.get("forbidden", []))
    global_forbidden = set(common.get("globally_forbidden", []))
    for key in sorted(required):
        if key not in record.metadata or record.metadata[key] in (None, ""):
            findings.append(_finding(record, "missing-required-key", f"required key is missing: {key}"))
    for key in sorted(record.metadata):
        if key not in forbidden:
            continue
        code = "forbidden-key" if key in global_forbidden else "type-inappropriate-key"
        findings.append(_finding(record, code, f"key is forbidden for {record.artifact_type}: {key}"))

    status = record.metadata.get("status")
    allowed_statuses = raw_profile.get("allowed_statuses", [])
    if status is not None:
        if not isinstance(status, str) or status not in allowed_statuses:
            findings.append(
                _finding(record, "invalid-status", f"status is not allowed for {record.artifact_type}")
            )
        if status == "archived" and record.artifact_type != "archive":
            findings.append(
                _finding(record, "archived-outside-stage-98", "archived status is reserved for archive tombstones")
            )
    previous_status = record.previous_status
    if isinstance(status, str) and previous_status and status != previous_status:
        transitions = common.get("transitions", {})
        allowed_next = transitions.get(previous_status, []) if isinstance(transitions, dict) else []
        override_key = (record.path.as_posix(), previous_status, status)
        if status not in allowed_next and override_key not in (transition_overrides or {}):
            findings.append(
                _finding(
                    record,
                    "invalid-transition",
                    f"lifecycle transition requires explicit override: {previous_status} -> {status}",
                )
            )

    artifact_id = record.metadata.get("artifact_id")
    if artifact_id is not None and (not isinstance(artifact_id, str) or not artifact_id.strip()):
        findings.append(_finding(record, "invalid-artifact-id", "artifact_id must be a non-empty string"))
    if isinstance(artifact_id, str) and artifact_id.strip() in typed_manifest.duplicates:
        paths = ", ".join(path.as_posix() for path in typed_manifest.duplicates[artifact_id.strip()])
        findings.append(_finding(record, "duplicate-artifact-id", f"artifact_id occurs at: {paths}"))

    declared_type = record.metadata.get("artifact_type")
    if declared_type is not None:
        if not isinstance(declared_type, str) or declared_type != record.artifact_type:
            findings.append(
                _finding(
                    record,
                    "artifact-type-mismatch",
                    f"declared artifact_type does not match inferred profile {record.artifact_type}",
                )
            )

    parent_value = record.metadata.get("parent_ids")
    parent_ids = _string_list(parent_value) if parent_value is not None else None
    if parent_value is not None and parent_ids is None:
        findings.append(_finding(record, "invalid-parent-ids", "parent_ids must be a list of non-empty strings"))
    if parent_ids is not None:
        if len(parent_ids) != len(set(parent_ids)):
            findings.append(_finding(record, "duplicate-parent", "parent_ids contains duplicate IDs"))
        root_exceptions = common.get("root_exceptions", {})
        root_permitted = raw_profile.get("allow_empty_parents", False) or (
            isinstance(root_exceptions, dict) and record.path.as_posix() in root_exceptions
        )
        if not parent_ids and not root_permitted:
            findings.append(_finding(record, "missing-parent", "this artifact profile does not permit a root"))
        parent_type_order = raw_profile.get("allowed_parent_types", [])
        allowed_parent_types = set(parent_type_order)
        for parent_id in parent_ids:
            if isinstance(artifact_id, str) and parent_id == artifact_id.strip():
                findings.append(_finding(record, "self-parent", f"artifact references itself as parent: {parent_id}"))
                continue
            parent_record = typed_manifest.records_by_id.get(parent_id)
            if parent_id not in typed_manifest:
                findings.append(_finding(record, "unresolved-parent", f"parent artifact_id is unresolved: {parent_id}"))
            elif parent_record and allowed_parent_types and parent_record.artifact_type not in allowed_parent_types:
                findings.append(
                    _finding(
                        record,
                        "invalid-parent-type",
                        f"parent type {parent_record.artifact_type} is not allowed: {parent_id}",
                    )
                )
        if (
            len(parent_ids) == len(set(parent_ids))
            and not any(parent_id in typed_manifest.duplicates for parent_id in parent_ids)
            and isinstance(parent_type_order, list)
        ):
            type_precedence = {
                parent_type: index for index, parent_type in enumerate(parent_type_order)
            }
            resolved_parents = [typed_manifest.records_by_id.get(parent_id) for parent_id in parent_ids]
            if all(
                parent_record is not None and parent_record.artifact_type in type_precedence
                for parent_record in resolved_parents
            ):
                expected_parent_ids = sorted(
                    parent_ids,
                    key=lambda parent_id: (
                        type_precedence[typed_manifest.records_by_id[parent_id].artifact_type],
                        parent_id,
                    ),
                )
                if parent_ids != expected_parent_ids:
                    findings.append(
                        _finding(
                            record,
                            "parent-order",
                            "parent_ids do not follow deterministic type-precedence and ID serialization",
                        )
                    )
        if _has_parent_cycle(record, parent_ids, typed_manifest):
            findings.append(_finding(record, "parent-cycle", "parent_ids creates a cycle"))

    supersedes_value = record.metadata.get("supersedes")
    if supersedes_value is not None:
        supersedes = _string_list(supersedes_value)
        if supersedes is None:
            findings.append(_finding(record, "invalid-supersedes", "supersedes must be a list of non-empty strings"))
        else:
            for replaced_id in supersedes:
                if isinstance(artifact_id, str) and replaced_id == artifact_id.strip():
                    findings.append(_finding(record, "self-supersession", f"artifact supersedes itself: {replaced_id}"))
                elif replaced_id not in typed_manifest:
                    findings.append(
                        _finding(record, "unresolved-supersedes", f"superseded artifact_id is unresolved: {replaced_id}")
                    )
                else:
                    replaced_record = typed_manifest.records_by_id.get(replaced_id)
                    if replaced_record and replaced_record.metadata.get("status") != "superseded":
                        findings.append(
                            _finding(
                                record,
                                "invalid-supersession-state",
                                f"superseded target is not in superseded status: {replaced_id}",
                            )
                        )

    if status == "superseded" and "artifact_id" in required:
        replacement_ids = {
            replaced_id
            for candidate in typed_manifest.records_by_id.values()
            for replaced_id in (_string_list(candidate.metadata.get("supersedes")) or [])
        }
        if not isinstance(artifact_id, str) or artifact_id.strip() not in replacement_ids:
            findings.append(
                _finding(
                    record,
                    "replacement-free-supersession",
                    "superseded artifact has no resolvable replacement relation",
                )
            )

    reviewed_at = record.metadata.get("reviewed_at")
    if status == "active" and "reviewed_at" in required and reviewed_at in (None, ""):
        findings.append(
            _finding(record, "stale-active", "active freshness-managed artifact lacks reviewed_at evidence")
        )
    if reviewed_at is not None and not _valid_iso_temporal(reviewed_at):
        findings.append(
            _finding(record, "invalid-reviewed-at", "reviewed_at must be a strict ISO date or timezone-aware date-time")
        )
    review_cycle = record.metadata.get("review_cycle")
    if review_cycle is not None and (not isinstance(review_cycle, str) or not review_cycle.strip()):
        findings.append(_finding(record, "invalid-review-cycle", "review_cycle must be a non-empty string"))
    generated_by = record.metadata.get("generated_by")
    if generated_by is not None and not _safe_repo_path(generated_by, "scripts/"):
        findings.append(
            _finding(record, "invalid-generator", "generated_by must be a safe canonical scripts/ repository path")
        )

    if record.artifact_type == "archive":
        archive_path_fields = {
            "archived_from": "invalid-archived-from",
            "current_replacement": "invalid-current-replacement",
        }
        for key, code in archive_path_fields.items():
            value = record.metadata.get(key)
            if value is not None and not _safe_repo_path(value, "docs/"):
                findings.append(_finding(record, code, f"{key} must be a safe canonical docs/ repository path"))
        archived_on = record.metadata.get("archived_on")
        if archived_on is not None and not _valid_iso_date(archived_on):
            findings.append(_finding(record, "invalid-archived-on", "archived_on must be a strict ISO date"))
        archive_reason = record.metadata.get("archive_reason")
        if archive_reason is not None and (not isinstance(archive_reason, str) or not archive_reason.strip()):
            findings.append(_finding(record, "invalid-archive-reason", "archive_reason must be a non-empty string"))

    if not raw_profile.get("allow_additional", False):
        known = required | optional | forbidden
        for key in sorted(set(record.metadata) - known):
            findings.append(
                _finding(record, "type-inappropriate-key", f"key is not declared for {record.artifact_type}: {key}")
            )
    return sorted(set(findings))


def load_profiles(path: pathlib.Path = DEFAULT_PROFILES) -> dict[str, object]:
    """Load and structurally validate the typed metadata profile contract."""

    try:
        source = path.read_text(encoding="utf-8")
        loaded = _safe_load_unique(source)
    except (OSError, UnicodeError, yaml.YAMLError) as error:
        raise ProfileError(f"cannot load profile YAML: {error}") from error
    if not isinstance(loaded, dict):
        raise ProfileError("profile document must be a mapping")
    schema_version = loaded.get("schema_version")
    if type(schema_version) is not int or schema_version != 1:
        raise ProfileError("schema_version must be the integer 1")
    common, profile_map = _profile_mapping(loaded)
    if not all(isinstance(name, str) for name in profile_map):
        raise ProfileError("profile names must be strings")
    actual_types = set(profile_map)
    if actual_types != EXPECTED_PROFILE_TYPES:
        missing = ", ".join(sorted(EXPECTED_PROFILE_TYPES - actual_types)) or "none"
        unexpected = ", ".join(sorted(actual_types - EXPECTED_PROFILE_TYPES)) or "none"
        raise ProfileError(f"profile type mismatch; missing={missing}; unexpected={unexpected}")
    common_list_names = (
        "allowed_statuses",
        "terminal_statuses",
        "globally_forbidden",
        "typed_keys",
        "inventory_excludes",
    )
    common_lists: dict[str, list[str]] = {}
    for key in common_list_names:
        value = common.get(key)
        if not isinstance(value, list) or not all(isinstance(item, str) and item for item in value):
            raise ProfileError(f"common.{key} must be a list of non-empty strings")
        if len(value) != len(set(value)):
            raise ProfileError(f"common.{key} must not contain duplicates")
        common_lists[key] = value
    frontmatter_order = common.get("frontmatter_order")
    if not isinstance(frontmatter_order, list) or not all(
        isinstance(item, str) and item for item in frontmatter_order
    ):
        raise ProfileError("common.frontmatter_order must be a list of non-empty strings")
    if len(frontmatter_order) != len(set(frontmatter_order)):
        raise ProfileError("common.frontmatter_order must not contain duplicates")
    if tuple(frontmatter_order) != EXPECTED_FRONTMATTER_ORDER:
        raise ProfileError("common.frontmatter_order must define the exact canonical typed-key order")
    template_placeholders = common.get("template_placeholders")
    if not isinstance(template_placeholders, dict) or set(template_placeholders) != EXPECTED_TEMPLATE_PLACEHOLDER_KEYS:
        raise ProfileError("common.template_placeholders must define the exact Stage 99 placeholder keys")
    if not all(isinstance(value, str) and value.strip() for value in template_placeholders.values()):
        raise ProfileError("common.template_placeholders values must be non-empty strings")
    root_exceptions = common.get("root_exceptions")
    if not isinstance(root_exceptions, dict):
        raise ProfileError("common.root_exceptions must be a path-to-reason mapping")
    for root_path, reason in root_exceptions.items():
        if not isinstance(root_path, str) or _normalized_target_path(root_path) is None:
            raise ProfileError("common.root_exceptions keys must be canonical target Markdown paths")
        if not isinstance(reason, str) or not reason.strip():
            raise ProfileError("common.root_exceptions reasons must be non-empty strings")
    allowed_statuses = set(common_lists["allowed_statuses"])
    terminal_statuses = set(common_lists["terminal_statuses"])
    if not terminal_statuses <= allowed_statuses:
        raise ProfileError("common.terminal_statuses must be a subset of allowed_statuses")
    transitions = common.get("transitions")
    if not isinstance(transitions, dict) or not all(isinstance(key, str) for key in transitions):
        raise ProfileError("common.transitions must be a mapping")
    if set(transitions) != allowed_statuses:
        raise ProfileError("common.transitions must define every and only allowed status")
    for state, targets in transitions.items():
        if not isinstance(targets, list) or not all(isinstance(item, str) and item for item in targets):
            raise ProfileError(f"common.transitions.{state} must be a list of non-empty strings")
        if len(targets) != len(set(targets)):
            raise ProfileError(f"common.transitions.{state} must not contain duplicates")
        unknown_targets = set(targets) - allowed_statuses
        if unknown_targets:
            raise ProfileError(
                f"common.transitions.{state} has unknown statuses: {', '.join(sorted(unknown_targets))}"
            )
        if state in terminal_statuses and targets:
            raise ProfileError(f"terminal status {state} must not have outgoing transitions")
    for name, raw_profile in sorted(profile_map.items()):
        if not isinstance(raw_profile, dict):
            raise ProfileError(f"profile {name} must be a mapping")
        required = raw_profile.get("required")
        optional = raw_profile.get("optional")
        forbidden = raw_profile.get("forbidden")
        if not all(
            isinstance(value, list) and all(isinstance(item, str) and item for item in value)
            for value in (required, optional, forbidden)
        ):
            raise ProfileError(f"profile {name} required/optional/forbidden must be string lists")
        if any(len(value) != len(set(value)) for value in (required, optional, forbidden)):
            raise ProfileError(f"profile {name} key disposition lists must not contain duplicates")
        overlap = (set(required) & set(optional)) | (set(required) & set(forbidden)) | (set(optional) & set(forbidden))
        if overlap:
            raise ProfileError(f"profile {name} has overlapping key dispositions: {', '.join(sorted(overlap))}")
        profile_statuses = raw_profile.get("allowed_statuses")
        if not isinstance(profile_statuses, list) or not all(
            isinstance(item, str) and item for item in profile_statuses
        ):
            raise ProfileError(f"profile {name} allowed_statuses must be a string list")
        if len(profile_statuses) != len(set(profile_statuses)):
            raise ProfileError(f"profile {name} allowed_statuses must not contain duplicates")
        unknown_statuses = set(profile_statuses) - allowed_statuses
        if unknown_statuses:
            raise ProfileError(f"profile {name} has unknown statuses: {', '.join(sorted(unknown_statuses))}")
        parent_types = raw_profile.get("allowed_parent_types")
        if not isinstance(parent_types, list) or not all(isinstance(item, str) and item for item in parent_types):
            raise ProfileError(f"profile {name} allowed_parent_types must be a string list")
        if len(parent_types) != len(set(parent_types)):
            raise ProfileError(f"profile {name} allowed_parent_types must not contain duplicates")
        unknown_parents = set(parent_types) - EXPECTED_PROFILE_TYPES
        if unknown_parents:
            raise ProfileError(f"profile {name} has unknown parent types: {', '.join(sorted(unknown_parents))}")
        if type(raw_profile.get("allow_empty_parents")) is not bool:
            raise ProfileError(f"profile {name} allow_empty_parents must be boolean")
        if "allow_additional" in raw_profile and type(raw_profile["allow_additional"]) is not bool:
            raise ProfileError(f"profile {name} allow_additional must be boolean")
        disposition = raw_profile.get("disposition")
        if not isinstance(disposition, str) or not disposition.strip():
            raise ProfileError(f"profile {name} disposition must be a non-empty string")
    document_families = loaded.get("document_families")
    if not isinstance(document_families, dict) or set(document_families) != set(EXPECTED_DOCUMENT_FAMILIES):
        raise ProfileError("document_families must define exactly sdlc and common")
    family_members: list[str] = []
    for family_name, expected_members in EXPECTED_DOCUMENT_FAMILIES.items():
        members = document_families.get(family_name)
        if not isinstance(members, list) or not all(isinstance(item, str) and item for item in members):
            raise ProfileError(f"document_families.{family_name} must be a list of non-empty strings")
        if len(members) != len(set(members)):
            raise ProfileError(f"document_families.{family_name} must not contain duplicates")
        unknown_members = set(members) - actual_types
        if unknown_members:
            raise ProfileError(
                f"document_families.{family_name} has unknown profiles: {', '.join(sorted(unknown_members))}"
            )
        if tuple(members) != expected_members:
            raise ProfileError(f"document_families.{family_name} must define the exact canonical members")
        family_members.extend(members)
    if len(family_members) != len(set(family_members)):
        raise ProfileError("document_families members must be unique across families")

    readme_profiles = loaded.get("readme_profiles")
    if not isinstance(readme_profiles, dict) or not readme_profiles:
        raise ProfileError("readme_profiles must be a non-empty mapping")
    declared_globs: list[tuple[str, str]] = []
    for profile_name, readme_profile in sorted(readme_profiles.items()):
        if not isinstance(profile_name, str) or not profile_name.strip():
            raise ProfileError("readme_profiles names must be non-empty strings")
        if not isinstance(readme_profile, dict) or set(readme_profile) != README_PROFILE_KEYS:
            raise ProfileError(f"README profile {profile_name} must define the exact contract members")
        path_globs = readme_profile.get("path_globs")
        if not isinstance(path_globs, list) or not path_globs or not all(
            isinstance(pattern, str) and _safe_readme_glob(pattern) for pattern in path_globs
        ):
            raise ProfileError(
                f"README profile {profile_name} path_globs must be safe repository-relative README patterns"
            )
        if len(path_globs) != len(set(path_globs)):
            raise ProfileError(f"README profile {profile_name} path_globs must not contain duplicates")
        for pattern in path_globs:
            for other_name, other_pattern in declared_globs:
                if _readme_globs_overlap(pattern, other_pattern):
                    raise ProfileError(
                        f"README profile globs overlap: {other_name}:{other_pattern} and {profile_name}:{pattern}"
                    )
            declared_globs.append((profile_name, pattern))

        behavior = readme_profile.get("frontmatter")
        if behavior not in {"forbidden", "optional"}:
            raise ProfileError(f"README profile {profile_name} frontmatter behavior is unknown")
        allowed_keys = readme_profile.get("allowed_frontmatter_keys")
        if not isinstance(allowed_keys, list) or not all(
            isinstance(item, str) and item for item in allowed_keys
        ):
            raise ProfileError(f"README profile {profile_name} allowed_keys must be a string list")
        if len(allowed_keys) != len(set(allowed_keys)):
            raise ProfileError(f"README profile {profile_name} allowed_keys must not contain duplicates")
        unknown_keys = set(allowed_keys) - README_FRONTMATTER_ALLOWED_KEYS
        if unknown_keys:
            raise ProfileError(
                f"README profile {profile_name} has unknown frontmatter keys: {', '.join(sorted(unknown_keys))}"
            )
        consumer = readme_profile.get("frontmatter_consumer")
        if behavior == "forbidden":
            if consumer is not None or allowed_keys:
                raise ProfileError(
                    f"README profile {profile_name} forbidden frontmatter cannot declare keys or a consumer"
                )
        elif not isinstance(consumer, str) or not _safe_repo_path(consumer, "scripts/"):
            raise ProfileError(f"README profile {profile_name} optional frontmatter requires a scripts/ consumer")

        heading_sets: list[set[str]] = []
        for heading_key in ("required_headings", "optional_headings", "forbidden_headings"):
            headings = readme_profile.get(heading_key)
            if not isinstance(headings, list) or not all(
                isinstance(heading, str) and heading.strip() for heading in headings
            ):
                raise ProfileError(f"README profile {profile_name} {heading_key} must be a string list")
            if len(headings) != len(set(headings)):
                raise ProfileError(f"README profile {profile_name} {heading_key} must not contain duplicates")
            heading_sets.append(set(headings))
        if any(heading_sets[left] & heading_sets[right] for left, right in ((0, 1), (0, 2), (1, 2))):
            raise ProfileError(f"README profile {profile_name} heading contracts must not overlap")

        local_role = readme_profile.get("allowed_local_content_role")
        if not isinstance(local_role, str) or not local_role.strip():
            raise ProfileError(f"README profile {profile_name} allowed_local_content_role must be non-empty")
        owner = readme_profile.get("canonical_shared_rule_owner")
        if not isinstance(owner, str) or not _safe_repo_path(owner):
            raise ProfileError(f"README profile {profile_name} canonical_shared_rule_owner must be a safe path")
    template_roles = loaded.get("template_roles")
    if not isinstance(template_roles, dict) or set(template_roles) != EXPECTED_TEMPLATE_ROLE_NAMES:
        raise ProfileError("template_roles must define the exact 23 canonical role names")
    declared_sources: dict[str, str] = {}
    declared_target_globs: dict[str, str] = {}
    declared_matchers: list[tuple[str, str, str]] = []
    for role_name, role in sorted(template_roles.items()):
        if not isinstance(role, dict) or set(role) != TEMPLATE_ROLE_KEYS:
            raise ProfileError(f"template role {role_name} must define the exact contract members")
        source_path = role.get("source")
        if (
            not isinstance(source_path, str)
            or not _safe_repo_path(source_path, "docs/99.templates/templates/")
            or not source_path.endswith(".template.md")
        ):
            raise ProfileError(f"template role {role_name} source must be a safe canonical Markdown template path")
        if source_path in declared_sources:
            raise ProfileError(
                f"template roles must have unique sources: {declared_sources[source_path]} and {role_name}"
            )
        declared_sources[source_path] = role_name
        artifact_profile = role.get("artifact_profile")
        if artifact_profile not in actual_types:
            raise ProfileError(f"template role {role_name} has unknown artifact profile: {artifact_profile}")
        target_globs = role.get("target_globs")
        if not isinstance(target_globs, list) or not target_globs or not all(
            _safe_target_glob(pattern) for pattern in target_globs
        ):
            raise ProfileError(f"template role {role_name} target_globs must be safe Markdown target patterns")
        if len(target_globs) != len(set(target_globs)):
            raise ProfileError(f"template role {role_name} target_globs must not contain duplicates")
        for pattern in sorted(target_globs):
            if pattern in declared_target_globs:
                raise ProfileError(
                    "template role target globs overlap: "
                    f"{declared_target_globs[pattern]}:{pattern} and {role_name}:{pattern}"
                )
            declared_target_globs[pattern] = role_name
            for other_role, other_profile, other_pattern in declared_matchers:
                if (
                    other_role == role_name
                    or other_profile != artifact_profile
                    or _target_glob_specificity(other_pattern)
                    != _target_glob_specificity(pattern)
                ):
                    continue
                witness = _target_glob_intersection_witness(other_pattern, pattern)
                if witness is not None:
                    raise ProfileError(
                        "template role target globs overlap at equal specificity: "
                        f"{other_role}:{other_pattern} and {role_name}:{pattern}; "
                        f"witness={witness}"
                    )
            declared_matchers.append((role_name, artifact_profile, pattern))
        heading_sets: list[set[str]] = []
        for heading_key in ("required_headings", "conditional_headings", "forbidden_headings"):
            headings = role.get(heading_key)
            if not isinstance(headings, list) or not headings or not all(
                isinstance(heading, str)
                and heading.startswith("## ")
                and heading.strip() == heading
                for heading in headings
            ):
                raise ProfileError(
                    f"template role {role_name} {heading_key} must be a non-empty H2 heading list"
                )
            if len(headings) != len(set(headings)):
                raise ProfileError(f"template role {role_name} {heading_key} must not contain duplicates")
            heading_sets.append(set(headings))
        if any(heading_sets[left] & heading_sets[right] for left, right in ((0, 1), (0, 2), (1, 2))):
            raise ProfileError(f"template role {role_name} heading contracts must not overlap")
    return loaded


def _run_git(
    root: pathlib.Path,
    args: Sequence[str],
    *,
    operation: str,
    text: bool = False,
) -> subprocess.CompletedProcess[bytes] | subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            ["git", "-C", str(root), *args],
            capture_output=True,
            text=text,
            check=False,
        )
    except OSError:
        raise ProfileError(
            f"cannot establish local Git snapshot: Git executable unavailable during {operation}"
        ) from None


def _decode_git_paths(output: bytes, operation: str) -> list[pathlib.Path]:
    try:
        return [pathlib.Path(item.decode("utf-8")) for item in output.split(b"\0") if item]
    except UnicodeDecodeError:
        raise ProfileError(
            f"cannot establish local Git snapshot: {operation} returned a non-UTF-8 path"
        ) from None


def _require_git_worktree(root: pathlib.Path) -> None:
    result = _run_git(
        root,
        ["rev-parse", "--is-inside-work-tree"],
        operation="Git worktree validation",
        text=True,
    )
    if result.returncode != 0 or result.stdout.strip() != "true":
        raise ProfileError("cannot establish local Git snapshot: --root is not a Git worktree")


def _tracked_markdown(root: pathlib.Path, *, require_git: bool = False) -> list[pathlib.Path]:
    try:
        result = _run_git(
            root,
            ["ls-files", "-z", "--", "*.md"],
            operation="tracked Markdown discovery",
        )
    except ProfileError:
        if require_git:
            raise
        result = None
    if result is not None and result.returncode == 0:
        paths = _decode_git_paths(result.stdout, "tracked Markdown discovery")
    elif require_git:
        raise ProfileError("cannot establish local Git snapshot: tracked Markdown discovery failed")
    else:
        paths = [path.relative_to(root) for path in root.rglob("*.md") if path.is_file()]
    return sorted(
        {
            path
            for path in paths
            if path.as_posix().startswith(TARGET_MARKDOWN_PREFIXES)
        },
        key=lambda path: path.as_posix(),
    )


def _tracked_repository_markdown(root: pathlib.Path) -> list[pathlib.Path]:
    result = _run_git(
        root,
        ["ls-files", "-z", "--", "*.md"],
        operation="repository contract Markdown discovery",
    )
    if result.returncode != 0:
        raise ProfileError("cannot establish local Git snapshot: repository contract Markdown discovery failed")
    return sorted(
        set(_decode_git_paths(result.stdout, "repository contract Markdown discovery")),
        key=lambda path: path.as_posix(),
    )


def _registry_string_arrays(value: object, path: tuple[str, ...] = ()) -> list[tuple[tuple[str, ...], list[str]]]:
    arrays: list[tuple[tuple[str, ...], list[str]]] = []
    if isinstance(value, dict):
        for key, member in value.items():
            if isinstance(key, str):
                arrays.extend(_registry_string_arrays(member, (*path, key)))
    elif isinstance(value, list) and all(isinstance(member, str) for member in value):
        arrays.append((path, value))
    return arrays


def _fenced_yaml_string_arrays(text: str) -> list[tuple[tuple[str, ...], list[str]]]:
    arrays: list[tuple[tuple[str, ...], list[str]]] = []
    for match in re.finditer(r"(?ms)^```(?:yaml|yml)\s*\n(.*?)^```\s*$", text):
        try:
            loaded = _safe_load_unique(match.group(1))
        except yaml.YAMLError:
            continue
        if isinstance(loaded, dict):
            arrays.extend(_registry_string_arrays(loaded))
    return arrays


def validate_repository_contracts(root: pathlib.Path, profiles: dict[str, object]) -> list[Finding]:
    """Validate tracked repository surfaces backed by the canonical registry."""

    _require_git_worktree(root)
    findings: list[Finding] = []
    tracked_markdown = _tracked_repository_markdown(root)

    if any(prefix.startswith("_workspace/") for prefix in TARGET_MARKDOWN_PREFIXES) or _normalized_target_path(
        "_workspace/README.md"
    ) is not None:
        findings.append(
            Finding(
                "scripts/validation/check-document-metadata.py",
                "workspace-inventory-coupling",
                "_workspace must remain outside docs metadata inventory inference",
            )
        )

    classified_readmes: list[Record] = []
    for path in tracked_markdown:
        if path.name != "README.md":
            continue
        try:
            text = (root / path).read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            findings.append(Finding(path.as_posix(), "readme-unreadable", str(error)))
            continue
        record = dataclasses.replace(
            _record_from_text(path, text),
            artifact_type=infer_artifact_type(path),
        )
        matches = matching_readme_profiles(path, profiles)
        if not matches:
            findings.append(Finding(path.as_posix(), "readme-unclassified", "tracked README has no profile"))
        elif len(matches) > 1:
            findings.append(
                Finding(
                    path.as_posix(),
                    "readme-ambiguous",
                    f"tracked README has multiple profiles: {', '.join(matches)}",
                )
            )
        else:
            classified_readmes.append(record)

    readme_manifest = build_manifest(classified_readmes)
    for record in classified_readmes:
        findings.extend(validate_record(record, profiles, readme_manifest))

    template_roles = profiles.get("template_roles", {})
    if not isinstance(template_roles, dict):
        raise ProfileError("template_roles must be a mapping")
    roles_by_source = {
        role["source"]: (name, role)
        for name, role in template_roles.items()
        if isinstance(name, str)
        and isinstance(role, dict)
        and isinstance(role.get("source"), str)
    }
    template_target_types = EXPECTED_PROFILE_TYPES - {
        "generated",
        "governance",
        "readme",
        "template-source",
        "unsupported",
    }
    tracked_templates = [
        path
        for path in tracked_markdown
        if path.as_posix().startswith("docs/99.templates/templates/")
        and path.name != "README.md"
    ]
    for path in tracked_templates:
        try:
            values = parse_frontmatter(root / path)
        except FrontmatterError as error:
            findings.append(Finding(path.as_posix(), "template-source-invalid", str(error)))
            continue
        declares_type = "artifact_type" in values
        declared_type = values.get("artifact_type")
        mapped = roles_by_source.get(path.as_posix())
        mapped_type = mapped[1].get("artifact_profile") if mapped else None
        if path.as_posix() in TRANSITIONAL_UNREGISTERED_TEMPLATE_SOURCES:
            continue
        if not declares_type and mapped_type is None:
            continue
        if not declares_type and mapped_type in {"governance", "readme"}:
            continue
        if declared_type is None:
            findings.append(
                Finding(
                    path.as_posix(),
                    "template-source-missing-type",
                    "registered or typed Markdown template requires a non-null artifact_type",
                )
            )
            continue
        if not isinstance(declared_type, str) or declared_type not in template_target_types:
            findings.append(
                Finding(
                    path.as_posix(),
                    "template-source-unknown-type",
                    f"typed Markdown template declares unsupported artifact_type {declared_type!r}",
                )
            )
        if mapped_type is None:
            findings.append(
                Finding(path.as_posix(), "template-source-unmapped", "typed Markdown template is not registered")
            )
        if mapped_type is not None and declared_type != mapped_type:
            findings.append(
                Finding(
                    path.as_posix(),
                    "template-source-type-mismatch",
                    f"registry target {mapped_type!r} differs from declared artifact_type {declared_type!r}",
                )
            )
    for source_path in sorted(roles_by_source):
        if not (root / source_path).is_file():
            findings.append(
                Finding(source_path, "template-source-missing", "registered Markdown template does not exist")
            )

    release_sources = sorted(
        source_path
        for source_path, (_, role) in roles_by_source.items()
        if role.get("artifact_profile") == "release"
    )
    if len(release_sources) != 1:
        findings.append(
            Finding(
                "docs/99.templates/support/document-metadata-profiles.yaml",
                "release-template-cardinality",
                f"registry must map exactly one Release template; found {len(release_sources)}",
            )
        )
    else:
        release_source = release_sources[0]
        release_name = pathlib.PurePosixPath(release_source).name
        release_route = "docs/05.operations/releases/YYYY-MM-DD-release-name.md"
        route_contracts = {
            "docs/99.templates/support/template-selection.md": (release_route, release_name),
            "docs/00.agent-governance/rules/stage-authoring-matrix.md": (release_route, release_source),
            "docs/05.operations/releases/README.md": ("YYYY-MM-DD-release-name.md", release_name),
        }
        for path_text, required_literals in route_contracts.items():
            path = root / path_text
            try:
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeError):
                text = ""
            missing = [literal for literal in required_literals if literal not in text]
            if missing:
                findings.append(
                    Finding(
                        path_text,
                        "release-route-incomplete",
                        f"missing canonical Release route literals: {', '.join(missing)}",
                    )
                )

    human_support = [
        path
        for path in tracked_markdown
        if path.as_posix().startswith("docs/99.templates/support/") and path.suffix == ".md"
    ]
    registry_arrays_by_key: dict[str, list[tuple[tuple[str, ...], list[str]]]] = collections.defaultdict(list)
    for registry_path, members in _registry_string_arrays(profiles):
        if registry_path:
            registry_arrays_by_key[registry_path[-1]].append((registry_path, members))
    for path in human_support:
        try:
            text = (root / path).read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            findings.append(Finding(path.as_posix(), "support-contract-unreadable", str(error)))
            continue
        duplicated: set[str] = set()
        for candidate_path, candidate_members in _fenced_yaml_string_arrays(text):
            if not candidate_path:
                continue
            for registry_path, registry_members in registry_arrays_by_key.get(candidate_path[-1], []):
                if candidate_members == registry_members:
                    duplicated.add(".".join(registry_path))
        if duplicated:
            findings.append(
                Finding(
                    path.as_posix(),
                    "registry-array-duplicated",
                    f"human support document copies canonical registry arrays: {', '.join(sorted(duplicated))}",
                )
            )

    return sorted(set(findings))


def _normalized_target_path(path_text: str) -> pathlib.Path | None:
    if not path_text.endswith(".md") or "\\" in path_text:
        return None
    pure = pathlib.PurePosixPath(path_text)
    if pure.is_absolute() or any(part in {"", ".", ".."} for part in pure.parts):
        return None
    normalized = pure.as_posix()
    if not normalized.startswith(TARGET_MARKDOWN_PREFIXES):
        return None
    return pathlib.Path(normalized)


def _git_lines(root: pathlib.Path, args: Sequence[str]) -> list[str]:
    result = _run_git(
        root,
        args,
        operation="base resolution",
        text=True,
    )
    if result.returncode != 0:
        return []
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def _verified_commit(root: pathlib.Path, ref: str) -> str | None:
    lines = _git_lines(root, ["rev-parse", "--verify", "--end-of-options", f"{ref}^{{commit}}"])
    return lines[0] if len(lines) == 1 and re.fullmatch(r"[0-9a-fA-F]{40,64}", lines[0]) else None


def resolve_base_selection(root: pathlib.Path, explicit_ref: str | None) -> BaseSelection:
    """Resolve a safe comparison base without ever falling back to the full corpus."""

    if explicit_ref:
        commit = _verified_commit(root, explicit_ref)
        if commit is None:
            raise ProfileError(f"explicit --base-ref is not a commit: {explicit_ref}")
        merge_base = _git_lines(root, ["merge-base", "HEAD", commit])
        if not merge_base:
            raise ProfileError(f"explicit --base-ref has no merge base with HEAD: {explicit_ref}")
        return BaseSelection("explicit", explicit_ref, merge_base[0])

    candidates: list[tuple[str, str]] = []
    template_base = os.environ.get("TEMPLATE_GATE_BASE", "").strip()
    if template_base:
        candidates.append(("env:TEMPLATE_GATE_BASE", template_base))
    github_base = os.environ.get("GITHUB_BASE_REF", "").strip()
    if github_base:
        candidates.extend(
            [
                ("env:GITHUB_BASE_REF", f"origin/{github_base}"),
                ("env:GITHUB_BASE_REF", github_base),
            ]
        )
    candidates.extend(
        [
            ("local:upstream", "@{upstream}"),
            ("local:origin/main", "origin/main"),
            ("local:main", "main"),
        ]
    )
    seen: set[str] = set()
    for source, ref in candidates:
        if ref in seen:
            continue
        seen.add(ref)
        commit = _verified_commit(root, ref)
        if commit is None:
            continue
        merge_base = _git_lines(root, ["merge-base", "HEAD", commit])
        if merge_base:
            return BaseSelection(source, ref, merge_base[0])
    return BaseSelection("fallback:working-tree-only", None, None)


def _metadata_at_ref(root: pathlib.Path, path: pathlib.Path, base_ref: str | None) -> dict[str, object] | None:
    if not base_ref:
        return None
    result = _run_git(
        root,
        ["show", f"{base_ref}:{path.as_posix()}"],
        operation="prior metadata discovery",
        text=True,
    )
    if result.returncode != 0:
        return None
    try:
        return _parse_frontmatter_text(result.stdout)
    except FrontmatterError:
        return None


def _previous_status(root: pathlib.Path, path: pathlib.Path, base_ref: str | None) -> str | None:
    loaded = _metadata_at_ref(root, path, base_ref)
    return loaded.get("status") if isinstance(loaded, dict) and isinstance(loaded.get("status"), str) else None


def _record_from_text(
    relative_path: pathlib.Path,
    text: str,
    previous_status: str | None = None,
) -> Record:
    lines = text.splitlines()
    frontmatter_present = bool(lines and lines[0].strip() == "---")
    try:
        values = _parse_frontmatter_text(text)
        parse_error = None
        parse_error_code = None
    except FrontmatterError as error:
        values = {}
        parse_error = str(error)
        parse_error_code = error.code
    artifact_type = "generated" if "generated_by" in values else infer_artifact_type(relative_path)
    return Record(
        relative_path,
        values,
        artifact_type,
        previous_status=previous_status,
        parse_error=parse_error,
        parse_error_code=parse_error_code,
        frontmatter_present=frontmatter_present,
    )


def collect_records_at_ref(
    root: pathlib.Path,
    profiles: dict[str, object],
    base_ref: str,
) -> list[Record]:
    """Collect and parse the exact target Markdown corpus stored at a Git ref."""

    common, _ = _profile_mapping(profiles)
    excluded = set(common.get("inventory_excludes", []))
    result = _run_git(
        root,
        ["ls-tree", "-r", "-z", "--name-only", base_ref, "--", "docs"],
        operation="base Markdown discovery",
    )
    if result.returncode != 0:
        raise ProfileError(f"cannot enumerate Markdown records at base ref: {base_ref}")
    paths = sorted(
        {
            path
            for path in _decode_git_paths(result.stdout, "base Markdown discovery")
            if path.as_posix().endswith(".md")
            and path.as_posix().startswith(TARGET_MARKDOWN_PREFIXES)
            and path.as_posix() not in excluded
        },
        key=lambda path: path.as_posix(),
    )
    records: list[Record] = []
    for relative_path in paths:
        shown = _run_git(
            root,
            ["show", f"{base_ref}:{relative_path.as_posix()}"],
            operation="base Markdown record discovery",
            text=True,
        )
        if shown.returncode != 0:
            raise ProfileError(f"cannot read base Markdown record: {relative_path.as_posix()}")
        records.append(_record_from_text(relative_path, shown.stdout))
    return records


def collect_selected_records_at_ref(
    root: pathlib.Path,
    selected_paths: Sequence[str],
    ref: str,
) -> dict[str, Record]:
    """Collect selected records that exist at a ref without scanning its full corpus."""

    records: dict[str, Record] = {}
    for path_text in sorted(set(selected_paths)):
        relative_path = _normalized_target_path(path_text)
        if relative_path is None:
            continue
        shown = _run_git(
            root,
            ["show", f"{ref}:{relative_path.as_posix()}"],
            operation="selected historical record discovery",
            text=True,
        )
        if shown.returncode == 0:
            records[relative_path.as_posix()] = _record_from_text(relative_path, shown.stdout)
    return records


def collect_records(
    root: pathlib.Path,
    profiles: dict[str, object],
    base_ref: str | None = None,
    selected_paths: Sequence[str] = (),
    previous_records: Mapping[str, Record] | None = None,
    require_git: bool = False,
) -> list[Record]:
    """Collect tracked records plus selected existing new paths, excluding deletions."""

    common, _ = _profile_mapping(profiles)
    excluded = set(common.get("inventory_excludes", []))
    candidates = set(_tracked_markdown(root, require_git=require_git))
    for path_text in selected_paths:
        candidate = _normalized_target_path(path_text)
        if candidate is not None and (root / candidate).is_file():
            candidates.add(candidate)
    records: list[Record] = []
    for relative_path in sorted(candidates, key=lambda path: path.as_posix()):
        if relative_path.as_posix() in excluded:
            continue
        absolute_path = root / relative_path
        if not absolute_path.is_file():
            continue
        try:
            text = absolute_path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            records.append(
                Record(
                    relative_path,
                    {},
                    infer_artifact_type(relative_path),
                    parse_error=f"cannot read UTF-8 Markdown: {error}",
                    parse_error_code="malformed-yaml",
                )
            )
            continue
        previous_record = (previous_records or {}).get(relative_path.as_posix())
        previous_status = (
            previous_record.metadata.get("status")
            if previous_record and isinstance(previous_record.metadata.get("status"), str)
            else _previous_status(root, relative_path, base_ref)
        )
        records.append(_record_from_text(relative_path, text, previous_status=previous_status))
    return records


def load_transition_overrides(
    path: pathlib.Path,
    root: pathlib.Path,
    profiles: dict[str, object],
) -> dict[tuple[str, str, str], TransitionOverride]:
    """Load explicit, path-scoped reverse-transition approval evidence."""

    try:
        loaded = _safe_load_unique(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as error:
        raise ProfileError(f"cannot load transition override file: {error}") from error
    if not isinstance(loaded, dict) or set(loaded) != {"transition_overrides"}:
        raise ProfileError("transition override file must contain only transition_overrides")
    rows = loaded.get("transition_overrides")
    if not isinstance(rows, list) or not rows:
        raise ProfileError("transition_overrides must be a non-empty list")
    common, _ = _profile_mapping(profiles)
    allowed_statuses = set(common.get("allowed_statuses", []))
    expected_keys = {
        "path",
        "previous_status",
        "new_status",
        "evidence_task",
        "approval",
        "reason",
    }
    overrides: dict[tuple[str, str, str], TransitionOverride] = {}
    for index, row in enumerate(rows):
        if not isinstance(row, dict) or set(row) != expected_keys:
            raise ProfileError(f"transition override row {index} must define the exact evidence fields")
        if not all(isinstance(row[key], str) and row[key].strip() for key in expected_keys):
            raise ProfileError(f"transition override row {index} values must be non-empty strings")
        target = _normalized_target_path(row["path"])
        evidence = _normalized_target_path(row["evidence_task"])
        if target is None or not (root / target).is_file():
            raise ProfileError(f"transition override row {index} target path is not an existing canonical document")
        if (
            evidence is None
            or not evidence.as_posix().startswith("docs/04.execution/tasks/")
            or not (root / evidence).is_file()
        ):
            raise ProfileError(f"transition override row {index} evidence_task must be an existing Stage 04 task")
        previous_status = row["previous_status"].strip()
        new_status = row["new_status"].strip()
        if previous_status not in allowed_statuses or new_status not in allowed_statuses:
            raise ProfileError(f"transition override row {index} uses an unknown lifecycle status")
        if previous_status == new_status:
            raise ProfileError(f"transition override row {index} does not describe a transition")
        override = TransitionOverride(
            target.as_posix(),
            previous_status,
            new_status,
            evidence.as_posix(),
            row["approval"].strip(),
            row["reason"].strip(),
        )
        key = (override.path, override.previous_status, override.new_status)
        if key in overrides:
            raise ProfileError(f"duplicate transition override scope: {' -> '.join(key)}")
        overrides[key] = override
    return overrides


def _legacy_deficit_identity(finding: Finding) -> tuple[str, str]:
    return finding.code, finding.message


def _legacy_exception_evidence(
    record: Record,
    findings: Sequence[Finding],
    base_record: Record | None,
    base_findings: Sequence[Finding],
) -> tuple[int, int] | None:
    if record.path.as_posix() in APPROVED_MIGRATION_PATHS or record.parse_error or base_record is None:
        return None
    if record.artifact_type in {"readme", "generated", "template-source", "governance", "archive", "unsupported"}:
        return None
    if base_record.parse_error or MIGRATION_TYPED_KEYS & set(base_record.metadata) or MIGRATION_TYPED_KEYS & set(record.metadata):
        return None
    current_errors = [finding for finding in findings if finding.severity == "error"]
    base_errors = [finding for finding in base_findings if finding.severity == "error"]
    if not current_errors:
        return None
    if any(finding.code not in LEGACY_EXCEPTION_CODES for finding in [*base_errors, *current_errors]):
        return None
    current_deficits = {_legacy_deficit_identity(finding) for finding in current_errors}
    base_deficits = {_legacy_deficit_identity(finding) for finding in base_errors}
    if not current_deficits <= base_deficits:
        return None
    return len(current_deficits), len(base_deficits)


def _relation_impact_findings(
    selected_paths: set[str],
    records_by_path: Mapping[str, Record],
    head_records_by_path: Mapping[str, Record],
    base_records_by_path: Mapping[str, Record],
    manifest: Manifest,
    findings_by_path: Mapping[str, Sequence[Finding]],
) -> dict[str, list[Finding]]:
    """Return only relation findings newly caused by selected typed identity removal."""

    removed_ids: set[str] = set()
    for path in sorted(selected_paths):
        for previous in (head_records_by_path.get(path), base_records_by_path.get(path)):
            artifact_id = previous.metadata.get("artifact_id") if previous else None
            if isinstance(artifact_id, str) and artifact_id.strip() and artifact_id.strip() not in manifest:
                removed_ids.add(artifact_id.strip())
    if not removed_ids:
        return {}

    expected_messages = {
        "unresolved-parent": {
            f"parent artifact_id is unresolved: {artifact_id}" for artifact_id in removed_ids
        },
        "unresolved-supersedes": {
            f"superseded artifact_id is unresolved: {artifact_id}" for artifact_id in removed_ids
        },
    }
    impacted: dict[str, list[Finding]] = {}
    for path, findings in sorted(findings_by_path.items()):
        relation_findings = [
            finding
            for finding in findings
            if finding.severity == "error"
            and finding.message in expected_messages.get(finding.code, set())
        ]
        if relation_findings:
            impacted[path] = sorted(relation_findings)
    return impacted


def _escape_cell(value: object) -> str:
    rendered = str(value).replace("|", "\\|").replace("\n", " ")
    return rendered or "—"


def _profile_sets(profile: dict[str, object]) -> tuple[set[str], set[str], set[str]]:
    return (
        set(profile.get("required", [])),
        set(profile.get("optional", [])),
        set(profile.get("forbidden", [])),
    )


def _frontmatter_state(record: Record, findings: Sequence[Finding]) -> str:
    if record.parse_error_code:
        return record.parse_error_code
    if not record.frontmatter_present:
        return "missing-fence"
    if any(finding.severity == "error" for finding in findings):
        return "profile-semantic-error"
    return "allowed-syntax"


def _identity_state(record: Record, profile: dict[str, object], codes: set[str]) -> str:
    if record.parse_error:
        return "unavailable-parser-error"
    required, optional, forbidden = _profile_sets(profile)
    value = record.metadata.get("artifact_id")
    if "artifact_id" in forbidden:
        return "not-applicable"
    if value is None:
        return "missing" if "artifact_id" in required else "not-provided-optional"
    if "invalid-artifact-id" in codes:
        return "invalid"
    if "duplicate-artifact-id" in codes:
        return "duplicate"
    return "valid" if "artifact_id" in required | optional else "type-inappropriate"


def _relation_state(record: Record, profile: dict[str, object], codes: set[str]) -> str:
    if record.parse_error:
        return "unavailable-parser-error"
    required, optional, forbidden = _profile_sets(profile)
    if "parent_ids" in forbidden:
        parent_state = "not-applicable"
        order_state = "not-applicable"
    elif "parent_ids" not in record.metadata:
        parent_state = "missing" if "parent_ids" in required else "not-provided-optional"
        order_state = "not-provided"
    else:
        relation_errors = sorted(
            codes
            & {
                "invalid-parent-ids",
                "duplicate-parent",
                "missing-parent",
                "self-parent",
                "unresolved-parent",
                "invalid-parent-type",
                "parent-cycle",
            }
        )
        parents = _string_list(record.metadata.get("parent_ids"))
        order_state = "declared-list" if parents is not None else "invalid"
        if relation_errors:
            parent_state = "invalid:" + ",".join(relation_errors)
        elif parents:
            parent_state = f"resolved:{len(parents)}"
        else:
            parent_state = "root-permitted"
    if "supersedes" not in record.metadata:
        return f"parents={parent_state}; order={order_state}; supersedes=not-provided"
    supersession_errors = sorted(code for code in codes if "supersed" in code or "supersession" in code)
    supersedes_state = "invalid:" + ",".join(supersession_errors) if supersession_errors else "resolved"
    return f"parents={parent_state}; order={order_state}; supersedes={supersedes_state}"


def _lifecycle_state(record: Record, profile: dict[str, object], codes: set[str]) -> str:
    if record.parse_error:
        return "unavailable-parser-error"
    required, optional, forbidden = _profile_sets(profile)
    if "status" in forbidden:
        return "not-applicable"
    status = record.metadata.get("status")
    if status is None:
        return "missing" if "status" in required else "not-provided-optional"
    signals = sorted(
        codes & {"invalid-status", "stale-active", "replacement-free-supersession", "archived-outside-stage-98"}
    )
    state = "invalid" if "invalid-status" in signals else "allowed"
    suffix = "; signals=" + ",".join(signals) if signals else ""
    rendered_status = "invalid-value" if "invalid-status" in signals else status
    return f"status={rendered_status}; {state}{suffix}"


def _transition_state(record: Record, profile: dict[str, object], codes: set[str]) -> str:
    if record.parse_error:
        return "unavailable-parser-error"
    if record.artifact_type in {"readme", "generated", "template-source", "governance", "unsupported"}:
        return "not-applicable"
    required, optional, forbidden = _profile_sets(profile)
    if "status" in forbidden or "status" not in required | optional:
        return "not-applicable"
    status = record.metadata.get("status")
    if not isinstance(status, str):
        return "not-applicable"
    if record.previous_status is None:
        return "unavailable-no-history"
    if record.previous_status == status:
        return "available-unchanged"
    verdict = "invalid" if "invalid-transition" in codes else "valid"
    return f"available:{record.previous_status}->{status}; {verdict}"


def _freshness_state(record: Record, profile: dict[str, object], codes: set[str]) -> str:
    if record.parse_error:
        return "unavailable-parser-error"
    required, optional, forbidden = _profile_sets(profile)
    states: list[str] = []
    invalid_codes = {"reviewed_at": "invalid-reviewed-at", "review_cycle": "invalid-review-cycle"}
    for key in ("reviewed_at", "review_cycle"):
        disposition = "required" if key in required else "optional" if key in optional else "forbidden"
        if key in forbidden and key not in record.metadata:
            evidence = "not-applicable"
        elif key not in record.metadata:
            evidence = "missing" if disposition == "required" else "not-provided"
        elif invalid_codes[key] in codes:
            evidence = "invalid"
        else:
            evidence = "present"
        states.append(f"{key}={disposition}:{evidence}")
    return "; ".join(states)


def _exception_context(record: Record, codes: set[str], profiles: dict[str, object]) -> str:
    if record.parse_error:
        return "unavailable-parser-error"
    if record.artifact_type == "readme":
        matches = matching_readme_profiles(record.path, profiles)
        if not matches:
            return "README profile=unclassified; consumer=unavailable; role=folder-index"
        if len(matches) > 1:
            return (
                f"README profile=ambiguous({','.join(matches)}); "
                "consumer=unavailable; role=folder-index"
            )
        profile_name = matches[0]
        readme_profiles = profiles.get("readme_profiles", {})
        raw_profile = readme_profiles.get(profile_name, {}) if isinstance(readme_profiles, dict) else {}
        declared_consumer = raw_profile.get("frontmatter_consumer") if isinstance(raw_profile, dict) else None
        consumer = declared_consumer if isinstance(declared_consumer, str) and declared_consumer else "not-declared"
        return f"README profile={profile_name}; consumer={consumer}; role=folder-index"
    if record.artifact_type == "generated":
        owner = record.metadata.get("generated_by")
        rendered = owner if isinstance(owner, str) and "invalid-generator" not in codes else "invalid-or-missing"
        return f"generated profile; owner={rendered}"
    if record.artifact_type in {"template-source", "governance", "archive", "unsupported"}:
        return f"{record.artifact_type} profile"
    return "not-applicable"


def render_report(
    records: Sequence[Record],
    profiles: dict[str, object],
    findings_by_path: dict[str, list[Finding]],
) -> str:
    """Render the deterministic exhaustive advisory Markdown inventory."""

    _, profile_map = _profile_mapping(profiles)
    profile_counts = collections.Counter(record.artifact_type for record in records)
    finding_counts = collections.Counter(
        finding.code for findings in findings_by_path.values() for finding in findings
    )
    semantic_count = sum(1 for findings in findings_by_path.values() if findings)
    parse_count = sum(1 for record in records if record.parse_error)
    lines = [
        "---",
        "status: active",
        "generated_by: scripts/validation/check-document-metadata.py",
        "---",
        "",
        "<!-- Target: docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/frontmatter-semantic-inventory.md -->",
        "",
        "# Reference: Frontmatter Semantic Inventory",
        "",
        "## Overview",
        "",
        "This generated advisory reference inventories every tracked target-stage and",
        "governance/template Markdown document except this self-referential output. It records inferred profiles",
        "and metadata findings without printing body content, secret values, or raw logs.",
        "",
        "## Purpose",
        "",
        "Provide the deterministic pre/post-migration comparison for Spec 123 Tasks 7 and 8.",
        "Historical semantic findings remain advisory here; the separate changed/new",
        "checker enforces only its safely selected diff scope.",
        "",
        "## Repository Role",
        "",
        "Stage 00 and Stage 99 own active metadata policy. This Stage 90 snapshot is",
        "generated evidence only; regenerate it with `check-document-metadata.py`.",
        "",
        "## Scope",
        "",
        "### In Scope",
        "",
        "- Tracked Markdown paths, inferred profiles, safe frontmatter parse state, and finding codes",
        "- Identity, parent, lifecycle, freshness, README, generated, governance, template, and archive profiles",
        "",
        "### Out of Scope",
        "",
        "- Automatic document rewrites, corpus-wide blocking, or lifecycle changes",
        "- Filesystem modification times as freshness evidence",
        "- Raw document bodies, logs, credentials, or secret values",
        "",
        "## Definitions / Facts",
        "",
        f"- **Tracked records**: {len(records)}",
        f"- **Records with findings**: {semantic_count}",
        f"- **Frontmatter parser failures**: {parse_count}",
        "- **Enforcement state**: full inventory advisory; changed/new pre-push selection blocking",
        "",
        "## Profile Summary",
        "",
        "| Profile | Records |",
        "| --- | ---: |",
    ]
    lines.extend(f"| `{name}` | {count} |" for name, count in sorted(profile_counts.items()))
    lines.extend(["", "## Finding Summary", "", "| Finding | Count |", "| --- | ---: |"])
    if finding_counts:
        lines.extend(f"| `{code}` | {count} |" for code, count in sorted(finding_counts.items()))
    else:
        lines.append("| `none` | 0 |")
    lines.extend(
        [
            "",
            "## Inventory",
            "",
            "| Path | Profile | Frontmatter | Identity | Relations | Lifecycle | Transition Evidence | Freshness | Exception Context | Findings | Disposition |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for record in sorted(records, key=lambda item: item.path.as_posix()):
        findings = findings_by_path.get(record.path.as_posix(), [])
        code_set = {finding.code for finding in findings}
        codes = ", ".join(sorted(code_set)) or "none"
        raw_profile = profile_map.get(record.artifact_type, {})
        disposition = raw_profile.get("disposition", "advisory-only") if isinstance(raw_profile, dict) else "advisory-only"
        row = [
            f"`{record.path.as_posix()}`",
            f"`{record.artifact_type}`",
            _frontmatter_state(record, findings),
            _identity_state(record, raw_profile, code_set),
            _relation_state(record, raw_profile, code_set),
            _lifecycle_state(record, raw_profile, code_set),
            _transition_state(record, raw_profile, code_set),
            _freshness_state(record, raw_profile, code_set),
            _exception_context(record, code_set, profiles),
            codes,
            disposition,
        ]
        lines.append("| " + " | ".join(_escape_cell(value) for value in row) + " |")
    lines.extend(
        [
            "",
            "## Source Rules",
            "",
            "- Paths come from sorted `git ls-files '*.md'` output filtered to canonical docs stages; non-Git fixtures use sorted recursive discovery.",
            "- YAML is parsed with PyYAML `safe_load` behavior plus duplicate-key rejection.",
            "- Every row states parse, identity, relation, lifecycle, transition-evidence, freshness, and exception semantics; unavailable history is never inferred.",
            "- The report shows only bounded metadata states, safe repository paths, counts, and finding codes.",
            "- Graphify is advisory and is not used as inventory proof.",
            "",
            "## Sources",
            "",
            "- [Frontmatter contract](../../../99.templates/support/frontmatter-contract.md) - metadata ownership and exception rules",
            "- [Lifecycle status](../../../99.templates/support/lifecycle-status.md) - lifecycle vocabulary and transitions",
            "- [Spec 123](../../../03.specs/123-agentic-engineering-audit-remediation/spec.md) - typed metadata and rollout contract",
            "- [Semantic audit](./frontmatter-template-readme-implementation.md) - pre-remediation criteria and baseline",
            "",
            "## Maintenance",
            "",
            "- **Owner**: Metadata program owner / rules-engineer",
            "- **Review Cadence**: Regenerate when tracked Markdown or metadata profiles change",
            "- **Update Trigger**: Profile, parser, lifecycle, relation, exception, or corpus changes",
            "",
            "## Related Documents",
            "",
            "- [Audit pack README](./README.md)",
            "- [Frontmatter/template/README audit](./frontmatter-template-readme-implementation.md)",
            "- [SDLC and document-contract audit](./sdlc-document-contracts-implementation.md)",
            "",
        ]
    )
    return "\n".join(lines)


def _changed_paths(
    root: pathlib.Path,
    explicit: Sequence[str],
    base: BaseSelection,
) -> set[str]:
    changed: set[str] = set()
    commands = [
        (
            "unstaged Markdown discovery",
            ["diff", "--name-only", "-z", "--diff-filter=ACDMRT", "--", "*.md"],
        ),
        (
            "staged Markdown discovery",
            ["diff", "--cached", "--name-only", "-z", "--diff-filter=ACDMRT", "--", "*.md"],
        ),
        (
            "untracked Markdown discovery",
            ["ls-files", "-z", "--others", "--exclude-standard", "--", "*.md"],
        ),
    ]
    if base.merge_base:
        commands.insert(
            0,
            (
                "committed branch Markdown discovery",
                [
                    "diff",
                    "--name-only",
                    "-z",
                    "--diff-filter=ACDMRT",
                    f"{base.merge_base}...HEAD",
                    "--",
                    "*.md",
                ],
            ),
        )
    for operation, command in commands:
        result = _run_git(root, command, operation=operation)
        if result.returncode != 0:
            raise ProfileError(f"cannot establish local Git snapshot: {operation} failed")
        changed.update(
            normalized.as_posix()
            for path in _decode_git_paths(result.stdout, operation)
            if (normalized := _normalized_target_path(path.as_posix())) is not None
        )
    if explicit:
        return {
            normalized.as_posix()
            for path in explicit
            if (normalized := _normalized_target_path(path)) is not None
        }
    return changed


def _write_or_check_output(output: pathlib.Path, rendered: str, check: bool) -> bool:
    if check:
        try:
            return output.read_text(encoding="utf-8") == rendered
        except OSError:
            return False
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(rendered, encoding="utf-8")
    return True


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--mode",
        choices=("report", "check-changed", "check-active", "check-contracts"),
        default="report",
    )
    parser.add_argument("--root", type=pathlib.Path, default=ROOT)
    parser.add_argument("--profiles", type=pathlib.Path, default=DEFAULT_PROFILES)
    parser.add_argument("--output", type=pathlib.Path)
    parser.add_argument("--check", action="store_true", help="compare --output without writing")
    parser.add_argument("--changed-path", action="append", default=[])
    parser.add_argument("--base-ref", default=None, help="optional Git ref for lifecycle transition comparison")
    parser.add_argument(
        "--transition-override-file",
        type=pathlib.Path,
        help="explicit scoped reverse-transition approval evidence",
    )
    args = parser.parse_args(argv)
    if args.check and args.output is None:
        parser.error("--check requires --output")
    root = args.root.resolve()
    try:
        profiles = load_profiles(args.profiles.resolve())
    except ProfileError as error:
        print(f"configuration-error: {error}", file=sys.stderr)
        return 2
    if args.mode == "check-contracts":
        try:
            contract_findings = validate_repository_contracts(root, profiles)
        except ProfileError as error:
            print(f"configuration-error: {error}", file=sys.stderr)
            return 2
        for finding in contract_findings:
            print(f"{finding.code}: {finding.path}: {finding.message}")
        print(f"metadata repository contracts: violations={len(contract_findings)}")
        return 1 if contract_findings else 0
    base = BaseSelection("not-applicable", None, None)
    transition_overrides: dict[tuple[str, str, str], TransitionOverride] = {}
    changed_selection: set[str] = set()
    if args.mode == "check-changed":
        try:
            _require_git_worktree(root)
            base = resolve_base_selection(root, args.base_ref)
            if args.transition_override_file:
                transition_overrides = load_transition_overrides(
                    args.transition_override_file.resolve(),
                    root,
                    profiles,
                )
            changed_selection = _changed_paths(root, args.changed_path, base)
        except ProfileError as error:
            print(f"configuration-error: {error}", file=sys.stderr)
            return 2
        if base.merge_base:
            print(
                f"metadata base: source={base.source} ref={base.ref} merge_base={base.merge_base}",
                file=sys.stderr,
            )
        else:
            print(
                "metadata base: fallback=working-tree-only; committed branch delta unavailable; full corpus not selected",
                file=sys.stderr,
            )
    elif args.transition_override_file:
        print("configuration-error: --transition-override-file requires --mode check-changed", file=sys.stderr)
        return 2
    base_records: list[Record] = []
    if base.merge_base:
        try:
            base_records = collect_records_at_ref(root, profiles, base.merge_base)
        except ProfileError as error:
            print(f"configuration-error: {error}", file=sys.stderr)
            return 2
    base_records_by_path = {record.path.as_posix(): record for record in base_records}
    try:
        records = collect_records(
            root,
            profiles,
            selected_paths=sorted(changed_selection),
            previous_records=base_records_by_path,
            require_git=args.mode == "check-changed",
        )
    except ProfileError as error:
        print(f"configuration-error: {error}", file=sys.stderr)
        return 2
    manifest = build_manifest(records)
    base_manifest = build_manifest(base_records)
    base_findings_by_path = {
        record.path.as_posix(): validate_record(record, profiles, base_manifest)
        for record in base_records
        if record.path.as_posix() in changed_selection
    }
    findings_by_path = {
        record.path.as_posix(): validate_record(
            record,
            profiles,
            manifest,
            transition_overrides=transition_overrides,
        )
        for record in records
    }
    records_by_path = {record.path.as_posix(): record for record in records}
    relation_impact_findings: dict[str, list[Finding]] = {}
    if args.mode == "check-changed":
        try:
            head_records_by_path = collect_selected_records_at_ref(
                root,
                changed_selection,
                "HEAD",
            )
        except ProfileError as error:
            print(f"configuration-error: {error}", file=sys.stderr)
            return 2
        relation_impact_findings = _relation_impact_findings(
            changed_selection,
            records_by_path,
            head_records_by_path,
            base_records_by_path,
            manifest,
            findings_by_path,
        )
    parser_failures = [record for record in records if record.parse_error]
    rendered = render_report(records, profiles, findings_by_path)

    if args.mode == "report":
        if args.output:
            output = args.output if args.output.is_absolute() else root / args.output
            fresh = _write_or_check_output(output, rendered, args.check)
            if args.check and not fresh:
                print(f"metadata inventory is stale: {output}", file=sys.stderr)
                return 1
            action = "fresh" if args.check else "generated"
            print(f"metadata inventory {action}: records={len(records)} findings={sum(map(len, findings_by_path.values()))}")
        else:
            sys.stdout.write(rendered)
        return 2 if parser_failures else 0

    directly_selected_paths = (
        changed_selection
        if args.mode == "check-changed"
        else {record.path.as_posix() for record in records if record.metadata.get("status") == "active"}
    )
    selected_paths = directly_selected_paths | set(relation_impact_findings)
    legacy_exception_evidence = {
        path: evidence
        for path in selected_paths
        if path in records_by_path
        and (
            evidence := _legacy_exception_evidence(
                records_by_path[path],
                findings_by_path.get(path, []),
                base_records_by_path.get(path),
                base_findings_by_path.get(path, []),
            )
        )
        is not None
    }
    legacy_exceptions = set(legacy_exception_evidence)
    for path, (current_count, base_count) in sorted(legacy_exception_evidence.items()):
        print(
            f"{path}: legacy metadata exception: base-existing unmigrated document outside approved Task 8 scope; "
            f"current_deficits={current_count} base_deficits={base_count} new_deficits=0",
            file=sys.stderr,
        )
    selected_findings = sorted(
        {
            finding
            for path in directly_selected_paths - legacy_exceptions
            for finding in findings_by_path.get(path, [])
            if finding.severity == "error"
        }
        | {
            finding
            for path, findings in relation_impact_findings.items()
            if path not in legacy_exceptions
            for finding in findings
        }
    )
    for finding in selected_findings:
        print(f"{finding.path}: {finding.code}: {finding.message}")
    print(
        f"metadata {args.mode}: selected={len(selected_paths)} violations={len(selected_findings)} "
        f"legacy_exceptions={len(legacy_exceptions)} transition_overrides={len(transition_overrides)}"
    )
    return 1 if selected_findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
