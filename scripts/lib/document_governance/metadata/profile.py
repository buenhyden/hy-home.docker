#!/usr/bin/env python3
"""Registry profiles, shared metadata models, and path classification."""

from __future__ import annotations

import collections
import copy
import dataclasses
import datetime as dt
import fnmatch
import os
import pathlib
import re
import stat
import sys
from collections.abc import Mapping, Sequence

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
    if (
        not stat.S_ISDIR(descriptor.st_mode)
        or (descriptor.st_dev, descriptor.st_ino)
        != (direct.st_dev, direct.st_ino)
    ):
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
    parse_frontmatter_text as _parse_frontmatter_text,
    read_frontmatter_values,
    safe_load_unique as _safe_load_unique,
)
from scripts.lib.document_governance.git_provenance import (  # noqa: E402
    HistoricalDocument,
)
from scripts.lib.document_governance.registry import (  # noqa: E402
    DEFAULT_REGISTRY,
    DocumentRegistry,
    RegistryError,
    classify_path as classify_registered_path,
    load_registry,
)
from scripts.lib.document_governance.taxonomy import (  # noqa: E402
    classify_path as classify_taxonomy_path,
    requirement_package_identity,
)


# Retain the validator's established public parser name while keeping the
# shared implementation imported under its canonical library name.
parse_frontmatter = read_frontmatter_values


DEFAULT_PROFILES = DEFAULT_REGISTRY
LEGACY_TRANSITION_PROFILES = (
    HistoricalDocument(
        ROOT, "494065806794980080b081439298d7b534d10803",
        "docs/99.templates/support/document-metadata-profiles.yaml",
    )
)
DEFAULT_AGENT_GOVERNANCE_REGISTRY = ROOT / "docs/99.templates/registry.json"
OPERATIONS_CATALOG_DOMAINS = frozenset(
    {
        "00-workspace",
        "01-gateway",
        "02-auth",
        "03-security",
        "04-data",
        "05-messaging",
        "06-observability",
        "07-workflow",
        "08-ai",
        "09-tooling",
        "10-communication",
        "11-laboratory",
        "12-infra-net",
    }
)
EXPECTED_ARCHIVE_DISPOSITIONS = (
    "superseded",
    "duplicate",
    "conflict",
    "withdrawn",
    "evidence-preserve",
)
EXPECTED_PRESERVATION_CLASSES = ("git-history", "immutable-snapshot")
EXPECTED_SNAPSHOT_ARCHIVE_DISPOSITIONS = ("evidence-preserve",)
EXPECTED_MANIFEST_DISPOSITIONS = (
    "migrate",
    "preserve",
    "move",
    "merge",
    "archive",
    "delete",
    "regenerate",
    "exempt",
)
EXPECTED_MANIFEST_SCHEMA = {
    "top_level_fields": [
        "schema_version",
        "wave",
        "baseline_commit",
        "generated_by",
        "enforcement",
        "entries",
    ],
    "entry_fields": [
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
    ],
    "evidence_fields": [
        "commands",
        "sources",
        "repository_paths",
        "consumer_scan",
        "rollback",
    ],
    "review_verdict_fields": ["specification", "quality"],
    "review_verdict_values": ["pending", "pass", "changes-required"],
    "field_contracts": {
        "schema_version": {
            "type": "integer",
            "nullable": False,
            "domain": "constant-1",
        },
        "wave": {
            "type": "string",
            "nullable": False,
            "domain": "non-empty-string",
        },
        "baseline_commit": {
            "type": "string",
            "nullable": False,
            "domain": "lowercase-full-object-id",
        },
        "generated_by": {
            "type": "string",
            "nullable": False,
            "domain": "non-empty-string",
        },
        "enforcement": {
            "type": "string",
            "nullable": False,
            "domain": "advisory-or-blocking",
        },
        "entries": {
            "type": "list",
            "nullable": False,
            "domain": "migration-entry",
        },
        "source_path": {
            "type": "string",
            "nullable": False,
            "domain": "safe-baseline-tracked-path",
        },
        "target_path": {
            "type": "string",
            "nullable": True,
            "domain": "safe-repository-path",
            "null_condition": "disposition-delete",
        },
        "artifact_id": {
            "type": "string",
            "nullable": True,
            "domain": "canonical-metadata-artifact-id",
            "null_condition": "selected-profile-does-not-require-artifact-id",
        },
        "artifact_type": {
            "type": "string",
            "nullable": False,
            "domain": "registered-artifact-type",
        },
        "status_before": {
            "type": "string",
            "nullable": True,
            "domain": "registered-lifecycle-status",
            "null_condition": "selected-profile-does-not-require-status",
        },
        "status_after": {
            "type": "string",
            "nullable": True,
            "domain": "registered-lifecycle-status",
            "null_condition": "selected-profile-does-not-require-status",
        },
        "parent_ids": {
            "type": "list",
            "nullable": False,
            "domain": "deterministic-string-list",
        },
        "disposition": {
            "type": "string",
            "nullable": False,
            "domain": "registered-manifest-disposition",
        },
        "canonical_replacement": {
            "type": "string",
            "nullable": True,
            "domain": "non-empty-string",
            "null_condition": "replacement-requirements",
        },
        "active_consumers": {
            "type": "list",
            "nullable": False,
            "domain": "deterministic-safe-path-list",
        },
        "partition_plan": {
            "type": "string",
            "nullable": True,
            "domain": "safe-approved-plan-path",
        },
        "preservation_class": {
            "type": "string",
            "nullable": True,
            "domain": "registered-preservation-class",
            "null_condition": "non-destructive-row",
        },
        "evidence": {
            "type": "mapping",
            "nullable": False,
            "domain": "exact-evidence-mapping",
        },
        "review_verdict": {
            "type": "mapping",
            "nullable": False,
            "domain": "exact-review-verdict-mapping",
        },
        "evidence.commands": {
            "type": "list",
            "nullable": False,
            "domain": "deterministic-string-list",
        },
        "evidence.sources": {
            "type": "list",
            "nullable": False,
            "domain": "deterministic-string-list",
        },
        "evidence.repository_paths": {
            "type": "list",
            "nullable": False,
            "domain": "deterministic-string-list",
        },
        "evidence.consumer_scan": {
            "type": "list",
            "nullable": False,
            "domain": "deterministic-string-list",
        },
        "evidence.rollback": {
            "type": "list",
            "nullable": False,
            "domain": "deterministic-string-list",
        },
        "review_verdict.specification": {
            "type": "string",
            "nullable": False,
            "domain": "review-verdict-values",
        },
        "review_verdict.quality": {
            "type": "string",
            "nullable": False,
            "domain": "review-verdict-values",
        },
    },
    "deterministic_order": {
        "entries": "source_path",
        "parent_ids": "lexicographic",
        "active_consumers": "lexicographic",
        "evidence.commands": "lexicographic",
        "evidence.sources": "lexicographic",
        "evidence.repository_paths": "lexicographic",
        "evidence.consumer_scan": "lexicographic",
        "evidence.rollback": "lexicographic",
    },
    "destructive_execution": {
        "dispositions": ["merge", "archive", "delete"],
        "active_consumers_required": True,
        "empty_consumers_require": "evidence.consumer_scan",
        "non_empty_evidence": [
            "commands",
            "sources",
            "repository_paths",
            "consumer_scan",
            "rollback",
        ],
        "preservation_class_required": True,
        "replacement_semantics": "replacement_requirements",
        "required_review": {"specification": "pass", "quality": "pass"},
    },
}
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
EXPECTED_MANIFEST_SCHEMA_V2 = {
    **EXPECTED_MANIFEST_SCHEMA,
    "entry_fields": [
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
    ],
    "field_contracts": {
        **{
            key: value
            for key, value in EXPECTED_MANIFEST_SCHEMA["field_contracts"].items()
            if key != "artifact_type"
        },
        "schema_version": {
            "type": "integer",
            "nullable": False,
            "domain": "constant-2",
        },
        "artifact_id": {
            "type": "string",
            "nullable": True,
            "domain": "canonical-metadata-artifact-id",
            "null_condition": "target-profile-does-not-require-artifact-id-or-delete",
        },
        "status_before": {
            "type": "string",
            "nullable": True,
            "domain": "registered-lifecycle-status",
            "null_condition": "baseline-profile-does-not-require-status",
        },
        "status_after": {
            "type": "string",
            "nullable": True,
            "domain": "registered-lifecycle-status",
            "null_condition": "target-profile-does-not-require-status-or-delete",
        },
        "artifact_type_before": {
            "type": "string",
            "nullable": True,
            "domain": "registered-artifact-type",
            "null_condition": "baseline-surface-is-native-or-unsupported",
        },
        "artifact_type_after": {
            "type": "string",
            "nullable": True,
            "domain": "registered-artifact-type",
            "null_condition": "target-surface-is-native-or-unsupported-or-delete",
        },
        "surface_class": {
            "type": "string",
            "nullable": False,
            "domain": "registered-surface-class",
        },
    },
}
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
    "docs/00.agent-governance/policies/documentation-protocol.md",
    "docs/00.agent-governance/policies/stage-authoring-matrix.md",
    "docs/00.agent-governance/policies/task-checklists.md",
    "docs/01.requirements/005-data-analytics.md",
    "docs/02.architecture/decisions/0015-analytics-engine-selection.md",
    "docs/02.architecture/requirements/0012-data-analytics-architecture.md",
    "docs/03.specs/0005-data-analytics/README.md",
    "docs/03.specs/0005-data-analytics/spec.md",
    "docs/03.specs/README.md",
    "docs/05.operations/" "guides/04-data/analytics/README.md",
    "docs/05.operations/" "guides/04-data/analytics/influxdb.md",
    "docs/05.operations/" "guides/04-data/lake-and-object/seaweedfs.md",
    "docs/05.operations/" "guides/09-tooling/k6.md",
    "docs/05.operations/" "guides/09-tooling/locust.md",
    "docs/05.operations/" "guides/09-tooling/performance-testing.md",
    "docs/05.operations/" "policies/04-data/analytics/influxdb.md",
    "docs/05.operations/" "policies/04-data/lake-and-object/seaweedfs.md",
    "docs/05.operations/" "policies/09-tooling/k6.md",
    "docs/05.operations/" "policies/09-tooling/locust.md",
    "docs/05.operations/" "policies/09-tooling/performance-testing.md",
    "docs/05.operations/" "runbooks/04-data/analytics/influxdb.md",
    "docs/05.operations/" "runbooks/09-tooling/k6.md",
    "docs/05.operations/" "runbooks/09-tooling/locust.md",
    "docs/05.operations/" "runbooks/09-tooling/performance-testing.md",
    "docs/90.references/audits/0019-readme/README.md",
    "docs/90.references/audits/0021-automation-candidates/README.md",
    "docs/90.references/audits/0022-compose-infrastructure-operations-readiness/README.md",
    "docs/90.references/audits/0023-frontmatter-semantic-inventory/README.md",
    "docs/90.references/audits/0024-frontmatter-template-readme-implementation/README.md",
    "docs/90.references/audits/0026-implementation-overview/README.md",
    "docs/90.references/audits/0029-sdlc-document-contracts-implementation/README.md",
    "docs/90.references/audits/0030-sdlc-quality-formatting-implementation/README.md",
    "docs/90.references/audits/0031-security-framework-maturity/README.md",
    "docs/90.references/data/0076-llm-wiki-stage-category-coverage/README.md",
    "docs/90.references/data/0082-llm-wiki-index/README.md",
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
EXPECTED_EXCEPTION_SCHEMA = {
    "top_level_fields": ["schema_version", "exceptions"],
    "entry_fields": [
        "finding_code",
        "scope_paths",
        "owner",
        "reason",
        "approved_at",
        "expires_on",
        "exit_condition",
        "evidence",
    ],
    "field_contracts": {
        "schema_version": {
            "type": "integer",
            "nullable": False,
            "domain": "constant-1",
        },
        "exceptions": {
            "type": "list",
            "nullable": False,
            "domain": "bounded-exception",
        },
        "finding_code": {
            "type": "string",
            "nullable": False,
            "domain": "validator-known-finding-code",
        },
        "scope_paths": {
            "type": "list",
            "nullable": False,
            "domain": "deterministic-bounded-safe-path-list",
        },
        "owner": {
            "type": "string",
            "nullable": False,
            "domain": "non-empty-string",
        },
        "reason": {
            "type": "string",
            "nullable": False,
            "domain": "non-empty-string",
        },
        "approved_at": {
            "type": "string",
            "nullable": False,
            "domain": "strict-iso-date-not-future",
        },
        "expires_on": {
            "type": "string",
            "nullable": False,
            "domain": "strict-iso-date-after-validation-date",
        },
        "exit_condition": {
            "type": "string",
            "nullable": False,
            "domain": "non-empty-string",
        },
        "evidence": {
            "type": "list",
            "nullable": False,
            "domain": "deterministic-non-empty-safe-path-list",
        },
    },
    "deterministic_order": {
        "exceptions": "finding_code-and-scope-paths",
        "scope_paths": "lexicographic",
        "evidence": "lexicographic",
    },
    "bounded_semantics": {
        "finding_code_source": "validator-known-finding-codes",
        "require_non_empty_scope_paths": True,
        "forbid_wildcards": True,
        "forbid_global_scopes": ["*", "**", ".", "all", "global"],
        "require_non_empty_text": ["owner", "reason", "exit_condition"],
        "approval": "approved_at-not-future",
        "expiry": "expires_on-after-validation-date",
        "require_non_empty_safe_evidence_paths": True,
    },
}
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
EXPECTED_ARCHIVE_REQUIRED = (
    "status",
    "artifact_id",
    "artifact_type",
    "parent_ids",
    "archived_from",
    "archived_at",
    "archive_reason",
    "archive_disposition",
    "archived_commit",
    "archived_blob",
    "preservation_class",
)
EXPECTED_ARCHIVE_OPTIONAL = (
    "layer",
    "supersedes",
    "current_replacement",
    "snapshot_path",
    "content_sha256",
    "snapshot_reason",
)
EXPECTED_ARCHIVE_CONDITIONS = {
    "replacement": {
        "field": "current_replacement",
        "required_for": ["superseded", "duplicate", "conflict"],
        "forbidden_for": ["withdrawn"],
        "optional_for": ["evidence-preserve"],
    },
    "snapshot": {
        "fields": ["snapshot_path", "content_sha256", "snapshot_reason"],
        "required_for": ["immutable-snapshot"],
        "forbidden_for": ["git-history"],
    },
}
EXPECTED_ARCHIVE_SOURCE_PREFIXES = ("docs/", "archive/")
EXPECTED_DOCUMENT_FAMILIES = {
    "sdlc": (
        "prd",
        "srs",
        "interface-requirement",
        "architecture-description",
        "adr",
        "spec",
        "plan",
        "task",
        "guide",
        "policy",
        "runbook",
        "incident",
        "postmortem",
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
TYPED_EXAMPLE_FIXTURE_PATH = "examples/sample-web-service/service.md"
TYPED_EXAMPLE_FIXTURE_STATUS = "draft"
TYPED_EXAMPLE_FIXTURE_PARENT_IDS = (
    "spec:126-security-supply-chain-remediation",
    "spec:127-deployment-release-engineering-remediation",
)
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
ARCHIVE_PROFILE_KEYS = frozenset(
    {
        "path_globs",
        "template",
        "artifact_type",
        "id_pattern",
        "path_identity",
        "parent_id_pattern",
        "artifact_id_identity_pattern",
        "identity_capture",
        "required",
        "optional",
        "forbidden",
        "allowed_statuses",
        "allowed_parent_types",
        "allow_empty_parents",
        "disposition",
        "conditions",
    }
)
EXPECTED_ARCHIVE_PROFILE_NAMES = (
    "change-plan",
    "change-task",
    "tombstone",
    "migration",
)
EXPECTED_TEMPLATE_ROLE_NAMES = frozenset(
    {
        "adr",
        "agent-design",
        "api-spec",
        "archive",
        "architecture-description",
        "audit",
        "data-model",
        "guide",
        "incident",
        "plan",
        "policy",
        "postmortem",
        "prd",
        "readme",
        "reference",
        "runbook",
        "srs",
        "service",
        "spec",
        "task",
        "interface-requirement",
        "tests",
    }
)
TRANSITIONAL_UNREGISTERED_TEMPLATE_SOURCES: frozenset[str] = frozenset()
TARGET_MARKDOWN_PREFIXES = (
    "docs/00.agent-governance/",
    "docs/01.requirements/",
    "docs/02.architecture/",
    "docs/03.specs/",
    "docs/05.operations/",
    "docs/90.references/",
    "docs/98.archive/",
    "docs/99.templates/",
)
MIGRATION_TYPED_KEYS = frozenset(
    {"artifact_id", "artifact_type", "parent_ids", "supersedes", "reviewed_at", "next_review_at"}
)
APPROVED_MIGRATION_PATHS = frozenset(
    {
        "docs/90.references/audits/0019-readme/README.md",
        "docs/90.references/audits/0020-agent-instructions-catalog-vibe-models/README.md",
        "docs/90.references/audits/0021-automation-candidates/README.md",
        "docs/90.references/audits/0022-compose-infrastructure-operations-readiness/README.md",
        "docs/90.references/audits/0024-frontmatter-template-readme-implementation/README.md",
        "docs/90.references/audits/0025-harness-engineering-implementation/README.md",
        "docs/90.references/audits/0026-implementation-overview/README.md",
        "docs/90.references/audits/0027-loop-engineering-implementation/README.md",
        "docs/90.references/audits/0028-provider-harness-loop-implementation/README.md",
        "docs/90.references/audits/0029-sdlc-document-contracts-implementation/README.md",
        "docs/90.references/audits/0030-sdlc-quality-formatting-implementation/README.md",
        "docs/90.references/audits/0031-security-framework-maturity/README.md",
        "docs/90.references/audits/0032-workspace-rules-environment-implementation/README.md",
        "docs/99.templates/templates/common/readme.template.md",
        "docs/99.templates/templates/operations/guide.template.md",
        "docs/99.templates/templates/operations/incident.template.md",
        "docs/99.templates/templates/operations/policy.template.md",
        "docs/99.templates/templates/operations/postmortem.template.md",
        "docs/99.templates/templates/operations/runbook.template.md",
    }
)
LEGACY_EXCEPTION_CODES = frozenset(
    {"missing-required-key", "replacement-free-supersession", "stale-active"}
)
EXPECTED_TEMPLATE_PLACEHOLDER_KEYS = frozenset(
    {
        "artifact_id",
        "parent_id",
        "created",
        "updated",
        "completed_at",
        "reviewed_at",
        "next_review_at",
        "occurred_at",
        "resolved_at",
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
    }
)
MARKDOWN_BODY_TOKEN = re.compile(r"{{[a-z][a-z0-9_]*}}")
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
OPENAPI_JWT_VALUE = re.compile(
    r"\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b"
)
OPENAPI_AUTH_SCHEMES = frozenset({"basic", "bearer", "oauth", "oauth2", "openidconnect"})
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
    generated_outputs = common.get("generated_outputs") if isinstance(common, Mapping) else None
    if not isinstance(generated_outputs, Mapping):
        return None
    owner = generated_outputs.get(path.as_posix())
    return owner if isinstance(owner, str) else None


def _stage00_specialization_entry(
    path: pathlib.Path,
    contract_path: pathlib.Path = DEFAULT_AGENT_GOVERNANCE_REGISTRY,
) -> Mapping[str, object] | None:
    """Return the one Stage 99 profile registered for a Stage 00 path."""

    normalized = normalize_repo_relative_path(path)
    try:
        registry = load_registry(contract_path)
    except RegistryError:
        return None
    profile_id = classify_registered_path(normalized, registry)
    if profile_id is None or not normalized.startswith("docs/00.agent-governance/"):
        return None
    return registry.profiles.get(profile_id)


def infer_stage00_specialization(
    path: pathlib.Path,
    contract_path: pathlib.Path = DEFAULT_AGENT_GOVERNANCE_REGISTRY,
) -> str | None:
    """Infer the exact Stage 99 profile for a registered Stage 00 path."""

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
        legacy_map = profiles.get("_legacy_profiles")
        if not isinstance(legacy_map, Mapping):
            return "unsupported"
        if isinstance(legacy_map, Mapping):
            legacy_match = classify_taxonomy_path(
                pathlib.PurePosixPath(normalized), legacy_map
            )
            if legacy_match is not None:
                return legacy_match
        if registered_generated_owner(pathlib.Path(normalized), profiles) is not None:
            return "generated"
        # These are explicit, removable legacy corpus envelopes. Canonical
        # Stage 01/02/03/05 role paths must match Registry above or fail closed.
        if pathlib.PurePosixPath(normalized).name == "README.md":
            try:
                classify_readme_profile(pathlib.Path(normalized), dict(profiles))
            except ProfileError:
                pass
            else:
                return "readme"
        if normalized.startswith("docs/00.agent-governance/") or normalized.startswith(
            "docs/99.templates/support/"
        ):
            return "governance"
        if normalized.startswith("docs/98.archive/"):
            return "archive"
        if normalized.startswith("docs/90.references/audits/"):
            return "audit"
        if normalized.startswith("docs/90.references/"):
            return "reference"
        if normalized.startswith("docs/99.templates/templates/") and normalized.endswith(
            ".template.md"
        ):
            return "template-source"
        return "unsupported"
    name = pathlib.PurePosixPath(normalized).name
    if registered_generated_owner(pathlib.Path(normalized), profiles) is not None:
        return "generated"
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
        if pathlib.PurePosixPath(normalized).name.startswith("srs-"):
            return "srs"
        if pathlib.PurePosixPath(normalized).name.startswith("interface-"):
            return "interface-requirement"
        return "prd"
    if normalized.startswith("docs/02.architecture/descriptions/"):
        return "architecture-description"
    if normalized.startswith("docs/02.architecture/decisions/"):
        return "adr"
    if normalized.startswith("docs/03.specs/"):
        if name == "plan.md":
            return "plan"
        if name == "task.md":
            return "task"
        return "spec"
    if normalized.startswith("docs/05.operations/"):
        if name == "guide.md":
            return "guide"
        if name == "policy.md":
            return "policy"
        if name == "runbook.md":
            return "runbook"
    if normalized.startswith("docs/05.operations/incidents/"):
        return "postmortem" if name == "postmortem.md" else "incident"
    if normalized.startswith("docs/90.references/audits/"):
        return "audit"
    if normalized.startswith("docs/90.references/"):
        return "reference"
    return "unsupported"


LEGACY_SPEC_RELATION_PATH = re.compile(
    r"docs/03\.specs/spec-(?P<number>[0-9]{4})-[a-z0-9]+(?:-[a-z0-9]+)*/spec\.md"
)
LEGACY_SPEC_RELATION_ID = re.compile(r"spec-(?P<number>[0-9]{4})")
CANONICAL_REQUIREMENT_RELATION_PATH = re.compile(
    r"docs/01\.requirements/(?P<number>[0-9]{4})-[a-z0-9]+(?:-[a-z0-9]+)*\.md"
)
CANONICAL_REQUIREMENT_RELATION_ID = re.compile(r"REQ-(?P<number>[0-9]{4})")
LEGACY_REQUIREMENT_RELATION_ID = re.compile(r"prd-[0-9]{4}")


def _legacy_spec_relation_alias(record: Record) -> str | None:
    """Return the one-way canonical relation alias for a valid legacy Spec."""

    if (
        record.artifact_type != "spec"
        or record.metadata.get("type") != "specs/spec"
    ):
        return None
    path_match = LEGACY_SPEC_RELATION_PATH.fullmatch(record.path.as_posix())
    artifact_id = record.metadata.get("artifact_id")
    id_match = (
        LEGACY_SPEC_RELATION_ID.fullmatch(artifact_id)
        if isinstance(artifact_id, str)
        else None
    )
    if path_match is None or id_match is None:
        return None
    if path_match.group("number") != id_match.group("number"):
        return None
    return f"SPEC-{id_match.group('number')}"


def _legacy_requirement_relation_alias(record: Record) -> str | None:
    """Expose one read-only relation alias for immutable pre-migration evidence."""

    if record.artifact_type != "requirements-package":
        return None
    path_match = CANONICAL_REQUIREMENT_RELATION_PATH.fullmatch(
        record.path.as_posix()
    )
    artifact_id = record.metadata.get("artifact_id")
    id_match = (
        CANONICAL_REQUIREMENT_RELATION_ID.fullmatch(artifact_id)
        if isinstance(artifact_id, str)
        else None
    )
    if path_match is None or id_match is None:
        return None
    if path_match.group("number") != id_match.group("number"):
        return None
    return f"prd-{id_match.group('number')}"


def _legacy_requirement_reference_permitted(
    referencing_record: Record, artifact_id: str
) -> bool:
    """Limit legacy Requirement aliases to immutable Stage 98 evidence."""

    if LEGACY_REQUIREMENT_RELATION_ID.fullmatch(artifact_id) is None:
        return True
    return (
        referencing_record.path.as_posix().startswith("docs/98.archive/")
        and referencing_record.artifact_type in {"archive", "migration", "tombstone"}
        and referencing_record.metadata.get("status")
        in {"archived", "completed", "superseded"}
    )


def build_manifest(records: Sequence[Record], *, retired_records: Sequence[Record] = ()) -> dict[str, pathlib.Path]:
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
    relation_candidates: dict[str, list[Record]] = collections.defaultdict(list)
    for record in sorted(records, key=lambda item: item.path.as_posix()):
        artifact_id = record.metadata.get("artifact_id")
        if isinstance(artifact_id, str) and artifact_id.strip():
            relation_candidates[artifact_id.strip()].append(record)
        alias = _legacy_spec_relation_alias(record)
        if alias is not None:
            relation_candidates[alias].append(record)
        requirement_alias = _legacy_requirement_relation_alias(record)
        if requirement_alias is not None:
            relation_candidates[requirement_alias].append(record)

    relation_records_by_id: dict[str, Record] = {}
    relation_conflicts: dict[str, tuple[pathlib.Path, ...]] = {}
    for relation_id, candidates in sorted(relation_candidates.items()):
        unique = {
            candidate.path.as_posix(): candidate
            for candidate in candidates
        }
        if len(unique) == 1:
            relation_records_by_id[relation_id] = next(iter(unique.values()))
        else:
            relation_conflicts[relation_id] = tuple(
                sorted(candidate.path for candidate in unique.values())
            )

    for record in retired_records:
        artifact_id = record.metadata.get("artifact_id")
        if isinstance(artifact_id, str) and artifact_id not in relation_records_by_id:
            relation_records_by_id[artifact_id] = record
    return Manifest(
        values,
        duplicates,
        records_by_id,
        relation_records_by_id,
        relation_conflicts,
    )


def _profile_mapping(profiles: dict[str, object]) -> tuple[dict[str, object], dict[str, object]]:
    common = profiles.get("common", {})
    profile_map = profiles.get("profiles", {})
    if not isinstance(common, dict) or not isinstance(profile_map, dict):
        raise ProfileError("common and profiles must be mappings")
    return common, profile_map


def build_current_manifest(root: pathlib.Path, records: Sequence[Record]) -> dict[str, pathlib.Path]:
    """Resolve retired Spec lineage only through exact verified compact evidence."""

    current = build_manifest(records)
    needed: set[str] = set()
    for record in records:
        for field in ("parent_ids", "supersedes", "superseded_by"):
            value = record.metadata.get(field)
            values = [value] if isinstance(value, str) else value if isinstance(value, list) else []
            needed.update(item for item in values if isinstance(item, str)
                          and item.startswith("SPEC-") and item not in current)
    if not needed or not (root / "docs/98.archive/migrations/0003-workspace-governance-simplification.md").exists():
        return current
    from scripts.lib.document_governance.archive import _migration_document
    from scripts.lib.document_governance.git_provenance import HistoricalDocument

    try:
        migration = _migration_document(root)
        retired = []
        if migration["schema_version"] == 3:
            for row in migration["rows"]:
                source = row["source_path"]
                if (row["action"] != "delete" or row["artifact_id"] not in needed
                        or not source.endswith("/spec.md") or (root / source).exists()):
                    continue
                text = HistoricalDocument(root, row["recovery_commit"], source).read_text()
                values = _parse_frontmatter_text(text)
                # Read at its recovery commit, where the role key was still
                # `artifact_type`; the blob is frozen and never re-typed.
                if values.get("artifact_id") != row["artifact_id"] or values.get(
                    "artifact_type"
                ) != "spec":
                    raise ValueError("retired Spec identity does not match recovery")
                retired.append(Record(pathlib.Path(source), {**values, "status": "retired"}, "spec"))
        return build_manifest(records, retired_records=retired)
    except ValueError as error:
        raise ProfileError("retired Spec lineage recovery is invalid") from error


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
    if pure.is_absolute() or value != pure.as_posix() or any(part in {"", ".", ".."} for part in pure.parts):
        return False
    return required_prefix is None or value.startswith(required_prefix)


def _valid_lowercase_object_id(value: object) -> bool:
    return isinstance(value, str) and LOWERCASE_OBJECT_ID_RE.fullmatch(value) is not None


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
    without_digit_classes = value.replace("[0-9]", "")
    if any(marker in without_digit_classes for marker in "?[]{}"):
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
        right_star = right_index < len(right_tokens) and right_tokens[right_index] == "*"
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


def matching_archive_profiles(path: pathlib.Path, profiles: dict[str, object]) -> list[str]:
    """Return every path-selected archive profile matching one archive path."""

    normalized = pathlib.PurePosixPath(path.as_posix())
    if normalized.is_absolute() or any(part in {"", ".", ".."} for part in normalized.parts):
        return []
    archive_profiles = profiles.get("archive_profiles", {})
    if not isinstance(archive_profiles, dict):
        return []
    matches: list[str] = []
    for name, raw_profile in archive_profiles.items():
        if not isinstance(name, str) or not isinstance(raw_profile, dict):
            continue
        patterns = raw_profile.get("path_globs", [])
        if isinstance(patterns, list) and any(
            isinstance(pattern, str) and _target_glob_matches(normalized, pattern)
            for pattern in patterns
        ):
            matches.append(name)
    return matches


def classify_archive_profile(path: pathlib.Path, profiles: dict[str, object]) -> str:
    """Select exactly one semantic archive profile for a repository path."""

    matches = matching_archive_profiles(path, profiles)
    normalized = path.as_posix()
    if not matches:
        raise ProfileError(f"archive path is unclassified: {normalized}")
    if len(matches) > 1:
        raise ProfileError(
            f"archive path is ambiguous: {normalized}; profiles={','.join(matches)}"
        )
    return matches[0]


def archive_identity_profile(path: pathlib.Path, profiles: dict[str, object]) -> str | None:
    """Return the typed Stage 98 identity family, including malformed paths.

    Exact archive classification remains the acceptance boundary. This broader
    family router exists only so an invalid dated or misshapen Stage 98 path is
    still checked by the Task 1 stable-identity validator and receives the
    deterministic identity findings that explain why it is invalid.
    """

    normalized = pathlib.PurePosixPath(path.as_posix())
    parts = normalized.parts
    prefix = ("docs", "98.archive")
    if normalized.is_absolute() or parts[:2] != prefix or len(parts) < 4:
        return None
    family = parts[2]
    if family == "changes" and normalized.name == "plan.md":
        candidate = "change-plan"
    elif family == "changes" and normalized.name == "task.md":
        candidate = "change-task"
    elif family == "tombstones":
        candidate = "tombstone"
    elif family == "migrations":
        candidate = "migration"
    else:
        return None
    archive_profiles = profiles.get("archive_profiles", {})
    return candidate if isinstance(archive_profiles, dict) and candidate in archive_profiles else None


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


def _relation_record(
    manifest: Manifest,
    artifact_id: str,
    referencing_record: Record | None = None,
) -> Record | None:
    """Resolve exact IDs or one-way legacy Spec aliases for relations only."""

    if (
        referencing_record is not None
        and artifact_id not in manifest.records_by_id
        and not _legacy_requirement_reference_permitted(
            referencing_record, artifact_id
        )
    ):
        return None
    if artifact_id in manifest.relation_conflicts:
        return None
    return manifest.relation_records_by_id.get(artifact_id)


def _relation_reference_exists(
    manifest: Manifest,
    artifact_id: str,
    referencing_record: Record | None = None,
) -> bool:
    """Return whether an exact or unique transition relation is resolvable."""

    return (
        (
            referencing_record is None
            or artifact_id in manifest.records_by_id
            or _legacy_requirement_reference_permitted(
                referencing_record, artifact_id
            )
        )
        and artifact_id not in manifest.relation_conflicts
        and (
            artifact_id in manifest.relation_records_by_id
            or artifact_id in manifest
        )
    )


def _relation_ids_for_record(record: Record) -> frozenset[str]:
    relation_ids: set[str] = set()
    artifact_id = record.metadata.get("artifact_id")
    if isinstance(artifact_id, str) and artifact_id.strip():
        relation_ids.add(artifact_id.strip())
    alias = _legacy_spec_relation_alias(record)
    if alias is not None:
        relation_ids.add(alias)
    requirement_alias = _legacy_requirement_relation_alias(record)
    if requirement_alias is not None:
        relation_ids.add(requirement_alias)
    return frozenset(relation_ids)


def _has_parent_cycle(record: Record, parent_ids: list[str], manifest: Manifest) -> bool:
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


def _canonical_partition_plan_path(value: object) -> bool:
    return (
        isinstance(value, str)
        and _safe_contract_path(value)
        and CANONICAL_PARTITION_PLAN_PATH.fullmatch(value) is not None
    )




def _require_exact_mapping(
    value: object,
    fields: Sequence[str],
    label: str,
) -> Mapping[str, object]:
    if not isinstance(value, Mapping) or set(value) != set(fields):
        raise ProfileError(f"{label} must define the exact canonical fields")
    return value


def _deterministic_string_list(
    value: object,
    label: str,
    *,
    require_non_empty: bool = False,
    safe_paths: bool = False,
) -> list[str]:
    if not isinstance(value, list) or not all(
        isinstance(item, str) and item and item == item.strip() for item in value
    ):
        raise ProfileError(f"{label} must be a deterministic string list")
    if require_non_empty and not value:
        raise ProfileError(f"{label} must not be empty")
    if value != sorted(value) or len(value) != len(set(value)):
        raise ProfileError(f"{label} must be uniquely lexicographically ordered")
    if safe_paths and not all(_safe_contract_path(item) for item in value):
        raise ProfileError(f"{label} must contain only safe bounded repository paths")
    return value


def _non_empty_string(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip() or value != value.strip():
        raise ProfileError(f"{label} must be a non-empty canonical string")
    return value


def _profile_field_ownership(
    profile: Mapping[str, object],
    field: str,
    label: str,
) -> str:
    owners: list[str] = []
    for group in ("required", "optional", "forbidden"):
        members = profile.get(group)
        if not isinstance(members, list) or not all(
            isinstance(member, str) for member in members
        ):
            raise ProfileError(f"{label} selected profile has invalid {group} ownership")
        if field in members:
            owners.append(group)
    if len(owners) != 1:
        raise ProfileError(
            f"{label} selected profile must own {field} in exactly one field group"
        )
    return owners[0]


def _validate_static_migration_manifest_v2(
    document: object,
    contract: Mapping[str, object],
    profiles: Mapping[str, object],
) -> None:
    """Validate v2 surface rows without assuming every source is UTF-8 Markdown."""

    if contract.get("manifest_schema_v2") != EXPECTED_MANIFEST_SCHEMA_V2:
        raise ProfileError("manifest contract must use the exact v2 static schema")
    manifest = _require_exact_mapping(
        document,
        EXPECTED_MANIFEST_SCHEMA_V2["top_level_fields"],
        "migration manifest",
    )
    if type(manifest.get("schema_version")) is not int or manifest.get("schema_version") != 2:
        raise ProfileError("manifest schema_version must be the integer 2")
    _non_empty_string(manifest.get("wave"), "manifest wave")
    if not _valid_lowercase_object_id(manifest.get("baseline_commit")):
        raise ProfileError("manifest baseline_commit must be a lowercase full object ID")
    _non_empty_string(manifest.get("generated_by"), "manifest generated_by")
    if manifest.get("enforcement") not in {"advisory", "blocking"}:
        raise ProfileError("manifest enforcement must be advisory or blocking")

    raw_profile_map = profiles.get("profiles")
    raw_common = profiles.get("common")
    if not isinstance(raw_profile_map, Mapping) or not isinstance(raw_common, Mapping):
        raise ProfileError("manifest validation requires the typed profile registry")
    artifact_types = set(raw_profile_map)
    allowed_statuses = set(raw_common.get("allowed_statuses", []))
    raw_manifest_contract = contract.get("manifest")
    raw_archive_contract = contract.get("archive")
    if not isinstance(raw_manifest_contract, Mapping) or not isinstance(raw_archive_contract, Mapping):
        raise ProfileError("manifest validation requires disposition registries")
    dispositions = set(raw_manifest_contract.get("dispositions", []))
    preservation_classes = set(raw_archive_contract.get("preservation_classes", []))
    replacement_requirements = contract.get("replacement_requirements")
    if not isinstance(replacement_requirements, Mapping):
        raise ProfileError("manifest validation requires replacement semantics")
    replacement_required = set(replacement_requirements.get("required_for", []))
    replacement_optional = set(replacement_requirements.get("optional_for", []))
    replacement_forbidden = set(replacement_requirements.get("forbidden_for", []))
    destructive = set(EXPECTED_MANIFEST_SCHEMA_V2["destructive_execution"]["dispositions"])
    verdict_values = set(EXPECTED_MANIFEST_SCHEMA_V2["review_verdict_values"])

    entries = manifest.get("entries")
    if not isinstance(entries, list):
        raise ProfileError("manifest entries must be a list")
    source_paths: list[str] = []
    for index, raw_entry in enumerate(entries):
        label = f"manifest entry {index}"
        entry = _require_exact_mapping(
            raw_entry, EXPECTED_MANIFEST_SCHEMA_V2["entry_fields"], label
        )
        source_path = entry.get("source_path")
        if not isinstance(source_path, str) or not _safe_contract_path(source_path):
            raise ProfileError(f"{label} source_path must be a safe repository path")
        source_paths.append(source_path)
        disposition = entry.get("disposition")
        if disposition not in dispositions:
            raise ProfileError(f"{label} disposition must be registered")
        target_path = entry.get("target_path")
        if target_path is not None and not _safe_contract_path(target_path):
            raise ProfileError(f"{label} target_path must be null or safe")
        if disposition == "delete" and target_path is not None:
            raise ProfileError(f"{label} delete target_path must be null")
        if disposition in {"move", "merge", "archive"} and (
            target_path is None or target_path == source_path
        ):
            raise ProfileError(f"{label} target_path must be distinct for its disposition")
        if disposition in {"migrate", "preserve", "regenerate", "exempt"} and target_path != source_path:
            raise ProfileError(f"{label} target_path must equal source_path")

        surface_class = entry.get("surface_class")
        if surface_class not in TARGET_SURFACE_CLASSES:
            raise ProfileError(f"{label} surface_class must be registered")
        before = entry.get("artifact_type_before")
        after = entry.get("artifact_type_after")
        bounded_legacy_source_type = (
            before == "ard"
            and source_path.startswith("docs/02.architecture/requirements/")
            and source_path in TARGET_SURFACE_DIRECT_SOURCE_PATHS
        )
        for field, value in (("artifact_type_before", before), ("artifact_type_after", after)):
            if value is not None and value not in artifact_types and not bounded_legacy_source_type:
                raise ProfileError(f"{label} {field} must be null or registered")
        if surface_class == "content-archive" and after != "archive":
            raise ProfileError(f"{label} content-archive must converge to semantic archive")
        selected_type = after if isinstance(after, str) else before
        artifact_id = entry.get("artifact_id")
        if artifact_id is not None and not _valid_metadata_artifact_id(artifact_id):
            raise ProfileError(f"{label} artifact_id must satisfy canonical validation")
        if selected_type is None and artifact_id is not None:
            raise ProfileError(f"{label} native row artifact_id must be null")
        for status_field in ("status_before", "status_after"):
            status = entry.get(status_field)
            if status is not None and status not in allowed_statuses:
                raise ProfileError(f"{label} {status_field} must be null or registered")
        _deterministic_string_list(entry.get("parent_ids"), f"{label} parent_ids")
        _deterministic_string_list(
            entry.get("active_consumers"), f"{label} active_consumers", safe_paths=True
        )

        replacement = entry.get("canonical_replacement")
        if replacement is not None:
            _non_empty_string(replacement, f"{label} canonical_replacement")
        if disposition in replacement_required and replacement is None:
            raise ProfileError(f"{label} canonical_replacement is required")
        if disposition in replacement_forbidden and replacement is not None:
            raise ProfileError(f"{label} canonical_replacement must be null")
        if disposition not in replacement_required | replacement_optional | replacement_forbidden:
            raise ProfileError(f"{label} disposition lacks replacement semantics")
        partition_plan = entry.get("partition_plan")
        if partition_plan is not None and not _canonical_partition_plan_path(
            partition_plan
        ):
            raise ProfileError(
                f"{label} partition_plan must be a canonical Spec Package Plan path"
            )
        preservation_class = entry.get("preservation_class")
        if preservation_class is not None and preservation_class not in preservation_classes:
            raise ProfileError(f"{label} preservation_class must be registered")
        evidence = _require_exact_mapping(
            entry.get("evidence"), EXPECTED_MANIFEST_SCHEMA_V2["evidence_fields"], f"{label} evidence"
        )
        evidence_lists = {
            field: _deterministic_string_list(evidence.get(field), f"{label} evidence.{field}")
            for field in EXPECTED_MANIFEST_SCHEMA_V2["evidence_fields"]
        }
        review = _require_exact_mapping(
            entry.get("review_verdict"),
            EXPECTED_MANIFEST_SCHEMA_V2["review_verdict_fields"],
            f"{label} review_verdict",
        )
        if any(review.get(field) not in verdict_values for field in EXPECTED_MANIFEST_SCHEMA_V2["review_verdict_fields"]):
            raise ProfileError(f"{label} review_verdict values must be registered")
        if disposition in destructive:
            if preservation_class is None:
                raise ProfileError(f"{label} destructive row requires preservation_class")
            if any(not evidence_lists[field] for field in evidence_lists):
                raise ProfileError(f"{label} destructive evidence lists must not be empty")
            if review != {"specification": "pass", "quality": "pass"}:
                raise ProfileError(f"{label} destructive row requires pass/pass review")
    if source_paths != sorted(source_paths) or len(source_paths) != len(set(source_paths)):
        raise ProfileError("manifest entries must be uniquely ordered by source_path")


def validate_static_migration_manifest(
    document: object,
    contract: Mapping[str, object],
    profiles: Mapping[str, object],
) -> None:
    """Validate manifest semantics that require no repository or object access."""

    if isinstance(document, Mapping) and document.get("schema_version") == 2:
        _validate_static_migration_manifest_v2(document, contract, profiles)
        return

    if contract.get("manifest_schema") != EXPECTED_MANIFEST_SCHEMA:
        raise ProfileError("manifest contract must use the exact static schema")
    manifest = _require_exact_mapping(
        document,
        EXPECTED_MANIFEST_SCHEMA["top_level_fields"],
        "migration manifest",
    )
    if type(manifest.get("schema_version")) is not int or manifest.get("schema_version") != 1:
        raise ProfileError("manifest schema_version must be the integer 1")
    _non_empty_string(manifest.get("wave"), "manifest wave")
    if not _valid_lowercase_object_id(manifest.get("baseline_commit")):
        raise ProfileError("manifest baseline_commit must be a lowercase full object ID")
    _non_empty_string(manifest.get("generated_by"), "manifest generated_by")
    enforcement = manifest.get("enforcement")
    if not isinstance(enforcement, str) or enforcement not in {"advisory", "blocking"}:
        raise ProfileError("manifest enforcement must be advisory or blocking")

    raw_profile_map = profiles.get("profiles")
    raw_common = profiles.get("common")
    if not isinstance(raw_profile_map, Mapping) or not isinstance(raw_common, Mapping):
        raise ProfileError("manifest validation requires the typed profile registry")
    artifact_types = set(raw_profile_map)
    allowed_status_values = raw_common.get("allowed_statuses")
    if not isinstance(allowed_status_values, list) or not all(
        isinstance(status, str) and status for status in allowed_status_values
    ):
        raise ProfileError("manifest validation requires registered lifecycle statuses")
    allowed_statuses = set(allowed_status_values)

    raw_manifest_contract = contract.get("manifest")
    raw_archive_contract = contract.get("archive")
    if not isinstance(raw_manifest_contract, Mapping) or not isinstance(
        raw_archive_contract, Mapping
    ):
        raise ProfileError("manifest validation requires disposition registries")
    dispositions = set(raw_manifest_contract.get("dispositions", []))
    preservation_classes = set(raw_archive_contract.get("preservation_classes", []))
    replacement_requirements = contract.get("replacement_requirements")
    if not isinstance(replacement_requirements, Mapping):
        raise ProfileError("manifest validation requires replacement semantics")
    replacement_required = set(replacement_requirements.get("required_for", []))
    replacement_optional = set(replacement_requirements.get("optional_for", []))
    replacement_forbidden = set(replacement_requirements.get("forbidden_for", []))

    entries = manifest.get("entries")
    if not isinstance(entries, list):
        raise ProfileError("manifest entries must be a list")
    source_paths: list[str] = []
    entry_fields = EXPECTED_MANIFEST_SCHEMA["entry_fields"]
    evidence_fields = EXPECTED_MANIFEST_SCHEMA["evidence_fields"]
    review_fields = EXPECTED_MANIFEST_SCHEMA["review_verdict_fields"]
    verdict_values = set(EXPECTED_MANIFEST_SCHEMA["review_verdict_values"])
    destructive = set(
        EXPECTED_MANIFEST_SCHEMA["destructive_execution"]["dispositions"]
    )

    for index, raw_entry in enumerate(entries):
        label = f"manifest entry {index}"
        entry = _require_exact_mapping(raw_entry, entry_fields, label)
        source_path = entry.get("source_path")
        if not isinstance(source_path, str) or not _safe_contract_path(source_path):
            raise ProfileError(f"{label} source_path must be a safe repository path")
        source_paths.append(source_path)

        disposition = entry.get("disposition")
        if not isinstance(disposition, str) or disposition not in dispositions:
            raise ProfileError(f"{label} disposition must be registered")

        target_path = entry.get("target_path")
        if target_path is not None and not _safe_contract_path(target_path):
            raise ProfileError(f"{label} target_path must be null or a safe repository path")
        if disposition == "delete" and target_path is not None:
            raise ProfileError(f"{label} delete target_path must be null")
        if disposition in {"move", "merge", "archive"} and (
            target_path is None or target_path == source_path
        ):
            raise ProfileError(f"{label} target_path must be distinct for its disposition")
        if disposition in {"migrate", "preserve", "regenerate", "exempt"} and (
            target_path != source_path
        ):
            raise ProfileError(f"{label} target_path must equal source_path")

        artifact_type = entry.get("artifact_type")
        if not isinstance(artifact_type, str) or artifact_type not in artifact_types:
            raise ProfileError(f"{label} artifact_type must be registered")
        selected_profile = raw_profile_map.get(artifact_type)
        if not isinstance(selected_profile, Mapping):
            raise ProfileError(f"{label} artifact_type must select a metadata profile")

        artifact_id_ownership = _profile_field_ownership(
            selected_profile,
            "artifact_id",
            label,
        )
        artifact_id = entry.get("artifact_id")
        if artifact_id is None:
            if artifact_id_ownership == "required":
                raise ProfileError(
                    f"{label} artifact_id is required by the selected metadata profile"
                )
        elif artifact_id_ownership == "forbidden":
            raise ProfileError(
                f"{label} artifact_id is forbidden by the selected metadata profile"
            )
        elif not _valid_metadata_artifact_id(artifact_id):
            raise ProfileError(
                f"{label} artifact_id must satisfy canonical metadata validation"
            )

        status_ownership = _profile_field_ownership(selected_profile, "status", label)
        for status_field in ("status_before", "status_after"):
            status = entry.get(status_field)
            if status is None:
                if status_ownership == "required":
                    raise ProfileError(
                        f"{label} {status_field} is required by the selected metadata profile"
                    )
            elif status_ownership == "forbidden":
                raise ProfileError(
                    f"{label} {status_field} is forbidden by the selected metadata profile"
                )
            elif not isinstance(status, str) or status not in allowed_statuses:
                raise ProfileError(f"{label} {status_field} must be registered")

        _deterministic_string_list(entry.get("parent_ids"), f"{label} parent_ids")
        _deterministic_string_list(
            entry.get("active_consumers"),
            f"{label} active_consumers",
            safe_paths=True,
        )

        replacement = entry.get("canonical_replacement")
        if replacement is not None:
            _non_empty_string(replacement, f"{label} canonical_replacement")
        if disposition in replacement_required and replacement is None:
            raise ProfileError(f"{label} canonical_replacement is required")
        if disposition in replacement_forbidden and replacement is not None:
            raise ProfileError(f"{label} canonical_replacement must be null")
        if disposition not in replacement_required | replacement_optional | replacement_forbidden:
            raise ProfileError(f"{label} disposition lacks replacement semantics")

        partition_plan = entry.get("partition_plan")
        if partition_plan is not None and not _canonical_partition_plan_path(
            partition_plan
        ):
            raise ProfileError(
                f"{label} partition_plan must be a canonical Spec Package Plan path"
            )

        preservation_class = entry.get("preservation_class")
        if preservation_class is not None and (
            not isinstance(preservation_class, str)
            or preservation_class not in preservation_classes
        ):
            raise ProfileError(f"{label} preservation_class must be registered")

        evidence = _require_exact_mapping(
            entry.get("evidence"), evidence_fields, f"{label} evidence"
        )
        evidence_lists = {
            field: _deterministic_string_list(
                evidence.get(field), f"{label} evidence.{field}"
            )
            for field in evidence_fields
        }
        review = _require_exact_mapping(
            entry.get("review_verdict"), review_fields, f"{label} review_verdict"
        )
        for field in review_fields:
            verdict = review.get(field)
            if not isinstance(verdict, str) or verdict not in verdict_values:
                raise ProfileError(f"{label} review_verdict values must be registered")

        if disposition in destructive:
            if preservation_class is None:
                raise ProfileError(f"{label} destructive row requires preservation_class")
            if not evidence_lists["consumer_scan"]:
                raise ProfileError(f"{label} consumer enumeration requires scan evidence")
            if any(not evidence_lists[field] for field in evidence_fields):
                raise ProfileError(f"{label} destructive evidence lists must not be empty")
            if review != {"specification": "pass", "quality": "pass"}:
                raise ProfileError(f"{label} destructive row requires pass/pass review")

    if source_paths != sorted(source_paths) or len(source_paths) != len(set(source_paths)):
        raise ProfileError("manifest entries must be uniquely ordered by source_path")


def validate_static_exception_document(
    document: object,
    contract: Mapping[str, object],
    known_finding_codes: Sequence[str] | set[str] | frozenset[str],
    validation_date: dt.date,
) -> None:
    """Validate bounded exceptions without reading repository or payload bytes."""

    if contract.get("exception_schema") != EXPECTED_EXCEPTION_SCHEMA:
        raise ProfileError("exception contract must use the exact bounded schema")
    if isinstance(validation_date, dt.datetime) or not isinstance(validation_date, dt.date):
        raise ProfileError("exception validation_date must be a date")
    known_codes = set(known_finding_codes)
    if not known_codes or not all(isinstance(code, str) and code for code in known_codes):
        raise ProfileError("known finding codes must be a non-empty string set")

    exception_document = _require_exact_mapping(
        document,
        EXPECTED_EXCEPTION_SCHEMA["top_level_fields"],
        "exception document",
    )
    if (
        type(exception_document.get("schema_version")) is not int
        or exception_document.get("schema_version") != 1
    ):
        raise ProfileError("exception schema_version must be the integer 1")
    exceptions = exception_document.get("exceptions")
    if not isinstance(exceptions, list):
        raise ProfileError("exceptions must be a list")

    bounded = EXPECTED_EXCEPTION_SCHEMA["bounded_semantics"]
    global_scopes = set(bounded["forbid_global_scopes"])
    ordering_keys: list[tuple[str, tuple[str, ...]]] = []
    for index, raw_exception in enumerate(exceptions):
        label = f"exception {index}"
        exception = _require_exact_mapping(
            raw_exception,
            EXPECTED_EXCEPTION_SCHEMA["entry_fields"],
            label,
        )
        finding_code = _non_empty_string(exception.get("finding_code"), f"{label} finding_code")
        if finding_code in global_scopes or finding_code not in known_codes:
            raise ProfileError(f"{label} finding_code must be a known specific code")

        scope_paths = _deterministic_string_list(
            exception.get("scope_paths"),
            f"{label} scope_paths",
            require_non_empty=True,
            safe_paths=True,
        )
        if any(path.lower() in global_scopes for path in scope_paths):
            raise ProfileError(f"{label} scope_paths must not be global")
        ordering_keys.append((finding_code, tuple(scope_paths)))

        for field in bounded["require_non_empty_text"]:
            _non_empty_string(exception.get(field), f"{label} {field}")

        approved_at = exception.get("approved_at")
        expires_on = exception.get("expires_on")
        if not isinstance(approved_at, str) or not _valid_iso_date(approved_at):
            raise ProfileError(f"{label} approved_at must be a strict ISO date")
        if not isinstance(expires_on, str) or not _valid_iso_date(expires_on):
            raise ProfileError(f"{label} expires_on must be a finite strict ISO date")
        approved_date = dt.date.fromisoformat(approved_at)
        expiry_date = dt.date.fromisoformat(expires_on)
        if approved_date > validation_date:
            raise ProfileError(f"{label} must already be approved")
        if expiry_date <= validation_date or expiry_date <= approved_date:
            raise ProfileError(f"{label} must be unexpired and time-bounded")

        _deterministic_string_list(
            exception.get("evidence"),
            f"{label} evidence",
            require_non_empty=True,
            safe_paths=True,
        )

    if ordering_keys != sorted(ordering_keys) or len(ordering_keys) != len(set(ordering_keys)):
        raise ProfileError("exceptions must be uniquely ordered by finding_code and scope_paths")








def _load_legacy_profiles(
    path: pathlib.Path = DEFAULT_PROFILES,
) -> dict[str, object]:
    """Load and structurally validate the typed metadata profile contract."""

    try:
        source = path.read_text(encoding="utf-8")
        loaded = _safe_load_unique(source)
    except (OSError, UnicodeError, yaml.YAMLError) as error:
        raise ProfileError(f"cannot load profile YAML: {error}") from error
    if not isinstance(loaded, dict):
        raise ProfileError("profile document must be a mapping")
    schema_version = loaded.get("schema_version")
    if type(schema_version) is not int or schema_version != 2:
        raise ProfileError("schema_version must be the integer 2")
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
        "archive_source_prefixes",
    )
    common_lists: dict[str, list[str]] = {}
    for key in common_list_names:
        value = common.get(key)
        if not isinstance(value, list) or not all(isinstance(item, str) and item for item in value):
            raise ProfileError(f"common.{key} must be a list of non-empty strings")
        if len(value) != len(set(value)):
            raise ProfileError(f"common.{key} must not contain duplicates")
        common_lists[key] = value
    if tuple(common_lists["archive_source_prefixes"]) != EXPECTED_ARCHIVE_SOURCE_PREFIXES:
        raise ProfileError(
            "common.archive_source_prefixes must define the exact historical archive source roots"
        )
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
    generated_outputs = common.get("generated_outputs")
    if not isinstance(generated_outputs, dict) or not generated_outputs:
        raise ProfileError("common.generated_outputs must be a non-empty exact-path-to-generator mapping")
    for output_path, owner in generated_outputs.items():
        normalized_output = (
            _normalized_target_path(output_path) if isinstance(output_path, str) else None
        )
        generated_package_readme = bool(
            isinstance(output_path, str)
            and re.fullmatch(
                r"docs/90\.references/data/[0-9]{4}-[a-z0-9][a-z0-9-]*/README\.md",
                output_path,
            )
        )
        if (
            normalized_output is None
            or (normalized_output.name == "README.md" and not generated_package_readme)
            or any(character in output_path for character in "*?[]")
        ):
            raise ProfileError(
                "common.generated_outputs keys must be exact canonical target Markdown paths"
            )
        if not _safe_repo_path(owner, "scripts/"):
            raise ProfileError(
                "common.generated_outputs values must be safe canonical scripts/ generator paths"
            )
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
        if name == "archive":
            archive_profile_keys = {
                "required",
                "optional",
                "forbidden",
                "allowed_statuses",
                "allowed_parent_types",
                "allow_empty_parents",
                "disposition",
                "conditions",
            }
            if set(raw_profile) != archive_profile_keys:
                raise ProfileError("profile archive must define the exact v2 contract members")
            if tuple(raw_profile.get("required", ())) != EXPECTED_ARCHIVE_REQUIRED:
                raise ProfileError("profile archive required must define the exact v2 fields")
            if tuple(raw_profile.get("optional", ())) != EXPECTED_ARCHIVE_OPTIONAL:
                raise ProfileError("profile archive optional must define the exact v2 fields")
            if raw_profile.get("conditions") != EXPECTED_ARCHIVE_CONDITIONS:
                raise ProfileError("profile archive conditions must define the exact v2 rules")
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

    archive_profiles = loaded.get("archive_profiles")
    if (
        not isinstance(archive_profiles, dict)
        or tuple(archive_profiles) != EXPECTED_ARCHIVE_PROFILE_NAMES
    ):
        raise ProfileError("archive_profiles must define the exact ordered semantic selectors")
    declared_archive_globs: list[tuple[str, str]] = []
    for profile_name, archive_profile in archive_profiles.items():
        if not isinstance(archive_profile, dict) or set(archive_profile) != ARCHIVE_PROFILE_KEYS:
            raise ProfileError(
                f"archive profile {profile_name} must define the exact contract members"
            )
        path_globs = archive_profile.get("path_globs")
        if not isinstance(path_globs, list) or not path_globs or not all(
            _safe_target_glob(pattern) for pattern in path_globs
        ):
            raise ProfileError(
                f"archive profile {profile_name} path_globs must be safe Markdown patterns"
            )
        if len(path_globs) != len(set(path_globs)):
            raise ProfileError(f"archive profile {profile_name} path_globs must be unique")
        for pattern in path_globs:
            for other_name, other_pattern in declared_archive_globs:
                witness = _target_glob_intersection_witness(other_pattern, pattern)
                if witness is not None:
                    raise ProfileError(
                        "archive profile globs overlap: "
                        f"{other_name}:{other_pattern} and {profile_name}:{pattern}"
                    )
            declared_archive_globs.append((profile_name, pattern))
        template = archive_profile.get("template")
        if (
            not isinstance(template, str)
            or not _safe_repo_path(template, "docs/99.templates/templates/common/")
            or not template.endswith(".template.md")
        ):
            raise ProfileError(f"archive profile {profile_name} template must be canonical")
        if archive_profile.get("artifact_type") != "archive":
            raise ProfileError(f"archive profile {profile_name} must keep semantic archive type")
        id_pattern = archive_profile.get("id_pattern")
        if not isinstance(id_pattern, str) or not id_pattern:
            raise ProfileError(f"archive profile {profile_name} id_pattern must be a non-empty regex")
        try:
            re.compile(id_pattern)
        except re.error as error:
            raise ProfileError(
                f"archive profile {profile_name} id_pattern must compile"
            ) from error
        path_identity = archive_profile.get("path_identity")
        identity_fields = (
            "parent_id_pattern",
            "artifact_id_identity_pattern",
            "identity_capture",
        )
        if path_identity == "direct":
            if any(archive_profile.get(field) is not None for field in identity_fields):
                raise ProfileError(
                    f"archive profile {profile_name} direct identity must not define correlation fields"
                )
        elif path_identity == "inherited":
            if not all(
                isinstance(archive_profile.get(field), str)
                and archive_profile[field]
                for field in identity_fields
            ):
                raise ProfileError(
                    f"archive profile {profile_name} inherited identity requires exact correlation fields"
                )
            try:
                parent_pattern = re.compile(archive_profile["parent_id_pattern"])
                artifact_pattern = re.compile(
                    archive_profile["artifact_id_identity_pattern"]
                )
            except re.error as error:
                raise ProfileError(
                    f"archive profile {profile_name} correlation patterns must compile"
                ) from error
            capture = archive_profile["identity_capture"]
            if capture not in parent_pattern.groupindex or capture not in artifact_pattern.groupindex:
                raise ProfileError(
                    f"archive profile {profile_name} correlation patterns must expose identity_capture"
                )
        else:
            raise ProfileError(
                f"archive profile {profile_name} path_identity must be direct or inherited"
            )
        for group in ("required", "optional", "forbidden"):
            values = archive_profile.get(group)
            if not isinstance(values, list) or not all(
                isinstance(value, str) and value for value in values
            ) or len(values) != len(set(values)):
                raise ProfileError(f"archive profile {profile_name} {group} must be a unique string list")
        ownership = [set(archive_profile[group]) for group in ("required", "optional", "forbidden")]
        if any(ownership[left] & ownership[right] for left, right in ((0, 1), (0, 2), (1, 2))):
            raise ProfileError(f"archive profile {profile_name} field ownership must not overlap")
        for inherited in ("allowed_statuses", "allow_empty_parents", "disposition"):
            if archive_profile.get(inherited) != profile_map["archive"].get(inherited):
                raise ProfileError(
                    f"archive profile {profile_name} must preserve archive {inherited} semantics"
                )
        conditions = archive_profile.get("conditions")
        if not isinstance(conditions, dict) or set(conditions) != {"replacement", "snapshot"}:
            raise ProfileError(f"archive profile {profile_name} conditions are invalid")

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
        raise ProfileError("template_roles must define the exact canonical role names")
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


def load_profiles(
    path: pathlib.Path = DEFAULT_PROFILES,
) -> Mapping[str, Mapping[str, object]] | dict[str, object]:
    """Return the Registry profile map; accept legacy YAML only as transition input."""

    if path.suffix.lower() == ".json":
        try:
            return load_registry(path).profiles
        except RegistryError as error:
            raise ProfileError(str(error)) from error
    return _load_legacy_profiles(path)


def build_registry_profiles(registry: DocumentRegistry) -> dict[str, object]:
    """Project only current Registry profiles into the metadata reader envelope."""

    keys = list(dict.fromkeys(
        key
        for profile in registry.profiles.values()
        for field in ("required_frontmatter", "optional_frontmatter")
        for key in profile.get(field, ())
    ))
    profiles = build_registry_transition_profiles(registry, {
        "common": {"typed_keys": keys, "frontmatter_order": []},
        "profiles": {},
        "template_roles": {},
        "document_families": {"sdlc": []},
    })
    del profiles["_legacy_profiles"]
    return profiles


def build_registry_transition_profiles(
    registry: DocumentRegistry,
    legacy_profiles: Mapping[str, object],
) -> dict[str, object]:
    """Adapt Registry profiles over the bounded legacy corpus envelope.

    The legacy YAML remains an explicit migration input until Task 3 moves the
    corpus. Canonical target routes are classified and validated by Registry;
    old routes retain their pre-migration profiles without becoming a second
    authority for new paths.
    """

    adapted = copy.deepcopy(dict(legacy_profiles))
    legacy_map = adapted.get("profiles")
    common = adapted.get("common")
    if not isinstance(legacy_map, dict) or not isinstance(common, dict):
        raise ProfileError("legacy transition profiles require common and profiles")
    for key in ("typed_keys", "frontmatter_order"):
        values = common.get(key)
        if isinstance(values, list) and "type" not in values:
            common[key] = ["type", *values]
    translated = dict(legacy_map)
    legacy_spec = translated.get("spec")
    if isinstance(legacy_spec, dict):
        legacy_spec = copy.deepcopy(legacy_spec)
        optional = legacy_spec.get("optional")
        if isinstance(optional, list) and "superseded_by" not in optional:
            legacy_spec["optional"] = [*optional, "superseded_by"]
        translated["spec"] = legacy_spec
        legacy_map["spec"] = copy.deepcopy(legacy_spec)
    for profile_id, profile in registry.profiles.items():
        lifecycle_id = profile.get("lifecycle_id")
        statuses = (
            list(registry.lifecycles[lifecycle_id])
            if isinstance(lifecycle_id, str) and lifecycle_id in registry.lifecycles
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
                for status, targets in registry.transitions.get(
                    profile_id, {}
                ).items()
            }
            if profile_id in registry.transitions
            else {}
        )
        translated[profile_id] = {
            "type": profile.get("type"),
            "required": list(profile.get("required_frontmatter", ())),
            "optional": list(profile.get("optional_frontmatter", ())),
            "forbidden": [],
            "allowed_statuses": statuses,
            "allowed_parent_types": parents,
            "allow_empty_parents": (
                profile_id in {"research", "audit", "data"}
                or profile.get("identity_relation") == "subject-member"
                or not parents
            ),
            "allow_additional": False,
            "disposition": "registry-canonical",
            "path_pattern": profile.get("path_pattern"),
            "artifact_id_pattern": profile.get("artifact_id_pattern"),
            "identity_relation": profile.get("identity_relation"),
            "transitions": transitions,
        }
    adapted["profiles"] = translated
    adapted["_legacy_profiles"] = copy.deepcopy(legacy_map)
    legacy_roles = adapted.get("template_roles")
    projected_roles = dict(legacy_roles) if isinstance(legacy_roles, dict) else {}
    for role_id, role in registry.template_roles.items():
        profile_id = role.get("profile_id")
        profile = registry.profiles.get(str(profile_id))
        path_pattern = profile.get("path_pattern") if isinstance(profile, Mapping) else None
        if not isinstance(profile, Mapping) or not isinstance(path_pattern, str):
            continue
        additional_paths = profile.get("additional_paths", ())
        target_patterns = [path_pattern]
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
    families = adapted.get("document_families")
    if isinstance(families, dict):
        existing = [
            member
            for members in families.values()
            if isinstance(members, list)
            for member in members
            if isinstance(member, str)
        ]
        canonical = [
            profile_id
            for profile_id in registry.profiles
            if profile_id
            not in {
                "readme",
                "governance",
                "template-source",
                "generated",
                "repo-support",
                "unsupported",
            }
            and profile_id not in existing
        ]
        sdlc = families.get("sdlc")
        if isinstance(sdlc, list):
            families["sdlc"] = [*sdlc, *canonical]
    adapted["_registry"] = registry
    return adapted


def _registry_path_glob(pattern: str) -> str:
    rendered = re.sub(r"\{[^{}]+:4\}", "[0-9][0-9][0-9][0-9]", pattern)
    return re.sub(r"\{(?:slug|domain|stage)\}", "*", rendered)



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
