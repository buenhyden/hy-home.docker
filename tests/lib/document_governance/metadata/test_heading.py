"""Heading and body-contract tests."""

from __future__ import annotations

import json
import pathlib
import subprocess
import unittest

from jsonschema import Draft202012Validator

from scripts.lib.document_governance.metadata import heading as heading_module
from scripts.lib.document_governance.registry import classify_path
from tests.lib.document_governance.metadata._support import (
    POLICY_TARGET_BODY,
    REQUIREMENT_TARGET_BODY,
    ROOT,
    body_with_headings,
    current_profiles,
    metadata,
)


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
                "docs/05.operations/catalog/00-workspace/"
                "0001-common-optimizations-template-exceptions/policy.md"
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
                    "docs/05.operations/catalog/00-workspace/"
                    "0001-common-optimizations-template-exceptions/policy.md"
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
                profile["sealed_section_shapes"] = [list(self._NEW_SHAPE)]
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
        body = body_with_headings(*(f"## {name}" for name in self._NEW_SHAPE))

        def codes(base_record: object, base_text: str | None) -> list[str]:
            return [
                finding.code
                for finding in heading_module._introduced_body_findings(
                    record, body, base_record, base_text, profiles
                )
            ]

        self.assertIn("body-sealed-shape", codes(None, None))
        self.assertNotIn("body-sealed-shape", codes(record, body))
