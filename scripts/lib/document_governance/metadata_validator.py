#!/usr/bin/env python3
"""Compatibility facade for the responsibility-split metadata validator."""

from __future__ import annotations

from scripts.lib.document_governance.frontmatter import (
    FrontmatterError,
    parse_frontmatter_text as _parse_frontmatter_text,
    read_frontmatter_values as parse_frontmatter,
    safe_load_unique as _safe_load_unique,
)
from scripts.lib.document_governance.identity_history import collect_issued_identities
from scripts.lib.document_governance.registry import (
    DEFAULT_REGISTRY,
    DocumentRegistry,
    RegistryError,
    load_registry,
    validate_frontmatter,
)
from scripts.lib.document_governance.metadata.heading import (
    _introduced_body_findings,
    _native_migration_compaction_witness,
    validate_body_contract,
)
from scripts.lib.document_governance.metadata.lifecycle import (
    _record_from_text,
    collect_records_at_ref,
    load_transition_overrides,
    validate_record,
)
from scripts.lib.document_governance.metadata.profile import (
    EXPECTED_EXCEPTION_SCHEMA,
    TARGET_MARKDOWN_PREFIXES,
    Finding,
    ProfileError,
    Record,
    _safe_repo_path,
    _valid_metadata_artifact_id,
    build_current_manifest,
    build_manifest,
    build_registry_profiles,
    classify_template_role,
    infer_artifact_type,
    load_profiles,
    matching_template_roles,
    registered_generated_owner,
    validate_static_exception_document,
    validate_static_migration_manifest,
)
from scripts.lib.document_governance.metadata.reference import (
    _write_or_check_output,
    main,
    render_report,
    validate_repository_contracts,
)


__all__ = (
    "DEFAULT_REGISTRY",
    "DocumentRegistry",
    "EXPECTED_EXCEPTION_SCHEMA",
    "Finding",
    "FrontmatterError",
    "ProfileError",
    "Record",
    "RegistryError",
    "TARGET_MARKDOWN_PREFIXES",
    "_introduced_body_findings",
    "_native_migration_compaction_witness",
    "_parse_frontmatter_text",
    "_record_from_text",
    "_safe_load_unique",
    "_safe_repo_path",
    "_valid_metadata_artifact_id",
    "_write_or_check_output",
    "build_current_manifest",
    "build_manifest",
    "build_registry_profiles",
    "collect_issued_identities",
    "collect_records_at_ref",
    "classify_template_role",
    "infer_artifact_type",
    "load_profiles",
    "load_registry",
    "load_transition_overrides",
    "main",
    "matching_template_roles",
    "parse_frontmatter",
    "registered_generated_owner",
    "render_report",
    "validate_body_contract",
    "validate_frontmatter",
    "validate_record",
    "validate_repository_contracts",
    "validate_static_exception_document",
    "validate_static_migration_manifest",
)
