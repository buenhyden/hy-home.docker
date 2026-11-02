"""P09 control, resource, and retirement owners select bounded QA gates."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.lib.gate.ci_gate_contract import (
    load_contract_document,
    parse_public_gate_contract,
    public_root_gate_ids,
    select_public_suites,
)

ROOT = Path(__file__).resolve().parents[2]
P09_ROUTING_MODULE = "tests.validation.test_p09_ci_routing"
P09_CONTROLS_MODULE = "tests.validation.test_p09_compose_controls"
CONTROL_SURFACES = (
    "scripts/validation/compose_controls.py",
    "infra/common-optimizations.yml",
    "infra/common-optimizations.exceptions.json",
    "tests/validation/test_p09_compose_controls.py",
    "tests/validation/test_p09_ci_routing.py",
)
RESOURCE_SURFACES = (
    "scripts/lib/ops/root_resource_assessment.py",
    "scripts/operations/root-resource-assessment.py",
    "tests/lib/ops/test_root_resource_assessment.py",
    "tests/validation/test_root_resource_contract.py",
)
RETIREMENT_SURFACES = (
    "scripts/lib/ops/retire_materials.py",
    "scripts/operations/retire-materials.py",
    "tests/lib/ops/test_retirement.py",
    "tests/validation/test_retirement_cli.py",
)
UNRELATED_RETIREMENT_SUITES = {
    "agent-governance",
    "document-contract",
    "document-graph",
    "document-lifecycle",
    "operations",
}


class P09RoutingTests(unittest.TestCase):
    def setUp(self):
        self.document = json.loads(
            (ROOT / ".github/workflow-contract.yml").read_text(encoding="utf-8")
        )
        self.nodes = {node["gate_id"]: node for node in self.document["gate_nodes"]}
        self.public = parse_public_gate_contract(load_contract_document(ROOT))

    def selected(self, path: str) -> tuple[tuple[str, ...], tuple[str, ...]]:
        changed = (path,)
        suites = select_public_suites(self.public, "changed", changed)
        roots = public_root_gate_ids(self.public, suites, changed_paths=changed)
        return suites, roots

    def test_control_changes_select_focused_hardening_and_regressions(self):
        expected_roots = {
            "local.infrastructure-hardening",
            "local.template-security-baseline",
            "leaf.repository-integrity-regressions",
        }
        for path in CONTROL_SURFACES:
            with self.subTest(path=path):
                suites, roots = self.selected(path)
                self.assertIn("operations", suites)
                self.assertIn("repository-integrity", suites)
                self.assertLessEqual(expected_roots, set(roots))

    def test_resource_changes_keep_registered_repository_checks(self):
        for path in RESOURCE_SURFACES:
            with self.subTest(path=path):
                suites, roots = self.selected(path)
                self.assertIn("repository-integrity", suites)
                self.assertIn("leaf.local-script-manifest", roots)
                self.assertIn("leaf.repository-integrity-regressions", roots)

    def test_retirement_changes_do_not_fall_back_to_unrelated_suites(self):
        for path in RETIREMENT_SURFACES:
            with self.subTest(path=path):
                suites, roots = self.selected(path)
                self.assertIn("repository-integrity", suites)
                self.assertTrue(UNRELATED_RETIREMENT_SUITES.isdisjoint(suites))
                self.assertIn("leaf.local-script-manifest", roots)
                self.assertIn("leaf.repository-integrity-regressions", roots)

    def test_p09_modules_are_registered_once(self):
        repository_argv = self.nodes["leaf.repository-integrity-regressions"]["argv"]
        for module in (
            P09_ROUTING_MODULE,
            "tests.lib.ops.test_retirement",
            "tests.validation.test_retirement_cli",
            "tests.lib.ops.test_root_resource_assessment",
            "tests.validation.test_root_resource_contract",
        ):
            with self.subTest(module=module):
                self.assertEqual(1, repository_argv.count(module))

        compose_argv = self.nodes["leaf.compose-baseline-regressions"]["argv"]
        self.assertEqual(1, compose_argv.count(P09_CONTROLS_MODULE))


if __name__ == "__main__":
    unittest.main()
