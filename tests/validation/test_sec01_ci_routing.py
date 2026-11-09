"""SEC01 source regressions must run in hosted candidate QA."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

from scripts.lib.gate import ci_gate_contract as gate_contract

ROOT = Path(__file__).resolve().parents[2]
OFFLINE = (
    "tests.lib.ops.test_openbao_issuance",
    "tests.lib.ops.test_openbao_issuance_trust",
    "tests.validation.test_openbao_candidate",
    "tests.validation.test_restic_offsite_artifact",
    "tests.validation.test_sec01_version_contract",
    "tests.validation.test_sec01_next_stable_candidates",
    "tests.validation.test_sec01_next_tool_candidates",
    "tests.lib.supply_chain.test_update_gates",
    "tests.validation.test_workflow_version_bundle",
)
OFFLINE_CLASSES = (
    "tests.validation.test_openbao_candidate.ExpiryRegression",
    "tests.validation.test_workflow_version_bundle.WorkflowVersionBundleTests",
)
NATIVE = (
    "tests.validation.test_openbao_candidate.CandidateNative",
    "tests.validation.test_restic_offsite_artifact.ArtifactRehearsalTests",
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

    def test_ledger_drift_gate_runs_once_in_the_hosted_compose_leaf(self):
        module = "tests.lib.supply_chain.test_update_gates"
        compose = self.nodes["leaf.compose-baseline-regressions"]["argv"]
        local_only = self.nodes["leaf.supply-chain-fixture-policy"]["argv"]
        self.assertEqual(1, compose.count(module))
        self.assertNotIn(module, local_only)

    def test_compose_only_change_selects_the_suite_running_the_ledger_gate(self):
        public = gate_contract.parse_public_gate_contract(
            gate_contract.load_contract_document(ROOT)
        )
        reached: dict[str, set[str]] = {}
        for route in public.suites:
            pending = list(route.root_gate_ids)
            seen: set[str] = set()
            while pending:
                gate_id = pending.pop()
                if gate_id not in seen:
                    seen.add(gate_id)
                    pending.extend(self.nodes[gate_id].get("children", ()))
            reached[route.name] = seen
        for path in (
            "docker-compose.yml",
            "infra/05-messaging/kafka/docker-compose.yml",
            "infra/08-ai/crawl4ai/docker-compose.yml",
        ):
            with self.subTest(path=path):
                suites = gate_contract.select_public_suites(public, "changed", (path,))
                self.assertTrue(
                    any(
                        "leaf.compose-baseline-regressions" in reached[name]
                        for name in suites
                    )
                )

    def test_routing_regression_is_itself_required(self):
        argv = self.nodes["leaf.repository-integrity-regressions"]["argv"]
        self.assertIn("tests.validation.test_sec01_ci_routing", argv)
