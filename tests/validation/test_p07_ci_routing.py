"""P07 public-source and synthetic checks must remain in the selected gate."""

from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from scripts.lib.gate import github_workflow_contract
from scripts.lib.gate.ci_gate_contract import (
    load_contract_document,
    parse_public_gate_contract,
    public_root_gate_ids,
    select_public_suites,
)
from scripts.validation.ci_gate_runner import GateInvocation, selected_prerequisites

ROOT = Path(__file__).resolve().parents[2]
LAUNCHER_MODULE = "tests.lib.ops.test_compose_start"
LAUNCHER_PATHS = (
    "scripts/operations/compose-start.py",
    "scripts/lib/ops/compose_start.py",
    "tests/lib/ops/test_compose_start.py",
    "tests/validation/test_p07_ci_routing.py",
    "docs/05.operations/policies/01-common/0078-compose-profile-vocabulary.md",
)
OBSERVATION_MODULES = (
    "tests.lib.ops.test_compose_observation",
    "tests.validation.test_p07_quality_metrics",
    "tests.validation.test_p07_ci_routing",
)
OBSERVATION_PATHS = (
    "scripts/lib/ops/compose_observation.py",
    "tests/lib/ops/test_compose_observation.py",
    "tests/validation/test_p07_quality_metrics.py",
    "tests/validation/fixtures/p07-observation/rules.test.yml",
    "tests/validation/fixtures/p07-observation/dashboards.test.yml",
    "examples/operations/quality-metrics/acceptance.py",
    "examples/operations/quality-metrics/docker-compose.yml",
)


class P07RoutingTests(unittest.TestCase):
    def test_compose_prerequisite_step_is_enforced(self):
        document = next(
            item
            for item in github_workflow_contract.load_workflows(ROOT)
            if item.path == ".github/workflows/ci-quality.yml"
        )
        contract = github_workflow_contract.load_workflow_contract(ROOT)
        for field, value in (
            ("if", "false"),
            ("shell", "bash"),
            ("run", "true"),
            ("name", "removed"),
        ):
            with self.subTest(field=field):
                data = copy.deepcopy(document.data)
                step = next(
                    item
                    for item in data["jobs"]["candidate-quality"]["steps"]
                    if item.get("name") == "Verify selected Compose CLI prerequisite"
                )
                step[field] = value
                findings = github_workflow_contract._workflow_projection_findings(
                    document.path, data, data["jobs"], contract
                )
                self.assertTrue(
                    any("compose" in finding.message.lower() for finding in findings)
                )

    def test_repository_integrity_requires_compose_prerequisite(self):
        invocation = GateInvocation(
            "leaf.repository-integrity-regressions",
            Path("scripts/lib/gate/ci_gate_adapters.py"),
            (),
            Path("."),
            (),
            1200,
        )
        prerequisites = selected_prerequisites((invocation,), ())
        self.assertTrue(prerequisites.compose)
        self.assertFalse(prerequisites.docker)
        workflow = (ROOT / ".github/workflows/ci-quality.yml").read_text()
        self.assertIn("docker compose version", workflow)

    def test_dashboard_and_fixture_changes_select_p07_regressions(self):
        contract = parse_public_gate_contract(load_contract_document(ROOT))
        for path in (
            "infra/06-observability/grafana/dashboards/Observability/prometheus-overview.json",
            "tests/validation/fixtures/p07-observation/dashboards.test.yml",
            "docs/05.operations/policies/01-common/0078-compose-profile-vocabulary.md",
        ):
            with self.subTest(path=path):
                changed = (path,)
                suites = select_public_suites(contract, "changed", changed)
                roots = public_root_gate_ids(contract, suites, changed_paths=changed)
                self.assertIn("repository-integrity", suites)
                self.assertIn("leaf.repository-integrity-regressions", roots)

    def test_launcher_checks_and_changed_surfaces_are_required(self):
        contract = json.loads((ROOT / ".github/workflow-contract.yml").read_text())
        nodes = {node["gate_id"]: node for node in contract["gate_nodes"]}
        argv = nodes["leaf.repository-integrity-regressions"]["argv"]
        self.assertEqual(1, argv.count(LAUNCHER_MODULE))
        public = contract["public_gate"]
        for path in LAUNCHER_PATHS:
            with self.subTest(path=path):
                self.assertTrue(
                    any(
                        path in rule["prefixes"]
                        and "repository-integrity" in rule["suites"]
                        for rule in public["changed_path_rules"]
                    )
                )
                self.assertTrue(
                    any(
                        path in rule["prefixes"]
                        and "leaf.repository-integrity-regressions"
                        in rule["root_gate_ids"]
                        for rule in public["changed_root_rules"]
                    )
                )

    def test_observation_checks_are_required_for_changed_surfaces(self):
        contract = json.loads((ROOT / ".github/workflow-contract.yml").read_text())
        nodes = {node["gate_id"]: node for node in contract["gate_nodes"]}
        argv = nodes["leaf.repository-integrity-regressions"]["argv"]
        for module in OBSERVATION_MODULES:
            with self.subTest(module=module):
                self.assertEqual(1, argv.count(module))
        public = contract["public_gate"]
        for path in OBSERVATION_PATHS:
            with self.subTest(path=path):
                self.assertTrue(
                    any(
                        path in rule["prefixes"]
                        and "repository-integrity" in rule["suites"]
                        for rule in public["changed_path_rules"]
                    )
                )
                self.assertTrue(
                    any(
                        path in rule["prefixes"]
                        and "leaf.repository-integrity-regressions"
                        in rule["root_gate_ids"]
                        for rule in public["changed_root_rules"]
                    )
                )


if __name__ == "__main__":
    unittest.main()
