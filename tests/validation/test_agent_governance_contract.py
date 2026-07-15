from __future__ import annotations

import dataclasses
import importlib.util
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


ROOT = pathlib.Path(__file__).resolve().parents[2]
CHECKER = ROOT / "scripts/validation/check-agent-governance-contract.py"
MODULE = ROOT / "scripts/validation/agent_governance_contract.py"
CONTRACT_DIR = ROOT / "docs/00.agent-governance/contracts"
CONTRACT_FILES = (
    "agent-governance-artifacts.yaml",
    "agent-catalog.yaml",
    "provider-models.yaml",
)

spec = importlib.util.spec_from_file_location("agent_governance_contract", MODULE)
if spec is None or spec.loader is None:
    raise RuntimeError(f"unable to load contract module: {MODULE}")
contract = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = contract
spec.loader.exec_module(contract)


def copy_contracts(root: pathlib.Path) -> None:
    target = root / "docs/00.agent-governance/contracts"
    target.mkdir(parents=True, exist_ok=True)
    for name in CONTRACT_FILES:
        shutil.copy2(CONTRACT_DIR / name, target / name)


def copy_task2_harness_surfaces(root: pathlib.Path) -> None:
    """Copy the registered Task 2 repository projection into a fixture root."""

    copy_contracts(root)
    for relative_path in (
        "AGENTS.md",
        "CLAUDE.md",
        "GEMINI.md",
        ".agents/README.md",
        ".claude/CLAUDE.md",
        ".codex/README.md",
        "scripts/README.md",
    ):
        source = ROOT / relative_path
        target = root / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    governance = root / "docs/00.agent-governance"
    shutil.copytree(
        ROOT / "docs/00.agent-governance",
        governance,
        dirs_exist_ok=True,
    )


def mutate_yaml(root: pathlib.Path, name: str, mutate) -> None:
    path = root / "docs/00.agent-governance/contracts" / name
    values = yaml.safe_load(path.read_text(encoding="utf-8"))
    mutate(values)
    path.write_text(yaml.safe_dump(values, sort_keys=False), encoding="utf-8")


def validate_fixture(root: pathlib.Path) -> list[object]:
    bundle = contract.load_contract_bundle(root)
    return contract.validate_contract_bundle(root, bundle)


def codes(findings: list[object]) -> set[str]:
    return {finding.code for finding in findings}


class ContractLoadingTests(unittest.TestCase):
    def test_missing_markdown_parser_dependency_fails_contract_loading(self) -> None:
        with mock.patch.object(contract, "_MarkdownIt", None):
            with self.assertRaises(contract.ContractLoadError) as context:
                contract.load_contract_bundle(ROOT)
        self.assertEqual("AGC-DEPENDENCY-MISSING", context.exception.code)
        self.assertEqual("markdown-it-py", context.exception.path)

    def test_canonical_contracts_are_valid_and_have_target_counts(self) -> None:
        bundle = contract.load_contract_bundle(ROOT)
        self.assertEqual([], contract.validate_contract_bundle(ROOT, bundle))
        self.assertEqual(14, len(bundle.catalog["agents"]))
        self.assertEqual(22, len(bundle.catalog["functions"]))
        self.assertEqual(3, len(bundle.providers["providers"]))

    def test_bundle_and_findings_are_immutable(self) -> None:
        bundle = contract.load_contract_bundle(ROOT)
        finding = contract.Finding(
            code="AGC-TEST",
            path="test",
            location="field",
            expected="expected-kind",
            actual="actual-kind",
            source="fixture",
        )
        with self.assertRaises(dataclasses.FrozenInstanceError):
            bundle.catalog = {}  # type: ignore[misc]
        with self.assertRaises(TypeError):
            bundle.catalog["agents"] = ()  # type: ignore[index]
        with self.assertRaises(dataclasses.FrozenInstanceError):
            finding.code = "changed"  # type: ignore[misc]

    def test_duplicate_yaml_keys_are_rejected_without_values(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_contracts(root)
            path = root / "docs/00.agent-governance/contracts/agent-catalog.yaml"
            path.write_text(
                path.read_text(encoding="utf-8") + "\nschema_version: 999\n",
                encoding="utf-8",
            )
            with self.assertRaises(contract.ContractLoadError) as context:
                contract.load_contract_bundle(root)
            self.assertEqual("AGC-YAML-DUPLICATE-KEY", context.exception.code)
            self.assertNotIn("999", str(context.exception))

    def test_non_string_yaml_key_collision_is_rejected_before_freeze(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_contracts(root)
            path = root / "docs/00.agent-governance/contracts/agent-catalog.yaml"
            path.write_text(
                path.read_text(encoding="utf-8")
                + "\n1: sentinel-numeric-key\n'1': sentinel-string-key\n",
                encoding="utf-8",
            )
            with self.assertRaises(contract.ContractLoadError) as context:
                contract.load_contract_bundle(root)
            self.assertEqual("AGC-YAML-NONSTRING-KEY", context.exception.code)
            self.assertNotIn("sentinel", str(context.exception))

    def test_fixed_contract_paths_reject_external_symlinks_without_reading_targets(self) -> None:
        for relative in contract.CONTRACT_RELATIVE_PATHS.values():
            with self.subTest(relative=relative), tempfile.TemporaryDirectory() as directory:
                root = pathlib.Path(directory)
                copy_contracts(root)
                outside = root.parent / f"outside-{pathlib.Path(relative).name}"
                outside.write_text("outside-sentinel: true\n", encoding="utf-8")
                path = root / relative
                path.unlink()
                path.symlink_to(outside)
                try:
                    with self.assertRaises(contract.ContractLoadError) as context:
                        contract.load_contract_bundle(root)
                    self.assertEqual("AGC-CONTRACT-UNSAFE-FILE", context.exception.code)
                    self.assertEqual(relative.as_posix(), context.exception.path)
                    self.assertNotIn("outside-sentinel", str(context.exception))
                finally:
                    outside.unlink(missing_ok=True)

    def test_contract_reader_fails_closed_for_nonregular_encoding_and_read_errors(self) -> None:
        original_open = os.open
        original_read = os.read
        cases = (
            ("nonregular-directory", "AGC-CONTRACT-UNSAFE-FILE"),
            ("nonregular-fifo", "AGC-CONTRACT-UNSAFE-FILE"),
            ("encoding", "AGC-CONTRACT-ENCODING"),
            ("read", "AGC-CONTRACT-READ"),
        )
        for relative in contract.CONTRACT_RELATIVE_PATHS.values():
            for mutation, expected in cases:
                with self.subTest(
                    relative=relative, mutation=mutation
                ), tempfile.TemporaryDirectory() as directory:
                    root = pathlib.Path(directory)
                    copy_contracts(root)
                    path = root / relative
                    if mutation == "nonregular-directory":
                        path.unlink()
                        path.mkdir()
                    elif mutation == "nonregular-fifo":
                        path.unlink()
                        os.mkfifo(path)
                    elif mutation == "encoding":
                        path.write_bytes(b"\xff\xfe")
                    if mutation == "read":
                        target_fd: int | None = None

                        def record_target_open(
                            candidate, flags: int, mode: int = 0o777, *, dir_fd=None
                        ) -> int:
                            nonlocal target_fd
                            descriptor = original_open(
                                candidate, flags, mode, dir_fd=dir_fd
                            )
                            if candidate == relative.name and dir_fd is not None:
                                target_fd = descriptor
                            return descriptor

                        def fail_target_read(descriptor: int, size: int) -> bytes:
                            if descriptor == target_fd:
                                raise PermissionError("read-sentinel")
                            return original_read(descriptor, size)

                        with mock.patch.object(
                            contract.os, "open", new=record_target_open
                        ), mock.patch.object(
                            contract.os, "read", new=fail_target_read
                        ):
                            with self.assertRaises(
                                contract.ContractLoadError
                            ) as context:
                                contract.load_contract_bundle(root)
                    else:
                        with self.assertRaises(contract.ContractLoadError) as context:
                            contract.load_contract_bundle(root)
                    self.assertEqual(expected, context.exception.code)
                    self.assertEqual(relative.as_posix(), context.exception.path)
                    self.assertNotIn(directory, str(context.exception))

    def test_contract_reader_opens_and_reads_the_same_confined_file_descriptor(self) -> None:
        relative = contract.CONTRACT_RELATIVE_PATHS["artifacts"]
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_contracts(root)
            path = root / relative
            outside = root.parent / "outside-agent-governance-artifacts.yaml"
            outside.write_text(
                path.read_text(encoding="utf-8") + "\n# outside-sentinel\n",
                encoding="utf-8",
            )
            original_open = os.open
            swapped = False

            def swap_before_final_open(
                candidate, flags: int, mode: int = 0o777, *, dir_fd=None
            ) -> int:
                nonlocal swapped
                if candidate == relative.name and dir_fd is not None and not swapped:
                    path.unlink()
                    path.symlink_to(outside)
                    swapped = True
                return original_open(candidate, flags, mode, dir_fd=dir_fd)

            try:
                with mock.patch.object(
                    contract.os, "open", new=swap_before_final_open
                ), mock.patch.object(
                    pathlib.Path,
                    "read_text",
                    side_effect=AssertionError("path was reopened after validation"),
                ):
                    with self.assertRaises(contract.ContractLoadError) as context:
                        contract.load_contract_bundle(root)
                self.assertTrue(swapped)
                self.assertEqual("AGC-CONTRACT-UNSAFE-FILE", context.exception.code)
                self.assertNotIn("outside-sentinel", str(context.exception))
            finally:
                outside.unlink(missing_ok=True)


class ContractSchemaTests(unittest.TestCase):
    def test_artifact_profiles_require_unique_ids_sections_and_registered_values(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_contracts(root)

            def mutate(values) -> None:
                values["artifacts"][1]["profile_id"] = values["artifacts"][0][
                    "profile_id"
                ]
                values["artifacts"][2]["repository_section"] = "unknown"
                values["artifacts"][2]["expected_values"]["legacy"] = True

            mutate_yaml(root, "agent-governance-artifacts.yaml", mutate)
            observed = codes(validate_fixture(root))
            self.assertIn("AGC-SCHEMA-DUPLICATE-ID", observed)
            self.assertIn("AGC-SCHEMA-INVALID-ENUM", observed)
            self.assertIn("AGC-ARTIFACT-EXPECTED-KEY", observed)

    def test_artifact_profile_patterns_must_not_intersect(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_contracts(root)

            def mutate(values) -> None:
                values["artifacts"][1]["path_pattern"] = values["artifacts"][0][
                    "path_pattern"
                ]

            mutate_yaml(root, "agent-governance-artifacts.yaml", mutate)
            self.assertIn(
                "AGC-ARTIFACT-PROFILE-OVERLAP",
                codes(validate_fixture(root)),
            )

    def test_artifact_pattern_overlap_fails_closed_for_recursive_and_class_globs(self) -> None:
        self.assertTrue(
            contract._artifact_patterns_overlap("docs/*/**", "docs/a/**")
        )
        self.assertTrue(
            contract._artifact_patterns_overlap(
                "docs/[ab]foo.md", "docs/[bc]foo.md"
            )
        )

    def test_enumerated_patterns_reject_unsupported_glob_grammar(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_contracts(root)
            mutate_yaml(
                root,
                "agent-governance-artifacts.yaml",
                lambda values: values["readme_profiles"][0].update(
                    {"path_pattern": "docs/***/README.md"}
                ),
            )
            self.assertIn("AGC-PATTERN-UNSUPPORTED", codes(validate_fixture(root)))

    def test_enumerated_patterns_validate_every_expanded_brace_choice(self) -> None:
        for pattern in (
            "{..,docs}/x",
            "docs/{../..,safe}/x",
            "{safe,/tmp}/x",
        ):
            with self.subTest(pattern=pattern), tempfile.TemporaryDirectory() as directory:
                root = pathlib.Path(directory)
                copy_contracts(root)
                mutate_yaml(
                    root,
                    "agent-governance-artifacts.yaml",
                    lambda values, pattern=pattern: values["readme_profiles"][0].update(
                        {"path_pattern": pattern}
                    ),
                )
                self.assertIn("AGC-PATH-UNSAFE", codes(validate_fixture(root)))

    def test_governed_families_require_typed_safe_fields(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_contracts(root)

            def mutate(values) -> None:
                values["governed_families"][0]["legacy"] = True
                del values["governed_families"][1]["repository_sections"]
                values["governed_families"][2]["path_pattern"] = "../outside/**"

            mutate_yaml(root, "agent-governance-artifacts.yaml", mutate)
            observed = codes(validate_fixture(root))
            self.assertIn("AGC-SCHEMA-UNKNOWN-FIELD", observed)
            self.assertIn("AGC-SCHEMA-MISSING-FIELD", observed)
            self.assertIn("AGC-PATH-UNSAFE", observed)

    def test_root_and_readme_profiles_require_exact_contract_fields(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_contracts(root)

            def mutate(values) -> None:
                del values["root_shims"][0]["provider_target"]
                values["root_shims"][1]["import_style"] = "literal-fence"
                del values["readme_profiles"][0]["required_sections"]

            mutate_yaml(root, "agent-governance-artifacts.yaml", mutate)
            observed = codes(validate_fixture(root))
            self.assertIn("AGC-SCHEMA-MISSING-FIELD", observed)
            self.assertIn("AGC-SCHEMA-INVALID-ENUM", observed)

    def test_unknown_top_level_key_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_contracts(root)
            mutate_yaml(
                root,
                "agent-governance-artifacts.yaml",
                lambda values: values.update({"unexpected": True}),
            )
            self.assertIn("AGC-SCHEMA-UNKNOWN-FIELD", codes(validate_fixture(root)))

    def test_absolute_and_traversal_paths_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_contracts(root)

            def mutate(values) -> None:
                values["root_shims"][0]["path"] = "/tmp/private"
                values["path_authority"][0]["path_patterns"][0] = "../outside/**"

            mutate_yaml(root, "agent-governance-artifacts.yaml", mutate)
            findings = validate_fixture(root)
            self.assertEqual(2, sum(item.code == "AGC-PATH-UNSAFE" for item in findings))

    def test_control_and_noncanonical_repo_paths_are_rejected(self) -> None:
        for value in (
            "",
            "line\nbreak",
            ".",
            "..",
            "double//slash",
            "dot/./segment",
            "back\\slash",
        ):
            with self.subTest(value=repr(value)):
                self.assertFalse(contract._is_safe_repo_path(value))
        self.assertTrue(contract._is_safe_repo_path("docs/**/{rules,scopes}/*.md"))

        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_contracts(root)

            def mutate(values) -> None:
                paths = [
                    "line\nbreak",
                    ".",
                    "..",
                    "double//slash",
                    "dot/./segment",
                    "back\\slash",
                ]
                for index, value in enumerate(paths):
                    values["path_authority"][index]["path_patterns"][0] = value

            mutate_yaml(root, "agent-governance-artifacts.yaml", mutate)
            findings = validate_fixture(root)
            self.assertEqual(6, sum(item.code == "AGC-PATH-UNSAFE" for item in findings))

    def test_canonically_equivalent_authority_patterns_still_overlap(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_contracts(root)

            def mutate(values) -> None:
                values["path_authority"][0]["path_patterns"][0] = "zz/target"
                values["path_authority"][1]["path_patterns"][0] = "zz/./target"

            mutate_yaml(root, "agent-governance-artifacts.yaml", mutate)
            findings = validate_fixture(root)
            self.assertIn("AGC-PATH-UNSAFE", codes(findings))
            self.assertIn("AGC-AUTHORITY-OVERLAP", codes(findings))

    def test_glob_authority_overlap_fails_closed_at_literal_prefixes(self) -> None:
        cases = (
            ("zz/a*", "zz/ab?", True),
            ("zz/**", "zz/alpha", True),
            ("zz/a?", "zz/ab", True),
            ("zz/[ab]*", "zz/alpha", True),
            ("zz/[ab]*", "zz/[cd]*", True),
            ("zz/{alpha,beta}", "zz/alpha", True),
            ("zz/alpha", "zz/a*", True),
            ("zz/a*", "zz/a/child", True),
            ("zz/alpha", "zz/alpha", True),
            ("zz/a*", "zz/b?", False),
            ("zz/a/**", "zz/ab/**", False),
            ("zz/alpha", "zz/alphabet", False),
            ("zz/a", "zz/a/child", False),
            ("zz/alpha", "zz/b*", False),
        )
        for left, right, expected in cases:
            with self.subTest(left=left, right=right):
                self.assertEqual(expected, contract._patterns_overlap(left, right))
                self.assertEqual(expected, contract._patterns_overlap(right, left))

        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_contracts(root)

            def mutate(values) -> None:
                values["path_authority"][0]["path_patterns"][0] = "zz/a*"
                values["path_authority"][1]["path_patterns"][0] = "zz/ab?"

            mutate_yaml(root, "agent-governance-artifacts.yaml", mutate)
            self.assertIn("AGC-AUTHORITY-OVERLAP", codes(validate_fixture(root)))

    def test_scalar_provider_collections_return_schema_findings(self) -> None:
        for field in ("providers", "compatibility_surfaces", "work_profiles"):
            with self.subTest(field=field), tempfile.TemporaryDirectory() as directory:
                root = pathlib.Path(directory)
                copy_contracts(root)
                mutate_yaml(
                    root,
                    "provider-models.yaml",
                    lambda values, field=field: values.update({field: 1}),
                )
                findings = validate_fixture(root)
                self.assertEqual(findings, validate_fixture(root))
                matching = [
                    item
                    for item in findings
                    if item.code == "AGC-SCHEMA-TYPE" and item.location == field
                ]
                self.assertEqual(1, len(matching))
                self.assertNotIn(str(root), contract.render_findings(findings))

    def test_unhashable_reference_scalars_return_deterministic_findings(self) -> None:
        sentinel = "sentinel-unhashable-reference"
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_contracts(root)

            def mutate_catalog(values) -> None:
                values["agents"][0]["scope"] = [sentinel]
                values["agents"][0]["permission_profile"] = {"id": sentinel}
                values["agents"][0]["work_profile"] = [sentinel]
                values["functions"][0]["scope"] = {"id": sentinel}
                values["functions"][0]["owner_agent"] = [sentinel]
                values["capability_intake"][0]["owner_agent"] = {"id": sentinel}
                values["capability_intake"][0]["evaluation_function"] = [sentinel]

            def mutate_artifacts(values) -> None:
                values["path_authority"][0]["canonical_owner"] = [sentinel]
                values["path_authority"][0]["permitted_contributors"] = [[sentinel]]

            def mutate_providers(values) -> None:
                values["models"][0]["provider"] = [sentinel]
                values["semantic_events"][0]["provider_bindings"][0]["provider"] = {
                    "id": sentinel
                }

            mutate_yaml(root, "agent-catalog.yaml", mutate_catalog)
            mutate_yaml(root, "agent-governance-artifacts.yaml", mutate_artifacts)
            mutate_yaml(root, "provider-models.yaml", mutate_providers)
            first = validate_fixture(root)
            second = validate_fixture(root)
            self.assertEqual(first, second)
            self.assertIn("AGC-CATALOG-UNKNOWN-REFERENCE", codes(first))
            self.assertIn("AGC-SCHEMA-TYPE", codes(first))
            rendered = contract.render_findings(first)
            self.assertNotIn(sentinel, rendered)
            self.assertNotIn(str(root), rendered)

    def test_duplicate_agent_and_function_ids_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_contracts(root)

            def mutate(values) -> None:
                values["agents"][1]["agent_id"] = values["agents"][0]["agent_id"]
                values["functions"][1]["function_id"] = values["functions"][0]["function_id"]

            mutate_yaml(root, "agent-catalog.yaml", mutate)
            findings = validate_fixture(root)
            duplicate_locations = [
                item.location
                for item in findings
                if item.code == "AGC-CATALOG-DUPLICATE-ID"
            ]
            self.assertEqual(["agents", "functions"], duplicate_locations)

    def test_invalid_catalog_cross_references_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_contracts(root)

            def mutate(values) -> None:
                values["agents"][0]["function_ids"] = ["missing-function"]
                values["functions"][0]["owner_agent"] = "missing-agent"
                values["role_transfers"][0]["successor_agent_ids"] = ["missing-agent"]

            mutate_yaml(root, "agent-catalog.yaml", mutate)
            findings = validate_fixture(root)
            locations = {
                item.location
                for item in findings
                if item.code == "AGC-CATALOG-UNKNOWN-REFERENCE"
            }
            self.assertTrue(
                {
                    "agents.ci-cd-engineer.function_ids",
                    "functions[0].owner_agent",
                    "path_authority[0].entry_reviewers[0].agent_field",
                    "role_transfers[0].successor_agent_ids",
                }
                <= locations,
                locations,
            )

    def test_overlapping_canonical_ownership_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_contracts(root)

            def mutate(values) -> None:
                values["path_authority"][1]["path_patterns"][0] = values["path_authority"][0][
                    "path_patterns"
                ][0]

            mutate_yaml(root, "agent-governance-artifacts.yaml", mutate)
            self.assertIn("AGC-AUTHORITY-OVERLAP", codes(validate_fixture(root)))

    def test_role_catalog_requires_domain_owner_and_rules_engineer_authority(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_contracts(root)

            def mutate(values) -> None:
                authority = next(
                    item
                    for item in values["path_authority"]
                    if item["authority_id"] == "agent-role-catalog"
                )
                authority["canonical_owner"] = "doc-writer"
                authority["entry_owners"] = []

            mutate_yaml(root, "agent-governance-artifacts.yaml", mutate)
            findings = validate_fixture(root)
            locations = {
                item.location
                for item in findings
                if item.code == "AGC-AUTHORITY-SEMANTICS"
            }
            self.assertEqual(
                {
                    "path_authority[1].canonical_owner",
                    "path_authority[1].entry_owners",
                },
                locations,
            )

    def test_function_catalog_requires_skill_creator_and_domain_owner_review(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_contracts(root)

            def mutate(values) -> None:
                authority = next(
                    item
                    for item in values["path_authority"]
                    if item["authority_id"] == "agent-function-catalog"
                )
                authority["canonical_owner"] = "rules-engineer"
                authority["entry_reviewers"] = []

            mutate_yaml(root, "agent-governance-artifacts.yaml", mutate)
            findings = validate_fixture(root)
            locations = {
                item.location
                for item in findings
                if item.code == "AGC-AUTHORITY-SEMANTICS"
            }
            self.assertEqual(
                {
                    "path_authority[0].canonical_owner",
                    "path_authority[0].entry_reviewers",
                    "path_authority[0].mandatory_reviewers",
                },
                locations,
            )

    def test_protected_authority_requires_an_effective_reviewer(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_contracts(root)

            def mutate(values) -> None:
                authority = next(
                    item
                    for item in values["path_authority"]
                    if item["authority_id"] == "provider-adapters-and-hooks"
                )
                authority["mandatory_reviewers"] = []

            mutate_yaml(root, "agent-governance-artifacts.yaml", mutate)
            findings = validate_fixture(root)
            matching = [
                item
                for item in findings
                if item.code == "AGC-AUTHORITY-SEMANTICS"
                and item.location.endswith(".mandatory_reviewers")
            ]
            self.assertEqual(1, len(matching))

    def test_projection_targets_are_derived_from_providers_and_active_compatibility(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_contracts(root)

            def mutate(values) -> None:
                values["projection_targets"].append("unknown-sorted-target")

            mutate_yaml(root, "agent-catalog.yaml", mutate)
            findings = validate_fixture(root)
            self.assertEqual(
                1,
                sum(
                    item.code == "AGC-CATALOG-PROJECTION-TARGET-MISMATCH"
                    for item in findings
                ),
            )

    def test_invalid_provider_and_model_states_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_contracts(root)

            def mutate(values) -> None:
                values["providers"][0]["adoption_status"] = "sentinel-provider-state"
                values["models"][0]["provider_status"] = "sentinel-model-state"

            mutate_yaml(root, "provider-models.yaml", mutate)
            findings = validate_fixture(root)
            self.assertEqual(
                2,
                sum(item.code == "AGC-PROVIDER-INVALID-STATE" for item in findings),
            )

    def test_missing_source_url_and_checked_time_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_contracts(root)

            def mutate(values) -> None:
                values["models"][0].pop("source_url")
                values["models"][1].pop("checked_at")

            mutate_yaml(root, "provider-models.yaml", mutate)
            findings = validate_fixture(root)
            self.assertEqual(
                2,
                sum(item.code == "AGC-SCHEMA-MISSING-FIELD" for item in findings),
            )

    def test_default_ineligible_fallback_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_contracts(root)

            def mutate(values) -> None:
                ineligible = next(
                    item for item in values["models"] if not item["repository_default_eligible"]
                )
                eligible = next(
                    item
                    for item in values["models"]
                    if item["provider"] == ineligible["provider"]
                    and item["repository_default_eligible"]
                )
                eligible["fallback"] = ineligible["model_id"]

            mutate_yaml(root, "provider-models.yaml", mutate)
            self.assertIn("AGC-MODEL-INELIGIBLE-FALLBACK", codes(validate_fixture(root)))

    def test_findings_are_deterministic_and_rendered_without_raw_values(self) -> None:
        sentinel = "sentinel-do-not-render"
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_contracts(root)

            def mutate(values) -> None:
                values["models"][0]["provider_status"] = sentinel
                values["models"][1]["source_url"] = sentinel

            mutate_yaml(root, "provider-models.yaml", mutate)
            first = validate_fixture(root)
            second = validate_fixture(root)
            self.assertEqual(first, second)
            self.assertEqual(
                sorted(first, key=contract.finding_sort_key),
                first,
            )
            rendered = contract.render_findings(first)
            self.assertNotIn(sentinel, rendered)
            self.assertIn("AGC-PROVIDER-INVALID-STATE", rendered)


class CommandLineTests(unittest.TestCase):
    def run_checker_for_root(
        self, root: pathlib.Path, *args: str
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(CHECKER), "--root", str(root), *args],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def run_checker(self, *args: str) -> subprocess.CompletedProcess[str]:
        return self.run_checker_for_root(ROOT, *args)

    def test_scalar_provider_collections_fail_without_traceback_or_absolute_path(self) -> None:
        for field in ("providers", "compatibility_surfaces", "work_profiles"):
            with self.subTest(field=field), tempfile.TemporaryDirectory() as directory:
                root = pathlib.Path(directory)
                copy_contracts(root)
                mutate_yaml(
                    root,
                    "provider-models.yaml",
                    lambda values, field=field: values.update({field: 1}),
                )
                result = self.run_checker_for_root(root, "--mode", "contract")
                self.assertEqual(1, result.returncode)
                self.assertIn("AGC-SCHEMA-TYPE", result.stderr)
                self.assertNotIn("Traceback", result.stderr)
                self.assertNotIn(str(root), result.stderr)

    def test_repository_mode_never_line_injects_an_unsafe_catalog_path(self) -> None:
        sentinel = "sentinel-injected-line"
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_contracts(root)

            def mutate(values) -> None:
                values["agents"][0]["catalog_path"] = f"safe-prefix\n{sentinel}"

            mutate_yaml(root, "agent-catalog.yaml", mutate)
            bundle = contract.load_contract_bundle(root)
            findings = contract.validate_repository(root, bundle, "catalog")
            rendered = contract.render_findings(findings)
            self.assertIn("AGC-REPOSITORY-UNSAFE-PATH", rendered)
            self.assertNotIn(sentinel, rendered)
            self.assertNotIn(str(root), rendered)

    def test_contract_mode_prints_required_pass_marker(self) -> None:
        result = self.run_checker("--mode", "contract")
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual(
            "agent_governance_contract: PASS contracts=3 agents=14 functions=22 providers=3 failures=0\n",
            result.stdout,
        )
        self.assertEqual("", result.stderr)

    def test_repository_mode_reports_current_parity_without_aggregate_activation(self) -> None:
        result = self.run_checker("--mode", "repository", "--section", "catalog")
        self.assertEqual(1, result.returncode)
        self.assertIn("AGC-REPOSITORY-MISSING-CATALOG-PATH", result.stderr)

    def test_incompatible_section_flag_fails_closed(self) -> None:
        result = self.run_checker("--mode", "contract", "--section", "catalog")
        self.assertEqual(2, result.returncode)
        self.assertIn("--section requires --mode repository", result.stderr)

    def test_repository_mode_requires_an_explicit_section(self) -> None:
        result = self.run_checker("--mode", "repository")
        self.assertEqual(2, result.returncode)
        self.assertIn("--mode repository requires --section", result.stderr)


class Task2GovernanceSurfaceTests(unittest.TestCase):
    GOVERNANCE = "docs/00.agent-governance"
    ROOT_SHIMS = {
        "AGENTS.md": (
            f"{GOVERNANCE}/rules/bootstrap.md",
            f"{GOVERNANCE}/providers/agents-md.md",
            f"{GOVERNANCE}/memory/README.md",
            f"{GOVERNANCE}/memory/progress.md",
        ),
        "CLAUDE.md": (
            f"{GOVERNANCE}/rules/bootstrap.md",
            f"{GOVERNANCE}/providers/claude.md",
            f"{GOVERNANCE}/memory/README.md",
            f"{GOVERNANCE}/memory/progress.md",
        ),
        "GEMINI.md": (
            f"{GOVERNANCE}/rules/bootstrap.md",
            f"{GOVERNANCE}/providers/gemini.md",
            f"{GOVERNANCE}/memory/README.md",
            f"{GOVERNANCE}/memory/progress.md",
        ),
    }

    def test_root_shims_have_no_frontmatter_and_only_executable_bootstrap_envelope(self) -> None:
        for relative_path, targets in self.ROOT_SHIMS.items():
            with self.subTest(path=relative_path):
                text = (ROOT / relative_path).read_text(encoding="utf-8")
                self.assertFalse(text.startswith("---\n"))
                self.assertLessEqual(len(text.splitlines()), 12)
                for target in targets:
                    self.assertEqual(1, text.count(target), target)
                if relative_path in {"CLAUDE.md", "GEMINI.md"}:
                    imports = [
                        line.strip().removeprefix("@./").removeprefix("@")
                        for line in text.splitlines()
                        if line.strip().startswith("@")
                    ]
                    self.assertEqual(list(targets), imports)

    def test_stage00_metadata_uses_exact_registered_envelopes(self) -> None:
        provider_paths = [
            ROOT / "docs/00.agent-governance/providers/agents-md.md",
            ROOT / "docs/00.agent-governance/providers/claude.md",
            ROOT / "docs/00.agent-governance/providers/codex.md",
            ROOT / "docs/00.agent-governance/providers/gemini.md",
        ]
        expected_runtimes = ["shared", "claude", "codex", "gemini"]
        for path, runtime in zip(provider_paths, expected_runtimes, strict=True):
            with self.subTest(path=path.name):
                self.assertEqual(
                    {"layer": "agentic", "runtime": runtime},
                    yaml.safe_load(path.read_text(encoding="utf-8").split("---", 2)[1]),
                )

        scope_dir = ROOT / "docs/00.agent-governance/scopes"
        scope_names = (
            "agentic", "architecture", "backend", "common", "entry", "frontend",
            "infra", "meta", "mobile", "ops", "product", "qa", "security",
        )
        for name in scope_names:
            with self.subTest(scope=name):
                source = (scope_dir / f"{name}.md").read_text(encoding="utf-8")
                self.assertEqual({"layer": name}, yaml.safe_load(source.split("---", 2)[1]))

    def test_provider_entry_indexes_use_navigation_profiles_without_copied_policy(self) -> None:
        allowed = {"Scope", "Structure", "How to Work in This Area", "Related Documents"}
        for relative_path in (".agents/README.md", ".claude/CLAUDE.md", ".codex/README.md"):
            with self.subTest(path=relative_path):
                text = (ROOT / relative_path).read_text(encoding="utf-8")
                headings = {
                    match.group(1).strip()
                    for match in re.finditer(r"^##\s+(.+?)\s*$", text, re.MULTILINE)
                }
                self.assertLessEqual(headings, allowed)
                self.assertNotIn("Canonical Shared Rules", text)
                self.assertNotIn("model-default", text.lower())

    def test_hookify_references_resolve_to_tracked_native_files(self) -> None:
        governed = (
            ROOT / "docs/00.agent-governance/providers/claude.md",
            ROOT / "docs/00.agent-governance/rules/provider-capability-matrix.md",
            ROOT / ".claude/CLAUDE.md",
        )
        for path in governed:
            with self.subTest(path=path.as_posix()):
                text = path.read_text(encoding="utf-8")
                self.assertNotIn("hookify.*.local.md", text)
                if "hookify" not in text.lower():
                    continue
                self.assertIn(
                    "docs/00.agent-governance/rules/hooks/hookify.*.md",
                    text,
                )
        matches = sorted(
            ROOT.glob("docs/00.agent-governance/rules/hooks/hookify.*.md")
        )
        self.assertTrue(matches)
        tracked = subprocess.run(
            ["git", "ls-files", "--error-unmatch", *[str(path.relative_to(ROOT)) for path in matches]],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, tracked.returncode, tracked.stderr)

    def test_repository_harness_rejects_wrong_metadata_keys_order_and_values(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_task2_harness_surfaces(root)
            provider = root / f"{self.GOVERNANCE}/providers/claude.md"
            text = provider.read_text(encoding="utf-8")
            provider.write_text(
                text.replace(
                    "layer: agentic\nruntime: claude",
                    "runtime: wrong-provider\nlayer: agentic\nlegacy: true",
                    1,
                ),
                encoding="utf-8",
            )
            bundle = contract.load_contract_bundle(root)
            observed = codes(contract.validate_repository(root, bundle, "harness"))
            self.assertIn("AGC-REPOSITORY-METADATA-KEYS", observed)
            self.assertIn("AGC-REPOSITORY-METADATA-KEY-ORDER", observed)
            self.assertIn("AGC-REPOSITORY-METADATA-VALUE", observed)

    def test_repository_harness_rejects_missing_required_sections(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_task2_harness_surfaces(root)
            provider = root / f"{self.GOVERNANCE}/providers/claude.md"
            provider.write_text(
                provider.read_text(encoding="utf-8").replace(
                    "## 2. Provider-Specific Rules",
                    "### Provider-Specific Rules",
                    1,
                ),
                encoding="utf-8",
            )
            bundle = contract.load_contract_bundle(root)
            self.assertIn(
                "AGC-REPOSITORY-MISSING-SECTION",
                codes(contract.validate_repository(root, bundle, "harness")),
            )

    def test_repository_harness_does_not_accept_fenced_required_heading(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_task2_harness_surfaces(root)
            provider = root / ".claude/CLAUDE.md"
            provider.write_text(
                provider.read_text(encoding="utf-8").replace(
                    "## Scope",
                    "### Scope\n\n```markdown\n## Scope\n```",
                    1,
                ),
                encoding="utf-8",
            )
            bundle = contract.load_contract_bundle(root)
            self.assertIn(
                "AGC-REPOSITORY-MISSING-SECTION",
                codes(contract.validate_repository(root, bundle, "harness")),
            )

    def test_repository_harness_does_not_accept_raw_html_required_heading(self) -> None:
        for raw_html in (
            "<pre>\n## Scope\n</pre>",
            "<code>\n## Scope\n</code>",
        ):
            with self.subTest(raw_html=raw_html), tempfile.TemporaryDirectory() as directory:
                root = pathlib.Path(directory)
                copy_task2_harness_surfaces(root)
                provider = root / ".claude/CLAUDE.md"
                provider.write_text(
                    provider.read_text(encoding="utf-8").replace(
                        "## Scope",
                        f"### Scope\n\n{raw_html}",
                        1,
                    ),
                    encoding="utf-8",
                )
                bundle = contract.load_contract_bundle(root)
                self.assertIn(
                    "AGC-REPOSITORY-MISSING-SECTION",
                    codes(contract.validate_repository(root, bundle, "harness")),
                )

    def test_repository_harness_does_not_accept_cross_token_html_hidden_heading(self) -> None:
        for tag in ("code", "pre", "script", "style"):
            with self.subTest(tag=tag), tempfile.TemporaryDirectory() as directory:
                root = pathlib.Path(directory)
                copy_task2_harness_surfaces(root)
                provider = root / ".claude/CLAUDE.md"
                provider.write_text(
                    provider.read_text(encoding="utf-8").replace(
                        "## Scope",
                        f"### Scope\n\n<{tag}>\n\n## Scope\n\n</{tag}>",
                        1,
                    ),
                    encoding="utf-8",
                )
                bundle = contract.load_contract_bundle(root)
                self.assertIn(
                    "AGC-REPOSITORY-MISSING-SECTION",
                    codes(contract.validate_repository(root, bundle, "harness")),
                )

    def test_section_names_use_only_strict_h2_tokens(self) -> None:
        source = """\
## 2. Visible Section

<pre>
## Pre Example
</pre>

<code>
## Code Example
</code>

```markdown
## Fence Example
```
"""
        self.assertEqual(("Visible Section",), contract._section_names(source))

    def test_section_names_require_top_level_h2_and_preserve_semantic_code_text(self) -> None:
        self.assertEqual(
            ("Scope",),
            contract._section_names(
                "## <code>Scope</code>\n\n> ## Quote Example\n\n- ## List Example\n"
            ),
        )

    def test_section_names_preserve_independent_html_state_across_tokens(self) -> None:
        for tag in ("code", "pre", "script", "style"):
            with self.subTest(tag=tag):
                self.assertEqual(
                    (), contract._section_names(f"<{tag}>\n\n## Scope\n\n</{tag}>")
                )
        self.assertEqual(
            ("Scope",),
            contract._section_names(
                "<code>\n\nexample\n\n</code>\n\n## Scope"
            ),
        )
        self.assertEqual(
            ("Scope",),
            contract._section_names(
                "<div><code>\n\nexample\n\n</div>\n\n## Scope\n\n</code>"
            ),
        )
        self.assertEqual(
            (),
            contract._section_names(
                "<code>\n\nexample\n\n</span>\n\n## Scope\n\n</code>"
            ),
        )

    def test_repository_harness_does_not_accept_nested_required_heading(self) -> None:
        for nested_heading in ("> ## Scope", "- ## Scope"):
            with self.subTest(
                nested_heading=nested_heading
            ), tempfile.TemporaryDirectory() as directory:
                root = pathlib.Path(directory)
                copy_task2_harness_surfaces(root)
                provider = root / ".claude/CLAUDE.md"
                provider.write_text(
                    provider.read_text(encoding="utf-8").replace(
                        "## Scope", f"### Scope\n\n{nested_heading}", 1
                    ),
                    encoding="utf-8",
                )
                bundle = contract.load_contract_bundle(root)
                self.assertIn(
                    "AGC-REPOSITORY-MISSING-SECTION",
                    codes(contract.validate_repository(root, bundle, "harness")),
                )

    def test_repository_harness_does_not_close_fence_with_info_text(self) -> None:
        self.assertNotIn(
            "Scope",
            contract._section_names(
                "```markdown\n```not-a-close\n## Scope\n```\n"
            ),
        )
        for indentation in ("\t", "\N{NO-BREAK SPACE}"):
            with self.subTest(indentation=repr(indentation)):
                self.assertNotIn(
                    "Scope",
                    contract._section_names(
                        f"```\n{indentation}```\n## Scope\n```\n"
                    ),
                )
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_task2_harness_surfaces(root)
            provider = root / ".claude/CLAUDE.md"
            provider.write_text(
                provider.read_text(encoding="utf-8").replace(
                    "## Scope",
                    "### Scope\n\n```markdown\n```not-a-close\n## Scope\n```",
                    1,
                ),
                encoding="utf-8",
            )
            bundle = contract.load_contract_bundle(root)
            self.assertIn(
                "AGC-REPOSITORY-MISSING-SECTION",
                codes(contract.validate_repository(root, bundle, "harness")),
            )

    def test_repository_harness_requires_exactly_one_profile_for_new_memory_docs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_task2_harness_surfaces(root)
            memory = root / f"{self.GOVERNANCE}/memory/unregistered-note.md"
            memory.write_text(
                "---\nlayer: agentic\n---\n\n# Unregistered note\n\n"
                "## Problem\n\nProblem.\n\n## Context\n\nContext.\n\n"
                "## Resolution\n\nResolution.\n\n## Evidence\n\nEvidence.\n\n"
                "## Related Documents\n\n- `README.md`\n",
                encoding="utf-8",
            )
            bundle = contract.load_contract_bundle(root)
            self.assertIn(
                "AGC-REPOSITORY-PROFILE-COVERAGE",
                codes(contract.validate_repository(root, bundle, "harness")),
            )

    def test_repository_harness_inventory_has_111_uniquely_routed_artifacts(self) -> None:
        bundle = contract.load_contract_bundle(ROOT)
        inventory = contract._governed_inventory_paths(ROOT, bundle.artifacts)
        self.assertEqual(111, len(inventory))
        findings = contract.validate_repository(ROOT, bundle, "harness")
        self.assertFalse(
            codes(findings)
            & {
                "AGC-REPOSITORY-PROFILE-COVERAGE",
                "AGC-REPOSITORY-PROFILE-SECTION",
            }
        )

    def test_repository_harness_routes_future_catalog_files_without_harness_validation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_task2_harness_surfaces(root)
            catalog = root / f"{self.GOVERNANCE}/agents/agents/future-reviewer.md"
            catalog.write_text("future catalog placeholder\n", encoding="utf-8")
            bundle = contract.load_contract_bundle(root)
            findings = contract.validate_repository(root, bundle, "harness")
            self.assertFalse(
                codes(findings)
                & {
                    "AGC-REPOSITORY-PROFILE-COVERAGE",
                    "AGC-REPOSITORY-PROFILE-SECTION",
                    "AGC-REPOSITORY-METADATA-KEYS",
                    "AGC-REPOSITORY-MISSING-SECTION",
                }
            )

    def test_repository_harness_rejects_governed_symlinks(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_task2_harness_surfaces(root)
            external = root.parent / f"{root.name}-external.md"
            external.write_text("## Scope\n", encoding="utf-8")
            provider = root / ".claude/CLAUDE.md"
            provider.unlink()
            provider.symlink_to(external)
            try:
                bundle = contract.load_contract_bundle(root)
                findings = contract.validate_repository(root, bundle, "harness")
            finally:
                external.unlink(missing_ok=True)
            self.assertIn("AGC-REPOSITORY-UNSAFE-FILE", codes(findings))
            self.assertNotIn(str(root), contract.render_findings(findings))

    def test_repository_harness_rejects_missing_and_nonregular_readmes(self) -> None:
        for replacement in ("missing", "directory", "fifo"):
            with self.subTest(replacement=replacement), tempfile.TemporaryDirectory() as directory:
                root = pathlib.Path(directory)
                copy_task2_harness_surfaces(root)
                readme = root / "scripts/README.md"
                readme.unlink()
                if replacement == "directory":
                    readme.mkdir()
                elif replacement == "fifo":
                    os.mkfifo(readme)
                bundle = contract.load_contract_bundle(root)
                observed = codes(contract.validate_repository(root, bundle, "harness"))
                if replacement == "missing":
                    self.assertIn("AGC-REPOSITORY-MISSING-README", observed)
                else:
                    self.assertIn("AGC-REPOSITORY-UNSAFE-FILE", observed)

    def test_repository_harness_normalizes_enumeration_errors(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_task2_harness_surfaces(root)
            bundle = contract.load_contract_bundle(root)
            original = pathlib.Path.glob

            def guarded_glob(path, pattern, *args, **kwargs):
                if path == root and pattern == "docs/00.agent-governance/**/*.md":
                    raise OSError("sentinel-private-enumeration-error")
                return original(path, pattern, *args, **kwargs)

            with mock.patch.object(pathlib.Path, "glob", guarded_glob):
                findings = contract.validate_repository(root, bundle, "harness")
            rendered = contract.render_findings(findings)
            self.assertIn("AGC-REPOSITORY-PATH-ENUMERATION", codes(findings))
            self.assertNotIn("sentinel-private-enumeration-error", rendered)
            self.assertNotIn(str(root), rendered)

    def test_repository_harness_converts_read_errors_to_value_free_findings(self) -> None:
        for relative in ("AGENTS.md", ".claude/CLAUDE.md", "scripts/README.md"):
            with self.subTest(path=relative), tempfile.TemporaryDirectory() as directory:
                root = pathlib.Path(directory)
                copy_task2_harness_surfaces(root)
                bundle = contract.load_contract_bundle(root)
                target = root / relative
                target_stat = target.stat()
                original_read = os.read

                def guarded_read(descriptor: int, size: int) -> bytes:
                    descriptor_stat = os.fstat(descriptor)
                    if (
                        descriptor_stat.st_dev == target_stat.st_dev
                        and descriptor_stat.st_ino == target_stat.st_ino
                    ):
                        raise OSError("sentinel-private-read-error")
                    return original_read(descriptor, size)

                with mock.patch.object(contract.os, "read", new=guarded_read):
                    findings = contract.validate_repository(root, bundle, "harness")
                rendered = contract.render_findings(findings)
                self.assertIn("AGC-REPOSITORY-FILE-READ", codes(findings))
                self.assertNotIn("sentinel-private-read-error", rendered)
                self.assertNotIn(str(root), rendered)

    def test_repository_harness_converts_invalid_utf8_to_value_free_findings(self) -> None:
        for relative in ("AGENTS.md", ".claude/CLAUDE.md", "scripts/README.md"):
            with self.subTest(path=relative), tempfile.TemporaryDirectory() as directory:
                root = pathlib.Path(directory)
                copy_task2_harness_surfaces(root)
                (root / relative).write_bytes(b"\xff\xfe")
                bundle = contract.load_contract_bundle(root)
                findings = contract.validate_repository(root, bundle, "harness")
                rendered = contract.render_findings(findings)
                self.assertIn("AGC-REPOSITORY-FILE-ENCODING", codes(findings))
                self.assertNotIn(str(root), rendered)

    def test_repository_harness_rejects_invalid_root_shim_envelope(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_task2_harness_surfaces(root)
            shim = root / "CLAUDE.md"
            shim.write_text(
                shim.read_text(encoding="utf-8")
                + "\n## Provider Policy\n\nUse an unregistered provider default.\n",
                encoding="utf-8",
            )
            bundle = contract.load_contract_bundle(root)
            self.assertIn(
                "AGC-REPOSITORY-ROOT-SHIM-ENVELOPE",
                codes(contract.validate_repository(root, bundle, "harness")),
            )

    def test_repository_harness_rejects_readme_sections_and_forbidden_policy(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_task2_harness_surfaces(root)
            readme = root / ".codex/README.md"
            readme.write_text(
                readme.read_text(encoding="utf-8")
                + "\n## Model Defaults\n\nProvider model defaults are owned here.\n",
                encoding="utf-8",
            )
            bundle = contract.load_contract_bundle(root)
            observed = codes(contract.validate_repository(root, bundle, "harness"))
            self.assertIn("AGC-REPOSITORY-README-SECTION", observed)
            self.assertIn("AGC-REPOSITORY-README-POLICY", observed)

    def test_repository_harness_rejects_policy_prose_inside_allowed_readme_section(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_task2_harness_surfaces(root)
            readme = root / ".codex/README.md"
            readme.write_text(
                readme.read_text(encoding="utf-8").replace(
                    "Change canonical Stage 00 sources first",
                    "Provider model defaults are defined here.\n\n"
                    "Change canonical Stage 00 sources first",
                    1,
                ),
                encoding="utf-8",
            )
            bundle = contract.load_contract_bundle(root)
            observed = codes(contract.validate_repository(root, bundle, "harness"))
            self.assertIn("AGC-REPOSITORY-README-POLICY", observed)
            self.assertNotIn("AGC-REPOSITORY-README-SECTION", observed)

    def test_repository_harness_rejects_html_wrapped_and_entity_policy_prose(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            copy_task2_harness_surfaces(root)
            readme = root / ".codex/README.md"
            readme.write_text(
                readme.read_text(encoding="utf-8").replace(
                    "Change canonical Stage 00 sources first",
                    "Provider <span>model</span>&#32;defaults are defined here.\n\n"
                    "Change canonical Stage 00 sources first",
                    1,
                ),
                encoding="utf-8",
            )
            bundle = contract.load_contract_bundle(root)
            observed = codes(contract.validate_repository(root, bundle, "harness"))
            self.assertIn("AGC-REPOSITORY-README-POLICY", observed)
            self.assertNotIn("AGC-REPOSITORY-README-SECTION", observed)

    def test_repository_harness_ignores_policy_examples_in_raw_html_code(self) -> None:
        for raw_html in (
            "<pre>Provider model defaults are defined here.</pre>",
            "<code>Provider model defaults are defined here.</code>",
        ):
            with self.subTest(raw_html=raw_html), tempfile.TemporaryDirectory() as directory:
                root = pathlib.Path(directory)
                copy_task2_harness_surfaces(root)
                readme = root / ".codex/README.md"
                readme.write_text(
                    readme.read_text(encoding="utf-8").replace(
                        "Change canonical Stage 00 sources first",
                        f"{raw_html}\n\nChange canonical Stage 00 sources first",
                        1,
                    ),
                    encoding="utf-8",
                )
                bundle = contract.load_contract_bundle(root)
                observed = codes(contract.validate_repository(root, bundle, "harness"))
                self.assertNotIn("AGC-REPOSITORY-README-POLICY", observed)

    def test_repository_harness_preserves_html_hidden_state_across_markdown_tokens(self) -> None:
        cases = tuple(
            (
                f"<{tag}>\n\nProvider model defaults are defined here.\n\n</{tag}>",
                False,
            )
            for tag in ("code", "pre", "script", "style")
        ) + (
            (
                "<code>\n\nexample\n\n</code>\n\n"
                "Provider model defaults are defined here.",
                True,
            ),
            (
                "<div><code>\n\nexample\n\n</div>\n\n"
                "Provider model defaults are defined here.</code>",
                True,
            ),
            (
                "<code>\n\nexample\n\n</span>\n\n"
                "Provider model defaults are defined here.</code>",
                False,
            ),
        )
        for source, expected_policy in cases:
            with self.subTest(
                source=source, expected_policy=expected_policy
            ), tempfile.TemporaryDirectory() as directory:
                root = pathlib.Path(directory)
                copy_task2_harness_surfaces(root)
                readme = root / ".codex/README.md"
                readme.write_text(
                    readme.read_text(encoding="utf-8").replace(
                        "Change canonical Stage 00 sources first",
                        f"{source}\n\nChange canonical Stage 00 sources first",
                        1,
                    ),
                    encoding="utf-8",
                )
                bundle = contract.load_contract_bundle(root)
                observed = codes(contract.validate_repository(root, bundle, "harness"))
                self.assertEqual(
                    expected_policy,
                    "AGC-REPOSITORY-README-POLICY" in observed,
                )

    def test_repository_harness_keeps_visible_prose_after_hidden_html_ancestor_closes(self) -> None:
        sources = (
            "<pre><code>example</pre>"
            "Provider model defaults are defined here.</code>",
            "<div><code>example</div>"
            "Provider model defaults are defined here.</code>",
            "<span><code>example</span>"
            "Provider model defaults are defined here.</code>",
            "<blockquote><pre>example</blockquote>"
            "Provider model defaults are defined here.</pre>",
        )
        for source in sources:
            with self.subTest(source=source), tempfile.TemporaryDirectory() as directory:
                root = pathlib.Path(directory)
                copy_task2_harness_surfaces(root)
                readme = root / ".codex/README.md"
                readme.write_text(
                    readme.read_text(encoding="utf-8").replace(
                        "Change canonical Stage 00 sources first",
                        f"{source}\n\nChange canonical Stage 00 sources first",
                        1,
                    ),
                    encoding="utf-8",
                )
                bundle = contract.load_contract_bundle(root)
                self.assertIn(
                    "AGC-REPOSITORY-README-POLICY",
                    codes(contract.validate_repository(root, bundle, "harness")),
                )

    def test_repository_harness_rejects_visible_multiline_tag_like_policy_prose(self) -> None:
        for source in (
            "Provider <model\n>defaults are defined here.",
            "Provider <span title=model\n>defaults are defined here.",
        ):
            with self.subTest(source=source), tempfile.TemporaryDirectory() as directory:
                root = pathlib.Path(directory)
                copy_task2_harness_surfaces(root)
                readme = root / ".codex/README.md"
                readme.write_text(
                    readme.read_text(encoding="utf-8").replace(
                        "Change canonical Stage 00 sources first",
                        f"{source}\n\nChange canonical Stage 00 sources first",
                        1,
                    ),
                    encoding="utf-8",
                )
                bundle = contract.load_contract_bundle(root)
                observed = codes(contract.validate_repository(root, bundle, "harness"))
                self.assertIn("AGC-REPOSITORY-README-POLICY", observed)

    def test_repository_harness_rejects_policy_hidden_by_unbalanced_code_runs(self) -> None:
        cases = (
            "Provider model ``defaults` are defined here.",
            "Provider model ``defaults are defined here. Later `routing`.",
            r"Provider \`model defaults\` are defined here.",
        )
        for source in cases:
            with self.subTest(source=source), tempfile.TemporaryDirectory() as directory:
                root = pathlib.Path(directory)
                copy_task2_harness_surfaces(root)
                readme = root / ".codex/README.md"
                readme.write_text(
                    readme.read_text(encoding="utf-8").replace(
                        "Change canonical Stage 00 sources first",
                        f"{source}\n\nChange canonical Stage 00 sources first",
                        1,
                    ),
                    encoding="utf-8",
                )
                bundle = contract.load_contract_bundle(root)
                observed = codes(contract.validate_repository(root, bundle, "harness"))
                self.assertIn("AGC-REPOSITORY-README-POLICY", observed)

    def test_repository_harness_keeps_code_runs_inside_inline_block_boundaries(self) -> None:
        cases = (
            "Intro `unclosed\n\nProvider model defaults `",
            "Intro `unclosed\n## Existing heading\nProvider model defaults `",
            "- Intro `unclosed\n- Provider model defaults `",
            "1. Intro `unclosed\n2. Provider model defaults `",
            "- Intro `unclosed\n    - Provider model defaults `",
            "1. Intro `unclosed\n    1. Provider model defaults `",
            "Intro `unclosed\n> Provider model defaults `",
            "Intro `unclosed\n\n***\nProvider model defaults `",
            "Intro `unclosed\nHeading\n---\nProvider model defaults `",
            "Intro `unclosed\n\n    literal code\nProvider model defaults `",
            "Intro `unclosed\n```text\nliteral code\n```\nProvider model defaults `",
            "> ~~~text\n> `unclosed\n> ~~~\n> Provider model defaults `",
            "- ~~~text\n  `unclosed\n  ~~~\n- Provider model defaults `",
            " \tIntro `unclosed\nProvider model defaults `",
            "Intro `unclosed\n\n[label]: https://example.invalid\nProvider model defaults `",
            "[label]: https://example.invalid\n  \"title `unclosed\"\nProvider model defaults `",
            "[label]:\n  https://example.invalid\n  \"title `unclosed\"\nProvider model defaults `",
            "Intro `unclosed\n<div>visible block</div>\nProvider model defaults `",
            "Visible <span\n\nProvider model defaults>",
            "```text\n<span\n```\nProvider model defaults>",
            "Intro `unclosed\n<span\n>Provider model defaults `",
            "Provider model <span title='`'>defaults</span> later `routing`",
            "Provider model <!-- ` -->defaults later `routing`",
            "Intro `unclosed\n<script>const marker=1;</script>\nProvider model defaults `",
            "Intro `unclosed\n<style>.marker { color: red; }</style>\nProvider model defaults `",
            "Intro `unclosed\n<textarea>visible value</textarea>\nProvider model defaults `",
        )
        for source in cases:
            with self.subTest(source=source), tempfile.TemporaryDirectory() as directory:
                root = pathlib.Path(directory)
                copy_task2_harness_surfaces(root)
                readme = root / ".codex/README.md"
                readme.write_text(
                    readme.read_text(encoding="utf-8").replace(
                        "Change canonical Stage 00 sources first",
                        f"{source}\n\nChange canonical Stage 00 sources first",
                        1,
                    ),
                    encoding="utf-8",
                )
                bundle = contract.load_contract_bundle(root)
                observed = codes(contract.validate_repository(root, bundle, "harness"))
                self.assertIn("AGC-REPOSITORY-README-POLICY", observed)

    def test_registered_readme_routing_prose_does_not_trigger_policy_topics(self) -> None:
        bundle = contract.load_contract_bundle(ROOT)
        findings = contract.validate_repository(ROOT, bundle, "harness")
        policy_findings = [
            finding
            for finding in findings
            if finding.code == "AGC-REPOSITORY-README-POLICY"
        ]
        self.assertEqual([], policy_findings)
        scripts_text = (ROOT / "scripts/README.md").read_text(encoding="utf-8")
        self.assertIn("path-authority", scripts_text)

    def test_readme_policy_prose_excludes_non_prose_markdown_surfaces(self) -> None:
        source = """\
## Model Defaults

`model defaults`

[routing](https://example.invalid/model-defaults)

docs/model-defaults/owner.md

```text
model defaults
```
"""
        self.assertNotIn(" model defaults ", contract._readme_policy_prose(source))
        self.assertIn(
            " model defaults ",
            contract._readme_policy_prose("Provider model defaults are defined here."),
        )
        self.assertIn(
            " model defaults ",
            contract._readme_policy_prose("Provider <span>model</span>&#32;defaults."),
        )
        self.assertIn(
            " model defaults ",
            contract._readme_policy_prose("Provider <div>model defaults</div>."),
        )
        for raw_html in (
            "Provider <code>model defaults</code> here.",
            "<pre>Provider model defaults here.</pre>",
            "<pre><code>Provider model defaults here.</code></pre>",
        ):
            with self.subTest(raw_html=raw_html):
                self.assertNotIn(
                    " model defaults ", contract._readme_policy_prose(raw_html)
                )
        self.assertIn(
            " model defaults ",
            contract._readme_policy_prose(
                "<pre><code>example</pre>Provider model defaults are defined here.</code>"
            ),
        )
        for raw_html in (
            "<div><code>example</div>Provider model defaults are defined here.</code>",
            "<span><code>example</span>Provider model defaults are defined here.</code>",
            "<blockquote><pre>example</blockquote>"
            "Provider model defaults are defined here.</pre>",
        ):
            with self.subTest(raw_html=raw_html):
                self.assertIn(
                    " model defaults ", contract._readme_policy_prose(raw_html)
                )
        self.assertNotIn(
            " model defaults ",
            contract._readme_policy_prose(
                "<pre>Provider </code>model defaults are an example.</pre>"
            ),
        )

    def test_readme_policy_prose_preserves_html_state_across_markdown_tokens(self) -> None:
        for tag in ("code", "pre", "script", "style"):
            with self.subTest(tag=tag):
                self.assertNotIn(
                    " model defaults ",
                    contract._readme_policy_prose(
                        f"<{tag}>\n\n"
                        "Provider model defaults are defined here.\n\n"
                        f"</{tag}>"
                    ),
                )
        self.assertIn(
            " model defaults ",
            contract._readme_policy_prose(
                "<code>\n\nexample\n\n</code>\n\n"
                "Provider model defaults are defined here."
            ),
        )
        self.assertIn(
            " model defaults ",
            contract._readme_policy_prose(
                "<div><code>\n\nexample\n\n</div>\n\n"
                "Provider model defaults are defined here.</code>"
            ),
        )
        self.assertNotIn(
            " model defaults ",
            contract._readme_policy_prose(
                "<code>\n\nexample\n\n</span>\n\n"
                "Provider model defaults are defined here.</code>"
            ),
        )

    def test_readme_policy_prose_requires_equal_code_span_delimiters(self) -> None:
        for source in (
            "Provider model ``defaults` are defined here.",
            "Provider model ``defaults are defined here. Later `routing`.",
        ):
            with self.subTest(source=source):
                self.assertIn(" model defaults ", contract._readme_policy_prose(source))
        self.assertNotIn(
            " model defaults ",
            contract._readme_policy_prose(
                "Provider ``model defaults`` are defined here."
            ),
        )

    def test_readme_policy_prose_respects_inline_block_and_html_precedence(self) -> None:
        for source in (
            "Intro `unclosed\n\nProvider model defaults `",
            "Intro `unclosed\n## Existing heading\nProvider model defaults `",
            "- Intro `unclosed\n- Provider model defaults `",
            "1. Intro `unclosed\n2. Provider model defaults `",
            "- Intro `unclosed\n    - Provider model defaults `",
            "1. Intro `unclosed\n    1. Provider model defaults `",
            "Intro `unclosed\n> Provider model defaults `",
            "Intro `unclosed\n\n***\nProvider model defaults `",
            "Intro `unclosed\nHeading\n---\nProvider model defaults `",
            "Intro `unclosed\n\n    literal code\nProvider model defaults `",
            "Intro `unclosed\n```text\nliteral code\n```\nProvider model defaults `",
            "> ~~~text\n> `unclosed\n> ~~~\n> Provider model defaults `",
            "- ~~~text\n  `unclosed\n  ~~~\n- Provider model defaults `",
            " \tIntro `unclosed\nProvider model defaults `",
            "Intro `unclosed\n\n[label]: https://example.invalid\nProvider model defaults `",
            "[label]: https://example.invalid\n  \"title `unclosed\"\nProvider model defaults `",
            "[label]:\n  https://example.invalid\n  \"title `unclosed\"\nProvider model defaults `",
            "Intro `unclosed\n<div>visible block</div>\nProvider model defaults `",
            "Visible <span\n\nProvider model defaults>",
            "```text\n<span\n```\nProvider model defaults>",
            "Intro `unclosed\n<span\n>Provider model defaults `",
            "Provider model <span title='`'>defaults</span> later `routing`",
            "Provider model <!-- ` -->defaults later `routing`",
            "Intro `unclosed\n<script>const marker=1;</script>\nProvider model defaults `",
            "Intro `unclosed\n<style>.marker { color: red; }</style>\nProvider model defaults `",
            "Intro `unclosed\n<textarea>visible value</textarea>\nProvider model defaults `",
        ):
            with self.subTest(source=source):
                self.assertIn(" model defaults ", contract._readme_policy_prose(source))
        self.assertIn(
            " model defaults ",
            contract._readme_policy_prose(r"Provider \`model defaults\` here."),
        )
        self.assertNotIn(
            " model defaults ",
            contract._readme_policy_prose(
                "Provider ``model defaults\\`` are defined here."
            ),
        )
        for tag in ("script", "style"):
            with self.subTest(hidden_html=tag):
                self.assertNotIn(
                    " model defaults ",
                    contract._readme_policy_prose(
                        f"<{tag}>model defaults</{tag}>"
                    ),
                )

    def test_readme_policy_prose_passes_source_unchanged_to_strict_markdown(self) -> None:
        real_markdown = contract._MarkdownIt
        observed_sources: list[str] = []

        class RecordingMarkdown:
            def __init__(self, *args, **kwargs) -> None:
                self.delegate = real_markdown(*args, **kwargs)

            def parse(self, source: str):
                observed_sources.append(source)
                return self.delegate.parse(source)

        legacy_source = "Provider mo<span\n>del</span> defaults"
        with mock.patch.object(contract, "_MarkdownIt", RecordingMarkdown):
            legacy_prose = contract._readme_policy_prose(legacy_source)

        self.assertEqual([legacy_source], observed_sources)
        self.assertNotIn(" model defaults ", legacy_prose)
        for source in (
            "Provider <model\n>defaults are defined here.",
            "Provider <span title=model\n>defaults are defined here.",
        ):
            with self.subTest(source=source):
                self.assertIn(" model defaults ", contract._readme_policy_prose(source))

    def test_codeowners_keeps_repository_principal_and_covers_governed_surfaces(self) -> None:
        text = (ROOT / ".github/CODEOWNERS").read_text(encoding="utf-8")
        self.assertNotRegex(text, r"@(rules-engineer|qa-engineer|security-auditor)")
        for pattern in (
            ".agents/**", ".claude/**", ".codex/**", ".gemini/**",
            "docs/00.agent-governance/contracts/**",
            "scripts/validation/check-agent-governance-contract.py",
            "scripts/validation/check-document-metadata.py",
            "tests/validation/test_agent_governance_contract.py",
            "tests/validation/test_document_metadata.py",
        ):
            with self.subTest(pattern=pattern):
                self.assertIn(f"{pattern} @buenhyden", text)


if __name__ == "__main__":
    unittest.main()
