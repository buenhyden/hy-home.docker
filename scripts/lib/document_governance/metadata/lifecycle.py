"""Document lifecycle validation, snapshots, and transition evidence."""

from __future__ import annotations

import os
import pathlib
import re
from collections.abc import Mapping, Sequence

import yaml

from scripts.lib.document_governance.frontmatter import (
    FrontmatterError,
    parse_frontmatter_text as _parse_frontmatter_text,
    safe_load_unique as _safe_load_unique,
)
from scripts.lib.document_governance.git_provenance import resolve_git_provenance
from scripts.lib.document_governance.registry import (
    DocumentRegistry,
    RegistryError,
    classify_path as classify_registered_path,
    document_type,
)
from scripts.lib.document_governance.taxonomy import validate_stable_identity
from scripts.lib.document_governance.metadata.heading import _validate_template_source
from scripts.lib.document_governance.metadata.identity import (
    _decode_git_paths,
    _run_git,
    _tracked_markdown,
)
from scripts.lib.document_governance.metadata.profile import (
    APPROVED_MIGRATION_PATHS,
    EXPECTED_ARCHIVE_DISPOSITIONS,
    EXPECTED_PRESERVATION_CLASSES,
    EXPECTED_SNAPSHOT_ARCHIVE_DISPOSITIONS,
    LEGACY_EXCEPTION_CODES,
    MIGRATION_TYPED_KEYS,
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
    _condition_members,
    _contains_template_placeholder,
    _finding,
    _has_parent_cycle,
    _normalized_target_path,
    _profile_mapping,
    _relation_ids_for_record,
    _relation_record,
    _relation_reference_exists,
    _safe_repo_path,
    _safe_snapshot_path,
    _stage00_specialization_entry,
    _string_list,
    _template_angle_tokens,
    _typed_target_types,
    _valid_iso_temporal,
    _valid_lowercase_object_id,
    _valid_lowercase_sha256,
    _valid_metadata_artifact_id,
    infer_artifact_type,
    registered_generated_owner,
)

def _expected_document_type(profile_id: str) -> str:
    """Return the Registry family/kind type, falling back to the profile id."""

    try:
        return document_type(profile_id)
    except (KeyError, RegistryError):
        return profile_id


def validate_record(
    record: Record,
    profiles: dict[str, object],
    manifest: dict[str, pathlib.Path],
    transition_overrides: Mapping[tuple[str, str, str], TransitionOverride] | None = None,
    migration_compaction_witness: Record | None = None,
) -> list[Finding]:
    """Validate one record against its typed profile and the global manifest."""

    common, profile_map = _profile_mapping(profiles)
    if record.path.as_posix() in profiles.get("_delegated_reference_paths", ()):
        # The caller has already run the exact Reference content validator.
        return []
    raw_profile = profile_map.get(record.artifact_type)
    registry = profiles.get("_registry")
    legacy_map = profiles.get("_legacy_profiles")
    if (
        isinstance(registry, DocumentRegistry)
        and classify_registered_path(record.path.as_posix(), registry) is None
        and isinstance(legacy_map, Mapping)
    ):
        legacy_profile = legacy_map.get(record.artifact_type)
        if isinstance(legacy_profile, dict):
            raw_profile = legacy_profile
    profile_label = record.artifact_type
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
    if record.path.as_posix() == TYPED_EXAMPLE_FIXTURE_PATH:
        if record.metadata.get("status") != TYPED_EXAMPLE_FIXTURE_STATUS:
            findings.append(
                _finding(
                    record,
                    "typed-example-status-invalid",
                    "typed example fixture must remain draft and cannot be active truth",
                )
            )
        if record.metadata.get("parent_ids") != list(
            TYPED_EXAMPLE_FIXTURE_PARENT_IDS
        ):
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

    registry_classification = (
        classify_registered_path(record.path.as_posix(), registry)
        if isinstance(registry, DocumentRegistry)
        else None
    )
    uses_legacy_parent_contract = record.artifact_type == "archive" or (
        isinstance(registry, DocumentRegistry)
        and registry_classification is None
        and isinstance(legacy_map, Mapping)
        and isinstance(legacy_map.get(record.artifact_type), dict)
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
        # by the focused Stage 00 validator, not duplicated here.
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
            if key == "generated_by" and record.artifact_type == "generated" and registered_owner:
                continue
            findings.append(_finding(record, "missing-required-key", f"required key is missing: {key}"))
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
                _finding(record, "invalid-status", f"status is not allowed for {profile_label}")
            )
        if status == "archived" and record.artifact_type != "archive":
            findings.append(
                _finding(record, "archived-outside-stage-98", "archived status is reserved for archive tombstones")
            )
    previous_status = record.previous_status
    if isinstance(status, str) and previous_status and status != previous_status:
        transitions = raw_profile.get("transitions", common.get("transitions", {}))
        allowed_next = transitions.get(previous_status, []) if isinstance(transitions, dict) else []
        # A previous status the lifecycle never defined is not a state this
        # document can transition out of, so moving to a defined status repairs
        # it rather than transitioning. Demanding an override for a repair
        # makes an invalid status cheaper to keep than to correct, and the
        # override is not reachable in this repository anyway.
        defined_statuses = set(transitions) if isinstance(transitions, dict) else set()
        repairs_undefined_previous = bool(defined_statuses) and (
            previous_status not in defined_statuses and status in defined_statuses
        )
        override_key = (record.path.as_posix(), previous_status, status)
        if (
            status not in allowed_next
            and not repairs_undefined_previous
            and override_key not in (transition_overrides or {})
            and record != migration_compaction_witness
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
        findings.append(_finding(record, "invalid-artifact-id", "artifact_id must be a non-empty string"))
    if isinstance(artifact_id, str) and artifact_id.strip() in typed_manifest.duplicates:
        paths = ", ".join(path.as_posix() for path in typed_manifest.duplicates[artifact_id.strip()])
        findings.append(_finding(record, "duplicate-artifact-id", f"artifact_id occurs at: {paths}"))

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

    active_registry = profiles.get("_registry")

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
        uses_legacy_transition_identity = (
            isinstance(active_registry, DocumentRegistry)
            and registry_classification is None
            and isinstance(legacy_map, Mapping)
            and isinstance(legacy_map.get(record.artifact_type), dict)
        )
        identity_profiles = (
            {record.artifact_type: raw_profile}
            if record.artifact_type == "archive" or uses_legacy_transition_identity
            else profile_map
        )
        for taxonomy_finding in validate_stable_identity(
            pathlib.PurePosixPath(record.path.as_posix()),
            record.metadata,
            identity_profiles,
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
        relation_ids = _relation_ids_for_record(record)
        for parent_id in parent_ids:
            if parent_id in relation_ids:
                findings.append(_finding(record, "self-parent", f"artifact references itself as parent: {parent_id}"))
                continue
            parent_record = _relation_record(typed_manifest, parent_id, record)
            if parent_id in typed_manifest.relation_conflicts:
                findings.append(
                    _finding(
                        record,
                        "ambiguous-relation-reference",
                        f"parent relation resolves to multiple exact or legacy Spec records: {parent_id}",
                    )
                )
            elif not _relation_reference_exists(typed_manifest, parent_id, record):
                findings.append(_finding(record, "unresolved-parent", f"parent artifact_id is unresolved: {parent_id}"))
            elif parent_record and allowed_parent_types:
                parent_type = parent_record.artifact_type
                if (
                    uses_legacy_parent_contract
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
                parent_type: index for index, parent_type in enumerate(parent_type_order)
            }
            resolved_parents = [
                _relation_record(typed_manifest, parent_id, record)
                for parent_id in parent_ids
            ]
            if all(
                parent_record is not None and parent_record.artifact_type in type_precedence
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
            findings.append(_finding(record, "parent-cycle", "parent_ids creates a cycle"))

    supersedes_value = record.metadata.get("supersedes")
    if supersedes_value is not None:
        supersedes = _string_list(supersedes_value)
        if supersedes is None:
            findings.append(_finding(record, "invalid-supersedes", "supersedes must be a list of non-empty strings"))
        else:
            relation_ids = _relation_ids_for_record(record)
            for replaced_id in supersedes:
                if replaced_id in relation_ids:
                    findings.append(_finding(record, "self-supersession", f"artifact supersedes itself: {replaced_id}"))
                elif replaced_id in typed_manifest.relation_conflicts:
                    findings.append(
                        _finding(
                            record,
                            "ambiguous-relation-reference",
                            f"supersedes relation resolves to multiple exact or legacy Spec records: {replaced_id}",
                        )
                    )
                elif not _relation_reference_exists(
                    typed_manifest, replaced_id, record
                ):
                    findings.append(
                        _finding(record, "unresolved-supersedes", f"superseded artifact_id is unresolved: {replaced_id}")
                    )
                else:
                    replaced_record = _relation_record(
                        typed_manifest, replaced_id, record
                    )
                    if replaced_record and replaced_record.metadata.get("status") != "superseded":
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
            for replaced_id in (
                _string_list(candidate.metadata.get("supersedes")) or []
            ):
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
    if successor is not None and (not isinstance(successor, str) or not _relation_reference_exists(typed_manifest, successor, record)):
        findings.append(_finding(record, "unresolved-superseded-by", "superseded_by must resolve to current or verified retired lineage"))
    if status == "active" and "reviewed_at" in required and reviewed_at in (None, ""):
        findings.append(
            _finding(record, "stale-active", "active freshness-managed artifact lacks reviewed_at evidence")
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
        "archived_at",
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
            _finding(record, "invalid-generator", "generated_by must be a safe canonical scripts/ repository path")
        )
    elif registered_owner is not None and generated_by is not None and generated_by != registered_owner:
        findings.append(
            _finding(
                record,
                "generated-owner-mismatch",
                "generated_by differs from the exact registered generator owner",
            )
        )

    if record.artifact_type == "archive":
        archived_from = record.metadata.get("archived_from")
        archive_source_prefixes = common.get("archive_source_prefixes", [])
        if archived_from is not None and not (
            isinstance(archive_source_prefixes, list)
            and any(
                _safe_repo_path(archived_from, prefix)
                for prefix in archive_source_prefixes
            )
        ):
            findings.append(
                _finding(
                    record,
                    "invalid-archived-from",
                    "archived_from must be a safe canonical path under a registered historical source root",
                )
            )
        current_replacement = record.metadata.get("current_replacement")
        if current_replacement is not None and not _safe_repo_path(
            current_replacement, "docs/"
        ):
            findings.append(
                _finding(
                    record,
                    "invalid-current-replacement",
                    "current_replacement must be a safe canonical docs/ repository path",
                )
            )
        archive_reason = record.metadata.get("archive_reason")
        if archive_reason is not None and (not isinstance(archive_reason, str) or not archive_reason.strip()):
            findings.append(_finding(record, "invalid-archive-reason", "archive_reason must be a non-empty string"))

        archive_disposition = record.metadata.get("archive_disposition")
        archive_disposition_valid = (
            isinstance(archive_disposition, str)
            and archive_disposition in EXPECTED_ARCHIVE_DISPOSITIONS
        )
        if archive_disposition is not None and not archive_disposition_valid:
            findings.append(
                _finding(
                    record,
                    "invalid-archive-disposition",
                    "archive_disposition must be a registered archive disposition",
                )
            )
        replacement_required_for = _condition_members(
            raw_profile,
            "replacement",
            "required_for",
        )
        replacement_forbidden_for = _condition_members(
            raw_profile,
            "replacement",
            "forbidden_for",
        )
        replacement_present = "current_replacement" in record.metadata
        replacement = record.metadata.get("current_replacement")
        if (
            archive_disposition_valid
            and archive_disposition in replacement_required_for
            and replacement in (None, "")
        ):
            findings.append(
                _finding(
                    record,
                    "archive-replacement-required",
                    "current_replacement is required for this archive disposition",
                )
            )
        if (
            archive_disposition_valid
            and archive_disposition in replacement_forbidden_for
            and replacement_present
        ):
            findings.append(
                _finding(
                    record,
                    "archive-replacement-forbidden",
                    "current_replacement is forbidden for this archive disposition",
                )
            )

        for key, code in (
            ("archived_commit", "invalid-archived-commit"),
            ("archived_blob", "invalid-archived-blob"),
        ):
            if key in record.metadata and not _valid_lowercase_object_id(record.metadata.get(key)):
                findings.append(
                    _finding(
                        record,
                        code,
                        f"{key} must be a lowercase full 40- or 64-hex object ID",
                    )
                )

        preservation_class = record.metadata.get("preservation_class")
        preservation_class_valid = (
            isinstance(preservation_class, str)
            and preservation_class in EXPECTED_PRESERVATION_CLASSES
        )
        if preservation_class is not None and not preservation_class_valid:
            findings.append(
                _finding(
                    record,
                    "invalid-preservation-class",
                    "preservation_class must be a registered archive preservation class",
                )
            )
        snapshot_fields = ("snapshot_path", "content_sha256", "snapshot_reason")
        snapshot_required_for = _condition_members(
            raw_profile,
            "snapshot",
            "required_for",
        )
        snapshot_forbidden_for = _condition_members(
            raw_profile,
            "snapshot",
            "forbidden_for",
        )
        if (
            preservation_class_valid
            and preservation_class in snapshot_forbidden_for
            and any(key in record.metadata for key in snapshot_fields)
        ):
            findings.append(
                _finding(
                    record,
                    "archive-snapshot-forbidden",
                    "snapshot fields are forbidden for this preservation class",
                )
            )
        if preservation_class_valid and preservation_class in snapshot_required_for:
            if (
                archive_disposition_valid
                and archive_disposition not in EXPECTED_SNAPSHOT_ARCHIVE_DISPOSITIONS
            ):
                findings.append(
                    _finding(
                        record,
                        "archive-snapshot-disposition-forbidden",
                        "immutable snapshots require an admitted archive disposition",
                    )
                )
            required_codes = {
                "snapshot_path": "archive-snapshot-path-required",
                "content_sha256": "archive-content-sha256-required",
                "snapshot_reason": "archive-snapshot-reason-required",
            }
            for key in snapshot_fields:
                if record.metadata.get(key) in (None, ""):
                    findings.append(
                        _finding(
                            record,
                            required_codes[key],
                            f"{key} is required for immutable snapshot preservation",
                        )
                    )

        if "snapshot_path" in record.metadata and not _safe_snapshot_path(
            record.metadata.get("snapshot_path")
        ):
            findings.append(
                _finding(
                    record,
                    "invalid-snapshot-path",
                    "snapshot_path must be a safe canonical archive evidence path",
                )
            )
        if "content_sha256" in record.metadata and not _valid_lowercase_sha256(
            record.metadata.get("content_sha256")
        ):
            findings.append(
                _finding(
                    record,
                    "invalid-content-sha256",
                    "content_sha256 must be a lowercase full 64-hex digest",
                )
            )
        snapshot_reason = record.metadata.get("snapshot_reason")
        if "snapshot_reason" in record.metadata and (
            not isinstance(snapshot_reason, str) or not snapshot_reason.strip()
        ):
            findings.append(
                _finding(
                    record,
                    "invalid-snapshot-reason",
                    "snapshot_reason must be a non-empty string",
                )
            )

    if not raw_profile.get("allow_additional", False):
        known = required | optional | forbidden | specialization_keys
        for key in sorted(set(record.metadata) - known):
            findings.append(
                _finding(record, "type-inappropriate-key", f"key is not declared for {profile_label}: {key}")
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
        return _parse_frontmatter_text(result.stdout)
    except FrontmatterError:
        return None


def _text_at_ref(root: pathlib.Path, path: pathlib.Path, base_ref: str | None) -> str | None:
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


def _previous_status(root: pathlib.Path, path: pathlib.Path, base_ref: str | None) -> str | None:
    loaded = _metadata_at_ref(root, path, base_ref)
    return loaded.get("status") if isinstance(loaded, dict) and isinstance(loaded.get("status"), str) else None


def _record_from_text(
    relative_path: pathlib.Path,
    text: str,
    previous_status: str | None = None,
    profiles: Mapping[str, object] | None = None,
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
    inferred_type = infer_artifact_type(relative_path, profiles)
    registry = profiles.get("_registry") if isinstance(profiles, Mapping) else None
    registered_package_readme = bool(
        inferred_type in {"data", "audit", "research"}
        and isinstance(registry, DocumentRegistry)
        and classify_registered_path(relative_path.as_posix(), registry) == inferred_type
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
        ["ls-tree", "-r", "-z", "--name-only", base_ref, "--", "docs", "archive"],
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
        records.append(_record_from_text(relative_path, shown.stdout, profiles=profiles))
    return records


def collect_selected_records_at_ref(
    root: pathlib.Path,
    profiles: dict[str, object],
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
            records[relative_path.as_posix()] = _record_from_text(
                relative_path,
                shown.stdout,
                profiles=profiles,
            )
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
                    infer_artifact_type(relative_path, profiles),
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
        raise ProfileError("transition override file must contain only transition_overrides")
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
            status
            for statuses in registry.lifecycles.values()
            for status in statuses
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
            raise ProfileError(f"transition override row {index} must define the exact evidence fields")
        if not all(isinstance(row[key], str) and row[key].strip() for key in expected_keys):
            raise ProfileError(f"transition override row {index} values must be non-empty strings")
        target = _normalized_target_path(row["path"])
        evidence = _normalized_target_path(row["evidence_task"])
        if target is None or not (root / target).is_file():
            raise ProfileError(f"transition override row {index} target path is not an existing canonical document")
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
    body_findings: Sequence[Finding],
    link_only_change: bool,
    task5_legacy_parent_ids: set[str],
    approved_structural_move: bool = False,
) -> tuple[int, int] | None:
    if record.parse_error or base_record is None:
        return None
    metadata_preserved = record.metadata == base_record.metadata
    if base_record.parse_error or not metadata_preserved:
        return None
    if any(finding.severity == "error" for finding in body_findings):
        return None
    current_errors = [finding for finding in findings if finding.severity == "error"]
    base_errors = [finding for finding in base_findings if finding.severity == "error"]
    if not current_errors:
        return None
    current_deficits = {_legacy_deficit_identity(finding) for finding in current_errors}
    base_deficits = {_legacy_deficit_identity(finding) for finding in base_errors}
    new_deficits = current_deficits - base_deficits
    if new_deficits:
        proven_parent_deficits = {
            _legacy_deficit_identity(finding)
            for finding in current_errors
            if finding.code == "unresolved-parent"
            and finding.message.removeprefix("parent artifact_id is unresolved: ")
            in task5_legacy_parent_ids
        }
        if not link_only_change or not new_deficits <= proven_parent_deficits:
            return None
    if approved_structural_move:
        return len(current_deficits), len(base_deficits)
    if link_only_change:
        return len(current_deficits), len(base_deficits)
    if record.path.as_posix() in APPROVED_MIGRATION_PATHS:
        return None
    if record.artifact_type in {
        "readme",
        "generated",
        "template-source",
        "governance",
        "archive",
        "unsupported",
    }:
        return None
    if MIGRATION_TYPED_KEYS & set(base_record.metadata) or MIGRATION_TYPED_KEYS & set(record.metadata):
        return None
    if any(finding.code not in LEGACY_EXCEPTION_CODES for finding in [*base_errors, *current_errors]):
        return None
    return len(current_deficits), len(base_deficits)


MARKDOWN_LINK_TARGET = re.compile(r"(?<!!)(?<!\\)\[([^\]\n]+)\]\([^)\n]+\)")


def _link_target_neutral_text(text: str) -> str:
    """Erase only Markdown destinations so link-only rewrites compare exactly."""

    return MARKDOWN_LINK_TARGET.sub(r"\1", text)


def _task5_move_body_sources(root: pathlib.Path) -> dict[str, tuple[str, str]]:
    """Return exact moved target -> immutable source mappings from mig-0001."""

    ledger = root / "docs/98.archive/migrations/0001-sdlc-taxonomy-convergence.md"
    try:
        text = ledger.read_text(encoding="utf-8")
        fenced = text.split("## Archive Ledger", 1)[1].split("```yaml", 1)[1].split(
            "```", 1
        )[0]
        document = _safe_load_unique(fenced)
    except (OSError, UnicodeError, IndexError, yaml.YAMLError):
        return {}
    records = document.get("records") if isinstance(document, dict) else None
    if not isinstance(records, list):
        return {}
    mappings: dict[str, tuple[str, str]] = {}
    for row in records:
        if not isinstance(row, dict) or row.get("action") != "move":
            continue
        target = row.get("stable_path")
        source = row.get("legacy_path")
        commit = row.get("source_commit")
        if not all(isinstance(value, str) and value for value in (target, source, commit)):
            return {}
        if target in mappings:
            return {}
        mappings[target] = (source, commit)
    return mappings


def _task5_legacy_parent_ids(root: pathlib.Path) -> set[str]:
    """Derive retired pre-taxonomy parent IDs only from frozen ledger rows."""

    ledger = root / "docs/98.archive/migrations/0001-sdlc-taxonomy-convergence.md"
    try:
        text = ledger.read_text(encoding="utf-8")
        fenced = text.split("## Archive Ledger", 1)[1].split("```yaml", 1)[1].split(
            "```", 1
        )[0]
        document = _safe_load_unique(fenced)
    except (OSError, UnicodeError, IndexError, yaml.YAMLError):
        return set()
    records = document.get("records") if isinstance(document, dict) else None
    if not isinstance(records, list):
        return set()
    identities: set[str] = set()
    for row in records:
        if not isinstance(row, dict):
            return set()
        legacy = row.get("legacy_path")
        artifact_id = row.get("artifact_id")
        if not isinstance(legacy, str) or not isinstance(artifact_id, str):
            continue
        spec_match = re.fullmatch(r"docs/(?:98\.archive/03\.specs/|03\.specs/)(\d{3})-([^/]+)/spec\.md", legacy)
        if artifact_id.startswith("spec-") and spec_match:
            identities.add(f"spec:{spec_match.group(1)}-{spec_match.group(2)}")
        execution_match = re.fullmatch(r"docs/04\.execution/(plans|tasks)/([^/]+)\.md", legacy)
        if execution_match:
            role = "plan" if execution_match.group(1) == "plans" else "task"
            identities.add(f"{role}:{execution_match.group(2)}")
    return identities


def _task5_moved_body_baseline(
    root: pathlib.Path,
    target: pathlib.Path,
    profiles: dict[str, object],
    mappings: Mapping[str, tuple[str, str]],
) -> tuple[Record | None, str | None]:
    """Read a moved document's body baseline through its frozen Git provenance."""

    source = mappings.get(target.as_posix())
    if source is None:
        return None, None
    legacy_path, source_commit = source
    shown = _run_git(
        root,
        ["show", f"{source_commit}:{legacy_path}"],
        operation="Task 5 moved-body baseline discovery",
        text=True,
    )
    if shown.returncode != 0:
        return None, None
    return _record_from_text(target, shown.stdout, profiles=profiles), shown.stdout


_TASK10_ARCHIVE_MOVE_SOURCES = {
    "docs/98.archive/migrations/0001-sdlc-taxonomy-convergence.md":
        "docs/98.archive/migrations/mig-0001-sdlc-taxonomy-convergence.md",
    "docs/98.archive/migrations/0002-operations-catalog-convergence.md":
        "docs/98.archive/migrations/mig-0002-operations-catalog-convergence.md",
    "docs/98.archive/migrations/0003-workspace-governance-simplification.md":
        "docs/98.archive/migrations/mig-0003-workspace-governance-simplification.md",
}


def _task10_archive_moved_body_baseline(
    root: pathlib.Path,
    target: pathlib.Path,
    profiles: dict[str, object],
    base_ref: str | None,
) -> tuple[Record | None, str | None]:
    """Read one exact prefix-removal source for the approved Stage 98 move."""

    legacy = _TASK10_ARCHIVE_MOVE_SOURCES.get(target.as_posix())
    if legacy is None:
        return None, None
    legacy_text = _text_at_ref(root, pathlib.Path(legacy), base_ref)
    if legacy_text is None:
        return None, None
    return _record_from_text(target, legacy_text, profiles=profiles), legacy_text
