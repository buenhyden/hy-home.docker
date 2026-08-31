"""Heading and body-contract tests."""

from __future__ import annotations

import pathlib
import unittest

from scripts.lib.document_governance.metadata import heading as heading_module
from tests.lib.document_governance.metadata._support import (
    POLICY_TARGET_BODY,
    REQUIREMENT_TARGET_BODY,
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
        body = REQUIREMENT_TARGET_BODY + "\n{{existing_token}}\n"
        self.assertEqual([], self.introduced(body + "\nEditorial text.\n", body))

    def test_additional_body_token_is_blocked_without_value_leakage(self) -> None:
        base = REQUIREMENT_TARGET_BODY + "\n{{existing_token}}\n"
        findings = self.introduced(base + "\n{{additional_token}}\n", base)
        self.assertEqual(["template-body-token-in-target"], [item.code for item in findings])
        rendered = "\n".join(item.message for item in findings)
        self.assertNotIn("existing_token", rendered)
        self.assertNotIn("additional_token", rendered)

    def test_replaced_body_token_is_a_new_private_deficit(self) -> None:
        findings = self.introduced(
            REQUIREMENT_TARGET_BODY + "\n{{replacement_token}}\n",
            REQUIREMENT_TARGET_BODY + "\n{{original_token}}\n",
        )
        self.assertEqual(["template-body-token-in-target"], [item.code for item in findings])
        rendered = "\n".join(item.message for item in findings)
        self.assertNotIn("original_token", rendered)
        self.assertNotIn("replacement_token", rendered)

    def test_new_instruction_is_blocked_without_literal_echo(self) -> None:
        findings = self.introduced(
            REQUIREMENT_TARGET_BODY + "\n> Rules:\n",
            REQUIREMENT_TARGET_BODY,
        )
        self.assertEqual(["template-instruction-in-target"], [item.code for item in findings])
        self.assertNotIn("> Rules:", "\n".join(item.message for item in findings))

    def test_new_file_body_deficit_is_blocked(self) -> None:
        findings = self.introduced(
            REQUIREMENT_TARGET_BODY + "\n{{new_file_token}}\n",
            None,
        )
        self.assertEqual(["template-body-token-in-target"], [item.code for item in findings])

    def test_current_operations_policy_preserves_its_own_body_baseline(self) -> None:
        record = metadata.Record(
            pathlib.Path(
                "docs/05.operations/catalog/00-workspace/"
                "0001-common-optimizations-template-exceptions/policy.md"
            ),
            {
                "profile_id": "policy",
                "status": "active",
                "artifact_id": "policy-0001",
                "artifact_type": "policy",
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
            "profile_id": "policy",
            "status": "active",
            "artifact_id": "policy-0001",
            "artifact_type": "policy",
            "parent_ids": [],
            "created": "2026-08-01",
            "updated": "2026-08-01",
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
            {item.code for item in findings({"owner": "undeclared"})},
        )

    def test_commonmark_code_hides_template_residue(self) -> None:
        cases = (
            "```markdown\n> Rules:\n{{fenced_token}}\n```\n",
            "~~~markdown\n> Rules:\n{{fenced_token}}\n~~~\n",
            "```markdown\n> Rules:\n{{fenced_token}}\n",
            "Document `> Rules:` and `{{inline_token}}`.\n",
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
            + "\n```markdown\n{{fenced_token}}\n```\n"
            + "Document `{{inline_token}}`.\n"
            + "{{outside_token}}\n"
        )
        self.assertEqual(
            ["template-body-token-in-target"],
            [item.code for item in self.introduced(body, REQUIREMENT_TARGET_BODY)],
        )
