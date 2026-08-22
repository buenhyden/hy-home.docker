"""Immutable, fail-closed loader for the Stage 99 document registry."""

from __future__ import annotations

import dataclasses
import datetime as dt
import json
import os
import pathlib
import re
import stat
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
    child_spaces: Mapping[str, "IdentitySpace"]


@dataclasses.dataclass(frozen=True)
class DocumentRegistry:
    source: pathlib.PurePosixPath
    profiles: Mapping[str, Mapping[str, object]]
    template_roles: Mapping[str, Mapping[str, object]]
    lifecycles: Mapping[str, tuple[str, ...]]
    identity_spaces: Mapping[str, IdentitySpace]
    transitions: Mapping[str, Mapping[str, tuple[str, ...]]]


def _read_regular_file(path: pathlib.Path, maximum: int) -> bytes:
    try:
        metadata = path.lstat()
    except OSError as error:
        raise RegistryError(f"cannot stat registry input: {error}") from error
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode):
        raise RegistryError("registry input must be a regular non-symlink file")
    if metadata.st_size > maximum:
        raise RegistryError("registry input exceeds the byte limit")
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(path, flags)
        try:
            opened = os.fstat(descriptor)
            if not stat.S_ISREG(opened.st_mode):
                raise RegistryError("registry input changed to a non-regular file")
            data = os.read(descriptor, maximum + 1)
        finally:
            os.close(descriptor)
    except OSError as error:
        raise RegistryError(f"cannot read registry input: {error}") from error
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
    except (json.JSONDecodeError, RegistryError) as error:
        raise RegistryError(f"invalid registry JSON: {error}") from error
    _require_bounded_depth(raw)
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
        return MappingProxyType({str(key): _freeze(item) for key, item in value.items()})
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
        child_spaces=MappingProxyType(
            {
                str(name): _identity_space(child)
                for name, child in children.items()
                if isinstance(child, Mapping)
            }
        ),
    )


def validate_registry(raw: Mapping[str, object]) -> tuple[RegistryFinding, ...]:
    """Return deterministic schema and semantic findings for ``raw``."""

    findings: list[RegistryFinding] = []
    try:
        schema = _parse_json(DEFAULT_PROFILE_SCHEMA, MAX_SCHEMA_BYTES)
    except RegistryError as error:
        return (RegistryFinding("schema-unavailable", "$", str(error)),)
    if not isinstance(schema, Mapping):
        return (RegistryFinding("schema-invalid", "$", "profile schema is not a mapping"),)
    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError:
        return (
            RegistryFinding(
                "schema-invalid", "$", "profile schema is not valid Draft 2020-12"
            ),
        )
    validator = Draft202012Validator(schema)
    for error in sorted(validator.iter_errors(raw), key=lambda item: tuple(map(str, item.path))):
        location = ".".join(map(str, error.path)) or "$"
        findings.append(RegistryFinding("schema-invalid", location, error.message))
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
                            "retired-profile", f"profiles.{index}", "Release is not an active profile"
                        )
                    )
            path_pattern = profile.get("path_pattern")
            if isinstance(path_pattern, str) and not _safe_path_pattern(path_pattern):
                findings.append(
                    RegistryFinding("path-pattern-invalid", f"profiles.{index}", path_pattern)
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
            if _path_patterns_overlap(left_pattern, right_pattern):
                findings.append(
                    RegistryFinding(
                        "profile-path-overlap",
                        f"profiles.{left_index},profiles.{right_index}",
                        f"profiles {left_id} and {right_id} can own the same path",
                    )
                )
    known_profiles = set(profile_ids)
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
                    RegistryFinding("template-target-forbidden", f"template_roles.{role}", ",".join(sorted(extra)))
                )
            if definition.get("profile_id") not in known_profiles:
                findings.append(
                    RegistryFinding("template-profile-unknown", f"template_roles.{role}", str(definition.get("profile_id")))
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
    for source in sorted({item for item in role_sources if role_sources.count(item) > 1}):
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
                        "profile-template-unknown", f"profiles.{index}", str(template_id)
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
        if frontmatter_policy == "required":
            if (
                not isinstance(required_frontmatter, list)
                or "profile_id" not in required_frontmatter
                or isinstance(optional_frontmatter, list)
                and "profile_id" in optional_frontmatter
            ):
                findings.append(
                    RegistryFinding(
                        "profile-id-contract-invalid",
                        f"profiles.{index}",
                        "frontmatter-required profiles must require exact profile_id",
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
            identity_relation == "none" and artifact_pattern is None
        ) or (
            identity_relation == "direct"
            and "number" in path_tokens
            and "number" in artifact_tokens
        ) or (
            identity_relation == "package-member"
            and bool(
                {"package_number", "number"}
                & path_tokens
                & artifact_tokens
            )
        ) or (
            identity_relation == "subject-member"
            and "subject_number" in path_tokens
            and "number" in artifact_tokens
            and isinstance(traceability, Mapping)
            and traceability.get("membership_authority")
            == "operations-migration-manifest"
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
            source = definition.get("source") if isinstance(definition, Mapping) else None
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
                        RegistryFinding("lifecycle-incomplete", f"lifecycles.{lifecycle_id}", "every status requires one transition entry")
                    )
                for source, targets in transitions.items():
                    if isinstance(targets, list) and not set(targets) <= status_set:
                        findings.append(
                            RegistryFinding("transition-unregistered", f"lifecycles.{lifecycle_id}.{source}", "transition target is not a registered status")
                        )
    spaces = raw.get("identity_spaces")
    if isinstance(spaces, Mapping):
        _validate_identity_spaces(spaces, "identity_spaces", findings)
        requirement_space = spaces.get("requirement")
        if isinstance(requirement_space, Mapping):
            _validate_requirement_child_spaces(requirement_space, findings)
    transitions = raw.get("transitions")
    if isinstance(transitions, Mapping):
        for profile_id, lifecycle_id in transitions.items():
            if profile_id not in known_profiles:
                findings.append(RegistryFinding("transition-profile-unknown", "transitions", str(profile_id)))
            if not isinstance(lifecycles, Mapping) or lifecycle_id not in lifecycles:
                findings.append(RegistryFinding("transition-lifecycle-unknown", f"transitions.{profile_id}", str(lifecycle_id)))
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
    return tuple(sorted(set(findings)))


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
        if type(high_water) is int and type(next_number) is int and next_number <= high_water:
            findings.append(
                RegistryFinding("identity-not-monotonic", f"{location}.{name}", "next_number must exceed high_water")
            )
        children = value.get("child_spaces")
        if isinstance(children, Mapping):
            _validate_identity_spaces(children, f"{location}.{name}.child_spaces", findings)


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
        expected_packages = {f"REQ-{number:04d}" for number in range(1, high_water + 1)}
        for package_id in sorted(expected_packages - set(packages)):
            findings.append(
                RegistryFinding(
                    "requirement-package-space-missing",
                    "identity_spaces.requirement.child_spaces",
                    f"reserved package has no child allocation spaces: {package_id}",
                )
            )


_TOKEN_PATTERN = re.compile(
    r"\{(?:number|package_number|task_number|subject_number|year):4\}"
    r"|\{(?:slug|hook_slug|domain|stage)\}"
)
_ARTIFACT_TOKEN_PATTERN = re.compile(
    r"\{(?:number|package_number|task_number|subject_number|year):4\}"
)


def _safe_path_pattern(value: str) -> bool:
    path = pathlib.PurePosixPath(value)
    tokens = re.findall(r"\{[^{}]+\}", value)
    without_tokens = _TOKEN_PATTERN.sub("", value)
    return bool(
        (value.startswith("docs/") or value == ".github/INDEX.md")
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
        and all(_ARTIFACT_TOKEN_PATTERN.fullmatch(token) is not None for token in tokens)
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
        and value.endswith((".template.md", ".template.yaml", ".template.graphql", ".template.proto"))
    )


def _path_regex(pattern: str) -> re.Pattern[str]:
    cursor = 0
    rendered: list[str] = ["^"]
    for match in _TOKEN_PATTERN.finditer(pattern):
        rendered.append(re.escape(pattern[cursor : match.start()]))
        token = match.group(0)
        if token.endswith(":4}"):
            rendered.append(r"[0-9]{4}")
        elif token == "{hook_slug}":
            rendered.append(r"[a-z0-9][a-z0-9.-]*")
        elif token == "{slug}":
            rendered.append(r"[a-z0-9][a-z0-9-]*")
        elif token == "{stage}":
            rendered.append(r"(?:00\.agent-governance|01\.requirements|02\.architecture|03\.specs|05\.operations|90\.references|98\.archive|99\.templates)")
        else:
            rendered.append(r"[a-z0-9][a-z0-9-]*")
        cursor = match.end()
    rendered.append(re.escape(pattern[cursor:]))
    rendered.append("$")
    return re.compile("".join(rendered))


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
        if isinstance(profile.get("path_pattern"), str)
        and _path_regex(str(profile["path_pattern"])).fullmatch(normalized)
    ]
    specific = [item for item in matches if item not in FALLBACK_PROFILE_IDS]
    if specific:
        return specific[0] if len(specific) == 1 else None
    return matches[0] if len(matches) == 1 else None


def load_registry(path: pathlib.Path = DEFAULT_REGISTRY) -> DocumentRegistry:
    """Load, validate, and deeply freeze the sole Stage 99 machine authority."""

    candidate = path.resolve(strict=False) if not path.is_symlink() else path
    raw = _parse_json(candidate, MAX_REGISTRY_BYTES)
    if not isinstance(raw, Mapping):
        raise RegistryError("registry document must be a mapping")
    findings = validate_registry(raw)
    if findings:
        first = findings[0]
        raise RegistryError(f"{first.code} at {first.path}: {first.message}")
    profiles_raw = raw["profiles"]
    roles_raw = raw["template_roles"]
    lifecycles_raw = raw["lifecycles"]
    spaces_raw = raw["identity_spaces"]
    transition_map = raw["transitions"]
    if not (
        isinstance(profiles_raw, list)
        and isinstance(roles_raw, Mapping)
        and isinstance(lifecycles_raw, Mapping)
        and isinstance(spaces_raw, Mapping)
        and isinstance(transition_map, Mapping)
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
    )
