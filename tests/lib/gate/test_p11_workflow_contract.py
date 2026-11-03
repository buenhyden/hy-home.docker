from __future__ import annotations

import copy
import unittest

from scripts.lib.gate import ci_gate_contract as gate_contract
from scripts.validation import ci_gate_runner as gate_runner
from tests.lib.gate.test_github_workflow_contract import ROOT

GATE_ID = "leaf.p11-hermes"
ENTRYPOINT = "scripts/validation/check-p11-hermes.py"
WORKLOAD = "infra/07-workflow/n8n/workloads/hermes-blog-ingestion/"


class P11WorkflowContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.document = gate_contract.load_contract_document(ROOT)
        self.public = gate_contract.parse_public_gate_contract(self.document)
        self.registry = gate_contract.parse_gate_registry(
            self.document,
            ".github/workflow-contract.yml",
        )

    def _plan(
        self,
        document: dict[str, object],
        context: gate_runner.ExecutionContext,
    ):
        public = gate_contract.parse_public_gate_contract(document)
        registry = gate_contract.parse_gate_registry(
            document,
            ".github/workflow-contract.yml",
        )
        changed_paths = (ENTRYPOINT,)
        selected = gate_contract.select_public_suites(
            public,
            "changed",
            changed_paths,
        )
        roots = gate_contract.public_root_gate_ids(
            public,
            selected,
            changed_paths=changed_paths,
        )
        return gate_runner.build_public_validation_plan(
            registry,
            roots,
            public,
            selected,
            context,
            profile="changed",
            root=ROOT,
        )

    def test_p11_gate_is_closed_and_preserves_p03(self) -> None:
        nodes = {node["gate_id"]: node for node in self.document["gate_nodes"]}
        gate = nodes[GATE_ID]
        self.assertEqual(ENTRYPOINT, gate["entrypoint"])
        self.assertEqual([], gate["argv"])
        self.assertEqual([], gate["allowed_env_keys"])
        self.assertEqual(".", gate["cwd"])
        self.assertTrue(gate["opaque"])
        self.assertIn("leaf.p03-hermes", nodes)

        repository = nodes["leaf.repository-integrity-regressions"]
        self.assertEqual(
            1,
            repository["argv"].count("tests.validation.test_p11_hermes_gate"),
        )

    def test_p11_validator_has_exact_public_context_ownership(self) -> None:
        validator = next(
            item for item in self.public.validators if item.gate_id == GATE_ID
        )
        self.assertEqual("repository-integrity", validator.suite)
        self.assertEqual(ENTRYPOINT, validator.entrypoint.as_posix())
        self.assertEqual((), validator.argv)
        self.assertEqual(
            ("local", "pull_request", "push", "workflow_dispatch"),
            validator.contexts,
        )

        for context in (
            gate_runner.ExecutionContext.LOCAL,
            gate_runner.ExecutionContext.PULL_REQUEST,
            gate_runner.ExecutionContext.PUSH,
            gate_runner.ExecutionContext.PUSH_INITIAL,
            gate_runner.ExecutionContext.WORKFLOW_DISPATCH,
        ):
            with self.subTest(context=context):
                changed_paths = (ENTRYPOINT,)
                selected = gate_contract.select_public_suites(
                    self.public,
                    "changed",
                    changed_paths,
                )
                plan = self._plan(self.document, context)
                matches = [item for item in plan if item.gate_id == GATE_ID]
                self.assertEqual(1, len(matches))
                self.assertEqual(validator.entrypoint, matches[0].entrypoint)
                self.assertEqual(validator.argv, matches[0].argv)
                gate_runner.validate_public_execution_parity(
                    self.public,
                    selected,
                    plan,
                    context,
                    profile="changed",
                )

    def test_p11_validator_mutations_fail_closed(self) -> None:
        context = gate_runner.ExecutionContext.WORKFLOW_DISPATCH
        changed_paths = (ENTRYPOINT,)
        selected = gate_contract.select_public_suites(
            self.public,
            "changed",
            changed_paths,
        )
        baseline_plan = self._plan(self.document, context)
        cases: list[tuple[str, dict[str, object]]] = []

        missing = copy.deepcopy(self.document)
        missing["public_gate"]["validators"] = [
            row
            for row in missing["public_gate"]["validators"]
            if row["gate_id"] != GATE_ID
        ]
        cases.append(("missing", missing))

        for field, value in (
            ("suite", "operations"),
            ("entrypoint", "scripts/validation/check-p03-hermes.py"),
            ("argv", ["--weaken"]),
            ("contexts", ["local"]),
        ):
            candidate = copy.deepcopy(self.document)
            validator = next(
                row
                for row in candidate["public_gate"]["validators"]
                if row["gate_id"] == GATE_ID
            )
            validator[field] = value
            cases.append((field, candidate))

        for label, candidate in cases:
            with self.subTest(label=label):
                with self.assertRaises(gate_contract.GateContractError):
                    mutated = gate_contract.parse_public_gate_contract(candidate)
                    gate_runner.validate_public_execution_parity(
                        mutated,
                        selected,
                        baseline_plan,
                        context,
                        profile="changed",
                    )

    def test_all_hermes_sources_and_gate_files_route_to_p11(self) -> None:
        for path in (
            ENTRYPOINT,
            "tests/validation/test_p11_hermes_gate.py",
            WORKLOAD + "install.py",
            WORKLOAD + "publisher/gateway_adapter.py",
            WORKLOAD + "tests/test_attester.py",
            WORKLOAD + "tests/e2e-cache-contract.sh",
            WORKLOAD + "tests/e2e_collect_harness.py",
        ):
            with self.subTest(path=path):
                changed = (path,)
                suites = gate_contract.select_public_suites(
                    self.public,
                    "changed",
                    changed,
                )
                roots = gate_contract.public_root_gate_ids(
                    self.public,
                    suites,
                    changed_paths=changed,
                )
                expanded = gate_contract.expand_public_gate_ids(self.registry, roots)
                self.assertIn("repository-integrity", suites)
                self.assertIn(GATE_ID, roots)
                self.assertIn(GATE_ID, expanded)


if __name__ == "__main__":
    unittest.main()
