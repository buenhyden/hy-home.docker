"""Fail-closed source readiness checks; native rehearsal is explicitly NOT_RUN."""

import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORKLOAD = ROOT / "infra/07-workflow/n8n/workloads/manifest-outbox-notifier"


class OutboxRehearsalPreflightTests(unittest.TestCase):
    def test_structurally_reviewed_binding_still_cannot_authorize_operation(self):
        spec = importlib.util.spec_from_file_location(
            "p05_preflight", WORKLOAD / "tools/preflight.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        binding = {
            "sql_commit": "a" * 40,
            "sql_sha256": "b" * 64,
            "interface_version": 1,
            "review_receipt": "synthetic-review",
        }
        self.assertEqual(
            ("native_receipts_and_exact_targets", "current_operator_authorization"),
            module.pending_prerequisites({"status": "reviewed", "binding": binding}),
        )
        for key in binding:
            self.assertIn(
                "reviewed_p04_sql_binding",
                module.pending_prerequisites(
                    {"status": "reviewed", "binding": {**binding, key: None}}
                ),
            )
        self.assertIn("reviewed_p04_sql_binding", module.pending_prerequisites(None))

    def test_reviewed_source_contract_still_cannot_satisfy_native_prerequisites(self):
        spec = importlib.util.spec_from_file_location(
            "p05_preflight", WORKLOAD / "tools/preflight.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        contract = json.loads((WORKLOAD / "outbox-contract.json").read_text())
        self.assertEqual(
            ("native_receipts_and_exact_targets", "current_operator_authorization"),
            module.pending_prerequisites(contract),
        )

    def test_hash_only_does_not_claim_sql_review_or_runtime_authorization(self):
        spec = importlib.util.spec_from_file_location(
            "p05_preflight", WORKLOAD / "tools/preflight.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        fake = {
            "status": "provisional",
            "binding": {"sql_commit": "a" * 40, "sql_sha256": "b" * 64},
        }
        self.assertIn("reviewed_p04_sql_binding", module.pending_prerequisites(fake))
        self.assertIn(
            "current_operator_authorization", module.pending_prerequisites(fake)
        )
