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
    load_registry,
    load_registry_document,
    template_definition,
    validate_registry,
)

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


class TemplateDefinitionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = load_registry()
        cls.definitions = {
            role: template_definition(cls.registry, role)
            for role in cls.registry.template_roles
        }

    def test_vendored_schema_is_the_approved_bytes(self) -> None:
        import hashlib

        digest = hashlib.sha256(SCHEMA_PATH.read_bytes()).hexdigest()
        self.assertTrue(digest.startswith("e490cf402419"), digest)

    def test_every_definition_validates_against_the_schema(self) -> None:
        self.assertEqual(39, len(self.definitions))
        for role, definition in self.definitions.items():
            with self.subTest(role=role):
                self.assertEqual([], _errors(definition))

    def test_headings_equal_the_profile_sections(self) -> None:
        for role, definition in self.definitions.items():
            profile = self.registry.profiles[
                self.registry.template_roles[role]["profiles"][0]
            ]
            if not profile.get("required_sections"):
                continue  # structural units; see test_headingless_templates_*
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
                    self.assertEqual(
                        [
                            *profile.get("required_subsections", {}).get(title, ()),
                            *profile.get("optional_subsections", {}).get(title, ()),
                        ],
                        [child["title"] for child in heading["children"]],
                    )

    def test_authored_references_resolve(self) -> None:
        glossary = GLOSSARY.read_text(encoding="utf-8")
        for role, definition in self.definitions.items():
            with self.subTest(role=role):
                for path in definition["consumer_paths"]:
                    self.assertTrue((ROOT / path).is_file(), path)
                for ref in definition["policy_refs"]:
                    path, _, anchor = ref.partition("#")
                    self.assertRegex(path, r"^\.agents/governance/[a-z-]+\.md$")
                    text = (ROOT / path).read_text(encoding="utf-8")
                    anchors = {
                        _slug(match)
                        for match in re.findall(r"^#{1,6} +(.+)$", text, re.M)
                    }
                    self.assertIn(anchor, anchors, ref)
                for term in definition["vocabulary_refs"]:
                    self.assertIn(f"| {term.removeprefix('local:')} |", glossary, term)
                for kind in ("positive", "negative", "regression"):
                    for name in definition["validation"][kind]:
                        module, _, attribute = name.partition(":")
                        loaded = importlib.import_module(module)
                        for part in filter(None, attribute.split(".")):
                            loaded = getattr(loaded, part)

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
        }
        for role, titles in expected.items():
            with self.subTest(role=role):
                self.assertEqual(
                    titles, [h["title"] for h in self.definitions[role]["headings"]]
                )
        claude = [
            h["title"] for h in self.definitions["governance/claude-agent"]["headings"]
        ]
        self.assertEqual("frontmatter name", claude[0])
        self.assertIn("H1 {{NAME}}", claude)
        self.assertIn("Body {{AGENT_BODY}}", claude)

    def test_empty_headings_are_rejected(self) -> None:
        definition = copy.deepcopy(self.definitions["sdlc/openapi"])
        definition["headings"] = []
        self.assertIn("headings: minItems", _errors(definition))

    def test_a_missing_required_field_is_rejected(self) -> None:
        definition = copy.deepcopy(self.definitions["sdlc/task"])
        del definition["purpose"]
        self.assertIn(": required", _errors(definition))

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


if __name__ == "__main__":
    unittest.main()
