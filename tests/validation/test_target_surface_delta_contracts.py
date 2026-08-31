from __future__ import annotations

import contextlib
import copy
import dataclasses
import io
import pathlib
import subprocess
import tempfile
import unittest
from unittest import mock

import yaml

from scripts.lib.gate import ci_gate_contract
from scripts.validation import ci_gate_runner
from scripts.lib.target_surface import target_surface_delta_contract as contract


ROOT = pathlib.Path(__file__).resolve().parents[2]
CLI = ROOT / "scripts/validation/check-target-surface-delta-contract.py"


class LivePublicGateContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.manifest, self.gates, self.public = contract._load_models(ROOT)

    def test_repository_satisfies_live_contract(self) -> None:
        self.assertEqual((), contract.validate_repository(ROOT))

    def test_cli_wrapper_enforces_the_live_contract_in_both_modes(self) -> None:
        for mode in ("advisory", "blocking"):
            with self.subTest(mode=mode):
                result = subprocess.run(
                    ["python3", str(CLI), "--mode", mode],
                    cwd=ROOT,
                    capture_output=True,
                    text=True,
                    check=False,
                    timeout=10,
                )
                self.assertEqual(0, result.returncode, result.stderr)

    def test_exact_suites_profiles_and_explain_ownership(self) -> None:
        self.assertEqual(contract.PUBLIC_SUITES, self.manifest.public_names)
        self.assertEqual(contract.PUBLIC_SUITES, self.public.suite_names)
        self.assertEqual(contract.PUBLIC_PROFILES, self.public.profile_names)

        plan = ci_gate_runner.build_public_validation_plan(
            self.gates,
            ci_gate_contract.public_root_gate_ids(
                self.public, self.public.suite_names
            ),
            self.manifest,
            self.public.suite_names,
            ci_gate_runner.ExecutionContext.LOCAL,
        )
        lines = ci_gate_runner.render_public_validation_plan(
            plan,
            self.manifest,
            self.public.suite_names,
            ci_gate_runner.ExecutionContext.LOCAL,
        )
        rendered = tuple(line.split("\t", 1)[1] for line in lines)
        expected = tuple(
            item.path.as_posix()
            for item in self.manifest.validators
            if "local" in item.execution_contexts
        )
        self.assertCountEqual(expected, rendered)
        self.assertEqual(len(expected), len(set(rendered)))

    def test_every_executable_route_has_one_public_owner(self) -> None:
        routed: list[str] = []
        for route in self.public.suites:
            plan = ci_gate_runner.build_public_validation_plan(
                self.gates,
                route.root_gate_ids,
                self.manifest,
                (route.name,),
                ci_gate_runner.ExecutionContext.LOCAL,
            )
            self.assertTrue(plan, route.name)
            routed.extend(item.gate_id for item in plan)
        self.assertEqual(len(routed), len(set(routed)))

    def test_changed_path_selection_covers_impacted_responsibilities(self) -> None:
        cases = {
            "docs/00.agent-governance/current.md": (
                "agent-governance",
                "document-contract",
                "document-graph",
                "document-lifecycle",
                "repository-integrity",
            ),
            "docs/03.specs/example/spec.md": (
                "document-contract",
                "document-graph",
                "document-lifecycle",
                "repository-integrity",
            ),
            "infra/01-gateway/README.md": (
                "document-contract",
                "document-graph",
                "document-lifecycle",
                "operations",
                "repository-integrity",
            ),
            "scripts/validation/example.py": contract.PUBLIC_SUITES,
            "NOTICE": ("repository-integrity",),
        }
        for path, expected in cases.items():
            with self.subTest(path=path):
                self.assertEqual(
                    expected,
                    ci_gate_contract.select_public_suites(
                        self.public,
                        "changed",
                        (path,),
                    ),
                )

    def test_unknown_profiles_and_unsafe_paths_fail_closed(self) -> None:
        with self.assertRaises(ci_gate_contract.GateContractError):
            ci_gate_contract.select_public_suites(self.public, "legacy", ())
        with self.assertRaises(ci_gate_contract.GateContractError):
            ci_gate_contract.select_public_suites(
                self.public,
                "changed",
                ("../escape",),
            )

    def test_retired_and_task4_paths_are_absent(self) -> None:
        for relative in (*contract.RETIRED_PATHS, *contract.TASK4_REMOVED_PATHS):
            with self.subTest(path=relative):
                self.assertFalse((ROOT / relative).exists())
        manifest_text = (ROOT / "scripts/manifest.yaml").read_text(encoding="utf-8")
        for relative in contract.RETIRED_PATHS:
            self.assertNotIn(relative, manifest_text)

    def test_exact_task4_contract_artifact_reintroduction_is_blocking(self) -> None:
        forbidden = contract.TASK4_REMOVED_PATHS[1]
        self.assertEqual(
            "docs/00.agent-governance/contracts/agent-governance-artifacts.yaml",
            forbidden,
        )
        with tempfile.TemporaryDirectory(dir="/tmp") as directory:
            root = pathlib.Path(directory)
            path = root / forbidden
            path.parent.mkdir(parents=True)
            path.write_text("regressed: true\n", encoding="utf-8")
            findings = contract._retirement_findings(root)
        self.assertIn(
            ("task4-removal-regressed", forbidden),
            {(item.code, item.path) for item in findings},
        )

    def test_current_infra_runner_links_are_exact_and_mutation_blocks(self) -> None:
        self.assertEqual([], contract._infra_link_findings(ROOT))
        with tempfile.TemporaryDirectory(dir="/tmp") as directory:
            root = pathlib.Path(directory)
            readme = root / "infra/01-gateway/nginx/README.md"
            readme.parent.mkdir(parents=True)
            readme.write_text(
                "[run-ci-gate.py](../../.python3 "
                "scripts/validation/run-ci-gate.py --profile changed)\n",
                encoding="utf-8",
            )
            findings = contract._infra_link_findings(root)
        self.assertEqual(
            ["public-infra-runner-link"],
            [item.code for item in findings],
        )


class LivePublicGateMutationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.manifest, self.gates, self.public = contract._load_models(ROOT)
        self.document = ci_gate_contract.load_contract_document(ROOT)

    def test_missing_suite_route_is_rejected(self) -> None:
        document = copy.deepcopy(self.document)
        del document["public_gate"]["suite_roots"]["operations"]
        with self.assertRaises(ci_gate_contract.GateContractError):
            ci_gate_contract.parse_public_gate_contract(document, self.manifest)

    def test_duplicate_suite_route_is_rejected(self) -> None:
        document = copy.deepcopy(self.document)
        roots = document["public_gate"]["suite_roots"]
        roots["document-contract"] = [roots["agent-governance"][0]]
        with self.assertRaises(ci_gate_contract.GateContractError):
            ci_gate_contract.parse_public_gate_contract(document, self.manifest)

    def test_unknown_changed_suite_is_rejected(self) -> None:
        document = copy.deepcopy(self.document)
        document["public_gate"]["changed_path_rules"][-1]["suites"].append(
            "unknown-suite"
        )
        with self.assertRaises(ci_gate_contract.GateContractError):
            ci_gate_contract.parse_public_gate_contract(document, self.manifest)

    def test_changed_rule_cannot_skip_an_owning_suite(self) -> None:
        rules = list(self.public.changed_rules)
        scripts_rule = rules[-1]
        rules[-1] = dataclasses.replace(
            scripts_rule,
            suites=tuple(
                name for name in scripts_rule.suites if name != "agent-governance"
            ),
        )
        mutated = dataclasses.replace(self.public, changed_rules=tuple(rules))
        findings = contract._changed_impact_findings(self.manifest, mutated)
        self.assertIn("public-changed-impact-missing", {item.code for item in findings})

    def test_untracked_validator_fails_closed(self) -> None:
        first = self.manifest.validators[0].path.as_posix()
        original = contract._tracked

        def tracked(root: pathlib.Path, relative: str) -> bool:
            return relative != first and original(root, relative)

        with mock.patch.object(contract, "_tracked", side_effect=tracked):
            findings = contract._suite_ownership_findings(
                ROOT,
                self.manifest,
                self.gates,
                self.public,
            )
        self.assertIn(
            ("public-validator-untracked", first),
            {(item.code, item.path) for item in findings},
        )

    def test_cross_suite_duplicate_execution_route_fails_closed(self) -> None:
        routes = list(self.public.suites)
        routes[1] = dataclasses.replace(
            routes[1],
            root_gate_ids=(routes[0].root_gate_ids[0], *routes[1].root_gate_ids),
        )
        mutated = dataclasses.replace(self.public, suites=tuple(routes))
        findings = contract._suite_ownership_findings(
            ROOT,
            self.manifest,
            self.gates,
            mutated,
        )
        self.assertIn("public-route-duplicate", {item.code for item in findings})

    def test_empty_execution_route_fails_closed(self) -> None:
        routes = list(self.public.suites)
        routes[0] = dataclasses.replace(routes[0], root_gate_ids=())
        mutated = dataclasses.replace(self.public, suites=tuple(routes))
        findings = contract._suite_ownership_findings(
            ROOT,
            self.manifest,
            self.gates,
            mutated,
        )
        self.assertIn("public-suite-empty", {item.code for item in findings})

    def test_copied_atomic_command_fails_closed(self) -> None:
        original = contract._read_surface
        target = "scripts/hooks/post-tool-validate.sh"

        def surface(root: pathlib.Path, relative: str) -> str:
            source = original(root, relative)
            if relative == target:
                return f"{source}\nscripts/validation/check-document-links.py\n"
            return source

        with mock.patch.object(contract, "_read_surface", side_effect=surface):
            findings = contract._surface_findings(ROOT, self.gates)
        self.assertIn(
            ("public-surface-copied-validator", target),
            {(item.code, item.path) for item in findings},
        )

    def test_missing_and_duplicate_workflow_routes_fail_closed(self) -> None:
        path = ".github/workflows/ci-quality.yml"
        source = contract._read_surface(ROOT, path)
        document = yaml.safe_load(source)
        document["jobs"]["validation-changed"]["steps"][-1]["run"] = (
            contract.FULL_COMMAND
        )
        missing = yaml.safe_dump(document, sort_keys=False)
        with mock.patch.object(contract, "_read_surface", return_value=missing):
            self.assertIn(
                "public-workflow-route",
                {item.code for item in contract._workflow_findings(ROOT)},
            )

        document = yaml.safe_load(source)
        document["jobs"]["validation-full"]["steps"].append(
            {"run": contract.FULL_COMMAND}
        )
        duplicate = yaml.safe_dump(document, sort_keys=False)
        with mock.patch.object(contract, "_read_surface", return_value=duplicate):
            self.assertIn(
                "public-workflow-route",
                {item.code for item in contract._workflow_findings(ROOT)},
            )

    def test_workflow_requires_exact_bootstrap_then_one_public_command(self) -> None:
        path = ".github/workflows/ci-quality.yml"
        original = yaml.safe_load(contract._read_surface(ROOT, path))
        bootstrap = "python3 -m pip install -r scripts/requirements.txt"
        self.assertEqual([], contract._workflow_findings(ROOT))
        for job_id, command in (("validation-changed", contract.CHANGED_COMMAND),
                                ("validation-full", contract.FULL_COMMAND)):
            cases = (
                [command], [bootstrap], [bootstrap, bootstrap, command],
                [command, bootstrap], [bootstrap, command, command],
                ["python3 -m pip install pyyaml", command],
                [bootstrap + " --upgrade", command],
                [bootstrap + "\necho extra", command],
                [bootstrap, command, "python3 scripts/validation/check-document-links.py --mode all"],
                [bootstrap, "echo extra", command],
            )
            for runs in cases:
                with self.subTest(job=job_id, runs=runs):
                    document = copy.deepcopy(original)
                    steps = document["jobs"][job_id]["steps"]
                    document["jobs"][job_id]["steps"] = [
                        step for step in steps if "run" not in step
                    ] + [{"run": run} for run in runs]
                    with mock.patch.object(contract, "_read_surface", return_value=yaml.safe_dump(document, sort_keys=False)):
                        findings = contract._workflow_findings(ROOT)
                    self.assertEqual(
                        [("public-workflow-route", f"{path}#{job_id}")],
                        [(item.code, item.path) for item in findings],
                    )

    def test_advisory_mode_cannot_downgrade_findings(self) -> None:
        finding = contract.DeltaFinding("test", "surface", "failure")
        for mode in ("advisory", "blocking"):
            with self.subTest(mode=mode), mock.patch.object(
                contract,
                "validate_repository",
                return_value=(finding,),
            ):
                stderr = io.StringIO()
                with contextlib.redirect_stderr(stderr):
                    self.assertEqual(1, contract.main(["--mode", mode]))
                self.assertIn("FAIL [test]", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
