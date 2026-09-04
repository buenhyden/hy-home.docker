"""Repository-composition and compatibility-facade tests."""

from __future__ import annotations

import contextlib
import io
import pathlib
import shutil
import subprocess
import tempfile
import unittest

from scripts.lib.document_governance import archive as archive_authority
from scripts.lib.document_governance.lifecycle.recovery import (
    run as run_recovery,
)

from scripts.lib.document_governance.metadata import reference as reference_module
from scripts.lib.document_governance.metadata.heading import (
    extract_markdown_headings,
)
from scripts.lib.document_governance.metadata.profile import (
    classify_registered_path,
)
from scripts.lib.document_governance.registry import (
    PRESERVED_DISPOSITIONS,
    preserved_origin_path,
)
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
            "docs/99.templates/templates/specs/contracts/openapi.template.yaml"
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
            "docs/99.templates/templates/requirements/requirement-package.template.md"
        )
        cases = (
            (
                "profile",
                'type: "sdlc/requirement"',
                'type: "sdlc/spec"',
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

    def test_repository_contracts_fail_closed_on_openapi_parse_boundaries_without_leaks(
        self,
    ) -> None:
        relative_path = (
            "docs/99.templates/templates/specs/contracts/openapi.template.yaml"
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
            "docs/99.templates/templates/specs/contracts/openapi.template.yaml"
        )
        values = {
            "default": "fixture-default-leak",
            "example": "fixture-example-leak",
            "const": "fixture-const-leak",
            "enum": "[fixture-enum-leak, __PASSWORD_SECONDARY__]",
        }
        for keyword, value in values.items():
            with (
                self.subTest(keyword=keyword),
                tempfile.TemporaryDirectory() as directory,
            ):
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
        with (
            self.subTest(keyword="direct-list"),
            tempfile.TemporaryDirectory() as directory,
        ):
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

    def test_repository_contracts_reject_openapi_credential_plural_examples_without_leaks(
        self,
    ) -> None:
        relative_path = (
            "docs/99.templates/templates/specs/contracts/openapi.template.yaml"
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

    def test_repository_contracts_accept_exact_nested_openapi_credential_examples_tokens(
        self,
    ) -> None:
        relative_path = (
            "docs/99.templates/templates/specs/contracts/openapi.template.yaml"
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
            "docs/99.templates/templates/specs/contracts/openapi.template.yaml"
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


class IndexMembershipTests(unittest.TestCase):
    """The index rule must fire, and must not fire on a listed package."""

    def _findings(self, index_body: str) -> list[object]:
        registry = metadata.load_registry()
        member = "docs/90.references/research/0002-agentic-engineering-research-pack/README.md"
        self.assertEqual(
            "research",
            classify_registered_path(member, registry),
            "fixture path must classify as the indexed member profile",
        )
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            index = root / "docs/90.references/research/README.md"
            index.parent.mkdir(parents=True)
            index.write_text(index_body, encoding="utf-8")
            record = metadata.Record(pathlib.Path(member), {}, "research")
            findings = reference_module._index_membership_findings(
                root, registry, [record]
            )
        # The fixture root holds only the research index and one research
        # record, so the other registered indexes govern nothing and are
        # skipped. Scoping keeps this test about the research rule alone.
        return [
            finding
            for finding in findings
            if finding.path == "docs/90.references/research/README.md"
            and finding.code != "index-unreadable"
        ]

    def test_unlisted_package_is_reported(self) -> None:
        findings = self._findings("# Research Packages\n")
        self.assertEqual(
            ["index-member-unlisted"], [finding.code for finding in findings]
        )

    def test_listed_package_is_accepted(self) -> None:
        findings = self._findings(
            "# Research Packages\n\n"
            "| [RES-0002](./0002-agentic-engineering-research-pack/README.md) | x |\n"
        )
        self.assertEqual([], findings)

    def test_every_registered_index_governs_at_least_one_package(self) -> None:
        """A rule that enumerates nothing passes without checking anything."""

        registry = metadata.load_registry()
        self.assertTrue(registry.indexes)
        for index_path, member_profile in registry.indexes.items():
            with self.subTest(index=index_path):
                self.assertTrue((ROOT / index_path).is_file())
                governed = [
                    path
                    for path in (ROOT / index_path).parent.rglob("*.md")
                    if classify_registered_path(
                        path.relative_to(ROOT).as_posix(), registry
                    )
                    == member_profile
                ]
                governed.extend(
                    self._preserved_members(registry, index_path, member_profile)
                )
                self.assertTrue(governed, f"{index_path} governs no document")

    @staticmethod
    def _preserved_members(
        registry: object, index_path: str, member_profile: str
    ) -> list[pathlib.Path]:
        """Members an index still governs after preservation moved their bodies.

        An active stage empties out when its last package completes, which is a
        real state and not a vacuous rule: Stage 03 holds no package exactly
        when no change is in flight. Preservation moves the body without ending
        the governance relation, so the index's own listing still routes to
        every one of them. Count them by the path they were moved from.
        """

        stage_dir = pathlib.PurePosixPath(index_path).parent
        found: list[pathlib.Path] = []
        for disposition in PRESERVED_DISPOSITIONS:
            root = ROOT / "docs/98.archive" / disposition
            if not root.is_dir():
                continue
            for path in root.rglob("*.md"):
                origin = preserved_origin_path(path.relative_to(ROOT).as_posix())
                if origin is None:
                    continue
                if not origin.startswith(f"{stage_dir}/"):
                    continue
                if classify_registered_path(origin, registry) == member_profile:
                    found.append(path)
        return found


class ReadmeSectionProfileTests(unittest.TestCase):
    """Sections come from the document's own profile, not from `readme`."""

    def test_every_readme_profile_that_declares_sections_is_satisfied(self) -> None:
        registry = metadata.load_registry()
        checked = 0
        for path in ROOT.glob("**/README.md"):
            relative = path.relative_to(ROOT).as_posix()
            if relative.startswith((".git/", ".worktrees/", "node_modules/")):
                continue
            profile_id = classify_registered_path(relative, registry)
            if profile_id is None:
                continue
            required = registry.profiles.get(profile_id, {}).get(
                "required_sections", ()
            )
            if not required:
                continue
            checked += 1
            _, h2 = extract_markdown_headings(path.read_text(encoding="utf-8"))
            for section in required:
                with self.subTest(path=relative, section=section):
                    self.assertIn(f"## {section}", h2)
        # A profile-driven check that inspects nothing passes vacuously.
        self.assertGreater(checked, 100, "too few READMEs carry a section contract")

    def test_profiles_beyond_readme_declare_sections(self) -> None:
        """The rule is only worth enforcing if other profiles use it."""

        registry = metadata.load_registry()
        with_sections = {
            profile_id
            for profile_id, profile in registry.profiles.items()
            if profile.get("required_sections")
        }
        self.assertIn("readme", with_sections)
        self.assertTrue(with_sections - {"readme"})


class GloballyForbiddenKeyTests(unittest.TestCase):
    """A retired key is reported as retired, not as an unknown typo."""

    def _codes(self, key: str) -> list[str]:
        registry = metadata.load_registry()
        profiles = metadata.build_registry_profiles(registry)
        record = metadata.Record(
            pathlib.Path("docs/00.agent-governance/providers/README.md"),
            {
                "title": "Providers",
                "version": "1.0.0",
                "type": "governance/provider-index",
                "status": "active",
                "owner": "@buenhyden",
                key: "x",
            },
            "governance-provider-index",
        )
        manifest = metadata.build_manifest([record])
        return [
            finding.code
            for finding in metadata.validate_record(record, profiles, manifest)
            if finding.code in {"forbidden-key", "type-inappropriate-key"}
        ]

    def test_every_globally_forbidden_key_is_reported_as_forbidden(self) -> None:
        registry = metadata.load_registry()
        forbidden = registry.common.get("globally_forbidden", ())
        self.assertTrue(forbidden, "the contract declares nothing to enforce")
        for key in forbidden:
            with self.subTest(key=key):
                self.assertIn("forbidden-key", self._codes(key))

    def test_an_undeclared_key_keeps_the_other_code(self) -> None:
        self.assertEqual(["type-inappropriate-key"], self._codes("bogus_key"))


class ArchiveContractDiagnosticTests(unittest.TestCase):
    """An archive contract violation must name the document, not be an error."""

    def _corrupted_root(self, directory: str) -> pathlib.Path:
        root = pathlib.Path(directory)
        shutil.copytree(ROOT / "docs/98.archive", root / "docs/98.archive")
        victim = next((root / "docs/98.archive/tombstones").rglob("*.md"))
        victim.write_text(
            victim.read_text(encoding="utf-8")
            + "\n## Original Body\n\nA retired body copied into the pointer.\n",
            encoding="utf-8",
        )
        self.relative = victim.relative_to(root).as_posix()
        return root

    def test_violation_is_reported_with_its_path(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self._corrupted_root(directory)
            stream = io.StringIO()
            with contextlib.redirect_stdout(stream):
                code = run_recovery(root)
        output = stream.getvalue()
        self.assertEqual(1, code, output)
        self.assertIn("archive-contract-invalid", output)
        self.assertIn(self.relative, output)

    def test_intact_archive_still_loads(self) -> None:
        inventory = archive_authority.load_archive(ROOT / "docs/98.archive")
        self.assertTrue(inventory.tombstones)
        self.assertTrue(inventory.migrations)


class TemplateCatalogTests(unittest.TestCase):
    """The catalog is the documented way to find a template, so it must be whole."""

    def test_catalog_lists_every_registered_role(self) -> None:
        registry = metadata.load_registry()
        findings = reference_module._template_catalog_findings(ROOT, registry)
        self.assertEqual([], findings)

    def test_the_rule_governs_every_role(self) -> None:
        """A catalog check that inspects nothing passes vacuously."""

        registry = metadata.load_registry()
        self.assertTrue(registry.template_catalog)
        self.assertGreater(len(registry.template_roles), 30)

    def test_a_missing_row_is_reported(self) -> None:
        registry = metadata.load_registry()
        catalog = ROOT / registry.template_catalog
        victim = sorted(registry.template_roles)[0]
        source = registry.template_roles[victim]["source"]
        kept = [
            line
            for line in catalog.read_text(encoding="utf-8").splitlines()
            if source.split("templates/")[-1] not in line
        ]
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            target = root / registry.template_catalog
            target.parent.mkdir(parents=True)
            target.write_text("\n".join(kept), encoding="utf-8")
            # The rule only governs roles whose source is present, so the
            # omitted template has to exist for the omission to matter.
            copied = root / source
            copied.parent.mkdir(parents=True, exist_ok=True)
            copied.write_text(
                (ROOT / source).read_text(encoding="utf-8"), encoding="utf-8"
            )
            findings = reference_module._template_catalog_findings(root, registry)
        self.assertIn(
            "template-catalog-unlisted", [finding.code for finding in findings]
        )
