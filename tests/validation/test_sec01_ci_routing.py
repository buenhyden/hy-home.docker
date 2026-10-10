"""SEC01 source regressions must run in hosted candidate QA."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OFFLINE = (
    "tests.lib.ops.test_openbao_issuance",
    "tests.lib.ops.test_openbao_issuance_trust",
    "tests.validation.test_openbao_candidate",
    "tests.validation.test_sec01_version_contract",
    "tests.validation.test_workflow_version_bundle",
)
OFFLINE_CLASSES = (
    "tests.validation.test_openbao_candidate.ExpiryRegression",
    "tests.validation.test_workflow_version_bundle.WorkflowVersionBundleTests",
)
NATIVE = (
    "tests.validation.test_openbao_candidate.CandidateNative",
    "tests.validation.test_workflow_version_bundle.WorkflowCandidateRehearsalTests",
)


class Sec01RoutingTests(unittest.TestCase):
    def setUp(self):
        self.contract = json.loads((ROOT / ".github/workflow-contract.yml").read_text())
        self.nodes = {n["gate_id"]: n for n in self.contract["gate_nodes"]}

    def test_offline_security_version_and_issuance_regressions_are_required(self):
        argv = self.nodes["leaf.compose-baseline-regressions"]["argv"]
        boundary = argv.index("--optional-runtime-skips")
        required = argv[:boundary]
        optional = argv[boundary + 1 : -1]
        for module in OFFLINE:
            with self.subTest(module=module):
                self.assertEqual(1, argv.count(module))
                self.assertIn(module, required)
                self.assertNotIn(module, optional)
        for selector in OFFLINE_CLASSES:
            with self.subTest(selector=selector):
                self.assertNotIn(selector, optional)

    def test_native_classes_follow_their_required_modules(self):
        argv = self.nodes["leaf.compose-baseline-regressions"]["argv"]
        boundary = argv.index("--optional-runtime-skips")
        required = argv[:boundary]
        optional = argv[boundary + 1 : -1]
        for selector in NATIVE:
            with self.subTest(selector=selector):
                self.assertEqual(1, argv.count(selector))
                self.assertNotIn(selector, required)
                self.assertIn(selector, optional)

    def test_required_modules_have_unique_canonical_skip_receipts(self):
        modules = (
            "tests.validation.test_openbao_candidate",
            "tests.validation.test_openbao_rehearsal",
            "tests.validation.test_workflow_version_bundle",
        )
        scopes = (
            "tests.validation.test_openbao_candidate.CandidateNative",
            "tests.validation.test_openbao_rehearsal.OpenBaoRehearsalTests",
            "tests.validation.test_workflow_version_bundle.WorkflowCandidateRehearsalTests",
        )
        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/lib/gate/ci_gate_adapters.py"),
                "run-unittest",
                *modules,
                "--optional-runtime-skips",
                *scopes,
                "-v",
            ],
            cwd=ROOT,
            env={"PATH": os.environ["PATH"]},
            capture_output=True,
            text=True,
            check=False,
            timeout=60,
        )
        self.assertEqual(0, result.returncode, result.stderr)

    def test_supply_chain_gate_negatives_are_required(self):
        argv = self.nodes["leaf.supply-chain-fixture-policy"]["argv"]
        self.assertIn("tests.lib.supply_chain.test_update_gates", argv)

    def test_routing_regression_is_itself_required(self):
        argv = self.nodes["leaf.repository-integrity-regressions"]["argv"]
        self.assertIn("tests.validation.test_sec01_ci_routing", argv)
