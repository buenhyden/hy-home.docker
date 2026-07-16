#!/usr/bin/env python3
"""Load and validate the typed Stage 00 agent-governance contracts."""

from __future__ import annotations

import datetime as dt
import errno
import fnmatch
import importlib.util
import json
import os
import pathlib
import re
import secrets
import stat
import sys
import tomllib
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from types import MappingProxyType
from urllib.parse import urlparse

import yaml

try:
    from markdown_it import MarkdownIt as _MarkdownIt
except ModuleNotFoundError:  # pragma: no cover - exercised through dependency guard
    _MarkdownIt = None  # type: ignore[misc,assignment]

try:
    import html5lib as _html5lib
except ModuleNotFoundError:  # pragma: no cover - exercised through dependency guard
    _html5lib = None  # type: ignore[assignment]


_OPEN_SUPPORTS_DIR_FD = os.open in os.supports_dir_fd


CONTRACT_RELATIVE_PATHS = MappingProxyType(
    {
        "artifacts": pathlib.PurePosixPath(
            "docs/00.agent-governance/contracts/agent-governance-artifacts.yaml"
        ),
        "catalog": pathlib.PurePosixPath(
            "docs/00.agent-governance/contracts/agent-catalog.yaml"
        ),
        "providers": pathlib.PurePosixPath(
            "docs/00.agent-governance/contracts/provider-models.yaml"
        ),
    }
)

EXPECTED_AGENT_COUNT = 14
EXPECTED_FUNCTION_COUNT = 22
EXPECTED_PROVIDER_COUNT = 3
MAX_BRACE_GROUPS = 64
MAX_EXPANDED_PATHS = 1024
MAX_PATTERN_LENGTH = 4096

COMMON_TOP_FIELDS = {"schema_version", "checked_at"}
ARTIFACT_TOP_FIELDS = COMMON_TOP_FIELDS | {
    "artifacts",
    "governed_families",
    "path_pattern_limits",
    "root_shims",
    "readme_profiles",
    "path_authority",
}
CATALOG_TOP_FIELDS = COMMON_TOP_FIELDS | {
    "projection_targets",
    "scopes",
    "permissions",
    "agents",
    "functions",
    "role_transfers",
    "capability_intake",
    "evaluation",
}
PROVIDER_TOP_FIELDS = {
    "schema_version",
    "cutoff_at",
    "retrieved_at",
    "providers",
    "compatibility_surfaces",
    "work_profiles",
    "fallback_approvals",
    "cutoff_evidence",
    "models",
    "harness_loops",
    "semantic_events",
}

ARTIFACT_FIELDS = {
    "profile_id",
    "artifact_type",
    "path_pattern",
    "repository_section",
    "canonical",
    "required_keys",
    "key_order",
    "required_sections",
    "expected_values",
}
GOVERNED_FAMILY_FIELDS = {
    "family_id",
    "path_pattern",
    "repository_sections",
}
PATH_PATTERN_LIMIT_FIELDS = {
    "max_brace_groups",
    "max_expanded_paths",
    "max_pattern_length",
}
ROOT_SHIM_FIELDS = {
    "path",
    "provider",
    "bootstrap_target",
    "provider_target",
    "memory_targets",
    "import_style",
    "frontmatter",
}
README_PROFILE_FIELDS = {
    "profile_id",
    "path_pattern",
    "required_sections",
    "allowed_sections",
    "forbidden_policy_topics",
}
AUTHORITY_FIELDS = {
    "authority_id",
    "path_patterns",
    "canonical_owner",
    "entry_owners",
    "permitted_contributors",
    "mandatory_reviewers",
    "entry_reviewers",
    "protected",
    "validators",
    "rollback",
}
ENTRY_AUTHORITY_FIELDS = {
    "authority_role",
    "catalog_collection",
    "identity_field",
    "agent_field",
}
PERMISSION_FIELDS = {"permission_id", "mutation_allowed", "evidence_required"}
AGENT_FIELDS = {
    "agent_id",
    "category",
    "scope",
    "tier",
    "status",
    "catalog_path",
    "permission_profile",
    "work_profile",
    "function_ids",
    "provider_projections",
}
FUNCTION_FIELDS = {
    "function_id",
    "scope",
    "status",
    "catalog_path",
    "owner_agent",
    "reviewer_agents",
    "inputs",
    "outputs",
    "gates",
    "provider_projections",
}
ROLE_TRANSFER_FIELDS = {
    "retired_agent_id",
    "status",
    "successor_agent_ids",
    "successor_function_ids",
    "rationale",
}
CAPABILITY_INTAKE_FIELDS = {
    "capability_id",
    "source",
    "source_url",
    "decision",
    "owner_agent",
    "evaluation_function",
}
EVALUATION_FIELDS = {
    "owner_agent",
    "reviewer_agent",
    "fixture_catalog_path",
    "scorer_path",
    "runner_path",
    "test_path",
    "fixture_count",
    "regression_count",
    "input_classification",
    "input_roots",
    "pass_markers",
    "fixture_thresholds",
}
PROVIDER_FIELDS = {
    "provider_id",
    "capability_status",
    "adoption_status",
    "native_agent_pattern",
    "native_config_path",
    "native_skill_pattern",
    "canonical_skill_source_pattern",
    "source_url",
    "hook_source_url",
    "local_cli_version",
    "local_cli_observation",
    "local_runtime_acceptance",
}
COMPATIBILITY_FIELDS = {
    "surface_id",
    "path_pattern",
    "status",
    "consumers",
    "source_url",
}
WORK_PROFILE_FIELDS = {"profile_id", "description", "defaults"}
WORK_PROFILE_DEFAULT_REASONING_FIELDS = {"provider", "model_id", "reasoning"}
WORK_PROFILE_DEFAULT_CLAUDE_FIELDS = {"provider", "model_id", "effort"}
FALLBACK_APPROVAL_FIELDS = {
    "approval_id",
    "provider",
    "source_model_id",
    "target_model_id",
    "work_profiles",
    "reference",
}
CUTOFF_EVIDENCE_FIELDS = {
    "evidence_id",
    "provider",
    "source_url",
    "published_at",
    "observed_at",
}
MODEL_COMMON_FIELDS = {
    "provider",
    "model_id",
    "canonical_model_id",
    "provider_status",
    "normalized_status",
    "repository_default_eligible",
    "entitlement",
    "runtime_acceptance",
    "work_profiles",
    "agent_coding_fit",
    "task_characteristics",
    "fallback",
    "fallback_policy",
    "fallback_approval",
    "cutoff_evidence_status",
    "cutoff_evidence_id",
    "checked_at",
    "source_url",
}
MODEL_REASONING_FIELDS = MODEL_COMMON_FIELDS | {
    "reasoning_control_kind",
    "supported_reasoning_controls",
    "repository_reasoning_controls",
}
MODEL_CLAUDE_FIELDS = MODEL_COMMON_FIELDS | {
    "thinking_control_kind",
    "supported_thinking_controls",
    "repository_thinking_controls",
    "supported_effort_controls",
    "repository_effort_controls",
}
EVENT_FIELDS = {"event_id", "required", "provider_bindings"}
HARNESS_LOOP_FIELDS = {
    "event_id",
    "owner_agent",
    "reviewer_agent",
    "permission_profile",
    "allowed_tools",
    "max_attempts",
    "stop_condition",
    "on_failure",
    "evidence_fields",
    "prohibited_evidence",
    "capability_status",
    "adoption_status",
    "runtime_depth",
}
EVENT_BINDING_FIELDS = {
    "provider",
    "native_event",
    "capability_status",
    "adoption_status",
    "runtime_depth",
    "provider_can_block",
    "repository_hook_mode",
    "timeout_unit",
    "timeout_value",
}

PROVIDER_CAPABILITY_STATES = {"supported", "unsupported", "needs_revalidation"}
PROVIDER_ADOPTION_STATES = {
    "adopted",
    "deferred",
    "not_applicable",
    "partial",
    "planned",
}
MODEL_STATES = {
    "active",
    "current",
    "deprecated",
    "generally-available",
    "limited-availability",
    "listed",
    "preview",
    "stable",
}
NORMALIZED_MODEL_STATES = {
    "current",
    "deprecated",
    "limited",
    "preview",
    "stable",
    "unclassified-listed",
}
ENTITLEMENT_STATES = {"available", "needs_revalidation", "unavailable"}
RUNTIME_ACCEPTANCE_STATES = {"accepted", "needs_revalidation", "rejected"}
AGENT_CATEGORIES = {"implementation-operations", "review-evaluation", "supervisor"}
AGENT_TIERS = {"supervisor", "worker"}
AGENT_STATUSES = {"active", "retired"}
CAPABILITY_DECISIONS = {"adopt", "defer", "merge", "reject"}
TIMEOUT_UNITS = {"milliseconds", "seconds"}
LOCAL_CLI_OBSERVATIONS = {"observed", "unavailable"}
REASONING_CONTROL_KINDS = {
    "adaptive",
    "adaptive-always-on",
    "adaptive-default",
    "effort",
    "extended-thinking",
    "reasoning-effort",
    "thinking-level",
    "unverified",
}
AGENT_CODING_FITS = {"bounded", "exceptional", "historical", "strong"}
CUTOFF_EVIDENCE_STATES = {"historical-state-unverified", "verified-before-cutoff"}
FALLBACK_POLICIES = {"approved-degraded", "same-profile"}
REPOSITORY_HOOK_MODES = {
    "advisory",
    "blocking",
    "deny-retry",
    "retry",
    "unsupported",
}
RUNTIME_DEPTH_STATES = {
    "configured-not-executed",
    "repository-enforced",
    "runtime-validated",
    "unsupported",
}
LOOP_PERMISSION_TOOLS = MappingProxyType(
    {
        "read-only": frozenset({"focused-validation", "read", "search"}),
        "workspace-write": frozenset(
            {
                "controlled-qa-wrapper",
                "focused-validation",
                "read",
                "search",
                "workspace-edit",
            }
        ),
    }
)
EXPECTED_HARNESS_LOOPS = MappingProxyType(
    {
        "approved-all-files-gate": (1, "controlled-wrapper-pass", "record_and_stop"),
        "bounded-implementation-loop": (
            2,
            "focused-checks-pass",
            "narrow_then_escalate",
        ),
        "context-bootstrap": (1, "bootstrap-contract-pass", "escalate"),
        "independent-review-loop": (2, "critical_and_important_zero", "escalate"),
    }
)
SANITIZED_EVIDENCE_FIELDS = (
    "command",
    "result",
    "rollback",
    "skipped_checks",
)
PROHIBITED_EVIDENCE_FIELDS = (
    "auth_files",
    "credentials",
    "raw_logs",
    "secret_values",
    "shell_history",
    "tokens",
)
FALLBACK_APPROVAL_REFERENCE = (
    "docs/03.specs/132-agent-governance-harness-convergence/"
    "spec.md#approved-fallback-edges"
)
PROVIDER_OFFICIAL_EVIDENCE_HOSTS = MappingProxyType(
    {
        "claude": frozenset({"platform.claude.com"}),
        "codex": frozenset({"developers.openai.com", "learn.chatgpt.com"}),
        "gemini": frozenset({"ai.google.dev"}),
    }
)
EXPECTED_REPOSITORY_HOOK_MODES = MappingProxyType(
    {
        ("post-tool", "claude"): "advisory",
        ("post-tool", "codex"): "advisory",
        ("post-tool", "gemini"): "advisory",
        ("pre-compaction", "claude"): "advisory",
        ("pre-compaction", "codex"): "advisory",
        ("pre-compaction", "gemini"): "advisory",
        ("pre-tool", "claude"): "advisory",
        ("pre-tool", "codex"): "advisory",
        ("pre-tool", "gemini"): "advisory",
        ("session-end", "claude"): "advisory",
        ("session-end", "codex"): "unsupported",
        ("session-end", "gemini"): "advisory",
        ("session-start", "claude"): "advisory",
        ("session-start", "codex"): "advisory",
        ("session-start", "gemini"): "advisory",
        ("stop", "claude"): "blocking",
        ("stop", "codex"): "retry",
        ("stop", "gemini"): "deny-retry",
        ("user-prompt-intake", "claude"): "advisory",
        ("user-prompt-intake", "codex"): "advisory",
        ("user-prompt-intake", "gemini"): "advisory",
    }
)

DOMAIN_OWNER_REFERENCE_FIELDS = MappingProxyType(
    {
        "agents": ("agent_id", "agent_id"),
        "functions": ("function_id", "owner_agent"),
    }
)
CATALOG_AUTHORITY_SEMANTICS = MappingProxyType(
    {
        "agent-function-catalog": MappingProxyType(
            {
                "canonical_owner": "skill-creator",
                "mandatory_reviewers": (),
                "entry_owners": (),
                "entry_reviewers": (
                    ("domain-owner", "functions", "function_id", "owner_agent"),
                ),
            }
        ),
        "agent-role-catalog": MappingProxyType(
            {
                "canonical_owner": "rules-engineer",
                "mandatory_reviewers": ("workflow-supervisor",),
                "entry_owners": (("domain-owner", "agents", "agent_id", "agent_id"),),
                "entry_reviewers": (),
            }
        ),
    }
)


@dataclass(frozen=True)
class Finding:
    code: str
    path: str
    location: str
    expected: str
    actual: str
    source: str


@dataclass(frozen=True)
class ContractBundle:
    artifacts: Mapping[str, object]
    catalog: Mapping[str, object]
    providers: Mapping[str, object]


class ContractLoadError(Exception):
    """A normalized, value-free contract loading failure."""

    def __init__(self, code: str, path: str, location: str) -> None:
        self.code = code
        self.path = path
        self.location = location
        super().__init__(f"{code} path={path} location={location}")


class _DuplicateKeyError(yaml.YAMLError):
    def __init__(self, line: int) -> None:
        self.line = line
        super().__init__("duplicate mapping key")


class _NonStringKeyError(yaml.YAMLError):
    def __init__(self, line: int) -> None:
        self.line = line
        super().__init__("non-string mapping key")


class _UnsafeRootFileError(Exception):
    """A repository file failed the root-confined regular-file boundary."""


class _UniqueKeyLoader(yaml.SafeLoader):
    pass


def _construct_unique_mapping(
    loader: _UniqueKeyLoader, node: yaml.nodes.MappingNode, deep: bool = False
) -> dict[object, object]:
    mapping: dict[object, object] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if not isinstance(key, str):
            raise _NonStringKeyError(key_node.start_mark.line + 1)
        duplicate = key in mapping
        if duplicate:
            raise _DuplicateKeyError(key_node.start_mark.line + 1)
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


_UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_unique_mapping,
)


def _freeze(value: object) -> object:
    if isinstance(value, Mapping):
        return MappingProxyType({key: _freeze(item) for key, item in value.items()})
    if isinstance(value, list | tuple):
        return tuple(_freeze(item) for item in value)
    return value


def _read_root_confined_regular_text(
    root: pathlib.Path, relative_path: pathlib.PurePosixPath
) -> str:
    required_flags = ("O_DIRECTORY", "O_NOFOLLOW", "O_NONBLOCK")
    if any(not hasattr(os, name) for name in required_flags):
        raise _UnsafeRootFileError
    if not _OPEN_SUPPORTS_DIR_FD:
        raise _UnsafeRootFileError
    if (
        relative_path.is_absolute()
        or not relative_path.parts
        or any(part in {"", ".", ".."} for part in relative_path.parts)
    ):
        raise _UnsafeRootFileError

    directory_flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    final_flags = os.O_RDONLY | os.O_NONBLOCK | os.O_NOFOLLOW
    close_on_exec = getattr(os, "O_CLOEXEC", 0)
    directory_flags |= close_on_exec
    final_flags |= close_on_exec
    descriptors: list[int] = []

    def open_component(
        component: os.PathLike[str] | str,
        flags: int,
        *,
        dir_fd: int | None = None,
    ) -> int:
        try:
            descriptor = os.open(component, flags, dir_fd=dir_fd)
        except OSError as error:
            if error.errno in {errno.ELOOP, errno.ENOTDIR, errno.ENXIO}:
                raise _UnsafeRootFileError from error
            raise
        descriptors.append(descriptor)
        return descriptor

    try:
        current = open_component(root, directory_flags)
        for part in relative_path.parts[:-1]:
            current = open_component(part, directory_flags, dir_fd=current)
        final = open_component(relative_path.parts[-1], final_flags, dir_fd=current)
        if not stat.S_ISREG(os.fstat(final).st_mode):
            raise _UnsafeRootFileError
        chunks: list[bytes] = []
        while True:
            chunk = os.read(final, 64 * 1024)
            if not chunk:
                break
            chunks.append(chunk)
        return b"".join(chunks).decode("utf-8")
    finally:
        for descriptor in reversed(descriptors):
            try:
                os.close(descriptor)
            except OSError:
                pass


def _load_yaml(
    root: pathlib.Path, relative_path: pathlib.PurePosixPath
) -> Mapping[str, object]:
    relative_text = relative_path.as_posix()
    try:
        text = _read_root_confined_regular_text(root, relative_path)
    except FileNotFoundError as error:
        raise ContractLoadError(
            "AGC-CONTRACT-MISSING", relative_text, "file"
        ) from error
    except _UnsafeRootFileError as error:
        raise ContractLoadError(
            "AGC-CONTRACT-UNSAFE-FILE", relative_text, "file"
        ) from error
    except UnicodeError as error:
        raise ContractLoadError(
            "AGC-CONTRACT-ENCODING", relative_text, "file"
        ) from error
    except OSError as error:
        raise ContractLoadError("AGC-CONTRACT-READ", relative_text, "file") from error
    try:
        value = yaml.load(text, Loader=_UniqueKeyLoader)
    except _DuplicateKeyError as error:
        raise ContractLoadError(
            "AGC-YAML-DUPLICATE-KEY", relative_text, f"line:{error.line}"
        ) from error
    except _NonStringKeyError as error:
        raise ContractLoadError(
            "AGC-YAML-NONSTRING-KEY", relative_text, f"line:{error.line}"
        ) from error
    except yaml.YAMLError as error:
        raise ContractLoadError("AGC-YAML-MALFORMED", relative_text, "yaml") from error
    if not isinstance(value, Mapping):
        raise ContractLoadError("AGC-YAML-NOT-MAPPING", relative_text, "root")
    return _freeze(value)  # type: ignore[return-value]


def load_artifact_contract(
    root: pathlib.Path, contract_path: pathlib.Path
) -> Mapping[str, object]:
    """Load one arbitrary artifact registry through the confined YAML boundary."""

    root_absolute = root.absolute()
    candidate = contract_path
    try:
        if candidate.is_absolute():
            relative = candidate.absolute().relative_to(root_absolute)
        else:
            relative = candidate
        relative_path = pathlib.PurePosixPath(relative.as_posix())
        if (
            relative_path.is_absolute()
            or not relative_path.parts
            or any(part in {"", ".", ".."} for part in relative_path.parts)
        ):
            raise ValueError
    except (OSError, ValueError) as error:
        raise ContractLoadError(
            "AGC-CONTRACT-UNSAFE-FILE", "artifact-contract", "file"
        ) from error
    try:
        return _load_yaml(root_absolute, relative_path)
    except ContractLoadError as error:
        raise ContractLoadError(
            error.code, "artifact-contract", error.location
        ) from error


def load_contract_bundle(root: pathlib.Path) -> ContractBundle:
    """Load the three fixed Stage 00 contract files beneath ``root``."""

    if _MarkdownIt is None:
        raise ContractLoadError(
            "AGC-DEPENDENCY-MISSING", "markdown-it-py", "validation-runtime"
        )
    if _html5lib is None:
        raise ContractLoadError(
            "AGC-DEPENDENCY-MISSING", "html5lib", "validation-runtime"
        )
    loaded: dict[str, Mapping[str, object]] = {}
    for key, relative in CONTRACT_RELATIVE_PATHS.items():
        loaded[key] = _load_yaml(root, relative)
    return ContractBundle(
        artifacts=loaded["artifacts"],
        catalog=loaded["catalog"],
        providers=loaded["providers"],
    )


def finding_sort_key(finding: Finding) -> tuple[str, str, str, str, str, str]:
    return (
        finding.path,
        finding.location,
        finding.code,
        finding.expected,
        finding.actual,
        finding.source,
    )


def _add(
    findings: list[Finding],
    code: str,
    path: str,
    location: str,
    expected: str,
    actual: str,
    source: str,
) -> None:
    findings.append(Finding(code, path, location, expected, actual, source))


def _check_fields(
    value: object,
    expected: set[str],
    path: str,
    location: str,
    findings: list[Finding],
    source: str,
) -> Mapping[str, object] | None:
    if not isinstance(value, Mapping):
        _add(
            findings,
            "AGC-SCHEMA-TYPE",
            path,
            location,
            "mapping",
            "non-mapping",
            source,
        )
        return None
    keys = {str(key) for key in value}
    for key in sorted(expected - keys):
        _add(
            findings,
            "AGC-SCHEMA-MISSING-FIELD",
            path,
            f"{location}.{key}",
            "required-field",
            "missing-field",
            source,
        )
    for key in sorted(keys - expected):
        _add(
            findings,
            "AGC-SCHEMA-UNKNOWN-FIELD",
            path,
            f"{location}.{key}",
            "registered-field",
            "unknown-field",
            source,
        )
    return value


def _as_sequence(
    value: object,
    path: str,
    location: str,
    findings: list[Finding],
    source: str,
) -> Sequence[object] | None:
    if isinstance(value, Sequence) and not isinstance(value, str | bytes):
        return value
    _add(
        findings,
        "AGC-SCHEMA-TYPE",
        path,
        location,
        "list",
        "non-list",
        source,
    )
    return None


def _sequence_or_empty(value: object) -> Sequence[object]:
    """Return only a validated collection shape for downstream reads."""

    if isinstance(value, Sequence) and not isinstance(value, str | bytes):
        return value
    return ()


def _is_registered_string(value: object, registered: Sequence[str] | set[str]) -> bool:
    """Check a reference without hashing an unvalidated scalar."""

    return isinstance(value, str) and value in registered


def _is_nonempty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _is_bool(value: object) -> bool:
    return type(value) is bool


def _check_string(
    value: object,
    path: str,
    location: str,
    findings: list[Finding],
    source: str,
) -> bool:
    if _is_nonempty_string(value):
        return True
    _add(
        findings,
        "AGC-SCHEMA-TYPE",
        path,
        location,
        "non-empty-string",
        "invalid-string",
        source,
    )
    return False


def _check_enum(
    value: object,
    allowed: set[str],
    path: str,
    location: str,
    findings: list[Finding],
    source: str,
    code: str = "AGC-SCHEMA-INVALID-ENUM",
) -> bool:
    if isinstance(value, str) and value in allowed:
        return True
    _add(findings, code, path, location, "allowed-enum", "invalid-enum", source)
    return False


def _check_bool(
    value: object,
    path: str,
    location: str,
    findings: list[Finding],
    source: str,
) -> bool:
    if _is_bool(value):
        return True
    _add(findings, "AGC-SCHEMA-TYPE", path, location, "boolean", "non-boolean", source)
    return False


def _check_string_list(
    value: object,
    path: str,
    location: str,
    findings: list[Finding],
    source: str,
    *,
    allow_empty: bool = False,
    require_sorted: bool = False,
) -> tuple[str, ...] | None:
    sequence = _as_sequence(value, path, location, findings, source)
    if sequence is None:
        return None
    if not allow_empty and not sequence:
        _add(
            findings,
            "AGC-SCHEMA-EMPTY-LIST",
            path,
            location,
            "non-empty-list",
            "empty-list",
            source,
        )
    strings: list[str] = []
    for index, item in enumerate(sequence):
        if _check_string(item, path, f"{location}[{index}]", findings, source):
            strings.append(item)  # type: ignore[arg-type]
    if len(strings) != len(set(strings)):
        _add(
            findings,
            "AGC-SCHEMA-DUPLICATE-LIST-VALUE",
            path,
            location,
            "unique-list",
            "duplicate-list-value",
            source,
        )
    if require_sorted and strings != sorted(strings):
        _add(
            findings,
            "AGC-SCHEMA-NONDETERMINISTIC-ORDER",
            path,
            location,
            "lexicographic-order",
            "non-lexicographic-order",
            source,
        )
    return tuple(strings)


def _check_entry_authority_list(
    value: object,
    path: str,
    location: str,
    findings: list[Finding],
    source: str,
) -> tuple[tuple[str, str, str, str], ...]:
    sequence = _as_sequence(value, path, location, findings, source)
    if sequence is None:
        return ()
    references: list[tuple[str, str, str, str]] = []
    for index, raw in enumerate(sequence):
        entry_location = f"{location}[{index}]"
        entry = _check_fields(
            raw,
            ENTRY_AUTHORITY_FIELDS,
            path,
            entry_location,
            findings,
            source,
        )
        if entry is None:
            continue
        role = entry.get("authority_role")
        collection = entry.get("catalog_collection")
        identity_field = entry.get("identity_field")
        agent_field = entry.get("agent_field")
        role_valid = _check_enum(
            role,
            {"domain-owner"},
            path,
            f"{entry_location}.authority_role",
            findings,
            source,
        )
        collection_valid = _check_enum(
            collection,
            set(DOMAIN_OWNER_REFERENCE_FIELDS),
            path,
            f"{entry_location}.catalog_collection",
            findings,
            source,
        )
        identity_valid = _check_string(
            identity_field,
            path,
            f"{entry_location}.identity_field",
            findings,
            source,
        )
        agent_valid = _check_string(
            agent_field,
            path,
            f"{entry_location}.agent_field",
            findings,
            source,
        )
        reference_fields_valid = True
        if collection_valid:
            expected_identity, expected_agent = DOMAIN_OWNER_REFERENCE_FIELDS[
                str(collection)
            ]
            if identity_field != expected_identity:
                reference_fields_valid = False
                _add(
                    findings,
                    "AGC-AUTHORITY-REFERENCE",
                    path,
                    f"{entry_location}.identity_field",
                    "catalog-identity-field",
                    "invalid-identity-field",
                    source,
                )
            if agent_field != expected_agent:
                reference_fields_valid = False
                _add(
                    findings,
                    "AGC-AUTHORITY-REFERENCE",
                    path,
                    f"{entry_location}.agent_field",
                    "catalog-agent-reference-field",
                    "invalid-agent-reference-field",
                    source,
                )
        if all(
            (
                role_valid,
                collection_valid,
                identity_valid,
                agent_valid,
                reference_fields_valid,
            )
        ):
            references.append(
                (str(role), str(collection), str(identity_field), str(agent_field))
            )
    if len(references) != len(set(references)):
        _add(
            findings,
            "AGC-SCHEMA-DUPLICATE-LIST-VALUE",
            path,
            location,
            "unique-list",
            "duplicate-list-value",
            source,
        )
    if references != sorted(references):
        _add(
            findings,
            "AGC-SCHEMA-NONDETERMINISTIC-ORDER",
            path,
            location,
            "lexicographic-order",
            "non-lexicographic-order",
            source,
        )
    return tuple(references)


def _check_checked_at(
    value: object,
    path: str,
    location: str,
    findings: list[Finding],
    source: str,
) -> None:
    if not isinstance(value, str):
        _add(
            findings,
            "AGC-SOURCE-INVALID-CHECKED-TIME",
            path,
            location,
            "timezone-aware-iso8601",
            "invalid-checked-time",
            source,
        )
        return
    try:
        parsed = dt.datetime.fromisoformat(value)
    except ValueError:
        parsed = None
    if parsed is None or parsed.tzinfo is None or parsed.utcoffset() is None:
        _add(
            findings,
            "AGC-SOURCE-INVALID-CHECKED-TIME",
            path,
            location,
            "timezone-aware-iso8601",
            "invalid-checked-time",
            source,
        )


def _check_source_url(
    value: object,
    path: str,
    location: str,
    findings: list[Finding],
    source: str,
) -> bool:
    valid = False
    if isinstance(value, str):
        parsed = urlparse(value)
        valid = parsed.scheme == "https" and bool(parsed.netloc)
    if not valid:
        _add(
            findings,
            "AGC-SOURCE-INVALID-URL",
            path,
            location,
            "https-source-url",
            "invalid-source-url",
            source,
        )
    return valid


def _canonical_repo_path(value: str) -> str:
    parts: list[str] = []
    for part in value.split("/"):
        if part in {"", "."}:
            continue
        if part == "..":
            if parts and parts[-1] != "..":
                parts.pop()
            else:
                parts.append(part)
            continue
        parts.append(part)
    return "/".join(parts)


def _is_safe_repo_path(value: object) -> bool:
    if not _is_nonempty_string(value):
        return False
    text = str(value)
    if (
        any(ord(character) < 32 or 127 <= ord(character) <= 159 for character in text)
        or "\\" in text
        or text.startswith(("/", "~"))
    ):
        return False
    if re.match(r"^[A-Za-z]:", text):
        return False
    raw_parts = text.split("/")
    if not raw_parts or any(part in {"", ".", ".."} for part in raw_parts):
        return False
    return _canonical_repo_path(text) == text


def _check_path(
    value: object,
    path: str,
    location: str,
    findings: list[Finding],
    source: str,
) -> bool:
    if _is_safe_repo_path(value):
        return True
    _add(
        findings,
        "AGC-PATH-UNSAFE",
        path,
        location,
        "safe-repo-path",
        "unsafe-path",
        source,
    )
    return False


def _is_supported_enumerated_pattern(value: str) -> bool:
    """Limit enumerated contracts to the deterministic glob grammar we implement."""

    try:
        expanded_patterns = _expand_braces(value)
    except _BracePatternError:
        return False
    for expanded in expanded_patterns:
        for segment in expanded.split("/"):
            if any(marker in segment for marker in ("?", "[", "]")):
                return False
            if "**" in segment and segment != "**":
                return False
    return True


def read_repository_text(root: pathlib.Path, relative_path: str) -> str:
    """Read one UTF-8 repository file through the shared confined boundary."""

    if not _is_safe_repo_path(relative_path):
        raise ContractLoadError(
            "AGC-REPOSITORY-UNSAFE-PATH", "repository-artifact", "path"
        )
    try:
        return _read_root_confined_regular_text(
            root, pathlib.PurePosixPath(relative_path)
        )
    except FileNotFoundError as error:
        raise ContractLoadError(
            "AGC-REPOSITORY-FILE-MISSING", "repository-artifact", "file"
        ) from error
    except _UnsafeRootFileError as error:
        raise ContractLoadError(
            "AGC-REPOSITORY-UNSAFE-FILE", "repository-artifact", "file"
        ) from error
    except UnicodeError as error:
        raise ContractLoadError(
            "AGC-REPOSITORY-FILE-ENCODING", "repository-artifact", "file"
        ) from error
    except OSError as error:
        raise ContractLoadError(
            "AGC-REPOSITORY-FILE-READ", "repository-artifact", "file"
        ) from error


def _check_enumerated_pattern(
    value: object,
    path: str,
    location: str,
    findings: list[Finding],
    source: str,
) -> bool:
    if not _check_path(value, path, location, findings, source):
        return False
    if isinstance(value, str) and _is_supported_enumerated_pattern(value):
        if all(_is_safe_repo_path(expanded) for expanded in _expand_braces(value)):
            return True
        _add(
            findings,
            "AGC-PATH-UNSAFE",
            path,
            location,
            "safe-expanded-repo-paths",
            "unsafe-expanded-path",
            source,
        )
        return False
    _add(
        findings,
        "AGC-PATTERN-UNSUPPORTED",
        path,
        location,
        "supported-enumerated-pattern",
        "unsupported-pattern-grammar",
        source,
    )
    return False


def _check_common(
    document: Mapping[str, object],
    expected_fields: set[str],
    path: str,
    findings: list[Finding],
    *,
    time_field: str = "checked_at",
) -> None:
    source = path
    _check_fields(document, expected_fields, path, "root", findings, source)
    if document.get("schema_version") != 1:
        _add(
            findings,
            "AGC-SCHEMA-VERSION",
            path,
            "schema_version",
            "constant-1",
            "invalid-version",
            source,
        )
    _check_checked_at(document.get(time_field), path, time_field, findings, source)


def _validate_artifact_contract(
    document: Mapping[str, object], findings: list[Finding]
) -> None:
    path = CONTRACT_RELATIVE_PATHS["artifacts"].as_posix()
    source = path
    _check_common(document, ARTIFACT_TOP_FIELDS, path, findings)

    path_pattern_limits = _check_fields(
        document.get("path_pattern_limits"),
        PATH_PATTERN_LIMIT_FIELDS,
        path,
        "path_pattern_limits",
        findings,
        source,
    )
    if path_pattern_limits is not None:
        expected_limits = {
            "max_brace_groups": MAX_BRACE_GROUPS,
            "max_expanded_paths": MAX_EXPANDED_PATHS,
            "max_pattern_length": MAX_PATTERN_LENGTH,
        }
        for field, expected in expected_limits.items():
            observed = path_pattern_limits.get(field)
            if type(observed) is not int or observed != expected:
                _add(
                    findings,
                    "AGC-SCHEMA-CONSTANT",
                    path,
                    f"path_pattern_limits.{field}",
                    "validator-safety-ceiling",
                    "invalid-constant",
                    source,
                )

    artifacts = _as_sequence(
        document.get("artifacts"), path, "artifacts", findings, source
    )
    profile_ids: list[str] = []
    artifact_patterns: list[tuple[str, str, str]] = []
    if artifacts is not None:
        for index, raw in enumerate(artifacts):
            location = f"artifacts[{index}]"
            entry = _check_fields(
                raw, ARTIFACT_FIELDS, path, location, findings, source
            )
            if entry is None:
                continue
            profile_id = entry.get("profile_id")
            if _check_string(
                profile_id, path, f"{location}.profile_id", findings, source
            ):
                profile_ids.append(str(profile_id))
            _check_string(
                entry.get("artifact_type"),
                path,
                f"{location}.artifact_type",
                findings,
                source,
            )
            pattern = entry.get("path_pattern")
            if _check_enumerated_pattern(
                pattern,
                path,
                f"{location}.path_pattern",
                findings,
                source,
            ):
                artifact_patterns.append((str(profile_id), str(pattern), location))
            _check_enum(
                entry.get("repository_section"),
                {"catalog", "harness", "providers"},
                path,
                f"{location}.repository_section",
                findings,
                source,
            )
            _check_bool(
                entry.get("canonical"), path, f"{location}.canonical", findings, source
            )
            required_keys = _check_string_list(
                entry.get("required_keys"),
                path,
                f"{location}.required_keys",
                findings,
                source,
                allow_empty=True,
            )
            key_order = _check_string_list(
                entry.get("key_order"),
                path,
                f"{location}.key_order",
                findings,
                source,
                allow_empty=True,
            )
            _check_string_list(
                entry.get("required_sections"),
                path,
                f"{location}.required_sections",
                findings,
                source,
                allow_empty=True,
            )
            if (
                required_keys is not None
                and key_order is not None
                and required_keys != key_order
            ):
                _add(
                    findings,
                    "AGC-ARTIFACT-KEY-ORDER",
                    path,
                    f"{location}.key_order",
                    "exact-required-key-order",
                    "key-order-mismatch",
                    source,
                )
            expected_values = entry.get("expected_values")
            if not isinstance(expected_values, Mapping):
                _add(
                    findings,
                    "AGC-SCHEMA-TYPE",
                    path,
                    f"{location}.expected_values",
                    "mapping",
                    "non-mapping",
                    source,
                )
            else:
                for key, value in expected_values.items():
                    if not isinstance(key, str) or (
                        not isinstance(value, str) and not _is_bool(value)
                    ):
                        _add(
                            findings,
                            "AGC-SCHEMA-TYPE",
                            path,
                            f"{location}.expected_values",
                            "string-keys-and-scalar-values",
                            "invalid-mapping-entry",
                            source,
                        )
                if required_keys is not None and not set(expected_values).issubset(
                    required_keys
                ):
                    _add(
                        findings,
                        "AGC-ARTIFACT-EXPECTED-KEY",
                        path,
                        f"{location}.expected_values",
                        "required-key-subset",
                        "unregistered-expected-key",
                        source,
                    )
    _check_sorted_unique_ids(profile_ids, path, "artifacts", findings, source)
    for left_index, (left_id, left_pattern, left_location) in enumerate(
        artifact_patterns
    ):
        for right_id, right_pattern, right_location in artifact_patterns[
            left_index + 1 :
        ]:
            if _artifact_patterns_overlap(left_pattern, right_pattern):
                _add(
                    findings,
                    "AGC-ARTIFACT-PROFILE-OVERLAP",
                    path,
                    f"{left_location}.path_pattern|{right_location}.path_pattern",
                    "disjoint-artifact-profile-patterns",
                    "intersecting-artifact-profile-patterns",
                    source,
                )

    families = _as_sequence(
        document.get("governed_families"),
        path,
        "governed_families",
        findings,
        source,
    )
    family_ids: list[str] = []
    family_patterns: list[tuple[str, str, str]] = []
    if families is not None:
        for index, raw in enumerate(families):
            location = f"governed_families[{index}]"
            entry = _check_fields(
                raw,
                GOVERNED_FAMILY_FIELDS,
                path,
                location,
                findings,
                source,
            )
            if entry is None:
                continue
            family_id = entry.get("family_id")
            if _check_string(
                family_id,
                path,
                f"{location}.family_id",
                findings,
                source,
            ):
                family_ids.append(str(family_id))
            pattern = entry.get("path_pattern")
            if _check_enumerated_pattern(
                pattern,
                path,
                f"{location}.path_pattern",
                findings,
                source,
            ):
                family_patterns.append((str(family_id), str(pattern), location))
            sections = _check_string_list(
                entry.get("repository_sections"),
                path,
                f"{location}.repository_sections",
                findings,
                source,
                require_sorted=True,
            )
            for section_index, repository_section in enumerate(sections or ()):
                _check_enum(
                    repository_section,
                    {"catalog", "harness", "providers"},
                    path,
                    f"{location}.repository_sections[{section_index}]",
                    findings,
                    source,
                )
    _check_sorted_unique_ids(family_ids, path, "governed_families", findings, source)
    for left_index, (_, left_pattern, left_location) in enumerate(family_patterns):
        for _, right_pattern, right_location in family_patterns[left_index + 1 :]:
            if _artifact_patterns_overlap(left_pattern, right_pattern):
                _add(
                    findings,
                    "AGC-GOVERNED-FAMILY-OVERLAP",
                    path,
                    f"{left_location}.path_pattern|{right_location}.path_pattern",
                    "disjoint-governed-family-patterns",
                    "intersecting-governed-family-patterns",
                    source,
                )

    root_shims = _as_sequence(
        document.get("root_shims"), path, "root_shims", findings, source
    )
    root_paths: list[str] = []
    if root_shims is not None:
        for index, raw in enumerate(root_shims):
            location = f"root_shims[{index}]"
            entry = _check_fields(
                raw, ROOT_SHIM_FIELDS, path, location, findings, source
            )
            if entry is None:
                continue
            shim_path = entry.get("path")
            if _check_path(shim_path, path, f"{location}.path", findings, source):
                root_paths.append(str(shim_path))
            _check_enum(
                entry.get("provider"),
                {"claude", "codex", "gemini", "shared"},
                path,
                f"{location}.provider",
                findings,
                source,
            )
            _check_path(
                entry.get("bootstrap_target"),
                path,
                f"{location}.bootstrap_target",
                findings,
                source,
            )
            _check_path(
                entry.get("provider_target"),
                path,
                f"{location}.provider_target",
                findings,
                source,
            )
            memory_targets = _check_string_list(
                entry.get("memory_targets"),
                path,
                f"{location}.memory_targets",
                findings,
                source,
            )
            for target_index, target in enumerate(memory_targets or ()):
                _check_path(
                    target,
                    path,
                    f"{location}.memory_targets[{target_index}]",
                    findings,
                    source,
                )
            _check_enum(
                entry.get("import_style"),
                {"at-dot-import", "at-import", "numbered-load"},
                path,
                f"{location}.import_style",
                findings,
                source,
            )
            _check_enum(
                entry.get("frontmatter"),
                {"forbidden", "provider-required"},
                path,
                f"{location}.frontmatter",
                findings,
                source,
            )
    _check_sorted_unique_ids(root_paths, path, "root_shims", findings, source)

    readmes = _as_sequence(
        document.get("readme_profiles"), path, "readme_profiles", findings, source
    )
    readme_ids: list[str] = []
    if readmes is not None:
        for index, raw in enumerate(readmes):
            location = f"readme_profiles[{index}]"
            entry = _check_fields(
                raw, README_PROFILE_FIELDS, path, location, findings, source
            )
            if entry is None:
                continue
            profile_id = entry.get("profile_id")
            if _check_string(
                profile_id, path, f"{location}.profile_id", findings, source
            ):
                readme_ids.append(str(profile_id))
            _check_enumerated_pattern(
                entry.get("path_pattern"),
                path,
                f"{location}.path_pattern",
                findings,
                source,
            )
            _check_string_list(
                entry.get("required_sections"),
                path,
                f"{location}.required_sections",
                findings,
                source,
            )
            _check_string_list(
                entry.get("allowed_sections"),
                path,
                f"{location}.allowed_sections",
                findings,
                source,
            )
            _check_string_list(
                entry.get("forbidden_policy_topics"),
                path,
                f"{location}.forbidden_policy_topics",
                findings,
                source,
                require_sorted=True,
            )
    _check_sorted_unique_ids(readme_ids, path, "readme_profiles", findings, source)

    authorities = _as_sequence(
        document.get("path_authority"), path, "path_authority", findings, source
    )
    authority_ids: list[str] = []
    authority_patterns: list[tuple[str, str, str]] = []
    if authorities is not None:
        for index, raw in enumerate(authorities):
            location = f"path_authority[{index}]"
            entry = _check_fields(
                raw, AUTHORITY_FIELDS, path, location, findings, source
            )
            if entry is None:
                continue
            authority_id = entry.get("authority_id")
            if _check_string(
                authority_id, path, f"{location}.authority_id", findings, source
            ):
                authority_ids.append(str(authority_id))
            patterns = _check_string_list(
                entry.get("path_patterns"),
                path,
                f"{location}.path_patterns",
                findings,
                source,
                require_sorted=True,
            )
            if patterns is not None:
                for pattern_index, pattern in enumerate(patterns):
                    _check_path(
                        pattern,
                        path,
                        f"{location}.path_patterns[{pattern_index}]",
                        findings,
                        source,
                    )
                    if isinstance(pattern, str):
                        authority_patterns.append(
                            (str(authority_id), pattern, location)
                        )
            _check_string(
                entry.get("canonical_owner"),
                path,
                f"{location}.canonical_owner",
                findings,
                source,
            )
            entry_owners = _check_entry_authority_list(
                entry.get("entry_owners"),
                path,
                f"{location}.entry_owners",
                findings,
                source,
            )
            _check_string_list(
                entry.get("permitted_contributors"),
                path,
                f"{location}.permitted_contributors",
                findings,
                source,
                require_sorted=True,
            )
            mandatory_reviewers = (
                _check_string_list(
                    entry.get("mandatory_reviewers"),
                    path,
                    f"{location}.mandatory_reviewers",
                    findings,
                    source,
                    allow_empty=True,
                    require_sorted=True,
                )
                or ()
            )
            entry_reviewers = _check_entry_authority_list(
                entry.get("entry_reviewers"),
                path,
                f"{location}.entry_reviewers",
                findings,
                source,
            )
            protected = entry.get("protected")
            _check_bool(protected, path, f"{location}.protected", findings, source)
            if protected is True and not mandatory_reviewers and not entry_reviewers:
                _add(
                    findings,
                    "AGC-AUTHORITY-SEMANTICS",
                    path,
                    f"{location}.mandatory_reviewers",
                    "effective-protected-authority-reviewer",
                    "missing-effective-reviewer",
                    source,
                )
            _check_string_list(
                entry.get("validators"),
                path,
                f"{location}.validators",
                findings,
                source,
            )
            _check_string(
                entry.get("rollback"), path, f"{location}.rollback", findings, source
            )
            semantics = CATALOG_AUTHORITY_SEMANTICS.get(str(authority_id))
            if semantics is not None:
                observed = {
                    "canonical_owner": entry.get("canonical_owner"),
                    "mandatory_reviewers": mandatory_reviewers,
                    "entry_owners": entry_owners,
                    "entry_reviewers": entry_reviewers,
                }
                for field in (
                    "canonical_owner",
                    "mandatory_reviewers",
                    "entry_owners",
                    "entry_reviewers",
                ):
                    if observed[field] != semantics[field]:
                        _add(
                            findings,
                            "AGC-AUTHORITY-SEMANTICS",
                            path,
                            f"{location}.{field}",
                            "spec-authority-policy",
                            "authority-policy-mismatch",
                            source,
                        )
    _check_sorted_unique_ids(authority_ids, path, "path_authority", findings, source)
    for index, (owner, pattern, location) in enumerate(authority_patterns):
        for other_owner, other_pattern, other_location in authority_patterns[
            index + 1 :
        ]:
            if owner != other_owner and _patterns_overlap(pattern, other_pattern):
                _add(
                    findings,
                    "AGC-AUTHORITY-OVERLAP",
                    path,
                    f"{location}.path_patterns|{other_location}.path_patterns",
                    "single-canonical-authority",
                    "overlapping-authority",
                    source,
                )


def _check_sorted_unique_ids(
    values: Sequence[str],
    path: str,
    location: str,
    findings: list[Finding],
    source: str,
    *,
    duplicate_code: str = "AGC-SCHEMA-DUPLICATE-ID",
) -> None:
    if len(values) != len(set(values)):
        _add(
            findings,
            duplicate_code,
            path,
            location,
            "unique-ids",
            "duplicate-id",
            source,
        )
    if list(values) != sorted(values):
        _add(
            findings,
            "AGC-SCHEMA-NONDETERMINISTIC-ORDER",
            path,
            location,
            "lexicographic-id-order",
            "non-lexicographic-id-order",
            source,
        )


def _patterns_overlap(left: str, right: str) -> bool:
    left = _canonical_repo_path(left)
    right = _canonical_repo_path(right)
    if left == right:
        return True

    def literal_prefix(pattern: str) -> tuple[str, bool]:
        marker_positions = [
            position
            for marker in ("*", "?", "{", "[")
            if (position := pattern.find(marker)) >= 0
        ]
        if not marker_positions:
            return pattern, False
        return pattern[: min(marker_positions)], True

    left_prefix, left_has_glob = literal_prefix(left)
    right_prefix, right_has_glob = literal_prefix(right)
    if not left_has_glob and not right_has_glob:
        return False
    return left_prefix.startswith(right_prefix) or right_prefix.startswith(left_prefix)


def _validate_catalog_contract(
    document: Mapping[str, object],
    provider_document: Mapping[str, object],
    artifact_document: Mapping[str, object],
    findings: list[Finding],
) -> None:
    path = CONTRACT_RELATIVE_PATHS["catalog"].as_posix()
    source = path
    _check_common(document, CATALOG_TOP_FIELDS, path, findings)
    projections = (
        _check_string_list(
            document.get("projection_targets"),
            path,
            "projection_targets",
            findings,
            source,
            require_sorted=True,
        )
        or ()
    )
    provider_targets = {
        str(entry.get("provider_id"))
        for entry in _sequence_or_empty(provider_document.get("providers"))
        if isinstance(entry, Mapping) and _is_nonempty_string(entry.get("provider_id"))
    }
    compatibility_targets = {
        str(entry.get("surface_id"))
        for entry in _sequence_or_empty(provider_document.get("compatibility_surfaces"))
        if isinstance(entry, Mapping)
        and entry.get("status") == "active"
        and _is_nonempty_string(entry.get("surface_id"))
    }
    canonical_projection_targets = tuple(
        sorted(provider_targets | compatibility_targets)
    )
    if projections != canonical_projection_targets:
        _add(
            findings,
            "AGC-CATALOG-PROJECTION-TARGET-MISMATCH",
            path,
            "projection_targets",
            "provider-and-active-compatibility-targets",
            "projection-target-set-mismatch",
            source,
        )
    scopes = set(
        _check_string_list(
            document.get("scopes"),
            path,
            "scopes",
            findings,
            source,
            require_sorted=True,
        )
        or ()
    )

    permissions = _as_sequence(
        document.get("permissions"), path, "permissions", findings, source
    )
    permission_ids: list[str] = []
    if permissions is not None:
        for index, raw in enumerate(permissions):
            location = f"permissions[{index}]"
            entry = _check_fields(
                raw, PERMISSION_FIELDS, path, location, findings, source
            )
            if entry is None:
                continue
            permission_id = entry.get("permission_id")
            if _check_string(
                permission_id, path, f"{location}.permission_id", findings, source
            ):
                permission_ids.append(str(permission_id))
            _check_bool(
                entry.get("mutation_allowed"),
                path,
                f"{location}.mutation_allowed",
                findings,
                source,
            )
            _check_bool(
                entry.get("evidence_required"),
                path,
                f"{location}.evidence_required",
                findings,
                source,
            )
    _check_sorted_unique_ids(permission_ids, path, "permissions", findings, source)
    permission_set = set(permission_ids)

    agents = _as_sequence(document.get("agents"), path, "agents", findings, source)
    agent_ids: list[str] = []
    agent_functions: dict[str, set[str]] = {}
    if agents is not None:
        for index, raw in enumerate(agents):
            location = f"agents[{index}]"
            entry = _check_fields(raw, AGENT_FIELDS, path, location, findings, source)
            if entry is None:
                continue
            agent_id = entry.get("agent_id")
            if _check_string(agent_id, path, f"{location}.agent_id", findings, source):
                agent_ids.append(str(agent_id))
            _check_enum(
                entry.get("category"),
                AGENT_CATEGORIES,
                path,
                f"{location}.category",
                findings,
                source,
            )
            if not _is_registered_string(entry.get("scope"), scopes):
                _unknown_reference(findings, path, f"{location}.scope", source)
            _check_enum(
                entry.get("tier"),
                AGENT_TIERS,
                path,
                f"{location}.tier",
                findings,
                source,
            )
            _check_enum(
                entry.get("status"),
                AGENT_STATUSES,
                path,
                f"{location}.status",
                findings,
                source,
            )
            _check_path(
                entry.get("catalog_path"),
                path,
                f"{location}.catalog_path",
                findings,
                source,
            )
            if not _is_registered_string(
                entry.get("permission_profile"), permission_set
            ):
                _unknown_reference(
                    findings, path, f"{location}.permission_profile", source
                )
            _check_string(
                entry.get("work_profile"),
                path,
                f"{location}.work_profile",
                findings,
                source,
            )
            function_ids = (
                _check_string_list(
                    entry.get("function_ids"),
                    path,
                    f"{location}.function_ids",
                    findings,
                    source,
                    allow_empty=True,
                    require_sorted=True,
                )
                or ()
            )
            if isinstance(agent_id, str):
                agent_functions[agent_id] = set(function_ids)
            projection_values = (
                _check_string_list(
                    entry.get("provider_projections"),
                    path,
                    f"{location}.provider_projections",
                    findings,
                    source,
                    require_sorted=True,
                )
                or ()
            )
            for projection in projection_values:
                if projection not in projections:
                    _unknown_reference(
                        findings, path, f"{location}.provider_projections", source
                    )
    _check_sorted_unique_ids(
        agent_ids,
        path,
        "agents",
        findings,
        source,
        duplicate_code="AGC-CATALOG-DUPLICATE-ID",
    )
    if agents is not None and len(agents) != EXPECTED_AGENT_COUNT:
        _add(
            findings,
            "AGC-CATALOG-CARDINALITY",
            path,
            "agents",
            "exact-agent-count",
            "wrong-agent-count",
            source,
        )
    agent_set = set(agent_ids)

    functions = _as_sequence(
        document.get("functions"), path, "functions", findings, source
    )
    function_ids: list[str] = []
    function_owners: dict[str, str] = {}
    if functions is not None:
        for index, raw in enumerate(functions):
            location = f"functions[{index}]"
            entry = _check_fields(
                raw, FUNCTION_FIELDS, path, location, findings, source
            )
            if entry is None:
                continue
            function_id = entry.get("function_id")
            if _check_string(
                function_id, path, f"{location}.function_id", findings, source
            ):
                function_ids.append(str(function_id))
            if not _is_registered_string(entry.get("scope"), scopes):
                _unknown_reference(findings, path, f"{location}.scope", source)
            _check_enum(
                entry.get("status"),
                AGENT_STATUSES,
                path,
                f"{location}.status",
                findings,
                source,
            )
            _check_path(
                entry.get("catalog_path"),
                path,
                f"{location}.catalog_path",
                findings,
                source,
            )
            owner = entry.get("owner_agent")
            if not _is_registered_string(owner, agent_set):
                _unknown_reference(findings, path, f"{location}.owner_agent", source)
            elif isinstance(function_id, str) and isinstance(owner, str):
                function_owners[function_id] = owner
            reviewers = (
                _check_string_list(
                    entry.get("reviewer_agents"),
                    path,
                    f"{location}.reviewer_agents",
                    findings,
                    source,
                    require_sorted=True,
                )
                or ()
            )
            for reviewer in reviewers:
                if reviewer not in agent_set:
                    _unknown_reference(
                        findings, path, f"{location}.reviewer_agents", source
                    )
            for field in ("inputs", "outputs", "gates"):
                _check_string_list(
                    entry.get(field), path, f"{location}.{field}", findings, source
                )
            projection_values = (
                _check_string_list(
                    entry.get("provider_projections"),
                    path,
                    f"{location}.provider_projections",
                    findings,
                    source,
                    require_sorted=True,
                )
                or ()
            )
            for projection in projection_values:
                if projection not in projections:
                    _unknown_reference(
                        findings, path, f"{location}.provider_projections", source
                    )
    _check_sorted_unique_ids(
        function_ids,
        path,
        "functions",
        findings,
        source,
        duplicate_code="AGC-CATALOG-DUPLICATE-ID",
    )
    if functions is not None and len(functions) != EXPECTED_FUNCTION_COUNT:
        _add(
            findings,
            "AGC-CATALOG-CARDINALITY",
            path,
            "functions",
            "exact-function-count",
            "wrong-function-count",
            source,
        )
    function_set = set(function_ids)

    evaluation = _check_fields(
        document.get("evaluation"),
        EVALUATION_FIELDS,
        path,
        "evaluation",
        findings,
        source,
    )
    if evaluation is not None:
        owner = evaluation.get("owner_agent")
        reviewer = evaluation.get("reviewer_agent")
        for field, value in (("owner_agent", owner), ("reviewer_agent", reviewer)):
            if not _is_registered_string(value, agent_set):
                _unknown_reference(findings, path, f"evaluation.{field}", source)
        if owner != "eval-engineer" or reviewer != "code-reviewer" or owner == reviewer:
            _add(
                findings,
                "AGC-EVAL-ROLE-SEPARATION",
                path,
                "evaluation",
                "eval-owner-and-independent-code-reviewer",
                "evaluation-role-contract-mismatch",
                source,
            )
        expected_paths = {
            "fixture_catalog_path": "docs/90.references/data/governance/agent-output-eval-fixtures.md",
            "scorer_path": "scripts/validation/agent_output_eval.py",
            "runner_path": "scripts/validation/run-agent-output-eval-fixtures.sh",
            "test_path": "tests/validation/test_agent_output_eval_fixtures.py",
        }
        for field, expected_path in expected_paths.items():
            _check_path(
                evaluation.get(field), path, f"evaluation.{field}", findings, source
            )
            if evaluation.get(field) != expected_path:
                _add(
                    findings,
                    "AGC-EVAL-PATH",
                    path,
                    f"evaluation.{field}",
                    "canonical-evaluation-path",
                    "evaluation-path-mismatch",
                    source,
                )
        for field, expected_count in (("fixture_count", 8), ("regression_count", 10)):
            actual = evaluation.get(field)
            if isinstance(actual, bool) or actual != expected_count:
                _add(
                    findings,
                    "AGC-EVAL-CARDINALITY",
                    path,
                    f"evaluation.{field}",
                    "exact-evaluation-cardinality",
                    "evaluation-cardinality-mismatch",
                    source,
                )
        if evaluation.get("input_classification") != "synthetic-fixture":
            _add(
                findings,
                "AGC-EVAL-INPUT-POLICY",
                path,
                "evaluation.input_classification",
                "synthetic-fixture",
                "evaluation-input-classification-mismatch",
                source,
            )
        input_roots = _check_string_list(
            evaluation.get("input_roots"),
            path,
            "evaluation.input_roots",
            findings,
            source,
            require_sorted=True,
        )
        if tuple(input_roots or ()) != (
            "docs/90.references/data/governance/agent-output-eval-synthetic",
            "tests/fixtures/agent-output-eval",
        ):
            _add(
                findings,
                "AGC-EVAL-INPUT-POLICY",
                path,
                "evaluation.input_roots",
                "exact-synthetic-input-roots",
                "evaluation-input-root-mismatch",
                source,
            )
        markers = _check_string_list(
            evaluation.get("pass_markers"),
            path,
            "evaluation.pass_markers",
            findings,
            source,
            require_sorted=True,
        )
        if tuple(markers or ()) != (
            "fixtures_check=pass",
            "regressions_check=pass",
        ):
            _add(
                findings,
                "AGC-EVAL-MARKER",
                path,
                "evaluation.pass_markers",
                "exact-evaluation-pass-markers",
                "evaluation-marker-mismatch",
                source,
            )
        thresholds = evaluation.get("fixture_thresholds")
        expected_threshold_ids = {
            "AOE-ADAPTER-001",
            "AOE-CLOSURE-001",
            "AOE-DOC-001",
            "AOE-HOOK-001",
            "AOE-INFRA-001",
            "AOE-PROVIDER-001",
            "AOE-ROLE-001",
            "AOE-ROUTING-001",
        }
        if (
            not isinstance(thresholds, Mapping)
            or set(thresholds) != expected_threshold_ids
            or any(
                isinstance(value, bool)
                or not isinstance(value, int | float)
                or value != 0.50
                for value in thresholds.values()
            )
        ):
            _add(
                findings,
                "AGC-EVAL-THRESHOLD",
                path,
                "evaluation.fixture_thresholds",
                "exact-per-fixture-threshold-map",
                "evaluation-threshold-mismatch",
                source,
            )

    for index, loop in enumerate(
        _sequence_or_empty(provider_document.get("harness_loops"))
    ):
        if not isinstance(loop, Mapping):
            continue
        for field in ("owner_agent", "reviewer_agent"):
            if not _is_registered_string(loop.get(field), agent_set):
                _unknown_reference(
                    findings,
                    CONTRACT_RELATIVE_PATHS["providers"].as_posix(),
                    f"harness_loops[{index}].{field}",
                    CONTRACT_RELATIVE_PATHS["providers"].as_posix(),
                )
        if not _is_registered_string(loop.get("permission_profile"), permission_set):
            _unknown_reference(
                findings,
                CONTRACT_RELATIVE_PATHS["providers"].as_posix(),
                f"harness_loops[{index}].permission_profile",
                CONTRACT_RELATIVE_PATHS["providers"].as_posix(),
            )

    for agent_id, referenced_functions in agent_functions.items():
        for function_id in sorted(referenced_functions):
            if function_id not in function_set:
                _unknown_reference(
                    findings, path, f"agents.{agent_id}.function_ids", source
                )
            elif function_owners.get(function_id) != agent_id:
                _add(
                    findings,
                    "AGC-CATALOG-OWNER-MISMATCH",
                    path,
                    f"agents.{agent_id}.function_ids",
                    "function-owner-parity",
                    "function-owner-mismatch",
                    source,
                )
    for function_id, owner in function_owners.items():
        if function_id not in agent_functions.get(owner, set()):
            _add(
                findings,
                "AGC-CATALOG-OWNER-MISMATCH",
                path,
                f"functions.{function_id}.owner_agent",
                "agent-function-parity",
                "agent-function-mismatch",
                source,
            )

    transfers = _as_sequence(
        document.get("role_transfers"), path, "role_transfers", findings, source
    )
    transfer_ids: list[str] = []
    if transfers is not None:
        for index, raw in enumerate(transfers):
            location = f"role_transfers[{index}]"
            entry = _check_fields(
                raw, ROLE_TRANSFER_FIELDS, path, location, findings, source
            )
            if entry is None:
                continue
            retired = entry.get("retired_agent_id")
            if _check_string(
                retired, path, f"{location}.retired_agent_id", findings, source
            ):
                transfer_ids.append(str(retired))
                if retired in agent_set:
                    _add(
                        findings,
                        "AGC-CATALOG-RETIRED-ACTIVE",
                        path,
                        f"{location}.retired_agent_id",
                        "retired-id-absent-from-active-catalog",
                        "retired-id-active",
                        source,
                    )
            _check_enum(
                entry.get("status"),
                {"retired"},
                path,
                f"{location}.status",
                findings,
                source,
            )
            successors = (
                _check_string_list(
                    entry.get("successor_agent_ids"),
                    path,
                    f"{location}.successor_agent_ids",
                    findings,
                    source,
                    require_sorted=True,
                )
                or ()
            )
            successor_functions = (
                _check_string_list(
                    entry.get("successor_function_ids"),
                    path,
                    f"{location}.successor_function_ids",
                    findings,
                    source,
                    require_sorted=True,
                )
                or ()
            )
            for successor in successors:
                if successor not in agent_set:
                    _unknown_reference(
                        findings, path, f"{location}.successor_agent_ids", source
                    )
            for function_id in successor_functions:
                if function_id not in function_set:
                    _unknown_reference(
                        findings, path, f"{location}.successor_function_ids", source
                    )
            _check_string(
                entry.get("rationale"), path, f"{location}.rationale", findings, source
            )
    _check_sorted_unique_ids(transfer_ids, path, "role_transfers", findings, source)

    intake = _as_sequence(
        document.get("capability_intake"), path, "capability_intake", findings, source
    )
    intake_ids: list[str] = []
    if intake is not None:
        for index, raw in enumerate(intake):
            location = f"capability_intake[{index}]"
            entry = _check_fields(
                raw, CAPABILITY_INTAKE_FIELDS, path, location, findings, source
            )
            if entry is None:
                continue
            capability_id = entry.get("capability_id")
            if _check_string(
                capability_id, path, f"{location}.capability_id", findings, source
            ):
                intake_ids.append(str(capability_id))
            _check_string(
                entry.get("source"), path, f"{location}.source", findings, source
            )
            _check_source_url(
                entry.get("source_url"),
                path,
                f"{location}.source_url",
                findings,
                source,
            )
            _check_enum(
                entry.get("decision"),
                CAPABILITY_DECISIONS,
                path,
                f"{location}.decision",
                findings,
                source,
            )
            if not _is_registered_string(entry.get("owner_agent"), agent_set):
                _unknown_reference(findings, path, f"{location}.owner_agent", source)
            if not _is_registered_string(
                entry.get("evaluation_function"), function_set
            ):
                _unknown_reference(
                    findings, path, f"{location}.evaluation_function", source
                )
    _check_sorted_unique_ids(intake_ids, path, "capability_intake", findings, source)

    work_profile_ids = {
        entry.get("profile_id")
        for entry in _sequence_or_empty(provider_document.get("work_profiles"))
        if isinstance(entry, Mapping) and isinstance(entry.get("profile_id"), str)
    }
    if agents is not None:
        for index, raw in enumerate(agents):
            if isinstance(raw, Mapping) and not _is_registered_string(
                raw.get("work_profile"), work_profile_ids
            ):
                _unknown_reference(
                    findings, path, f"agents[{index}].work_profile", source
                )

    path_authorities = _sequence_or_empty(artifact_document.get("path_authority"))
    if path_authorities:
        for index, raw in enumerate(path_authorities):
            if not isinstance(raw, Mapping):
                continue
            for field in ("canonical_owner",):
                if not _is_registered_string(raw.get(field), agent_set):
                    _unknown_reference(
                        findings,
                        CONTRACT_RELATIVE_PATHS["artifacts"].as_posix(),
                        f"path_authority[{index}].{field}",
                        CONTRACT_RELATIVE_PATHS["artifacts"].as_posix(),
                    )
            for field in ("permitted_contributors", "mandatory_reviewers"):
                for item in _sequence_or_empty(raw.get(field)):
                    if not _is_registered_string(item, agent_set):
                        _unknown_reference(
                            findings,
                            CONTRACT_RELATIVE_PATHS["artifacts"].as_posix(),
                            f"path_authority[{index}].{field}",
                            CONTRACT_RELATIVE_PATHS["artifacts"].as_posix(),
                        )
            for field in ("entry_owners", "entry_reviewers"):
                references = _sequence_or_empty(raw.get(field))
                for reference_index, reference in enumerate(references):
                    if not isinstance(reference, Mapping):
                        continue
                    collection = reference.get("catalog_collection")
                    agent_field = reference.get("agent_field")
                    entries = _sequence_or_empty(document.get(str(collection)))
                    for catalog_entry in entries:
                        if not isinstance(catalog_entry, Mapping):
                            continue
                        if not _is_registered_string(
                            catalog_entry.get(str(agent_field)), agent_set
                        ):
                            _unknown_reference(
                                findings,
                                CONTRACT_RELATIVE_PATHS["artifacts"].as_posix(),
                                (
                                    f"path_authority[{index}].{field}"
                                    f"[{reference_index}].agent_field"
                                ),
                                CONTRACT_RELATIVE_PATHS["artifacts"].as_posix(),
                            )


def _unknown_reference(
    findings: list[Finding], path: str, location: str, source: str
) -> None:
    _add(
        findings,
        "AGC-CATALOG-UNKNOWN-REFERENCE",
        path,
        location,
        "registered-reference",
        "unknown-reference",
        source,
    )


def _validate_provider_contract(
    root: pathlib.Path,
    document: Mapping[str, object],
    findings: list[Finding],
) -> None:
    path = CONTRACT_RELATIVE_PATHS["providers"].as_posix()
    source = path
    _check_common(
        document, PROVIDER_TOP_FIELDS, path, findings, time_field="retrieved_at"
    )
    _check_checked_at(document.get("cutoff_at"), path, "cutoff_at", findings, source)
    try:
        cutoff_at = dt.datetime.fromisoformat(str(document.get("cutoff_at")))
        retrieved_at = dt.datetime.fromisoformat(str(document.get("retrieved_at")))
    except ValueError:
        cutoff_at = None
        retrieved_at = None
    if (
        cutoff_at is not None
        and retrieved_at is not None
        and cutoff_at.tzinfo is not None
        and retrieved_at.tzinfo is not None
        and retrieved_at < cutoff_at
    ):
        _add(
            findings,
            "AGC-SOURCE-OBSERVATION-ORDER",
            path,
            "retrieved_at",
            "retrieval-not-before-cutoff",
            "backdated-retrieval",
            source,
        )
    providers = _as_sequence(
        document.get("providers"), path, "providers", findings, source
    )
    provider_ids: list[str] = []
    if providers is not None:
        for index, raw in enumerate(providers):
            location = f"providers[{index}]"
            entry = _check_fields(
                raw, PROVIDER_FIELDS, path, location, findings, source
            )
            if entry is None:
                continue
            provider_id = entry.get("provider_id")
            if _check_string(
                provider_id, path, f"{location}.provider_id", findings, source
            ):
                provider_ids.append(str(provider_id))
            _check_enum(
                entry.get("capability_status"),
                PROVIDER_CAPABILITY_STATES,
                path,
                f"{location}.capability_status",
                findings,
                source,
                code="AGC-PROVIDER-INVALID-STATE",
            )
            _check_enum(
                entry.get("adoption_status"),
                PROVIDER_ADOPTION_STATES,
                path,
                f"{location}.adoption_status",
                findings,
                source,
                code="AGC-PROVIDER-INVALID-STATE",
            )
            for field in (
                "native_agent_pattern",
                "native_config_path",
                "native_skill_pattern",
                "canonical_skill_source_pattern",
            ):
                _check_path(
                    entry.get(field), path, f"{location}.{field}", findings, source
                )
            _check_source_url(
                entry.get("source_url"),
                path,
                f"{location}.source_url",
                findings,
                source,
            )
            _check_source_url(
                entry.get("hook_source_url"),
                path,
                f"{location}.hook_source_url",
                findings,
                source,
            )
            observation = entry.get("local_cli_observation")
            _check_enum(
                observation,
                LOCAL_CLI_OBSERVATIONS,
                path,
                f"{location}.local_cli_observation",
                findings,
                source,
            )
            version = entry.get("local_cli_version")
            if observation == "observed":
                _check_string(
                    version,
                    path,
                    f"{location}.local_cli_version",
                    findings,
                    source,
                )
            elif version is not None:
                _add(
                    findings,
                    "AGC-PROVIDER-LOCAL-OBSERVATION",
                    path,
                    f"{location}.local_cli_version",
                    "null-when-unavailable",
                    "version-without-observation",
                    source,
                )
            _check_enum(
                entry.get("local_runtime_acceptance"),
                RUNTIME_ACCEPTANCE_STATES,
                path,
                f"{location}.local_runtime_acceptance",
                findings,
                source,
                code="AGC-PROVIDER-INVALID-STATE",
            )
    _check_sorted_unique_ids(provider_ids, path, "providers", findings, source)
    if providers is not None and len(providers) != EXPECTED_PROVIDER_COUNT:
        _add(
            findings,
            "AGC-PROVIDER-CARDINALITY",
            path,
            "providers",
            "exact-provider-count",
            "wrong-provider-count",
            source,
        )
    provider_set = set(provider_ids)

    compatibility = _as_sequence(
        document.get("compatibility_surfaces"),
        path,
        "compatibility_surfaces",
        findings,
        source,
    )
    compatibility_ids: list[str] = []
    if compatibility is not None:
        for index, raw in enumerate(compatibility):
            location = f"compatibility_surfaces[{index}]"
            entry = _check_fields(
                raw, COMPATIBILITY_FIELDS, path, location, findings, source
            )
            if entry is None:
                continue
            surface_id = entry.get("surface_id")
            if _check_string(
                surface_id, path, f"{location}.surface_id", findings, source
            ):
                compatibility_ids.append(str(surface_id))
            _check_path(
                entry.get("path_pattern"),
                path,
                f"{location}.path_pattern",
                findings,
                source,
            )
            _check_enum(
                entry.get("status"),
                {"active", "retired"},
                path,
                f"{location}.status",
                findings,
                source,
            )
            _check_string_list(
                entry.get("consumers"),
                path,
                f"{location}.consumers",
                findings,
                source,
                require_sorted=True,
            )
            _check_source_url(
                entry.get("source_url"),
                path,
                f"{location}.source_url",
                findings,
                source,
            )
    _check_sorted_unique_ids(
        compatibility_ids, path, "compatibility_surfaces", findings, source
    )

    work_profiles = _as_sequence(
        document.get("work_profiles"), path, "work_profiles", findings, source
    )
    profile_ids: list[str] = []
    profile_defaults: list[tuple[str, str, str, str | None, str | None]] = []
    if work_profiles is not None:
        for index, raw in enumerate(work_profiles):
            location = f"work_profiles[{index}]"
            entry = _check_fields(
                raw, WORK_PROFILE_FIELDS, path, location, findings, source
            )
            if entry is None:
                continue
            profile_id = entry.get("profile_id")
            if _check_string(
                profile_id, path, f"{location}.profile_id", findings, source
            ):
                profile_ids.append(str(profile_id))
            _check_string(
                entry.get("description"),
                path,
                f"{location}.description",
                findings,
                source,
            )
            defaults = _as_sequence(
                entry.get("defaults"), path, f"{location}.defaults", findings, source
            )
            default_providers: list[str] = []
            if defaults is not None:
                for default_index, raw_default in enumerate(defaults):
                    default_location = f"{location}.defaults[{default_index}]"
                    default_fields = (
                        WORK_PROFILE_DEFAULT_CLAUDE_FIELDS
                        if isinstance(raw_default, Mapping)
                        and raw_default.get("provider") == "claude"
                        else WORK_PROFILE_DEFAULT_REASONING_FIELDS
                    )
                    default = _check_fields(
                        raw_default,
                        default_fields,
                        path,
                        default_location,
                        findings,
                        source,
                    )
                    if default is None:
                        continue
                    provider = default.get("provider")
                    model_id = default.get("model_id")
                    reasoning = default.get("reasoning")
                    effort = default.get("effort")
                    if _check_string(
                        provider, path, f"{default_location}.provider", findings, source
                    ):
                        default_providers.append(str(provider))
                    _check_string(
                        model_id, path, f"{default_location}.model_id", findings, source
                    )
                    if provider == "claude":
                        if effort is not None:
                            _check_string(
                                effort,
                                path,
                                f"{default_location}.effort",
                                findings,
                                source,
                            )
                    else:
                        _check_string(
                            reasoning,
                            path,
                            f"{default_location}.reasoning",
                            findings,
                            source,
                        )
                    if all(
                        isinstance(item, str)
                        for item in (profile_id, provider, model_id)
                    ):
                        profile_defaults.append(
                            (
                                str(profile_id),
                                str(provider),
                                str(model_id),
                                str(reasoning) if isinstance(reasoning, str) else None,
                                str(effort) if isinstance(effort, str) else None,
                            )
                        )
            _check_sorted_unique_ids(
                default_providers, path, f"{location}.defaults", findings, source
            )
            if set(default_providers) != provider_set:
                _add(
                    findings,
                    "AGC-PROVIDER-PROFILE-COVERAGE",
                    path,
                    f"{location}.defaults",
                    "exact-provider-set",
                    "provider-set-mismatch",
                    source,
                )
    _check_sorted_unique_ids(profile_ids, path, "work_profiles", findings, source)
    profile_set = set(profile_ids)

    approvals = _as_sequence(
        document.get("fallback_approvals"),
        path,
        "fallback_approvals",
        findings,
        source,
    )
    approval_ids: list[str] = []
    approval_entries: dict[str, Mapping[str, object]] = {}
    if approvals is not None:
        for index, raw in enumerate(approvals):
            location = f"fallback_approvals[{index}]"
            entry = _check_fields(
                raw,
                FALLBACK_APPROVAL_FIELDS,
                path,
                location,
                findings,
                source,
            )
            if entry is None:
                continue
            approval_id = entry.get("approval_id")
            provider = entry.get("provider")
            source_model = entry.get("source_model_id")
            target_model = entry.get("target_model_id")
            reference = entry.get("reference")
            if _check_string(
                approval_id,
                path,
                f"{location}.approval_id",
                findings,
                source,
            ):
                approval_ids.append(str(approval_id))
                approval_entries[str(approval_id)] = entry
            if not _is_registered_string(provider, provider_set):
                _unknown_reference(findings, path, f"{location}.provider", source)
            _check_string(
                source_model,
                path,
                f"{location}.source_model_id",
                findings,
                source,
            )
            _check_string(
                target_model,
                path,
                f"{location}.target_model_id",
                findings,
                source,
            )
            approval_profiles = (
                _check_string_list(
                    entry.get("work_profiles"),
                    path,
                    f"{location}.work_profiles",
                    findings,
                    source,
                    allow_empty=True,
                    require_sorted=True,
                )
                or ()
            )
            for approval_profile in approval_profiles:
                if approval_profile not in profile_set:
                    _unknown_reference(
                        findings, path, f"{location}.work_profiles", source
                    )
            _check_string(
                reference,
                path,
                f"{location}.reference",
                findings,
                source,
            )
            reference_valid = reference == FALLBACK_APPROVAL_REFERENCE
            if reference_valid:
                reference_path, _anchor = FALLBACK_APPROVAL_REFERENCE.split("#", 1)
                try:
                    reference_text = _read_root_confined_regular_text(
                        root, pathlib.PurePosixPath(reference_path)
                    )
                except (FileNotFoundError, OSError, UnicodeError, _UnsafeRootFileError):
                    reference_valid = False
                else:
                    reference_valid = bool(
                        re.search(
                            r"(?m)^### Approved Fallback Edges\s*$", reference_text
                        )
                    )
            if not reference_valid:
                _add(
                    findings,
                    "AGC-MODEL-FALLBACK-APPROVAL-REFERENCE",
                    path,
                    f"{location}.reference",
                    "resolvable-approved-fallback-edge-authority",
                    "missing-or-wrong-fallback-authority",
                    source,
                )
    _check_sorted_unique_ids(approval_ids, path, "fallback_approvals", findings, source)

    evidence = _as_sequence(
        document.get("cutoff_evidence"),
        path,
        "cutoff_evidence",
        findings,
        source,
    )
    evidence_ids: list[str] = []
    evidence_entries: dict[str, Mapping[str, object]] = {}
    if evidence is not None:
        for index, raw in enumerate(evidence):
            location = f"cutoff_evidence[{index}]"
            entry = _check_fields(
                raw,
                CUTOFF_EVIDENCE_FIELDS,
                path,
                location,
                findings,
                source,
            )
            if entry is None:
                continue
            evidence_id = entry.get("evidence_id")
            provider = entry.get("provider")
            source_url = entry.get("source_url")
            published_at = entry.get("published_at")
            observed_at = entry.get("observed_at")
            if _check_string(
                evidence_id,
                path,
                f"{location}.evidence_id",
                findings,
                source,
            ):
                evidence_ids.append(str(evidence_id))
                evidence_entries[str(evidence_id)] = entry
            if not _is_registered_string(provider, provider_set):
                _unknown_reference(findings, path, f"{location}.provider", source)
            source_valid = _check_source_url(
                source_url,
                path,
                f"{location}.source_url",
                findings,
                source,
            )
            if source_valid:
                hostname = (urlparse(str(source_url)).hostname or "").lower()
                allowed_hosts = PROVIDER_OFFICIAL_EVIDENCE_HOSTS.get(str(provider), ())
                if hostname not in allowed_hosts:
                    _add(
                        findings,
                        "AGC-MODEL-CUTOFF-EVIDENCE-SOURCE",
                        path,
                        f"{location}.source_url",
                        "provider-allowlisted-official-domain",
                        "unofficial-evidence-domain",
                        source,
                    )
            _check_checked_at(
                published_at,
                path,
                f"{location}.published_at",
                findings,
                source,
            )
            _check_checked_at(
                observed_at,
                path,
                f"{location}.observed_at",
                findings,
                source,
            )
            try:
                published = dt.datetime.fromisoformat(str(published_at))
                observed = dt.datetime.fromisoformat(str(observed_at))
            except ValueError:
                published = None
                observed = None
            if (
                published is None
                or observed is None
                or cutoff_at is None
                or published.tzinfo is None
                or observed.tzinfo is None
                or cutoff_at.tzinfo is None
                or published > cutoff_at
                or observed_at != document.get("retrieved_at")
            ):
                _add(
                    findings,
                    "AGC-MODEL-CUTOFF-EVIDENCE-DATE",
                    path,
                    location,
                    "published-at-or-before-cutoff-and-observed-at-retrieval",
                    "unbound-or-backdated-evidence-time",
                    source,
                )
    _check_sorted_unique_ids(evidence_ids, path, "cutoff_evidence", findings, source)

    models = _as_sequence(document.get("models"), path, "models", findings, source)
    model_keys: list[tuple[str, str]] = []
    model_entries: dict[tuple[str, str], Mapping[str, object]] = {}
    referenced_approval_ids: set[str] = set()
    referenced_evidence_ids: set[str] = set()
    if models is not None:
        for index, raw in enumerate(models):
            location = f"models[{index}]"
            model_fields = (
                MODEL_CLAUDE_FIELDS
                if isinstance(raw, Mapping) and raw.get("provider") == "claude"
                else MODEL_REASONING_FIELDS
            )
            entry = _check_fields(raw, model_fields, path, location, findings, source)
            if entry is None:
                continue
            provider = entry.get("provider")
            model_id = entry.get("model_id")
            if not _is_registered_string(provider, provider_set):
                _unknown_reference(findings, path, f"{location}.provider", source)
            if _check_string(model_id, path, f"{location}.model_id", findings, source):
                if "latest" in str(model_id).lower():
                    _add(
                        findings,
                        "AGC-MODEL-FLOATING-ALIAS",
                        path,
                        f"{location}.model_id",
                        "pinned-model-id",
                        "floating-model-id",
                        source,
                    )
            _check_string(
                entry.get("canonical_model_id"),
                path,
                f"{location}.canonical_model_id",
                findings,
                source,
            )
            if isinstance(provider, str) and isinstance(model_id, str):
                key = (provider, model_id)
                model_keys.append(key)
                model_entries[key] = entry
            status_valid = _check_enum(
                entry.get("provider_status"),
                MODEL_STATES,
                path,
                f"{location}.provider_status",
                findings,
                source,
                code="AGC-PROVIDER-INVALID-STATE",
            )
            normalized_status = entry.get("normalized_status")
            normalized_valid = _check_enum(
                normalized_status,
                NORMALIZED_MODEL_STATES,
                path,
                f"{location}.normalized_status",
                findings,
                source,
                code="AGC-PROVIDER-INVALID-STATE",
            )
            expected_normalized = {
                "active": "stable",
                "current": "stable",
                "deprecated": "deprecated",
                "generally-available": "stable",
                "limited-availability": "limited",
                "listed": "unclassified-listed",
                "preview": "preview",
                "stable": "stable",
            }.get(entry.get("provider_status"))
            if (
                status_valid
                and normalized_valid
                and normalized_status != expected_normalized
            ):
                _add(
                    findings,
                    "AGC-MODEL-STATUS-NORMALIZATION",
                    path,
                    f"{location}.normalized_status",
                    "evidence-backed-normalization",
                    "status-normalization-mismatch",
                    source,
                )
            eligible = entry.get("repository_default_eligible")
            _check_bool(
                eligible,
                path,
                f"{location}.repository_default_eligible",
                findings,
                source,
            )
            if (
                normalized_valid
                and eligible is True
                and normalized_status
                not in {
                    "current",
                    "stable",
                    "unclassified-listed",
                }
            ):
                _add(
                    findings,
                    "AGC-MODEL-INELIGIBLE-STATUS",
                    path,
                    f"{location}.repository_default_eligible",
                    "current-or-stable-model-only",
                    "ineligible-normalized-status",
                    source,
                )
            _check_enum(
                entry.get("entitlement"),
                ENTITLEMENT_STATES,
                path,
                f"{location}.entitlement",
                findings,
                source,
                code="AGC-PROVIDER-INVALID-STATE",
            )
            _check_enum(
                entry.get("runtime_acceptance"),
                RUNTIME_ACCEPTANCE_STATES,
                path,
                f"{location}.runtime_acceptance",
                findings,
                source,
                code="AGC-PROVIDER-INVALID-STATE",
            )
            if provider == "claude":
                _check_enum(
                    entry.get("thinking_control_kind"),
                    REASONING_CONTROL_KINDS,
                    path,
                    f"{location}.thinking_control_kind",
                    findings,
                    source,
                )
                for prefix in ("thinking", "effort"):
                    supported_controls = (
                        _check_string_list(
                            entry.get(f"supported_{prefix}_controls"),
                            path,
                            f"{location}.supported_{prefix}_controls",
                            findings,
                            source,
                            require_sorted=True,
                            allow_empty=True,
                        )
                        or ()
                    )
                    repository_controls = (
                        _check_string_list(
                            entry.get(f"repository_{prefix}_controls"),
                            path,
                            f"{location}.repository_{prefix}_controls",
                            findings,
                            source,
                            require_sorted=True,
                            allow_empty=True,
                        )
                        or ()
                    )
                    if not set(repository_controls).issubset(supported_controls):
                        _add(
                            findings,
                            "AGC-MODEL-REASONING-POLICY",
                            path,
                            f"{location}.repository_{prefix}_controls",
                            "subset-of-provider-supported-controls",
                            "unsupported-repository-control",
                            source,
                        )
            else:
                _check_enum(
                    entry.get("reasoning_control_kind"),
                    REASONING_CONTROL_KINDS,
                    path,
                    f"{location}.reasoning_control_kind",
                    findings,
                    source,
                )
                supported_controls = (
                    _check_string_list(
                        entry.get("supported_reasoning_controls"),
                        path,
                        f"{location}.supported_reasoning_controls",
                        findings,
                        source,
                        require_sorted=True,
                        allow_empty=True,
                    )
                    or ()
                )
                repository_controls = (
                    _check_string_list(
                        entry.get("repository_reasoning_controls"),
                        path,
                        f"{location}.repository_reasoning_controls",
                        findings,
                        source,
                        require_sorted=True,
                        allow_empty=True,
                    )
                    or ()
                )
                if not set(repository_controls).issubset(supported_controls):
                    _add(
                        findings,
                        "AGC-MODEL-REASONING-POLICY",
                        path,
                        f"{location}.repository_reasoning_controls",
                        "subset-of-provider-supported-controls",
                        "unsupported-repository-control",
                        source,
                    )
            profiles = (
                _check_string_list(
                    entry.get("work_profiles"),
                    path,
                    f"{location}.work_profiles",
                    findings,
                    source,
                    require_sorted=True,
                    allow_empty=True,
                )
                or ()
            )
            for profile in profiles:
                if profile not in profile_set:
                    _unknown_reference(
                        findings, path, f"{location}.work_profiles", source
                    )
            _check_enum(
                entry.get("agent_coding_fit"),
                AGENT_CODING_FITS,
                path,
                f"{location}.agent_coding_fit",
                findings,
                source,
            )
            _check_string_list(
                entry.get("task_characteristics"),
                path,
                f"{location}.task_characteristics",
                findings,
                source,
                require_sorted=True,
            )
            _check_string(
                entry.get("fallback"), path, f"{location}.fallback", findings, source
            )
            _check_enum(
                entry.get("fallback_policy"),
                FALLBACK_POLICIES,
                path,
                f"{location}.fallback_policy",
                findings,
                source,
            )
            approval = entry.get("fallback_approval")
            if entry.get("fallback_policy") == "approved-degraded":
                _check_string(
                    approval,
                    path,
                    f"{location}.fallback_approval",
                    findings,
                    source,
                )
                approval_entry = approval_entries.get(str(approval))
                if approval_entry is None:
                    _add(
                        findings,
                        "AGC-MODEL-FALLBACK-APPROVAL-REFERENCE",
                        path,
                        f"{location}.fallback_approval",
                        "registered-fallback-approval",
                        "missing-fallback-approval",
                        source,
                    )
                else:
                    referenced_approval_ids.add(str(approval))
                    expected_profiles = tuple(
                        item
                        for item in _sequence_or_empty(entry.get("work_profiles"))
                        if isinstance(item, str)
                    )
                    approval_profiles = tuple(
                        item
                        for item in _sequence_or_empty(
                            approval_entry.get("work_profiles")
                        )
                        if isinstance(item, str)
                    )
                    if (
                        approval_entry.get("provider") != provider
                        or approval_entry.get("source_model_id") != model_id
                        or approval_entry.get("target_model_id")
                        != entry.get("fallback")
                        or approval_profiles != expected_profiles
                    ):
                        _add(
                            findings,
                            "AGC-MODEL-FALLBACK-APPROVAL-EDGE",
                            path,
                            f"{location}.fallback_approval",
                            "exact-provider-source-target-profile-edge",
                            "fallback-approval-edge-mismatch",
                            source,
                        )
            elif approval is not None:
                _add(
                    findings,
                    "AGC-MODEL-FALLBACK-POLICY",
                    path,
                    f"{location}.fallback_approval",
                    "null-for-same-profile",
                    "unexpected-fallback-approval",
                    source,
                )
            _check_enum(
                entry.get("cutoff_evidence_status"),
                CUTOFF_EVIDENCE_STATES,
                path,
                f"{location}.cutoff_evidence_status",
                findings,
                source,
            )
            evidence_id = entry.get("cutoff_evidence_id")
            _check_checked_at(
                entry.get("checked_at"),
                path,
                f"{location}.checked_at",
                findings,
                source,
            )
            _check_source_url(
                entry.get("source_url"),
                path,
                f"{location}.source_url",
                findings,
                source,
            )
            if entry.get("checked_at") != document.get("retrieved_at"):
                _add(
                    findings,
                    "AGC-SOURCE-OBSERVATION-ORDER",
                    path,
                    f"{location}.checked_at",
                    "equal-to-retrieved-at",
                    "model-observation-time-mismatch",
                    source,
                )
            if entry.get("cutoff_evidence_status") == "verified-before-cutoff":
                evidence_entry = evidence_entries.get(str(evidence_id))
                if not isinstance(evidence_id, str) or evidence_entry is None:
                    _add(
                        findings,
                        "AGC-MODEL-CUTOFF-EVIDENCE-REFERENCE",
                        path,
                        f"{location}.cutoff_evidence_id",
                        "registered-dated-official-evidence",
                        "missing-cutoff-evidence-reference",
                        source,
                    )
                else:
                    referenced_evidence_ids.add(evidence_id)
                    if evidence_entry.get("provider") != provider:
                        _add(
                            findings,
                            "AGC-MODEL-CUTOFF-EVIDENCE-REFERENCE",
                            path,
                            f"{location}.cutoff_evidence_id",
                            "same-provider-evidence-reference",
                            "provider-evidence-mismatch",
                            source,
                        )
            elif evidence_id is not None:
                _add(
                    findings,
                    "AGC-MODEL-CUTOFF-EVIDENCE-REFERENCE",
                    path,
                    f"{location}.cutoff_evidence_id",
                    "null-for-unverified-historical-state",
                    "unverified-model-has-evidence-reference",
                    source,
                )
    if len(model_keys) != len(set(model_keys)):
        _add(
            findings,
            "AGC-MODEL-DUPLICATE-ID",
            path,
            "models",
            "unique-provider-model-pairs",
            "duplicate-provider-model-pair",
            source,
        )
    if model_keys != sorted(model_keys):
        _add(
            findings,
            "AGC-SCHEMA-NONDETERMINISTIC-ORDER",
            path,
            "models",
            "provider-model-order",
            "non-provider-model-order",
            source,
        )
    for approval_id in sorted(set(approval_entries) - referenced_approval_ids):
        _add(
            findings,
            "AGC-MODEL-FALLBACK-APPROVAL-EDGE",
            path,
            "fallback_approvals",
            "one-model-edge-per-approval",
            "unreferenced-fallback-approval",
            source,
        )
    for evidence_id in sorted(set(evidence_entries) - referenced_evidence_ids):
        _add(
            findings,
            "AGC-MODEL-CUTOFF-EVIDENCE-REFERENCE",
            path,
            "cutoff_evidence",
            "referenced-model-evidence",
            "unreferenced-cutoff-evidence",
            source,
        )
    for key, entry in model_entries.items():
        fallback_key = (key[0], str(entry.get("fallback")))
        fallback = model_entries.get(fallback_key)
        if fallback is None:
            _unknown_reference(
                findings, path, f"models.{key[0]}.{key[1]}.fallback", source
            )
        elif fallback.get("repository_default_eligible") is not True:
            _add(
                findings,
                "AGC-MODEL-INELIGIBLE-FALLBACK",
                path,
                f"models.{key[0]}.{key[1]}.fallback",
                "eligible-same-provider-fallback",
                "ineligible-fallback",
                source,
            )
        else:
            source_profiles = {
                item
                for item in _sequence_or_empty(entry.get("work_profiles"))
                if isinstance(item, str)
            }
            fallback_profiles = {
                item
                for item in _sequence_or_empty(fallback.get("work_profiles"))
                if isinstance(item, str)
            }
            same_profile = bool(source_profiles) and source_profiles.issubset(
                fallback_profiles
            )
            policy = entry.get("fallback_policy")
            if same_profile and policy != "same-profile":
                _add(
                    findings,
                    "AGC-MODEL-FALLBACK-POLICY",
                    path,
                    f"models.{key[0]}.{key[1]}.fallback_policy",
                    "same-profile-policy",
                    "unnecessary-degradation-policy",
                    source,
                )
            if not same_profile and policy != "approved-degraded":
                _add(
                    findings,
                    "AGC-MODEL-FALLBACK-POLICY",
                    path,
                    f"models.{key[0]}.{key[1]}.fallback_policy",
                    "approved-degraded-policy",
                    "unapproved-profile-degradation",
                    source,
                )
    for profile_id, provider, model_id, reasoning, effort in profile_defaults:
        model = model_entries.get((provider, model_id))
        if model is None:
            _unknown_reference(
                findings,
                path,
                f"work_profiles.{profile_id}.defaults.{provider}.model_id",
                source,
            )
            continue
        if model.get("repository_default_eligible") is not True:
            _add(
                findings,
                "AGC-MODEL-INELIGIBLE-DEFAULT",
                path,
                f"work_profiles.{profile_id}.defaults.{provider}.model_id",
                "eligible-default-model",
                "ineligible-default-model",
                source,
            )
        if provider == "claude":
            efforts = _sequence_or_empty(model.get("repository_effort_controls"))
            if effort is not None and effort not in efforts:
                _add(
                    findings,
                    "AGC-MODEL-REASONING-MISMATCH",
                    path,
                    f"work_profiles.{profile_id}.defaults.{provider}",
                    "model-supported-native-agent-effort",
                    "unsupported-native-agent-effort",
                    source,
                )
        else:
            controls = _sequence_or_empty(model.get("repository_reasoning_controls"))
            if reasoning not in controls:
                _add(
                    findings,
                    "AGC-MODEL-REASONING-MISMATCH",
                    path,
                    f"work_profiles.{profile_id}.defaults.{provider}.reasoning",
                    "model-supported-reasoning",
                    "unsupported-reasoning",
                    source,
                )
        profiles = _sequence_or_empty(model.get("work_profiles"))
        if profile_id not in profiles:
            _add(
                findings,
                "AGC-MODEL-PROFILE-MISMATCH",
                path,
                f"work_profiles.{profile_id}.defaults.{provider}.model_id",
                "model-profile-membership",
                "missing-model-profile",
                source,
            )

    loops = _as_sequence(
        document.get("harness_loops"), path, "harness_loops", findings, source
    )
    loop_ids: list[str] = []
    if loops is not None:
        for index, raw in enumerate(loops):
            location = f"harness_loops[{index}]"
            entry = _check_fields(
                raw, HARNESS_LOOP_FIELDS, path, location, findings, source
            )
            if entry is None:
                continue
            event_id = entry.get("event_id")
            if _check_string(event_id, path, f"{location}.event_id", findings, source):
                loop_ids.append(str(event_id))
            for field in (
                "owner_agent",
                "reviewer_agent",
                "stop_condition",
                "on_failure",
            ):
                _check_string(
                    entry.get(field), path, f"{location}.{field}", findings, source
                )
            if isinstance(entry.get("owner_agent"), str) and entry.get(
                "owner_agent"
            ) == entry.get("reviewer_agent"):
                _add(
                    findings,
                    "AGC-LOOP-REVIEWER-INDEPENDENCE",
                    path,
                    f"{location}.reviewer_agent",
                    "independent-reviewer",
                    "owner-reviewer-identity-collision",
                    source,
                )
            permission = entry.get("permission_profile")
            _check_enum(
                permission,
                set(LOOP_PERMISSION_TOOLS),
                path,
                f"{location}.permission_profile",
                findings,
                source,
            )
            allowed_tools = (
                _check_string_list(
                    entry.get("allowed_tools"),
                    path,
                    f"{location}.allowed_tools",
                    findings,
                    source,
                    require_sorted=True,
                )
                or ()
            )
            if not set(allowed_tools).issubset(
                LOOP_PERMISSION_TOOLS.get(str(permission), frozenset())
            ):
                _add(
                    findings,
                    "AGC-LOOP-LEAST-PRIVILEGE",
                    path,
                    f"{location}.allowed_tools",
                    "permission-bounded-tool-set",
                    "tool-outside-permission-profile",
                    source,
                )
            attempts = entry.get("max_attempts")
            if (
                isinstance(attempts, bool)
                or not isinstance(attempts, int)
                or attempts <= 0
            ):
                _add(
                    findings,
                    "AGC-LOOP-ATTEMPT-BOUND",
                    path,
                    f"{location}.max_attempts",
                    "positive-bounded-attempt-count",
                    "invalid-attempt-bound",
                    source,
                )
            expected = EXPECTED_HARNESS_LOOPS.get(str(event_id))
            if (
                expected is None
                or (
                    attempts,
                    entry.get("stop_condition"),
                    entry.get("on_failure"),
                )
                != expected
            ):
                _add(
                    findings,
                    "AGC-LOOP-SEMANTICS",
                    path,
                    location,
                    "registered-attempt-stop-failure-contract",
                    "loop-contract-mismatch",
                    source,
                )
            evidence_fields = _check_string_list(
                entry.get("evidence_fields"),
                path,
                f"{location}.evidence_fields",
                findings,
                source,
                require_sorted=True,
            )
            prohibited = _check_string_list(
                entry.get("prohibited_evidence"),
                path,
                f"{location}.prohibited_evidence",
                findings,
                source,
                require_sorted=True,
            )
            if (
                tuple(evidence_fields or ()) != SANITIZED_EVIDENCE_FIELDS
                or tuple(prohibited or ()) != PROHIBITED_EVIDENCE_FIELDS
            ):
                _add(
                    findings,
                    "AGC-LOOP-EVIDENCE",
                    path,
                    location,
                    "exact-sanitized-evidence-contract",
                    "unsafe-or-incomplete-evidence-contract",
                    source,
                )
            _check_enum(
                entry.get("capability_status"),
                PROVIDER_CAPABILITY_STATES,
                path,
                f"{location}.capability_status",
                findings,
                source,
                code="AGC-PROVIDER-INVALID-STATE",
            )
            _check_enum(
                entry.get("adoption_status"),
                PROVIDER_ADOPTION_STATES,
                path,
                f"{location}.adoption_status",
                findings,
                source,
                code="AGC-PROVIDER-INVALID-STATE",
            )
            _check_enum(
                entry.get("runtime_depth"),
                RUNTIME_DEPTH_STATES,
                path,
                f"{location}.runtime_depth",
                findings,
                source,
            )
            if (
                entry.get("capability_status") != "supported"
                or entry.get("adoption_status") != "adopted"
                or entry.get("runtime_depth") != "repository-enforced"
            ):
                _add(
                    findings,
                    "AGC-LOOP-ADOPTION-DEPTH",
                    path,
                    location,
                    "supported-adopted-repository-enforced",
                    "loop-adoption-depth-mismatch",
                    source,
                )
    _check_sorted_unique_ids(loop_ids, path, "harness_loops", findings, source)
    if set(loop_ids) != set(EXPECTED_HARNESS_LOOPS):
        _add(
            findings,
            "AGC-LOOP-COVERAGE",
            path,
            "harness_loops",
            "exact-semantic-loop-set",
            "semantic-loop-set-mismatch",
            source,
        )

    events = _as_sequence(
        document.get("semantic_events"), path, "semantic_events", findings, source
    )
    event_ids: list[str] = []
    if events is not None:
        for index, raw in enumerate(events):
            location = f"semantic_events[{index}]"
            entry = _check_fields(raw, EVENT_FIELDS, path, location, findings, source)
            if entry is None:
                continue
            event_id = entry.get("event_id")
            if _check_string(event_id, path, f"{location}.event_id", findings, source):
                event_ids.append(str(event_id))
            _check_bool(
                entry.get("required"), path, f"{location}.required", findings, source
            )
            bindings = _as_sequence(
                entry.get("provider_bindings"),
                path,
                f"{location}.provider_bindings",
                findings,
                source,
            )
            binding_providers: list[str] = []
            if bindings is not None:
                for binding_index, raw_binding in enumerate(bindings):
                    binding_location = f"{location}.provider_bindings[{binding_index}]"
                    binding = _check_fields(
                        raw_binding,
                        EVENT_BINDING_FIELDS,
                        path,
                        binding_location,
                        findings,
                        source,
                    )
                    if binding is None:
                        continue
                    provider = binding.get("provider")
                    if _check_string(
                        provider, path, f"{binding_location}.provider", findings, source
                    ):
                        binding_providers.append(str(provider))
                    if not _is_registered_string(provider, provider_set):
                        _unknown_reference(
                            findings, path, f"{binding_location}.provider", source
                        )
                    capability = binding.get("capability_status")
                    _check_enum(
                        capability,
                        PROVIDER_CAPABILITY_STATES,
                        path,
                        f"{binding_location}.capability_status",
                        findings,
                        source,
                        code="AGC-PROVIDER-INVALID-STATE",
                    )
                    native_event = binding.get("native_event")
                    if capability == "unsupported":
                        if native_event is not None:
                            _add(
                                findings,
                                "AGC-EVENT-UNSUPPORTED-NATIVE",
                                path,
                                f"{binding_location}.native_event",
                                "null-for-unsupported",
                                "native-event-present",
                                source,
                            )
                    else:
                        _check_string(
                            native_event,
                            path,
                            f"{binding_location}.native_event",
                            findings,
                            source,
                        )
                    _check_enum(
                        binding.get("adoption_status"),
                        PROVIDER_ADOPTION_STATES,
                        path,
                        f"{binding_location}.adoption_status",
                        findings,
                        source,
                        code="AGC-PROVIDER-INVALID-STATE",
                    )
                    runtime_depth = binding.get("runtime_depth")
                    _check_enum(
                        runtime_depth,
                        RUNTIME_DEPTH_STATES,
                        path,
                        f"{binding_location}.runtime_depth",
                        findings,
                        source,
                    )
                    expected_depth = (
                        "unsupported"
                        if capability == "unsupported"
                        else "configured-not-executed"
                    )
                    if runtime_depth != expected_depth:
                        _add(
                            findings,
                            "AGC-EVENT-RUNTIME-DEPTH",
                            path,
                            f"{binding_location}.runtime_depth",
                            "honest-configured-runtime-depth",
                            "runtime-depth-mismatch",
                            source,
                        )
                    can_block = binding.get("provider_can_block")
                    _check_bool(
                        can_block,
                        path,
                        f"{binding_location}.provider_can_block",
                        findings,
                        source,
                    )
                    hook_mode = binding.get("repository_hook_mode")
                    _check_enum(
                        hook_mode,
                        REPOSITORY_HOOK_MODES,
                        path,
                        f"{binding_location}.repository_hook_mode",
                        findings,
                        source,
                    )
                    expected_mode = EXPECTED_REPOSITORY_HOOK_MODES.get(
                        (str(event_id), str(provider))
                    )
                    if expected_mode is None or hook_mode != expected_mode:
                        _add(
                            findings,
                            "AGC-EVENT-SEMANTICS",
                            path,
                            f"{binding_location}.repository_hook_mode",
                            "exact-provider-event-repository-mode",
                            "provider-event-mode-mismatch",
                            source,
                        )
                    if capability == "unsupported" and (
                        can_block is not False or hook_mode != "unsupported"
                    ):
                        _add(
                            findings,
                            "AGC-EVENT-UNSUPPORTED-MODE",
                            path,
                            binding_location,
                            "unsupported-nonblocking-binding",
                            "unsupported-binding-mode-mismatch",
                            source,
                        )
                    if hook_mode == "blocking" and can_block is not True:
                        _add(
                            findings,
                            "AGC-EVENT-BLOCKING-MISMATCH",
                            path,
                            f"{binding_location}.repository_hook_mode",
                            "provider-block-capability",
                            "blocking-without-capability",
                            source,
                        )
                    if hook_mode == "retry" and can_block is not True:
                        _add(
                            findings,
                            "AGC-EVENT-BLOCKING-MISMATCH",
                            path,
                            f"{binding_location}.repository_hook_mode",
                            "provider-retry-capability",
                            "retry-without-capability",
                            source,
                        )
                    if hook_mode == "deny-retry" and can_block is not True:
                        _add(
                            findings,
                            "AGC-EVENT-BLOCKING-MISMATCH",
                            path,
                            f"{binding_location}.repository_hook_mode",
                            "provider-deny-retry-capability",
                            "deny-retry-without-capability",
                            source,
                        )
                    if (
                        event_id == "stop"
                        and provider == "gemini"
                        and (
                            native_event != "AfterAgent"
                            or can_block is not True
                            or hook_mode != "deny-retry"
                        )
                    ):
                        _add(
                            findings,
                            "AGC-EVENT-SEMANTICS",
                            path,
                            binding_location,
                            "gemini-after-agent-deny-retry",
                            "underreported-or-mismapped-after-agent",
                            source,
                        )
                    timeout_unit = binding.get("timeout_unit")
                    _check_enum(
                        timeout_unit,
                        TIMEOUT_UNITS,
                        path,
                        f"{binding_location}.timeout_unit",
                        findings,
                        source,
                    )
                    expected_unit = (
                        "milliseconds" if provider == "gemini" else "seconds"
                    )
                    if isinstance(provider, str) and timeout_unit != expected_unit:
                        _add(
                            findings,
                            "AGC-EVENT-TIMEOUT-UNIT",
                            path,
                            f"{binding_location}.timeout_unit",
                            "provider-native-time-unit",
                            "timeout-unit-mismatch",
                            source,
                        )
                    timeout_value = binding.get("timeout_value")
                    if (
                        isinstance(timeout_value, bool)
                        or not isinstance(timeout_value, int)
                        or timeout_value <= 0
                    ):
                        _add(
                            findings,
                            "AGC-EVENT-TIMEOUT-VALUE",
                            path,
                            f"{binding_location}.timeout_value",
                            "positive-integer",
                            "invalid-timeout-value",
                            source,
                        )
            _check_sorted_unique_ids(
                binding_providers,
                path,
                f"{location}.provider_bindings",
                findings,
                source,
            )
            if set(binding_providers) != provider_set:
                _add(
                    findings,
                    "AGC-EVENT-PROVIDER-COVERAGE",
                    path,
                    f"{location}.provider_bindings",
                    "exact-provider-set",
                    "provider-set-mismatch",
                    source,
                )
    _check_sorted_unique_ids(event_ids, path, "semantic_events", findings, source)


def validate_contract_bundle(
    root: pathlib.Path, bundle: ContractBundle
) -> list[Finding]:
    """Validate contract schema, identities, references, and deterministic policy."""

    findings: list[Finding] = []
    _validate_artifact_contract(bundle.artifacts, findings)
    _validate_provider_contract(root, bundle.providers, findings)
    _validate_catalog_contract(
        bundle.catalog, bundle.providers, bundle.artifacts, findings
    )
    return sorted(findings, key=finding_sort_key)


class _BracePatternError(ValueError):
    """Signal unsupported or resource-unsafe simple brace grammar."""


def _parse_brace_groups(pattern: str) -> tuple[tuple[str, tuple[str, ...]], ...]:
    """Parse bounded non-nested groups without materializing expanded paths."""

    if len(pattern) > MAX_PATTERN_LENGTH:
        raise _BracePatternError("pattern length limit")
    groups: list[tuple[str, tuple[str, ...]]] = []
    literal_start = 0
    index = 0
    while index < len(pattern):
        character = pattern[index]
        if character == "}":
            raise _BracePatternError("unmatched brace")
        if character != "{":
            index += 1
            continue

        if len(groups) >= MAX_BRACE_GROUPS:
            raise _BracePatternError("brace group limit")
        brace_end = pattern.find("}", index + 1)
        if brace_end < 0:
            raise _BracePatternError("unmatched brace")
        choice_text = pattern[index + 1 : brace_end]
        if "{" in choice_text:
            raise _BracePatternError("nested brace")
        raw_choices = choice_text.split(",")
        if len(raw_choices) < 2 or any(not choice for choice in raw_choices):
            raise _BracePatternError("invalid brace choices")
        choices = tuple(dict.fromkeys(raw_choices))
        groups.append((pattern[literal_start:index], choices))
        index = brace_end + 1
        literal_start = index

    return tuple(groups)


def _expand_braces(pattern: str) -> tuple[str, ...]:
    """Expand bounded simple braces iteratively with stable early deduplication."""

    groups = _parse_brace_groups(pattern)
    if not groups:
        return (pattern,)

    partials: tuple[str, ...] = ("",)
    for literal, choices in groups:
        next_partials: dict[str, None] = {}
        for partial in partials:
            base = partial + literal
            for choice in choices:
                next_partials.setdefault(base + choice, None)
                if len(next_partials) > MAX_EXPANDED_PATHS:
                    raise _BracePatternError("expanded path limit")
        partials = tuple(next_partials)

    final_brace_end = pattern.rfind("}")
    suffix = pattern[final_brace_end + 1 :]
    return tuple(partial + suffix for partial in partials)


def _segment_patterns_overlap(left: str, right: str) -> bool:
    """Return false only when two single-segment globs are provably disjoint."""

    markers = "*?["
    left_glob = any(marker in left for marker in markers)
    right_glob = any(marker in right for marker in markers)
    if not left_glob and not right_glob:
        return left == right
    if not left_glob:
        return fnmatch.fnmatchcase(left, right)
    if not right_glob:
        return fnmatch.fnmatchcase(right, left)

    # Two wildcard-bearing segment languages are conservatively treated as
    # intersecting. Unsupported constructs are rejected by the schema; this
    # fail-closed branch prevents a false disjoint result for character classes.
    return True


def _simple_glob_patterns_overlap(left: str, right: str) -> bool:
    left_parts = left.split("/")
    right_parts = right.split("/")
    for left_part, right_part in zip(left_parts, right_parts):
        if left_part == "**" or right_part == "**":
            return True
        if not _segment_patterns_overlap(left_part, right_part):
            return False
    if len(left_parts) == len(right_parts):
        return True
    remainder = (
        left_parts[len(right_parts) :]
        if len(left_parts) > len(right_parts)
        else right_parts[len(left_parts) :]
    )
    return all(part == "**" for part in remainder)


def _artifact_patterns_overlap(left: str, right: str) -> bool:
    """Fail closed when artifact glob intersection cannot be disproved."""

    try:
        left_expanded_patterns = _expand_braces(_canonical_repo_path(left))
        right_expanded_patterns = _expand_braces(_canonical_repo_path(right))
    except _BracePatternError:
        return True
    return any(
        _simple_glob_patterns_overlap(left_expanded, right_expanded)
        for left_expanded in left_expanded_patterns
        for right_expanded in right_expanded_patterns
    )


def normalize_repo_relative_path(path: str | pathlib.PurePath) -> str:
    """Remove one literal ``./`` prefix without stripping dot-directory names."""

    text = path.as_posix() if isinstance(path, pathlib.PurePath) else str(path)
    return text.removeprefix("./")


def _path_matches_pattern(relative: str, pattern: str) -> bool:
    path_parts = relative.split("/")

    try:
        expanded_patterns = _expand_braces(pattern)
    except _BracePatternError:
        return False
    for expanded in expanded_patterns:
        reachable: set[int] = {0}
        for segment in expanded.split("/"):
            if not reachable:
                break
            if segment == "**":
                reachable = set(range(min(reachable), len(path_parts) + 1))
                continue
            reachable = {
                path_index + 1
                for path_index in reachable
                if path_index < len(path_parts)
                and fnmatch.fnmatchcase(path_parts[path_index], segment)
            }
        if len(path_parts) in reachable:
            return True
    return False


def path_matches_artifact_pattern(
    relative: str | pathlib.PurePath, pattern: str
) -> bool:
    """Match a bounded artifact pattern against one full repository-relative path."""

    normalized = normalize_repo_relative_path(relative)
    if not _is_safe_repo_path(normalized) or not _is_supported_enumerated_pattern(
        pattern
    ):
        return False
    try:
        expanded_patterns = _expand_braces(pattern)
    except _BracePatternError:
        return False
    if not all(_is_safe_repo_path(expanded) for expanded in expanded_patterns):
        return False
    return _path_matches_pattern(normalized, pattern)


@dataclass(frozen=True)
class _RegisteredPathInventory:
    paths: tuple[pathlib.Path, ...]
    missing_exact: tuple[str, ...]
    has_glob: bool
    enumeration_failed: bool


def _registered_paths(root: pathlib.Path, pattern: str) -> _RegisteredPathInventory:
    """Resolve a profile pattern without dropping required exact alternatives."""

    paths: set[pathlib.Path] = set()
    missing_exact: set[str] = set()
    has_glob = False
    enumeration_failed = False
    try:
        expanded_patterns = _expand_braces(pattern)
    except _BracePatternError:
        return _RegisteredPathInventory((), (), False, True)
    for expanded in sorted(expanded_patterns):
        if any(marker in expanded for marker in ("*", "?", "[")):
            has_glob = True
            try:
                paths.update(root.glob(expanded))
            except (OSError, ValueError):
                enumeration_failed = True
        else:
            candidate = root / expanded
            if candidate.exists() or candidate.is_symlink():
                paths.add(candidate)
            else:
                missing_exact.add(expanded)
    return _RegisteredPathInventory(
        paths=tuple(sorted(paths, key=lambda item: item.relative_to(root).as_posix())),
        missing_exact=tuple(sorted(missing_exact)),
        has_glob=has_glob,
        enumeration_failed=enumeration_failed,
    )


class _RepositoryReader:
    """Read repository text through one fail-closed, value-free boundary."""

    def __init__(self, root: pathlib.Path, findings: list[Finding]) -> None:
        self.root = root
        self.findings = findings
        self._cache: dict[str, str | None] = {}
        self._enumeration_cache: dict[str, _RegisteredPathInventory] = {}

    def inventory(
        self, pattern: str, location: str, source: str
    ) -> _RegisteredPathInventory:
        if pattern in self._enumeration_cache:
            return self._enumeration_cache[pattern]
        try:
            inventory = _registered_paths(self.root, pattern)
        except (OSError, ValueError):
            inventory = _RegisteredPathInventory(
                paths=(),
                missing_exact=(),
                has_glob=any(marker in pattern for marker in ("*", "?", "[")),
                enumeration_failed=True,
            )
        if inventory.enumeration_failed:
            _add(
                self.findings,
                "AGC-REPOSITORY-PATH-ENUMERATION",
                pattern,
                location,
                "deterministic-governed-path-enumeration",
                "path-enumeration-failed",
                source,
            )
        self._enumeration_cache[pattern] = inventory
        return inventory

    def paths(
        self, pattern: str, location: str, source: str
    ) -> tuple[pathlib.Path, ...]:
        return self.inventory(pattern, location, source).paths

    def read(
        self,
        relative: str,
        location: str,
        source: str,
        *,
        missing_code: str = "AGC-REPOSITORY-FILE-READ",
        missing_expected: str = "readable-governed-file",
        missing_actual: str = "governed-file-read-failed",
    ) -> str | None:
        if relative in self._cache:
            return self._cache[relative]
        self._cache[relative] = None
        try:
            text = _read_root_confined_regular_text(
                self.root, pathlib.PurePosixPath(relative)
            )
        except FileNotFoundError:
            _add(
                self.findings,
                missing_code,
                relative,
                location,
                missing_expected,
                missing_actual,
                source,
            )
            return None
        except _UnsafeRootFileError:
            _add(
                self.findings,
                "AGC-REPOSITORY-UNSAFE-FILE",
                relative,
                location,
                "inside-root-nonsymlink-regular-file",
                "unsafe-governed-file",
                source,
            )
            return None
        except UnicodeError:
            _add(
                self.findings,
                "AGC-REPOSITORY-FILE-ENCODING",
                relative,
                location,
                "utf-8-text",
                "invalid-text-encoding",
                source,
            )
            return None
        except OSError:
            _add(
                self.findings,
                "AGC-REPOSITORY-FILE-READ",
                relative,
                location,
                "readable-governed-file",
                "governed-file-read-failed",
                source,
            )
            return None
        self._cache[relative] = text
        return text


def _frontmatter(text: str) -> tuple[list[str], Mapping[str, object] | None]:
    if not text.startswith("---\n"):
        return [], {}
    boundary = text.find("\n---\n", 4)
    if boundary < 0:
        return [], None
    try:
        values = yaml.load(text[4:boundary], Loader=_UniqueKeyLoader)
    except (_DuplicateKeyError, _NonStringKeyError, yaml.YAMLError):
        return [], None
    if not isinstance(values, Mapping):
        return [], None
    return [str(key) for key in values], values


def _markdown_body(text: str) -> str:
    if text.startswith("---\n"):
        boundary = text.find("\n---\n", 4)
        if boundary >= 0:
            return text[boundary + 5 :]
    return text


_HTML_NAMESPACE = "http://www.w3.org/1999/xhtml"
_MARKDOWN_HEADING_ATTR = "data-agent-governance-markdown-heading"
_MARKDOWN_LEVEL_ATTR = "data-agent-governance-markdown-level"
_MARKDOWN_BOUNDARY_ATTR = "data-agent-governance-markdown-boundary"
_MARKDOWN_AUTOLINK_ATTR = "data-agent-governance-markdown-autolink"
_README_HIDDEN_HTML_TAGS = frozenset({"code", "pre", "script", "style", "template"})
_SECTION_HIDDEN_ANCESTOR_TAGS = frozenset(
    {"code", "pre", "script", "style", "template"}
)
_SECTION_HIDDEN_DESCENDANT_TAGS = frozenset({"script", "style", "template"})
_HTML_BLOCK_TAGS = frozenset(
    {
        "address",
        "article",
        "aside",
        "blockquote",
        "body",
        "caption",
        "center",
        "colgroup",
        "dd",
        "details",
        "dialog",
        "dir",
        "div",
        "dl",
        "dt",
        "fieldset",
        "figcaption",
        "figure",
        "footer",
        "form",
        "frameset",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "head",
        "header",
        "hgroup",
        "hr",
        "html",
        "iframe",
        "legend",
        "li",
        "main",
        "menu",
        "nav",
        "noframes",
        "ol",
        "optgroup",
        "option",
        "p",
        "pre",
        "search",
        "section",
        "summary",
        "table",
        "tbody",
        "td",
        "tfoot",
        "th",
        "thead",
        "title",
        "tr",
        "ul",
    }
)


def _markdown_parser() -> object:
    if (
        _MarkdownIt is None
    ):  # guarded by load_contract_bundle; keeps helpers fail closed
        raise ContractLoadError(
            "AGC-DEPENDENCY-MISSING", "markdown-it-py", "validation-runtime"
        )
    return _MarkdownIt("commonmark", {"html": True})


def _html_fragment(markup: str) -> object:
    if _html5lib is None:  # guarded by load_contract_bundle; keeps helpers fail closed
        raise ContractLoadError(
            "AGC-DEPENDENCY-MISSING", "html5lib", "validation-runtime"
        )
    return _html5lib.parseFragment(markup, container="div")


def _token_stream(tokens: Sequence[object]) -> Sequence[object]:
    flattened: list[object] = []
    pending = list(reversed(tokens))
    while pending:
        token = pending.pop()
        flattened.append(token)
        children = getattr(token, "children", None) or ()
        pending.extend(reversed(children))
    return tuple(flattened)


def _markdown_dom(text: str) -> tuple[object, str]:
    """Render strict CommonMark and parse it with WHATWG tree construction."""

    markdown = _markdown_parser()
    tokens = markdown.parse(_markdown_body(text))
    raw_markup = markdown.renderer.render(tokens, markdown.options, {})
    raw_dom = _html_fragment(raw_markup)
    marker_values = {
        value
        for element in raw_dom.iter()
        for attr in (
            _MARKDOWN_HEADING_ATTR,
            _MARKDOWN_BOUNDARY_ATTR,
            _MARKDOWN_AUTOLINK_ATTR,
        )
        if isinstance((value := element.attrib.get(attr)), str)
    }
    attempt = 0
    while True:
        marker = f"{secrets.token_hex(16)}-{attempt}"
        if marker not in marker_values:
            break
        attempt += 1

    for token in _token_stream(tokens):
        token_type = getattr(token, "type", "")
        if token_type == "heading_open":
            token.attrSet(_MARKDOWN_HEADING_ATTR, marker)
            token.attrSet(_MARKDOWN_LEVEL_ATTR, str(getattr(token, "level", -1)))
        elif token_type == "link_open" and getattr(token, "markup", "") == "autolink":
            token.attrSet(_MARKDOWN_AUTOLINK_ATTR, marker)

    def render_heading_open(
        rendered_tokens: Sequence[object],
        index: int,
        options: Mapping[str, object],
        environment: Mapping[str, object],
    ) -> str:
        opening = markdown.renderer.renderToken(
            rendered_tokens, index, options, environment
        )
        token = rendered_tokens[index]
        if token.attrGet(_MARKDOWN_HEADING_ATTR) != marker:
            return opening
        return f'{opening}<span {_MARKDOWN_BOUNDARY_ATTR}="{marker}"></span>'

    markdown.renderer.rules["heading_open"] = render_heading_open
    markup = markdown.renderer.render(tokens, markdown.options, {})
    return _html_fragment(markup), marker


def _html_local_name(element: object) -> str | None:
    tag = getattr(element, "tag", None)
    if not isinstance(tag, str):
        return None
    prefix = f"{{{_HTML_NAMESPACE}}}"
    if not tag.startswith(prefix):
        return None
    return tag[len(prefix) :]


def _visible_dom_text(
    root: object,
    *,
    hidden_html_tags: frozenset[str],
    hidden_element_ids: frozenset[int] = frozenset(),
    marker: str | None = None,
    skip_markdown_headings: bool = False,
) -> str:
    parts: list[str] = []
    pending: list[tuple[str, object]] = [("element", root)]
    while pending:
        action, value = pending.pop()
        if action == "text":
            if isinstance(value, str):
                parts.append(value)
            continue

        element = value
        tag_value = getattr(element, "tag", None)
        if not isinstance(tag_value, str):
            continue
        local_name = _html_local_name(element)
        attributes = getattr(element, "attrib", {})
        if id(element) in hidden_element_ids or local_name in hidden_html_tags:
            continue
        if marker is not None and (
            (
                skip_markdown_headings
                and attributes.get(_MARKDOWN_HEADING_ATTR) == marker
            )
            or attributes.get(_MARKDOWN_AUTOLINK_ATTR) == marker
        ):
            continue

        is_block = local_name in _HTML_BLOCK_TAGS
        if is_block or local_name == "br":
            parts.append("\n\n")
        if is_block:
            pending.append(("text", "\n\n"))
        if local_name == "img":
            alt = attributes.get("alt")
            if isinstance(alt, str):
                parts.append(alt)
        else:
            element_text = getattr(element, "text", None)
            if isinstance(element_text, str):
                parts.append(element_text)
            for child in reversed(tuple(element)):
                child_tail = getattr(child, "tail", None)
                if isinstance(child_tail, str):
                    pending.append(("text", child_tail))
                pending.append(("element", child))

    return "".join(parts)


def _section_names(text: str) -> tuple[str, ...]:
    dom, marker = _markdown_dom(text)
    headings: list[str] = []
    pending: list[tuple[object, bool]] = [(dom, False)]
    while pending:
        element, hidden_ancestor = pending.pop()
        local_name = _html_local_name(element)
        hidden = hidden_ancestor or local_name in _SECTION_HIDDEN_ANCESTOR_TAGS
        attributes = getattr(element, "attrib", {})
        if (
            not hidden
            and local_name == "h2"
            and attributes.get(_MARKDOWN_HEADING_ATTR) == marker
            and attributes.get(_MARKDOWN_LEVEL_ATTR) == "0"
        ):
            inherited_hidden_ids: set[int] = set()
            active_hidden_ids: list[int] = []
            boundary_pending: list[tuple[str, object]] = [("enter", element)]
            while boundary_pending:
                boundary_action, candidate = boundary_pending.pop()
                if boundary_action == "exit-hidden":
                    active_hidden_ids.pop()
                    continue
                candidate_local = _html_local_name(candidate)
                added_hidden = candidate_local in _SECTION_HIDDEN_ANCESTOR_TAGS
                if added_hidden:
                    active_hidden_ids.append(id(candidate))
                    boundary_pending.append(("exit-hidden", candidate))
                candidate_attributes = getattr(candidate, "attrib", {})
                if candidate_attributes.get(_MARKDOWN_BOUNDARY_ATTR) == marker:
                    inherited_hidden_ids.update(active_hidden_ids)
                    inherited_hidden_ids.add(id(candidate))
                for candidate_child in reversed(tuple(candidate)):
                    boundary_pending.append(("enter", candidate_child))
            heading = _visible_dom_text(
                element,
                hidden_html_tags=_SECTION_HIDDEN_DESCENDANT_TAGS,
                hidden_element_ids=frozenset(inherited_hidden_ids),
            ).strip()
            heading = re.sub(r"^\d+(?:\.\d+)*\.?\s+", "", heading)
            if heading:
                headings.append(heading)
        for child in reversed(tuple(element)):
            pending.append((child, hidden))

    return tuple(headings)


def _readme_policy_prose(text: str) -> str:
    """Return normalized natural-language README prose for policy-topic scans."""

    dom, marker = _markdown_dom(text)
    visible = _visible_dom_text(
        dom,
        hidden_html_tags=_README_HIDDEN_HTML_TAGS,
        marker=marker,
        skip_markdown_headings=True,
    )
    visible = re.sub(
        r"(?<!\w)(?:\.{0,2}/)?[A-Za-z0-9_.{}*-]+(?:/[A-Za-z0-9_.{}*-]+)+",
        " ",
        visible,
    )
    return " " + re.sub(r"[^a-z0-9]+", " ", visible.lower()).strip() + " "


def _validate_artifact_projection(
    reader: _RepositoryReader,
    artifact_document: Mapping[str, object],
    section: str,
    findings: list[Finding],
) -> None:
    for index, entry in enumerate(
        _sequence_or_empty(artifact_document.get("artifacts"))
    ):
        if not isinstance(entry, Mapping):
            continue
        repository_section = entry.get("repository_section")
        if section != "all" and repository_section != section:
            continue
        pattern = entry.get("path_pattern")
        if not isinstance(pattern, str) or not _is_safe_repo_path(pattern):
            continue
        inventory = reader.inventory(
            pattern,
            f"artifacts[{index}].path_pattern",
            "agent-governance-artifacts",
        )
        for missing in inventory.missing_exact:
            _add(
                findings,
                "AGC-REPOSITORY-MISSING-ARTIFACT",
                missing,
                f"artifacts[{index}].path_pattern",
                "registered-artifact",
                "missing-artifact",
                "agent-governance-artifacts",
            )
        if not inventory.paths and inventory.has_glob:
            _add(
                findings,
                "AGC-REPOSITORY-MISSING-ARTIFACT",
                pattern,
                f"artifacts[{index}].path_pattern",
                "registered-artifact",
                "missing-artifact",
                "agent-governance-artifacts",
            )
        paths = inventory.paths
        if not paths:
            continue
        required_keys = tuple(
            value
            for value in _sequence_or_empty(entry.get("required_keys"))
            if isinstance(value, str)
        )
        key_order = tuple(
            value
            for value in _sequence_or_empty(entry.get("key_order"))
            if isinstance(value, str)
        )
        required_sections = tuple(
            value
            for value in _sequence_or_empty(entry.get("required_sections"))
            if isinstance(value, str)
        )
        expected_values = entry.get("expected_values")
        for path in paths:
            relative = path.relative_to(reader.root).as_posix()
            text = reader.read(
                relative,
                f"artifacts[{index}].path_pattern",
                "agent-governance-artifacts",
            )
            if text is None:
                continue
            keys, metadata = _frontmatter(text)
            if metadata is None:
                _add(
                    findings,
                    "AGC-REPOSITORY-METADATA-PARSE",
                    relative,
                    "frontmatter",
                    "valid-yaml-mapping",
                    "invalid-frontmatter",
                    "agent-governance-artifacts",
                )
                continue
            if set(keys) != set(required_keys):
                _add(
                    findings,
                    "AGC-REPOSITORY-METADATA-KEYS",
                    relative,
                    "frontmatter",
                    "exact-profile-keys",
                    "key-set-mismatch",
                    "agent-governance-artifacts",
                )
            if tuple(keys) != key_order:
                _add(
                    findings,
                    "AGC-REPOSITORY-METADATA-KEY-ORDER",
                    relative,
                    "frontmatter",
                    "exact-profile-key-order",
                    "key-order-mismatch",
                    "agent-governance-artifacts",
                )
            if isinstance(expected_values, Mapping):
                for key, expected in expected_values.items():
                    resolved = path.stem if expected == "$path_stem" else expected
                    if metadata.get(key) != resolved:
                        _add(
                            findings,
                            "AGC-REPOSITORY-METADATA-VALUE",
                            relative,
                            f"frontmatter.{key}",
                            "registered-profile-value",
                            "value-mismatch",
                            "agent-governance-artifacts",
                        )
            headings = set(_section_names(text))
            for required in required_sections:
                if required not in headings:
                    _add(
                        findings,
                        "AGC-REPOSITORY-MISSING-SECTION",
                        relative,
                        f"section.{required}",
                        "required-profile-section",
                        "missing-section",
                        "agent-governance-artifacts",
                    )


def _validate_root_shims(
    reader: _RepositoryReader,
    artifact_document: Mapping[str, object],
    findings: list[Finding],
) -> None:
    for index, entry in enumerate(
        _sequence_or_empty(artifact_document.get("root_shims"))
    ):
        if not isinstance(entry, Mapping) or not isinstance(entry.get("path"), str):
            continue
        relative = str(entry["path"])
        text = reader.read(
            relative, f"root_shims[{index}]", "agent-governance-artifacts"
        )
        if text is None:
            continue
        targets = [entry.get("bootstrap_target"), entry.get("provider_target")]
        targets.extend(_sequence_or_empty(entry.get("memory_targets")))
        valid_targets = [target for target in targets if isinstance(target, str)]
        metadata_keys, metadata = _frontmatter(text)
        envelope_valid = metadata == {} and not metadata_keys
        envelope_valid = envelope_valid and _section_names(text) == ("Bootstrap",)
        envelope_valid = envelope_valid and all(
            text.count(target) == 1 for target in valid_targets
        )
        nonblank = [line for line in text.splitlines() if line.strip()]
        style = entry.get("import_style")
        if style == "at-import":
            expected = [
                f"# {relative}",
                "## Bootstrap",
                *[f"@{target}" for target in valid_targets],
            ]
            envelope_valid = envelope_valid and nonblank == expected
        elif style == "at-dot-import":
            expected = [
                f"# {relative}",
                "## Bootstrap",
                *[f"@./{target}" for target in valid_targets],
            ]
            envelope_valid = envelope_valid and nonblank == expected
        elif style == "numbered-load":
            envelope_valid = envelope_valid and len(valid_targets) == 4
            if len(valid_targets) == 4:
                expected = [
                    f"# {relative}",
                    "## Bootstrap",
                    f"1. Load `{valid_targets[0]}`.",
                    f"2. Load `{valid_targets[1]}`.",
                    f"3. Load `{valid_targets[2]}` and `{valid_targets[3]}`.",
                ]
                envelope_valid = envelope_valid and nonblank == expected
        if not envelope_valid:
            _add(
                findings,
                "AGC-REPOSITORY-ROOT-SHIM-ENVELOPE",
                relative,
                f"root_shims[{index}]",
                "exact-bootstrap-envelope",
                "shim-envelope-mismatch",
                "agent-governance-artifacts",
            )


def _validate_readme_profiles(
    reader: _RepositoryReader,
    artifact_document: Mapping[str, object],
    findings: list[Finding],
) -> None:
    for index, entry in enumerate(
        _sequence_or_empty(artifact_document.get("readme_profiles"))
    ):
        if not isinstance(entry, Mapping) or not isinstance(
            entry.get("path_pattern"), str
        ):
            continue
        pattern = str(entry["path_pattern"])
        inventory = reader.inventory(
            pattern,
            f"readme_profiles[{index}].path_pattern",
            "agent-governance-artifacts",
        )
        for missing in inventory.missing_exact:
            _add(
                findings,
                "AGC-REPOSITORY-MISSING-README",
                missing,
                f"readme_profiles[{index}].path_pattern",
                "registered-readme-path",
                "missing-readme-path",
                "agent-governance-artifacts",
            )
        if not inventory.paths and inventory.has_glob:
            _add(
                findings,
                "AGC-REPOSITORY-MISSING-README",
                pattern,
                f"readme_profiles[{index}].path_pattern",
                "registered-readme-path",
                "missing-readme-path",
                "agent-governance-artifacts",
            )
        paths = inventory.paths
        for path in paths:
            relative = path.relative_to(reader.root).as_posix()
            text = reader.read(
                relative,
                f"readme_profiles[{index}].path_pattern",
                "agent-governance-artifacts",
            )
            if text is None:
                continue
            headings = _section_names(text)
            allowed = set(
                value
                for value in _sequence_or_empty(entry.get("allowed_sections"))
                if isinstance(value, str)
            )
            required = set(
                value
                for value in _sequence_or_empty(entry.get("required_sections"))
                if isinstance(value, str)
            )
            for heading in headings:
                if heading not in allowed:
                    _add(
                        findings,
                        "AGC-REPOSITORY-README-SECTION",
                        relative,
                        f"readme_profiles[{index}]",
                        "allowed-profile-section",
                        "unexpected-section",
                        "agent-governance-artifacts",
                    )
            for heading in sorted(required - set(headings)):
                _add(
                    findings,
                    "AGC-REPOSITORY-MISSING-SECTION",
                    relative,
                    f"section.{heading}",
                    "required-readme-section",
                    "missing-section",
                    "agent-governance-artifacts",
                )
            normalized_text = _readme_policy_prose(text)
            for topic in _sequence_or_empty(entry.get("forbidden_policy_topics")):
                if not isinstance(topic, str):
                    continue
                normalized_topic = re.sub(r"[^a-z0-9]+", " ", topic.lower()).strip()
                if normalized_topic and f" {normalized_topic} " in normalized_text:
                    _add(
                        findings,
                        "AGC-REPOSITORY-README-POLICY",
                        relative,
                        f"readme_profiles[{index}].forbidden_policy_topics",
                        "navigation-only-profile",
                        "forbidden-policy-topic",
                        "agent-governance-artifacts",
                    )


def _governed_inventory_paths(
    root: pathlib.Path, artifact_document: Mapping[str, object]
) -> tuple[pathlib.Path, ...]:
    paths: set[pathlib.Path] = set()
    for family in _sequence_or_empty(artifact_document.get("governed_families")):
        if not isinstance(family, Mapping):
            continue
        pattern = family.get("path_pattern")
        if isinstance(pattern, str) and _is_safe_repo_path(pattern):
            paths.update(_registered_paths(root, pattern).paths)
    return tuple(sorted(paths, key=lambda item: item.relative_to(root).as_posix()))


def _validate_governed_inventory(
    reader: _RepositoryReader,
    artifact_document: Mapping[str, object],
    findings: list[Finding],
) -> None:
    artifacts = tuple(
        entry
        for entry in _sequence_or_empty(artifact_document.get("artifacts"))
        if isinstance(entry, Mapping)
    )
    seen: set[str] = set()
    for family_index, family in enumerate(
        _sequence_or_empty(artifact_document.get("governed_families"))
    ):
        if not isinstance(family, Mapping):
            continue
        pattern = family.get("path_pattern")
        if not isinstance(pattern, str) or not _is_safe_repo_path(pattern):
            continue
        allowed_sections = {
            value
            for value in _sequence_or_empty(family.get("repository_sections"))
            if isinstance(value, str)
        }
        for path in reader.paths(
            pattern,
            f"governed_families[{family_index}].path_pattern",
            "agent-governance-artifacts",
        ):
            relative = path.relative_to(reader.root).as_posix()
            if relative in seen:
                continue
            seen.add(relative)
            reader.read(
                relative,
                f"governed_families[{family_index}].path_pattern",
                "agent-governance-artifacts",
            )
            matches = [
                entry
                for entry in artifacts
                if isinstance(entry.get("path_pattern"), str)
                and _path_matches_pattern(relative, str(entry["path_pattern"]))
            ]
            if len(matches) != 1:
                _add(
                    findings,
                    "AGC-REPOSITORY-PROFILE-COVERAGE",
                    relative,
                    f"governed_families[{family_index}]",
                    "exactly-one-artifact-profile",
                    "missing-or-ambiguous-artifact-profile",
                    "agent-governance-artifacts",
                )
                continue
            repository_section = matches[0].get("repository_section")
            if repository_section not in allowed_sections:
                _add(
                    findings,
                    "AGC-REPOSITORY-PROFILE-SECTION",
                    relative,
                    f"governed_families[{family_index}].repository_sections",
                    "family-permitted-repository-section",
                    "misrouted-artifact-profile",
                    "agent-governance-artifacts",
                )


def _provider_native_schema_finding(
    findings: list[Finding], path: str, location: str, actual: str
) -> None:
    _add(
        findings,
        "AGC-PROVIDER-NATIVE-SCHEMA",
        path,
        location,
        "strict-provider-native-schema",
        actual,
        "provider-models",
    )


def _validate_provider_native_surfaces(
    reader: _RepositoryReader, bundle: ContractBundle, findings: list[Finding]
) -> None:
    defaults: dict[tuple[str, str], tuple[str, str | None]] = {}
    for profile in _sequence_or_empty(bundle.providers.get("work_profiles")):
        if not isinstance(profile, Mapping):
            continue
        profile_id = profile.get("profile_id")
        if not isinstance(profile_id, str):
            continue
        for entry in _sequence_or_empty(profile.get("defaults")):
            if not isinstance(entry, Mapping):
                continue
            provider = entry.get("provider")
            model_id = entry.get("model_id")
            control = (
                entry.get("effort") if provider == "claude" else entry.get("reasoning")
            )
            if isinstance(provider, str) and isinstance(model_id, str):
                defaults[(profile_id, str(provider))] = (
                    str(model_id),
                    str(control) if isinstance(control, str) else None,
                )

    markdown_schemas = {
        "claude": {
            "name",
            "description",
            "tools",
            "model",
            "permissionMode",
            "skills",
        },
        "gemini": {
            "name",
            "description",
            "kind",
            "tools",
            "model",
            "max_turns",
            "timeout_mins",
        },
        "agents-md": {"name", "description"},
    }
    codex_schema = {
        "name",
        "description",
        "developer_instructions",
        "model",
        "model_reasoning_effort",
        "sandbox_mode",
    }
    for index, agent in enumerate(_sequence_or_empty(bundle.catalog.get("agents"))):
        if not isinstance(agent, Mapping):
            continue
        agent_id = agent.get("agent_id")
        profile = agent.get("work_profile")
        permission = agent.get("permission_profile")
        catalog_path = agent.get("catalog_path")
        if not all(
            isinstance(item, str)
            for item in (agent_id, profile, permission, catalog_path)
        ):
            continue
        source_marker = f"source: {catalog_path}"
        for provider, relative in (
            ("claude", f".claude/agents/{agent_id}.md"),
            ("gemini", f".gemini/agents/{agent_id}.md"),
            ("agents-md", f".agents/agents/{agent_id}.md"),
        ):
            text = reader.read(
                relative,
                f"agents[{index}].provider_projections",
                "provider-models",
            )
            if text is None:
                continue
            keys, metadata = _frontmatter(text)
            expected = defaults.get((str(profile), provider))
            expected_schema = set(markdown_schemas[provider])
            if (
                provider == "claude"
                and expected is not None
                and expected[1] is not None
            ):
                expected_schema.add("effort")
            if (
                metadata is None
                or set(keys) != expected_schema
                or metadata.get("name") != agent_id
                or source_marker not in text
            ):
                _provider_native_schema_finding(
                    findings, relative, "frontmatter", "key-value-or-origin-mismatch"
                )
                continue
            if provider != "agents-md":
                if expected is None or metadata.get("model") != expected[0]:
                    _provider_native_schema_finding(
                        findings,
                        relative,
                        "frontmatter.model",
                        "profile-model-mismatch",
                    )
                if provider == "claude" and expected is not None:
                    if metadata.get("effort") != expected[1] or "thinking" in metadata:
                        _provider_native_schema_finding(
                            findings,
                            relative,
                            "frontmatter.effort",
                            "profile-effort-or-thinking-mismatch",
                        )
            tools = metadata.get("tools")
            if provider in {"claude", "gemini"} and not isinstance(
                tools, (list, tuple)
            ):
                _provider_native_schema_finding(
                    findings, relative, "frontmatter.tools", "non-list-tools"
                )
            if permission == "read-only" and provider == "claude":
                if metadata.get("permissionMode") != "plan" or any(
                    tool in _sequence_or_empty(tools) for tool in ("Edit", "Write")
                ):
                    _provider_native_schema_finding(
                        findings,
                        relative,
                        "frontmatter.permissions",
                        "write-capable-read-only-role",
                    )
            if permission == "read-only" and provider == "gemini":
                if any(
                    tool in _sequence_or_empty(tools)
                    for tool in ("*", "replace", "write_file")
                ):
                    _provider_native_schema_finding(
                        findings,
                        relative,
                        "frontmatter.tools",
                        "write-capable-read-only-role",
                    )

        codex_path = f".codex/agents/{agent_id}.toml"
        codex_text = reader.read(
            codex_path,
            f"agents[{index}].provider_projections",
            "provider-models",
        )
        if codex_text is not None:
            try:
                codex = tomllib.loads(codex_text)
            except tomllib.TOMLDecodeError:
                codex = {}
            expected = defaults.get((str(profile), "codex"))
            valid = set(codex) == codex_schema and codex.get("name") == agent_id
            valid = valid and source_marker in codex_text and expected is not None
            if expected is not None:
                valid = valid and codex.get("model") == expected[0]
                valid = valid and codex.get("model_reasoning_effort") == expected[1]
            valid = valid and codex.get("sandbox_mode") == (
                "read-only" if permission == "read-only" else "workspace-write"
            )
            if not valid:
                _provider_native_schema_finding(
                    findings, codex_path, "toml", "key-value-or-origin-mismatch"
                )

    for function_index, function in enumerate(
        _sequence_or_empty(bundle.catalog.get("functions"))
    ):
        if not isinstance(function, Mapping) or not isinstance(
            function.get("function_id"), str
        ):
            continue
        function_id = str(function["function_id"])
        for relative in (
            f".claude/skills/{function_id}/SKILL.md",
            f".agents/skills/{function_id}/SKILL.md",
        ):
            reader.read(
                relative,
                f"functions[{function_index}].provider_projections",
                "provider-models",
            )

    codex_skills = reader.root / ".codex/skills"
    if codex_skills.exists() or codex_skills.is_symlink():
        _provider_native_schema_finding(
            findings,
            ".codex/skills",
            "native_skill_pattern",
            "forbidden-codex-skill-root",
        )

    provider_entries = {
        str(entry["provider_id"]): entry
        for entry in _sequence_or_empty(bundle.providers.get("providers"))
        if isinstance(entry, Mapping) and isinstance(entry.get("provider_id"), str)
    }
    event_bindings: dict[str, dict[str, Mapping[str, object]]] = {}
    for event in _sequence_or_empty(bundle.providers.get("semantic_events")):
        if not isinstance(event, Mapping) or not isinstance(event.get("event_id"), str):
            continue
        for binding in _sequence_or_empty(event.get("provider_bindings")):
            if isinstance(binding, Mapping) and isinstance(
                binding.get("provider"), str
            ):
                event_bindings.setdefault(str(binding["provider"]), {})[
                    str(event["event_id"])
                ] = binding
    for provider, entry in provider_entries.items():
        config_path = entry.get("native_config_path")
        if not isinstance(config_path, str):
            continue
        text = reader.read(config_path, "native_config_path", "provider-models")
        if text is None:
            continue
        try:
            config = json.loads(text)
        except json.JSONDecodeError:
            _provider_native_schema_finding(
                findings, config_path, "json", "malformed-provider-config"
            )
            continue
        top_level_schemas = {
            "claude": {
                "autoMode",
                "deniedMcpServers",
                "hooks",
                "outputStyle",
                "permissions",
            },
            "codex": {"hooks"},
            "gemini": {"hooks", "security"},
        }
        if (
            not isinstance(config, Mapping)
            or set(config) != top_level_schemas[provider]
        ):
            _provider_native_schema_finding(
                findings, config_path, "json", "invalid-top-level-keys"
            )
        hooks = config.get("hooks") if isinstance(config, Mapping) else None
        if not isinstance(hooks, Mapping):
            _provider_native_schema_finding(
                findings, config_path, "hooks", "missing-hooks-mapping"
            )
            continue
        expected_events = {
            str(binding["native_event"])
            for binding in event_bindings.get(provider, {}).values()
            if binding.get("capability_status") == "supported"
            and binding.get("adoption_status") == "adopted"
        }
        if set(hooks) != expected_events:
            _provider_native_schema_finding(
                findings, config_path, "hooks", "native-event-set-mismatch"
            )
        for semantic_id, binding in event_bindings.get(provider, {}).items():
            native = binding.get("native_event")
            if not isinstance(native, str) or native not in hooks:
                continue
            groups = hooks.get(native)
            if (
                not isinstance(groups, Sequence)
                or isinstance(groups, str | bytes)
                or len(groups) != 1
                or not isinstance(groups[0], Mapping)
            ):
                _provider_native_schema_finding(
                    findings, config_path, f"hooks.{native}", "invalid-hook-shape"
                )
                continue
            group = groups[0]
            handlers = group.get("hooks")
            if (
                not isinstance(handlers, Sequence)
                or isinstance(handlers, str | bytes)
                or len(handlers) != 1
                or not isinstance(handlers[0], Mapping)
            ):
                _provider_native_schema_finding(
                    findings, config_path, f"hooks.{native}", "invalid-hook-shape"
                )
                continue
            handler = handlers[0]
            matcher_expected = not (
                (provider == "codex" and semantic_id in {"stop", "user-prompt-intake"})
                or (
                    provider == "gemini"
                    and semantic_id not in {"pre-tool", "post-tool"}
                )
            )
            expected_group_keys = (
                {"hooks", "matcher"} if matcher_expected else {"hooks"}
            )
            if set(group) != expected_group_keys:
                _provider_native_schema_finding(
                    findings, config_path, f"hooks.{native}", "invalid-hook-group-keys"
                )
            matchers = {
                (
                    "claude",
                    "pre-tool",
                ): "Bash|Read|Glob|Grep|LS|Edit|Write|MultiEdit|apply_patch|ApplyPatch",
                ("claude", "post-tool"): "Write|Edit|MultiEdit|apply_patch|ApplyPatch",
                (
                    "codex",
                    "pre-tool",
                ): "Bash|Read|Glob|Grep|LS|Edit|Write|MultiEdit|apply_patch|ApplyPatch",
                ("codex", "post-tool"): "Edit|Write|MultiEdit|apply_patch|ApplyPatch",
                (
                    "gemini",
                    "pre-tool",
                ): "read_file|read_many_files|search_file_content|glob|list_directory|write_file|replace|run_shell_command",
                ("gemini", "post-tool"): "write_file|replace|run_shell_command",
            }
            if matcher_expected and group.get("matcher") != matchers.get(
                (provider, semantic_id), "*"
            ):
                _provider_native_schema_finding(
                    findings, config_path, f"hooks.{native}.matcher", "matcher-mismatch"
                )
            if (
                set(handler) != {"type", "command", "timeout"}
                or handler.get("type") != "command"
            ):
                _provider_native_schema_finding(
                    findings,
                    config_path,
                    f"hooks.{native}",
                    "invalid-handler-keys-or-type",
                )
            if handler.get("timeout") != binding.get("timeout_value"):
                _provider_native_schema_finding(
                    findings,
                    config_path,
                    f"hooks.{native}.timeout",
                    "timeout-unit-or-value-mismatch",
                )
            claude_files = {
                "session-start": "session-start.sh",
                "pre-tool": "docker-compose-pre.sh",
                "post-tool": "post-tool-validate.sh",
                "session-end": "session-end.sh",
                "stop": "stop.sh",
                "pre-compaction": "pre-compact.sh",
                "user-prompt-intake": "user-prompt-submit.sh",
            }
            expected_command = {
                "claude": f'bash "$CLAUDE_PROJECT_DIR/.claude/hooks/{claude_files.get(semantic_id, "")}"',
                "codex": (
                    "HY_HOME_HOOK_PROVIDER=codex bash "
                    '"${CODEX_PROJECT_DIR:-$(git rev-parse --show-toplevel)}'
                    f'/scripts/hooks/agent-event-hook.sh" {native}'
                ),
                "gemini": (
                    'bash "${GEMINI_PROJECT_DIR:-$(git rev-parse --show-toplevel)}'
                    f'/.gemini/hooks/agent-event-hook.sh" {native}'
                ),
            }[provider]
            if handler.get("command") != expected_command:
                _provider_native_schema_finding(
                    findings, config_path, f"hooks.{native}.command", "command-mismatch"
                )


def _validate_exact_provider_projection(
    root: pathlib.Path, findings: list[Finding]
) -> None:
    renderer_path = (
        pathlib.Path(__file__).resolve().parents[1]
        / "operations/provider_surface_renderer.py"
    )
    module_name = f"_agent_governance_provider_renderer_{secrets.token_hex(8)}"
    spec = importlib.util.spec_from_file_location(module_name, renderer_path)
    if spec is None or spec.loader is None:
        _provider_native_schema_finding(
            findings, renderer_path.as_posix(), "renderer", "renderer-unavailable"
        )
        return
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    try:
        spec.loader.exec_module(module)
        drift = module.find_native_projection_drift(root)
    except (ContractLoadError, OSError, ValueError):
        _provider_native_schema_finding(
            findings, ".", "renderer", "renderer-validation-error"
        )
        return
    finally:
        sys.modules.pop(module_name, None)
    for entry in drift:
        _add(
            findings,
            "AGC-PROVIDER-PROJECTION-DRIFT",
            entry.path.as_posix(),
            "renderer",
            "exact-generated-projection",
            str(entry.kind),
            "provider-models",
        )


def _validate_harness_semantic_surfaces(
    reader: _RepositoryReader,
    bundle: ContractBundle,
    findings: list[Finding],
) -> None:
    required_fragments = {
        "scripts/validation/validate-harness.sh": ("run-local-qa-gates.sh --harness",),
        "scripts/validation/run-local-qa-gates.sh": (
            "sync-provider-surfaces.sh --check",
            "run-agent-output-eval-fixtures.sh --check-fixtures --check-regressions",
            "--mode repository --section all",
            "scripts/validation/run-agent-precommit-all-files.sh",
            "initially clean linked worktree",
            "tracked Task evidence",
            "--allow-prefix",
        ),
        ".github/PULL_REQUEST_TEMPLATE.md": (
            "## Harness Impact",
            "validate-harness.sh",
            "run-agent-output-eval-fixtures.sh --check-fixtures --check-regressions",
            "fixtures_check=pass",
            "regressions_check=pass",
        ),
        "scripts/README.md": (
            "validate-harness.sh",
            "run-local-qa-gates.sh --harness",
        ),
        "docs/00.agent-governance/README.md": ("harness-implementation-map.md",),
        "docs/00.agent-governance/harness-implementation-map.md": (
            "scripts/validation/validate-harness.sh",
        ),
        "docs/00.agent-governance/rules/approval-boundaries.md": (
            "validate-harness.sh",
        ),
        "docs/99.templates/templates/sdlc/task.template.md": (
            "## Verification Evidence",
        ),
    }
    for relative, fragments in required_fragments.items():
        text = reader.read(relative, "harness", "agent-governance-artifacts")
        if text is None:
            continue
        for fragment in fragments:
            if fragment not in text:
                _add(
                    findings,
                    "AGC-REPOSITORY-HARNESS-SEMANTICS",
                    relative,
                    "harness",
                    "canonical-harness-delegation",
                    "missing-harness-semantic",
                    "agent-governance-artifacts",
                )

    hook_path = "scripts/hooks/agent-event-hook.sh"
    hook_text = reader.read(hook_path, "hook-dispatcher", "provider-models")
    if hook_text is not None:
        if 'run(["docker", "ps"' in hook_text or ".claude/skills/" in hook_text:
            _add(
                findings,
                "AGC-REPOSITORY-HOOK-SEMANTICS",
                hook_path,
                "session-start",
                "repository-context-only-canonical-routing",
                "runtime-probe-or-provider-local-routing",
                "provider-models",
            )
        for function_id in (
            "compose-stack-agent",
            "execution-plan-agent",
            "knowledge-map-agent",
            "ops-runbook-agent",
            "policy-gate-agent",
            "requirements-to-design-agent",
            "task-breakdown-agent",
        ):
            canonical_path = (
                f"docs/00.agent-governance/agents/functions/{function_id}.md"
            )
            if canonical_path not in hook_text:
                _add(
                    findings,
                    "AGC-REPOSITORY-HOOK-SEMANTICS",
                    hook_path,
                    "user-prompt-intake",
                    "complete-canonical-function-routing",
                    "missing-canonical-function-route",
                    "provider-models",
                )

    evaluation = bundle.catalog.get("evaluation")
    if isinstance(evaluation, Mapping):
        for field in (
            "fixture_catalog_path",
            "scorer_path",
            "runner_path",
            "test_path",
        ):
            relative = evaluation.get(field)
            if isinstance(relative, str):
                reader.read(
                    relative,
                    f"evaluation.{field}",
                    "agent-catalog",
                    missing_code="AGC-REPOSITORY-MISSING-EVAL-SURFACE",
                    missing_expected="tracked-evaluation-surface",
                    missing_actual="missing-evaluation-surface",
                )


def validate_repository(
    root: pathlib.Path, bundle: ContractBundle, section: str = "all"
) -> list[Finding]:
    """Validate repository projection for an explicitly activated section.

    Task 1 exposes this read-only diagnostic mode but does not call it from the
    aggregate repository gate. Later tasks activate one aggregate section at a
    time after the corresponding surfaces converge.
    """

    if section not in {"all", "catalog", "providers", "harness"}:
        return [
            Finding(
                "AGC-REPOSITORY-INVALID-SECTION",
                ".",
                "section",
                "registered-section",
                "invalid-section",
                "cli",
            )
        ]
    findings: list[Finding] = []
    reader = _RepositoryReader(root, findings)
    if section in {"all", "harness"}:
        _validate_governed_inventory(reader, bundle.artifacts, findings)
    _validate_artifact_projection(reader, bundle.artifacts, section, findings)
    if section in {"all", "catalog"}:
        for collection_name in ("agents", "functions"):
            entries = _sequence_or_empty(bundle.catalog.get(collection_name))
            for index, entry in enumerate(entries):
                if not isinstance(entry, Mapping):
                    continue
                catalog_path = entry.get("catalog_path")
                location = f"{collection_name}[{index}].catalog_path"
                if isinstance(catalog_path, str) and not _is_safe_repo_path(
                    catalog_path
                ):
                    _add(
                        findings,
                        "AGC-REPOSITORY-UNSAFE-PATH",
                        CONTRACT_RELATIVE_PATHS["catalog"].as_posix(),
                        location,
                        "safe-repo-path",
                        "unsafe-repository-path",
                        "agent-catalog",
                    )
                    continue
                if isinstance(catalog_path, str):
                    reader.read(
                        catalog_path,
                        location,
                        "agent-catalog",
                        missing_code="AGC-REPOSITORY-MISSING-CATALOG-PATH",
                        missing_expected="tracked-catalog-file",
                        missing_actual="missing-catalog-file",
                    )
    if section in {"all", "providers"}:
        providers = _sequence_or_empty(bundle.providers.get("providers"))
        for index, provider in enumerate(providers):
            if not isinstance(provider, Mapping):
                continue
            config_path = provider.get("native_config_path")
            location = f"providers[{index}].native_config_path"
            if isinstance(config_path, str) and not _is_safe_repo_path(config_path):
                _add(
                    findings,
                    "AGC-REPOSITORY-UNSAFE-PATH",
                    CONTRACT_RELATIVE_PATHS["providers"].as_posix(),
                    location,
                    "safe-repo-path",
                    "unsafe-repository-path",
                    "provider-models",
                )
                continue
            if isinstance(config_path, str) and not (root / config_path).is_file():
                _add(
                    findings,
                    "AGC-REPOSITORY-MISSING-PROVIDER-CONFIG",
                    config_path,
                    location,
                    "tracked-provider-config",
                    "missing-provider-config",
                    "provider-models",
                )
        _validate_provider_native_surfaces(reader, bundle, findings)
        _validate_exact_provider_projection(root, findings)
    if section in {"all", "harness"}:
        _validate_root_shims(reader, bundle.artifacts, findings)
        _validate_readme_profiles(reader, bundle.artifacts, findings)
        _validate_harness_semantic_surfaces(reader, bundle, findings)
        harness = root / "docs/00.agent-governance/harness-implementation-map.md"
        if not harness.is_file():
            _add(
                findings,
                "AGC-REPOSITORY-MISSING-HARNESS",
                "docs/00.agent-governance/harness-implementation-map.md",
                "harness",
                "tracked-harness-map",
                "missing-harness-map",
                "agent-governance-artifacts",
            )
    return sorted(findings, key=finding_sort_key)


def render_findings(findings: Sequence[Finding]) -> str:
    """Render deterministic, value-free diagnostics."""

    return "\n".join(
        " ".join(
            (
                finding.code,
                f"path={finding.path}",
                f"location={finding.location}",
                f"expected={finding.expected}",
                f"actual={finding.actual}",
                f"source={finding.source}",
            )
        )
        for finding in sorted(findings, key=finding_sort_key)
    )
