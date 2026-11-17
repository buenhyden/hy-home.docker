from __future__ import annotations

import copy
import importlib
import json
import pathlib
import re
import tempfile
import unittest

from jsonschema import Draft202012Validator

from scripts.lib.document_governance.registry import (
    ROOT,
    RegistryError,
    _registry_from_document,
    load_registry,
    load_registry_document,
    validate_registry,
)
from scripts.lib.document_governance.template_definition import template_definition

SCHEMA_PATH = ROOT / "docs/99.templates/contracts/template-definition.schema.json"
GLOSSARY = ROOT / ".agents/knowledge/glossary.md"


def _errors(definition: object) -> list[str]:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    return sorted(
        "/".join(map(str, error.absolute_path)) + ": " + error.validator
        for error in validator.iter_errors(definition)
    )


def _slug(value: str) -> str:
    text = re.sub(r"[`*_~]", "", value.strip().lower())
    text = re.sub(r"[^\w\- ]", "", text)
    return re.sub(r"[ -]+", "-", text).strip("-")


def _reference_failures(definition: dict) -> list[str]:
    """Return every authored reference that does not resolve."""

    failures = []
    glossary = GLOSSARY.read_text(encoding="utf-8")
    for path in definition["consumer_paths"]:
        if not (ROOT / path).is_file():
            failures.append(path)
    for ref in definition["policy_refs"]:
        path, _, anchor = ref.partition("#")
        target = ROOT / path
        if (
            not re.fullmatch(r"\.agents/governance/[a-z-]+\.md", path)
            or not target.is_file()
        ):
            failures.append(ref)
            continue
        text = target.read_text(encoding="utf-8")
        if anchor not in {_slug(h) for h in re.findall(r"^#{1,6} +(.+)$", text, re.M)}:
            failures.append(ref)
    for term in definition["vocabulary_refs"]:
        if f"| {term.removeprefix('local:')} |" not in glossary:
            failures.append(term)
    for kind in ("positive", "negative", "regression"):
        for name in definition["validation"][kind]:
            if name.startswith("scripts/"):
                if not (ROOT / name.split()[0]).is_file():
                    failures.append(name)
                continue
            module, _, attribute = name.partition(":")
            try:
                loaded = importlib.import_module(module)
                for part in filter(None, attribute.split(".")):
                    loaded = getattr(loaded, part)
            except (ImportError, AttributeError):
                failures.append(name)
    return failures


def _template_headings(text: str) -> list[tuple[int, str]]:
    from scripts.lib.document_governance.metadata.heading import (
        _HEADING_LINE,
        _markdown_unfenced_lines,
    )

    found = []
    for line in _markdown_unfenced_lines(text):
        match = _HEADING_LINE.match(line)
        if match and len(match.group(1)) in (2, 3):
            found.append((len(match.group(1)), match.group(2)))
    return found


class TemplateDefinitionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = load_registry()
        cls.definitions = {
            role: template_definition(cls.registry, role)
            for role in cls.registry.template_roles
        }

    def _profile(self, role: str):
        return self.registry.profiles[self.registry.template_roles[role]["profiles"][0]]

    def test_schema_rejects_a_combined_contract_version(self) -> None:
        definition = dict(self.definitions["sdlc/task"])
        definition["contract_version"] = "COMMON-DOC-FORM-1/1.0.0"
        del definition["contract_id"]
        errors = _errors(definition)
        self.assertIn(": required", errors)
        self.assertIn("contract_version: pattern", errors)

    def test_every_definition_validates_against_the_schema(self) -> None:
        Draft202012Validator.check_schema(
            json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        )
        for role, definition in self.definitions.items():
            with self.subTest(role=role):
                self.assertEqual([], _errors(definition))

    def test_section_ids_are_unique(self) -> None:
        for role, definition in self.definitions.items():
            ids = [h["section_id"] for h in definition["headings"]] + [
                c["section_id"] for h in definition["headings"] for c in h["children"]
            ]
            with self.subTest(role=role):
                self.assertEqual(len(ids), len(set(ids)))

    def test_headings_equal_the_profile_sections(self) -> None:
        for role, definition in self.definitions.items():
            profile = self._profile(role)
            if not (
                profile.get("required_sections") or profile.get("optional_sections")
            ):
                continue
            with self.subTest(role=role):
                self.assertEqual(
                    [
                        *profile.get("required_sections", ()),
                        *profile.get("optional_sections", ()),
                    ],
                    [heading["title"] for heading in definition["headings"]],
                )
                for heading in definition["headings"]:
                    title = heading["title"]
                    # Order is the template's; see the declared-order test.
                    self.assertCountEqual(
                        [
                            *profile.get("required_subsections", {}).get(title, ()),
                            *profile.get("optional_subsections", {}).get(title, ()),
                        ],
                        [child["title"] for child in heading["children"]],
                    )

    def test_headings_match_the_template_file(self) -> None:
        for role, definition in self.definitions.items():
            source = self.registry.template_roles[role]["source"]
            if not source.endswith(".md") or not self._profile(role).get(
                "required_sections"
            ):
                continue
            found = _template_headings((ROOT / source).read_text(encoding="utf-8"))
            h2 = [title for level, title in found if level == 2]
            with self.subTest(role=role):
                derived = [h["title"] for h in definition["headings"]]
                required = [
                    h["title"]
                    for h in definition["headings"]
                    if h["requiredness"] == "required"
                ]
                # The template shows every required H2 in order; any other
                # H2 it shows is a registered optional section.
                self.assertEqual(required, [t for t in h2 if t in required])
                self.assertLessEqual(set(h2), set(derived))
                if self._profile(role).get("required_subsections"):
                    h3 = [title for level, title in found if level == 3]
                    children = [
                        c for h in definition["headings"] for c in h["children"]
                    ]
                    required_children = [
                        c["title"] for c in children if c["requiredness"] == "required"
                    ]
                    # The validator orders required subsections only; an
                    # optional one may sit anywhere under its parent.
                    self.assertEqual(
                        required_children, [t for t in h3 if t in required_children]
                    )
                    self.assertLessEqual(set(h3), {c["title"] for c in children})

    def test_conditional_subsections_carry_the_contract_condition(self) -> None:
        # COMMON-DOC-FORM-1 1.0.0 marks exactly these H3s conditional.
        expected = {
            ("sdlc/requirement", "Quality Requirements"): "when a quality "
            "requirement applies",
            ("sdlc/architecture-decision", "Supersession"): "when an actual "
            "predecessor or successor decision exists, or the change supersedes one",
        }
        found = {}
        for role, definition in self.definitions.items():
            for heading in definition["headings"]:
                for child in heading["children"]:
                    if child["requiredness"] != "required":
                        found[(role, child["title"])] = (
                            child["requiredness"],
                            child["condition"],
                            child["empty_policy"],
                        )
        self.assertEqual(
            {
                key: ("conditional", text, "omit_when_condition_false")
                for key, text in expected.items()
            },
            found,
        )

    def test_subsections_keep_the_declared_order(self) -> None:
        recovery = next(
            h
            for h in self.definitions["operation/runbook"]["headings"]
            if h["title"] == "Escalation"
        )
        self.assertEqual(
            [("Next Owner", 1), ("Recovery or Forward Repair", 2)],
            [(c["title"], c["order"]) for c in recovery["children"]],
        )
        for role, definition in self.definitions.items():
            if not self._profile(role).get("required_subsections"):
                continue
            source = self.registry.template_roles[role]["source"]
            found = _template_headings((ROOT / source).read_text(encoding="utf-8"))
            h3 = [title for level, title in found if level == 3]
            with self.subTest(role=role):
                children = [
                    c["title"] for h in definition["headings"] for c in h["children"]
                ]
                self.assertEqual([t for t in h3 if t in children], children)

    def test_prohibited_content_keys_name_template_roles(self) -> None:
        # A misspelled key would otherwise be ignored silently.
        keys = set(self.registry.common["section_prohibited_content"])
        self.assertLessEqual(keys, set(self.registry.template_roles))

    def test_sections_carry_their_role_prohibited_content(self) -> None:
        # COMMON-DOC-FORM-1 1.0.0: an H2 carries the role rule and one empty
        # rule that includes a guidance-comment-only body; an H3 carries the
        # role rule and the stand-in rule, and no empty rule.
        role_rule = {
            "sdlc/requirement": "Implementation detail or Task status, which "
            "the Requirement does not own.",
            "operation/runbook": "Procedure guidance presented as execution "
            "approval, or a stored secret value.",
            "governance/policy": "A rule weakened to suit a test.",
        }
        stand_in = (
            "A same-named heading inside a code fence, quote or comment "
            "standing in for the real section."
        )
        empty = (
            "A heading with no body, or a body that is only an unexplained "
            "TODO, TBD, N/A, - or a template guidance comment."
        )
        for role, definition in self.definitions.items():
            if not self._profile(role).get("required_subsections"):
                continue
            with self.subTest(role=role):
                for heading in definition["headings"]:
                    rules = heading["prohibited_content"]
                    self.assertEqual(2, len(rules), heading["title"])
                    self.assertEqual(empty, rules[1])
                    if role in role_rule:
                        self.assertEqual(role_rule[role], rules[0])
                    for child in heading["children"]:
                        self.assertEqual(
                            [rules[0], stand_in], child["prohibited_content"]
                        )

    def test_headingless_templates_use_their_real_top_level_units(self) -> None:
        expected = {
            "sdlc/openapi": ["openapi", "info", "paths", "components"],
            "sdlc/graphql": ["schema", "type Query", "type __OBJECT_TYPE__"],
            "sdlc/proto": [
                'syntax = "proto3"',
                "package __PACKAGE_NAME__",
                "service __SERVICE_NAME__",
                "message HealthRequest",
                "message HealthResponse",
            ],
            "governance/codex-agent": [
                "name",
                "description",
                "developer_instructions",
                "model",
                "model_reasoning_effort",
                "sandbox_mode",
            ],
            "governance/claude-agent": [
                "frontmatter name",
                "frontmatter description",
                "frontmatter tools",
                "frontmatter model",
                "frontmatter effort",
                "frontmatter permissionMode",
                "frontmatter skills",
                "Generated-by marker comment",
                "H1 {{NAME}}",
                "Body {{AGENT_BODY}}",
            ],
        }
        for role, titles in expected.items():
            with self.subTest(role=role):
                self.assertEqual(
                    titles, [h["title"] for h in self.definitions[role]["headings"]]
                )
        proto = {
            h["title"]: h["requiredness"]
            for h in self.definitions["sdlc/proto"]["headings"]
        }
        self.assertEqual("conditional", proto["message HealthRequest"])
        self.assertEqual("required", proto["service __SERVICE_NAME__"])
        codex = self.definitions["governance/codex-agent"]
        self.assertEqual(
            expected["governance/codex-agent"], [m["name"] for m in codex["metadata"]]
        )

    def test_a_codex_projection_carries_only_the_rendered_keys(self) -> None:
        from scripts.operations import provider_surface_renderer as renderer

        profile = self.registry.profiles["runtime-projection-codex"]
        rendered = {
            m["name"] for m in self.definitions["governance/codex-agent"]["metadata"]
        }
        self.assertLessEqual(
            {*profile["required_frontmatter"], *profile["optional_frontmatter"]},
            rendered,
        )
        projection = (ROOT / ".codex/agents/doc-writer.toml").read_bytes()
        self.assertTrue(renderer._is_codex_agent_projection(projection))
        self.assertFalse(
            renderer._is_codex_agent_projection(
                projection + b'permissionMode = "plan"\n'
            )
        )

    def test_a_claude_projection_carries_only_the_rendered_keys(self) -> None:
        from scripts.lib.document_governance.frontmatter import parse_frontmatter_text
        from scripts.operations import provider_surface_renderer as renderer

        expected = {
            path.as_posix(): content
            for path, content in renderer.expected_projection(ROOT, "claude").items()
            if path.as_posix().startswith(".claude/agents/")
        }
        self.assertTrue(expected)
        written: set[str] = set()
        for content in expected.values():
            written |= set(parse_frontmatter_text(content.decode("utf-8")))
        self.assertTrue({"model_reasoning_effort", "version"}.isdisjoint(written))
        profile = self.registry.profiles["runtime-projection-claude"]
        self.assertLessEqual(
            {*profile["required_frontmatter"], *profile["optional_frontmatter"]},
            written,
        )
        # The renderer --check compares each tracked projection with these
        # bytes, so a projection carrying a Codex-only key is drift.
        path = ".claude/agents/doc-writer.md"
        self.assertEqual(expected[path], (ROOT / path).read_bytes())
        tampered = expected[path].replace(
            b"\n---\n", b'\nmodel_reasoning_effort: "high"\n---\n', 1
        )
        self.assertIn(b"model_reasoning_effort", tampered)
        self.assertNotEqual(expected[path], tampered)

    def test_authored_references_resolve(self) -> None:
        for role, definition in self.definitions.items():
            with self.subTest(role=role):
                self.assertEqual([], _reference_failures(definition))

    def test_dangling_authored_references_are_reported(self) -> None:
        definition = copy.deepcopy(self.definitions["sdlc/task"])
        definition["consumer_paths"] = ["scripts/does-not-exist.py"]
        definition["policy_refs"] = [".agents/governance/sdlc.md#no-such-anchor"]
        definition["vocabulary_refs"] = ["TERM-NOT-A-TERM"]
        definition["validation"]["positive"] = [
            "tests.lib.document_governance.test_registry:NoSuchTests"
        ]
        self.assertEqual(4, len(_reference_failures(definition)))

    def test_a_missing_required_field_is_rejected(self) -> None:
        for role, definition in self.definitions.items():
            changed = copy.deepcopy(definition)
            del changed["purpose"]
            with self.subTest(role=role):
                self.assertIn(": required", _errors(changed))

    def test_empty_headings_are_rejected(self) -> None:
        for role, definition in self.definitions.items():
            changed = copy.deepcopy(definition)
            changed["headings"] = []
            with self.subTest(role=role):
                self.assertIn("headings: minItems", _errors(changed))

    def test_a_release_role_is_rejected(self) -> None:
        for role in ("Release", "release", "operations/release"):
            definition = copy.deepcopy(self.definitions["sdlc/task"])
            definition["role"] = role
            with self.subTest(role=role):
                self.assertIn("role: not", _errors(definition))

    def test_an_unknown_key_is_rejected(self) -> None:
        definition = copy.deepcopy(self.definitions["sdlc/task"])
        definition["owner"] = "@someone"
        self.assertIn(": additionalProperties", _errors(definition))
        raw = copy.deepcopy(dict(load_registry_document()))
        raw["template_roles"]["sdlc/task"]["owner"] = "@someone"
        findings = validate_registry(raw)
        self.assertIn(
            ("schema-invalid", "template_roles.sdlc/task"),
            {(finding.code, finding.path) for finding in findings},
        )

    def test_a_duplicate_key_is_rejected(self) -> None:
        text = (ROOT / "docs/99.templates/registry.json").read_text(encoding="utf-8")
        duplicated = text.replace(
            '"purpose": ', '"purpose": "first",\n      "purpose": ', 1
        )
        self.assertNotEqual(text, duplicated)
        with tempfile.TemporaryDirectory() as temp:
            path = pathlib.Path(temp) / "registry.json"
            path.write_text(duplicated, encoding="utf-8")
            with self.assertRaisesRegex(RegistryError, "duplicate JSON member"):
                load_registry_document(path)

    def test_a_missing_dictionary_entry_is_rejected(self) -> None:
        raw = copy.deepcopy(dict(load_registry_document()))
        del raw["common"]["frontmatter_key_definitions"]["artifact_id"]
        del raw["common"]["table_column_definitions"]["Resolves"]
        codes = {(f.code, f.message) for f in validate_registry(raw)}
        self.assertIn(("template-key-undefined", "artifact_id"), codes)
        self.assertIn(("template-column-undefined", "Resolves"), codes)
        with tempfile.TemporaryDirectory() as temp:
            path = pathlib.Path(temp) / "registry.json"
            path.write_text(json.dumps(raw), encoding="utf-8")
            with self.assertRaisesRegex(
                RegistryError, "template-(key|column)-undefined"
            ):
                load_registry(path)
        raw = copy.deepcopy(dict(load_registry_document()))
        del raw["common"]["table_column_definitions"]["Resolves"]
        registry = _registry_from_document(raw, pathlib.PurePosixPath("registry.json"))
        # An unbound role reads its columns from the dictionary.
        with self.assertRaisesRegex(RegistryError, "Resolves"):
            template_definition(registry, "sdlc/task")

    def _common_form_roles(self, registry) -> list[str]:
        return [
            role
            for role, entry in registry.template_roles.items()
            if registry.profiles[entry["profiles"][0]].get("required_subsections")
            and not entry.get("core_role")
        ]

    def test_the_common_form_revision_is_read_from_the_registry(self) -> None:
        """H-W01-2: the consumer reads the adopted revision, not a constant."""

        pinned = self.registry.common["common_form_contract"]
        roles = self._common_form_roles(self.registry)
        self.assertTrue(roles)
        for role in roles:
            self.assertEqual(
                pinned["contract_id"], self.definitions[role]["contract_id"]
            )
            self.assertEqual(
                pinned["contract_version"], self.definitions[role]["contract_version"]
            )
        raw = copy.deepcopy(dict(load_registry_document()))
        raw["common"]["common_form_contract"]["contract_version"] = "9.9.9"
        moved = _registry_from_document(raw, pathlib.PurePosixPath("registry.json"))
        for role in roles:
            with self.subTest(role=role):
                self.assertEqual(
                    "9.9.9",
                    template_definition(moved, role)["contract_version"],
                )
        legacy = next(role for role in moved.template_roles if role not in set(roles))
        self.assertEqual(
            moved.common["contract_id"],
            template_definition(moved, legacy)["contract_id"],
        )
        self.assertEqual(
            moved.common["contract_version"],
            template_definition(moved, legacy)["contract_version"],
        )

    def test_template_outline_ignores_commented_headings_and_tables(self) -> None:
        from scripts.lib.document_governance.template_definition import (
            _template_outline,
        )

        guidance, tables = _template_outline(
            "## Parent\n\n### Child\n\nWrite the reason.\n\n"
            "<!-- An example\n## Fake\n| False header |\n-->\n\n"
            "Write the result.\n"
        )
        self.assertEqual(
            {
                ("Parent", None): "",
                ("Parent", "Child"): "Write the reason. Write the result.",
            },
            guidance,
        )
        self.assertEqual([], tables)

    def test_template_outline_ignores_list_nested_tables(self) -> None:
        from scripts.lib.document_governance.template_definition import (
            _template_outline,
        )

        _, tables = _template_outline(
            "## Parent\n\n- Example\n\n  | False | Header |\n"
            "  | --- | --- |\n  | a | b |\n\n"
            "| Real | Header |\n| --- | --- |\n| c | d |\n"
        )
        self.assertEqual([("Parent", None, "| Real | Header |")], tables)

    def test_template_outline_refuses_an_invalid_table_delimiter(self) -> None:
        from scripts.lib.document_governance.template_definition import (
            _template_outline,
        )

        for rows in ("", "| :--- |\n", "| --- | invalid |\n", "| \u00a0--- | --- |\n"):
            with self.subTest(rows=rows):
                with self.assertRaisesRegex(RegistryError, "table delimiter"):
                    _template_outline(f"## Parent\n\n| Left | Right |\n{rows}")

    def test_template_outline_accepts_delimiter_without_outer_pipes(self) -> None:
        from scripts.lib.document_governance.template_definition import (
            _template_outline,
        )

        guidance, tables = _template_outline(
            "## Parent\n\n| Left | Right |\n:--- | ---:\n| a | b |\n"
        )
        self.assertEqual({("Parent", None): ""}, guidance)
        self.assertEqual([("Parent", None, "| Left | Right |")], tables)

    def test_a_registry_without_the_pin_fails_for_a_common_form_role(self) -> None:
        raw = copy.deepcopy(dict(load_registry_document()))
        del raw["common"]["common_form_contract"]
        self.assertIn("schema-invalid", {f.code for f in validate_registry(raw)})
        bare = _registry_from_document(raw, pathlib.PurePosixPath("registry.json"))
        role = self._common_form_roles(bare)[0]
        with self.assertRaisesRegex(RegistryError, "common_form_contract"):
            template_definition(bare, role)

    def test_a_malformed_common_form_pin_is_rejected(self) -> None:
        for value in (
            "1.0.0",
            "COMMON-DOC-FORM-1",
            "COMMON-DOC-FORM-1/1.0",
            "COMMON-DOC-FORM-1 1.0.0",
            1,
            {"contract_id": "COMMON-DOC-FORM-1", "contract_version": "1.0.0\n"},
            {"contract_id": "COMMON-DOC-FORM-1", "contract_version": "1.0.0-rc.1"},
        ):
            raw = copy.deepcopy(dict(load_registry_document()))
            raw["common"]["common_form_contract"] = value
            with self.subTest(value=value):
                self.assertIn(
                    "schema-invalid", {f.code for f in validate_registry(raw)}
                )

    def test_unknown_role_and_missing_field_raise_registry_error(self) -> None:
        with self.assertRaises(RegistryError):
            template_definition(self.registry, "operations/release")
        raw = copy.deepcopy(dict(load_registry_document()))
        del raw["template_roles"]["sdlc/task"]["purpose"]
        registry = _registry_from_document(raw, pathlib.PurePosixPath("registry.json"))
        with self.assertRaisesRegex(RegistryError, "purpose"):
            template_definition(registry, "sdlc/task")


def _core_from(definition: dict) -> dict:
    """Build a core role with the exact structure of one projection."""

    def required(item: dict) -> str:
        return "always" if item["requiredness"] == "required" else "when applicable"

    sections = []
    for h2 in definition["headings"]:
        subsections = [
            {
                "section_id": h3["section_id"],
                "title_en": h3["title"],
                "required_when": required(h3),
            }
            for h3 in h2["children"]
        ]
        sections.append(
            {
                "section_id": h2["section_id"],
                "title_en": h2["title"],
                "required_when": required(h2),
                "subsections": subsections,
            }
        )
    tables = [
        {
            "table_id": table["name"],
            "section_id": table["section"],
            "columns": [
                {"label": column["key"], "required": column["required"]}
                for column in table["columns"]
            ],
        }
        for table in definition["tables"]
    ]
    return {"role": "fixture", "sections": sections, "tables": tables}


class RoleDesignConformanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        from scripts.lib.document_governance.template_definition import (
            role_design_findings,
        )

        cls.findings = staticmethod(role_design_findings)
        cls.registry = load_registry()
        cls.task = template_definition(cls.registry, "sdlc/task")

    def _codes(self, core_role: dict, definition: dict) -> set[str]:
        return {
            code
            for code, _, _ in self.findings(
                {"fixture": core_role},
                {"sdlc/task": "fixture"},
                {"sdlc/task": definition},
            )
        }

    def test_an_identical_projection_conforms(self) -> None:
        self.assertEqual(set(), self._codes(_core_from(self.task), self.task))

    def test_same_titles_with_a_different_table_do_not_conform(self) -> None:
        core = _core_from(self.task)
        core["tables"][0]["columns"][3]["label"] = "Method"
        self.assertIn("role-design-table-mismatch", self._codes(core, self.task))

    def test_a_different_subsection_does_not_conform(self) -> None:
        core = _core_from(self.task)
        core["sections"][0]["subsections"][0]["title_en"] = "Problem"
        self.assertIn("role-design-heading-mismatch", self._codes(core, self.task))

    def test_requiredness_is_part_of_the_core(self) -> None:
        core = _core_from(self.task)
        core["sections"][1]["required_when"] = "when applicable"
        self.assertIn("role-design-heading-mismatch", self._codes(core, self.task))

    def test_a_table_may_sit_in_an_h3_of_its_core_owned_h2(self) -> None:
        core = _core_from(self.task)
        owner = next(
            h2["section_id"]
            for h2 in self.task["headings"]
            if any(
                h3["section_id"] == self.task["tables"][0]["section"]
                for h3 in h2["children"]
            )
        )
        core["tables"][0]["section_id"] = owner
        self.assertEqual(set(), self._codes(core, self.task))

    def test_an_extra_or_missing_table_does_not_conform(self) -> None:
        extra = _core_from(self.task)
        extra["tables"].append(copy.deepcopy(extra["tables"][0]))
        missing = _core_from(self.task)
        missing["tables"].pop()
        for core in (extra, missing):
            with self.subTest(tables=len(core["tables"])):
                self.assertIn(
                    "role-design-table-mismatch", self._codes(core, self.task)
                )

    def test_h3_requiredness_is_part_of_the_core(self) -> None:
        core = _core_from(self.task)
        core["sections"][0]["subsections"][0]["required_when"] = "when applicable"
        self.assertIn("role-design-heading-mismatch", self._codes(core, self.task))

    def _registry_with(self, edit) -> object:
        raw = json.loads(
            (ROOT / "docs/99.templates/registry.json").read_text(encoding="utf-8")
        )
        edit(raw)
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "registry.json"
            path.write_text(json.dumps(raw), encoding="utf-8")
            return load_registry(path)

    def test_an_unknown_or_unmapped_core_role_is_reported(self) -> None:
        from scripts.lib.document_governance.template_definition import (
            role_design_contract_findings,
        )

        def rename(raw: dict) -> None:
            exception = raw["template_roles"]["sdlc/architecture-decision"][
                "core_exception"
            ]
            exception["core_role"] = "no-such-role"

        codes = {
            code
            for code, _, _ in role_design_contract_findings(self._registry_with(rename))
        }
        self.assertEqual(
            {"role-design-unknown-role", "role-design-core-unmapped"}, codes
        )

    def test_the_schema_owns_the_exception_shape(self) -> None:
        from scripts.lib.document_governance.registry import validate_registry

        raw = json.loads(
            (ROOT / "docs/99.templates/registry.json").read_text(encoding="utf-8")
        )
        cases = {
            "pending without a core role": lambda role: role["core_exception"].pop(
                "core_role"
            ),
            "domain with a core role": lambda role: role["core_exception"].update(
                kind="domain"
            ),
            "both fields": lambda role: role.update(core_role="decision"),
            "neither field": lambda role: role.pop("core_exception"),
        }
        for name, edit in cases.items():
            with self.subTest(case=name):
                changed = copy.deepcopy(raw)
                edit(changed["template_roles"]["sdlc/architecture-decision"])
                self.assertIn(
                    "schema-invalid",
                    {finding.code for finding in validate_registry(changed)},
                )

    def test_a_different_core_identity_is_rejected(self) -> None:
        from scripts.lib.document_governance.template_definition import (
            role_design_contract_findings,
        )

        def bump(raw: dict) -> None:
            raw["common"]["role_design_contract"]["contract_version"] = "4.0.1"

        codes = {
            code
            for code, _, _ in role_design_contract_findings(self._registry_with(bump))
        }
        self.assertEqual({"role-design-identity"}, codes)

    def test_the_incident_and_postmortem_forms_are_bound_and_conform(self) -> None:
        from scripts.lib.document_governance.template_definition import (
            role_design_contract_findings,
        )

        bound = {
            template_id: role.get("core_role")
            for template_id, role in self.registry.template_roles.items()
            if role.get("core_role")
        }
        self.assertEqual("incident", bound.get("operation/incident"))
        self.assertEqual("postmortem", bound.get("operation/postmortem"))
        self.assertEqual("runbook", bound.get("operation/runbook"))
        self.assertEqual("guide", bound.get("operation/guide"))
        self.assertEqual("policy", bound.get("operation/policy"))
        self.assertEqual("policy", bound.get("governance/policy"))
        self.assertEqual([], role_design_contract_findings(self.registry))

    def test_a_runbook_steps_table_reads_the_core_columns(self) -> None:
        definition = template_definition(self.registry, "operation/runbook")
        self.assertEqual("workspace-document-role-design", definition["contract_id"])
        self.assertEqual(
            [
                ("Step", "integer"),
                ("Action", "string"),
                ("Expected Result", "string"),
                ("On Failure", "string"),
            ],
            [
                (column["key"], column["data_type"])
                for column in definition["tables"][0]["columns"]
            ],
        )

    def test_a_bound_table_reads_its_columns_from_the_core(self) -> None:
        definition = template_definition(self.registry, "operation/postmortem")
        self.assertEqual("workspace-document-role-design", definition["contract_id"])
        self.assertEqual(
            [
                ("Action", "string"),
                ("Owner", "string"),
                ("Condition", "string"),
                ("Evidence", "reference-or-none"),
            ],
            [
                (column["key"], column["data_type"])
                for column in definition["tables"][0]["columns"]
            ],
        )

    def test_a_core_table_under_another_h2_is_rejected(self) -> None:
        role = self.registry.template_roles["operation/postmortem"]
        contract = self.registry.common["role_design_contract"]
        source = ROOT / str(role["source"])
        text = source.read_text(encoding="utf-8")
        table = "\n".join(line for line in text.split("\n") if line.startswith("|"))
        moved = text.replace(table + "\n", "").replace(
            "### Contributing Factors\n",
            "### Contributing Factors\n\n" + table + "\n",
            1,
        )
        self.assertNotEqual(text, moved)
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            for relative in (
                str(contract["source_path"]),
                str(role["source"]),
                "docs/99.templates/contracts/document-frontmatter.schema.json",
            ):
                (root / relative).parent.mkdir(parents=True, exist_ok=True)
                (root / relative).write_bytes((ROOT / relative).read_bytes())
            (root / str(role["source"])).write_text(moved, encoding="utf-8")
            with self.assertRaisesRegex(RegistryError, "not in the core role"):
                template_definition(self.registry, "operation/postmortem", root=root)

    def test_the_registry_pins_the_tracked_core(self) -> None:
        from scripts.lib.document_governance.template_definition import (
            role_design_contract_findings,
        )

        contract = self.registry.common["role_design_contract"]
        self.assertEqual("workspace-document-role-design", contract["contract_id"])
        self.assertEqual([], role_design_contract_findings(self.registry))

    def test_a_changed_core_or_schema_file_is_rejected(self) -> None:
        from scripts.lib.document_governance.template_definition import (
            role_design_contract_findings,
        )

        contract = self.registry.common["role_design_contract"]
        for changed in ("source_path", "schema_path"):
            with (
                self.subTest(changed=changed),
                tempfile.TemporaryDirectory() as directory,
            ):
                root = pathlib.Path(directory)
                for key in ("source_path", "schema_path"):
                    target = root / contract[key]
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes((ROOT / contract[key]).read_bytes())
                target = root / contract[changed]
                target.write_bytes(target.read_bytes() + b"\n")
                findings = role_design_contract_findings(self.registry, root=root)
                self.assertEqual(
                    [("role-design-source-changed", contract[changed])],
                    [(code, location) for code, location, _ in findings],
                )


if __name__ == "__main__":
    unittest.main()
