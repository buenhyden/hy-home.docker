from __future__ import annotations

import dataclasses
import importlib.util
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

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


class ContractSchemaTests(unittest.TestCase):
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
                and item.location == "path_authority[3].mandatory_reviewers"
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


if __name__ == "__main__":
    unittest.main()
