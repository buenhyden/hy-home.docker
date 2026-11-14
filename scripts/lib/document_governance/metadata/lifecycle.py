"""Document lifecycle validation, snapshots, and transition evidence."""

from __future__ import annotations

import datetime
import os
import pathlib
import re
from collections.abc import Mapping, Sequence, Set

import yaml

from scripts.lib.document_governance.frontmatter import (
    FrontmatterError,
)
from scripts.lib.document_governance.frontmatter import (
    parse_frontmatter_text as _parse_frontmatter_text,
)
from scripts.lib.document_governance.frontmatter import (
    safe_load_unique as _safe_load_unique,
)
from scripts.lib.document_governance.git_provenance import (
    _GIT_OUTPUT_BYTES,
    resolve_git_provenance,
)
from scripts.lib.document_governance.git_provenance import (
    _run_git as _bounded_git,
)
from scripts.lib.document_governance.metadata.heading import _validate_template_source
from scripts.lib.document_governance.metadata.identity import (
    _decode_git_paths,
    _run_git,
    _tracked_markdown,
)
from scripts.lib.document_governance.metadata.profile import (
    TARGET_MARKDOWN_FILES,
    TARGET_MARKDOWN_PREFIXES,
    TYPED_EXAMPLE_FIXTURE_PARENT_IDS,
    TYPED_EXAMPLE_FIXTURE_PATH,
    TYPED_EXAMPLE_FIXTURE_STATUS,
    BaseSelection,
    Finding,
    Manifest,
    ProfileError,
    Record,
    TransitionOverride,
    _contains_template_placeholder,
    _finding,
    _has_parent_cycle,
    _normalized_document_values,
    _normalized_target_path,
    _profile_mapping,
    _relation_ids_for_record,
    _relation_record,
    _relation_reference_exists,
    _safe_repo_path,
    _stage00_specialization_entry,
    _string_list,
    _template_angle_tokens,
    _typed_target_types,
    _valid_iso_temporal,
    _valid_metadata_artifact_id,
    infer_artifact_type,
    registered_generated_owner,
)
from scripts.lib.document_governance.operations_catalog import (
    OperationsAuthorityError,
    read_bounded_regular,
)
from scripts.lib.document_governance.registry import (
    DocumentRegistry,
    RegistryError,
    document_type,
    preserved_origin_path,
    validate_frontmatter,
    validate_profile_values,
)
from scripts.lib.document_governance.registry import (
    classify_path as classify_registered_path,
)
from scripts.lib.document_governance.taxonomy import validate_stable_identity

# Historical Git blob origins only; never a current filesystem authority.
GOVERNANCE_RETIRED_PATHS = ("docs/00.agent-governance",)


def _expected_document_type(profile_id: str) -> str:
    """Return the Registry family/kind type, falling back to the profile id."""

    try:
        return document_type(profile_id)
    except (KeyError, RegistryError):
        return profile_id


# documentation-protocol.md: a Guide, Operations Policy or Runbook whose
# next_review_at has passed is stale until reviewed.
_CURRENCY_TYPES = frozenset(
    {"operation/guide", "operation/policy", "operation/runbook"}
)


# SDLC-06: the review date is at most this many days after `updated`, so a
# far-future date cannot keep an operations document current for good.
_REVIEW_INTERVAL_DAYS = 180


def _review_interval_exceeded(next_review: object, updated: object) -> bool:
    try:
        due = datetime.date.fromisoformat(str(next_review)[:10])
        last = datetime.date.fromisoformat(str(updated)[:10])
    except ValueError:
        return False  # absent or malformed: the date checks report it
    return (due - last).days > _REVIEW_INTERVAL_DAYS


def _retired_status_migration(
    registry: object, profile_id: str, previous: str, status: str
) -> bool:
    """D-02: a base status the profile's lifecycle no longer offers may move to
    the successor the Registry registers as a normalization."""

    if not isinstance(registry, DocumentRegistry):
        return False
    lifecycle_id = registry.profiles.get(profile_id, {}).get("lifecycle_id")
    if previous in registry.lifecycles.get(str(lifecycle_id), (previous,)):
        return False
    events = registry.common.get("task_lifecycle_events")
    migration = events.get("migration") if isinstance(events, Mapping) else None
    entries = (
        migration.get("normalizations", ()) if isinstance(migration, Mapping) else ()
    )
    return any(
        isinstance(entry, Mapping)
        and (
            entry.get("lifecycle_id"),
            entry.get("from_status"),
            entry.get("to_status"),
        )
        == (lifecycle_id, previous, status)
        for entry in entries
    )


def _review_overdue(next_review: object, reviewed: object) -> bool:
    try:
        due = datetime.date.fromisoformat(str(next_review)[:10])
    except ValueError:
        return False  # absent or malformed: invalid-next-review-at reports it
    if due >= datetime.datetime.now(datetime.UTC).date():
        return False
    try:
        return datetime.date.fromisoformat(str(reviewed)[:10]) < due
    except ValueError:
        return True


def validate_record(
    record: Record,
    profiles: dict[str, object],
    manifest: dict[str, pathlib.Path],
    transition_overrides: Mapping[tuple[str, str, str], TransitionOverride]
    | None = None,
    enforce_initial_status: bool = False,
    actual_lifecycle_transitions: Set[tuple[str, str, str]] | None = None,
    actual_lifecycle_normalizations: Set[tuple[str, str, str]] | None = None,
    actual_lifecycle_normalization_sources: Mapping[str, str] | None = None,
    unchanged_generation_statuses: Mapping[str, str] | None = None,
) -> list[Finding]:
    """Validate one record against its typed profile and the global manifest."""

    common, profile_map = _profile_mapping(profiles)
    if record.path.as_posix() in profiles.get("_delegated_reference_paths", ()):
        # The caller has already run the exact Reference content validator.
        return []
    raw_profile = profile_map.get(record.artifact_type)
    registry = profiles.get("_registry")
    profile_label = record.artifact_type
    if not isinstance(raw_profile, dict):
        return [
            _finding(
                record,
                "unknown-profile",
                f"profile is not configured: {record.artifact_type}",
            )
        ]
    typed_manifest = (
        manifest if isinstance(manifest, Manifest) else Manifest(dict(manifest), {}, {})
    )
    findings: list[Finding] = []
    if record.parse_error:
        parse_code = record.parse_error_code or "malformed-yaml"
        findings.append(
            _finding(record, f"frontmatter-{parse_code}", record.parse_error)
        )
        return findings
    template_findings = _validate_template_source(record, profiles)
    if template_findings is not None:
        return template_findings
    try:
        schema_findings = validate_frontmatter(record.metadata)
    except RegistryError:
        findings.append(
            _finding(
                record,
                "frontmatter-schema-unavailable",
                "frontmatter value schema cannot be trusted",
            )
        )
    else:
        findings.extend(
            _finding(record, finding.code, finding.message)
            for finding in schema_findings
        )
    if record.path.as_posix() == TYPED_EXAMPLE_FIXTURE_PATH:
        if record.metadata.get("status") != TYPED_EXAMPLE_FIXTURE_STATUS:
            findings.append(
                _finding(
                    record,
                    "typed-example-status-invalid",
                    "typed example fixture must remain draft and cannot be active truth",
                )
            )
        if record.metadata.get("parent_ids") != list(TYPED_EXAMPLE_FIXTURE_PARENT_IDS):
            findings.append(
                _finding(
                    record,
                    "typed-example-parent-ids-invalid",
                    "typed example fixture must use its exact domain parent pair",
                )
            )
    if record.artifact_type == "unsupported":
        findings.append(
            _finding(
                record,
                "unsupported-profile",
                "path is outside the typed document corpus",
                severity="warning",
            )
        )

    if isinstance(registry, DocumentRegistry):
        classify_registered_path(record.path.as_posix(), registry)
    uses_archive_parent_contract = record.artifact_type == "archive"
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
        _contains_template_placeholder(value, placeholder_values)
        for value in record.metadata.values()
    ):
        findings.append(
            _finding(
                record,
                "template-placeholder-in-target",
                "Stage 99 template placeholders must be replaced in instantiated documents",
            )
        )

    specialization = (
        _stage00_specialization_entry(record.path)
        if record.artifact_type == "governance"
        else None
    )
    specialization_type = (
        specialization.get("profile_id") if specialization is not None else None
    )
    if specialization_type == "governance-hook-policy":
        # Hookify owns a native metadata schema. Its exact envelope is enforced
        # by the focused governance validator, not duplicated here.
        return sorted(set(findings))

    specialization_keys = {
        key
        for key in (
            [
                *specialization.get("required_frontmatter", []),
                *specialization.get("optional_frontmatter", []),
            ]
            if specialization is not None
            else []
        )
        if isinstance(key, str)
    }
    required = set(raw_profile.get("required", []))
    optional = set(raw_profile.get("optional", []))
    if _declares_execution_items(record, common):
        # A multi-item Task derives its status from its rows (SPEC-0231).
        required.discard("status")
        if "status" in record.metadata:
            findings.append(
                _finding(
                    record,
                    "item-mode-status",
                    "multi-item Task must not declare a frontmatter status",
                )
            )
    findings.extend(
        _finding(record, item.code, f"{item.path}: {item.message}")
        for item in validate_profile_values(
            record.metadata, raw_profile, record.path.as_posix()
        )
    )
    global_forbidden = set(common.get("globally_forbidden", []))
    # `globally_forbidden` named three retired keys but was read only to pick a
    # finding code inside a loop no profile could enter, because no profile
    # declares `forbidden`. The whitelist below rejected the keys anyway, as
    # undeclared rather than as deliberately retired. Unioning them here makes
    # the declared contract the thing that decides, and restores the distinct
    # code that tells an author the key was removed on purpose.
    forbidden = (
        set(raw_profile.get("forbidden", [])) | global_forbidden
    ) - specialization_keys
    registered_owner = registered_generated_owner(record.path, profiles)
    for key in sorted(required):
        if key not in record.metadata or record.metadata[key] in (None, ""):
            if (
                key == "generated_by"
                and record.artifact_type == "generated"
                and registered_owner
            ):
                continue
            findings.append(
                _finding(
                    record, "missing-required-key", f"required key is missing: {key}"
                )
            )
    for key in sorted(record.metadata):
        if key not in forbidden:
            continue
        if key in global_forbidden:
            findings.append(
                _finding(
                    record,
                    "forbidden-key",
                    f"key is forbidden repository-wide: {key}",
                )
            )
            continue
        findings.append(
            _finding(
                record,
                "type-inappropriate-key",
                f"key is forbidden for {profile_label}: {key}",
            )
        )

    status = record.metadata.get("status")
    allowed_statuses = raw_profile.get("allowed_statuses", [])
    if status is not None:
        if not isinstance(status, str) or status not in allowed_statuses:
            findings.append(
                _finding(
                    record,
                    "invalid-status",
                    f"status is not allowed for {profile_label}",
                )
            )
        if status == "archived" and record.artifact_type != "archive":
            findings.append(
                _finding(
                    record,
                    "archived-outside-stage-98",
                    "archived status is reserved for archive tombstones",
                )
            )
    generation_status = (unchanged_generation_statuses or {}).get(
        record.path.as_posix()
    )
    previous_status = (
        generation_status if generation_status == status else record.previous_status
    )
    initial_status = raw_profile.get("initial_status")
    transitions = raw_profile.get("transitions", common.get("transitions", {}))
    initial_transition_evidence = (
        (
            (record.path.as_posix(), initial_status, status)
            in (transition_overrides or {})
            and isinstance(transitions, dict)
            and status in transitions.get(initial_status, ())
        )
        if isinstance(initial_status, str) and isinstance(status, str)
        else False
    )
    initial_actual_transition = (
        (record.path.as_posix(), initial_status, status)
        in (actual_lifecycle_transitions or ())
        if isinstance(initial_status, str) and isinstance(status, str)
        else False
    )
    normalization_source = (actual_lifecycle_normalization_sources or {}).get(
        record.path.as_posix()
    )
    initial_actual_normalization = isinstance(normalization_source, str) and (
        record.path.as_posix(),
        normalization_source,
        status,
    ) in (actual_lifecycle_normalizations or ())
    actual_normalization_transition = any(
        path == record.path.as_posix()
        and source == normalization_source
        and transition_path == path
        and transition_source == bridge
        and target == status
        for path, source, bridge in (actual_lifecycle_normalizations or ())
        for transition_path, transition_source, target in (
            actual_lifecycle_transitions or ()
        )
    )
    if (
        enforce_initial_status
        and isinstance(status, str)
        and previous_status is None
        and isinstance(initial_status, str)
        and status != initial_status
        and not initial_transition_evidence
        and not initial_actual_transition
        and not initial_actual_normalization
        and not actual_normalization_transition
    ):
        findings.append(
            _finding(
                record,
                "invalid-initial-status",
                f"new {profile_label} documents must start at {initial_status}",
            )
        )
    if isinstance(status, str) and previous_status and status != previous_status:
        allowed_next = (
            transitions.get(previous_status, [])
            if isinstance(transitions, dict)
            else []
        )
        override_key = (record.path.as_posix(), previous_status, status)
        if (
            status not in allowed_next
            and override_key not in (transition_overrides or {})
            and override_key not in (actual_lifecycle_transitions or ())
            and override_key not in (actual_lifecycle_normalizations or ())
            and not actual_normalization_transition
            and not _retired_status_migration(
                registry, record.artifact_type, previous_status, status
            )
        ):
            findings.append(
                _finding(
                    record,
                    "invalid-transition",
                    f"lifecycle transition requires explicit override: {previous_status} -> {status}",
                )
            )

    artifact_id = record.metadata.get("artifact_id")
    if artifact_id is not None and not _valid_metadata_artifact_id(artifact_id):
        findings.append(
            _finding(
                record, "invalid-artifact-id", "artifact_id must be a non-empty string"
            )
        )
    if (
        isinstance(artifact_id, str)
        and artifact_id.strip() in typed_manifest.duplicates
    ):
        paths = ", ".join(
            path.as_posix() for path in typed_manifest.duplicates[artifact_id.strip()]
        )
        findings.append(
            _finding(record, "duplicate-artifact-id", f"artifact_id occurs at: {paths}")
        )

    declared_type = record.metadata.get("type")
    expected_profile = (
        specialization_type
        if isinstance(specialization_type, str)
        else record.artifact_type
    )
    expected_type = _expected_document_type(expected_profile)
    if declared_type is not None:
        if not isinstance(declared_type, str) or declared_type != expected_type:
            findings.append(
                _finding(
                    record,
                    "type-mismatch",
                    f"declared type does not match inferred profile {record.artifact_type}",
                )
            )

    if (
        isinstance(declared_type, str)
        and declared_type == _expected_document_type(record.artifact_type)
        and (
            (
                isinstance(raw_profile.get("id_pattern"), str)
                and isinstance(raw_profile.get("path_identity"), str)
            )
            or (
                "artifact_id_pattern" in raw_profile
                and isinstance(raw_profile.get("identity_relation"), str)
            )
        )
    ):
        identity_profiles = (
            {record.artifact_type: raw_profile}
            if record.artifact_type == "archive"
            else profile_map
        )
        for taxonomy_finding in validate_stable_identity(
            pathlib.PurePosixPath(record.path.as_posix()),
            record.metadata,
            identity_profiles,
            profile_id=record.artifact_type,
        ):
            findings.append(
                _finding(
                    record,
                    taxonomy_finding.code,
                    taxonomy_finding.message,
                )
            )

    parent_value = record.metadata.get("parent_ids")
    parent_ids = _string_list(parent_value) if parent_value is not None else None
    if parent_value is not None and parent_ids is None:
        findings.append(
            _finding(
                record,
                "invalid-parent-ids",
                "parent_ids must be a list of non-empty strings",
            )
        )
    if parent_ids is not None:
        if len(parent_ids) != len(set(parent_ids)):
            findings.append(
                _finding(
                    record, "duplicate-parent", "parent_ids contains duplicate IDs"
                )
            )
        parent_count = None
        if isinstance(registry, DocumentRegistry):
            registered_profile = registry.profiles.get(record.artifact_type)
            traceability = (
                registered_profile.get("traceability")
                if isinstance(registered_profile, Mapping)
                else None
            )
            if isinstance(traceability, Mapping):
                parent_count = traceability.get("parent_count")
        if isinstance(parent_count, int) and len(parent_ids) != parent_count:
            findings.append(
                _finding(
                    record,
                    "parent-cardinality",
                    f"parent_ids must contain exactly {parent_count} entries",
                )
            )
        root_exceptions = common.get("root_exceptions", {})
        root_permitted = raw_profile.get("allow_empty_parents", False) or (
            isinstance(root_exceptions, dict)
            and record.path.as_posix() in root_exceptions
        )
        if not parent_ids and not root_permitted:
            findings.append(
                _finding(
                    record,
                    "missing-parent",
                    "this artifact profile does not permit a root",
                )
            )
        parent_type_order = raw_profile.get("allowed_parent_types", [])
        allowed_parent_types = set(parent_type_order)
        relation_ids = _relation_ids_for_record(record)
        for parent_id in parent_ids:
            if parent_id in relation_ids:
                findings.append(
                    _finding(
                        record,
                        "self-parent",
                        f"artifact references itself as parent: {parent_id}",
                    )
                )
                continue
            parent_record = _relation_record(typed_manifest, parent_id, record)
            if parent_id in typed_manifest.relation_conflicts:
                findings.append(
                    _finding(
                        record,
                        "ambiguous-relation-reference",
                        f"parent relation resolves to multiple records: {parent_id}",
                    )
                )
            elif not _relation_reference_exists(typed_manifest, parent_id, record):
                findings.append(
                    _finding(
                        record,
                        "unresolved-parent",
                        f"parent artifact_id is unresolved: {parent_id}",
                    )
                )
            elif parent_record and allowed_parent_types:
                parent_type = parent_record.artifact_type
                # A preserved parent kept its identity and its type; only its
                # location changed. Read the type back from the path it was
                # moved from, so preservation never invalidates a live child.
                origin = preserved_origin_path(parent_record.path.as_posix())
                if origin is not None and isinstance(registry, DocumentRegistry):
                    original_type = classify_registered_path(origin, registry)
                    if original_type is not None:
                        parent_type = original_type
                if (
                    uses_archive_parent_contract
                    and parent_type == "requirements-package"
                ):
                    parent_type = "prd"
                if parent_type in allowed_parent_types:
                    continue
                findings.append(
                    _finding(
                        record,
                        "invalid-parent-type",
                        f"parent type {parent_record.artifact_type} is not allowed: {parent_id}",
                    )
                )
        if (
            len(parent_ids) == len(set(parent_ids))
            and not any(
                parent_id in typed_manifest.duplicates
                or parent_id in typed_manifest.relation_conflicts
                for parent_id in parent_ids
            )
            and isinstance(parent_type_order, list)
        ):
            type_precedence = {
                parent_type: index
                for index, parent_type in enumerate(parent_type_order)
            }
            resolved_parents = [
                _relation_record(typed_manifest, parent_id, record)
                for parent_id in parent_ids
            ]
            if all(
                parent_record is not None
                and parent_record.artifact_type in type_precedence
                for parent_record in resolved_parents
            ):
                expected_parent_ids = sorted(
                    parent_ids,
                    key=lambda parent_id: (
                        type_precedence[
                            _relation_record(
                                typed_manifest, parent_id, record
                            ).artifact_type  # type: ignore[union-attr]
                        ],
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
            findings.append(
                _finding(record, "parent-cycle", "parent_ids creates a cycle")
            )

    supersedes_value = record.metadata.get("supersedes")
    if supersedes_value is not None:
        supersedes = _string_list(supersedes_value)
        if supersedes is None:
            findings.append(
                _finding(
                    record,
                    "invalid-supersedes",
                    "supersedes must be a list of non-empty strings",
                )
            )
        else:
            relation_ids = _relation_ids_for_record(record)
            for replaced_id in supersedes:
                if replaced_id in relation_ids:
                    findings.append(
                        _finding(
                            record,
                            "self-supersession",
                            f"artifact supersedes itself: {replaced_id}",
                        )
                    )
                elif replaced_id in typed_manifest.relation_conflicts:
                    findings.append(
                        _finding(
                            record,
                            "ambiguous-relation-reference",
                            f"supersedes relation resolves to multiple records: {replaced_id}",
                        )
                    )
                elif not _relation_reference_exists(
                    typed_manifest, replaced_id, record
                ):
                    findings.append(
                        _finding(
                            record,
                            "unresolved-supersedes",
                            f"superseded artifact_id is unresolved: {replaced_id}",
                        )
                    )
                else:
                    replaced_record = _relation_record(
                        typed_manifest, replaced_id, record
                    )
                    if (
                        replaced_record
                        and replaced_record.metadata.get("status") != "superseded"
                    ):
                        findings.append(
                            _finding(
                                record,
                                "invalid-supersession-state",
                                f"superseded target is not in superseded status: {replaced_id}",
                            )
                        )

    if status == "superseded" and "artifact_id" in required:
        replacement_ids: set[str] = set()
        for candidate in typed_manifest.relation_records_by_id.values():
            candidate_relation_ids = _relation_ids_for_record(candidate)
            for replaced_id in _string_list(candidate.metadata.get("supersedes")) or []:
                if (
                    replaced_id not in candidate_relation_ids
                    and replaced_id not in typed_manifest.relation_conflicts
                    and _relation_reference_exists(
                        typed_manifest, replaced_id, candidate
                    )
                ):
                    replacement_ids.add(replaced_id)
        relation_ids = _relation_ids_for_record(record)
        if not relation_ids.intersection(replacement_ids):
            findings.append(
                _finding(
                    record,
                    "replacement-free-supersession",
                    "superseded artifact has no resolvable replacement relation",
                )
            )

    reviewed_at = record.metadata.get("reviewed_at")
    successor = record.metadata.get("superseded_by")
    if successor is not None and (
        not isinstance(successor, str)
        or not _relation_reference_exists(typed_manifest, successor, record)
    ):
        findings.append(
            _finding(
                record,
                "unresolved-superseded-by",
                "superseded_by must resolve to current or verified retired lineage",
            )
        )
    if (
        status == "active"
        and record.metadata.get("type") in _CURRENCY_TYPES
        and _review_overdue(record.metadata.get("next_review_at"), reviewed_at)
    ):
        findings.append(
            _finding(
                record,
                "stale-active",
                "next_review_at has passed without a reviewed_at on or after it",
            )
        )
    if record.metadata.get("type") in _CURRENCY_TYPES and _review_interval_exceeded(
        record.metadata.get("next_review_at"), record.metadata.get("updated")
    ):
        findings.append(
            _finding(
                record,
                "review-interval-exceeded",
                f"next_review_at is more than {_REVIEW_INTERVAL_DAYS} days after updated",
            )
        )
    temporal_fields = (
        "created",
        "updated",
        "observed_at",
        "completed_at",
        "reviewed_at",
        "next_review_at",
        "occurred_at",
        "resolved_at",
    )
    for temporal_field in temporal_fields:
        temporal_value = record.metadata.get(temporal_field)
        if temporal_value is not None and not _valid_iso_temporal(temporal_value):
            findings.append(
                _finding(
                    record,
                    f"invalid-{temporal_field.replace('_', '-')}",
                    f"{temporal_field} must be a strict ISO date or timezone-aware date-time",
                )
            )
    generated_by = record.metadata.get("generated_by")
    if generated_by is not None and not _safe_repo_path(generated_by, "scripts/"):
        findings.append(
            _finding(
                record,
                "invalid-generator",
                "generated_by must be a safe canonical scripts/ repository path",
            )
        )
    elif (
        registered_owner is not None
        and generated_by is not None
        and generated_by != registered_owner
    ):
        findings.append(
            _finding(
                record,
                "generated-owner-mismatch",
                "generated_by differs from the exact registered generator owner",
            )
        )

    if not raw_profile.get("allow_additional", False):
        known = required | optional | forbidden | specialization_keys
        for key in sorted(set(record.metadata) - known):
            findings.append(
                _finding(
                    record,
                    "type-inappropriate-key",
                    f"key is not declared for {profile_label}: {key}",
                )
            )
    return sorted(set(findings))


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
    lines = _git_lines(
        root, ["rev-parse", "--verify", "--end-of-options", f"{ref}^{{commit}}"]
    )
    return (
        lines[0]
        if len(lines) == 1 and re.fullmatch(r"[0-9a-fA-F]{40,64}", lines[0])
        else None
    )


def resolve_base_selection(
    root: pathlib.Path, explicit_ref: str | None
) -> BaseSelection:
    """Resolve a safe comparison base without ever falling back to the full corpus."""

    if explicit_ref:
        commit = _verified_commit(root, explicit_ref)
        if commit is None:
            raise ProfileError(f"explicit --base-ref is not a commit: {explicit_ref}")
        merge_base = _git_lines(root, ["merge-base", "HEAD", commit])
        if not merge_base:
            raise ProfileError(
                f"explicit --base-ref has no merge base with HEAD: {explicit_ref}"
            )
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


def _metadata_at_ref(
    root: pathlib.Path,
    path: pathlib.Path,
    base_ref: str | None,
    profiles: Mapping[str, object] | None = None,
) -> dict[str, object] | None:
    if not base_ref:
        return None
    if not resolve_git_provenance(path, base_ref, repo_root=root).is_regular_blob:
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
        return _normalized_document_values(
            path, _parse_frontmatter_text(result.stdout), profiles
        )
    except (FrontmatterError, RegistryError):
        return None


def _text_at_ref(
    root: pathlib.Path, path: pathlib.Path, base_ref: str | None
) -> str | None:
    if not base_ref:
        return None
    if not resolve_git_provenance(path, base_ref, repo_root=root).is_regular_blob:
        return None
    result = _run_git(
        root,
        ["show", f"{base_ref}:{path.as_posix()}"],
        operation="prior body-contract discovery",
        text=True,
    )
    return result.stdout if result.returncode == 0 else None


def _governance_moved_body_baseline(
    root: pathlib.Path,
    target: pathlib.Path,
    profiles: Mapping[str, object],
    base_ref: str | None,
) -> tuple[Record | None, str | None]:
    """Recover the former governance home only from a verified historical blob.

    This is a historical path translation, never a current loading alias. The
    Registry still selects the destination; both records must retain its type
    and identity before the source can establish status or body-deficit history.
    """

    registry = profiles.get("_registry")
    if not isinstance(registry, DocumentRegistry) or not base_ref:
        return None, None
    profile_id = classify_registered_path(target.as_posix(), registry)
    origins = {
        "governance-policy": f"policies/{target.name}",
        "governance-hook-policy": f"policies/hooks/{target.name}",
        "governance-role": f"roles/{target.name}",
        "governance-skill": f"skills/{target.parent.name}.md",
        "governance-provider": f"providers/{target.parent.name.removeprefix('.')}.md",
        "governance-provider-index": "providers/README.md",
        "governance-sdlc": "sdlc.md",
    }
    origin = (
        "README.md"
        if target.as_posix() in {".agents/README.md", ".agents/evaluations/README.md"}
        else origins.get(profile_id)
    )
    if origin is None or profile_id is None:
        return None, None
    source = (
        pathlib.Path("evals/README.md")
        if target.as_posix() == ".agents/evaluations/README.md"
        else pathlib.Path(GOVERNANCE_RETIRED_PATHS[0]) / origin
    )
    text = _text_at_ref(root, source, base_ref)
    if text is None:
        return None, None
    try:
        previous = _parse_frontmatter_text(text)
        current = _normalized_document_values(
            target,
            _parse_frontmatter_text(read_bounded_regular(root, target).decode("utf-8")),
            profiles,
        )
    except (
        FrontmatterError,
        RegistryError,
        OperationsAuthorityError,
        UnicodeError,
        OSError,
    ):
        return None, None
    if previous.get("type") != registry.profiles[profile_id].get("type") or any(
        previous.get(key) != current.get(key)
        for key in ("type", "artifact_id", "function_id", "agent_id")
    ):
        return None, None
    return Record(target, previous, profile_id, frontmatter_present=True), text


# ADR-0057 moved every Operations member out of the domain catalog.
_OPERATIONS_ROLE_PROFILES = frozenset({"guide", "policy", "runbook"})
_RETIRED_OPERATIONS_CATALOG = "docs/05.operations/catalog/"  # retired-route-record


def _operations_moved_body_baseline(
    root: pathlib.Path,
    target: pathlib.Path,
    profiles: Mapping[str, object],
    base_records: Sequence[Record],
    base_ref: str | None,
) -> tuple[Record | None, str | None]:
    """Recover an Operations member's moved predecessor from a verified blob.

    This is a historical path translation, never a current loading alias. The
    catalog move kept the slug and identity; numbered family moves keep the
    exact basename, role and identity. Only one matching base record may supply
    the inherited status and body.
    """

    registry = profiles.get("_registry")
    if not isinstance(registry, DocumentRegistry) or not base_ref:
        return None, None
    profile_id = classify_registered_path(target.as_posix(), registry)
    if profile_id not in _OPERATIONS_ROLE_PROFILES:
        return None, None
    try:
        current = _parse_frontmatter_text(
            read_bounded_regular(root, target).decode("utf-8")
        )
    except (
        FrontmatterError,
        OperationsAuthorityError,
        UnicodeError,
        OSError,
    ):
        return None, None
    # The catalog subject folder is `####-<slug>` under `NN-<domain>`; the move
    # kept the slug or, for a generic slug, prefixed its domain word. A reused
    # identifier under any other slug is a new document, not a predecessor.
    slug = target.stem.split("-", 1)[-1]
    family_predecessors = (
        {
            target.parent.parent / target.name,
            target.parent.parent / target.parent.name[3:] / target.name,
        }
        if len(target.parts) == 5
        else set()
    )
    matches = [
        record
        for record in base_records
        if (
            record.path in family_predecessors
            # A move between numbered families of the same role (SPEC-0262).
            or (
                len(target.parts) == 5
                and record.path != target
                and record.path.name == target.name
                and record.path.parent.parent == target.parent.parent
                and re.fullmatch(r"[0-9]{2}-[a-z0-9-]+", record.path.parent.name)
                is not None
            )
            or (
                record.path.as_posix().startswith(_RETIRED_OPERATIONS_CATALOG)
                and slug
                in {
                    (subject := record.path.parent.name.split("-", 1)[-1]),
                    f"{record.path.parent.parent.name.split('-', 1)[-1]}-{subject}",
                }
            )
        )
        and record.metadata.get("type") == current.get("type")
        and record.metadata.get("artifact_id") == current.get("artifact_id")
    ]
    if len(matches) != 1 or not isinstance(current.get("artifact_id"), str):
        return None, None
    text = _text_at_ref(root, matches[0].path, base_ref)
    if text is None:
        return None, None
    try:
        previous = _parse_frontmatter_text(text)
    except FrontmatterError:
        return None, None
    return Record(target, previous, profile_id, frontmatter_present=True), text


def _previous_status(
    root: pathlib.Path,
    path: pathlib.Path,
    base_ref: str | None,
    profiles: Mapping[str, object] | None = None,
) -> str | None:
    loaded = _metadata_at_ref(root, path, base_ref, profiles)
    return (
        loaded.get("status")
        if isinstance(loaded, dict) and isinstance(loaded.get("status"), str)
        else None
    )


def _record_from_text(
    relative_path: pathlib.Path,
    text: str,
    previous_status: str | None = None,
    profiles: Mapping[str, object] | None = None,
) -> Record:
    lines = text.splitlines()
    frontmatter_present = bool(lines and lines[0].strip() == "---")
    try:
        values = _normalized_document_values(
            relative_path, _parse_frontmatter_text(text), profiles
        )
        parse_error = None
        parse_error_code = None
    except FrontmatterError as error:
        values = {}
        parse_error = str(error)
        parse_error_code = error.code
    except RegistryError as error:
        values = {}
        parse_error = str(error)
        parse_error_code = "native-skill-envelope-invalid"
    inferred_type = infer_artifact_type(relative_path, profiles)
    registry = profiles.get("_registry") if isinstance(profiles, Mapping) else None
    registered_package_readme = bool(
        inferred_type in {"data", "audit", "research"}
        and isinstance(registry, DocumentRegistry)
        and classify_registered_path(relative_path.as_posix(), registry)
        == inferred_type
    )
    # Only an exact Registry-classified Data package README retains Data
    # ownership; generated_by is provenance there. Every other generated
    # Markdown artifact, including README envelopes, keeps the generated
    # classification used before the Stage 90 transition.
    artifact_type = (
        "generated"
        if "generated_by" in values and not registered_package_readme
        else inferred_type
    )
    return Record(
        relative_path,
        values,
        artifact_type,
        previous_status=previous_status,
        parse_error=parse_error,
        parse_error_code=parse_error_code,
        frontmatter_present=frontmatter_present,
    )


def _read_markdown_texts_at_ref(
    root: pathlib.Path, paths: Sequence[str], ref: str
) -> dict[str, str]:
    """Read exact regular blobs with bounded batches; omit missing paths."""
    if not paths:
        return {}
    selected = set(paths)
    listed = _run_git(
        root,
        ["ls-tree", "-r", "-l", "-z", ref, "--", *sorted(selected)],
        operation="historical Markdown blob discovery",
    )
    if listed.returncode != 0:
        raise ProfileError("cannot enumerate historical Markdown blobs")
    entries: list[tuple[str, str, int]] = []
    for raw in filter(None, listed.stdout.split(b"\0")):
        try:
            header, raw_path = raw.split(b"\t", 1)
            mode, kind, oid, raw_size = header.decode("ascii").split()
            path = raw_path.decode("utf-8")
            size = int(raw_size)
        except (ValueError, UnicodeError) as error:
            raise ProfileError("malformed historical Markdown tree entry") from error
        if (
            path not in selected
            or mode not in {"100644", "100755"}
            or kind != "blob"
            or re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", oid) is None
            or size < 0
            or any(entry[0] == path for entry in entries)
        ):
            raise ProfileError(
                "historical Markdown entry must be an exact regular blob"
            )
        entries.append((path, oid, size))
    texts: dict[str, str] = {}
    pending = entries
    while pending:
        batch: list[tuple[str, str, int]] = []
        output_bytes = 0
        for entry in pending:
            _, oid, size = entry
            frame_bytes = len(oid) + len(str(size)) + size + 8
            if output_bytes + frame_bytes > _GIT_OUTPUT_BYTES:
                break
            batch.append(entry)
            output_bytes += frame_bytes
        if not batch:
            # Preserve the existing individual-read behavior for oversized documents.
            path, oid, _ = pending[0]
            shown = _run_git(
                root,
                ["cat-file", "blob", oid],
                operation="large historical Markdown read",
                text=True,
            )
            if shown.returncode != 0:
                raise ProfileError(f"cannot read historical Markdown record: {path}")
            texts[path] = shown.stdout
            pending = pending[1:]
            continue
        shown = _bounded_git(
            root,
            ["cat-file", "--batch"],
            input_bytes=("\n".join(oid for _, oid, _ in batch) + "\n").encode("ascii"),
        )
        if shown.returncode != 0:
            raise ProfileError("bounded historical Markdown batch failed")
        cursor = 0
        for path, oid, size in batch:
            end = shown.stdout.find(b"\n", cursor)
            expected = f"{oid} blob {size}".encode("ascii")
            if end < 0 or shown.stdout[cursor:end] != expected:
                raise ProfileError(
                    "historical Markdown batch has a missing or malformed blob"
                )
            cursor = end + 1
            payload = shown.stdout[cursor : cursor + size]
            cursor += size
            if len(payload) != size or shown.stdout[cursor : cursor + 1] != b"\n":
                raise ProfileError("historical Markdown batch payload is truncated")
            try:
                texts[path] = payload.decode("utf-8")
            except UnicodeError as error:
                raise ProfileError("historical Markdown blob is not UTF-8") from error
            cursor += 1
        if cursor != len(shown.stdout):
            raise ProfileError(
                "historical Markdown batch has unexpected trailing bytes"
            )
        pending = pending[len(batch) :]
    return texts


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
        [
            "ls-tree",
            "-r",
            "-z",
            "--name-only",
            base_ref,
            "--",
            "docs",
            "archive",
            "infra",
            ".agents",
            ".claude/provider.md",
            ".codex/provider.md",
        ],
        operation="base Markdown discovery",
    )
    if result.returncode != 0:
        raise ProfileError(f"cannot enumerate Markdown records at base ref: {base_ref}")
    paths = sorted(
        {
            path
            for path in _decode_git_paths(result.stdout, "base Markdown discovery")
            if path.as_posix().endswith(".md")
            and (
                path.as_posix() in TARGET_MARKDOWN_FILES
                or path.as_posix().startswith(TARGET_MARKDOWN_PREFIXES)
                or (path.as_posix().startswith("infra/") and path.name == "README.md")
            )
            and path.as_posix() not in excluded
        },
        key=lambda path: path.as_posix(),
    )
    texts = _read_markdown_texts_at_ref(
        root, [path.as_posix() for path in paths], base_ref
    )
    records: list[Record] = []
    for relative_path in paths:
        if relative_path.as_posix() not in texts:
            raise ProfileError(
                f"cannot read base Markdown record: {relative_path.as_posix()}"
            )
        records.append(
            _record_from_text(
                relative_path, texts[relative_path.as_posix()], profiles=profiles
            )
        )
    return records


def collect_selected_records_at_ref(
    root: pathlib.Path,
    profiles: dict[str, object],
    selected_paths: Sequence[str],
    ref: str,
) -> dict[str, Record]:
    """Collect selected records that exist at a ref without scanning its full corpus."""

    paths = sorted(
        {
            path.as_posix()
            for value in selected_paths
            if (path := _normalized_target_path(value)) is not None
        }
    )
    texts = _read_markdown_texts_at_ref(root, paths, ref)
    return {
        path: _record_from_text(pathlib.Path(path), text, profiles=profiles)
        for path, text in texts.items()
    }


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
            text = read_bounded_regular(
                root, relative_path, max_bytes=4 * 1024 * 1024
            ).decode("utf-8")
        except (OSError, UnicodeError, OperationsAuthorityError) as error:
            records.append(
                Record(
                    relative_path,
                    {},
                    infer_artifact_type(relative_path, profiles),
                    parse_error=f"cannot read UTF-8 Markdown: {error}",
                    parse_error_code="malformed-yaml",
                )
            )
            continue
        previous_record = (previous_records or {}).get(relative_path.as_posix())
        previous_status = (
            previous_record.metadata.get("status")
            if previous_record
            and isinstance(previous_record.metadata.get("status"), str)
            else _previous_status(root, relative_path, base_ref, profiles)
        )
        records.append(
            _record_from_text(
                relative_path,
                text,
                previous_status=previous_status,
                profiles=profiles,
            )
        )
    return records


CO_LOCATED_TASK_PATH = re.compile(
    r"docs/03\.specs/[0-9]{4}-[a-z0-9]([a-z0-9-]*[a-z0-9])?"
    r"/tasks/tsk-[0-9]{4}-[a-z0-9]([a-z0-9-]*[a-z0-9])?\.md"
)


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
        raise ProfileError(
            "transition override file must contain only transition_overrides"
        )
    rows = loaded.get("transition_overrides")
    if not isinstance(rows, list) or not rows:
        raise ProfileError("transition_overrides must be a non-empty list")
    common, _ = _profile_mapping(profiles)
    # `allowed_statuses` is a legacy-profile field. Registry-built profiles, the
    # ones the CLI uses, do not carry it, so reading only that key left the set
    # empty and rejected every override as "an unknown lifecycle status". The
    # registry's lifecycles are where statuses live now.
    registry = profiles.get("_registry")
    allowed_statuses = set(common.get("allowed_statuses", []))
    if isinstance(registry, DocumentRegistry):
        allowed_statuses |= {
            status for statuses in registry.lifecycles.values() for status in statuses
        }
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
            raise ProfileError(
                f"transition override row {index} must define the exact evidence fields"
            )
        if not all(
            isinstance(row[key], str) and row[key].strip() for key in expected_keys
        ):
            raise ProfileError(
                f"transition override row {index} values must be non-empty strings"
            )
        target = _normalized_target_path(row["path"])
        evidence = _normalized_target_path(row["evidence_task"])
        if target is None or not (root / target).is_file():
            raise ProfileError(
                f"transition override row {index} target path is not an existing canonical document"
            )
        # The co-located Task form Stage 03 actually uses. The retired
        # `docs/03.specs/spec-<slug>/task.md` shape has zero documents in this
        # repository against fifteen in this one, so requiring it made every
        # override unsatisfiable while the message below already named the
        # correct form.
        if (
            evidence is None
            or not CO_LOCATED_TASK_PATH.fullmatch(evidence.as_posix())
            or not (root / evidence).is_file()
        ):
            raise ProfileError(
                f"transition override row {index} evidence_task must be an existing co-located Task"
            )
        previous_status = row["previous_status"].strip()
        new_status = row["new_status"].strip()
        if (
            previous_status not in allowed_statuses
            or new_status not in allowed_statuses
        ):
            raise ProfileError(
                f"transition override row {index} uses an unknown lifecycle status"
            )
        if previous_status == new_status:
            raise ProfileError(
                f"transition override row {index} does not describe a transition"
            )
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
            raise ProfileError(
                f"duplicate transition override scope: {' -> '.join(key)}"
            )
        overrides[key] = override
    return overrides


def _declares_execution_items(record: Record, common: Mapping[str, object]) -> bool:
    contract = common.get("execution_items")
    if (
        record.artifact_type != "task"
        or common.get("lifecycle_generation", 0) < 6
        or not isinstance(contract, Mapping)
    ):
        return False
    header = "| " + " | ".join(contract.get("table_headers", ())) + " |"
    subsection = str(contract.get("subsection"))
    markers = {"### " + subsection, "#### " + subsection}
    try:
        lines = pathlib.Path(record.path).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return False
    lines = lines.splitlines()
    return header in lines and any(marker in lines for marker in markers)
