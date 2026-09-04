"""Profile, Registry, frontmatter, and template-role tests."""

from __future__ import annotations

import pathlib
import re
import tempfile
import unittest

from scripts.lib.document_governance.metadata import profile as profile_module
from scripts.lib.document_governance.registry import (
    _declares_provider_binding,
    document_type,
)
from tests.lib.document_governance.metadata._support import (
    REGISTRY,
    ROOT,
    current_profiles,
    metadata,
    run_checker,
    write_doc,
)


class SharedFrontmatterExtractionTests(unittest.TestCase):
    def test_metadata_checker_uses_the_shared_frontmatter_parser(self) -> None:
        from scripts.lib.document_governance import frontmatter

        self.assertIs(frontmatter.read_frontmatter_values, metadata.parse_frontmatter)
        self.assertIs(
            frontmatter.parse_frontmatter_text, metadata._parse_frontmatter_text
        )


class FrontmatterParsingTests(unittest.TestCase):
    def test_valid_yaml_frontmatter_is_parsed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "valid.md"
            write_doc(path, {"status": "active", "parent_ids": ["PRD-001"]})
            self.assertEqual(
                {"status": "active", "parent_ids": ["PRD-001"]},
                metadata.parse_frontmatter(path),
            )

    def test_missing_frontmatter_returns_empty_mapping(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "README.md"
            write_doc(path, None)
            self.assertEqual({}, metadata.parse_frontmatter(path))

    def test_invalid_yaml_frontmatter_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "invalid.md"
            path.write_text("---\nstatus: [active\n---\n# Invalid\n", encoding="utf-8")
            with self.assertRaises(metadata.FrontmatterError):
                metadata.parse_frontmatter(path)

    def test_duplicate_yaml_key_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "duplicate.md"
            path.write_text(
                "---\nstatus: active\nstatus: completed\n---\n", encoding="utf-8"
            )
            with self.assertRaises(metadata.FrontmatterError):
                metadata.parse_frontmatter(path)

    def test_unhashable_yaml_mapping_key_is_normalized(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "unhashable.md"
            path.write_text("---\n? [a, b]: c\n---\n", encoding="utf-8")
            with self.assertRaises(metadata.FrontmatterError) as context:
                metadata.parse_frontmatter(path)
            self.assertEqual("malformed-yaml", context.exception.code)


class CurrentRegistryContractTests(unittest.TestCase):
    def test_current_requirement_packages_satisfy_repository_contracts(self) -> None:
        from scripts.lib.document_governance.requirements import (
            load_requirement_packages,
        )

        self.assertTrue(load_requirement_packages(ROOT / "docs/01.requirements"))
        result = run_checker(ROOT, "check-contracts", profiles=REGISTRY)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("metadata repository contracts: violations=0", result.stdout)


class TemplateRoleInferenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        from scripts.lib.document_governance.registry import load_registry

        cls.profiles = current_profiles()
        cls.registry = load_registry(REGISTRY)

    def test_registered_targets_have_one_exact_role(self) -> None:
        token_values = {
            "number": "0901",
            "package_number": "0901",
            "task_number": "0001",
            "subject_number": "0901",
            "year": "2026",
            "member_number": "0001",
            "domain": "00-workspace",
            "stage": "03.specs",
            "slug": "fixture",
            "hook_slug": "fixture",
            "category": "audits",
            "subpath": "01-gateway/traefik",
        }

        def witness(pattern: str) -> str:
            return re.sub(
                r"\{(?P<name>[a-z_]+)(?::4)?\}",
                lambda match: token_values[match.group("name")],
                pattern,
            )

        for role_name, role in self.registry.template_roles.items():
            profile_id = str(role["profiles"][0])
            path_text = witness(str(self.registry.profiles[profile_id]["path_pattern"]))
            with self.subTest(role=role_name, path=path_text):
                self.assertEqual(
                    role_name,
                    profile_module.classify_template_role(
                        pathlib.Path(path_text), profile_id, self.profiles
                    ),
                )

    def test_common_readme_role_covers_every_additional_registered_path(self) -> None:
        readme = self.registry.profiles["readme"]
        for path_text in readme["additional_paths"]:
            with self.subTest(path=path_text):
                self.assertEqual(
                    "common/readme",
                    profile_module.classify_template_role(
                        pathlib.Path(path_text), "readme", self.profiles
                    ),
                )

    def test_common_readme_role_rejects_unregistered_routes(self) -> None:
        for path_text in (
            "docs/not-a-stage/README.md",
            "docs/02.architecture/unknown/README.md",
        ):
            with (
                self.subTest(path=path_text),
                self.assertRaises(profile_module.ProfileError),
            ):
                profile_module.classify_template_role(
                    pathlib.Path(path_text), "readme", self.profiles
                )


class TemplateMetadataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        from scripts.lib.document_governance.registry import load_registry

        cls.profiles = current_profiles()
        cls.registry = load_registry(REGISTRY)

    def test_task_2_copyable_markdown_forms_have_one_h1_and_no_legacy_guidance(
        self,
    ) -> None:
        for role_name, role in self.registry.template_roles.items():
            with self.subTest(role=role_name):
                source = ROOT / str(role["source"])
                if source.suffix != ".md":
                    continue
                text = source.read_text(encoding="utf-8")
                self.assertEqual(
                    1, sum(line.startswith("# ") for line in text.splitlines())
                )
                self.assertNotIn("> Rules:", text)
                self.assertNotIn("<!-- Target:", text)

    def test_task_2_forms_match_their_registered_required_heading_envelopes(
        self,
    ) -> None:
        for role_name, role in self.registry.template_roles.items():
            with self.subTest(role=role_name):
                source = ROOT / str(role["source"])
                if source.suffix != ".md":
                    continue
                profile = self.registry.profiles[str(role["profiles"][0])]
                text = source.read_text(encoding="utf-8")
                headings = [
                    line for line in text.splitlines() if line.startswith("## ")
                ]
                required = [f"## {item}" for item in profile["required_sections"]]
                optional = [f"## {item}" for item in profile["optional_sections"]]
                self.assertLessEqual(set(required), set(headings))
                self.assertLessEqual(set(headings), set(required) | set(optional))

    def test_audit_has_a_distinct_registered_form(self) -> None:
        role = self.registry.template_roles["reference/audit-pack"]
        self.assertEqual(("audit",), role["profiles"])
        self.assertTrue((ROOT / role["source"]).read_bytes())

    def test_retired_governance_forms_have_no_active_registry_role(self) -> None:
        roles = self.registry.template_roles
        self.assertNotIn("memory", roles)
        self.assertNotIn("progress", roles)

    def test_task_has_one_source_and_no_harness_competitor(self) -> None:
        roles = self.registry.template_roles
        task_sources = [
            role["source"] for role in roles.values() if "task" in role["profiles"]
        ]
        self.assertEqual(
            ["docs/99.templates/templates/specs/task.template.md"],
            task_sources,
        )
        self.assertFalse(
            (
                ROOT
                / "docs/99.templates/templates/governance/harness-task-contract.template.md"
            ).exists()
        )

    def test_task_form_contains_protected_surface_and_qa_evidence(self) -> None:
        text = (ROOT / "docs/99.templates/templates/specs/task.template.md").read_text(
            encoding="utf-8"
        )
        for heading in (
            "## Objective",
            "## Inputs",
            "## Work Log",
            "## Verification Evidence",
            "## Review Evidence",
            "## Commit Ledger",
        ):
            with self.subTest(heading=heading):
                self.assertIn(heading, text)

    def test_deleted_harness_task_source_has_no_active_route(self) -> None:
        deleted_path = (
            "docs/99.templates/templates/governance/harness-task-contract.template.md"
        )
        active_route_files = (
            "docs/00.agent-governance/README.md",
            "docs/00.agent-governance/policies/approval-boundaries.md",
            "docs/00.agent-governance/policies/documentation-protocol.md",
            "docs/00.agent-governance/policies/stage-authoring-matrix.md",
            "docs/00.agent-governance/policies/task-checklists.md",
            "docs/99.templates/README.md",
            "docs/99.templates/registry.json",
            "docs/99.templates/templates/README.md",
        )
        for relative_path in active_route_files:
            with self.subTest(path=relative_path):
                text = (ROOT / relative_path).read_text(encoding="utf-8")
                self.assertNotIn(deleted_path, text)

    def test_governance_policy_profile_binds_approval_boundary_body(self) -> None:
        profile = self.registry.profiles["governance-policy"]
        self.assertEqual(("Related Documents",), profile["required_sections"])
        text = (
            ROOT / "docs/00.agent-governance/policies/approval-boundaries.md"
        ).read_text(encoding="utf-8")
        self.assertEqual(
            ["## Related Documents"],
            [line for line in text.splitlines() if line.startswith("## ")],
        )
        for label in ("Core Rules", "Shared-worktree Safeguards", "Protected Surfaces"):
            self.assertIn(f"**{label}**", text)

    def test_stage_99_catalogs_publish_the_current_role_inventory(self) -> None:
        catalogs = {
            "docs/99.templates/README.md": (
                "Requirement Package",
                "Architecture Description",
                "Guide, Policy, Runbook, Incident, and Postmortem",
                "Research, Audit, Data, and Tombstone",
                "transition-only\n  Migration profile",
            ),
            "docs/99.templates/templates/README.md": (
                "Requirement Package",
                "Architecture Description, Architecture Decision",
                "Guide, Policy, Runbook, Incident, Postmortem",
                "Research, Audit, Data",
                "| Archive | `archive/` | Migration, Tombstone |",
            ),
        }
        for relative_path, literal_inventories in catalogs.items():
            with self.subTest(path=relative_path):
                text = (ROOT / relative_path).read_text(encoding="utf-8")
                for literal_inventory in literal_inventories:
                    self.assertIn(literal_inventory, text)
                self.assertNotRegex(
                    text,
                    r"(?<![A-Za-z0-9_-])harness-task-contract(?![A-Za-z0-9_-])",
                )
                self.assertNotIn("Release template", text)

    def test_registered_templates_declare_profile_ids_without_target_paths(
        self,
    ) -> None:
        for role_name, role in self.registry.template_roles.items():
            source = ROOT / str(role["source"])
            with self.subTest(role=role_name):
                self.assertTrue(source.is_file())
                if source.suffix != ".md":
                    continue
                profile = self.registry.profiles[str(role["profiles"][0])]
                values = metadata.parse_frontmatter(source)
                if _declares_provider_binding(profile):
                    # A provider runtime owns this binding, so it carries no type.
                    self.assertIn("name", values)
                    self.assertIn("description", values)
                    self.assertIsNone(values.get("type"))
                    continue
                self.assertEqual(
                    document_type(str(role["profiles"][0])), values.get("type")
                )
                text = source.read_text(encoding="utf-8")
                for target_prefix in (
                    "docs/01.requirements/",
                    "docs/02.architecture/",
                    "docs/03.specs/",
                    "docs/05.operations/",
                    "docs/90.references/",
                    "docs/98.archive/",
                ):
                    self.assertNotIn(target_prefix, text)

    def test_registered_markdown_templates_cover_profile_section_contracts(
        self,
    ) -> None:
        for role_name, role in self.registry.template_roles.items():
            source = ROOT / str(role["source"])
            if source.suffix != ".md":
                continue
            profile = self.registry.profiles[str(role["profiles"][0])]
            text = source.read_text(encoding="utf-8")
            headings = {
                line.removeprefix("## ")
                for line in text.splitlines()
                if line.startswith("## ")
            }
            with self.subTest(role=role_name):
                self.assertLessEqual(set(profile["required_sections"]), headings)
                self.assertEqual(
                    1, sum(line.startswith("# ") for line in text.splitlines())
                )

    def test_release_authority_is_absent(self) -> None:
        self.assertNotIn("release", self.registry.profiles)
        self.assertNotIn("release", self.registry.template_roles)
        self.assertNotIn("release", self.profiles["profiles"])
        self.assertNotIn("release", self.profiles["template_roles"])
        self.assertFalse(
            (
                ROOT / "docs/99.templates/templates/operations/release.template.md"
            ).exists()
        )
        self.assertFalse((ROOT / "docs/05.operations/releases").exists())

    def test_readme_template_uses_registered_minimum_envelope(self) -> None:
        path_text = "docs/99.templates/templates/common/readme-stage.template.md"
        values = metadata.parse_frontmatter(ROOT / path_text)
        self.assertEqual(
            {
                "title": "{{TITLE}}",
                "version": "0.1.0",
                "type": "common/readme",
                "status": "draft",
                "owner": "{{OWNER}}",
                "updated": "{{UPDATED}}",
            },
            values,
        )

    def test_governance_template_source_rejects_typed_leaf_metadata(self) -> None:
        record = metadata.Record(
            pathlib.Path("docs/99.templates/templates/governance/README.md"),
            {
                "status": "draft",
                "artifact_id": "template-source:invalid",
                "artifact_type": "template-source",
                "parent_ids": [],
            },
            "template-source",
            frontmatter_present=True,
        )
        codes = {
            finding.code
            for finding in metadata.validate_record(
                record,
                self.profiles,
                metadata.build_manifest([record]),
            )
        }
        self.assertIn("type-inappropriate-key", codes)
