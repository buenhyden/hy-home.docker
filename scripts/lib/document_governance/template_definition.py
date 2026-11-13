"""Project Registry template roles onto the approved TemplateDefinition v14.5.

A `template_roles` entry holds only the authored fields the Registry has no
other source for. Everything else is derived here from the bound profile, the
template file and the shared `common` dictionaries, so no fact is held twice.
The record shape is `docs/99.templates/contracts/template-definition.schema.json`.
"""

from __future__ import annotations

import functools
import json
import pathlib
import re
import tomllib
from collections.abc import Mapping, Sequence

from scripts.lib.document_governance.metadata.heading import (
    _HEADING_LINE,
    _markdown_unfenced_lines,
)
from scripts.lib.document_governance.registry import (
    MAX_SCHEMA_BYTES,
    ROOT,
    TEMPLATE_DEFINITION_FIELDS,
    DocumentRegistry,
    RegistryError,
    _parse_json,
)

# The documentation protocol: a role has moved to the common form when its
# profile declares `required_subsections`; every other role keeps the
# Registry `common.contract_id`. docs/99.templates/README.md states this rule.
COMMON_FORM_VERSION = "COMMON-DOC-FORM-1 1.0.0"

# COMMON-DOC-FORM-1 gives an H2 one empty rule and an H3 none; heading.py
# enforces it at every level, treating an HTML comment as no content.
_EMPTY_SECTION_RULE = (
    "A heading with no body, or a body that is only an unexplained "
    "TODO, TBD, N/A, - or a template guidance comment."
)
_STAND_IN_RULE = (
    "A same-named heading inside a code fence, quote or comment "
    "standing in for the real section."
)
# Registry `common` table contracts: (columns key, optional columns key,
# minimum rows). spec_packages rejects an empty registered table; a README
# Documents table is checked only when present.
_TABLE_CONTRACTS = (
    ("evidence_columns", None, 1),
    ("plan_columns", None, 1),
    ("criterion_acceptance_columns", None, 1),
    ("readme_documents_columns", "readme_documents_optional_columns", 0),
)
_PLACEHOLDER = re.compile(r"\{\{([A-Z][A-Z0-9_]*)\}\}")
_AUTHOR_PROMPT = re.compile(r"^<!--\s*Author prompt:\s*(.*?)\s*-->$")
# Top-level units of a template that has no registered Markdown section.
_STRUCTURAL_UNIT = {
    ".toml": re.compile(r"^(\[[^\]]+\]|[A-Za-z_][\w-]*)\s*="),
    ".yaml": re.compile(r"^([A-Za-z_][\w-]*):"),
    ".graphql": re.compile(
        r"^(?:schema|type|input|enum|interface|union|scalar|directive)\b"
    ),
    ".proto": re.compile(r"^(?:syntax|package|import|option|service|message|enum)\b"),
}
_FRONTMATTER_KEY = re.compile(r"^([A-Za-z_][\w-]*):")
PLACEHOLDER_CHECK = (
    "tests.lib.document_governance.test_registry:DocumentRegistryTests"
    ".test_registered_templates_use_one_placeholder_grammar"
)
UNITS_CHECK = (
    "tests.lib.document_governance.test_template_definition:TemplateDefinitionTests"
    ".test_headingless_templates_use_their_real_top_level_units"
)


def _plain(value: object) -> object:
    if isinstance(value, Mapping):
        return {str(key): _plain(item) for key, item in value.items()}
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        return [_plain(item) for item in value]
    return value


def _slug(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


def _words(token: str) -> str:
    return token.lower().replace("_", " ")


def _guidance_line(line: str) -> str:
    """One template body line as an instruction in words, never a bare token."""

    prompt = _AUTHOR_PROMPT.match(line)
    if prompt:
        return prompt.group(1)
    bare = re.fullmatch(r"[-*]?\s*\{\{([A-Z][A-Z0-9_]*)\}\}", line)
    if bare:
        return f"Write the {_words(bare.group(1))}."
    return _PLACEHOLDER.sub(lambda match: _words(match.group(1)), line)


def _template_outline(
    text: str,
) -> tuple[dict[tuple[str, str | None], str], list[tuple[str, str | None, str]]]:
    """Return each H2/H3's guidance and every pipe-table header row.

    An author prompt above the first H2 joins every section whose title it
    names; a prompt there that names no section is document-wide.
    """

    bodies: dict[tuple[str, str | None], list[str]] = {}
    preamble: list[str] = []
    headers: list[tuple[str, str | None, str]] = []
    h2: str | None = None
    h3: str | None = None
    previous = ""
    for raw in _markdown_unfenced_lines(text):
        line = raw.strip()
        match = _HEADING_LINE.match(raw)
        if match and len(match.group(1)) in (2, 3):
            if len(match.group(1)) == 2:
                h2, h3 = match.group(2), None
            elif h2 is not None:
                h3 = match.group(2)
            bodies.setdefault((h2, h3), [])  # type: ignore[arg-type]
            previous = ""
            continue
        if not line:
            continue
        if h2 is None:
            prompt = _AUTHOR_PROMPT.match(line)
            if prompt:
                preamble.append(prompt.group(1))
            continue
        if line.startswith("|"):
            if not previous.startswith("|"):
                headers.append((h2, h3, line))
        elif not line.startswith("#"):
            bodies[(h2, h3)].append(_guidance_line(line))
        previous = line
    guidance = {}
    for (parent, child), lines in bodies.items():
        title = child or parent
        named = [
            prompt
            for prompt in preamble
            # Code spans quote column names and commands, not section names.
            if re.search(
                rf"(?<![\w-]){re.escape(title)}(?![\w-])",
                re.sub(r"`[^`]*`", "", prompt),
            )
        ]
        guidance[(parent, child)] = " ".join([*named, *lines])
    return guidance, headers


@functools.lru_cache(maxsize=4)
def _frontmatter_properties(root: pathlib.Path) -> Mapping[str, Mapping[str, object]]:
    schema = _parse_json(
        root / "docs/99.templates/contracts/document-frontmatter.schema.json",
        MAX_SCHEMA_BYTES,
    )
    if not isinstance(schema, Mapping) or not isinstance(
        schema.get("properties"), Mapping
    ):
        raise RegistryError("frontmatter schema has no properties")
    return schema["properties"]  # type: ignore[return-value]


def _schema_data_type(spec: Mapping[str, object]) -> str:
    if "$ref" in spec:
        return str(spec["$ref"]).rsplit("/", 1)[-1]
    kind = spec.get("type", "string")
    kind = "|".join(kind) if isinstance(kind, list) else str(kind)
    return f"{kind} ({spec['format']})" if "format" in spec else kind


def _entry(dictionary: object, name: str, label: str) -> Mapping[str, object]:
    entry = dictionary.get(name) if isinstance(dictionary, Mapping) else None
    if not isinstance(entry, Mapping):
        raise RegistryError(f"{label} has no dictionary entry: {name}")
    return entry


def _structural_units(source: str, text: str) -> list[tuple[str, str, str | None]]:
    """Return (title, held text, frontmatter key or None) per top-level unit.

    Author prompts are removed before publishing, so they are no unit.
    """

    units: list[tuple[str, list[str], str | None]] = []
    lines = text.splitlines()
    if source.endswith(".md"):
        has_frontmatter = lines[:1] == ["---"]
        end = lines.index("---", 1) if has_frontmatter else -1
        for line in lines[1:end] if has_frontmatter else []:
            match = _FRONTMATTER_KEY.match(line)
            if match:
                units.append((f"frontmatter {match.group(1)}", [line], match.group(1)))
            elif units and line.strip():
                units[-1][1].append(line.strip())
        for line in lines[end + 1 :]:
            stripped = line.strip()
            if not stripped or _AUTHOR_PROMPT.match(stripped):
                continue
            if stripped.startswith("<!-- Generated by"):
                units.append(("Generated-by marker comment", [stripped], None))
            elif stripped.startswith("# "):
                units.append((f"H1 {stripped[2:]}", [stripped], None))
            else:
                units.append((f"Body {stripped}", [stripped], None))
    else:
        suffix = pathlib.PurePosixPath(source).suffix
        if suffix not in _STRUCTURAL_UNIT:
            raise RegistryError(f"no structural unit grammar for {source}")
        pattern = _STRUCTURAL_UNIT[suffix]
        for line in lines:
            match = pattern.match(line)
            if match:
                title = (match.group(1) if match.groups() else line).rstrip(" {};")
                units.append((title, [line.strip()], None))
            elif units and line.strip():
                units[-1][1].append(line.strip())
    return [(title, " ".join(held), key) for title, held, key in units]


def _structural_headings(
    template_id: str,
    source: str,
    text: str,
    profile: Mapping[str, object],
    conditional: Mapping[str, object],
) -> list[dict[str, object]]:
    required_keys = set(profile.get("required_frontmatter", ()))  # type: ignore[arg-type]
    grammar = (
        "{{UPPER_SNAKE_CASE}}" if source.endswith(".md") else "__UPPER_SNAKE_CASE__"
    )
    headings: list[dict[str, object]] = []
    units = _structural_units(source, text)
    unknown = set(conditional) - {title for title, _, _ in units}
    if unknown:
        raise RegistryError(f"{template_id} names absent units: {sorted(unknown)}")
    for order, (title, held, key) in enumerate(units, 1):
        if key is not None and key not in required_keys:
            requiredness, condition = (
                "optional",
                "a registered optional frontmatter key",
            )
        elif title in conditional:
            requiredness, condition = "conditional", str(conditional[title])
        else:
            requiredness, condition = "required", "always"
        checks = (
            ["template-frontmatter-missing", "template-frontmatter-unregistered"]
            if key in required_keys
            else ["template-frontmatter-unregistered"]
            if key
            else []
        )
        content = f"Holds `{held}` as it appears in {source}."
        headings.append(
            {
                "section_id": f"{template_id}-{_slug(title)}",
                "level": 2,
                "parent_id": None,
                "title": title,
                "order": order,
                "requiredness": requiredness,
                "condition": condition,
                "content": content,
                "required_content": [content],
                "prohibited_content": [
                    "An empty unit.",
                    f"A placeholder outside the {grammar} grammar.",
                ],
                "empty_policy": "forbidden"
                if requiredness == "required"
                else "omit_when_condition_false",
                "validation_ids": [*checks, PLACEHOLDER_CHECK, UNITS_CHECK],
                "children": [],
            }
        )
    return headings


def _section_headings(
    template_id: str,
    source: str,
    guidance: Mapping[tuple[str, str | None], str],
    profile: Mapping[str, object],
    conditional: Mapping[str, object],
    role_rule: str | None,
) -> list[dict[str, object]]:
    required_sub = profile.get("required_subsections") or {}
    optional_sub = profile.get("optional_subsections") or {}
    has_subsections = bool(required_sub or optional_sub)
    optional_titles = {str(name) for names in optional_sub.values() for name in names}
    unknown = set(conditional) - optional_titles
    if unknown:
        raise RegistryError(
            f"{template_id} names absent optional subsections: {sorted(unknown)}"
        )
    # The template states the declared subsection order.
    position = {key: index for index, key in enumerate(guidance)}
    ordered = bool(profile.get("ordered_sections"))
    nonempty = bool(profile.get("nonempty_sections"))

    def section(
        title: str,
        parent: str | None,
        parent_id: str | None,
        order: int,
        required: bool,
        children: list[dict[str, object]],
    ) -> dict[str, object]:
        level = 2 if parent is None else 3
        section_id = f"{parent_id or template_id}-{_slug(title)}"
        content = guidance.get((title, None) if parent is None else (parent, title))
        if not content:
            content = (
                "Groups the subsections "
                + ", ".join(str(child["title"]) for child in children)
                + "."
                if children
                else f"{source} gives no guidance for this registered section."
            )
        prefix = "body-heading" if level == 2 else "body-subheading"
        ids = [f"{prefix}-missing"] if required else []
        ids.append(f"{prefix}-duplicate")
        if required and ordered:
            ids.append(f"{prefix}-order")
        if nonempty:
            ids.append("body-section-empty")
        if has_subsections:
            ids.append("body-section-placeholder")
        if required:
            requiredness, condition = "required", "always"
        elif level == 3 and title in conditional:
            requiredness, condition = "conditional", str(conditional[title])
        else:
            requiredness, condition = (
                "optional",
                "optional: the profile registers no narrower condition; "
                "omit the section when the document has nothing for it",
            )
        return {
            "section_id": section_id,
            "level": level,
            "parent_id": parent_id,
            "title": title,
            "order": order,
            "requiredness": requiredness,
            "condition": condition,
            "content": content,
            "required_content": [content]
            + (
                ["The content, or one sentence on why none applies."]
                if required
                else []
            ),
            "prohibited_content": [
                *([role_rule] if role_rule else []),
                _STAND_IN_RULE if level == 3 else _EMPTY_SECTION_RULE,
            ],
            "empty_policy": "explain_none_or_not_applicable"
            if required
            else "omit_when_condition_false",
            "validation_ids": ids,
            "children": children,
        }

    headings = []
    titles = [
        *((str(name), True) for name in profile.get("required_sections", ())),
        *((str(name), False) for name in profile.get("optional_sections", ())),
    ]
    for order, (title, required) in enumerate(titles, start=1):
        parent_id = f"{template_id}-{_slug(title)}"
        sub = [
            *((str(name), True) for name in required_sub.get(title, ())),
            *((str(name), False) for name in optional_sub.get(title, ())),
        ]
        sub.sort(key=lambda item: position.get((title, item[0]), len(position)))
        children = [
            section(name, title, parent_id, index, flag, [])
            for index, (name, flag) in enumerate(sub, start=1)
        ]
        headings.append(section(title, None, None, order, required, children))
    return headings


def _metadata(
    source: str,
    text: str,
    profile: Mapping[str, object],
    common: Mapping[str, object],
    root: pathlib.Path,
) -> list[dict[str, object]]:
    keys = common.get("frontmatter_key_definitions")
    if source.endswith(".toml"):
        # The renderer writes exactly these keys and recognizes a projection
        # only when all of them are present, so each is required.
        try:
            document = tomllib.loads(text)
        except tomllib.TOMLDecodeError as error:
            raise RegistryError(f"{source} is not TOML: {error}") from error
        fields = [
            (
                name,
                "required",
                "always; the renderer writes every key",
                type(value).__name__.replace("str", "string"),
            )
            for name, value in document.items()
        ]
    else:
        properties = _frontmatter_properties(root)
        by_status: dict[str, list[str]] = {}
        for status, names in (
            profile.get("required_frontmatter_by_status") or {}
        ).items():
            for name in names:
                by_status.setdefault(str(name), []).append(str(status))
        required = set(profile.get("required_frontmatter", ()))  # type: ignore[arg-type]
        fixed = profile.get("frontmatter_values") or {}
        fields = []
        for name in dict.fromkeys(
            [
                *profile.get("required_frontmatter", ()),
                *profile.get("optional_frontmatter", ()),
                *by_status,
            ]
        ):
            if name in by_status:
                requiredness = "conditional"
                condition = "required when status is " + " or ".join(by_status[name])
            elif name in required:
                requiredness, condition = "required", "always"
            else:
                requiredness, condition = "optional", "present only when it applies"
            if name in fixed:
                condition += f"; value must be {json.dumps(_plain(fixed[name]))}"
            if name not in properties:
                raise RegistryError(f"frontmatter schema does not define {name}")
            fields.append(
                (name, requiredness, condition, _schema_data_type(properties[name]))
            )
    metadata = []
    for name, requiredness, condition, data_type in fields:
        entry = _entry(keys, str(name), "frontmatter key")
        metadata.append(
            {
                "name": name,
                "meaning": entry["meaning"],
                "data_type": data_type,
                "requiredness": requiredness,
                "condition": condition,
                "writer": entry["writer"],
                "consumers": _plain(entry["consumers"]),
            }
        )
    return metadata


def _tables(
    headings: list[dict[str, object]],
    headers: list[tuple[str, str | None, str]],
    common: Mapping[str, object],
) -> list[dict[str, object]]:
    ids: dict[tuple[str, str | None], str] = {}
    for heading in headings:
        ids[(str(heading["title"]), None)] = str(heading["section_id"])
        for child in heading["children"]:  # type: ignore[union-attr]
            ids[(str(heading["title"]), str(child["title"]))] = str(child["section_id"])
    dictionary = common.get("table_column_definitions")
    tables = []
    for h2, h3, header in headers:
        cells = [cell.strip() for cell in header.strip("|").split("|")]
        name, required_columns, optional_columns, minimum = (
            _slug(h3 or h2).replace("-", "_"),
            cells,
            [],
            0,
        )
        for key, optional_key, rows in _TABLE_CONTRACTS:
            contract = [str(item) for item in common.get(key, ())]
            extra = (
                [str(item) for item in common.get(optional_key, ())]
                if optional_key
                else []
            )
            if cells in (contract, contract + extra):
                name, required_columns, optional_columns, minimum = (
                    key.removesuffix("_columns"),
                    contract,
                    extra,
                    rows,
                )
                break
        section = ids.get((h2, h3)) or ids.get((h2, None))
        if section is None:
            raise RegistryError(f"table under unregistered section: {h2}")
        tables.append(
            {
                "name": name,
                "section": section,
                "columns": [
                    {
                        "key": column,
                        "meaning": _entry(dictionary, column, "table column")[
                            "meaning"
                        ],
                        "data_type": _entry(dictionary, column, "table column")[
                            "data_type"
                        ],
                        "required": column in required_columns,
                    }
                    for column in required_columns + optional_columns
                ],
                "minimum_rows": minimum,
                "row_identity": required_columns[0],
            }
        )
    return tables


def _extensions(
    profile_id: str, profile: Mapping[str, object], common: Mapping[str, object]
) -> list[dict[str, object]]:
    definitions = common.get("profile_exception_definitions")
    declared = [
        (str(item["kind"]), item.get("owner"))
        for item in profile.get("exceptions", ())  # type: ignore[union-attr]
    ]
    if profile.get("free_form_sections"):
        declared.append(("free-form-sections", None))
    extensions = []
    for kind, owner in declared:
        entry = _entry(definitions, kind, "profile exception")
        extensions.append(
            {
                "condition": f"The {profile_id} profile declares {kind}.",
                "owner": str(owner or entry["owner"]),
                "delta": str(entry["delta"]),
                "validation": str(entry["validation"]),
                "expiry_or_review": str(entry["expiry_or_review"]),
            }
        )
    return extensions


def template_definition(
    registry: DocumentRegistry, template_id: str, *, root: pathlib.Path = ROOT
) -> dict[str, object]:
    """Return the TemplateDefinition of one registered template role."""

    role = registry.template_roles.get(template_id)
    if role is None:
        raise RegistryError(f"unknown template role: {template_id}")
    missing = [field for field in TEMPLATE_DEFINITION_FIELDS if field not in role]
    if missing:
        raise RegistryError(f"{template_id} lacks authored fields: {missing}")
    profile_id = str(role["profiles"][0])  # type: ignore[index]
    profile = registry.profiles.get(profile_id)
    if profile is None:
        raise RegistryError(f"{template_id} names an unknown profile: {profile_id}")
    common = registry.common
    source = str(role["source"])
    try:
        text = (root / source).read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise RegistryError(f"cannot read template {source}: {error}") from error
    guidance, headers = _template_outline(text)
    if profile.get("required_sections") or profile.get("optional_sections"):
        role_rule = (common.get("section_prohibited_content") or {}).get(template_id)
        if profile.get("required_subsections") and not role_rule:
            raise RegistryError(f"{template_id} has no section_prohibited_content")
        headings = _section_headings(
            template_id,
            source,
            guidance,
            profile,
            role.get("conditional_units", {}),
            role_rule,
        )
    else:
        headings = _structural_headings(
            template_id, source, text, profile, role.get("conditional_units", {})
        )
    lifecycle_id = profile.get("lifecycle_id")
    if lifecycle_id is None:
        lifecycle = (
            "none: the profile has no lifecycle_id and its files carry no status"
        )
    elif lifecycle_id not in registry.lifecycles:
        raise RegistryError(f"{template_id} names an unknown lifecycle: {lifecycle_id}")
    else:
        lifecycle = (
            f"{lifecycle_id}: initial {registry.lifecycle_initial_statuses.get(lifecycle_id)}; "
            f"statuses {', '.join(registry.lifecycles[lifecycle_id])}; terminal "
            f"{', '.join(registry.lifecycle_terminal_statuses.get(lifecycle_id, ())) or 'none'}"
        )
    language = profile.get("language")
    return {
        "template_id": template_id,
        "contract_version": COMMON_FORM_VERSION
        if profile.get("required_subsections")
        else str(common.get("contract_id")),
        "role": template_id,
        "purpose": role["purpose"],
        "responsibility": role["responsibility"],
        "non_goals": _plain(role["non_goals"]),
        "policy_refs": _plain(role["policy_refs"]),
        "vocabulary_refs": _plain(role["vocabulary_refs"]),
        "applicability": role["applicability"],
        "metadata": _metadata(source, text, profile, common, root),
        "headings": headings,
        "tables": _tables(headings, headers, common),
        "relationships": _plain(role["relationships"]),
        "lifecycle": lifecycle,
        "language": str(language)
        if language
        else "undeclared: the profile declares no language, so the language check "
        "does not judge it",
        "consumer_paths": _plain(role["consumer_paths"]),
        "validation": _plain(role["validation"]),
        "migration": _plain(role["migration"]),
        "extensions": _extensions(profile_id, profile, common),
    }
