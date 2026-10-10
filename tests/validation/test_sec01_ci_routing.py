"""SEC01 source regressions must run in hosted candidate QA."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OFFLINE = (
    "tests.lib.ops.test_openbao_issuance",
    "tests.lib.ops.test_openbao_issuance_trust",
    "tests.validation.test_openbao_candidate.ExpiryRegression",
    "tests.validation.test_sec01_version_contract",
    "tests.validation.test_workflow_version_bundle.WorkflowVersionBundleTests",
)


class Sec01RoutingTests(unittest.TestCase):
    def setUp(self):
        self.contract = json.loads((ROOT / ".github/workflow-contract.yml").read_text())
        self.nodes = {n["gate_id"]: n for n in self.contract["gate_nodes"]}

    def test_offline_security_version_and_issuance_regressions_are_required(self):
        argv = self.nodes["leaf.compose-baseline-regressions"]["argv"]
        required = argv[: argv.index("--optional-runtime-skips")]
        for module in OFFLINE:
            with self.subTest(module=module):
                self.assertIn(module, required)

    def test_supply_chain_gate_negatives_are_required(self):
        argv = self.nodes["leaf.supply-chain-fixture-policy"]["argv"]
        self.assertIn("tests.lib.supply_chain.test_update_gates", argv)

    def test_routing_regression_is_itself_required(self):
        argv = self.nodes["leaf.repository-integrity-regressions"]["argv"]
        self.assertIn("tests.validation.test_sec01_ci_routing", argv)
