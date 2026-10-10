"""SMTP safety regressions remain required without native HOME execution."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class SmtpRoutingTests(unittest.TestCase):
    def setUp(self):
        self.contract = json.loads((ROOT / ".github/workflow-contract.yml").read_text())
        self.nodes = {n["gate_id"]: n for n in self.contract["gate_nodes"]}

    def test_proof_and_generator_regressions_are_required(self):
        argv = self.nodes["leaf.repository-integrity-regressions"]["argv"]
        for module in (
            "tests.lib.ops.test_smtp_contract",
            "tests.lib.ops.test_smtp_proof",
            "tests.validation.test_smtp_generator",
            "tests.validation.test_smtp_ci_routing",
        ):
            with self.subTest(module=module):
                self.assertIn(module, argv)

    def test_only_native_smtp_class_is_optional(self):
        argv = self.nodes["leaf.compose-baseline-regressions"]["argv"]
        split = argv.index("--optional-runtime-skips")
        self.assertIn("tests.validation.test_supabase_smtp_rehearsal", argv[:split])
        self.assertIn(
            "tests.validation.test_supabase_smtp_rehearsal.SupabaseSMTPRehearsalTests",
            argv[split:],
        )
        self.assertNotIn(
            "tests.validation.test_supabase_smtp_rehearsal.CapturedOutputSafetyTests",
            argv[split:],
        )
        self.assertNotIn(
            "tests.validation.test_supabase_smtp_rehearsal.FixtureCleanupTimeoutTests",
            argv[split:],
        )
