"""Heading and body-contract tests."""

from __future__ import annotations

import pathlib
import subprocess
import unittest

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
