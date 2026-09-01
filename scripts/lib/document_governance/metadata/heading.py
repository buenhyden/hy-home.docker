"""Markdown heading, template-body, and credential validation."""

from __future__ import annotations

import collections
import hashlib
import pathlib
import re
from collections.abc import Mapping

from scripts.lib.document_governance.frontmatter import (
    parse_frontmatter_text as _parse_frontmatter_text,
    safe_load_unique as _safe_load_unique,
)
from scripts.lib.document_governance.registry import (
    DocumentRegistry,
    classify_path as classify_registered_path,
)
from scripts.lib.document_governance.metadata.profile import (
    CREDENTIAL_KEY_NAME,
    MACHINE_EXAMPLE_VALUE,
    MACHINE_TEMPLATE_SUFFIXES,
    MACHINE_TEMPLATE_TOKEN,
    MARKDOWN_BODY_TOKEN,
    OPENAPI_AUTH_SCHEMES,
    OPENAPI_BEARER_VALUE,
    OPENAPI_CONCRETE_HOST,
    OPENAPI_CREDENTIAL_VALUE_KEYS,
    OPENAPI_JWT_VALUE,
    TARGET_TEMPLATE_LITERALS,
    Finding,
    MachineTemplateParseError,
    OpenApiInspection,
    ProfileError,
    Record,
    _finding,
    _profile_mapping,
    _string_list,
    _template_placeholder_values,
    _typed_target_types,
    classify_readme_profile,
    matching_template_roles,
    registered_generated_owner,
)

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
    if target_type == "readme":
        expected = {
            "profile_id": "readme",
            "status": "draft",
            "artifact_type": "readme",
        }
        return (
            []
            if record.metadata == expected
            else [
                _finding(
                    record,
                    "invalid-template-metadata",
                    "README source metadata must match the registered README template envelope",
                )
            ]
        )
    _, profile_map = _profile_mapping(profiles)
    target_profile = profile_map.get(target_type)
    if target_type == "archive":
        archive_profiles = profiles.get("archive_profiles", {})
        selected_archive_profile = (
            archive_profiles.get(role_name) if isinstance(archive_profiles, dict) else None
        )
        if isinstance(selected_archive_profile, dict):
            target_profile = selected_archive_profile
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
    parents = _string_list(record.metadata.get("parent_ids"))
    parent_placeholder = placeholders.get("parent_id")
    if "parent_ids" in forbidden and "parent_ids" not in record.metadata:
        pass
    elif parents is None:
        findings.append(_finding(record, "invalid-template-placeholder", "parent_ids must be a placeholder list"))
    elif not parents and not target_profile.get("allow_empty_parents", False):
        findings.append(_finding(record, "missing-parent", f"{target_type} template requires a direct parent placeholder"))
    elif any(parent != parent_placeholder for parent in parents):
        findings.append(_finding(record, "invalid-template-placeholder", "parent_ids contains a noncanonical placeholder"))
    for key in record.metadata:
        if key == "parent_ids":
            continue
        placeholder = placeholders.get(key)
        if placeholder is None:
            continue
        if record.metadata.get(key) != placeholder:
            findings.append(_finding(record, "invalid-template-placeholder", f"{key} must use the Stage 99 placeholder"))
    return sorted(set(findings))


def _markdown_unfenced_lines(text: str) -> list[str]:
    """Return Markdown lines outside backtick and tilde fenced blocks."""

    lines: list[str] = []
    fence_character: str | None = None
    fence_length = 0
    for line in text.splitlines():
        if fence_character is None:
            opening = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
            if opening:
                marker = opening.group(1)
                info_string = opening.group(2)
                if marker[0] == "`" and "`" in info_string:
                    lines.append(line)
                    continue
                fence_character = marker[0]
                fence_length = len(marker)
                continue
            lines.append(line)
            continue
        if re.match(
            rf"^ {{0,3}}{re.escape(fence_character)}{{{fence_length},}}[ \t]*$",
            line,
        ):
            fence_character = None
            fence_length = 0
    return lines


def _strip_inline_code_spans(text: str) -> str:
    """Remove CommonMark code spans closed by an equal backtick run."""

    rendered: list[str] = []
    index = 0
    while index < len(text):
        if text[index] != "`":
            rendered.append(text[index])
            index += 1
            continue
        opening_end = index
        while opening_end < len(text) and text[opening_end] == "`":
            opening_end += 1
        delimiter_length = opening_end - index
        cursor = opening_end
        closing_end: int | None = None
        while cursor < len(text):
            candidate = text.find("`", cursor)
            if candidate < 0:
                break
            run_end = candidate
            while run_end < len(text) and text[run_end] == "`":
                run_end += 1
            if run_end - candidate == delimiter_length:
                closing_end = run_end
                break
            cursor = run_end
        if closing_end is None:
            rendered.append(text[index:opening_end])
            index = opening_end
            continue
        rendered.append(" ")
        index = closing_end
    return "".join(rendered)


def extract_markdown_headings(text: str) -> tuple[list[str], list[str]]:
    """Return canonical H1 and H2 headings outside fenced code blocks."""

    h1: list[str] = []
    h2: list[str] = []
    for line in _markdown_unfenced_lines(text):
        match = re.match(r"^ {0,3}(#{1,2})[ \t]+(.+?)[ \t]*#*[ \t]*$", line)
        if not match:
            continue
        heading = f"{match.group(1)} {match.group(2).rstrip()}"
        (h1 if len(match.group(1)) == 1 else h2).append(heading)
    return h1, h2


def _body_target_scan_text(text: str) -> str:
    return _strip_inline_code_spans("\n".join(_markdown_unfenced_lines(text)))


def _machine_template_path(path: pathlib.Path) -> bool:
    normalized = path.as_posix()
    return normalized.startswith("docs/99.templates/templates/") and normalized.endswith(
        MACHINE_TEMPLATE_SUFFIXES
    )


def _normalized_credential_key(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    normalized = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", value)
    normalized = re.sub(r"[^A-Za-z0-9]+", "_", normalized).strip("_").lower()
    return normalized if CREDENTIAL_KEY_NAME.search(normalized) else None


def _approved_machine_token(value: object) -> bool:
    if not isinstance(value, str):
        return False
    candidate = value.strip()
    if len(candidate) >= 2 and candidate[0] == candidate[-1] and candidate[0] in {'"', "'"}:
        candidate = candidate[1:-1]
    return MACHINE_TEMPLATE_TOKEN.fullmatch(candidate) is not None


def _openapi_mapping(text: str) -> dict[object, object]:
    try:
        document = _safe_load_unique(text)
    except Exception:
        raise MachineTemplateParseError from None
    if not isinstance(document, dict):
        raise MachineTemplateParseError
    return document


def _approved_machine_values(value: object) -> bool:
    if isinstance(value, dict):
        return all(_approved_machine_values(member) for member in value.values())
    if isinstance(value, list):
        return all(_approved_machine_values(member) for member in value)
    return _approved_machine_token(value)


def _openapi_string_has_concrete_format_value(
    key: object,
    value: object,
    *,
    security_scheme_context: bool,
) -> bool:
    if not isinstance(value, str) or _approved_machine_token(value):
        return False
    if (
        OPENAPI_CONCRETE_HOST.search(value)
        or OPENAPI_BEARER_VALUE.search(value)
        or OPENAPI_JWT_VALUE.search(value)
    ):
        return True
    normalized_key = re.sub(r"[^A-Za-z0-9]+", "_", str(key)).strip("_").lower()
    normalized_value = value.strip().lower()
    if normalized_key in {"scheme", "auth", "authentication", "authorization"}:
        return normalized_value in OPENAPI_AUTH_SCHEMES
    return (
        security_scheme_context
        and normalized_key == "type"
        and normalized_value in OPENAPI_AUTH_SCHEMES
    )


def _inspect_openapi(text: str) -> OpenApiInspection:
    document = _openapi_mapping(text)
    concrete_credential = False
    concrete_format = False

    def inspect(
        value: object,
        *,
        security_scheme_context: bool = False,
        credential_context: bool = False,
    ) -> None:
        nonlocal concrete_credential, concrete_format
        if isinstance(value, dict):
            for key, member in value.items():
                normalized_key = re.sub(r"[^A-Za-z0-9]+", "_", str(key)).strip("_").lower()
                nested_security_context = security_scheme_context or normalized_key in {
                    "securityscheme",
                    "securityschemes",
                    "security_scheme",
                    "security_schemes",
                }
                credential_key = _normalized_credential_key(key) is not None
                nested_credential_context = credential_context or credential_key
                credential_value_annotation = (
                    credential_context
                    and normalized_key in OPENAPI_CREDENTIAL_VALUE_KEYS
                )
                if credential_value_annotation and not _approved_machine_values(member):
                    concrete_credential = True
                elif credential_key and not isinstance(member, dict):
                    if not _approved_machine_values(member):
                        concrete_credential = True

                if isinstance(member, list):
                    for item in member:
                        if _openapi_string_has_concrete_format_value(
                            key,
                            item,
                            security_scheme_context=nested_security_context,
                        ):
                            concrete_format = True
                        inspect(
                            item,
                            security_scheme_context=nested_security_context,
                            credential_context=nested_credential_context,
                        )
                else:
                    if _openapi_string_has_concrete_format_value(
                        key,
                        member,
                        security_scheme_context=nested_security_context,
                    ):
                        concrete_format = True
                    inspect(
                        member,
                        security_scheme_context=nested_security_context,
                        credential_context=nested_credential_context,
                    )
        elif isinstance(value, list):
            for member in value:
                inspect(
                    member,
                    security_scheme_context=security_scheme_context,
                    credential_context=credential_context,
                )

    inspect(document)
    return OpenApiInspection(concrete_credential, concrete_format)


GRAPHQL_VALUE = r'(?:"(?:\\.|[^"\\])*"|-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?|true|false|null|[A-Za-z_][A-Za-z0-9_]*)'


def _graphql_concrete_credential(text: str) -> bool:
    without_block_strings = re.sub(r'""".*?"""', "", text, flags=re.DOTALL)
    for raw_line in without_block_strings.splitlines():
        line = raw_line.split("#", 1)[0]
        if not line.strip():
            continue
        for name in re.findall(r"\b[A-Za-z_][A-Za-z0-9_]*\b", line):
            if _normalized_credential_key(name) is None:
                continue
            escaped = re.escape(name)
            default_match = re.search(
                rf"\b{escaped}\b\s*:\s*[A-Za-z_][A-Za-z0-9_]*(?:\s*[!\[\]])*\s*=\s*({GRAPHQL_VALUE})",
                line,
                flags=re.IGNORECASE,
            )
            if default_match and not _approved_machine_token(default_match.group(1)):
                return True
            literal_match = re.search(
                rf"\b{escaped}\b\s*:\s*(\"(?:\\.|[^\"\\])*\"|-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?|true|false|null)",
                line,
                flags=re.IGNORECASE,
            )
            if literal_match and not _approved_machine_token(literal_match.group(1)):
                return True
    return False


PROTO_VALUE = r'(?:"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[A-Za-z_][A-Za-z0-9_]*|-?[0-9]+)'


def _protobuf_concrete_credential(text: str) -> bool:
    without_blocks = re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)
    for raw_line in without_blocks.splitlines():
        line = raw_line.split("//", 1)[0]
        if not line.strip():
            continue
        for name in re.findall(r"\b[A-Za-z_][A-Za-z0-9_]*\b", line):
            if _normalized_credential_key(name) is None:
                continue
            if re.search(
                rf"\b{re.escape(name)}\b[^;\n]*\[\s*default\s*=\s*({PROTO_VALUE})",
                line,
                flags=re.IGNORECASE,
            ):
                default_value = re.search(
                    r"\[\s*default\s*=\s*(" + PROTO_VALUE + r")",
                    line,
                    flags=re.IGNORECASE,
                )
                if default_value and not _approved_machine_token(default_value.group(1)):
                    return True
            assignment = re.search(
                rf"(?:\b{re.escape(name)}\b|\({re.escape(name)}\))\s*=\s*({PROTO_VALUE})",
                line,
                flags=re.IGNORECASE,
            )
            if assignment:
                value = assignment.group(1)
                if re.fullmatch(r"[0-9]+", value):
                    continue
                if not _approved_machine_token(value):
                    return True
    return False


def _machine_concrete_credential(path: pathlib.Path, text: str) -> bool:
    suffix = path.as_posix()
    if suffix.endswith(".template.graphql"):
        return _graphql_concrete_credential(text)
    if suffix.endswith(".template.proto"):
        return _protobuf_concrete_credential(text)
    return False


def _machine_template_findings(record: Record, text: str) -> list[Finding]:
    findings: list[Finding] = []
    if MACHINE_TEMPLATE_TOKEN.search(text) is None:
        findings.append(
            _finding(
                record,
                "machine-template-token-missing",
                "machine template must contain an explicit uppercase unresolved token",
            )
        )
    suffix = record.path.as_posix()
    if suffix.endswith((".template.yaml", ".template.yml")):
        try:
            inspection = _inspect_openapi(text)
        except MachineTemplateParseError:
            findings.append(
                _finding(
                    record,
                    "machine-template-parse-error",
                    "machine template could not be parsed as a safe OpenAPI mapping",
                )
            )
            return sorted(set(findings))
        concrete_value = (
            inspection.concrete_credential_value or inspection.concrete_format_value
        )
    else:
        concrete_value = MACHINE_EXAMPLE_VALUE.search(text) is not None or _machine_concrete_credential(
            record.path,
            text,
        )
    if concrete_value:
        findings.append(
            _finding(
                record,
                "machine-template-example-value",
                "machine template contains a concrete example host, auth value, or credential-like value",
            )
        )
    return sorted(set(findings))


def _source_roles_for_path(
    path: pathlib.Path,
    profiles: dict[str, object],
) -> list[tuple[str, dict[str, object]]]:
    roles = profiles.get("template_roles", {})
    if not isinstance(roles, dict):
        return []
    return sorted(
        (
            (name, role)
            for name, role in roles.items()
            if isinstance(name, str)
            and isinstance(role, dict)
            and role.get("source") == path.as_posix()
        ),
        key=lambda item: item[0],
    )


def validate_body_contract(
    record: Record,
    text: str,
    profiles: dict[str, object],
    changed_boundary: bool,
) -> list[Finding]:
    """Validate role headings, source tokens, and changed-target residue."""

    if _machine_template_path(record.path):
        return _machine_template_findings(record, text)

    registry = profiles.get("_registry")
    if isinstance(registry, DocumentRegistry):
        owner = registered_generated_owner(record.path, profiles)
        if owner is not None and record.metadata.get("generated_by") == owner:
            # Its declared producer checks the generated body; metadata and
            # References still validate identity, membership, and current links.
            return []
        registered_profile = classify_registered_path(record.path.as_posix(), registry)
        profile = registry.profiles.get(record.artifact_type)
        if (
            registered_profile == record.artifact_type
            and isinstance(profile, Mapping)
            and profile.get("template_id") is None
        ):
            findings: list[Finding] = []
            h1, h2 = extract_markdown_headings(text)
            if len(h1) != 1:
                findings.append(
                    _finding(
                        record,
                        "body-h1-count",
                        f"profile {record.artifact_type} requires exactly one H1; found {len(h1)}",
                    )
                )
            required = {
                f"## {heading}"
                for heading in profile.get("required_sections", ())
                if isinstance(heading, str)
            }
            optional = {
                f"## {heading}"
                for heading in profile.get("optional_sections", ())
                if isinstance(heading, str)
            }
            for heading in sorted(required - set(h2)):
                findings.append(
                    _finding(
                        record,
                        "body-heading-missing",
                        f"profile {record.artifact_type} is missing required heading: {heading}",
                    )
                )
            # A profile whose documents share no heading vocabulary declares
            # itself free-form rather than registering a union nothing follows.
            # Without this, an unregistered heading is a violation only when a
            # change introduces it, so the profile passes its own corpus and
            # rejects every edit to it.
            if not profile.get("free_form_sections"):
                for heading in sorted(set(h2) - required - optional):
                    findings.append(
                        _finding(
                            record,
                            "body-heading-forbidden",
                            f"profile {record.artifact_type} contains unregistered heading: {heading}",
                        )
                    )
            return sorted(set(findings))

    source_roles = _source_roles_for_path(record.path, profiles)
    is_markdown_source = (
        record.path.as_posix().startswith("docs/99.templates/templates/")
        and record.path.name.endswith(".template.md")
    )
    role_name: str | None = None
    role: dict[str, object] | None = None
    findings: list[Finding] = []
    if source_roles:
        if len(source_roles) > 1:
            findings.append(
                _finding(
                    record,
                    "template-role-ambiguous",
                    "template source resolves to multiple roles: "
                    + ", ".join(name for name, _ in source_roles),
                )
            )
            return findings
        role_name, role = source_roles[0]
    elif is_markdown_source:
        findings.append(
            _finding(
                record,
                "template-role-missing",
                "Markdown template source has no registered role",
            )
        )
        return findings
    elif record.artifact_type == "readme":
        if not changed_boundary:
            return []
        try:
            readme_profile_name = classify_readme_profile(record.path, profiles)
        except ProfileError:
            return []
        if readme_profile_name != "template-catalog":
            return []
        readme_profiles = profiles.get("readme_profiles", {})
        readme_profile = (
            readme_profiles.get(readme_profile_name, {})
            if isinstance(readme_profiles, dict)
            else {}
        )
        _, h2 = extract_markdown_headings(text)
        required = readme_profile.get("required_headings", []) if isinstance(readme_profile, dict) else []
        for heading in required:
            canonical = f"## {heading}"
            if canonical not in h2:
                findings.append(
                    _finding(
                        record,
                        "readme-heading-missing",
                        f"template-catalog README is missing required heading: {canonical}",
                    )
                )
        forbidden = readme_profile.get("forbidden_headings", []) if isinstance(readme_profile, dict) else []
        for heading in forbidden:
            canonical = f"## {heading}"
            if canonical in h2:
                findings.append(
                    _finding(
                        record,
                        "readme-heading-forbidden",
                        f"template-catalog README contains forbidden heading: {canonical}",
                    )
                )
        return sorted(set(findings))
    elif changed_boundary and record.artifact_type in _typed_target_types(profiles):
        matches = matching_template_roles(record.path, record.artifact_type, profiles)
        if not matches:
            findings.append(
                _finding(
                    record,
                    "template-role-missing",
                    f"changed target has no role for profile {record.artifact_type}",
                )
            )
            return findings
        if len(matches) > 1:
            findings.append(
                _finding(
                    record,
                    "template-role-ambiguous",
                    f"changed target resolves to multiple roles: {', '.join(matches)}",
                )
            )
            return findings
        role_name = matches[0]
        roles = profiles.get("template_roles", {})
        candidate = roles.get(role_name, {}) if isinstance(roles, dict) else {}
        role = candidate if isinstance(candidate, dict) else None
    else:
        return []

    if role is None or role_name is None:
        return findings
    h1, h2 = extract_markdown_headings(text)
    if len(h1) != 1:
        findings.append(
            _finding(
                record,
                "body-h1-count",
                f"role {role_name} requires exactly one H1; found {len(h1)}",
            )
        )
    required_headings = role.get("required_headings", [])
    forbidden_headings = role.get("forbidden_headings", [])
    for heading in required_headings if isinstance(required_headings, list) else []:
        if heading not in h2:
            findings.append(
                _finding(
                    record,
                    "body-heading-missing",
                    f"role {role_name} is missing required heading: {heading}",
                )
            )
    for heading in forbidden_headings if isinstance(forbidden_headings, list) else []:
        if heading in h2:
            findings.append(
                _finding(
                    record,
                    "body-heading-forbidden",
                    f"role {role_name} contains forbidden heading: {heading}",
                )
            )

    unfenced_text = "\n".join(_markdown_unfenced_lines(text))
    if source_roles or (
        isinstance(registry, DocumentRegistry)
        and record.artifact_type == "plan"
        and classify_registered_path(record.path.as_posix(), registry) == record.artifact_type
    ):
        conditional = role.get("conditional_headings", [])
        allowed_headings = set(required_headings if isinstance(required_headings, list) else []) | set(
            conditional if isinstance(conditional, list) else []
        )
        for heading in sorted(set(h2) - allowed_headings):
            findings.append(
                _finding(
                    record,
                    "body-heading-forbidden",
                    f"role {role_name} source contains unregistered heading: {heading}",
                )
                )
    if source_roles:
        for literal in TARGET_TEMPLATE_LITERALS:
            if literal in unfenced_text:
                findings.append(
                    _finding(
                        record,
                        "template-instruction-in-source",
                        "template source contains a prohibited instruction literal",
                    )
                )
        if MARKDOWN_BODY_TOKEN.search(unfenced_text) is None:
            findings.append(
                _finding(
                    record,
                    "template-body-token-missing",
                    f"role {role_name} source requires an explicit Markdown body token",
                )
            )
    elif changed_boundary:
        target_scan_text = _body_target_scan_text(text)
        for literal in TARGET_TEMPLATE_LITERALS:
            if literal in target_scan_text:
                findings.append(
                    _finding(
                        record,
                        "template-instruction-in-target",
                        "changed target retains a template-only instruction literal",
                    )
                )
        if MARKDOWN_BODY_TOKEN.search(target_scan_text):
            findings.append(
                _finding(
                    record,
                    "template-body-token-in-target",
                    "changed target retains an unresolved Markdown body token",
                )
            )
    return sorted(set(findings))


BodyDeficitKey = tuple[str, str, str, str]


def _private_deficit_identity(code: str, value: str) -> str:
    """Return a deterministic internal identity that is never rendered."""

    return hashlib.sha256(f"{code}\0{value}".encode("utf-8")).hexdigest()


def _body_deficit_multiset(
    record: Record,
    text: str,
    profiles: dict[str, object],
    *,
    changed_boundary: bool,
) -> collections.Counter[BodyDeficitKey]:
    """Return exact non-rendered body deficit identities with multiplicity."""

    findings = validate_body_contract(record, text, profiles, changed_boundary)
    occurrence_codes = {
        "template-instruction-in-source",
        "template-instruction-in-target",
        "template-body-token-in-target",
    }
    deficits: collections.Counter[BodyDeficitKey] = collections.Counter()
    for finding in findings:
        if finding.code in occurrence_codes:
            continue
        identity = _private_deficit_identity(finding.code, finding.message)
        deficits[(finding.code, identity, "body contract deficit", finding.severity)] += 1

    source_roles = _source_roles_for_path(record.path, profiles)
    if source_roles:
        scan_text = "\n".join(_markdown_unfenced_lines(text))
        instruction_code = "template-instruction-in-source"
    elif changed_boundary:
        scan_text = _body_target_scan_text(text)
        instruction_code = "template-instruction-in-target"
    else:
        return deficits

    for literal in TARGET_TEMPLATE_LITERALS:
        identity = _private_deficit_identity(instruction_code, literal)
        count = len(tuple(re.finditer(re.escape(literal), scan_text)))
        if count:
            deficits[(instruction_code, identity, "template instruction", "error")] += count
    if not source_roles and changed_boundary:
        for match in MARKDOWN_BODY_TOKEN.finditer(scan_text):
            identity = _private_deficit_identity(
                "template-body-token-in-target",
                match.group(0),
            )
            deficits[
                (
                    "template-body-token-in-target",
                    identity,
                    "Markdown body token",
                    "error",
                )
            ] += 1
    return deficits


def _introduced_body_findings(
    record: Record,
    current_text: str,
    base_record: Record | None,
    base_text: str | None,
    profiles: dict[str, object],
) -> list[Finding]:
    current = _body_deficit_multiset(
        record,
        current_text,
        profiles,
        changed_boundary=True,
    )
    base = (
        _body_deficit_multiset(
            base_record,
            base_text,
            profiles,
            changed_boundary=True,
        )
        if base_record is not None and base_text is not None
        else collections.Counter()
    )
    introduced = current - base
    safe_counts: collections.Counter[tuple[str, str, str]] = collections.Counter()
    for (code, _identity, safe_label, severity), count in introduced.items():
        safe_counts[(code, safe_label, severity)] += count
    return [
        _finding(
            record,
            code,
            f"changed body introduces {safe_label} deficit(s); count={count}",
            severity,
        )
        for (code, safe_label, severity), count in sorted(safe_counts.items())
    ]


def _native_migration_compaction_witness(
    root: pathlib.Path, record: Record, base_ref: str | None,
) -> Record | None:
    """Bind the frozen historical ledger to its verified native compact state."""

    if (
        not base_ref
        or record.path.as_posix() != "docs/98.archive/migrations/0003-workspace-governance-simplification.md"
        or record.previous_status != "archived"
        or record.artifact_type != "migration"
        or record.metadata.get("artifact_type") != "migration"
        or record.metadata.get("artifact_id") != "mig-0003"
        or record.metadata.get("profile_id") != "migration"
        or record.metadata.get("status") != "completed"
    ):
        return None
    from scripts.lib.document_governance import archive

    try:
        previous = archive.HistoricalDocument(root, base_ref, record.path.as_posix()).read_bytes()
        if hashlib.sha256(previous).hexdigest() != archive.FROZEN_MIGRATION_SHA256:
            return None
        if archive._migration_document(root)["schema_version"] != 3:
            return None
        current = archive._read_regular(root / record.path).decode("utf-8")
        if _parse_frontmatter_text(current) != record.metadata:
            return None
    except ValueError:
        return None
    return record
