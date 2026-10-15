"""Synthetic outbox consumer behavior; no native DB or mail execution."""

import importlib.util
import json
import subprocess
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
WORKLOAD = ROOT / "infra/07-workflow/n8n/workloads/manifest-outbox-notifier"
BUILDER = WORKLOAD / "tools/build_workflow.py"


def load_builder():
    spec = importlib.util.spec_from_file_location("p05_builder", BUILDER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def claim():
    return {
        "id": 1,
        "run_id": "a" * 64,
        "source": "hy-home.docker",
        "row_count": 2,
        "lease_token": "00000000-0000-4000-8000-000000000002",
        "lease_until": "2099-01-01T00:00:00.000Z",
    }


class OutboxWorkflowTests(unittest.TestCase):
    def test_import_is_pure_and_builds_fresh_inactive_objects(self):
        with patch.object(
            Path, "write_text", side_effect=AssertionError("import write")
        ):
            builder = load_builder()
        first = builder.build_workflow()
        pristine = json.dumps(first, sort_keys=True)
        first["nodes"][0]["parameters"]["changed"] = True
        self.assertEqual(pristine, json.dumps(builder.build_workflow(), sort_keys=True))
        self.assertFalse(builder.build_workflow()["active"])

    def test_closed_claim_validation_rejects_malformed_input_without_echo(self):
        builder = load_builder()
        self.assertEqual(claim(), builder.validate_claim([claim()]))
        for key, value in (
            ("id", True),
            ("id", 0),
            ("id", 2**53),
            ("id", "01"),
            ("run_id", "PRIVATE-marker"),
            ("run_id", "a" * 64 + "\n"),
            ("source", "evil\r\nBcc:x"),
            ("row_count", 0),
            ("row_count", 5001),
            ("row_count", True),
            ("lease_token", "PRIVATE-marker"),
            ("lease_token", claim()["lease_token"] + "\n"),
            ("id", "1\n"),
            ("lease_until", "2099-02-30T00:00:00.000Z"),
            ("lease_until", "2099-01-01T00:00:00Z"),
            ("lease_until", None),
        ):
            with (
                self.subTest(key=key),
                self.assertRaisesRegex(ValueError, "^invalid_claim$"),
            ):
                builder.validate_claim([{**claim(), key: value}])
        for rows in (
            None,
            {},
            [None],
            [claim(), claim()],
            [{**claim(), "extra": 1}],
            [],
        ):
            with (
                self.subTest(rows=rows),
                self.assertRaisesRegex(ValueError, "^invalid_claim$"),
            ):
                builder.validate_claim(rows)
        big = {**claim(), "id": "9223372036854775807"}
        self.assertEqual(big, builder.validate_claim([big]))

    def test_javascript_and_python_guards_share_boundary_behavior(self):
        builder = load_builder()
        rows = [
            [claim()],
            [],
            [claim(), claim()],
            [{**claim(), "id": True}],
            [{**claim(), "source": "hy-home.docker\n"}],
            [{**claim(), "id": "9223372036854775807"}],
            [{**claim(), "run_id": "a" * 64 + "\n"}],
            [{**claim(), "lease_token": claim()["lease_token"] + "\n"}],
            [{**claim(), "id": "1\n"}],
        ]
        script = (
            "const validate="
            + builder.CLAIM_VALIDATOR_JS
            + ";process.stdout.write(JSON.stringify(JSON.parse(process.argv[1]).map(validate)));"
        )
        result = subprocess.run(
            ["node", "-e", script, json.dumps(rows)],
            capture_output=True,
            text=True,
            check=True,
            timeout=10,
        )
        self.assertEqual(
            [True, False, False, False, False, True, False, False, False],
            json.loads(result.stdout),
        )

    def test_public_synthetic_fixture_preserves_delivery_uncertainty(self):
        builder = load_builder()
        fixture = json.loads((WORKLOAD / "fixtures/cases.json").read_text())
        for case in fixture["outcomes"]:
            receipt = {"run_id": fixture["claim"]["run_id"], "state": case["state"]}
            self.assertEqual(
                case["expected"],
                builder.evaluate_outcome(
                    [fixture["claim"]],
                    receipt,
                    case["ack"],
                    case["retry"],
                    case["quarantine"],
                ),
            )
        self.assertEqual(
            "delivery_uncertain",
            builder.evaluate_outcome(
                [claim()], {"run_id": claim()["run_id"], "state": "unknown"}, None, True
            ),
        )

    def test_accepted_receipt_needs_current_run_and_strict_true_ack(self):
        builder = load_builder()
        receipt = {"run_id": claim()["run_id"], "state": "accepted_by_smtp"}
        self.assertEqual(
            "acknowledged", builder.evaluate_outcome([claim()], receipt, True, None)
        )
        for ack in (False, None, "true", 1):
            self.assertEqual(
                "quarantine_uncertain",
                builder.evaluate_outcome([claim()], receipt, ack, None),
            )
        for bad in (
            None,
            {},
            {**receipt, "run_id": "different"},
            {**receipt, "private": "marker"},
        ):
            self.assertEqual(
                "delivery_uncertain",
                builder.evaluate_outcome([claim()], bad, True, True),
            )

    def test_retry_requires_proven_no_send_and_unknown_requires_quarantine(self):
        builder = load_builder()
        uncertain = {"run_id": claim()["run_id"], "state": "uncertain"}
        self.assertEqual(
            "quarantine_uncertain",
            builder.evaluate_outcome([claim()], uncertain, None, True),
        )
        self.assertEqual(
            "quarantined",
            builder.evaluate_outcome([claim()], uncertain, None, True, True),
        )
        cancelled = {"run_id": claim()["run_id"], "state": "cancelled"}
        self.assertEqual(
            "retry_recorded_not_sent",
            builder.evaluate_outcome([claim()], cancelled, None, True),
        )
        for retry in (False, None, 1, "true"):
            self.assertEqual(
                "quarantine_uncertain",
                builder.evaluate_outcome([claim()], cancelled, None, retry),
            )
        self.assertEqual("empty", builder.evaluate_outcome([], None, None, None))
        self.assertEqual(
            "invalid_claim",
            builder.evaluate_outcome([{**claim(), "id": 0}], None, True, True),
        )
