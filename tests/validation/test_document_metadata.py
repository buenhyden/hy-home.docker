from __future__ import annotations

import collections
import copy
import dataclasses
import datetime as dt
import hashlib
import importlib.util
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

import yaml

from tests.lib.gate.subprocess_support import gate_root_pass_fds


ROOT = pathlib.Path(__file__).resolve().parents[2]
CHECKER = ROOT / "scripts" / "validation" / "check-document-metadata.py"
REGISTRY = ROOT / "docs/99.templates/registry.json"
SERVICE_EXAMPLE = ROOT / "examples" / "sample-web-service" / "service.md"
TARGET_SURFACE_MANIFEST = (
    ROOT
    / "docs/90.references/data/0069-target-surface-convergence/data.yaml"
)
TARGET_SURFACE_SUMMARY = (
    ROOT
    / "docs/90.references/data/governance/document-corpus-lifecycle/target-surface-convergence-summary.md"
)
RETIRING_RESEARCH_PACK_PREFIX = (
    "docs/90.references/research/0001-agentic-research-pack-refresh/"
)
NEW_RESEARCH_PACK_PREFIX = (
    "docs/90.references/research/"
    "2026-08-08-agentic-engineering-research-pack/"
)
# The frozen target-surface manifest is keyed by pre-migration paths, so the
# retiring pack has two names: the dated one it carried at the baseline commit,
# and the numbered one it carries in the live corpus. `5bab8b36` normalised the
# manifest onto the first; the live constants above stay on the second.
PINNED_RESEARCH_PACK_PREFIX = (
    "docs/90.references/research/2026-07-05-agentic-research-pack-refresh/"
)
RETIRING_APPROVED_MIGRATION_PATHS = frozenset(
    {
        f"{RETIRING_RESEARCH_PACK_PREFIX}README.md",
        f"{RETIRING_RESEARCH_PACK_PREFIX}agent-instructions-vibe-coding.md",
        f"{RETIRING_RESEARCH_PACK_PREFIX}agent-model-selection.md",
        f"{RETIRING_RESEARCH_PACK_PREFIX}ai-agent-catalogs.md",
        f"{RETIRING_RESEARCH_PACK_PREFIX}automation-pipeline-workflow.md",
        f"{RETIRING_RESEARCH_PACK_PREFIX}docker-compose-infrastructure.md",
        f"{RETIRING_RESEARCH_PACK_PREFIX}document-metadata-lifecycle.md",
        f"{RETIRING_RESEARCH_PACK_PREFIX}harness-engineering.md",
        f"{RETIRING_RESEARCH_PACK_PREFIX}loop-engineering.md",
        f"{RETIRING_RESEARCH_PACK_PREFIX}provider-implementation-comparison.md",
        f"{RETIRING_RESEARCH_PACK_PREFIX}provider-model-landscape.md",
        f"{RETIRING_RESEARCH_PACK_PREFIX}quality-ci-formatting.md",
        f"{RETIRING_RESEARCH_PACK_PREFIX}sdlc-document-roles.md",
        f"{RETIRING_RESEARCH_PACK_PREFIX}security-governance.md",
        f"{RETIRING_RESEARCH_PACK_PREFIX}spec-driven-sdlc.md",
        f"{RETIRING_RESEARCH_PACK_PREFIX}workspace-baseline.md",
    }
)
PRESERVED_MIGRATION_SENTINELS = frozenset(
    {
    }
)
PRESERVED_AUDIT_MIGRATION_PATHS = frozenset(
    {
        "docs/90.references/audits/0019-readme/README.md",
        "docs/90.references/audits/0020-agent-instructions-catalog-vibe-models/README.md",
        "docs/90.references/audits/0021-automation-candidates/README.md",
        "docs/90.references/audits/0022-compose-infrastructure-operations-readiness/README.md",
        "docs/90.references/audits/0024-frontmatter-template-readme-implementation/README.md",
        "docs/90.references/audits/0025-harness-engineering-implementation/README.md",
        "docs/90.references/audits/0026-implementation-overview/README.md",
        "docs/90.references/audits/0027-loop-engineering-implementation/README.md",
        "docs/90.references/audits/0028-provider-harness-loop-implementation/README.md",
        "docs/90.references/audits/0029-sdlc-document-contracts-implementation/README.md",
        "docs/90.references/audits/0030-sdlc-quality-formatting-implementation/README.md",
        "docs/90.references/audits/0031-security-framework-maturity/README.md",
        "docs/90.references/audits/0032-workspace-rules-environment-implementation/README.md",
    }
)
PRESERVED_RESEARCH_MIGRATION_PATHS = frozenset(
    {
    }
)
PRESERVED_TEMPLATE_MIGRATION_PATHS = frozenset(
    {
        "docs/99.templates/templates/common/readme.template.md",
        "docs/99.templates/templates/operations/guide.template.md",
        "docs/99.templates/templates/operations/incident.template.md",
        "docs/99.templates/templates/operations/policy.template.md",
        "docs/99.templates/templates/operations/postmortem.template.md",
        "docs/99.templates/templates/operations/runbook.template.md",
    }
)
PRESERVED_APPROVED_MIGRATION_PATHS = (
    PRESERVED_MIGRATION_SENTINELS
    | PRESERVED_AUDIT_MIGRATION_PATHS
    | PRESERVED_RESEARCH_MIGRATION_PATHS
    | PRESERVED_TEMPLATE_MIGRATION_PATHS
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


PINNED_TARGET_SURFACE_RESEARCH_PATHS = frozenset(
    {
        f"{PINNED_RESEARCH_PACK_PREFIX}README.md",
        f"{PINNED_RESEARCH_PACK_PREFIX}automation-pipeline-workflow.md",
        f"{PINNED_RESEARCH_PACK_PREFIX}docker-compose-infrastructure.md",
        f"{PINNED_RESEARCH_PACK_PREFIX}document-metadata-lifecycle.md",
        f"{PINNED_RESEARCH_PACK_PREFIX}quality-ci-formatting.md",
        f"{PINNED_RESEARCH_PACK_PREFIX}security-governance.md",
        f"{PINNED_RESEARCH_PACK_PREFIX}workspace-baseline.md",
    }
)
ARCHIVE_TEMPLATE = ROOT / "docs/99.templates/templates/archive/tombstone.template.md"

spec = importlib.util.spec_from_file_location("check_document_metadata", CHECKER)
if spec is None or spec.loader is None:
    raise RuntimeError(f"unable to load checker module: {CHECKER}")
metadata = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = metadata
spec.loader.exec_module(metadata)


def current_profiles() -> dict[str, object]:
    """Project the current Registry into the metadata validator envelope."""

    return metadata.build_registry_profiles(metadata.load_registry(REGISTRY))


class SharedFrontmatterExtractionTests(unittest.TestCase):
    def test_metadata_checker_uses_the_shared_frontmatter_parser(self) -> None:
        from scripts.lib.document_governance import frontmatter

        self.assertIs(frontmatter.read_frontmatter_values, metadata.parse_frontmatter)
        self.assertIs(frontmatter.parse_frontmatter_text, metadata._parse_frontmatter_text)


def write_doc(path: pathlib.Path, frontmatter: dict[str, object] | None, body: str = "# Fixture\n") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if frontmatter is None:
        path.write_text(body, encoding="utf-8")
        return
    if isinstance(frontmatter.get("artifact_type"), str):
        canonical: dict[str, object] = {}
        for key, value in frontmatter.items():
            canonical[key] = value
            if key == "parent_ids":
                canonical["created"] = frontmatter.get("created", "2026-08-07")
                canonical["updated"] = frontmatter.get("updated", "2026-08-07")
        frontmatter = canonical
    rendered = yaml.safe_dump(frontmatter, sort_keys=False).rstrip()
    path.write_text(f"---\n{rendered}\n---\n\n{body}", encoding="utf-8")


def git(root: pathlib.Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True,
        text=True,
        check=False,
    )


def init_git(root: pathlib.Path) -> None:
    initialized = git(root, "init", "-q")
    if initialized.returncode != 0:
        raise RuntimeError(initialized.stderr)
    git(root, "config", "core.hooksPath", "")
    git(root, "config", "user.name", "Metadata Fixture")
    git(root, "config", "user.email", "metadata@example.invalid")
    if git(root, "rev-parse", "--verify", "-q", "HEAD").returncode == 0:
        named = git(root, "branch", "-M", "main")
    else:
        named = git(root, "symbolic-ref", "HEAD", "refs/heads/main")
    if named.returncode != 0:
        raise RuntimeError(named.stderr)
    registry = root / "docs/99.templates/registry.json"
    registry.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(REGISTRY, registry)


def commit_all(root: pathlib.Path, message: str = "fixture") -> None:
    staged = git(root, "add", ".")
    if staged.returncode != 0:
        raise RuntimeError(staged.stderr)
    committed = git(root, "commit", "-qm", message)
    if committed.returncode != 0:
        raise RuntimeError(committed.stderr)


def copy_registry_contract_fixture(root: pathlib.Path) -> pathlib.Path:
    """Copy the current Registry, schemas, and registered template sources."""

    values = json.loads(REGISTRY.read_text(encoding="utf-8"))
    relative_paths = {
        pathlib.Path("README.md"),
        pathlib.Path("docs/05.operations/incidents/README.md"),
        pathlib.Path("docs/99.templates/registry.json"),
        pathlib.Path("docs/99.templates/contracts/document-profile.schema.json"),
        pathlib.Path("docs/99.templates/contracts/frontmatter.schema.json"),
        *(
            pathlib.Path(role["source"])
            for role in values["template_roles"].values()
        ),
    }
    for relative_path in sorted(relative_paths):
        target = root / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / relative_path, target)
    init_git(root)
    staged = git(root, "add", ".")
    if staged.returncode != 0:
        raise RuntimeError(staged.stderr)
    if git(root, "diff", "--cached", "--quiet").returncode != 0:
        committed = git(root, "commit", "-qm", "registry contract fixture")
        if committed.returncode != 0:
            raise RuntimeError(committed.stderr or committed.stdout)
    return root / "docs/99.templates/registry.json"


def body_with_headings(*headings: str) -> str:
    """Build a concrete target body for tests whose subject is not body validation."""

    sections = "\n\n".join(f"{heading}\n\nFixture content." for heading in headings)
    return f"# Fixture\n\n{sections}\n"


def target_promotion_invariant_digest(path: pathlib.Path) -> str:
    """Hash bytes outside the approved promotion and seven semantic corrections."""

    attestation_fields = {
        "docs/03.specs/133-target-surface-contract-convergence/spec.md": "status_after",
        "docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/frontmatter-semantic-inventory.md": "artifact_type_after",
        "docs/90.references/data/knowledge/llm-wiki-stage-category-coverage.md": "artifact_type_after",
        "docs/90.references/llm-wiki/llm-wiki-index.md": "artifact_type_after",
    }
    migrated_generated_outputs = {
        "docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/frontmatter-semantic-inventory.md",
        "docs/90.references/data/knowledge/llm-wiki-stage-category-coverage.md",
        "docs/90.references/llm-wiki/llm-wiki-index.md",
    }
    output: list[bytes] = []
    current_source: str | None = None
    for line in path.read_bytes().splitlines(keepends=True):
        if line.startswith(b"- source_path: "):
            current_source = (
                line.removeprefix(b"- source_path: ").strip().decode("utf-8")
            )
        if (
            line.startswith(b"enforcement: ")
            or line.startswith(b"    specification: ")
            or line.startswith(b"    quality: ")
        ):
            continue
        attestation_field = attestation_fields.get(current_source)
        if attestation_field and line.startswith(f"  {attestation_field}: ".encode("utf-8")):
            continue
        if current_source in migrated_generated_outputs and line.startswith(
            b"  disposition: "
        ):
            continue
        output.append(line)
    return hashlib.sha256(b"".join(output)).hexdigest()


REQUIREMENT_TARGET_BODY = body_with_headings(
    "## Problem and Goals",
    "## Stakeholders and User Needs",
    "## Functional Requirements",
    "## Non-functional Requirements",
    "## Constraints",
    "## Acceptance Criteria",
    "## Traceability",
)

POLICY_TARGET_BODY = body_with_headings(
    "## Purpose",
    "## Scope",
    "## Policy Statements",
    "## Enforcement",
    "## Exceptions",
    "## Verification",
    "## Traceability",
)

def _materialised_profiles() -> pathlib.Path:
    """Return the sole current document-profile authority."""

    return REGISTRY


def run_checker(
    root: pathlib.Path,
    mode: str = "report",
    *extra: str,
    env: dict[str, str] | None = None,
    profiles: pathlib.Path | None = None,
) -> subprocess.CompletedProcess[str]:
    resolved_profiles = _materialised_profiles() if profiles is None else profiles
    return _run_checker_process(
        root,
        mode,
        extra,
        env,
        resolved_profiles,
        gate_root_pass_fds(ROOT),
    )


def _run_checker_process(
    root: pathlib.Path,
    mode: str,
    extra: tuple[str, ...],
    env: dict[str, str] | None,
    resolved_profiles: pathlib.Path,
    descriptors: tuple[int, ...],
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(CHECKER),
            "--root",
            str(root),
            "--profiles",
            str(resolved_profiles),
            "--mode",
            mode,
            *extra,
        ],
        cwd=ROOT,
        env={**os.environ, **(env or {})},
        pass_fds=descriptors,
        capture_output=True,
        text=True,
        check=False,
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
            path.write_text("---\nstatus: active\nstatus: completed\n---\n", encoding="utf-8")
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
            "domain": "00-workspace",
            "stage": "03.specs",
            "slug": "fixture",
            "hook_slug": "fixture",
        }

        def witness(pattern: str) -> str:
            return re.sub(
                r"\{(?P<name>[a-z_]+)(?::4)?\}",
                lambda match: token_values[match.group("name")],
                pattern,
            )

        for role_name, role in self.registry.template_roles.items():
            profile_id = str(role["profile_id"])
            path_text = witness(str(self.registry.profiles[profile_id]["path_pattern"]))
            with self.subTest(role=role_name, path=path_text):
                self.assertEqual(
                    role_name,
                    metadata.classify_template_role(
                        pathlib.Path(path_text), profile_id, self.profiles
                    ),
                )


class TemplateMetadataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        from scripts.lib.document_governance.registry import load_registry

        cls.profiles = current_profiles()
        cls.registry = load_registry(REGISTRY)

    def test_task_2_copyable_markdown_forms_have_one_h1_and_no_legacy_guidance(self) -> None:
        for role_name, role in self.registry.template_roles.items():
            with self.subTest(role=role_name):
                source = ROOT / str(role["source"])
                if source.suffix != ".md":
                    continue
                text = source.read_text(encoding="utf-8")
                self.assertEqual(1, sum(line.startswith("# ") for line in text.splitlines()))
                self.assertNotIn("> Rules:", text)
                self.assertNotIn("<!-- Target:", text)

    def test_task_2_forms_match_their_registered_required_heading_envelopes(self) -> None:
        for role_name, role in self.registry.template_roles.items():
            with self.subTest(role=role_name):
                source = ROOT / str(role["source"])
                if source.suffix != ".md":
                    continue
                profile = self.registry.profiles[str(role["profile_id"])]
                text = source.read_text(encoding="utf-8")
                headings = [line for line in text.splitlines() if line.startswith("## ")]
                required = [f"## {item}" for item in profile["required_sections"]]
                optional = [f"## {item}" for item in profile["optional_sections"]]
                self.assertLessEqual(set(required), set(headings))
                self.assertLessEqual(set(headings), set(required) | set(optional))

    def test_audit_has_a_distinct_registered_form(self) -> None:
        role = self.registry.template_roles["references/audit"]
        self.assertEqual("audit", role["profile_id"])
        self.assertTrue((ROOT / role["source"]).read_bytes())

    def test_retired_governance_forms_have_no_active_registry_role(self) -> None:
        roles = self.registry.template_roles
        self.assertNotIn("memory", roles)
        self.assertNotIn("progress", roles)

    def test_task_has_one_source_and_no_harness_competitor(self) -> None:
        roles = self.registry.template_roles
        task_sources = [
            role["source"]
            for role in roles.values()
            if role["profile_id"] == "task"
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
        text = (
            ROOT / "docs/99.templates/templates/specs/task.template.md"
        ).read_text(encoding="utf-8")
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
            "docs/99.templates/templates/governance/"
            "harness-task-contract.template.md"
        )
        active_route_files = (
            "docs/00.agent-governance/README.md",
            "docs/00.agent-governance/policies/approval-boundaries.md",
            "docs/00.agent-governance/policies/documentation-protocol.md",
            "docs/00.agent-governance/policies/stage-authoring-matrix.md",
            "docs/00.agent-governance/policies/task-checklists.md",
            "docs/99.templates/README.md",
            "docs/99.templates/registry.json",
            "docs/99.templates/templates/governance/README.md",
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
        self.assertEqual(["## Related Documents"], [
            line for line in text.splitlines() if line.startswith("## ")
        ])
        for label in ("Core Rules", "Shared-worktree Safeguards", "Protected Surfaces"):
            self.assertIn(f"**{label}**", text)

    def test_stage_99_catalogs_publish_the_literal_canonical_role_inventory(self) -> None:
        catalogs = {
            "docs/99.templates/README.md": (
                "Requirement Package",
                "Architecture Description",
                "Guide, Policy, Runbook, Incident, and Postmortem",
                "Research, Audit, Data, Migration, and Tombstone",
            ),
            "docs/99.templates/templates/README.md": (
                "Requirement Package",
                "Architecture Description, ADR",
                "Guide, Policy, Runbook, Incident, Postmortem",
                "Research, Audit, Data",
                "Migration, Tombstone",
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

    def test_registered_templates_declare_profile_ids_without_target_paths(self) -> None:
        for role_name, role in self.registry.template_roles.items():
            source = ROOT / str(role["source"])
            with self.subTest(role=role_name):
                self.assertTrue(source.is_file())
                if source.suffix != ".md":
                    continue
                values = metadata.parse_frontmatter(source)
                self.assertEqual(role["profile_id"], values.get("profile_id"))
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


    def test_registered_markdown_templates_cover_profile_section_contracts(self) -> None:
        for role_name, role in self.registry.template_roles.items():
            source = ROOT / str(role["source"])
            if source.suffix != ".md":
                continue
            profile = self.registry.profiles[str(role["profile_id"])]
            text = source.read_text(encoding="utf-8")
            headings = {
                line.removeprefix("## ")
                for line in text.splitlines()
                if line.startswith("## ")
            }
            with self.subTest(role=role_name):
                self.assertLessEqual(set(profile["required_sections"]), headings)
                self.assertEqual(1, sum(line.startswith("# ") for line in text.splitlines()))


    def test_release_authority_is_absent(self) -> None:
        self.assertNotIn("release", self.registry.profiles)
        self.assertNotIn("release", self.registry.template_roles)
        self.assertNotIn("release", self.profiles["profiles"])
        self.assertNotIn("release", self.profiles["template_roles"])
        self.assertFalse(
            (ROOT / "docs/99.templates/templates/operations/release.template.md").exists()
        )
        self.assertFalse((ROOT / "docs/05.operations/releases").exists())

    def test_readme_template_remains_a_readme_exception_source(self) -> None:
        path_text = "docs/99.templates/templates/common/readme.template.md"
        values = metadata.parse_frontmatter(ROOT / path_text)
        self.assertEqual({"status": "draft"}, values)

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
                "profile_id: requirements-package",
                "profile_id: spec",
                "template-profile-mismatch",
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


class CheckerCliTests(unittest.TestCase):
    def test_duplicate_artifact_id_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            values = {
                "status": "active",
                "artifact_id": "SPEC-123",
                "artifact_type": "spec",
                "parent_ids": [],
            }
            write_doc(root / "docs/03.specs/spec-0123-a/spec.md", values)
            write_doc(root / "docs/03.specs/spec-0123-b/spec.md", values)
            result = run_checker(root, "report")
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertIn("duplicate-artifact-id", result.stdout)
            self.assertIn("| duplicate |", result.stdout)

    def test_duplicate_yaml_key_has_distinct_inventory_state(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            path = root / "docs/03.specs/spec-0123-example/spec.md"
            path.parent.mkdir(parents=True)
            path.write_text("---\nstatus: active\nstatus: completed\n---\n", encoding="utf-8")
            result = run_checker(root, "report")
            self.assertEqual(2, result.returncode)
            self.assertIn("frontmatter-duplicate-key", result.stdout)
            self.assertIn("| duplicate-key |", result.stdout)

    def test_report_returns_nonzero_for_parser_failure_but_renders_inventory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            path = root / "docs/03.specs/spec-0123-example/spec.md"
            path.parent.mkdir(parents=True)
            path.write_text("---\nstatus: [active\n---\n", encoding="utf-8")
            result = run_checker(root, "report")
            self.assertNotEqual(0, result.returncode)
            self.assertIn("frontmatter-malformed-yaml", result.stdout)
            self.assertIn(path.relative_to(root).as_posix(), result.stdout)

    def test_unhashable_mapping_key_has_no_traceback_and_writes_inventory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            path = root / "docs/03.specs/spec-0123-example/spec.md"
            path.parent.mkdir(parents=True)
            path.write_text("---\n? [a, b]: c\n---\n", encoding="utf-8")
            output = root / "inventory.md"
            result = run_checker(root, "report", "--output", str(output))
            self.assertEqual(2, result.returncode)
            self.assertNotIn("Traceback", result.stderr)
            rendered = output.read_text(encoding="utf-8")
            self.assertIn("frontmatter-malformed-yaml", rendered)
            self.assertIn("malformed-yaml", rendered)

    def test_report_order_is_deterministic_and_sorted_by_path(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            write_doc(root / "docs/03.specs/spec-0200-z/spec.md", {"status": "active"})
            write_doc(root / "docs/01.requirements/prd-0100-a.md", {"status": "active"})
            first = run_checker(root, "report")
            second = run_checker(root, "report")
            self.assertEqual(first.stdout, second.stdout)
            self.assertLess(
                first.stdout.index("docs/01.requirements/prd-0100-a.md"),
                first.stdout.index("docs/03.specs/spec-0200-z/spec.md"),
            )

    def test_report_output_check_detects_staleness(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            write_doc(root / "docs/03.specs/README.md", None)
            output = root / "inventory.md"
            generated = run_checker(root, "report", "--output", str(output))
            fresh = run_checker(root, "report", "--output", str(output), "--check")
            output.write_text("stale\n", encoding="utf-8")
            stale = run_checker(root, "report", "--output", str(output), "--check")
            self.assertEqual(0, generated.returncode, generated.stderr)
            self.assertEqual(0, fresh.returncode, fresh.stderr)
            self.assertNotEqual(0, stale.returncode)
            self.assertIn("metadata inventory is stale", stale.stderr)

    def test_active_mode_is_available_but_semantic_gate_is_not_auto_invoked(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            write_doc(root / "docs/03.specs/spec-0123-example/spec.md", {"status": "active"})
            result = run_checker(root, "check-active")
            self.assertNotEqual(0, result.returncode)
            self.assertIn("metadata check-active", result.stdout)

    def test_inventory_exposes_all_semantic_state_columns(self) -> None:
        profiles = current_profiles()
        records = [
            metadata.Record(
                pathlib.Path("docs/03.specs/README.md"),
                {"profile_id": "readme", "status": "active"},
                "readme",
                frontmatter_present=True,
            ),
            metadata.Record(
                pathlib.Path(
                    "docs/90.references/data/0001-generated/generated.md"
                ),
                {
                    "profile_id": "generated",
                    "status": "active",
                    "generated_by": "scripts/example.py",
                },
                "generated",
                frontmatter_present=True,
            ),
        ]
        manifest = metadata.build_manifest(records)
        findings = {
            record.path.as_posix(): metadata.validate_record(
                record,
                profiles,
                manifest,
            )
            for record in records
        }
        rendered = metadata.render_report(records, profiles, findings)
        self.assertIn(
            "| Path | Profile | Frontmatter | Identity | Relations | Lifecycle | Transition Evidence | Freshness | Exception Context | Findings | Disposition |",
            rendered,
        )
        self.assertIn("allowed-syntax", rendered)
        self.assertIn(
            "README profile=unclassified; consumer=unavailable; role=folder-index",
            rendered,
        )
        self.assertIn("generated profile; owner=scripts/example.py", rendered)
        self.assertIn("reviewed_at=forbidden:not-provided", rendered)

    def test_inventory_records_identity_relations_and_transition_evidence(self) -> None:
        profiles = current_profiles()
        parent = metadata.Record(
            pathlib.Path("docs/02.architecture/descriptions/ad-0123-parent.md"),
            {
                "status": "active",
                "artifact_id": "architecture-description:0123-parent",
                "artifact_type": "architecture-description",
                "parent_ids": [],
                "created": "2026-08-07",
                "updated": "2026-08-07",
            },
            "architecture-description",
            frontmatter_present=True,
        )
        child = metadata.Record(
            pathlib.Path("docs/03.specs/spec-0123-child/spec.md"),
            {
                "status": "completed",
                "artifact_id": "spec:0123-child",
                "artifact_type": "spec",
                "parent_ids": ["architecture-description:0123-parent"],
                "created": "2026-08-07",
                "updated": "2026-08-07",
            },
            "spec",
            previous_status="active",
            frontmatter_present=True,
        )
        records = [parent, child]
        manifest = metadata.build_manifest(records)
        findings = {
            record.path.as_posix(): metadata.validate_record(record, profiles, manifest) for record in records
        }
        report = metadata.render_report(records, profiles, findings)
        child_row = next(line for line in report.splitlines() if "docs/03.specs/spec-0123-child/spec.md" in line)
        self.assertIn("| valid | parents=resolved:1; order=declared-list; supersedes=not-provided |", child_row)
        self.assertIn("available:active->completed; valid", child_row)


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


class TransitionOverrideEvidencePathTests(unittest.TestCase):
    """The override's evidence path must name a Task form this repository has.

    `load_transition_overrides` required `docs/03.specs/spec-<slug>/task.md`.
    This repository has zero documents in that form and fifteen in the
    co-located `docs/03.specs/####-<slug>/tasks/tsk-####-<slug>.md` form, so
    every override was rejected while the error text said the evidence "must be
    an existing co-located Task". SPEC-0155 acceptance item 13 owns the
    correction.
    """

    def _override_file(self, root: pathlib.Path, evidence: str) -> pathlib.Path:
        override = root / "override.yaml"
        override.write_text(
            "transition_overrides:\n"
            "- path: docs/03.specs/0001-fixture/spec.md\n"
            "  previous_status: completed\n"
            "  new_status: active\n"
            f"  evidence_task: {evidence}\n"
            "  approval: reviewer\n"
            "  reason: corrects a mis-recorded status\n",
            encoding="utf-8",
        )
        return override

    def _tree(self, root: pathlib.Path, evidence: str) -> None:
        target = root / "docs/03.specs/0001-fixture/spec.md"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("# Fixture\n", encoding="utf-8")
        witness = root / evidence
        witness.parent.mkdir(parents=True, exist_ok=True)
        witness.write_text("# Task\n", encoding="utf-8")

    def test_co_located_task_evidence_is_accepted(self) -> None:
        evidence = "docs/03.specs/0001-fixture/tasks/tsk-0001-fixture.md"
        with tempfile.TemporaryDirectory() as raw:
            root = pathlib.Path(raw)
            self._tree(root, evidence)
            overrides = metadata.load_transition_overrides(
                self._override_file(root, evidence),
                root,
                metadata.build_registry_profiles(metadata.load_registry(REGISTRY)),
            )
        self.assertEqual(1, len(overrides))

    def test_the_retired_spec_slash_task_form_is_rejected(self) -> None:
        evidence = "docs/03.specs/spec-0001-fixture/task.md"
        with tempfile.TemporaryDirectory() as raw:
            root = pathlib.Path(raw)
            self._tree(root, evidence)
            with self.assertRaises(metadata.ProfileError):
                metadata.load_transition_overrides(
                    self._override_file(root, evidence),
                    root,
                    metadata.build_registry_profiles(metadata.load_registry(REGISTRY)),
                )


if __name__ == "__main__":
    unittest.main()
