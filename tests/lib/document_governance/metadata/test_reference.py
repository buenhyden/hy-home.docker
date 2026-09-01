"""Repository-composition and compatibility-facade tests."""

from __future__ import annotations

import pathlib
import subprocess
import tempfile
import unittest

from scripts.lib.document_governance.metadata import reference as reference_module
from tests.lib.document_governance.metadata._support import (
    ROOT,
    copy_registry_contract_fixture,
    current_profiles,
    metadata,
    run_checker,
)


class MetadataValidatorCompatibilityTests(unittest.TestCase):
    def test_metadata_validator_declares_its_compatibility_api(self) -> None:
        """The split preserves live imports, not incidental module globals."""

        from scripts.lib.document_governance import metadata_validator

        self.assertTrue(metadata_validator.__all__)
        missing = [
            name
            for name in metadata_validator.__all__
            if not hasattr(metadata_validator, name)
        ]
        self.assertEqual([], missing)

class RepositoryContractIntegrationTests(unittest.TestCase):
    def fixture(self, directory: str) -> tuple[pathlib.Path, pathlib.Path]:
        root = pathlib.Path(directory)
        return root, copy_registry_contract_fixture(root)

    def run_contracts(
        self,
        root: pathlib.Path,
        profiles: pathlib.Path,
    ) -> subprocess.CompletedProcess[str]:
        return run_checker(root, "check-contracts", profiles=profiles)

    def test_repository_contracts_validate_canonical_spec_packages(self) -> None:
        profiles = current_profiles()
        findings = metadata.validate_repository_contracts(ROOT, profiles)
        self.assertNotIn(
            "spec-package-invalid",
            {finding.code for finding in findings},
        )

    def test_repository_contracts_enforce_machine_source_safety(self) -> None:
        relative_path = (
            "docs/99.templates/templates/specs/openapi.template.yaml"
        )
        with tempfile.TemporaryDirectory() as directory:
            root, profiles = self.fixture(directory)
            path = root / relative_path
            path.write_text(
                "openapi: 3.1.0\n"
                "x-template-token: __API_TITLE__\n"
                "servers:\n"
                "  - url: https://api.example.com\n",
                encoding="utf-8",
            )
            result = self.run_contracts(root, profiles)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn(
                f"machine-template-example-value: {relative_path}",
                result.stdout,
            )

    def test_registry_contracts_parse_profile_and_section_contracts(self) -> None:
        relative_path = (
            "docs/99.templates/templates/requirements/"
            "requirement-package.template.md"
        )
        cases = (
            (
                "profile",
                "type: requirements/package",
                "type: specs/spec",
                "template-artifact-type-mismatch",
            ),
            (
                "heading",
                "## Acceptance Criteria",
                "## Verification Contract",
                "template-section-missing",
            ),
        )
        for label, before, after, expected in cases:
            with self.subTest(case=label), tempfile.TemporaryDirectory() as directory:
                root, profiles = self.fixture(directory)
                path = root / relative_path
                path.write_text(
                    path.read_text(encoding="utf-8").replace(before, after, 1),
                    encoding="utf-8",
                )
                result = self.run_contracts(root, profiles)
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                self.assertIn(f"{expected}: {relative_path}", result.stdout)

    def test_repository_contracts_fail_closed_on_openapi_parse_boundaries_without_leaks(self) -> None:
        relative_path = (
            "docs/99.templates/templates/specs/openapi.template.yaml"
        )
        cases = (
            (
                "malformed",
                "openapi: 3.1.0\nx-template-token: __API_TITLE__\npaths: [fixture-parse-leak\n",
                "fixture-parse-leak",
            ),
            (
                "duplicate-key",
                "openapi: 3.1.0\nx-template-token: __API_TITLE__\ninfo: fixture-first\ninfo: fixture-duplicate-leak\n",
                "fixture-duplicate-leak",
            ),
            (
                "constructor",
                "openapi: 3.1.0\nx-template-token: __API_TITLE__\nx-value: !!python/object:fixture-constructor-leak {}\n",
                "fixture-constructor-leak",
            ),
            (
                "non-mapping-root",
                "- __API_TITLE__\n- fixture-root-leak\n",
                "fixture-root-leak",
            ),
        )
        for label, text, private_value in cases:
            with self.subTest(case=label), tempfile.TemporaryDirectory() as directory:
                root, profiles = self.fixture(directory)
                (root / relative_path).write_text(text, encoding="utf-8")
                result = self.run_contracts(root, profiles)
                rendered = result.stdout + result.stderr
                self.assertEqual(1, result.returncode, rendered)
                self.assertIn(
                    f"machine-template-parse-error: {relative_path}: "
                    "machine template could not be parsed as a safe OpenAPI mapping",
                    result.stdout,
                )
                self.assertNotIn(private_value, rendered)
                self.assertNotRegex(rendered, r"(?i)(line|column) [0-9]+")

    def test_repository_contracts_bound_openapi_credential_value_keywords(self) -> None:
        relative_path = (
            "docs/99.templates/templates/specs/openapi.template.yaml"
        )
        values = {
            "default": "fixture-default-leak",
            "example": "fixture-example-leak",
            "const": "fixture-const-leak",
            "enum": "[fixture-enum-leak, __PASSWORD_SECONDARY__]",
        }
        for keyword, value in values.items():
            with self.subTest(keyword=keyword), tempfile.TemporaryDirectory() as directory:
                root, profiles = self.fixture(directory)
                (root / relative_path).write_text(
                    "openapi: 3.1.0\n"
                    "x-template-token: __API_TITLE__\n"
                    "components:\n"
                    "  schemas:\n"
                    "    Login:\n"
                    "      properties:\n"
                    "        password:\n"
                    "          type: string\n"
                    f"          {keyword}: {value}\n",
                    encoding="utf-8",
                )
                result = self.run_contracts(root, profiles)
                rendered = result.stdout + result.stderr
                self.assertEqual(1, result.returncode, rendered)
                self.assertIn(
                    f"machine-template-example-value: {relative_path}",
                    result.stdout,
                )
                self.assertNotIn("fixture-", rendered)
        with self.subTest(keyword="direct-list"), tempfile.TemporaryDirectory() as directory:
            root, profiles = self.fixture(directory)
            (root / relative_path).write_text(
                "openapi: 3.1.0\n"
                "x-template-token: __API_TITLE__\n"
                "access_token: [__ACCESS_TOKEN__, fixture-direct-list-leak]\n",
                encoding="utf-8",
            )
            result = self.run_contracts(root, profiles)
            rendered = result.stdout + result.stderr
            self.assertEqual(1, result.returncode, rendered)
            self.assertIn(
                f"machine-template-example-value: {relative_path}",
                result.stdout,
            )
            self.assertNotIn("fixture-direct-list-leak", rendered)

    def test_repository_contracts_reject_openapi_credential_plural_examples_without_leaks(self) -> None:
        relative_path = (
            "docs/99.templates/templates/specs/openapi.template.yaml"
        )
        cases = {
            "scalar": "fixture-scalar-cli-private",
            "list": "[__PASSWORD_PRIMARY__, fixture-list-cli-private]",
            "map": "{primary: __PASSWORD_PRIMARY__, secondary: fixture-map-cli-private}",
        }
        for label, examples in cases.items():
            with self.subTest(shape=label), tempfile.TemporaryDirectory() as directory:
                root, profiles = self.fixture(directory)
                (root / relative_path).write_text(
                    "openapi: 3.1.0\n"
                    "x-template-token: __API_TITLE__\n"
                    "components:\n"
                    "  schemas:\n"
                    "    Login:\n"
                    "      properties:\n"
                    "        password:\n"
                    "          type: string\n"
                    f"          examples: {examples}\n",
                    encoding="utf-8",
                )
                result = self.run_contracts(root, profiles)
                rendered = result.stdout + result.stderr
                self.assertEqual(1, result.returncode, rendered)
                self.assertIn(
                    f"machine-template-example-value: {relative_path}",
                    result.stdout,
                )
                self.assertNotIn("fixture-", rendered)

    def test_repository_contracts_accept_exact_nested_openapi_credential_examples_tokens(self) -> None:
        relative_path = (
            "docs/99.templates/templates/specs/openapi.template.yaml"
        )
        with tempfile.TemporaryDirectory() as directory:
            root, profiles = self.fixture(directory)
            (root / relative_path).write_text(
                "openapi: 3.1.0\n"
                "x-template-token: __API_TITLE__\n"
                "components:\n"
                "  schemas:\n"
                "    Login:\n"
                "      properties:\n"
                "        password:\n"
                "          type: string\n"
                "          examples:\n"
                "            primary: __PASSWORD_PRIMARY__\n"
                "            alternatives:\n"
                "              - __PASSWORD_SECONDARY__\n"
                "              - __PASSWORD_TERTIARY__\n",
                encoding="utf-8",
            )
            result = self.run_contracts(root, profiles)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_repository_contracts_accept_safe_openapi_credential_shapes(self) -> None:
        relative_path = (
            "docs/99.templates/templates/specs/openapi.template.yaml"
        )
        cases = (
            (
                "exact-tokens",
                "openapi: 3.1.0\n"
                "x-template-token: __API_TITLE__\n"
                "x-api-key: __API_KEY__\n"
                "components:\n"
                "  schemas:\n"
                "    Login:\n"
                "      properties:\n"
                "        password:\n"
                "          type: string\n"
                "          default: __PASSWORD_DEFAULT__\n"
                "          example: __PASSWORD_EXAMPLE__\n"
                "          const: __PASSWORD_CONST__\n"
                "          enum: [__PASSWORD_PRIMARY__, __PASSWORD_SECONDARY__]\n",
            ),
            (
                "schema-only-unrelated-default",
                "openapi: 3.1.0\n"
                "x-template-token: __API_TITLE__\n"
                "components:\n"
                "  schemas:\n"
                "    Login:\n"
                "      required: [password]\n"
                "      properties:\n"
                "        password:\n"
                "          type: string\n"
                "          format: password\n"
                "          description: caller-supplied credential\n"
                "        displayName:\n"
                "          type: string\n"
                "          default: fixture display name\n",
            ),
            (
                "standard-example-token",
                "openapi: 3.1.0\n"
                "x-template-token: __API_TITLE__\n"
                "components:\n"
                "  schemas:\n"
                "    Login:\n"
                "      properties:\n"
                "        password:\n"
                "          example: __PASSWORD_EXAMPLE__\n",
            ),
        )
        for label, text in cases:
            with self.subTest(case=label), tempfile.TemporaryDirectory() as directory:
                root, profiles = self.fixture(directory)
                (root / relative_path).write_text(text, encoding="utf-8")
                result = self.run_contracts(root, profiles)
                self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_workspace_cannot_become_a_docs_inventory_prefix(self) -> None:
        from scripts.lib.document_governance.metadata import reference

        profiles = current_profiles()
        original = reference.TARGET_MARKDOWN_PREFIXES
        try:
            reference.TARGET_MARKDOWN_PREFIXES = (*original, "_workspace/")
            findings = metadata.validate_repository_contracts(ROOT, profiles)
        finally:
            reference.TARGET_MARKDOWN_PREFIXES = original
        self.assertIn(
            "workspace-inventory-coupling",
            {finding.code for finding in findings},
        )
