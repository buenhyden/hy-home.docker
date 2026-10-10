"""SMTP safety regressions remain required without native HOME execution."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STORAGE_MODULE = "tests.validation.test_supabase_smtp_fixture_storage"
STORAGE_PATHS = (
    "tests/validation/_supabase_smtp_fixture_storage.py",
    "tests/validation/test_supabase_smtp_fixture_storage.py",
)


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
        optional = argv[split + 1 : -1]
        self.assertIn("tests.validation.test_supabase_smtp_rehearsal", argv[:split])
        self.assertIn(
            "tests.validation.test_supabase_smtp_rehearsal.SupabaseSMTPRehearsalTests",
            optional,
        )
        self.assertNotIn(
            "tests.validation.test_supabase_smtp_rehearsal.CapturedOutputSafetyTests",
            optional,
        )
        self.assertNotIn(
            "tests.validation.test_supabase_smtp_rehearsal.FixtureCleanupTimeoutTests",
            optional,
        )
        self.assertNotIn(STORAGE_MODULE, optional)
        self.assertEqual(15, len(optional))

    def test_fixture_storage_regression_and_changed_routes_are_required(self):
        argv = self.nodes["leaf.repository-integrity-regressions"]["argv"]
        self.assertEqual(1, argv.count(STORAGE_MODULE))

        public = self.contract["public_gate"]
        path_rules = [
            rule
            for rule in public["changed_path_rules"]
            if tuple(rule["prefixes"]) == STORAGE_PATHS
        ]
        self.assertEqual(
            [
                {
                    "prefixes": list(STORAGE_PATHS),
                    "suites": ["operations", "repository-integrity"],
                }
            ],
            path_rules,
        )
        root_rules = [
            rule
            for rule in public["changed_root_rules"]
            if tuple(rule["prefixes"]) == STORAGE_PATHS
        ]
        self.assertEqual(
            [
                {
                    "prefixes": list(STORAGE_PATHS),
                    "root_gate_ids": ["leaf.repository-integrity-regressions"],
                }
            ],
            root_rules,
        )
