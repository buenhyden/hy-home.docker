from __future__ import annotations

import copy
import hashlib
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

    def test_vendored_schema_is_the_approved_bytes(self) -> None:
        digest = hashlib.sha256(SCHEMA_PATH.read_bytes()).hexdigest()
        self.assertTrue(digest.startswith("e490cf402419"), digest)

    def test_every_definition_validates_against_the_schema(self) -> None:
        self.assertEqual(39, len(self.definitions))
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
            ("operation/runbook", "Rollback"): "when running the procedure or "
            "the change alters state or outputs",
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
            if h["title"] == "Recovery"
        )
        self.assertEqual(
            [("Rollback", 1), ("Escalation", 2)],
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
        # COMMON-DOC-FORM-1 1.0.0 gives every section of a role one role
        # rule; every H3 also forbids a stand-in heading.
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
        for role, definition in self.definitions.items():
            if not self._profile(role).get("required_subsections"):
                continue
            with self.subTest(role=role):
                for heading in definition["headings"]:
                    rules = heading["prohibited_content"]
                    self.assertEqual(3, len(rules), heading["title"])
                    self.assertIn("A heading with no body below it.", rules)
                    if role in role_rule:
                        self.assertEqual(role_rule[role], rules[0])
                    for child in heading["children"]:
                        self.assertEqual(
                            [*rules, stand_in], child["prohibited_content"]
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
        del raw["common"]["table_column_definitions"]["Tracking ID"]
        registry = _registry_from_document(raw, pathlib.PurePosixPath("registry.json"))
        with self.assertRaisesRegex(RegistryError, "Tracking ID"):
            template_definition(registry, "operation/postmortem")

    def test_unknown_role_and_missing_field_raise_registry_error(self) -> None:
        with self.assertRaises(RegistryError):
            template_definition(self.registry, "operations/release")
        raw = copy.deepcopy(dict(load_registry_document()))
        del raw["template_roles"]["sdlc/task"]["purpose"]
        registry = _registry_from_document(raw, pathlib.PurePosixPath("registry.json"))
        with self.assertRaisesRegex(RegistryError, "purpose"):
            template_definition(registry, "sdlc/task")


if __name__ == "__main__":
    unittest.main()
