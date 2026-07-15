#!/usr/bin/env python3
"""Load and validate the typed Stage 00 agent-governance contracts."""

from __future__ import annotations

import datetime as dt
import pathlib
import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from types import MappingProxyType
from urllib.parse import urlparse

import yaml


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

COMMON_TOP_FIELDS = {"schema_version", "checked_at"}
ARTIFACT_TOP_FIELDS = COMMON_TOP_FIELDS | {
    "artifacts",
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
}
PROVIDER_TOP_FIELDS = COMMON_TOP_FIELDS | {
    "providers",
    "compatibility_surfaces",
    "work_profiles",
    "models",
    "semantic_events",
}

ARTIFACT_FIELDS = {
    "artifact_type",
    "path_pattern",
    "canonical",
    "required_keys",
    "key_order",
    "required_sections",
}
ROOT_SHIM_FIELDS = {"path", "provider", "bootstrap_target", "frontmatter"}
README_PROFILE_FIELDS = {
    "profile_id",
    "path_pattern",
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
PROVIDER_FIELDS = {
    "provider_id",
    "capability_status",
    "adoption_status",
    "native_agent_pattern",
    "native_config_path",
    "shared_skill_surface",
    "source_url",
}
COMPATIBILITY_FIELDS = {
    "surface_id",
    "path_pattern",
    "status",
    "consumers",
    "source_url",
}
WORK_PROFILE_FIELDS = {"profile_id", "description", "defaults"}
WORK_PROFILE_DEFAULT_FIELDS = {"provider", "model_id", "reasoning"}
MODEL_FIELDS = {
    "provider",
    "model_id",
    "provider_status",
    "repository_default_eligible",
    "entitlement",
    "runtime_acceptance",
    "reasoning_controls",
    "work_profiles",
    "fallback",
    "checked_at",
    "source_url",
}
EVENT_FIELDS = {"event_id", "required", "provider_bindings"}
EVENT_BINDING_FIELDS = {
    "provider",
    "native_event",
    "capability_status",
    "adoption_status",
    "blocking",
    "timeout_unit",
}

PROVIDER_CAPABILITY_STATES = {"supported", "unsupported", "needs_revalidation"}
PROVIDER_ADOPTION_STATES = {
    "adopted",
    "deferred",
    "not_applicable",
    "partial",
    "planned",
}
MODEL_STATES = {"deprecated", "preview", "stable"}
ENTITLEMENT_STATES = {"available", "needs_revalidation", "unavailable"}
RUNTIME_ACCEPTANCE_STATES = {"accepted", "needs_revalidation", "rejected"}
AGENT_CATEGORIES = {"implementation-operations", "review-evaluation", "supervisor"}
AGENT_TIERS = {"supervisor", "worker"}
AGENT_STATUSES = {"active", "retired"}
CAPABILITY_DECISIONS = {"adopt", "defer", "merge", "reject"}
TIMEOUT_UNITS = {"milliseconds", "seconds"}

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
                "entry_owners": (
                    ("domain-owner", "agents", "agent_id", "agent_id"),
                ),
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


class _UnhashableKeyError(yaml.YAMLError):
    def __init__(self, line: int) -> None:
        self.line = line
        super().__init__("unhashable mapping key")


class _UniqueKeyLoader(yaml.SafeLoader):
    pass


def _construct_unique_mapping(
    loader: _UniqueKeyLoader, node: yaml.nodes.MappingNode, deep: bool = False
) -> dict[object, object]:
    mapping: dict[object, object] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            duplicate = key in mapping
        except TypeError as error:
            raise _UnhashableKeyError(key_node.start_mark.line + 1) from error
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
        return MappingProxyType({str(key): _freeze(item) for key, item in value.items()})
    if isinstance(value, list | tuple):
        return tuple(_freeze(item) for item in value)
    return value


def _load_yaml(path: pathlib.Path, relative_path: str) -> Mapping[str, object]:
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError as error:
        raise ContractLoadError("AGC-CONTRACT-MISSING", relative_path, "file") from error
    except (OSError, UnicodeError) as error:
        raise ContractLoadError("AGC-CONTRACT-READ", relative_path, "file") from error
    try:
        value = yaml.load(text, Loader=_UniqueKeyLoader)
    except _DuplicateKeyError as error:
        raise ContractLoadError(
            "AGC-YAML-DUPLICATE-KEY", relative_path, f"line:{error.line}"
        ) from error
    except _UnhashableKeyError as error:
        raise ContractLoadError(
            "AGC-YAML-UNHASHABLE-KEY", relative_path, f"line:{error.line}"
        ) from error
    except yaml.YAMLError as error:
        raise ContractLoadError("AGC-YAML-MALFORMED", relative_path, "yaml") from error
    if not isinstance(value, Mapping):
        raise ContractLoadError("AGC-YAML-NOT-MAPPING", relative_path, "root")
    return _freeze(value)  # type: ignore[return-value]


def load_contract_bundle(root: pathlib.Path) -> ContractBundle:
    """Load the three fixed Stage 00 contract files beneath ``root``."""

    resolved_root = root.resolve()
    loaded: dict[str, Mapping[str, object]] = {}
    for key, relative in CONTRACT_RELATIVE_PATHS.items():
        relative_text = relative.as_posix()
        loaded[key] = _load_yaml(resolved_root / relative, relative_text)
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
        if collection_valid:
            expected_identity, expected_agent = DOMAIN_OWNER_REFERENCE_FIELDS[str(collection)]
            if identity_field != expected_identity:
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
                _add(
                    findings,
                    "AGC-AUTHORITY-REFERENCE",
                    path,
                    f"{entry_location}.agent_field",
                    "catalog-agent-reference-field",
                    "invalid-agent-reference-field",
                    source,
                )
        if all((role_valid, collection_valid, identity_valid, agent_valid)):
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
) -> None:
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


def _is_safe_repo_path(value: object) -> bool:
    if not _is_nonempty_string(value):
        return False
    text = str(value)
    if "\x00" in text or "\\" in text or text.startswith(("/", "~")):
        return False
    if re.match(r"^[A-Za-z]:", text):
        return False
    parts = pathlib.PurePosixPath(text).parts
    return bool(parts) and all(part not in {".", "..", ""} for part in parts)


def _check_path(
    value: object,
    path: str,
    location: str,
    findings: list[Finding],
    source: str,
) -> bool:
    if _is_safe_repo_path(value):
        return True
    _add(findings, "AGC-PATH-UNSAFE", path, location, "safe-repo-path", "unsafe-path", source)
    return False


def _check_common(
    document: Mapping[str, object],
    expected_fields: set[str],
    path: str,
    findings: list[Finding],
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
    _check_checked_at(document.get("checked_at"), path, "checked_at", findings, source)


def _validate_artifact_contract(
    document: Mapping[str, object], findings: list[Finding]
) -> None:
    path = CONTRACT_RELATIVE_PATHS["artifacts"].as_posix()
    source = path
    _check_common(document, ARTIFACT_TOP_FIELDS, path, findings)

    artifacts = _as_sequence(document.get("artifacts"), path, "artifacts", findings, source)
    artifact_ids: list[str] = []
    if artifacts is not None:
        for index, raw in enumerate(artifacts):
            location = f"artifacts[{index}]"
            entry = _check_fields(raw, ARTIFACT_FIELDS, path, location, findings, source)
            if entry is None:
                continue
            artifact_type = entry.get("artifact_type")
            if _check_string(artifact_type, path, f"{location}.artifact_type", findings, source):
                artifact_ids.append(str(artifact_type))
            _check_path(entry.get("path_pattern"), path, f"{location}.path_pattern", findings, source)
            _check_bool(entry.get("canonical"), path, f"{location}.canonical", findings, source)
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
            )
            if required_keys is not None and key_order is not None and required_keys != key_order:
                _add(
                    findings,
                    "AGC-ARTIFACT-KEY-ORDER",
                    path,
                    f"{location}.key_order",
                    "exact-required-key-order",
                    "key-order-mismatch",
                    source,
                )
    _check_sorted_unique_ids(artifact_ids, path, "artifacts", findings, source)

    root_shims = _as_sequence(document.get("root_shims"), path, "root_shims", findings, source)
    root_paths: list[str] = []
    if root_shims is not None:
        for index, raw in enumerate(root_shims):
            location = f"root_shims[{index}]"
            entry = _check_fields(raw, ROOT_SHIM_FIELDS, path, location, findings, source)
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
            entry = _check_fields(raw, README_PROFILE_FIELDS, path, location, findings, source)
            if entry is None:
                continue
            profile_id = entry.get("profile_id")
            if _check_string(profile_id, path, f"{location}.profile_id", findings, source):
                readme_ids.append(str(profile_id))
            _check_path(entry.get("path_pattern"), path, f"{location}.path_pattern", findings, source)
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
            entry = _check_fields(raw, AUTHORITY_FIELDS, path, location, findings, source)
            if entry is None:
                continue
            authority_id = entry.get("authority_id")
            if _check_string(authority_id, path, f"{location}.authority_id", findings, source):
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
                    if _check_path(
                        pattern,
                        path,
                        f"{location}.path_patterns[{pattern_index}]",
                        findings,
                        source,
                    ):
                        authority_patterns.append((str(authority_id), pattern, location))
            _check_string(entry.get("canonical_owner"), path, f"{location}.canonical_owner", findings, source)
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
            mandatory_reviewers = _check_string_list(
                entry.get("mandatory_reviewers"),
                path,
                f"{location}.mandatory_reviewers",
                findings,
                source,
                allow_empty=True,
                require_sorted=True,
            ) or ()
            entry_reviewers = _check_entry_authority_list(
                entry.get("entry_reviewers"),
                path,
                f"{location}.entry_reviewers",
                findings,
                source,
            )
            _check_bool(entry.get("protected"), path, f"{location}.protected", findings, source)
            _check_string_list(entry.get("validators"), path, f"{location}.validators", findings, source)
            _check_string(entry.get("rollback"), path, f"{location}.rollback", findings, source)
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
        for other_owner, other_pattern, other_location in authority_patterns[index + 1 :]:
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
        _add(findings, duplicate_code, path, location, "unique-ids", "duplicate-id", source)
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
    if left == right:
        return True

    def prefix(pattern: str) -> str:
        marker_positions = [
            position for marker in ("*", "?", "{", "[") if (position := pattern.find(marker)) >= 0
        ]
        end = min(marker_positions) if marker_positions else len(pattern)
        return pattern[:end].rstrip("/")

    left_prefix = prefix(left)
    right_prefix = prefix(right)
    if not left_prefix or not right_prefix:
        return False
    return left_prefix == right_prefix or left_prefix.startswith(
        f"{right_prefix}/"
    ) or right_prefix.startswith(f"{left_prefix}/")


def _validate_catalog_contract(
    document: Mapping[str, object],
    provider_document: Mapping[str, object],
    artifact_document: Mapping[str, object],
    findings: list[Finding],
) -> None:
    path = CONTRACT_RELATIVE_PATHS["catalog"].as_posix()
    source = path
    _check_common(document, CATALOG_TOP_FIELDS, path, findings)
    projections = _check_string_list(
        document.get("projection_targets"),
        path,
        "projection_targets",
        findings,
        source,
        require_sorted=True,
    ) or ()
    provider_targets = {
        str(entry.get("provider_id"))
        for entry in provider_document.get("providers", ())
        if isinstance(entry, Mapping) and _is_nonempty_string(entry.get("provider_id"))
    }
    compatibility_targets = {
        str(entry.get("surface_id"))
        for entry in provider_document.get("compatibility_surfaces", ())
        if isinstance(entry, Mapping)
        and entry.get("status") == "active"
        and _is_nonempty_string(entry.get("surface_id"))
    }
    canonical_projection_targets = tuple(sorted(provider_targets | compatibility_targets))
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
            document.get("scopes"), path, "scopes", findings, source, require_sorted=True
        )
        or ()
    )

    permissions = _as_sequence(document.get("permissions"), path, "permissions", findings, source)
    permission_ids: list[str] = []
    if permissions is not None:
        for index, raw in enumerate(permissions):
            location = f"permissions[{index}]"
            entry = _check_fields(raw, PERMISSION_FIELDS, path, location, findings, source)
            if entry is None:
                continue
            permission_id = entry.get("permission_id")
            if _check_string(permission_id, path, f"{location}.permission_id", findings, source):
                permission_ids.append(str(permission_id))
            _check_bool(
                entry.get("mutation_allowed"), path, f"{location}.mutation_allowed", findings, source
            )
            _check_bool(
                entry.get("evidence_required"), path, f"{location}.evidence_required", findings, source
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
                entry.get("category"), AGENT_CATEGORIES, path, f"{location}.category", findings, source
            )
            if entry.get("scope") not in scopes:
                _unknown_reference(findings, path, f"{location}.scope", source)
            _check_enum(entry.get("tier"), AGENT_TIERS, path, f"{location}.tier", findings, source)
            _check_enum(
                entry.get("status"), AGENT_STATUSES, path, f"{location}.status", findings, source
            )
            _check_path(entry.get("catalog_path"), path, f"{location}.catalog_path", findings, source)
            if entry.get("permission_profile") not in permission_set:
                _unknown_reference(findings, path, f"{location}.permission_profile", source)
            _check_string(entry.get("work_profile"), path, f"{location}.work_profile", findings, source)
            function_ids = _check_string_list(
                entry.get("function_ids"),
                path,
                f"{location}.function_ids",
                findings,
                source,
                allow_empty=True,
                require_sorted=True,
            ) or ()
            if isinstance(agent_id, str):
                agent_functions[agent_id] = set(function_ids)
            projection_values = _check_string_list(
                entry.get("provider_projections"),
                path,
                f"{location}.provider_projections",
                findings,
                source,
                require_sorted=True,
            ) or ()
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

    functions = _as_sequence(document.get("functions"), path, "functions", findings, source)
    function_ids: list[str] = []
    function_owners: dict[str, str] = {}
    if functions is not None:
        for index, raw in enumerate(functions):
            location = f"functions[{index}]"
            entry = _check_fields(raw, FUNCTION_FIELDS, path, location, findings, source)
            if entry is None:
                continue
            function_id = entry.get("function_id")
            if _check_string(function_id, path, f"{location}.function_id", findings, source):
                function_ids.append(str(function_id))
            if entry.get("scope") not in scopes:
                _unknown_reference(findings, path, f"{location}.scope", source)
            _check_enum(
                entry.get("status"), AGENT_STATUSES, path, f"{location}.status", findings, source
            )
            _check_path(entry.get("catalog_path"), path, f"{location}.catalog_path", findings, source)
            owner = entry.get("owner_agent")
            if owner not in agent_set:
                _unknown_reference(findings, path, f"{location}.owner_agent", source)
            elif isinstance(function_id, str) and isinstance(owner, str):
                function_owners[function_id] = owner
            reviewers = _check_string_list(
                entry.get("reviewer_agents"),
                path,
                f"{location}.reviewer_agents",
                findings,
                source,
                require_sorted=True,
            ) or ()
            for reviewer in reviewers:
                if reviewer not in agent_set:
                    _unknown_reference(findings, path, f"{location}.reviewer_agents", source)
            for field in ("inputs", "outputs", "gates"):
                _check_string_list(entry.get(field), path, f"{location}.{field}", findings, source)
            projection_values = _check_string_list(
                entry.get("provider_projections"),
                path,
                f"{location}.provider_projections",
                findings,
                source,
                require_sorted=True,
            ) or ()
            for projection in projection_values:
                if projection not in projections:
                    _unknown_reference(findings, path, f"{location}.provider_projections", source)
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
    for agent_id, referenced_functions in agent_functions.items():
        for function_id in sorted(referenced_functions):
            if function_id not in function_set:
                _unknown_reference(findings, path, f"agents.{agent_id}.function_ids", source)
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
            entry = _check_fields(raw, ROLE_TRANSFER_FIELDS, path, location, findings, source)
            if entry is None:
                continue
            retired = entry.get("retired_agent_id")
            if _check_string(retired, path, f"{location}.retired_agent_id", findings, source):
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
            _check_enum(entry.get("status"), {"retired"}, path, f"{location}.status", findings, source)
            successors = _check_string_list(
                entry.get("successor_agent_ids"),
                path,
                f"{location}.successor_agent_ids",
                findings,
                source,
                require_sorted=True,
            ) or ()
            successor_functions = _check_string_list(
                entry.get("successor_function_ids"),
                path,
                f"{location}.successor_function_ids",
                findings,
                source,
                require_sorted=True,
            ) or ()
            for successor in successors:
                if successor not in agent_set:
                    _unknown_reference(findings, path, f"{location}.successor_agent_ids", source)
            for function_id in successor_functions:
                if function_id not in function_set:
                    _unknown_reference(
                        findings, path, f"{location}.successor_function_ids", source
                    )
            _check_string(entry.get("rationale"), path, f"{location}.rationale", findings, source)
    _check_sorted_unique_ids(transfer_ids, path, "role_transfers", findings, source)

    intake = _as_sequence(
        document.get("capability_intake"), path, "capability_intake", findings, source
    )
    intake_ids: list[str] = []
    if intake is not None:
        for index, raw in enumerate(intake):
            location = f"capability_intake[{index}]"
            entry = _check_fields(raw, CAPABILITY_INTAKE_FIELDS, path, location, findings, source)
            if entry is None:
                continue
            capability_id = entry.get("capability_id")
            if _check_string(capability_id, path, f"{location}.capability_id", findings, source):
                intake_ids.append(str(capability_id))
            _check_string(entry.get("source"), path, f"{location}.source", findings, source)
            _check_source_url(entry.get("source_url"), path, f"{location}.source_url", findings, source)
            _check_enum(
                entry.get("decision"),
                CAPABILITY_DECISIONS,
                path,
                f"{location}.decision",
                findings,
                source,
            )
            if entry.get("owner_agent") not in agent_set:
                _unknown_reference(findings, path, f"{location}.owner_agent", source)
            if entry.get("evaluation_function") not in function_set:
                _unknown_reference(findings, path, f"{location}.evaluation_function", source)
    _check_sorted_unique_ids(intake_ids, path, "capability_intake", findings, source)

    work_profile_ids = {
        entry.get("profile_id")
        for entry in provider_document.get("work_profiles", ())
        if isinstance(entry, Mapping) and isinstance(entry.get("profile_id"), str)
    }
    if agents is not None:
        for index, raw in enumerate(agents):
            if isinstance(raw, Mapping) and raw.get("work_profile") not in work_profile_ids:
                _unknown_reference(findings, path, f"agents[{index}].work_profile", source)

    if isinstance(artifact_document.get("path_authority"), Sequence):
        for index, raw in enumerate(artifact_document["path_authority"]):
            if not isinstance(raw, Mapping):
                continue
            for field in ("canonical_owner",):
                if raw.get(field) not in agent_set:
                    _unknown_reference(
                        findings,
                        CONTRACT_RELATIVE_PATHS["artifacts"].as_posix(),
                        f"path_authority[{index}].{field}",
                        CONTRACT_RELATIVE_PATHS["artifacts"].as_posix(),
                    )
            for field in ("permitted_contributors", "mandatory_reviewers"):
                values = raw.get(field, ())
                if isinstance(values, Sequence) and not isinstance(values, str | bytes):
                    for item in values:
                        if item not in agent_set:
                            _unknown_reference(
                                findings,
                                CONTRACT_RELATIVE_PATHS["artifacts"].as_posix(),
                                f"path_authority[{index}].{field}",
                                CONTRACT_RELATIVE_PATHS["artifacts"].as_posix(),
                            )
            for field in ("entry_owners", "entry_reviewers"):
                references = raw.get(field, ())
                if not isinstance(references, Sequence) or isinstance(
                    references, str | bytes
                ):
                    continue
                for reference_index, reference in enumerate(references):
                    if not isinstance(reference, Mapping):
                        continue
                    collection = reference.get("catalog_collection")
                    agent_field = reference.get("agent_field")
                    entries = document.get(str(collection), ())
                    if not isinstance(entries, Sequence) or isinstance(
                        entries, str | bytes
                    ):
                        continue
                    for catalog_entry in entries:
                        if not isinstance(catalog_entry, Mapping):
                            continue
                        if catalog_entry.get(str(agent_field)) not in agent_set:
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
    document: Mapping[str, object], findings: list[Finding]
) -> None:
    path = CONTRACT_RELATIVE_PATHS["providers"].as_posix()
    source = path
    _check_common(document, PROVIDER_TOP_FIELDS, path, findings)
    providers = _as_sequence(document.get("providers"), path, "providers", findings, source)
    provider_ids: list[str] = []
    if providers is not None:
        for index, raw in enumerate(providers):
            location = f"providers[{index}]"
            entry = _check_fields(raw, PROVIDER_FIELDS, path, location, findings, source)
            if entry is None:
                continue
            provider_id = entry.get("provider_id")
            if _check_string(provider_id, path, f"{location}.provider_id", findings, source):
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
            for field in ("native_agent_pattern", "native_config_path", "shared_skill_surface"):
                _check_path(entry.get(field), path, f"{location}.{field}", findings, source)
            _check_source_url(entry.get("source_url"), path, f"{location}.source_url", findings, source)
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
            entry = _check_fields(raw, COMPATIBILITY_FIELDS, path, location, findings, source)
            if entry is None:
                continue
            surface_id = entry.get("surface_id")
            if _check_string(surface_id, path, f"{location}.surface_id", findings, source):
                compatibility_ids.append(str(surface_id))
            _check_path(entry.get("path_pattern"), path, f"{location}.path_pattern", findings, source)
            _check_enum(entry.get("status"), {"active", "retired"}, path, f"{location}.status", findings, source)
            _check_string_list(
                entry.get("consumers"),
                path,
                f"{location}.consumers",
                findings,
                source,
                require_sorted=True,
            )
            _check_source_url(entry.get("source_url"), path, f"{location}.source_url", findings, source)
    _check_sorted_unique_ids(
        compatibility_ids, path, "compatibility_surfaces", findings, source
    )

    work_profiles = _as_sequence(
        document.get("work_profiles"), path, "work_profiles", findings, source
    )
    profile_ids: list[str] = []
    profile_defaults: list[tuple[str, str, str, str]] = []
    if work_profiles is not None:
        for index, raw in enumerate(work_profiles):
            location = f"work_profiles[{index}]"
            entry = _check_fields(raw, WORK_PROFILE_FIELDS, path, location, findings, source)
            if entry is None:
                continue
            profile_id = entry.get("profile_id")
            if _check_string(profile_id, path, f"{location}.profile_id", findings, source):
                profile_ids.append(str(profile_id))
            _check_string(entry.get("description"), path, f"{location}.description", findings, source)
            defaults = _as_sequence(entry.get("defaults"), path, f"{location}.defaults", findings, source)
            default_providers: list[str] = []
            if defaults is not None:
                for default_index, raw_default in enumerate(defaults):
                    default_location = f"{location}.defaults[{default_index}]"
                    default = _check_fields(
                        raw_default,
                        WORK_PROFILE_DEFAULT_FIELDS,
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
                    if _check_string(provider, path, f"{default_location}.provider", findings, source):
                        default_providers.append(str(provider))
                    _check_string(model_id, path, f"{default_location}.model_id", findings, source)
                    _check_string(reasoning, path, f"{default_location}.reasoning", findings, source)
                    if all(isinstance(item, str) for item in (profile_id, provider, model_id, reasoning)):
                        profile_defaults.append(
                            (str(profile_id), str(provider), str(model_id), str(reasoning))
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

    models = _as_sequence(document.get("models"), path, "models", findings, source)
    model_keys: list[tuple[str, str]] = []
    model_entries: dict[tuple[str, str], Mapping[str, object]] = {}
    if models is not None:
        for index, raw in enumerate(models):
            location = f"models[{index}]"
            entry = _check_fields(raw, MODEL_FIELDS, path, location, findings, source)
            if entry is None:
                continue
            provider = entry.get("provider")
            model_id = entry.get("model_id")
            if provider not in provider_set:
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
            eligible = entry.get("repository_default_eligible")
            _check_bool(eligible, path, f"{location}.repository_default_eligible", findings, source)
            if status_valid and eligible is True and entry.get("provider_status") != "stable":
                _add(
                    findings,
                    "AGC-MODEL-INELIGIBLE-STATUS",
                    path,
                    f"{location}.repository_default_eligible",
                    "stable-model-only",
                    "nonstable-default",
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
            _check_string_list(
                entry.get("reasoning_controls"),
                path,
                f"{location}.reasoning_controls",
                findings,
                source,
                require_sorted=True,
            )
            profiles = _check_string_list(
                entry.get("work_profiles"),
                path,
                f"{location}.work_profiles",
                findings,
                source,
                require_sorted=True,
            ) or ()
            for profile in profiles:
                if profile not in profile_set:
                    _unknown_reference(findings, path, f"{location}.work_profiles", source)
            _check_string(entry.get("fallback"), path, f"{location}.fallback", findings, source)
            _check_checked_at(entry.get("checked_at"), path, f"{location}.checked_at", findings, source)
            _check_source_url(entry.get("source_url"), path, f"{location}.source_url", findings, source)
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
    for key, entry in model_entries.items():
        fallback_key = (key[0], str(entry.get("fallback")))
        fallback = model_entries.get(fallback_key)
        if fallback is None:
            _unknown_reference(findings, path, f"models.{key[0]}.{key[1]}.fallback", source)
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
    for profile_id, provider, model_id, reasoning in profile_defaults:
        model = model_entries.get((provider, model_id))
        if model is None:
            _unknown_reference(
                findings, path, f"work_profiles.{profile_id}.defaults.{provider}.model_id", source
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
        controls = model.get("reasoning_controls", ())
        if not isinstance(controls, Sequence) or reasoning not in controls:
            _add(
                findings,
                "AGC-MODEL-REASONING-MISMATCH",
                path,
                f"work_profiles.{profile_id}.defaults.{provider}.reasoning",
                "model-supported-reasoning",
                "unsupported-reasoning",
                source,
            )
        profiles = model.get("work_profiles", ())
        if not isinstance(profiles, Sequence) or profile_id not in profiles:
            _add(
                findings,
                "AGC-MODEL-PROFILE-MISMATCH",
                path,
                f"work_profiles.{profile_id}.defaults.{provider}.model_id",
                "model-profile-membership",
                "missing-model-profile",
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
            _check_bool(entry.get("required"), path, f"{location}.required", findings, source)
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
                    if _check_string(provider, path, f"{binding_location}.provider", findings, source):
                        binding_providers.append(str(provider))
                    if provider not in provider_set:
                        _unknown_reference(findings, path, f"{binding_location}.provider", source)
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
                    _check_bool(
                        binding.get("blocking"),
                        path,
                        f"{binding_location}.blocking",
                        findings,
                        source,
                    )
                    _check_enum(
                        binding.get("timeout_unit"),
                        TIMEOUT_UNITS,
                        path,
                        f"{binding_location}.timeout_unit",
                        findings,
                        source,
                    )
            _check_sorted_unique_ids(
                binding_providers, path, f"{location}.provider_bindings", findings, source
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


def validate_contract_bundle(root: pathlib.Path, bundle: ContractBundle) -> list[Finding]:
    """Validate contract schema, identities, references, and deterministic policy."""

    del root  # Fixed contract paths are repository-relative and validated independently.
    findings: list[Finding] = []
    _validate_artifact_contract(bundle.artifacts, findings)
    _validate_provider_contract(bundle.providers, findings)
    _validate_catalog_contract(bundle.catalog, bundle.providers, bundle.artifacts, findings)
    return sorted(findings, key=finding_sort_key)


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
    if section in {"all", "catalog"}:
        for collection_name in ("agents", "functions"):
            entries = bundle.catalog.get(collection_name, ())
            if not isinstance(entries, Sequence):
                continue
            for index, entry in enumerate(entries):
                if not isinstance(entry, Mapping):
                    continue
                catalog_path = entry.get("catalog_path")
                if isinstance(catalog_path, str) and not (root / catalog_path).is_file():
                    _add(
                        findings,
                        "AGC-REPOSITORY-MISSING-CATALOG-PATH",
                        catalog_path,
                        f"{collection_name}[{index}].catalog_path",
                        "tracked-catalog-file",
                        "missing-catalog-file",
                        "agent-catalog",
                    )
    if section in {"all", "providers"}:
        providers = bundle.providers.get("providers", ())
        if isinstance(providers, Sequence):
            for index, provider in enumerate(providers):
                if not isinstance(provider, Mapping):
                    continue
                config_path = provider.get("native_config_path")
                if isinstance(config_path, str) and not (root / config_path).is_file():
                    _add(
                        findings,
                        "AGC-REPOSITORY-MISSING-PROVIDER-CONFIG",
                        config_path,
                        f"providers[{index}].native_config_path",
                        "tracked-provider-config",
                        "missing-provider-config",
                        "provider-models",
                    )
    if section in {"all", "harness"}:
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
