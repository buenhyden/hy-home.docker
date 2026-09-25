"""Heading and body-contract tests."""

from __future__ import annotations

import json
import os
import pathlib
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from jsonschema import Draft202012Validator

from scripts.lib.document_governance.metadata import heading as heading_module
from scripts.lib.document_governance.registry import classify_path
from tests.lib.document_governance.metadata._support import (
    POLICY_TARGET_BODY,
    REQUIREMENT_TARGET_BODY,
    ROOT,
    body_with_headings,
    copy_registry_contract_fixture,
    current_profiles,
    git,
    metadata,
    run_checker,
)
from tests.lib.gate.subprocess_support import gate_root_pass_fds


class CurrentBodyContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.profiles = current_profiles()

    def requirement_record(self) -> object:
        return metadata.Record(
            pathlib.Path("docs/01.requirements/0001-body-fixture.md"),
            {
                "profile_id": "requirements-package",
                "status": "active",
                "artifact_id": "REQ-0001",
                "artifact_type": "requirements-package",
                "parent_ids": [],
                "created": "2026-08-01",
                "updated": "2026-08-01",
            },
            "requirements-package",
            frontmatter_present=True,
        )

    def introduced(
        self,
        current_body: str,
        base_body: str | None,
    ) -> list[object]:
        record = self.requirement_record()
        return metadata._introduced_body_findings(
            record,
            current_body,
            record if base_body is not None else None,
            base_body,
            self.profiles,
        )

    def test_identical_body_deficit_multiset_is_preserved(self) -> None:
        body = REQUIREMENT_TARGET_BODY + "\n{{EXISTING_TOKEN}}\n"
        self.assertEqual([], self.introduced(body + "\nEditorial text.\n", body))

    def test_additional_body_token_is_blocked_without_value_leakage(self) -> None:
        base = REQUIREMENT_TARGET_BODY + "\n{{EXISTING_TOKEN}}\n"
        findings = self.introduced(base + "\n{{ADDITIONAL_TOKEN}}\n", base)
        self.assertEqual(
            ["template-body-token-in-target"], [item.code for item in findings]
        )
        rendered = "\n".join(item.message for item in findings)
        self.assertNotIn("EXISTING_TOKEN", rendered)
        self.assertNotIn("ADDITIONAL_TOKEN", rendered)

    def test_replaced_body_token_is_a_new_private_deficit(self) -> None:
        findings = self.introduced(
            REQUIREMENT_TARGET_BODY + "\n{{REPLACEMENT_TOKEN}}\n",
            REQUIREMENT_TARGET_BODY + "\n{{ORIGINAL_TOKEN}}\n",
        )
        self.assertEqual(
            ["template-body-token-in-target"], [item.code for item in findings]
        )
        rendered = "\n".join(item.message for item in findings)
        self.assertNotIn("ORIGINAL_TOKEN", rendered)
        self.assertNotIn("REPLACEMENT_TOKEN", rendered)

    def test_new_instruction_is_blocked_without_literal_echo(self) -> None:
        findings = self.introduced(
            REQUIREMENT_TARGET_BODY + "\n> Rules:\n",
            REQUIREMENT_TARGET_BODY,
        )
        self.assertEqual(
            ["template-instruction-in-target"], [item.code for item in findings]
        )
        self.assertNotIn("> Rules:", "\n".join(item.message for item in findings))

    def test_new_file_body_deficit_is_blocked(self) -> None:
        findings = self.introduced(
            REQUIREMENT_TARGET_BODY + "\n{{NEW_FILE_TOKEN}}\n",
            None,
        )
        self.assertEqual(
            ["template-body-token-in-target"], [item.code for item in findings]
        )

    def test_current_operations_policy_preserves_its_own_body_baseline(self) -> None:
        record = metadata.Record(
            pathlib.Path(
                "docs/05.operations/policies/"
                "0001-common-optimizations-template-exceptions.md"
            ),
            {
                "title": "Common Optimizations Template Exceptions",
                "type": "operation/policy",
                "layer": "operations",
                "status": "active",
                "owner": "@buenhyden",
                "artifact_id": "POL-0001",
                "parent_ids": [],
                "created": "2026-08-01",
                "updated": "2026-08-01",
            },
            "policy",
            frontmatter_present=True,
        )
        body = POLICY_TARGET_BODY + "\n> Rules:\n"
        self.assertEqual(
            [],
            metadata._introduced_body_findings(
                record,
                body + "\nEditorial text.\n",
                record,
                body,
                self.profiles,
            ),
        )

    def test_policy_optional_and_additional_fields_follow_the_registry(self) -> None:
        base = {
            "title": "Common Optimizations Template Exceptions",
            "version": "1.0.0",
            "type": "operation/policy",
            "status": "active",
            "owner": "@buenhyden",
            "updated": "2026-08-01",
            "layer": "operations",
            "artifact_id": "POL-0001",
            "parent_ids": [],
            "created": "2026-08-01",
        }

        def findings(extra: dict[str, object]) -> list[object]:
            record = metadata.Record(
                pathlib.Path(
                    "docs/05.operations/policies/"
                    "0001-common-optimizations-template-exceptions.md"
                ),
                {**base, **extra},
                "policy",
                frontmatter_present=True,
            )
            return metadata.validate_record(
                record,
                self.profiles,
                metadata.build_manifest([record]),
            )

        self.assertEqual([], findings({"reviewed_at": "2026-08-02"}))
        self.assertIn(
            "type-inappropriate-key",
            {item.code for item in findings({"undeclared_key": "value"})},
        )

    def test_commonmark_code_hides_template_residue(self) -> None:
        cases = (
            "```markdown\n> Rules:\n{{FENCED_TOKEN}}\n```\n",
            "~~~markdown\n> Rules:\n{{FENCED_TOKEN}}\n~~~\n",
            "```markdown\n> Rules:\n{{FENCED_TOKEN}}\n",
            "Document `> Rules:` and `{{INLINE_TOKEN}}`.\n",
        )
        for example in cases:
            with self.subTest(example=example.splitlines()[0]):
                self.assertEqual(
                    [],
                    self.introduced(
                        REQUIREMENT_TARGET_BODY + "\n" + example,
                        REQUIREMENT_TARGET_BODY,
                    ),
                )

    def test_residue_outside_commonmark_code_is_blocked(self) -> None:
        body = (
            REQUIREMENT_TARGET_BODY
            + "\n```markdown\n{{FENCED_TOKEN}}\n```\n"
            + "Document `{{INLINE_TOKEN}}`.\n"
            + "{{OUTSIDE_TOKEN}}\n"
        )
        self.assertEqual(
            ["template-body-token-in-target"],
            [item.code for item in self.introduced(body, REQUIREMENT_TARGET_BODY)],
        )


class RegisteredSectionContractTests(unittest.TestCase):
    """Every profile that declares sections has them enforced.

    A profile that also registered a template used to be exempt from the
    Registry section check and was covered only by its template role, which
    runs on changed paths alone. Twenty-eight of the twenty-nine profiles
    declaring a section contract carry a `template_id`, so the contract was
    declared and never applied to the documents it governs.
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.profiles = current_profiles()
        cls.registry = cls.profiles["_registry"]
        cls.representatives = cls._representative_paths()

    @classmethod
    def _representative_paths(cls) -> dict[str, pathlib.Path]:
        """Map each enforced profile to one tracked document that carries it."""

        tracked = subprocess.run(
            ["git", "ls-files", "docs"],
            capture_output=True,
            text=True,
            check=True,
            cwd=ROOT,
        ).stdout.split()
        found: dict[str, pathlib.Path] = {}
        for candidate in tracked:
            if not candidate.endswith(".md"):
                continue
            profile_id = classify_path(candidate, cls.registry)
            if profile_id is None or profile_id in found:
                continue
            profile = cls.registry.profiles.get(profile_id, {})
            if profile.get("required_sections") and not profile.get(
                "free_form_sections"
            ):
                found[profile_id] = pathlib.Path(candidate)
        return found

    def _findings(self, profile_id: str, body: str) -> list[str]:
        record = metadata.Record(
            self.representatives[profile_id],
            {"artifact_type": profile_id, "status": "active"},
            profile_id,
            frontmatter_present=True,
        )
        return [
            item.code
            for item in heading_module.validate_body_contract(
                record, body, self.profiles, False
            )
        ]

    def _conforming_body(self, profile_id: str) -> tuple[str, tuple[str, ...]]:
        required = tuple(
            self.registry.profiles[profile_id].get("required_sections", ())
        )
        return body_with_headings(*(f"## {name}" for name in required)), required

    def test_every_declaring_profile_accepts_its_own_contract(self) -> None:
        self.assertTrue(self.representatives, "no enforced profile has a document")
        for profile_id in sorted(self.representatives):
            with self.subTest(profile=profile_id):
                body, _ = self._conforming_body(profile_id)
                self.assertEqual([], self._findings(profile_id, body))

    def test_a_missing_required_section_is_reported(self) -> None:
        for profile_id in sorted(self.representatives):
            with self.subTest(profile=profile_id):
                _, required = self._conforming_body(profile_id)
                body = body_with_headings(*(f"## {name}" for name in required[:-1]))
                self.assertIn("body-heading-missing", self._findings(profile_id, body))

    def test_an_unregistered_section_is_reported(self) -> None:
        for profile_id in sorted(self.representatives):
            with self.subTest(profile=profile_id):
                body, _ = self._conforming_body(profile_id)
                body += "\n## Totally Unregistered Heading\n\nFixture content.\n"
                self.assertIn(
                    "body-heading-forbidden", self._findings(profile_id, body)
                )

    def test_a_repeated_section_is_reported(self) -> None:
        for profile_id in sorted(self.representatives):
            with self.subTest(profile=profile_id):
                body, required = self._conforming_body(profile_id)
                body += f"\n## {required[0]}\n\nFixture content.\n"
                self.assertIn(
                    "body-heading-duplicate", self._findings(profile_id, body)
                )

    def test_a_second_h1_is_reported(self) -> None:
        for profile_id in sorted(self.representatives):
            with self.subTest(profile=profile_id):
                body, _ = self._conforming_body(profile_id)
                self.assertIn(
                    "body-h1-count", self._findings(profile_id, body + "\n# Second\n")
                )


class TemplateAndAuthoredResidueTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.profiles = current_profiles()
        cls.spec_path = pathlib.Path("docs/03.specs/0001-residue-fixture/spec.md")
        required_sections = cls.profiles["_registry"].profiles["spec"][
            "required_sections"
        ]
        cls.spec_text = body_with_headings(
            *(f"## {section}" for section in required_sections)
        )
        cls.spec_record = metadata.Record(
            cls.spec_path,
            {
                "title": "Residue Fixture",
                "version": "1.0.0",
                "type": "sdlc/spec",
                "status": "active",
                "owner": "@fixture",
                "updated": "2026-08-01",
                "layer": "specs",
                "artifact_id": "SPEC-0001",
                "parent_ids": [],
                "created": "2026-08-01",
            },
            "spec",
            frontmatter_present=True,
        )
        cls.template_path = pathlib.Path(
            "docs/99.templates/templates/specs/spec.template.md"
        )
        cls.template_values = heading_module._parse_frontmatter_text(
            (ROOT / cls.template_path).read_text(encoding="utf-8")
        )

    def template_codes(self, values: dict[str, object]) -> set[str]:
        record = metadata.Record(
            self.template_path, values, "template-source", frontmatter_present=True
        )
        return {
            item.code
            for item in heading_module._validate_template_source(record, self.profiles)
        }

    def test_template_rejects_unknown_placeholder_without_key_mapping(self) -> None:
        self.assertNotIn(
            "next_review_at", self.profiles["common"]["template_placeholders"]
        )
        self.assertIn(
            "invalid-template-placeholder",
            self.template_codes(
                {**self.template_values, "next_review_at": "{{UNREGISTERED_VALUE}}"}
            ),
        )

    def test_incident_template_uses_registered_timestamp_placeholder(self) -> None:
        path = pathlib.Path(
            "docs/99.templates/templates/operations/incident.template.md"
        )
        values = heading_module._parse_frontmatter_text(
            (ROOT / path).read_text(encoding="utf-8")
        )
        self.assertEqual(
            self.profiles["common"]["template_placeholders"]["occurred_at"],
            values["occurred_at"],
        )
        record = metadata.Record(
            path, values, "template-source", frontmatter_present=True
        )
        self.assertEqual(
            [], heading_module._validate_template_source(record, self.profiles)
        )

    def test_shared_router_template_retains_registered_layer_placeholder(self) -> None:
        path = pathlib.Path(
            "docs/99.templates/templates/common/readme-stage.template.md"
        )
        values = heading_module._parse_frontmatter_text(
            (ROOT / path).read_text(encoding="utf-8")
        )
        self.assertEqual(
            self.profiles["common"]["template_placeholders"]["layer"], values["layer"]
        )
        record = metadata.Record(
            path, values, "template-source", frontmatter_present=True
        )
        self.assertEqual(
            [], heading_module._validate_template_source(record, self.profiles)
        )

    def test_template_rejects_wrong_or_placeholder_layer(self) -> None:
        for layer in ("wrong-layer", "{{LAYER}}"):
            with self.subTest(layer=layer):
                self.assertIn(
                    "frontmatter-value-invalid",
                    self.template_codes({**self.template_values, "layer": layer}),
                )

    def test_template_literals_follow_profile_data_without_parallel_taxonomy(
        self,
    ) -> None:
        profiles = current_profiles()
        profiles["profiles"]["spec"]["frontmatter_values"] = {"layer": "fixture-layer"}
        values = {**self.template_values, "layer": "fixture-layer"}
        record = metadata.Record(
            self.template_path, values, "template-source", frontmatter_present=True
        )
        self.assertEqual([], heading_module._validate_template_source(record, profiles))

    def test_template_rejects_key_order_concrete_identity_and_bad_version(self) -> None:
        cases = (
            (dict(reversed(tuple(self.template_values.items()))), "frontmatter-order"),
            (
                {**self.template_values, "artifact_id": "SPEC-0001"},
                "invalid-template-placeholder",
            ),
            (
                {**self.template_values, "version": "not-semver"},
                "frontmatter-schema-invalid",
            ),
            ({**self.template_values, "version": "1.0.0"}, "invalid-template-version"),
        )
        for values, code in cases:
            with self.subTest(code=code):
                self.assertIn(code, self.template_codes(values))
        self.assertEqual(set(), self.template_codes(dict(self.template_values)))

    def test_author_prompt_and_token_are_rejected_in_full_and_changed_modes(
        self,
    ) -> None:
        cases = (
            (
                "<!-- Author prompt: Fill this section. -->",
                "template-instruction-in-target",
            ),
            ("{{UNFILLED_BODY}}", "template-body-token-in-target"),
        )
        for changed in (False, True):
            for residue, code in cases:
                with self.subTest(changed=changed, code=code):
                    findings = heading_module.validate_body_contract(
                        self.spec_record,
                        self.spec_text + "\n" + residue + "\n",
                        self.profiles,
                        changed,
                    )
                    self.assertIn(code, {item.code for item in findings})
                    self.assertNotIn(
                        residue, "\n".join(item.message for item in findings)
                    )

    def test_residue_examples_are_not_unfilled_authored_content(self) -> None:
        examples = (
            "`<!-- Author prompt: Example. -->` and `{{BODY_TOKEN}}`.",
            "```markdown\n<!-- Author prompt: Example. -->\n{{BODY_TOKEN}}\n```",
            "> <!-- Author prompt: Example. -->\n> {{BODY_TOKEN}}",
        )
        for changed in (False, True):
            for example in examples:
                with self.subTest(changed=changed, example=example):
                    findings = heading_module.validate_body_contract(
                        self.spec_record,
                        self.spec_text + "\n" + example + "\n",
                        self.profiles,
                        changed,
                    )
                    self.assertFalse(
                        {
                            "template-instruction-in-target",
                            "template-body-token-in-target",
                        }
                        & {item.code for item in findings}
                    )

    def test_current_non_sdlc_authored_document_rejects_residue(self) -> None:
        path = pathlib.Path(".agents/governance/documentation-protocol.md")
        text = (ROOT / path).read_text(encoding="utf-8")
        record = metadata.Record(
            path,
            heading_module._parse_frontmatter_text(text),
            classify_path(path.as_posix(), self.profiles["_registry"]),
            frontmatter_present=True,
        )
        findings = heading_module.validate_body_contract(
            record,
            text + "\n<!-- Author prompt: Fill this. -->\n{{UNFILLED}}\n",
            self.profiles,
            False,
        )
        self.assertTrue(
            {"template-instruction-in-target", "template-body-token-in-target"}
            <= {item.code for item in findings}
        )

    def test_native_frozen_generated_and_template_bodies_keep_their_exemptions(
        self,
    ) -> None:
        registry = self.profiles["_registry"]
        paths = (
            "docs/99.templates/templates/runtime/claude-agent.template.md",
            "docs/03.specs/0001-example/contracts/openapi.yaml",
            "docs/98.archive/retired/03.specs/0001-example/spec.md",
            "docs/90.references/data/0066-foundation-summary/README.md",
        )
        for relative in paths:
            with self.subTest(path=relative):
                profile_id = classify_path(relative, registry)
                self.assertIsNotNone(profile_id)
                values = {}
                owner = heading_module.registered_generated_owner(
                    pathlib.Path(relative), self.profiles
                )
                if owner is not None:
                    values["generated_by"] = owner
                record = metadata.Record(pathlib.Path(relative), values, profile_id)
                findings = heading_module.validate_body_contract(
                    record,
                    "# Example\n\n<!-- Author prompt: Example. -->\n{{BODY_TOKEN}}\n",
                    self.profiles,
                    False,
                )
                self.assertFalse(
                    {"template-instruction-in-target", "template-body-token-in-target"}
                    & {item.code for item in findings}
                )
        template = metadata.Record(
            self.template_path,
            dict(self.template_values),
            "template-source",
            frontmatter_present=True,
        )
        findings = heading_module.validate_body_contract(
            template,
            (ROOT / self.template_path).read_text(encoding="utf-8"),
            self.profiles,
            False,
        )
        self.assertFalse(
            {"template-instruction-in-target", "template-body-token-in-target"}
            & {item.code for item in findings}
        )

    def test_changed_author_prompt_deficits_are_private_and_counted(self) -> None:
        original = self.spec_text + "\n<!-- Author prompt: Original prompt. -->\n"
        replacement = self.spec_text + "\n<!-- Author prompt: Replacement prompt. -->\n"
        self.assertEqual(
            [],
            heading_module._introduced_body_findings(
                self.spec_record,
                original + "\nEditorial change.\n",
                self.spec_record,
                original,
                self.profiles,
            ),
        )
        findings = heading_module._introduced_body_findings(
            self.spec_record, replacement, self.spec_record, original, self.profiles
        )
        self.assertEqual(
            ["template-instruction-in-target"], [item.code for item in findings]
        )
        self.assertNotIn(
            "Replacement prompt", "\n".join(item.message for item in findings)
        )


class RegistrySchemaBoundaryTests(unittest.TestCase):
    def test_current_registry_is_accepted_by_schema(self) -> None:
        self.assertEqual([], self.schema_errors(lambda raw: None))

    def schema_errors(self, mutate) -> list[object]:
        raw = json.loads(
            (ROOT / "docs/99.templates/registry.json").read_text(encoding="utf-8")
        )
        schema = json.loads(
            (
                ROOT / "docs/99.templates/contracts/document-profile.schema.json"
            ).read_text(encoding="utf-8")
        )
        mutate(raw)
        return list(Draft202012Validator(schema).iter_errors(raw))

    def test_unknown_common_property_is_rejected_by_schema(self) -> None:
        errors = self.schema_errors(
            lambda raw: raw["common"].update(unknown_common_policy=True)
        )
        self.assertTrue(
            any(
                list(error.path) == ["common"]
                and error.validator == "additionalProperties"
                for error in errors
            )
        )

    def test_common_value_types_are_enforced_by_schema(self) -> None:
        for key, value in (
            ("template_placeholders", []),
            ("frontmatter_order", "title"),
            ("generated_outputs", []),
        ):
            with self.subTest(key=key):
                errors = self.schema_errors(
                    lambda raw: raw["common"].update({key: value})
                )
                self.assertTrue(
                    any(list(error.path)[:2] == ["common", key] for error in errors)
                )

    def test_unknown_exception_kind_is_rejected_by_schema(self) -> None:
        errors = self.schema_errors(
            lambda raw: raw["profiles"][0]["exceptions"].append(
                {"kind": "unregistered-exemption"}
            )
        )
        self.assertTrue(any("exceptions" in error.path for error in errors))


_ROUTE_SECTIONS = ("Retired Path", "Successor", "Reason", "Traceability")
_SEALED_SECTIONS = (
    "Retired Path",
    "Replacement",
    "Reason",
    "Recovery Commit",
    "Traceability",
)
_TOMBSTONE_PROFILE = {
    "required_sections": list(_ROUTE_SECTIONS),
    "optional_sections": ["Related Documents"],
    "sealed_section_shapes": [list(_SEALED_SECTIONS)],
}


class SealedSectionShapeTests(unittest.TestCase):
    """A sealed section shape is admitted for a record present at the base only.

    The changed check subtracts the base record's deficits from the current
    record's, so a sealed-shape deficit raised only at the changed boundary
    cancels for a record the base already held and remains for an added one.
    """

    _NEW_SHAPE = _ROUTE_SECTIONS
    _SEALED_SHAPE = _SEALED_SECTIONS

    def codes(self, headings: tuple[str, ...], changed_boundary: bool) -> list[str]:
        record = metadata.Record(
            pathlib.Path("docs/98.archive/tombstones/01.requirements/0001-example.md"),
            {"artifact_type": "tombstone", "status": "sealed"},
            "tombstone",
            frontmatter_present=True,
        )
        body = body_with_headings(*(f"## {heading}" for heading in headings))
        return [
            finding.code
            for finding in heading_module._registered_section_findings(
                record, body, _TOMBSTONE_PROFILE, changed_boundary
            )
        ]

    def test_the_new_shape_passes_at_every_boundary(self) -> None:
        for changed_boundary in (False, True):
            with self.subTest(changed_boundary=changed_boundary):
                self.assertEqual([], self.codes(self._NEW_SHAPE, changed_boundary))

    def test_a_sealed_shape_is_a_deficit_only_at_the_changed_boundary(self) -> None:
        self.assertEqual([], self.codes(self._SEALED_SHAPE, False))
        self.assertEqual(["body-sealed-shape"], self.codes(self._SEALED_SHAPE, True))

    def test_a_shape_matching_neither_is_still_reported(self) -> None:
        self.assertIn(
            "body-heading-missing", self.codes(("Retired Path", "Reason"), False)
        )

    def test_a_migration_keeps_its_sealed_shape_the_same_way(self) -> None:
        profile = {
            "required_sections": [
                "Purpose",
                "Moved Scope",
                "Current Owner",
                "Approval",
                "Traceability",
            ],
            "optional_sections": ["Related Documents"],
            "sealed_section_shapes": [
                [
                    "Purpose",
                    "Authority Change",
                    "Path Mapping",
                    "Recovery",
                    "Approval",
                    "Traceability",
                ]
            ],
        }
        record = metadata.Record(
            pathlib.Path("docs/98.archive/migrations/0004-example.md"),
            {"artifact_type": "migration", "status": "sealed"},
            "migration",
            frontmatter_present=True,
        )
        for headings, changed_boundary, expected in (
            (profile["required_sections"], True, []),
            (profile["sealed_section_shapes"][0], False, []),
            (profile["sealed_section_shapes"][0], True, ["body-sealed-shape"]),
        ):
            with self.subTest(headings=headings[1], changed=changed_boundary):
                body = body_with_headings(*(f"## {name}" for name in headings))
                self.assertEqual(
                    expected,
                    [
                        finding.code
                        for finding in heading_module._registered_section_findings(
                            record, body, profile, changed_boundary
                        )
                    ],
                )

    def test_sealed_shapes_are_registered_only_once_the_model_is_adopted(self) -> None:
        """The shape lists move with the switch, so the rule is inert at transition."""

        from scripts.lib.document_governance.registry import (
            ARCHIVE_MODEL_ADOPTED,
            archive_disposition_model,
            load_registry,
        )

        registry = load_registry()
        adopted = archive_disposition_model(ROOT) == ARCHIVE_MODEL_ADOPTED
        for profile_id in ("tombstone", "migration"):
            with self.subTest(profile=profile_id):
                shapes = registry.profiles[profile_id]["sealed_section_shapes"]
                self.assertEqual(adopted, bool(shapes))
                self.assertTrue(all(shape for shape in shapes))

    def test_the_changed_check_rejects_only_an_added_sealed_shape_record(self) -> None:
        """End to end through the base subtraction, with a shape registered."""

        import tempfile

        registry_source = json.loads(
            (ROOT / "docs/99.templates/registry.json").read_text(encoding="utf-8")
        )
        for profile in registry_source["profiles"]:
            if profile["id"] == "tombstone":
                profile["required_sections"] = list(self._NEW_SHAPE)
                profile["sealed_section_shapes"] = [list(self._SEALED_SHAPE)]
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "registry.json"
            path.write_text(json.dumps(registry_source), encoding="utf-8")
            profiles = metadata.build_registry_profiles(metadata.load_registry(path))
        record = metadata.Record(
            pathlib.Path("docs/98.archive/tombstones/01.requirements/0001-example.md"),
            {"artifact_type": "tombstone", "status": "sealed"},
            "tombstone",
            frontmatter_present=True,
        )
        body = body_with_headings(*(f"## {name}" for name in self._SEALED_SHAPE))

        def codes(base_record: object, base_text: str | None) -> list[str]:
            return [
                finding.code
                for finding in heading_module._introduced_body_findings(
                    record, body, base_record, base_text, profiles
                )
            ]

        self.assertIn("body-sealed-shape", codes(None, None))
        self.assertNotIn("body-sealed-shape", codes(record, body))


class RuntimeVersionBodyTests(unittest.TestCase):
    ENTRIES = (
        {
            "component": "ExampleDB",
            "images": ["vendor/exampledb:4.2.3"],
            "compose_files": ["infra/04-data/exampledb/docker-compose.yml"],
            "direct_source": True,
        },
    )
    POINTER = "[Runtime declaration](docker-compose.yml)\n"

    def findings(self, body, path="infra/04-data/exampledb/README.md"):
        record = metadata.Record(pathlib.Path(path), {}, "common/readme")
        with patch.object(
            heading_module,
            "_runtime_version_entries",
            return_value=self.ENTRIES,
            create=True,
        ):
            return [
                finding
                for finding in metadata.validate_body_contract(
                    record, body, {"profiles": {}}, False
                )
                if finding.code.startswith("runtime-version-")
            ]

    def test_runtime_docs_require_an_actual_authority_link(self) -> None:
        self.assertEqual([], self.findings(self.POINTER + "ExampleDB service.\n"))
        for body in (
            "ExampleDB service.\n",
            "Runtime authority: `infra/tech-stack.versions.json`\n",
            "[Runtime](https://unrelated.example/docker-compose.yml)\n",
            "[Runtime](../unrelated/docker-compose.yml)\n",
            "<!-- [Runtime](docker-compose.yml) -->\n",
            "```markdown\n[Runtime](docker-compose.yml)\n```\n",
        ):
            with self.subTest(body=body):
                self.assertIn(
                    "runtime-version-source-missing",
                    {f.code for f in self.findings(body)},
                )

    def test_current_and_stale_patch_literals_are_both_rejected(self) -> None:
        for literal in (
            "vendor/exampledb:4.2.3",
            "vendor/exampledb:3.9.8",
            "ExampleDB 4.2.3",
            "ExampleDB 3.9.8",
            "Version: 3.9.8",
            "Document version: 1.0.0; ExampleDB 3.9.8",
        ):
            with self.subTest(literal=literal):
                self.assertIn(
                    "runtime-version-literal",
                    {f.code for f in self.findings(self.POINTER + literal)},
                )

    def test_reasoned_exceptions_are_scoped_to_their_own_line(self) -> None:
        for category in (
            "migration",
            "compatibility",
            "advisory",
            "workaround",
            "history",
        ):
            with self.subTest(category=category):
                exception = (
                    "ExampleDB 3.9.8 "
                    f"<!-- runtime-version-exception: {category} — explains the affected restore format -->\n"
                )
                self.assertEqual([], self.findings(self.POINTER + exception))
                self.assertIn(
                    "runtime-version-literal",
                    {
                        f.code
                        for f in self.findings(
                            self.POINTER + exception + "ExampleDB 4.2.3\n"
                        )
                    },
                )

    def test_invalid_or_reasonless_exceptions_do_not_hide_stale_pins(self) -> None:
        for marker in (
            "<!-- runtime-version-exception: compatibility — -->",
            "<!-- runtime-version-exception: anything — rationale -->",
            "<!-- runtime-version-exception: history -->",
        ):
            with self.subTest(marker=marker):
                self.assertIn(
                    "runtime-version-literal",
                    {
                        f.code
                        for f in self.findings(
                            self.POINTER + "ExampleDB 3.9.8 " + marker
                        )
                    },
                )

    def test_frontmatter_and_explicit_document_versions_are_not_runtime_pins(
        self,
    ) -> None:
        text = "---\nversion: 4.2.3\n---\n" + self.POINTER + "Document version: 4.2.3\n"
        self.assertEqual([], self.findings(text))
        self.assertEqual(
            [], self.findings("Document version: 7.8.9\n", "infra/navigation/README.md")
        )

    def test_runtime_endpoint_ipv4_is_not_a_version_literal(self) -> None:
        for endpoint in (
            "http://127.0.0.1:3100/ready",
            "/dev/tcp/127.0.0.1/9000",
            "127.0.0.1:${EXAMPLE_PORT}",
            "172.19.0.2",
        ):
            with self.subTest(endpoint=endpoint):
                self.assertEqual(
                    [], self.findings(self.POINTER + "ExampleDB health: " + endpoint)
                )

    def test_frozen_archive_and_nonruntime_guides_are_outside_scope(self) -> None:
        for path in (
            "docs/98.archive/legacy/README.md",
            "docs/05.operations/guides/0001-editing.md",
        ):
            with self.subTest(path=path):
                self.assertEqual([], self.findings("Document revision 7.8.9", path))
        self.assertEqual(
            [], self.findings("ExampleDB 3.9.8", "docs/98.archive/legacy/README.md")
        )

    def test_operation_component_slug_uses_authored_source_authority(self) -> None:
        path = "docs/05.operations/guides/0001-exampledb.md"
        pointer = "[Runtime](/infra/04-data/exampledb/docker-compose.yml)\n"
        self.assertEqual([], self.findings(pointer + "Connection setup.", path))
        self.assertIn(
            "runtime-version-literal",
            {f.code for f in self.findings(pointer + "ExampleDB 3.9.8", path)},
        )
        self.assertEqual(
            [],
            self.findings(
                "[Projection](/infra/tech-stack.versions.json)\nConnection setup.",
                path,
            ),
        )

    def test_real_active_cli_rejects_runtime_pin_and_accepts_authority_link(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            profiles = copy_registry_contract_fixture(root)
            registry = root / "infra/tech-stack.versions.json"
            registry.parent.mkdir(parents=True)
            registry.write_text(json.dumps({"entries": list(self.ENTRIES)}))
            document = root / "docs/05.operations/policies/9999-exampledb.md"
            document.parent.mkdir(parents=True)
            source = root / "infra/04-data/exampledb/docker-compose.yml"
            source.parent.mkdir(parents=True)
            source.write_text(
                "services:\n  exampledb:\n    image: vendor/exampledb:4.2.3\n"
            )
            frontmatter = (
                '---\ntitle: "ExampleDB"\nversion: "1.0.0"\n'
                'type: "operation/policy"\nstatus: "active"\n'
                'owner: "@fixture"\nupdated: "2026-09-19"\n'
                'layer: "operations"\nartifact_id: "POL-9999"\nparent_ids: []\n'
                'created: "2026-09-19"\n---\n\n# ExampleDB\n\n'
            )
            pointer = "[Runtime](/infra/04-data/exampledb/docker-compose.yml)\n"
            document.write_text(frontmatter + pointer + "ExampleDB 3.9.8\n")
            self.assertEqual(0, git(root, "add", ".").returncode)
            result = run_checker(root, "check-active", profiles=profiles)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn("runtime-version-literal", result.stdout)
            document.write_text(frontmatter + pointer + "Connection setup.\n")
            result = run_checker(root, "check-active", profiles=profiles)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)

            runtime_readme = root / "infra/04-data/exampledb/README.md"
            runtime_readme.parent.mkdir(parents=True, exist_ok=True)
            readme_metadata = frontmatter.replace(
                'type: "operation/policy"', 'type: "common/package-readme"'
            )
            readme_metadata = readme_metadata.replace(
                'layer: "operations"\nartifact_id: "POL-9999"\nparent_ids: []\n', ""
            )
            runtime_readme.write_text(readme_metadata + pointer + "ExampleDB 3.9.8\n")
            unrelated = runtime_readme.parent / "private-config.md"
            unrelated.write_text("---\ninvalid: [\n")
            self.assertEqual(0, git(root, "add", ".").returncode)
            untracked = root / "infra/untracked/README.md"
            untracked.parent.mkdir(parents=True)
            untracked.write_text("---\ninvalid: [\n")
            result = run_checker(root, "check-active", profiles=profiles)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn(
                "infra/04-data/exampledb/README.md: runtime-version-literal",
                result.stdout,
            )
            runtime_readme.write_text(readme_metadata + pointer + "Connection setup.\n")
            result = run_checker(root, "check-active", profiles=profiles)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_active_general_readmes_and_architecture_decisions_are_checked(
        self,
    ) -> None:
        text = "[Runtime](/infra/tech-stack.versions.json)\nExampleDB 3.9.8\n"
        for path in (
            "README.md",
            "docs/README.md",
            "docs/02.architecture/descriptions/9999-exampledb.md",
            "docs/02.architecture/decisions/9999-exampledb.md",
        ):
            with self.subTest(path=path):
                self.assertIn(
                    "runtime-version-literal",
                    {f.code for f in self.findings(text, path)},
                )

    def test_each_component_needs_authority_coverage(self):
        entries = (
            *self.ENTRIES,
            {
                "component": "OtherDB",
                "images": ["vendor/other:8.7.6"],
                "compose_files": ["infra/other/docker-compose.yml"],
                "direct_source": True,
            },
        )
        record = metadata.Record(
            pathlib.Path("docs/02.architecture/descriptions/9999-platform.md"),
            {},
            "architecture",
        )
        with patch.object(
            heading_module, "_runtime_version_entries", return_value=entries
        ):
            body = (
                "ExampleDB 4.2.2 and OtherDB 8.7.5 runtime.\n"
                "[First](/infra/04-data/exampledb/docker-compose.yml)\n"
            )
            self.assertIn(
                "runtime-version-source-missing",
                {
                    f.code
                    for f in heading_module._runtime_version_findings(record, body)
                },
            )
            self.assertNotIn(
                "runtime-version-source-missing",
                {
                    f.code
                    for f in heading_module._runtime_version_findings(
                        record, body + "[Second](/infra/other/docker-compose.yml)"
                    )
                },
            )
            self.assertNotIn(
                "runtime-version-source-missing",
                {
                    f.code
                    for f in heading_module._runtime_version_findings(
                        record, body + "[Registry](/infra/tech-stack.versions.json)"
                    )
                },
            )

    def test_cross_subject_mentions_without_versions_add_no_source_obligation(self):
        entries = (
            *self.ENTRIES,
            {
                "component": "OtherDB",
                "images": ["vendor/other:8.7.6"],
                "compose_files": ["infra/other/docker-compose.yml"],
                "direct_source": True,
            },
        )
        record = metadata.Record(
            pathlib.Path("docs/02.architecture/descriptions/9999-platform.md"),
            {},
            "architecture",
        )
        with patch.object(
            heading_module, "_runtime_version_entries", return_value=entries
        ):
            self.assertEqual(
                [],
                heading_module._runtime_version_findings(
                    record,
                    "ExampleDB and OtherDB exchange data.\n"
                    "[First](/infra/04-data/exampledb/docker-compose.yml)\n",
                ),
            )

    def test_cross_subject_upgrade_literal_uses_document_context(self) -> None:
        entries = (
            {
                "component": "Airflow",
                "images": ["hy-home/airflow:3.3.1-keycloak"],
                "compose_files": ["infra/07-workflow/airflow/docker-compose.yml"],
                "direct_source": True,
            },
        )
        record = metadata.Record(
            pathlib.Path(
                "docs/05.operations/guides/0079-application-auth-integration.md"
            ),
            {},
            "operation/guide",
        )
        with patch.object(
            heading_module, "_runtime_version_entries", return_value=entries
        ):
            findings = heading_module._runtime_version_findings(
                record,
                "Airflow provider integration.\n"
                "[Runtime](/infra/07-workflow/airflow/docker-compose.yml)\n"
                "Provider 0.9.0 upgrade requires permission repair.\n",
            )
        self.assertIn("runtime-version-literal", {item.code for item in findings})

    def test_owned_runtime_docs_reject_unlabelled_patch_literals(self) -> None:
        self.assertIn(
            "runtime-version-literal",
            {
                finding.code
                for finding in self.findings(
                    self.POINTER + "Secure mode is the default as of 4.2.3.\n"
                )
            },
        )

    def test_changed_runtime_literals_preserve_identity_and_multiplicity(self):
        record = metadata.Record(
            pathlib.Path("infra/04-data/exampledb/README.md"), {}, "common/readme"
        )
        base = self.POINTER + "ExampleDB 3.9.8\n"
        with patch.object(
            heading_module, "_runtime_version_entries", return_value=self.ENTRIES
        ):
            for current in (
                base + "ExampleDB 4.1.9\n",
                base + "ExampleDB 3.9.8\n",
                self.POINTER + "ExampleDB 4.1.9\n",
            ):
                self.assertIn(
                    "runtime-version-literal",
                    {
                        f.code
                        for f in heading_module._introduced_body_findings(
                            record, current, record, base, {"profiles": {}}
                        )
                    },
                )
            self.assertEqual(
                [],
                heading_module._introduced_body_findings(
                    record,
                    "ExampleDB 3.9.8\n" + self.POINTER,
                    record,
                    base,
                    {"profiles": {}},
                ),
            )

    def test_exception_reason_requires_explanation(self):
        for reason in (
            "x",
            ".",
            "TBD",
            "TODO",
            "   ",
            "____________",
            "TODO TODO TODO",
            "TBD placeholder TODO",
        ):
            body = (
                self.POINTER
                + "ExampleDB 3.9.8 <!-- runtime-version-exception: history — "
                + reason
                + " -->"
            )
            self.assertIn(
                "runtime-version-literal", {f.code for f in self.findings(body)}
            )
        for reason in (
            "required for the legacy restore format",
            "이전 백업 형식의 복원 호환성을 설명함",
        ):
            self.assertEqual(
                [],
                self.findings(
                    self.POINTER
                    + "ExampleDB 3.9.8 <!-- runtime-version-exception: compatibility — "
                    + reason
                    + " -->"
                ),
            )

    def test_calendar_dates_are_not_runtime_patch_literals(self) -> None:
        body = (
            self.POINTER
            + "ExampleDB review date: 2026.09.20, source audit completed.\n"
        )
        self.assertEqual([], self.findings(body))

    def test_smtp_status_codes_and_section_numbers_are_not_runtime_literals(
        self,
    ) -> None:
        for line in (
            "550 5.7.1 Relay not allowed",
            "The SMTP reply 5.7.1 means the relay was rejected.",
            "5.4.3 Verify the token role",
            "## 5.4.3 Verify the token role",
            "- 5.4.3 Verify the token role",
            "See section 5.4.3 for the token role.",
            "Repeat step 5.4.3 after the restart.",
            "See § 5.4.3.",
            "5.4.3 단계에서 토큰 역할을 확인한다.",
            "토큰 역할은 5.4.3 절을 따른다.",
        ):
            with self.subTest(line=line):
                self.assertEqual([], self.findings(self.POINTER + line + "\n"))
        for line in ("ExampleDB 3.9.8", "Upgrade ExampleDB to 3.9.8 in section 2."):
            with self.subTest(line=line):
                self.assertIn(
                    "runtime-version-literal",
                    {f.code for f in self.findings(self.POINTER + line + "\n")},
                )

    def test_nonnumeric_image_tags_do_not_turn_ordinary_prose_into_literals(
        self,
    ) -> None:
        entries = (
            {
                "component": "Gatus",
                "images": ["hy/gatus:local"],
                "compose_files": ["infra/06-observability/docker-compose.yml"],
                "direct_source": True,
            },
        )
        self.assertFalse(
            heading_module._runtime_literal_line(
                "Keep local validation evidence.", entries, owned_context=True
            )
        )

    def test_noncurated_compose_sources_cover_component_and_cross_subject_literals(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            self.assertEqual(0, git(root, "init").returncode)
            sources = {
                "infra/04-data/nosql/cassandra/docker-compose.yml": (
                    "services:\n  cassandra:\n    image: cassandra:5.0.9\n"
                ),
                "infra/04-data/nosql/mongodb/docker-compose.yml": (
                    "services:\n  mongodb:\n    image: mongo:8.3.11-noble\n"
                ),
            }
            for relative, content in sources.items():
                source = root / relative
                source.parent.mkdir(parents=True, exist_ok=True)
                source.write_text(content)
            self.assertEqual(0, git(root, "add", ".").returncode)

            cases = (
                (
                    "docs/05.operations/policies/0025-cassandra.md",
                    "[Runtime](/infra/04-data/nosql/cassandra/docker-compose.yml)\n"
                    "Cassandra 5.0.8 compatibility boundary.\n",
                ),
                (
                    "docs/05.operations/guides/0001-auth.md",
                    "[Runtime](/infra/04-data/nosql/mongodb/docker-compose.yml)\n"
                    "MongoDB 8.3.9 migration boundary.\n",
                ),
            )
            for path, body in cases:
                record = metadata.Record(pathlib.Path(path), {}, "operation/policy")
                with self.subTest(path=path):
                    self.assertEqual(
                        {"runtime-version-literal"},
                        {
                            finding.code
                            for finding in heading_module._runtime_version_findings(
                                record, body, root
                            )
                        },
                    )

    def test_root_compose_variants_are_discovered_and_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            self.assertEqual(0, git(root, "init").returncode)
            source = root / "compose.override.yml"
            source.write_text(
                "services:\n  exampledb:\n    image: vendor/exampledb:4.2.3\n"
            )
            self.assertEqual(0, git(root, "add", ".").returncode)
            self.assertEqual(
                (pathlib.Path("compose.override.yml"),),
                heading_module._runtime_tracked_sources(root),
            )
            record = metadata.Record(pathlib.Path("README.md"), {}, "common/readme")
            self.assertEqual(
                {"runtime-version-literal"},
                {
                    finding.code
                    for finding in heading_module._runtime_version_findings(
                        record,
                        "[Runtime](compose.override.yml)\nExampleDB 4.2.2.\n",
                        root,
                    )
                },
            )

            source.write_text(
                "services:\n  exampledb:\n    image: ${PRIVATE_EXAMPLE_IMAGE}\n"
            )
            with patch.dict(
                os.environ, {"PRIVATE_EXAMPLE_IMAGE": "vendor/exampledb:9.9.9"}
            ):
                self.assertEqual(
                    {"runtime-version-source-invalid"},
                    {
                        finding.code
                        for finding in heading_module._runtime_version_findings(
                            record,
                            "[Runtime](compose.override.yml)\nExampleDB runtime.\n",
                            root,
                        )
                    },
                )

    def test_unresolved_compose_image_authority_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            self.assertEqual(0, git(root, "init").returncode)
            source = root / "infra/04-data/nosql/cassandra/docker-compose.yml"
            source.parent.mkdir(parents=True)
            source.write_text(
                "services:\n  cassandra:\n    image: ${PRIVATE_CASSANDRA_IMAGE}\n"
            )
            self.assertEqual(0, git(root, "add", ".").returncode)
            record = metadata.Record(
                pathlib.Path("infra/04-data/nosql/cassandra/README.md"),
                {},
                "common/readme",
            )
            self.assertEqual(
                {"runtime-version-source-invalid"},
                {
                    finding.code
                    for finding in heading_module._runtime_version_findings(
                        record,
                        "[Runtime](docker-compose.yml)\nCassandra runtime.\n",
                        root,
                    )
                },
            )

    def test_compose_merge_keys_remain_an_authored_runtime_source(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            self.assertEqual(0, git(root, "init").returncode)
            source = root / "infra/09-tooling/opentofu/docker-compose.yml"
            source.parent.mkdir(parents=True)
            source.write_text(
                "x-runtime: &runtime\n"
                "  image: hy-home/opentofu:1.12.6-local\n"
                "services:\n"
                "  opentofu:\n"
                "    <<: *runtime\n"
            )
            self.assertEqual(0, git(root, "add", ".").returncode)
            record = metadata.Record(
                pathlib.Path("infra/09-tooling/opentofu/README.md"),
                {},
                "common/readme",
            )
            self.assertEqual(
                {"runtime-version-literal"},
                {
                    finding.code
                    for finding in heading_module._runtime_version_findings(
                        record,
                        "[Runtime](docker-compose.yml)\nOpenTofu 1.12.5.\n",
                        root,
                    )
                },
            )

    def test_inline_dockerfile_arg_defaults_are_authored_and_unresolved_fail_closed(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            self.assertEqual(0, git(root, "init").returncode)
            source = root / "infra/09-tooling/opentofu/docker-compose.yml"
            source.parent.mkdir(parents=True)
            source.write_text(
                "services:\n"
                "  opentofu:\n"
                "    build:\n"
                "      context: .\n"
                "      dockerfile_inline: |\n"
                "        ARG TOFU_VERSION=1.12.6\n"
                "        FROM ghcr.io/opentofu/opentofu:${TOFU_VERSION}-minimal AS tofu\n"
                "        FROM alpine:3.22\n"
            )
            self.assertEqual(0, git(root, "add", ".").returncode)
            record = metadata.Record(
                pathlib.Path("infra/09-tooling/opentofu/README.md"),
                {},
                "common/readme",
            )
            self.assertEqual(
                {"runtime-version-literal"},
                {
                    finding.code
                    for finding in heading_module._runtime_version_findings(
                        record,
                        "[Runtime](docker-compose.yml)\nOpenTofu 1.12.5.\n",
                        root,
                    )
                },
            )

            source.write_text(
                "services:\n"
                "  opentofu:\n"
                "    build:\n"
                "      context: .\n"
                "      dockerfile_inline: |\n"
                "        ARG TOFU_VERSION\n"
                "        FROM ghcr.io/opentofu/opentofu:${TOFU_VERSION}-minimal\n"
            )
            with patch.dict(os.environ, {"TOFU_VERSION": "9.9.9"}):
                self.assertEqual(
                    {"runtime-version-source-invalid"},
                    {
                        finding.code
                        for finding in heading_module._runtime_version_findings(
                            record,
                            "[Runtime](docker-compose.yml)\nOpenTofu runtime.\n",
                            root,
                        )
                    },
                )

    def test_unmapped_dockerfile_runtime_has_direct_authority(self):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            self.assertEqual(0, git(root, "init").returncode)
            source = root / "infra/buildonly/Dockerfile"
            source.parent.mkdir(parents=True)
            source.write_text("FROM vendor/buildonly:9.8.7\n")
            self.assertEqual(0, git(root, "add", ".").returncode)
            record = metadata.Record(
                pathlib.Path("infra/buildonly/README.md"), {}, "common/readme"
            )
            with patch.object(
                heading_module, "_runtime_version_entries", return_value=self.ENTRIES
            ):
                for body in (
                    "[Build](Dockerfile)\nvendor/buildonly:9.8.7",
                    "[Build](Dockerfile)\nBuildonly version: 9.8.6",
                ):
                    self.assertIn(
                        "runtime-version-literal",
                        {
                            f.code
                            for f in heading_module._runtime_version_findings(
                                record, body, root
                            )
                        },
                    )
                self.assertEqual(
                    [],
                    heading_module._runtime_version_findings(
                        record, "[Build](Dockerfile)\nBuild instructions.", root
                    ),
                )
                self.assertEqual(
                    [],
                    heading_module._runtime_version_findings(
                        record,
                        "[Registry](/infra/tech-stack.versions.json)\nBuild instructions.",
                        root,
                    ),
                )

    def test_build_source_defaults_are_authored_and_unresolved_args_fail_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            self.assertEqual(0, git(root, "init").returncode)
            source = root / "infra/buildonly/Dockerfile"
            source.parent.mkdir(parents=True)
            record = metadata.Record(
                pathlib.Path("infra/buildonly/README.md"), {}, "common/readme"
            )
            with patch.object(
                heading_module, "_runtime_version_entries", return_value=self.ENTRIES
            ):
                source.write_text(
                    "ARG BUILD_VERSION=9.8.7\nFROM vendor/buildonly:${BUILD_VERSION}\n"
                )
                self.assertEqual(0, git(root, "add", ".").returncode)
                findings = heading_module._runtime_version_findings(
                    record, "[Build](Dockerfile)\nvendor/buildonly:9.8.7", root
                )
                self.assertIn("runtime-version-literal", {f.code for f in findings})
                for content in (
                    "ARG BUILD_VERSION\nFROM vendor/buildonly:${BUILD_VERSION}\n",
                    "FROM vendor/buildonly:${BUILD_VERSION}\nARG BUILD_VERSION=9.8.7\n",
                ):
                    source.write_text(content)
                    self.assertIn(
                        "runtime-version-source-invalid",
                        {
                            f.code
                            for f in heading_module._runtime_version_findings(
                                record, "[Build](Dockerfile)", root
                            )
                        },
                    )

    def test_tracked_dockerfile_variants_are_covered_without_private_untracked_files(
        self,
    ):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            self.assertEqual(0, git(root, "init").returncode)
            source = root / "infra/buildonly/dev.Dockerfile"
            source.parent.mkdir(parents=True)
            source.write_text(
                "FROM vendor/buildonly:9.8.7 AS Builder\nFROM builder AS Final\n"
            )
            self.assertEqual(0, git(root, "add", ".").returncode)
            source.with_name("private.Dockerfile").write_text("FROM ${PRIVATE_IMAGE}\n")
            source.with_name("Dockerfile").write_text("FROM ${PRIVATE_IMAGE}\n")
            record = metadata.Record(
                pathlib.Path("infra/buildonly/README.md"), {}, "common/readme"
            )
            with patch.object(
                heading_module, "_runtime_version_entries", return_value=self.ENTRIES
            ):
                self.assertIn(
                    "runtime-version-literal",
                    {
                        f.code
                        for f in heading_module._runtime_version_findings(
                            record, "[Build](dev.Dockerfile)\nBuildonly 9.8.7", root
                        )
                    },
                )
                self.assertEqual(
                    [],
                    heading_module._runtime_version_findings(
                        record, "[Build](dev.Dockerfile)\nBuild instructions.", root
                    ),
                )

    def test_failed_tracked_build_discovery_fails_closed(self):
        record = metadata.Record(
            pathlib.Path("infra/04-data/exampledb/README.md"), {}, "common/readme"
        )
        with (
            patch.object(
                heading_module, "_runtime_version_entries", return_value=self.ENTRIES
            ),
            patch.object(
                heading_module.subprocess,
                "run",
                return_value=heading_module.subprocess.CompletedProcess(
                    [], 128, b"", b"discovery unavailable"
                ),
            ),
        ):
            self.assertIn(
                "runtime-version-source-invalid",
                {
                    f.code
                    for f in heading_module._runtime_version_findings(
                        record, self.POINTER + "ExampleDB service."
                    )
                },
            )

    def test_runtime_validation_under_inherited_gate_root_descriptor(self):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            self.assertEqual(0, git(root, "init").returncode)
            source = root / "infra/buildonly/Dockerfile"
            source.parent.mkdir(parents=True)
            source.write_text("FROM vendor/buildonly:9.8.7\n")
            (root / "infra/tech-stack.versions.json").write_text(
                json.dumps({"entries": list(self.ENTRIES)})
            )
            self.assertEqual(0, git(root, "add", ".").returncode)
            descriptor = os.open(root, os.O_RDONLY | os.O_DIRECTORY)
            try:
                program = """import pathlib, sys
from scripts.lib.document_governance.metadata.heading import _runtime_version_findings
from scripts.lib.document_governance.metadata.profile import Record
root = pathlib.Path('/proc/self/fd/' + sys.argv[1])
record = Record(pathlib.Path('infra/buildonly/README.md'), {}, 'common/readme')
findings = _runtime_version_findings(record, '[Build](Dockerfile)\\nBuildonly 9.8.7', root)
assert {f.code for f in findings} == {'runtime-version-literal'}, findings
"""
                result = subprocess.run(
                    [sys.executable, "-c", program, str(descriptor)],
                    cwd=ROOT,
                    check=False,
                    pass_fds=(*gate_root_pass_fds(ROOT), descriptor),
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            finally:
                os.close(descriptor)
