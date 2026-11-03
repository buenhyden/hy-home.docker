from __future__ import annotations

import json
import unittest

from scripts.lib.gate import ci_gate_contract as gate_contract
from scripts.validation import ci_gate_runner as gate_runner
from tests.lib.gate.test_github_workflow_contract import ROOT


class P03WorkflowContractTests(unittest.TestCase):
    def test_p03_hermes_validator_mutations_fail_closed(self) -> None:
        baseline = gate_contract.load_contract_document(ROOT)
        public = gate_contract.parse_public_gate_contract(baseline)
        registry = gate_contract.parse_gate_registry(
            baseline, ".github/workflow-contract.yml"
        )
        changed_paths = ("scripts/validation/check-p03-hermes.py",)
        selected = gate_contract.select_public_suites(public, "changed", changed_paths)
        roots = gate_contract.public_root_gate_ids(
            public, selected, changed_paths=changed_paths
        )
        actual_plan = gate_runner.build_public_validation_plan(
            registry,
            roots,
            public,
            selected,
            gate_runner.ExecutionContext.WORKFLOW_DISPATCH,
            profile="changed",
            root=ROOT,
        )
        cases: list[tuple[str, dict[str, object], str]] = []

        missing = json.loads(json.dumps(baseline))
        missing["public_gate"]["validators"] = [
            row
            for row in missing["public_gate"]["validators"]
            if row["gate_id"] != "leaf.p03-hermes"
        ]
        cases.append(("missing", missing, "ci-gate-public-execution-parity"))

        for field, value, expected_code in (
            ("suite", "operations", "ci-gate-public-execution-parity"),
            (
                "entrypoint",
                "scripts/validation/check-release.py",
                "ci-gate-public-validators",
            ),
            ("argv", ["--mode", "weakened"], "ci-gate-public-validators"),
            (
                "contexts",
                ["local", "pull_request", "push"],
                "ci-gate-public-execution-parity",
            ),
        ):
            candidate = json.loads(json.dumps(baseline))
            validator = next(
                row
                for row in candidate["public_gate"]["validators"]
                if row["gate_id"] == "leaf.p03-hermes"
            )
            validator[field] = value
            cases.append((field, candidate, expected_code))

        for label, document, expected_code in cases:
            with self.subTest(label=label):
                with self.assertRaises(gate_contract.GateContractError) as raised:
                    mutated = gate_contract.parse_public_gate_contract(document)
                    gate_runner.validate_public_execution_parity(
                        mutated,
                        selected,
                        actual_plan,
                        gate_runner.ExecutionContext.WORKFLOW_DISPATCH,
                        profile="changed",
                    )
                self.assertEqual(expected_code, raised.exception.code)

    def test_p03_hermes_validator_has_exact_public_context_ownership(self) -> None:
        document = gate_contract.load_contract_document(ROOT)
        public = gate_contract.parse_public_gate_contract(document)
        validator = next(
            item for item in public.validators if item.gate_id == "leaf.p03-hermes"
        )
        self.assertEqual("repository-integrity", validator.suite)
        self.assertEqual(
            "scripts/validation/check-p03-hermes.py",
            validator.entrypoint.as_posix(),
        )
        self.assertEqual((), validator.argv)
        self.assertEqual(
            ("local", "pull_request", "push", "workflow_dispatch"),
            validator.contexts,
        )

        registry = gate_contract.parse_gate_registry(
            document, ".github/workflow-contract.yml"
        )
        changed_paths = ("scripts/validation/check-p03-hermes.py",)
        selected = gate_contract.select_public_suites(public, "changed", changed_paths)
        roots = gate_contract.public_root_gate_ids(
            public, selected, changed_paths=changed_paths
        )
        for context in (
            gate_runner.ExecutionContext.LOCAL,
            gate_runner.ExecutionContext.PULL_REQUEST,
            gate_runner.ExecutionContext.PUSH,
            gate_runner.ExecutionContext.PUSH_INITIAL,
            gate_runner.ExecutionContext.WORKFLOW_DISPATCH,
        ):
            with self.subTest(context=context):
                plan = gate_runner.build_public_validation_plan(
                    registry,
                    roots,
                    public,
                    selected,
                    context,
                    profile="changed",
                    root=ROOT,
                )
                matches = [item for item in plan if item.gate_id == "leaf.p03-hermes"]
                self.assertEqual(1, len(matches))
                self.assertEqual(validator.entrypoint, matches[0].entrypoint)
                self.assertEqual(validator.argv, matches[0].argv)

    def test_p03_hermes_gate_is_closed_and_exactly_routed(self) -> None:
        document = gate_contract.load_contract_document(ROOT)
        nodes = {node["gate_id"]: node for node in document["gate_nodes"]}
        gate = nodes["leaf.p03-hermes"]
        self.assertEqual("scripts/validation/check-p03-hermes.py", gate["entrypoint"])
        self.assertEqual([], gate["argv"])
        self.assertEqual([], gate["allowed_env_keys"])
        self.assertEqual(".", gate["cwd"])

        repository = nodes["leaf.repository-integrity-regressions"]
        self.assertEqual(
            1,
            repository["argv"].count("tests.validation.test_p03_hermes_gate"),
        )
        public = gate_contract.parse_public_gate_contract(document)
        registry = gate_contract.parse_gate_registry(
            document, ".github/workflow-contract.yml"
        )
        for path in (
            "scripts/validation/check-p03-hermes.py",
            "tests/validation/test_p03_hermes_gate.py",
            "infra/07-workflow/n8n/workloads/hermes-blog-ingestion/"
            "hermes-plugin/webhook_transport.py",
            "infra/07-workflow/n8n/workloads/hermes-blog-ingestion/"
            "tests/test_webhook_transport.py",
        ):
            with self.subTest(path=path):
                suites = gate_contract.select_public_suites(public, "changed", (path,))
                self.assertIn("repository-integrity", suites)
                roots = gate_contract.public_root_gate_ids(
                    public, suites, changed_paths=(path,)
                )
                self.assertIn("leaf.p03-hermes", roots)
                expanded = gate_contract.expand_public_gate_ids(registry, roots)
                self.assertIn("leaf.p03-hermes", expanded)

    def test_p03_model_and_runner_contracts_are_required_and_exactly_routed(
        self,
    ) -> None:
        document = gate_contract.load_contract_document(ROOT)
        nodes = {node["gate_id"]: node for node in document["gate_nodes"]}
        repository = nodes["leaf.repository-integrity-regressions"]
        for module in (
            "tests.lib.ops.test_notebook_models",
            "tests.validation.test_p03_notebook_effects",
            "tests.validation.test_p03_notebook_models",
            "tests.validation.test_p03_owned_docker",
            "tests.validation.test_p03_worker_models",
            "tests.validation.test_p03_models_native",
        ):
            self.assertEqual(1, repository["argv"].count(module))
        repository_boundary = repository["argv"].index("--optional-runtime-skips")
        native_module = "tests.validation.test_p03_models_native"
        self.assertIn(native_module, repository["argv"][:repository_boundary])
        self.assertEqual(
            [
                native_module + ".NotebookModelsNativeExecutionTests",
                native_module + ".WorkerModelQueueNativeTests",
            ],
            repository["argv"][repository_boundary + 1 : -1],
        )
        self.assertEqual([], repository["allowed_env_keys"])

        compose = nodes["leaf.compose-baseline-regressions"]
        boundary = compose["argv"].index("--optional-runtime-skips")
        module = "tests.validation.test_p03_runner_isolation"
        scope = module + ".P03RunnerNativeRehearsal"
        self.assertEqual(1, compose["argv"][:boundary].count(module))
        self.assertEqual(
            1,
            compose["argv"][:boundary].count(
                "tests.validation.test_p03_runner_boundaries"
            ),
        )
        self.assertEqual(
            1,
            compose["argv"][:boundary].count(
                "tests.validation.test_p03_runner_consumers"
            ),
        )
        self.assertEqual(1, compose["argv"][boundary + 1 :].count(scope))
        self.assertEqual([], compose["allowed_env_keys"])

        public = gate_contract.parse_public_gate_contract(document)
        registry = gate_contract.parse_gate_registry(
            document, ".github/workflow-contract.yml"
        )
        for path in (
            "scripts/operations/notebook-models.py",
            "tests/fixtures/p03_models/notebook-model-policy.json",
            "tests/validation/_p03_notebook_effects.py",
            "tests/validation/_p03_notebook_protocol.py",
            "tests/validation/_p03_notebook_readiness.py",
            "tests/validation/_p03_owned_docker.py",
            "tests/validation/_p03_worker_ollama_fixture.py",
            "tests/validation/test_p03_notebook_effects.py",
            "tests/validation/test_p03_owned_docker.py",
            "tests/validation/test_p03_worker_models.py",
        ):
            with self.subTest(path=path):
                suites = gate_contract.select_public_suites(public, "changed", (path,))
                self.assertEqual(("repository-integrity",), suites)
                roots = gate_contract.public_root_gate_ids(
                    public, suites, changed_paths=(path,)
                )
                self.assertIn("leaf.repository-integrity-regressions", roots)

        for path in (
            "infra/07-workflow/n8n/n8n-task-runners.json",
            "tests/validation/_p03_runner_outcomes.py",
            "tests/validation/_p03_worker_model_native.py",
            "tests/validation/_p03_runner_native_fixture.py",
            "tests/validation/test_p03_models_native.py",
            "tests/validation/test_p03_runner_boundaries.py",
            "tests/validation/test_p03_runner_consumers.py",
            "tests/validation/test_p03_runner_isolation.py",
        ):
            with self.subTest(path=path):
                suites = gate_contract.select_public_suites(public, "changed", (path,))
                self.assertIn("operations", suites)
                self.assertIn("repository-integrity", suites)
                roots = gate_contract.public_root_gate_ids(
                    public, suites, changed_paths=(path,)
                )
                self.assertIn("leaf.repository-integrity-regressions", roots)
                expanded = gate_contract.expand_public_gate_ids(registry, roots)
                self.assertIn("leaf.compose-baseline-regressions", expanded)

        inventory_path = "scripts/lib/ops/_workspace_model_connections.py"
        suites = gate_contract.select_public_suites(
            public, "changed", (inventory_path,)
        )
        roots = gate_contract.public_root_gate_ids(
            public, suites, changed_paths=(inventory_path,)
        )
        self.assertIn("leaf.repository-integrity-regressions", roots)


if __name__ == "__main__":
    unittest.main()
