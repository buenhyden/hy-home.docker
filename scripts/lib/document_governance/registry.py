"""Immutable, fail-closed loader for the Stage 99 document registry."""

from __future__ import annotations

import dataclasses
import datetime as dt
import functools
import json
import os
import pathlib
import re
import selectors
import stat
import subprocess
import time
from collections.abc import Mapping, Sequence
from types import MappingProxyType

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import SchemaError
from scripts.lib.document_governance.taxonomy import (
    registered_path_patterns_overlap as _path_patterns_overlap,
)


ROOT = pathlib.Path(__file__).resolve().parents[3]
DEFAULT_REGISTRY = ROOT / "docs/99.templates/registry.json"
DEFAULT_PROFILE_SCHEMA = (
    ROOT / "docs/99.templates/contracts/document-profile.schema.json"
)
DEFAULT_FRONTMATTER_SCHEMA = (
    ROOT / "docs/99.templates/contracts/frontmatter.schema.json"
)
MAX_REGISTRY_BYTES = 1024 * 1024
MAX_SCHEMA_BYTES = 256 * 1024
MAX_JSON_DEPTH = 64
FALLBACK_PROFILE_IDS = frozenset({"unsupported"})
GIT_READ_TIMEOUT_SECONDS = 10
MAX_GIT_STDERR_BYTES = 64 * 1024
MAX_TRUSTED_REQUIREMENT_BYTES = 512 * 1024
MAX_TRUSTED_REQUIREMENT_PACKAGES = 9999
MAX_TRUSTED_REQUIREMENT_PATHS = MAX_TRUSTED_REQUIREMENT_PACKAGES + 1
MAX_TRUSTED_CHILD_HIGH_WATER = 9999
MAX_IDENTITY_ALLOCATION_VALUE = 9999
_GIT_OID = re.compile(r"[0-9a-f]{40,64}")
_TRUSTED_REQUIREMENT_PATH = re.compile(
    r"docs/01\.requirements/(?P<package>[0-9]{4})-[a-z0-9][a-z0-9-]*\.md"
)
_TRUSTED_LEGACY_REQUIREMENT_PATH = re.compile(
    r"docs/01\.requirements/prd-(?P<package>[0-9]{4})-"
    r"[a-z0-9][a-z0-9-]*\.md"
)
_TRUSTED_CHILD_ID = re.compile(
    r"REQ-(?P<package>[0-9]{4})-(?P<kind>FR|NFR|IF)-(?P<number>[0-9]{4})"
)
_TRUSTED_LEGACY_CHILD_ID = re.compile(
    r"PRD-(?P<package>[0-9]{4})-R(?P<number>[0-9]{4})"
)
_TRUSTED_REQUIREMENT_SECTION = re.compile(
    r"(?ms)^## (?P<name>Functional Requirements|Non-functional Requirements|"
    r"Interface Requirements)\n(?P<body>.*?)(?=^## |\Z)"
)
_TRUSTED_SECTION_KIND = {
    "Functional Requirements": "FR",
    "Non-functional Requirements": "NFR",
    "Interface Requirements": "IF",
}
_TRUSTED_LEGACY_REQUIREMENT_SECTION = re.compile(
    r"(?ms)^## (?P<name>Requirements|Non-functional Requirements)\n"
    r"(?P<body>.*?)(?=^## |\Z)"
)
_TRUSTED_LEGACY_SECTION_KIND = {
    "Requirements": "FR",
    "Non-functional Requirements": "NFR",
}
_TRUSTED_LEGACY_REQUIREMENT_SUBSECTION = re.compile(
    r"(?ms)^### (?P<name>Functional requirements|Non-functional requirements)\n"
    r"(?P<body>.*?)(?=^### |\Z)"
)
_TRUSTED_LEGACY_SUBSECTION_KIND = {
    "Functional requirements": "FR",
    "Non-functional requirements": "NFR",
}
_TRUSTED_CHILD_SPACE_NAME = re.compile(
    r"REQ-(?P<package>[0-9]{4})\.(?P<kind>FR|NFR|IF)"
)


class RegistryError(ValueError):
    """Raised when the Stage 99 registry cannot be trusted."""


@dataclasses.dataclass(frozen=True, order=True)
class RegistryFinding:
    code: str
    path: str
    message: str


@dataclasses.dataclass(frozen=True)
class IdentitySpace:
    prefix: str
    width: int
    high_water: int
    next_number: int
    current_issued: tuple[int, ...]
    reserved_history: tuple[int, ...]
    child_spaces: Mapping[str, "IdentitySpace"]


@dataclasses.dataclass(frozen=True)
class RequirementAllocationState:
    high_water: int
    next_number: int
    current_issued: tuple[int, ...]
    reserved_history: tuple[int, ...]


@dataclasses.dataclass(frozen=True)
class RequirementAllocationBaseline:
    source: str
    package_high_water: int
    child_spaces: Mapping[str, RequirementAllocationState]


@dataclasses.dataclass(frozen=True)
class DocumentRegistry:
    source: pathlib.PurePosixPath
    profiles: Mapping[str, Mapping[str, object]]
    template_roles: Mapping[str, Mapping[str, object]]
    lifecycles: Mapping[str, tuple[str, ...]]
    identity_spaces: Mapping[str, IdentitySpace]
    transitions: Mapping[str, Mapping[str, tuple[str, ...]]]
    indexes: Mapping[str, str]
    template_catalog: str
    common: Mapping[str, object]


@functools.lru_cache(maxsize=1)
def _registered_types() -> Mapping[str, str]:
    """Cache the Registry-declared family/kind document type per profile."""

    return MappingProxyType(
        {
            profile_id: str(profile["type"])
            for profile_id, profile in load_registry().profiles.items()
            if isinstance(profile.get("type"), str)
        }
    )


def document_type(profile_id: str) -> str:
    """Return the canonical `family/kind` document type for a Registry profile."""

    return _registered_types()[profile_id]


def _declares_provider_binding(profile: Mapping[str, object]) -> bool:
    """A provider runtime owns this surface, so the document type system defers."""

    exceptions = profile.get("exceptions")
    # The registry freeze turns declared lists into tuples, so accept both.
    return isinstance(exceptions, (list, tuple)) and any(
        isinstance(item, Mapping) and item.get("kind") == "provider-owned-binding"
        for item in exceptions
    )


def _trusted_requirement_path_match(path: str) -> re.Match[str] | None:
    """Match current or immutable predecessor Requirement Package paths."""

    return _TRUSTED_REQUIREMENT_PATH.fullmatch(
        path
    ) or _TRUSTED_LEGACY_REQUIREMENT_PATH.fullmatch(path)


def _read_regular_file(path: pathlib.Path, maximum: int) -> bytes:
    try:
        metadata = path.lstat()
    except OSError as error:
        raise RegistryError(f"cannot stat registry input: {error}") from error
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode):
        raise RegistryError("registry input must be a regular non-symlink file")
    if metadata.st_size > maximum:
        raise RegistryError("registry input exceeds the byte limit")
    absolute = pathlib.Path(os.path.abspath(path))
    directory_flags = (
        os.O_RDONLY
        | os.O_DIRECTORY
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NOFOLLOW", 0)
    )
    file_flags = (
        os.O_RDONLY
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NOFOLLOW", 0)
        | os.O_NONBLOCK
    )
    directory_descriptor = -1
    try:
        directory_descriptor = os.open(absolute.anchor, directory_flags)
        for component in absolute.parts[1:-1]:
            next_descriptor = os.open(
                component,
                directory_flags,
                dir_fd=directory_descriptor,
            )
            os.close(directory_descriptor)
            directory_descriptor = next_descriptor
        descriptor = os.open(
            absolute.name,
            file_flags,
            dir_fd=directory_descriptor,
        )
        try:
            opened = os.fstat(descriptor)
            if not stat.S_ISREG(opened.st_mode):
                raise RegistryError("registry input changed to a non-regular file")
            data = os.read(descriptor, maximum + 1)
        finally:
            os.close(descriptor)
    except OSError as error:
        raise RegistryError(f"cannot read registry input: {error}") from error
    finally:
        if directory_descriptor >= 0:
            os.close(directory_descriptor)
    if len(data) > maximum:
        raise RegistryError("registry input exceeds the byte limit")
    return data


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise RegistryError(f"duplicate JSON member: {key}")
        result[key] = value
    return result


def _parse_json(path: pathlib.Path, maximum: int) -> object:
    try:
        source = _read_regular_file(path, maximum).decode("utf-8")
    except UnicodeError as error:
        raise RegistryError("registry input must be UTF-8") from error
    try:
        raw = json.loads(source, object_pairs_hook=_unique_object)
    except (json.JSONDecodeError, RecursionError, RegistryError) as error:
        raise RegistryError(f"invalid registry JSON: {error}") from error
    _require_bounded_depth(raw)
    return raw


def load_registry_document(
    path: pathlib.Path = DEFAULT_REGISTRY,
) -> Mapping[str, object]:
    """Load one bounded Registry JSON document without interpreting its contract."""

    raw = _parse_json(path, MAX_REGISTRY_BYTES)
    if not isinstance(raw, Mapping):
        raise RegistryError("registry document must be a mapping")
    return raw


def _require_bounded_depth(value: object, depth: int = 0) -> None:
    if depth > MAX_JSON_DEPTH:
        raise RegistryError("registry JSON exceeds the depth limit")
    if isinstance(value, Mapping):
        for item in value.values():
            _require_bounded_depth(item, depth + 1)
    elif isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        for item in value:
            _require_bounded_depth(item, depth + 1)


def _freeze(value: object) -> object:
    if isinstance(value, Mapping):
        return MappingProxyType(
            {str(key): _freeze(item) for key, item in value.items()}
        )
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return tuple(_freeze(item) for item in value)
    return value


def _identity_space(raw: Mapping[str, object]) -> IdentitySpace:
    children = raw.get("child_spaces", {})
    if not isinstance(children, Mapping):
        raise RegistryError("identity child_spaces must be a mapping")
    return IdentitySpace(
        prefix=str(raw["prefix"]),
        width=int(raw["width"]),
        high_water=int(raw["high_water"]),
        next_number=int(raw["next_number"]),
        current_issued=tuple(int(number) for number in raw.get("current_issued", ())),
        reserved_history=tuple(
            int(number) for number in raw.get("reserved_history", ())
        ),
        child_spaces=MappingProxyType(
            {
                str(name): _identity_space(child)
                for name, child in children.items()
                if isinstance(child, Mapping)
            }
        ),
    )


def validate_registry(
    raw: Mapping[str, object],
    *,
    trusted_requirement_baseline: RequirementAllocationBaseline | None = None,
    allow_requirement_allocation_transition: bool = False,
) -> tuple[RegistryFinding, ...]:
    """Return deterministic schema and semantic findings for ``raw``."""

    findings: list[RegistryFinding] = []
    try:
        schema = _parse_json(DEFAULT_PROFILE_SCHEMA, MAX_SCHEMA_BYTES)
    except RegistryError as error:
        return (RegistryFinding("schema-unavailable", "$", str(error)),)
    if not isinstance(schema, Mapping):
        return (
            RegistryFinding("schema-invalid", "$", "profile schema is not a mapping"),
        )
    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError:
        return (
            RegistryFinding(
                "schema-invalid", "$", "profile schema is not valid Draft 2020-12"
            ),
        )
    validator = Draft202012Validator(schema)
    for error in sorted(
        validator.iter_errors(raw), key=lambda item: tuple(map(str, item.path))
    ):
        location = ".".join(map(str, error.path)) or "$"
        findings.append(RegistryFinding("schema-invalid", location, error.message))
    if findings:
        spaces = raw.get("identity_spaces")
        if isinstance(spaces, Mapping):
            _validate_identity_space_bounds(spaces, "identity_spaces", findings)
        return tuple(sorted(set(findings)))
    profiles = raw.get("profiles")
    profile_ids: list[str] = []
    profile_lifecycles: dict[str, object] = {}
    profile_entries: list[tuple[int, Mapping[str, object]]] = []
    if isinstance(profiles, list):
        for index, profile in enumerate(profiles):
            if not isinstance(profile, Mapping):
                continue
            profile_entries.append((index, profile))
            profile_id = profile.get("profile_id")
            if isinstance(profile_id, str):
                profile_ids.append(profile_id)
                profile_lifecycles[profile_id] = profile.get("lifecycle_id")
                if profile_id == "release":
                    findings.append(
                        RegistryFinding(
                            "retired-profile",
                            f"profiles.{index}",
                            "Release is not an active profile",
                        )
                    )
            path_pattern = profile.get("path_pattern")
            if isinstance(path_pattern, str) and not _safe_path_pattern(path_pattern):
                findings.append(
                    RegistryFinding(
                        "path-pattern-invalid", f"profiles.{index}", path_pattern
                    )
                )
            artifact_pattern = profile.get("artifact_id_pattern")
            if isinstance(artifact_pattern, str) and not _safe_artifact_pattern(
                artifact_pattern
            ):
                findings.append(
                    RegistryFinding(
                        "artifact-pattern-invalid",
                        f"profiles.{index}",
                        artifact_pattern,
                    )
                )
    duplicates = sorted({name for name in profile_ids if profile_ids.count(name) > 1})
    for name in duplicates:
        findings.append(RegistryFinding("profile-duplicate", "profiles", name))
    for left_offset, (left_index, left) in enumerate(profile_entries):
        left_id = left.get("profile_id")
        left_pattern = left.get("path_pattern")
        if (
            not isinstance(left_id, str)
            or left_id in FALLBACK_PROFILE_IDS
            or not isinstance(left_pattern, str)
        ):
            continue
        for right_index, right in profile_entries[left_offset + 1 :]:
            right_id = right.get("profile_id")
            right_pattern = right.get("path_pattern")
            if (
                not isinstance(right_id, str)
                or right_id in FALLBACK_PROFILE_IDS
                or not isinstance(right_pattern, str)
            ):
                continue
            if _declares_provider_binding(left) or _declares_provider_binding(right):
                # A provider-owned binding is a narrower runtime-owned surface
                # inside a generic document route; its runtime owner resolves it.
                continue
            if _path_patterns_overlap(left_pattern, right_pattern):
                findings.append(
                    RegistryFinding(
                        "profile-path-overlap",
                        f"profiles.{left_index},profiles.{right_index}",
                        f"profiles {left_id} and {right_id} can own the same path",
                    )
                )
    known_profiles = set(profile_ids)
    additional_owners: dict[str, str] = {}
    for index, profile in profile_entries:
        additional = profile.get("additional_paths", ())
        if not isinstance(additional, (list, tuple)):
            continue
        for path in additional:
            if (
                not isinstance(path, str)
                or not _registry_owned_root(path)
                or not _safe_path_pattern(path)
                or "{" in path
                or "}" in path
                or profile.get("identity_relation") != "none"
            ):
                findings.append(
                    RegistryFinding(
                        "additional-path-invalid",
                        f"profiles.{index}",
                        "additional paths must be exact safe identity-free routes",
                    )
                )
                continue
            owners = [
                other.get("profile_id")
                for _, other in profile_entries
                if other is not profile
                and other.get("profile_id") != "unsupported"
                and isinstance(other.get("path_pattern"), str)
                and _path_regex(other["path_pattern"]).fullmatch(path)
            ]
            if owners or path in additional_owners:
                findings.append(
                    RegistryFinding("profile-path-overlap", f"profiles.{index}", path)
                )
            additional_owners[path] = str(profile.get("profile_id"))
    roles = raw.get("template_roles")
    known_roles = set(roles) if isinstance(roles, Mapping) else set()
    role_sources: list[str] = []
    if isinstance(roles, Mapping):
        for role, definition in roles.items():
            if not isinstance(definition, Mapping):
                continue
            extra = set(definition) - {"source", "profile_id"}
            if extra:
                findings.append(
                    RegistryFinding(
                        "template-target-forbidden",
                        f"template_roles.{role}",
                        ",".join(sorted(extra)),
                    )
                )
            if definition.get("profile_id") not in known_profiles:
                findings.append(
                    RegistryFinding(
                        "template-profile-unknown",
                        f"template_roles.{role}",
                        str(definition.get("profile_id")),
                    )
                )
            source = definition.get("source")
            if isinstance(source, str):
                role_sources.append(source)
                if not _safe_template_source(source):
                    findings.append(
                        RegistryFinding(
                            "template-source-invalid",
                            f"template_roles.{role}",
                            "template source must be a canonical Stage 99 path",
                        )
                    )
    for source in sorted(
        {item for item in role_sources if role_sources.count(item) > 1}
    ):
        findings.append(
            RegistryFinding("template-source-duplicate", "template_roles", source)
        )
    for index, profile in profile_entries:
        profile_id = profile.get("profile_id")
        template_id = profile.get("template_id")
        if template_id is not None:
            definition = roles.get(template_id) if isinstance(roles, Mapping) else None
            if template_id not in known_roles or not isinstance(definition, Mapping):
                findings.append(
                    RegistryFinding(
                        "profile-template-unknown",
                        f"profiles.{index}",
                        str(template_id),
                    )
                )
            elif definition.get("profile_id") != profile_id:
                findings.append(
                    RegistryFinding(
                        "profile-template-mismatch",
                        f"profiles.{index}",
                        "template role must reference its owning profile",
                    )
                )
        for required_key, optional_key in (
            ("required_frontmatter", "optional_frontmatter"),
            ("required_sections", "optional_sections"),
        ):
            required_values = profile.get(required_key)
            optional_values = profile.get(optional_key)
            if isinstance(required_values, list) and isinstance(optional_values, list):
                overlap = set(required_values) & set(optional_values)
                if overlap:
                    findings.append(
                        RegistryFinding(
                            "profile-contract-overlap",
                            f"profiles.{index}",
                            ",".join(sorted(overlap)),
                        )
                    )
        traceability = profile.get("traceability")
        parents = (
            traceability.get("allowed_parent_profiles")
            if isinstance(traceability, Mapping)
            else None
        )
        if isinstance(parents, list):
            for parent in parents:
                if parent not in known_profiles:
                    findings.append(
                        RegistryFinding(
                            "traceability-profile-unknown",
                            f"profiles.{index}",
                            str(parent),
                        )
                    )
        path_pattern = profile.get("path_pattern")
        artifact_pattern = profile.get("artifact_id_pattern")
        identity_relation = profile.get("identity_relation")
        frontmatter_policy = profile.get("frontmatter_policy")
        required_frontmatter = profile.get("required_frontmatter")
        optional_frontmatter = profile.get("optional_frontmatter")
        if (
            isinstance(path_pattern, str)
            and path_pattern.endswith(".md")
            and profile_id not in FALLBACK_PROFILE_IDS
            and frontmatter_policy != "required"
        ):
            findings.append(
                RegistryFinding(
                    "markdown-frontmatter-policy-invalid",
                    f"profiles.{index}",
                    "canonical Markdown profiles must require frontmatter",
                )
            )
        if frontmatter_policy == "required" and not _declares_provider_binding(profile):
            if (
                not isinstance(required_frontmatter, list)
                or "type" not in required_frontmatter
                or isinstance(optional_frontmatter, list)
                and "type" in optional_frontmatter
            ):
                findings.append(
                    RegistryFinding(
                        "type-contract-invalid",
                        f"profiles.{index}",
                        "frontmatter-required profiles must require exact type",
                    )
                )
        elif frontmatter_policy == "absent" and (
            required_frontmatter or optional_frontmatter
        ):
            findings.append(
                RegistryFinding(
                    "frontmatter-policy-invalid",
                    f"profiles.{index}",
                    "frontmatter-absent profiles cannot declare frontmatter keys",
                )
            )
        elif frontmatter_policy == "unmanaged" and profile_id != "unsupported":
            findings.append(
                RegistryFinding(
                    "frontmatter-policy-invalid",
                    f"profiles.{index}",
                    "only the unsupported fallback may leave frontmatter unmanaged",
                )
            )
        path_tokens = (
            set(re.findall(r"\{([^{}:]+)(?::4)?\}", path_pattern))
            if isinstance(path_pattern, str)
            else set()
        )
        artifact_tokens = (
            set(re.findall(r"\{([^{}:]+)(?::4)?\}", artifact_pattern))
            if isinstance(artifact_pattern, str)
            else set()
        )
        relation_valid = (
            (identity_relation == "none" and artifact_pattern is None)
            or (
                # A tombstone reuses the retired document's identity instead of
                # allocating a new one; its owner script derives the exact value.
                identity_relation == "inherited"
                and "retired_artifact_id" in artifact_tokens
            )
            or (
                identity_relation == "direct"
                and "number" in path_tokens
                and "number" in artifact_tokens
            )
            or (
                identity_relation == "package-member"
                and bool({"package_number", "number"} & path_tokens & artifact_tokens)
            )
            or (
                identity_relation == "subject-member"
                and "subject_number" in path_tokens
                and "number" in artifact_tokens
            )
        )
        if not relation_valid:
            findings.append(
                RegistryFinding(
                    "identity-relation-invalid",
                    f"profiles.{index}",
                    "identity relation must use its registered path and artifact tokens",
                )
            )
        if isinstance(template_id, str) and isinstance(roles, Mapping):
            definition = roles.get(template_id)
            source = (
                definition.get("source") if isinstance(definition, Mapping) else None
            )
            if isinstance(source, str) and not source.endswith(".template.md"):
                media_type = profile.get("media_type")
                if not isinstance(media_type, str) or not media_type:
                    findings.append(
                        RegistryFinding(
                            "machine-media-type-missing",
                            f"profiles.{index}",
                            "machine contract profiles require a media_type",
                        )
                    )
    lifecycles = raw.get("lifecycles")
    if isinstance(lifecycles, Mapping):
        for lifecycle_id, lifecycle in lifecycles.items():
            if not isinstance(lifecycle, Mapping):
                continue
            statuses = lifecycle.get("statuses")
            transitions = lifecycle.get("transitions")
            status_set = set(statuses) if isinstance(statuses, list) else set()
            if isinstance(transitions, Mapping):
                if set(transitions) != status_set:
                    findings.append(
                        RegistryFinding(
                            "lifecycle-incomplete",
                            f"lifecycles.{lifecycle_id}",
                            "every status requires one transition entry",
                        )
                    )
                for source, targets in transitions.items():
                    if isinstance(targets, list) and not set(targets) <= status_set:
                        findings.append(
                            RegistryFinding(
                                "transition-unregistered",
                                f"lifecycles.{lifecycle_id}.{source}",
                                "transition target is not a registered status",
                            )
                        )
    spaces = raw.get("identity_spaces")
    if isinstance(spaces, Mapping):
        allocation_bounds_valid = _validate_identity_space_bounds(
            spaces, "identity_spaces", findings
        )
        if allocation_bounds_valid:
            _validate_identity_spaces(spaces, "identity_spaces", findings)
            requirement_space = spaces.get("requirement")
            if isinstance(requirement_space, Mapping):
                _validate_requirement_child_spaces(requirement_space, findings)
                if allow_requirement_allocation_transition:
                    _validate_requirement_allocation_transition(
                        requirement_space, trusted_requirement_baseline, findings
                    )
    transitions = raw.get("transitions")
    if isinstance(transitions, Mapping):
        for profile_id, lifecycle_id in transitions.items():
            if profile_id not in known_profiles:
                findings.append(
                    RegistryFinding(
                        "transition-profile-unknown", "transitions", str(profile_id)
                    )
                )
            if not isinstance(lifecycles, Mapping) or lifecycle_id not in lifecycles:
                findings.append(
                    RegistryFinding(
                        "transition-lifecycle-unknown",
                        f"transitions.{profile_id}",
                        str(lifecycle_id),
                    )
                )
        for profile_id, lifecycle_id in profile_lifecycles.items():
            mapped_lifecycle = transitions.get(profile_id)
            if lifecycle_id is None and mapped_lifecycle is not None:
                findings.append(
                    RegistryFinding(
                        "transition-profile-mismatch",
                        f"transitions.{profile_id}",
                        "profile without a lifecycle must not have a transition mapping",
                    )
                )
            elif lifecycle_id is not None and mapped_lifecycle != lifecycle_id:
                findings.append(
                    RegistryFinding(
                        "transition-profile-mismatch",
                        f"transitions.{profile_id}",
                        "transition mapping must equal the profile lifecycle_id",
                    )
                )
    indexes = raw.get("indexes")
    if isinstance(indexes, Mapping):
        for index_path, member_profile in indexes.items():
            if member_profile not in known_profiles:
                findings.append(
                    RegistryFinding(
                        "index-profile-unknown",
                        f"indexes.{index_path}",
                        str(member_profile),
                    )
                )
    return tuple(sorted(set(findings)))


TEMPLATE_PLACEHOLDER_SENTINELS: Mapping[str, str] = MappingProxyType(
    {
        "YYYY-MM-DDTHH:MM:SSZ": "2000-01-01T00:00:00Z",
        "YYYY-MM-DD": "2000-01-01",
        "#.#.#": "0.0.0",
    }
)


def resolve_template_placeholders(values: Mapping[str, object]) -> dict[str, object]:
    """Replace Stage 99 template placeholders with schema-valid sentinel values.

    A template source carries a readable placeholder where an authored document
    carries a typed value. One shared table keeps the schema strict for authored
    documents while every template consumer substitutes identically.
    """

    return {
        key: TEMPLATE_PLACEHOLDER_SENTINELS.get(value, value)
        if isinstance(value, str)
        else value
        for key, value in values.items()
    }


def validate_frontmatter(
    values: Mapping[str, object],
    schema_path: pathlib.Path = DEFAULT_FRONTMATTER_SCHEMA,
) -> tuple[RegistryFinding, ...]:
    """Validate one parsed frontmatter mapping against the bounded Stage 99 schema."""

    schema = _parse_json(schema_path, MAX_SCHEMA_BYTES)
    if not isinstance(schema, Mapping):
        raise RegistryError("frontmatter schema is not a mapping")
    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError as error:
        raise RegistryError("frontmatter schema is not valid Draft 2020-12") from error
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    normalized = _json_schema_value(values)
    return tuple(
        RegistryFinding(
            "frontmatter-schema-invalid",
            ".".join(map(str, error.path)) or "$",
            error.message,
        )
        for error in sorted(
            validator.iter_errors(normalized),
            key=lambda item: tuple(map(str, item.path)),
        )
    )


def _json_schema_value(value: object) -> object:
    if isinstance(value, Mapping):
        return {str(key): _json_schema_value(item) for key, item in value.items()}
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [_json_schema_value(item) for item in value]
    if isinstance(value, (dt.datetime, dt.date)):
        return value.isoformat()
    return value


def _validate_identity_spaces(
    spaces: Mapping[str, object], location: str, findings: list[RegistryFinding]
) -> None:
    for name, value in spaces.items():
        if not isinstance(value, Mapping):
            continue
        high_water = value.get("high_water")
        next_number = value.get("next_number")
        if (
            type(high_water) is int
            and type(next_number) is int
            and next_number != high_water + 1
        ):
            findings.append(
                RegistryFinding(
                    "identity-not-monotonic",
                    f"{location}.{name}",
                    "next_number must equal high_water plus one",
                )
            )
        current_issued = value.get("current_issued")
        reserved_history = value.get("reserved_history")
        for field_name, numbers in (
            ("current_issued", current_issued),
            ("reserved_history", reserved_history),
        ):
            if not isinstance(numbers, list) or type(high_water) is not int:
                continue
            if numbers != sorted(numbers):
                findings.append(
                    RegistryFinding(
                        "identity-allocation-order",
                        f"{location}.{name}",
                        f"{field_name} must be numerically sorted",
                    )
                )
            if any(
                type(number) is not int or number < 1 or number > high_water
                for number in numbers
            ):
                findings.append(
                    RegistryFinding(
                        "identity-allocation-invalid",
                        f"{location}.{name}",
                        f"{field_name} must stay within the allocation high-water",
                    )
                )
        if (
            isinstance(current_issued, list)
            and isinstance(reserved_history, list)
            and type(high_water) is int
        ):
            current_numbers = set(current_issued)
            reserved_numbers = set(reserved_history)
            if current_numbers & reserved_numbers:
                findings.append(
                    RegistryFinding(
                        "identity-reserved-history-reissued",
                        f"{location}.{name}",
                        "reserved_history numbers can never be currently issued again",
                    )
                )
            if current_numbers | reserved_numbers != set(range(1, high_water + 1)):
                findings.append(
                    RegistryFinding(
                        "identity-allocation-history-incomplete",
                        f"{location}.{name}",
                        "current and permanently reserved numbers must classify the full allocation history",
                    )
                )
        children = value.get("child_spaces")
        if isinstance(children, Mapping):
            _validate_identity_spaces(
                children, f"{location}.{name}.child_spaces", findings
            )


def _validate_identity_space_bounds(
    spaces: Mapping[str, object],
    location: str,
    findings: list[RegistryFinding],
) -> bool:
    """Reject allocation sizes before semantic range/set expansion."""

    if len(spaces) > MAX_IDENTITY_ALLOCATION_VALUE:
        findings.append(
            RegistryFinding(
                "identity-allocation-bound-exceeded",
                location,
                "identity-space count exceeds the four-digit allocation bound",
            )
        )
        return False
    valid = True
    for name, value in spaces.items():
        if not isinstance(value, Mapping):
            continue
        item_location = f"{location}.{name}"
        for field_name in ("high_water", "next_number"):
            number = value.get(field_name)
            if type(number) is int and number > MAX_IDENTITY_ALLOCATION_VALUE:
                findings.append(
                    RegistryFinding(
                        "identity-allocation-bound-exceeded",
                        f"{item_location}.{field_name}",
                        f"{field_name} exceeds the four-digit allocation bound",
                    )
                )
                valid = False
        for field_name in ("current_issued", "reserved_history"):
            numbers = value.get(field_name)
            if not isinstance(numbers, list):
                continue
            if len(numbers) > MAX_IDENTITY_ALLOCATION_VALUE:
                findings.append(
                    RegistryFinding(
                        "identity-allocation-bound-exceeded",
                        f"{item_location}.{field_name}",
                        f"{field_name} count exceeds the four-digit allocation bound",
                    )
                )
                valid = False
                continue
            if any(
                type(number) is int and number > MAX_IDENTITY_ALLOCATION_VALUE
                for number in numbers
            ):
                findings.append(
                    RegistryFinding(
                        "identity-allocation-bound-exceeded",
                        f"{item_location}.{field_name}",
                        f"{field_name} contains a value above the four-digit allocation bound",
                    )
                )
                valid = False
        children = value.get("child_spaces")
        if isinstance(children, Mapping) and not _validate_identity_space_bounds(
            children, f"{item_location}.child_spaces", findings
        ):
            valid = False
    return valid


def _validate_requirement_child_spaces(
    requirement: Mapping[str, object], findings: list[RegistryFinding]
) -> None:
    children = requirement.get("child_spaces")
    if not isinstance(children, Mapping):
        return
    packages: dict[str, set[str]] = {}
    for name, value in children.items():
        match = re.fullmatch(r"(REQ-[0-9]{4})\.(FR|NFR|IF)", str(name))
        if match is None or not isinstance(value, Mapping):
            findings.append(
                RegistryFinding(
                    "requirement-child-space-invalid",
                    f"identity_spaces.requirement.child_spaces.{name}",
                    "Requirement child spaces must be package-qualified",
                )
            )
            continue
        package_id, kind = match.groups()
        packages.setdefault(package_id, set()).add(kind)
        if value.get("prefix") != f"{package_id}-{kind}-":
            findings.append(
                RegistryFinding(
                    "requirement-child-prefix-invalid",
                    f"identity_spaces.requirement.child_spaces.{name}",
                    "child prefix must contain its full Requirement package ID",
                )
            )
        if not isinstance(value.get("current_issued"), list):
            findings.append(
                RegistryFinding(
                    "requirement-current-issued-missing",
                    f"identity_spaces.requirement.child_spaces.{name}",
                    "Requirement child spaces must record current_issued numbers",
                )
            )
        if not isinstance(value.get("reserved_history"), list):
            findings.append(
                RegistryFinding(
                    "requirement-reserved-history-missing",
                    f"identity_spaces.requirement.child_spaces.{name}",
                    "Requirement child spaces must record permanently reserved history",
                )
            )
    for package_id, kinds in packages.items():
        if kinds != {"FR", "NFR", "IF"}:
            findings.append(
                RegistryFinding(
                    "requirement-child-space-incomplete",
                    f"identity_spaces.requirement.child_spaces.{package_id}",
                    "each Requirement package needs FR, NFR, and IF allocation spaces",
                )
            )
    high_water = requirement.get("high_water")
    if type(high_water) is int:
        for package_id in sorted(packages):
            package_number = int(package_id.removeprefix("REQ-"))
            if package_number > high_water:
                findings.append(
                    RegistryFinding(
                        "requirement-child-space-above-package-high-water",
                        f"identity_spaces.requirement.child_spaces.{package_id}",
                        "Requirement child spaces cannot exceed the package high-water",
                    )
                )
        expected_packages = {f"REQ-{number:04d}" for number in range(1, high_water + 1)}
        for package_id in sorted(expected_packages - set(packages)):
            findings.append(
                RegistryFinding(
                    "requirement-package-space-missing",
                    "identity_spaces.requirement.child_spaces",
                    f"reserved package has no child allocation spaces: {package_id}",
                )
            )


def _terminate_process(process: subprocess.Popen[bytes]) -> None:
    if process.poll() is None:
        process.kill()
    try:
        process.wait(timeout=1)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()


def _run_bounded_process(
    argv: Sequence[str],
    *,
    stdout_limit: int,
    stderr_limit: int,
    timeout: float = GIT_READ_TIMEOUT_SECONDS,
) -> tuple[int, bytes, bytes]:
    """Run an argv-only process while bounding both output streams in flight."""

    if (
        not argv
        or stdout_limit < 0
        or stderr_limit < 0
        or timeout <= 0
        or any(not isinstance(part, str) or "\0" in part for part in argv)
    ):
        raise RegistryError("trusted subprocess invocation is invalid")
    try:
        process = subprocess.Popen(
            list(argv),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except OSError as error:
        raise RegistryError(f"cannot run trusted subprocess: {error}") from error
    assert process.stdout is not None
    assert process.stderr is not None
    streams = selectors.DefaultSelector()
    buffers = {"stdout": bytearray(), "stderr": bytearray()}
    limits = {"stdout": stdout_limit, "stderr": stderr_limit}
    streams.register(process.stdout, selectors.EVENT_READ, "stdout")
    streams.register(process.stderr, selectors.EVENT_READ, "stderr")
    deadline = time.monotonic() + timeout
    try:
        while streams.get_map():
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise RegistryError("trusted subprocess timed out")
            events = streams.select(min(remaining, 0.1))
            for key, _ in events:
                channel = str(key.data)
                allowance = limits[channel] - len(buffers[channel]) + 1
                chunk = os.read(key.fd, min(64 * 1024, max(1, allowance)))
                if not chunk:
                    streams.unregister(key.fileobj)
                    continue
                buffers[channel].extend(chunk)
                if len(buffers[channel]) > limits[channel]:
                    raise RegistryError(
                        f"trusted subprocess {channel} exceeds the byte limit"
                    )
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise RegistryError("trusted subprocess timed out")
        returncode = process.wait(timeout=remaining)
        return returncode, bytes(buffers["stdout"]), bytes(buffers["stderr"])
    except (OSError, subprocess.TimeoutExpired) as error:
        raise RegistryError(
            f"cannot read trusted subprocess output: {error}"
        ) from error
    finally:
        _terminate_process(process)
        streams.close()
        process.stdout.close()
        process.stderr.close()


def _git_read(args: Sequence[str], *, root: pathlib.Path = ROOT) -> str:
    try:
        returncode, stdout, stderr = _run_bounded_process(
            ["git", "-C", str(root), *args],
            stdout_limit=MAX_REGISTRY_BYTES,
            stderr_limit=MAX_GIT_STDERR_BYTES,
        )
    except RegistryError as error:
        raise RegistryError(
            f"cannot read trusted Git allocation state: {error}"
        ) from error
    if returncode != 0:
        message = stderr.decode("utf-8", errors="replace").strip()
        raise RegistryError(
            "cannot read trusted Git allocation state"
            + (f": {message}" if message else "")
        )
    try:
        return stdout.decode("utf-8")
    except UnicodeError as error:
        raise RegistryError("trusted Git allocation state must be UTF-8") from error


def _trusted_blob_snapshot(
    revision: str,
    *,
    root: pathlib.Path,
) -> tuple[str, str, Mapping[str, str]]:
    if revision == ":":
        source = "git-index"
        listing = _git_read(
            [
                "ls-files",
                "--stage",
                "-z",
                "--",
                "docs/99.templates/registry.json",
                "docs/01.requirements",
            ],
            root=root,
        )
        entry_pattern = re.compile(
            r"(?P<mode>[0-7]{6}) (?P<oid>[0-9a-f]{40,64}) "
            r"(?P<stage>[0-3])\t(?P<path>.+)",
            re.DOTALL,
        )
    else:
        resolved = _git_read(
            [
                "rev-parse",
                "--verify",
                "--end-of-options",
                f"{revision}^{{commit}}",
            ],
            root=root,
        ).strip()
        if _GIT_OID.fullmatch(resolved) is None:
            raise RegistryError(
                "trusted Git predecessor did not resolve to a commit OID"
            )
        source = resolved
        listing = _git_read(
            [
                "ls-tree",
                "-r",
                "-z",
                resolved,
                "--",
                "docs/99.templates/registry.json",
                "docs/01.requirements",
            ],
            root=root,
        )
        entry_pattern = re.compile(
            r"(?P<mode>[0-7]{6}) (?P<type>[a-z]+) "
            r"(?P<oid>[0-9a-f]{40,64})\t(?P<path>.+)",
            re.DOTALL,
        )

    entries = [entry for entry in listing.split("\0") if entry]
    if len(entries) > MAX_TRUSTED_REQUIREMENT_PATHS:
        raise RegistryError("trusted Requirement predecessor has too many paths")
    blobs: dict[str, str] = {}
    for entry in entries:
        match = entry_pattern.fullmatch(entry)
        if match is None:
            raise RegistryError("trusted Git allocation snapshot entry is malformed")
        path = match.group("path")
        if (
            path != "docs/99.templates/registry.json"
            and path != "docs/01.requirements/README.md"
            and _trusted_requirement_path_match(path) is None
        ):
            raise RegistryError(
                f"trusted Requirement predecessor path is not canonical: {path}"
            )
        if revision == ":" and match.group("stage") != "0":
            raise RegistryError("trusted Git index allocation snapshot is conflicted")
        if revision != ":" and match.group("type") != "blob":
            raise RegistryError("trusted Git allocation snapshot contains a non-blob")
        if match.group("mode") not in {"100644", "100755"}:
            raise RegistryError(
                "trusted Git allocation snapshot contains a non-regular blob"
            )
        if path in blobs:
            raise RegistryError(
                "trusted Git allocation snapshot contains duplicate paths"
            )
        blobs[path] = match.group("oid")
    registry_oid = blobs.pop("docs/99.templates/registry.json", None)
    blobs.pop("docs/01.requirements/README.md", None)
    if registry_oid is None:
        raise RegistryError("trusted Registry predecessor is missing")
    registry_text = _git_read(["cat-file", "blob", registry_oid], root=root)
    package_texts: dict[str, str] = {}
    for path, oid in sorted(blobs.items()):
        text = _git_read(["cat-file", "blob", oid], root=root)
        if len(text.encode("utf-8")) > MAX_TRUSTED_REQUIREMENT_BYTES:
            raise RegistryError(
                f"trusted Requirement predecessor exceeds the byte limit: {path}"
            )
        package_texts[path] = text
    return source, registry_text, MappingProxyType(package_texts)


def load_trusted_requirement_allocation_baseline(
    revision: str,
    *,
    root: pathlib.Path = ROOT,
) -> RequirementAllocationBaseline:
    """Derive immutable history from an explicit index marker or commit."""

    source, registry_text, package_texts = _trusted_blob_snapshot(revision, root=root)
    try:
        raw = json.loads(registry_text, object_pairs_hook=_unique_object)
    except (json.JSONDecodeError, RegistryError) as error:
        raise RegistryError(
            f"trusted Registry predecessor is invalid: {error}"
        ) from error
    if not isinstance(raw, Mapping):
        raise RegistryError("trusted Registry predecessor must be a mapping")
    identity_spaces = raw.get("identity_spaces")
    requirement = (
        identity_spaces.get("requirement")
        if isinstance(identity_spaces, Mapping)
        else None
    )
    children = (
        requirement.get("child_spaces") if isinstance(requirement, Mapping) else None
    )
    package_high_water = (
        requirement.get("high_water") if isinstance(requirement, Mapping) else None
    )
    package_next_number = (
        requirement.get("next_number") if isinstance(requirement, Mapping) else None
    )
    if (
        not isinstance(children, Mapping)
        or type(package_high_water) is not int
        or type(package_next_number) is not int
        or not 1 <= package_high_water <= MAX_TRUSTED_REQUIREMENT_PACKAGES
        or package_next_number != package_high_water + 1
    ):
        raise RegistryError("trusted Requirement allocation predecessor is missing")

    trusted_paths = sorted(package_texts)
    expected_packages = {f"{number:04d}" for number in range(1, package_high_water + 1)}
    actual_packages = {
        match.group("package")
        for path in trusted_paths
        if (match := _trusted_requirement_path_match(path)) is not None
    }
    if actual_packages and actual_packages != expected_packages:
        raise RegistryError(
            "trusted Requirement predecessor does not cover its package high-water"
        )

    current_paths = [
        path for path in trusted_paths if _TRUSTED_REQUIREMENT_PATH.fullmatch(path)
    ]
    legacy_paths = [
        path
        for path in trusted_paths
        if _TRUSTED_LEGACY_REQUIREMENT_PATH.fullmatch(path)
    ]
    if current_paths and legacy_paths:
        raise RegistryError(
            "trusted Requirement predecessor mixes current and legacy package paths"
        )
    legacy_predecessor = bool(legacy_paths)
    declarations: dict[str, set[int]] = {}
    for path in trusted_paths:
        path_match = _trusted_requirement_path_match(path)
        assert path_match is not None
        text = package_texts[path]
        package_number = path_match.group("package")
        section_pattern = (
            _TRUSTED_LEGACY_REQUIREMENT_SECTION
            if legacy_predecessor
            else _TRUSTED_REQUIREMENT_SECTION
        )
        section_kinds = (
            _TRUSTED_LEGACY_SECTION_KIND
            if legacy_predecessor
            else _TRUSTED_SECTION_KIND
        )
        child_pattern = (
            _TRUSTED_LEGACY_CHILD_ID if legacy_predecessor else _TRUSTED_CHILD_ID
        )
        for section in section_pattern.finditer(text):
            bodies = ((section_kinds[section.group("name")], section.group("body")),)
            if legacy_predecessor and section.group("name") == "Requirements":
                subsections = tuple(
                    _TRUSTED_LEGACY_REQUIREMENT_SUBSECTION.finditer(
                        section.group("body")
                    )
                )
                if subsections:
                    bodies = tuple(
                        (
                            _TRUSTED_LEGACY_SUBSECTION_KIND[subsection.group("name")],
                            subsection.group("body"),
                        )
                        for subsection in subsections
                    )
            for expected_kind, body in bodies:
                for match in child_pattern.finditer(body):
                    if match.group("package") != package_number or (
                        not legacy_predecessor and match.group("kind") != expected_kind
                    ):
                        raise RegistryError(
                            f"trusted Requirement predecessor has a foreign child ID: {path}"
                        )
                    number = int(match.group("number"))
                    name = f"REQ-{package_number}.{expected_kind}"
                    declarations.setdefault(name, set()).add(number)

    states: dict[str, RequirementAllocationState] = {}
    expected_children = {
        f"REQ-{number:04d}.{kind}"
        for number in range(1, package_high_water + 1)
        for kind in ("FR", "NFR", "IF")
    }
    if set(map(str, children)) != expected_children:
        raise RegistryError(
            "trusted Requirement predecessor child allocation coverage is incomplete"
        )
    for name, value in children.items():
        if not isinstance(value, Mapping):
            raise RegistryError(f"trusted Requirement child space is invalid: {name}")
        high_water = value.get("high_water")
        next_number = value.get("next_number")
        if (
            type(high_water) is not int
            or type(next_number) is not int
            or not 0 <= high_water <= MAX_TRUSTED_CHILD_HIGH_WATER
            or next_number != high_water + 1
        ):
            raise RegistryError(f"trusted Requirement allocation is invalid: {name}")
        child_name = _TRUSTED_CHILD_SPACE_NAME.fullmatch(str(name))
        if child_name is None:
            raise RegistryError(f"trusted Requirement child space is invalid: {name}")
        if legacy_predecessor:
            high_water = max(
                high_water,
                max(declarations.get(str(name), {0})),
            )
            next_number = high_water + 1
        declared = tuple(sorted(declarations.get(str(name), set())))
        explicit_current = value.get("current_issued")
        explicit_reserved = value.get("reserved_history")
        has_explicit_history = isinstance(explicit_current, list) and isinstance(
            explicit_reserved, list
        )
        if has_explicit_history:
            if any(
                type(number) is not int
                for number in (*explicit_current, *explicit_reserved)
            ):
                raise RegistryError(f"trusted Requirement history is invalid: {name}")
            current = tuple(sorted(set(explicit_current)))
            reserved = tuple(sorted(set(explicit_reserved)))
            if (
                current != tuple(explicit_current)
                or reserved != tuple(explicit_reserved)
                or set(current) & set(reserved)
                or set(current) | set(reserved) != set(range(1, high_water + 1))
            ):
                raise RegistryError(f"trusted Requirement history is invalid: {name}")
            if actual_packages and current != declared:
                raise RegistryError(
                    f"trusted Requirement declarations disagree with allocation history: {name}"
                )
        elif explicit_current is not None or explicit_reserved is not None:
            raise RegistryError(f"trusted Requirement history is incomplete: {name}")
        elif actual_packages:
            current = declared
            current_set = set(current)
            reserved = tuple(
                number
                for number in range(1, high_water + 1)
                if number not in current_set
            )
        else:
            raise RegistryError(
                "trusted Requirement predecessor needs packages or durable history"
            )
        if any(number < 1 or number > high_water for number in current):
            raise RegistryError(
                f"trusted Requirement declaration exceeds high-water: {name}"
            )
        states[str(name)] = RequirementAllocationState(
            high_water=high_water,
            next_number=next_number,
            current_issued=current,
            reserved_history=reserved,
        )
    return RequirementAllocationBaseline(
        source=source,
        package_high_water=package_high_water,
        child_spaces=MappingProxyType(states),
    )


def _validate_requirement_allocation_transition(
    requirement: Mapping[str, object],
    baseline: RequirementAllocationBaseline | None,
    findings: list[RegistryFinding],
) -> None:
    if baseline is None:
        findings.append(
            RegistryFinding(
                "requirement-allocation-baseline-required",
                "identity_spaces.requirement",
                "allocation transition validation requires a trusted baseline predecessor",
            )
        )
        return
    children = requirement.get("child_spaces")
    if not isinstance(children, Mapping):
        return
    package_high_water = requirement.get("high_water")
    if (
        type(package_high_water) is int
        and package_high_water < baseline.package_high_water
    ):
        findings.append(
            RegistryFinding(
                "requirement-package-high-water-regressed",
                "identity_spaces.requirement.high_water",
                "Requirement package high-water cannot regress below its trusted predecessor",
            )
        )
    for name, prior in baseline.child_spaces.items():
        candidate = children.get(name)
        if not isinstance(candidate, Mapping):
            findings.append(
                RegistryFinding(
                    "requirement-allocation-history-missing",
                    f"identity_spaces.requirement.child_spaces.{name}",
                    "trusted allocation history cannot be removed",
                )
            )
            continue
        high_water = candidate.get("high_water")
        current = candidate.get("current_issued")
        reserved = candidate.get("reserved_history")
        if (
            type(high_water) is not int
            or not isinstance(current, list)
            or not isinstance(reserved, list)
            or any(type(number) is not int for number in (*current, *reserved))
        ):
            continue
        current_numbers = set(current)
        reserved_numbers = set(reserved)
        prior_current = set(prior.current_issued)
        prior_reserved = set(prior.reserved_history)
        if not prior_reserved <= reserved_numbers:
            findings.append(
                RegistryFinding(
                    "requirement-reserved-history-reclassified",
                    f"identity_spaces.requirement.child_spaces.{name}",
                    "trusted terminal reservations must remain reserved",
                )
            )
        if high_water < prior.high_water:
            findings.append(
                RegistryFinding(
                    "requirement-allocation-high-water-regressed",
                    f"identity_spaces.requirement.child_spaces.{name}",
                    "allocation high-water cannot regress below its trusted predecessor",
                )
            )
            continue
        new_current = current_numbers - prior_current
        expected_new = set(range(prior.high_water + 1, high_water + 1))
        if new_current - prior_reserved != expected_new:
            findings.append(
                RegistryFinding(
                    "requirement-allocation-transition-invalid",
                    f"identity_spaces.requirement.child_spaces.{name}",
                    "new current IDs must be the contiguous advance above trusted high-water",
                )
            )
        if not prior_current <= current_numbers | reserved_numbers:
            findings.append(
                RegistryFinding(
                    "requirement-allocation-history-lost",
                    f"identity_spaces.requirement.child_spaces.{name}",
                    "trusted current IDs may remain current or retire, but cannot disappear",
                )
            )


def validate_requirement_allocation_transition(
    registry: DocumentRegistry,
    baseline: RequirementAllocationBaseline | None,
) -> tuple[RegistryFinding, ...]:
    """Validate one loaded Registry against explicit trusted allocation history."""

    requirement = registry.identity_spaces.get("requirement")
    if requirement is None:
        return (
            RegistryFinding(
                "requirement-allocation-space-missing",
                "identity_spaces.requirement",
                "Requirement allocation space is missing",
            ),
        )
    raw = {
        "high_water": requirement.high_water,
        "child_spaces": {
            name: {
                "high_water": space.high_water,
                "next_number": space.next_number,
                "current_issued": list(space.current_issued),
                "reserved_history": list(space.reserved_history),
            }
            for name, space in requirement.child_spaces.items()
        },
    }
    findings: list[RegistryFinding] = []
    _validate_requirement_allocation_transition(raw, baseline, findings)
    return tuple(sorted(set(findings)))


_TOKEN_PATTERN = re.compile(
    r"\{(?:number|package_number|task_number|member_number|subject_number|year):4\}"
    r"|\{(?:slug|hook_slug|domain|stage|category|subpath)\}"
)
_ARTIFACT_TOKEN_PATTERN = re.compile(
    r"\{(?:number|package_number|task_number|member_number|subject_number|year):4\}"
    r"|\{retired_artifact_id\}"
)


# Registry authority reaches outside docs/ only for the repository entrypoint
# surfaces that carry a registered README form. Every other root stays out.
_NON_DOCS_ROOTS = (
    ".agents/",
    "examples/",
    "infra/",
    "projects/",
)
_NON_DOCS_FILES = frozenset(
    {
        ".github/INDEX.md",
        "README.md",
        "infra/README.md",
        "projects/README.md",
        "scripts/README.md",
        "secrets/README.md",
        "tests/README.md",
    }
)


def _registry_owned_root(value: str) -> bool:
    return (
        value.startswith("docs/")
        or value in _NON_DOCS_FILES
        or value.startswith(_NON_DOCS_ROOTS)
    )


def _safe_path_pattern(value: str) -> bool:
    path = pathlib.PurePosixPath(value)
    tokens = re.findall(r"\{[^{}]+\}", value)
    without_tokens = _TOKEN_PATTERN.sub("", value)
    return bool(
        _registry_owned_root(value)
        and not value.startswith("/")
        and "\\" not in value
        and all(character.isprintable() for character in value)
        and "//" not in value
        and ".." not in path.parts
        and all(part not in {"", "."} for part in path.parts)
        and path.as_posix() == value
        and all(_TOKEN_PATTERN.fullmatch(token) is not None for token in tokens)
        and "{" not in without_tokens
        and "}" not in without_tokens
    )


def _safe_artifact_pattern(value: str) -> bool:
    tokens = re.findall(r"\{[^{}]+\}", value)
    rendered = _ARTIFACT_TOKEN_PATTERN.sub("0000", value)
    return bool(
        tokens
        and all(
            _ARTIFACT_TOKEN_PATTERN.fullmatch(token) is not None for token in tokens
        )
        and re.fullmatch(r"[A-Za-z][A-Za-z0-9-]*", rendered) is not None
    )


def _safe_template_source(value: str) -> bool:
    path = pathlib.PurePosixPath(value)
    return bool(
        value.startswith("docs/99.templates/templates/")
        and not value.startswith("/")
        and "\\" not in value
        and ".." not in path.parts
        and path.as_posix() == value
        and value.endswith(
            (
                ".template.md",
                ".template.yaml",
                ".template.graphql",
                ".template.proto",
                ".template.toml",
            )
        )
    )


# Artifact patterns may also carry the inherited-identity token, which never
# appears in a path pattern.
_RENDER_TOKEN_PATTERN = re.compile(_TOKEN_PATTERN.pattern + r"|\{retired_artifact_id\}")


def _path_regex(pattern: str) -> re.Pattern[str]:
    cursor = 0
    rendered: list[str] = ["^"]
    for match in _RENDER_TOKEN_PATTERN.finditer(pattern):
        rendered.append(re.escape(pattern[cursor : match.start()]))
        token = match.group(0)
        if token == "{retired_artifact_id}":
            rendered.append(r"[A-Za-z][A-Za-z0-9]*-[0-9]{4}")
        elif token.endswith(":4}"):
            rendered.append(r"[0-9]{4}")
        elif token == "{hook_slug}":
            rendered.append(r"[a-z0-9][a-z0-9.-]*")
        elif token == "{slug}":
            rendered.append(r"[a-z0-9][a-z0-9-]*")
        elif token == "{stage}":
            rendered.append(
                r"(?:00\.agent-governance|01\.requirements|02\.architecture|03\.specs|05\.operations|90\.references|98\.archive|99\.templates)"
            )
        elif token == "{category}":
            rendered.append(r"(?:audits|data|research)")
        elif token == "{subpath}":
            # One or more lowercase path segments, so one profile can own a
            # nested entrypoint tree without a profile per depth.
            rendered.append(r"(?:[a-z0-9][a-z0-9-]*/)*[a-z0-9][a-z0-9-]*")
        else:
            rendered.append(r"[a-z0-9][a-z0-9-]*")
        cursor = match.end()
    rendered.append(re.escape(pattern[cursor:]))
    rendered.append("$")
    return re.compile("".join(rendered))


def path_matches_pattern(
    path: str | pathlib.PurePosixPath,
    pattern: object,
) -> bool:
    """Return whether one repository path matches a Registry path pattern."""

    if not isinstance(pattern, str):
        return False
    normalized = pathlib.PurePosixPath(path).as_posix()
    return _path_regex(pattern).fullmatch(normalized) is not None


def classify_path(
    path: str | pathlib.PurePosixPath,
    registry: DocumentRegistry | None = None,
) -> str | None:
    """Return the unique registered profile for one canonical path."""

    active = registry or load_registry()
    normalized = pathlib.PurePosixPath(path).as_posix()
    matches = [
        profile_id
        for profile_id, profile in active.profiles.items()
        if normalized in profile.get("additional_paths", ())
        or path_matches_pattern(normalized, profile.get("path_pattern"))
    ]
    specific = [item for item in matches if item not in FALLBACK_PROFILE_IDS]
    if len(specific) > 1:
        # Same rule the overlap validation already applies: a provider-owned
        # binding is a narrower runtime-owned surface inside a generic document
        # route, so it wins rather than leaving the path unclassified.
        owned = [
            item
            for item in specific
            if _declares_provider_binding(active.profiles[item])
        ]
        if len(owned) == 1:
            return owned[0]
    if specific:
        return specific[0] if len(specific) == 1 else None
    return matches[0] if len(matches) == 1 else None


def load_registry(
    path: pathlib.Path = DEFAULT_REGISTRY,
    *,
    trusted_requirement_baseline: RequirementAllocationBaseline | None = None,
    allow_requirement_allocation_transition: bool = False,
) -> DocumentRegistry:
    """Load, validate, and deeply freeze the sole Stage 99 machine authority."""

    raw = load_registry_document(path)
    findings = validate_registry(
        raw,
        trusted_requirement_baseline=trusted_requirement_baseline,
        allow_requirement_allocation_transition=allow_requirement_allocation_transition,
    )
    if findings:
        first = findings[0]
        raise RegistryError(f"{first.code} at {first.path}: {first.message}")
    profiles_raw = raw["profiles"]
    roles_raw = raw["template_roles"]
    lifecycles_raw = raw["lifecycles"]
    spaces_raw = raw["identity_spaces"]
    transition_map = raw["transitions"]
    indexes_raw = raw["indexes"]
    template_catalog = raw["template_catalog"]
    if not (
        isinstance(profiles_raw, list)
        and isinstance(roles_raw, Mapping)
        and isinstance(lifecycles_raw, Mapping)
        and isinstance(spaces_raw, Mapping)
        and isinstance(transition_map, Mapping)
        and isinstance(indexes_raw, Mapping)
        and isinstance(template_catalog, str)
    ):
        raise RegistryError("registry members have invalid shapes")
    profiles = MappingProxyType(
        {
            str(profile["profile_id"]): _freeze(profile)
            for profile in profiles_raw
            if isinstance(profile, Mapping)
        }
    )
    lifecycles = MappingProxyType(
        {
            str(name): tuple(str(item) for item in value["statuses"])
            for name, value in lifecycles_raw.items()
            if isinstance(value, Mapping) and isinstance(value.get("statuses"), list)
        }
    )
    lifecycle_transitions = {
        str(name): MappingProxyType(
            {
                str(source): tuple(str(target) for target in targets)
                for source, targets in value["transitions"].items()
                if isinstance(targets, list)
            }
        )
        for name, value in lifecycles_raw.items()
        if isinstance(value, Mapping) and isinstance(value.get("transitions"), Mapping)
    }
    transitions = MappingProxyType(
        {
            str(profile_id): lifecycle_transitions[str(lifecycle_id)]
            for profile_id, lifecycle_id in transition_map.items()
            if str(lifecycle_id) in lifecycle_transitions
        }
    )
    return DocumentRegistry(
        source=pathlib.PurePosixPath(path.relative_to(ROOT).as_posix())
        if path.is_absolute() and path.is_relative_to(ROOT)
        else pathlib.PurePosixPath(path.as_posix()),
        profiles=profiles,
        template_roles=_freeze(roles_raw),  # type: ignore[arg-type]
        lifecycles=lifecycles,
        identity_spaces=MappingProxyType(
            {
                str(name): _identity_space(value)
                for name, value in spaces_raw.items()
                if isinstance(value, Mapping)
            }
        ),
        transitions=transitions,
        indexes=MappingProxyType(
            {str(key): str(value) for key, value in indexes_raw.items()}
        ),
        template_catalog=template_catalog,
        common=_freeze(raw.get("common", {})),  # type: ignore[arg-type]
    )
