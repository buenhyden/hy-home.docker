#!/usr/bin/env python3
"""Validate typed Markdown metadata and render an advisory inventory."""

from __future__ import annotations

import argparse
import collections
import dataclasses
import datetime as dt
import pathlib
import subprocess
import sys
from collections.abc import Sequence
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
    "runbook",
    "spec",
    "task",
    "template-source",
    "unsupported",
}
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


class FrontmatterError(ValueError):
    """Raised when a Markdown frontmatter block cannot be parsed safely."""


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
        if key in mapping:
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


def parse_frontmatter(path: pathlib.Path) -> dict[str, object]:
    """Return top-of-file YAML frontmatter, or an empty mapping when absent."""

    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise FrontmatterError(f"cannot read UTF-8 Markdown: {error}") from error
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
        raise FrontmatterError(f"invalid YAML frontmatter: {summary}") from error
    if loaded is None:
        return {}
    if not isinstance(loaded, dict) or not all(isinstance(key, str) for key in loaded):
        raise FrontmatterError("frontmatter must be a string-keyed YAML mapping")
    return dict(loaded)


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


def validate_record(
    record: Record,
    profiles: dict[str, object],
    manifest: dict[str, pathlib.Path],
) -> list[Finding]:
    """Validate one record against its typed profile and the global manifest."""

    common, profile_map = _profile_mapping(profiles)
    raw_profile = profile_map.get(record.artifact_type)
    if not isinstance(raw_profile, dict):
        return [_finding(record, "unknown-profile", f"profile is not configured: {record.artifact_type}")]
    typed_manifest = manifest if isinstance(manifest, Manifest) else Manifest(dict(manifest), {}, {})
    findings: list[Finding] = []
    if record.parse_error:
        findings.append(_finding(record, "frontmatter-parse-error", record.parse_error))
        return findings
    if record.artifact_type == "unsupported":
        findings.append(
            _finding(
                record,
                "unsupported-profile",
                "path is outside the typed document corpus",
                severity="warning",
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
        if status not in allowed_next:
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
        if not parent_ids and not raw_profile.get("allow_empty_parents", False):
            findings.append(_finding(record, "missing-parent", "this artifact profile does not permit a root"))
        allowed_parent_types = set(raw_profile.get("allowed_parent_types", []))
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
    if reviewed_at is not None and not isinstance(reviewed_at, (str, dt.date)):
        findings.append(_finding(record, "invalid-reviewed-at", "reviewed_at must be an ISO date"))
    review_cycle = record.metadata.get("review_cycle")
    if review_cycle is not None and (not isinstance(review_cycle, str) or not review_cycle.strip()):
        findings.append(_finding(record, "invalid-review-cycle", "review_cycle must be a non-empty string"))
    generated_by = record.metadata.get("generated_by")
    if generated_by is not None and (not isinstance(generated_by, str) or not generated_by.strip()):
        findings.append(_finding(record, "invalid-generator", "generated_by must be a non-empty script path"))

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
    if loaded.get("schema_version") != 1:
        raise ProfileError("schema_version must equal 1")
    common, profile_map = _profile_mapping(loaded)
    actual_types = set(profile_map)
    if actual_types != EXPECTED_PROFILE_TYPES:
        missing = ", ".join(sorted(EXPECTED_PROFILE_TYPES - actual_types)) or "none"
        unexpected = ", ".join(sorted(actual_types - EXPECTED_PROFILE_TYPES)) or "none"
        raise ProfileError(f"profile type mismatch; missing={missing}; unexpected={unexpected}")
    if not isinstance(common.get("transitions"), dict):
        raise ProfileError("common.transitions must be a mapping")
    for name, raw_profile in sorted(profile_map.items()):
        if not isinstance(raw_profile, dict):
            raise ProfileError(f"profile {name} must be a mapping")
        required = raw_profile.get("required")
        optional = raw_profile.get("optional")
        forbidden = raw_profile.get("forbidden")
        if not all(isinstance(value, list) and all(isinstance(item, str) for item in value) for value in (required, optional, forbidden)):
            raise ProfileError(f"profile {name} required/optional/forbidden must be string lists")
        overlap = (set(required) & set(optional)) | (set(required) & set(forbidden)) | (set(optional) & set(forbidden))
        if overlap:
            raise ProfileError(f"profile {name} has overlapping key dispositions: {', '.join(sorted(overlap))}")
        if not isinstance(raw_profile.get("allowed_statuses"), list):
            raise ProfileError(f"profile {name} allowed_statuses must be a list")
        if not isinstance(raw_profile.get("allowed_parent_types"), list):
            raise ProfileError(f"profile {name} allowed_parent_types must be a list")
        unknown_parents = set(raw_profile["allowed_parent_types"]) - EXPECTED_PROFILE_TYPES
        if unknown_parents:
            raise ProfileError(f"profile {name} has unknown parent types: {', '.join(sorted(unknown_parents))}")
    return loaded


def _tracked_markdown(root: pathlib.Path) -> list[pathlib.Path]:
    result = subprocess.run(
        ["git", "-C", str(root), "ls-files", "-z", "--", "*.md"],
        capture_output=True,
        check=False,
    )
    if result.returncode == 0:
        paths = [pathlib.Path(item.decode("utf-8")) for item in result.stdout.split(b"\0") if item]
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


def _previous_status(root: pathlib.Path, path: pathlib.Path, base_ref: str | None) -> str | None:
    if not base_ref:
        return None
    result = subprocess.run(
        ["git", "-C", str(root), "show", f"{base_ref}:{path.as_posix()}"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return None
    lines = result.stdout.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    closing = next((index for index in range(1, len(lines)) if lines[index].strip() == "---"), None)
    if closing is None:
        return None
    try:
        loaded = _safe_load_unique("\n".join(lines[1:closing]))
    except yaml.YAMLError:
        return None
    return loaded.get("status") if isinstance(loaded, dict) and isinstance(loaded.get("status"), str) else None


def collect_records(
    root: pathlib.Path,
    profiles: dict[str, object],
    base_ref: str | None = None,
) -> list[Record]:
    """Collect sorted tracked Markdown records without reading document bodies into output."""

    common, _ = _profile_mapping(profiles)
    excluded = set(common.get("inventory_excludes", []))
    records: list[Record] = []
    for relative_path in _tracked_markdown(root):
        if relative_path.as_posix() in excluded:
            continue
        absolute_path = root / relative_path
        try:
            values = parse_frontmatter(absolute_path)
            parse_error = None
        except FrontmatterError as error:
            values = {}
            parse_error = str(error)
        artifact_type = "generated" if "generated_by" in values else infer_artifact_type(relative_path)
        records.append(
            Record(
                relative_path,
                values,
                artifact_type,
                previous_status=_previous_status(root, relative_path, base_ref),
                parse_error=parse_error,
            )
        )
    return records


def _escape_cell(value: object) -> str:
    rendered = str(value).replace("|", "\\|").replace("\n", " ")
    return rendered or "—"


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
        "Provide the deterministic pre-migration baseline for Spec 123 Tasks 7 and 8.",
        "Semantic findings are advisory here and do not authorize metadata migration or",
        "changed/new blocking enforcement.",
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
        "- Automatic document rewrites or lifecycle changes",
        "- Filesystem modification times as freshness evidence",
        "- Raw document bodies, logs, credentials, or secret values",
        "",
        "## Definitions / Facts",
        "",
        f"- **Tracked records**: {len(records)}",
        f"- **Records with findings**: {semantic_count}",
        f"- **Frontmatter parser failures**: {parse_count}",
        "- **Enforcement state**: advisory-only; repository contracts check syntax, tests, and snapshot freshness only",
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
            "| Path | Profile | Parse | Status | Artifact ID | Parent Count | Findings | Disposition |",
            "| --- | --- | --- | --- | --- | ---: | --- | --- |",
        ]
    )
    for record in sorted(records, key=lambda item: item.path.as_posix()):
        findings = findings_by_path.get(record.path.as_posix(), [])
        codes = ", ".join(sorted({finding.code for finding in findings})) or "none"
        parent_ids = _string_list(record.metadata.get("parent_ids")) or []
        raw_profile = profile_map.get(record.artifact_type, {})
        disposition = raw_profile.get("disposition", "advisory-only") if isinstance(raw_profile, dict) else "advisory-only"
        row = [
            f"`{record.path.as_posix()}`",
            f"`{record.artifact_type}`",
            "error" if record.parse_error else ("valid" if record.metadata else "missing"),
            record.metadata.get("status", "—"),
            record.metadata.get("artifact_id", "—"),
            len(parent_ids),
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
            "- The report shows only bounded metadata fields, counts, and finding codes.",
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


def _changed_paths(root: pathlib.Path, explicit: Sequence[str]) -> set[str]:
    if explicit:
        return {pathlib.PurePosixPath(path).as_posix().lstrip("./") for path in explicit if path.endswith(".md")}
    changed: set[str] = set()
    for command in (
        ["git", "-C", str(root), "diff", "--name-only", "--diff-filter=ACMRT", "HEAD", "--", "*.md"],
        ["git", "-C", str(root), "ls-files", "--others", "--exclude-standard", "--", "*.md"],
    ):
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        if result.returncode == 0:
            changed.update(line.strip() for line in result.stdout.splitlines() if line.strip())
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
    parser.add_argument("--mode", choices=("report", "check-changed", "check-active"), default="report")
    parser.add_argument("--root", type=pathlib.Path, default=ROOT)
    parser.add_argument("--profiles", type=pathlib.Path, default=DEFAULT_PROFILES)
    parser.add_argument("--output", type=pathlib.Path)
    parser.add_argument("--check", action="store_true", help="compare --output without writing")
    parser.add_argument("--changed-path", action="append", default=[])
    parser.add_argument("--base-ref", default=None, help="optional Git ref for lifecycle transition comparison")
    args = parser.parse_args(argv)
    if args.check and args.output is None:
        parser.error("--check requires --output")
    root = args.root.resolve()
    try:
        profiles = load_profiles(args.profiles.resolve())
    except ProfileError as error:
        print(f"configuration-error: {error}", file=sys.stderr)
        return 2
    records = collect_records(root, profiles, base_ref=args.base_ref)
    manifest = build_manifest(records)
    findings_by_path = {
        record.path.as_posix(): validate_record(record, profiles, manifest) for record in records
    }
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

    selected_paths = (
        _changed_paths(root, args.changed_path)
        if args.mode == "check-changed"
        else {record.path.as_posix() for record in records if record.metadata.get("status") == "active"}
    )
    selected_findings = sorted(
        finding
        for path in selected_paths
        for finding in findings_by_path.get(path, [])
        if finding.severity == "error"
    )
    for finding in selected_findings:
        print(f"{finding.path}: {finding.code}: {finding.message}")
    print(
        f"metadata {args.mode}: selected={len(selected_paths)} violations={len(selected_findings)}"
    )
    return 1 if selected_findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
