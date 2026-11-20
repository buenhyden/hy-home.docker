"""Project Registry template roles onto TemplateDefinition.

A `template_roles` entry holds only the authored fields the Registry has no
other source for. Everything else is derived here from the bound profile, the
template file and the shared `common` dictionaries, so no fact is held twice.
The record shape is `docs/99.templates/01.contracts/template-definition.schema.json`.
"""

from __future__ import annotations

import functools
import json
import pathlib
import re
import tomllib
from collections.abc import Mapping, Sequence

from scripts.lib.document_governance.metadata.heading import (
    _markdown_form_lines,
    _table_delimiter_matches,
)
from scripts.lib.document_governance.registry import (
    MAX_SCHEMA_BYTES,
    ROOT,
    TEMPLATE_DEFINITION_FIELDS,
    DocumentRegistry,
    RegistryError,
    _parse_json,
    _read_regular_file,
)

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
    return re.sub(r"[\W_]+", "-", title.lower()).strip("-")


def _common_headings(template_id: str, core: Mapping) -> list[dict[str, object]]:
    """Project the one common outer contract; role sections remain its payload."""
    check = "tests.lib.document_governance.test_template_definition:CommonDocumentContractTests"

    def section(
        title: str, level: int, parent: str | None, order: int, children: list
    ) -> dict:
        rule = core["section_rules"].get(
            title,
            "Provide the stated common child sections without duplicating role responsibility.",
        )
        identity = f"{template_id}-core-{_slug(title)}"
        return {
            "section_id": identity,
            "level": level,
            "parent_id": parent,
            "title": title,
            "order": order,
            "requiredness": "required",
            "condition": "always",
            "content": rule,
            "required_content": [rule],
            "prohibited_content": [_EMPTY_SECTION_RULE, _STAND_IN_RULE],
            "empty_policy": "explain_none_or_not_applicable",
            "validation_ids": [check],
            "children": children,
        }

    result = []
    for order, (title, children) in enumerate(core["headings"].items(), 1):
        identity = f"{template_id}-core-{_slug(title)}"
        result.append(
            section(
                title,
                2,
                None,
                order,
                [
                    section(child, 3, identity, index, [])
                    for index, child in enumerate(children, 1)
                ],
            )
        )
    return result


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
    delimiter_index = -1
    lines = _markdown_form_lines(text)
    for index, raw, heading in lines:
        if index == delimiter_index:
            continue
        line = raw.strip()
        if heading is not None and heading[0] in (2, 3):
            level, title = heading
            if level == 2:
                h2, h3 = title, None
            elif h2 is not None:
                h3 = title
            else:
                continue
            bodies.setdefault((h2, h3), [])  # type: ignore[arg-type]
            previous = ""
            continue
        if not line:
            previous = ""
            continue
        if h2 is None:
            prompt = _AUTHOR_PROMPT.match(line)
            if prompt:
                preamble.append(prompt.group(1))
            continue
        if line.startswith("|"):
            if not previous.startswith("|"):
                if index + 1 == len(lines) or not _table_delimiter_matches(
                    raw, lines[index + 1][1]
                ):
                    raise RegistryError(
                        f"invalid table delimiter under {h2}/{h3 or '-'}"
                    )
                headers.append((h2, h3, line))
                delimiter_index = index + 1
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
        root / "docs/99.templates/01.contracts/document-frontmatter.schema.json",
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

    Source authoring controls removed before publishing are not output units.
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
            if (
                not stripped
                or _AUTHOR_PROMPT.match(stripped)
                or stripped == "<!-- markdownlint-disable-next-line MD041 -->"
            ):
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
    core: Mapping[str, object] | None = None,
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
        if core is not None:
            # A bound role's columns, types and requiredness are the core's.
            owners = {
                str(item["section_id"]): str(h2_section["title_en"])
                for h2_section in core["sections"]  # type: ignore[union-attr]
                for item in (h2_section, *h2_section.get("subsections", ()))
            }
            match = next(
                (
                    table
                    for table in core["tables"]  # type: ignore[union-attr]
                    if [column["label"] for column in table["columns"]] == cells
                    and owners.get(str(table["section_id"])) == h2
                ),
                None,
            )
            if match is None:
                raise RegistryError(f"table under {h2} is not in the core role")
            tables.append(
                {
                    "name": str(match["table_id"]),
                    "section": section,
                    "columns": [
                        {
                            "key": str(column["label"]),
                            "meaning": str(column["meaning"]),
                            "data_type": str(column["value_type"]),
                            "required": bool(column["required"]),
                        }
                        for column in match["columns"]
                    ],
                    "minimum_rows": 0,
                    "row_identity": str(match["columns"][0]["label"]),
                }
            )
            continue
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
    from scripts.lib.document_governance.common_document import (
        load_contract,
        template_payload,
    )

    source = str(role.get("native_source", role["source"]))
    try:
        text = template_payload(registry, template_id, root=root)
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
    if role.get("core_role"):
        binding = _entry(common, "role_design_contract", "common")
    elif profile.get("required_subsections"):
        binding = _entry(common, "common_form_contract", "common")
    else:
        binding = common
    definition = {
        "template_id": template_id,
        "contract_id": binding["contract_id"],
        "contract_version": binding["contract_version"],
        "role": template_id,
        "purpose": role["purpose"],
        "responsibility": role["responsibility"],
        "non_goals": _plain(role["non_goals"]),
        "policy_refs": _plain(role["policy_refs"]),
        "vocabulary_refs": _plain(role["vocabulary_refs"]),
        "applicability": role["applicability"],
        "metadata": _metadata(source, text, profile, common, root),
        "headings": headings,
        "tables": _tables(
            headings,
            headers,
            common,
            core_role_definition(registry, template_id, root=root),
        ),
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
    document_core = common.get("document_core")
    if not isinstance(document_core, Mapping):
        return definition
    try:
        core = load_contract(root=root)
    except ValueError as error:
        raise RegistryError(str(error)) from error
    binding = document_core["profile_bindings"][profile_id]
    native = bool(role.get("native_source"))
    metadata_adapter = (
        {
            "title": "definition.title",
            "version": "definition.version",
            "kind": "registry.profile_binding.kind",
            "owner": "definition.owner",
            "lifecycle": "definition.status",
            "scope": "definition.document_scope",
        }
        if native
        else {
            "title": "title",
            "version": "version",
            "kind": "registry.profile_binding.kind",
            "owner": "owner",
            "lifecycle": str(binding["lifecycle_field"]),
            "scope": "document_scope",
        }
    )
    return {
        **definition,
        "contract_id": document_core["contract_id"],
        "contract_version": document_core["contract_version"],
        "headings": _common_headings(template_id, core),
        "payload": {
            "contract_id": definition["contract_id"],
            "contract_version": definition["contract_version"],
            "kind": binding["kind"],
            "source": source,
            "format": pathlib.PurePosixPath(source).suffix.removeprefix("."),
            "headings": headings,
            "metadata_adapter": metadata_adapter,
        },
    }


def _core_required(item: Mapping[str, object]) -> bool:
    return item.get("required_when") == "always"


def role_design_findings(
    core_roles: Mapping[str, Mapping[str, object]],
    bindings: Mapping[str, str],
    definitions: Mapping[str, Mapping[str, object]],
) -> list[tuple[str, str, str]]:
    """Compare bound TemplateDefinition projections with their core roles.

    A role conforms only when its H2 and H3 titles, their array order and
    requiredness, and every table's owning section, column labels and column
    requiredness equal the core; an extra or missing table fails. A table the
    core assigns to an H2 may sit in any H3 of that H2. Not compared: a
    table's own required_when, which the projection does not carry, and the
    core's numeric order fields, which the array order already expresses.
    """

    findings: list[tuple[str, str, str]] = []
    for template_id, core_name in sorted(bindings.items()):
        core = core_roles.get(core_name)
        if core is None:
            findings.append(
                ("role-design-unknown-role", template_id, f"no core role {core_name}")
            )
            continue
        definition = definitions[template_id]
        headings = definition.get("payload", {}).get("headings", definition["headings"])
        actual = [
            (
                h2["title"],
                h2["requiredness"] == "required",
                [
                    (h3["title"], h3["requiredness"] == "required")
                    for h3 in h2["children"]
                ],
            )
            for h2 in headings  # type: ignore[union-attr]
        ]
        expected = [
            (
                section["title_en"],
                _core_required(section),
                [
                    (sub["title_en"], _core_required(sub))
                    for sub in section["subsections"]  # type: ignore[union-attr]
                ],
            )
            for section in core["sections"]  # type: ignore[union-attr]
        ]
        if actual != expected:
            findings.append(
                (
                    "role-design-heading-mismatch",
                    template_id,
                    f"H2/H3 titles or requiredness differ from core role {core_name}",
                )
            )
        core_places: dict[str, tuple[str, str | None]] = {}
        for section in core["sections"]:  # type: ignore[union-attr]
            core_places[str(section["section_id"])] = (str(section["title_en"]), None)
            for sub in section["subsections"]:  # type: ignore[union-attr]
                core_places[str(sub["section_id"])] = (
                    str(section["title_en"]),
                    str(sub["title_en"]),
                )
        expected_places = [
            core_places.get(str(table["section_id"]), ("", None))
            for table in core["tables"]  # type: ignore[union-attr]
        ]
        h2_owned = {h2 for h2, h3 in expected_places if h3 is None}
        places: dict[str, tuple[str, str | None]] = {}
        for h2 in headings:  # type: ignore[union-attr]
            places[str(h2["section_id"])] = (str(h2["title"]), None)
            for h3 in h2["children"]:
                places[str(h3["section_id"])] = (str(h2["title"]), str(h3["title"]))

        def place(
            key: tuple[str, str | None], owned: set[str] = h2_owned
        ) -> tuple[str, str]:
            h2, h3 = key
            return (h2, "") if h2 in owned or h3 is None else (h2, h3)

        actual_tables = sorted(
            (
                place(places.get(str(table["section"]), ("", None))),
                [(str(c["key"]), bool(c["required"])) for c in table["columns"]],
            )
            for table in definition["tables"]  # type: ignore[union-attr]
        )
        expected_tables = sorted(
            (
                place(key),
                [(str(c["label"]), bool(c["required"])) for c in table["columns"]],
            )
            for key, table in zip(expected_places, core["tables"], strict=True)  # type: ignore[arg-type]
        )
        if actual_tables != expected_tables:
            findings.append(
                (
                    "role-design-table-mismatch",
                    template_id,
                    f"tables differ from core role {core_name}",
                )
            )
    return findings


def _pinned_json(
    root: pathlib.Path, path: str, sha256: object
) -> tuple[object, tuple[str, str, str] | None]:
    import hashlib

    try:
        raw = _read_regular_file(root / path, MAX_SCHEMA_BYTES)
    except (OSError, RegistryError) as error:
        return None, ("role-design-source-unreadable", path, str(error))
    if hashlib.sha256(raw).hexdigest() != sha256:
        return None, (
            "role-design-source-changed",
            path,
            "sha256 differs from Registry",
        )
    try:
        return _parse_json(root / path, MAX_SCHEMA_BYTES), None
    except RegistryError as error:
        return None, ("role-design-source-invalid", path, str(error))


def role_design_contract_findings(
    registry: DocumentRegistry, *, root: pathlib.Path = ROOT
) -> list[tuple[str, str, str]]:
    """Check the Registry's pinned role design core and every role's binding.

    The profile schema owns the binding shape: exactly one of core_role and
    core_exception, and a pending-migration exception names its core role
    while a domain or native one names none.
    """

    from jsonschema import Draft202012Validator, SchemaError

    contract = registry.common.get("role_design_contract")
    if not isinstance(contract, Mapping):
        return [("role-design-contract-missing", "common", "")]
    source, schema_path = str(contract["source_path"]), str(contract["schema_path"])
    schema, failure = _pinned_json(root, schema_path, contract["schema_sha256"])
    if failure:
        return [failure]
    core, failure = _pinned_json(root, source, contract["source_sha256"])
    if failure:
        return [failure]
    try:
        Draft202012Validator.check_schema(schema)  # type: ignore[arg-type]
    except SchemaError as error:
        return [("role-design-source-invalid", schema_path, error.message)]
    findings = [
        ("role-design-source-invalid", source, error.message)
        for error in Draft202012Validator(schema).iter_errors(core)  # type: ignore[arg-type]
    ]
    if findings or not isinstance(core, Mapping):
        return findings or [("role-design-source-invalid", source, "not an object")]
    if (core.get("contract_id"), core.get("contract_version")) != (
        contract["contract_id"],
        contract["contract_version"],
    ):
        return [("role-design-identity", source, "id or version differs")]
    core_roles = {str(role["role"]): role for role in core["roles"]}  # type: ignore[union-attr]
    bindings: dict[str, str] = {}
    named: set[str] = set()
    for template_id, role in registry.template_roles.items():
        exception = role.get("core_exception")
        name = role.get("core_role") or (
            exception.get("core_role") if isinstance(exception, Mapping) else None
        )
        if name is not None and str(name) not in core_roles:
            findings.append(
                ("role-design-unknown-role", template_id, f"no core role {name}")
            )
            continue
        if name is not None:
            named.add(str(name))
        if role.get("core_role"):
            bindings[template_id] = str(role["core_role"])
    for missing in sorted(set(core_roles) - named):
        findings.append(("role-design-core-unmapped", missing, "no template role"))
    definitions: dict[str, Mapping[str, object]] = {}
    for template_id in list(bindings):
        try:
            definitions[template_id] = template_definition(
                registry, template_id, root=root
            )
        except RegistryError as error:
            findings.append(("role-design-projection", template_id, str(error)))
            del bindings[template_id]
    return findings + role_design_findings(core_roles, bindings, definitions)


@functools.lru_cache(maxsize=4)
def _pinned_core(root: pathlib.Path, path: str, sha256: str) -> Mapping[str, object]:
    core, failure = _pinned_json(root, path, sha256)
    if failure is not None:
        raise RegistryError(f"{failure[0]}: {failure[1]}")
    if not isinstance(core, Mapping):
        raise RegistryError(f"{path} is not a JSON object")
    return core


def core_role_definition(
    registry: DocumentRegistry, template_id: str, *, root: pathlib.Path = ROOT
) -> Mapping[str, object] | None:
    """Return the pinned core role a template role is bound to, if any."""

    name = registry.template_roles[template_id].get("core_role")
    if not name:
        return None
    contract = _entry(registry.common, "role_design_contract", "common")
    core = _pinned_core(
        root, str(contract["source_path"]), str(contract["source_sha256"])
    )
    for role in core["roles"]:  # type: ignore[union-attr]
        if role["role"] == name:
            return role
    raise RegistryError(f"{template_id} names an unknown core role: {name}")
