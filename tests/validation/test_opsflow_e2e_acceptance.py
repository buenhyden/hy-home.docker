"""Offline P04/P05 acceptance seams; no native SQL, SMTP or recovery proof."""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from scripts.lib.gate.ci_gate_contract import (
    load_contract_document,
    parse_public_gate_contract,
    public_root_gate_ids,
    select_public_suites,
)
from tests.lib.ops import test_opsflow_adapters as driver_fixtures

ROOT = Path(__file__).resolve().parents[2]
FIXTURES = ROOT / "tests/fixtures/opsflow-acceptance"
NOTIFIER = ROOT / "infra/07-workflow/n8n/workloads/manifest-outbox-notifier"
adapters = driver_fixtures.adapters
# Use the existing parser instance imported by the P04 adapter tests.
parser = sys.modules["workflow_lib.manifest"]


def load_tool(name):
    spec = importlib.util.spec_from_file_location(
        "p10_" + name, NOTIFIER / "tools" / (name + ".py")
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


builder = load_tool("build_workflow")
preflight = load_tool("preflight")


class OpsflowAcceptanceSeams(unittest.TestCase):
    """Compose real public APIs with existing synthetic SDK/driver doubles."""

    def setUp(self):
        self.raw = (FIXTURES / "manifest.valid.json").read_bytes()
        self.cases = json.loads((FIXTURES / "cases.json").read_text())
        self.client = driver_fixtures.S3Double()
        self.connection = driver_fixtures.ConnectionDouble()
        self.connect = Mock(return_value=self.connection)
        self.modules = patch.dict(
            sys.modules,
            {
                "boto3": types.SimpleNamespace(client=Mock(return_value=self.client)),
                "botocore.config": types.SimpleNamespace(Config=lambda **kw: kw),
                "psycopg2": types.SimpleNamespace(connect=self.connect),
                "psycopg2.extras": types.SimpleNamespace(Json=lambda value: value),
            },
        )
        self.modules.start()
        self.addCleanup(self.modules.stop)
        self.store = adapters.S3Store(driver_fixtures.s3_config())
        self.publisher = adapters.PgPublisher(driver_fixtures.pg_config())
        self.source = self.cases["source"]
        self.day = self.cases["business_date"]
        self.key = parser.object_key(self.source, self.day)
        self.client.objects[self.key] = self.raw

    def ingest(self):
        return parser.ingest(self.store, self.publisher, self.source, self.day)

    def claim(self, result):
        # Synthetic caller projection, not a DB claim/outbox implementation.
        return dict(
            self.cases["synthetic_claim"],
            run_id=result["run_id"],
            source=self.source,
            row_count=result["records"],
        )

    def test_verified_publication_identity_reaches_notification_projection(self):
        result = self.ingest()
        expected_digest = hashlib.sha256(self.raw).hexdigest()
        expected_id = hashlib.sha256(
            (self.source + ":" + expected_digest).encode()
        ).hexdigest()
        artifact = "manifest-validated/" + self.source + "/" + expected_id + ".json"
        self.assertEqual(
            result,
            {
                "run_id": expected_id,
                "data_version": expected_digest,
                "status": "published",
                "records": 1,
            },
        )
        self.assertEqual(self.connection.params[1:3], (expected_id, expected_digest))
        self.assertEqual(self.connection.params[-1], artifact)
        self.assertIn("ops_flow.publish_manifest(%s", self.connection.query)
        self.assertEqual(self.client.objects[artifact], self.raw)
        self.assertTrue(self.connection.committed)
        self.assertTrue(self.connection.closed)
        puts = [kw for kind, kw in self.client.requests if kind == "put"]
        self.assertEqual(puts[0]["IfNoneMatch"], "*")
        row = builder.validate_claim([self.claim(result)])
        self.assertEqual(row["run_id"], expected_id)
        self.assertNotIn("data_version", row)
        self.assertEqual(
            builder.evaluate_outcome(
                [row], {"run_id": expected_id, "state": "accepted_by_smtp"}, True, False
            ),
            "acknowledged",
        )
        # Synthetic publication cannot authorize native notification.
        contract = json.loads((NOTIFIER / "outbox-contract.json").read_text())
        pending = preflight.pending_prerequisites(contract)
        self.assertNotIn("reviewed_p04_sql_binding", pending)
        self.assertIn("native_receipts_and_exact_targets", pending)
        self.assertIn("current_operator_authorization", pending)

    def test_failed_database_keeps_verified_object_and_replay_reuses_it(self):
        self.connection.fail = True
        with self.assertRaisesRegex(parser.ContractError, "^publication_failed$"):
            self.ingest()
        self.assertTrue(self.connection.rolled_back)
        self.assertFalse(self.connection.committed)
        artifacts = {k: v for k, v in self.client.objects.items() if k != self.key}
        self.assertEqual(list(artifacts.values()), [self.raw])
        self.connection.fail = False
        self.connection.status = "replayed"
        result = self.ingest()
        self.assertEqual(result["status"], "replayed")
        self.assertEqual(result["run_id"], next(iter(artifacts)).split("/")[-1][:-5])
        self.assertEqual(len([r for r in self.client.requests if r[0] == "put"]), 1)
        self.assertEqual(
            builder.validate_claim([self.claim(result)])["run_id"], result["run_id"]
        )
        self.assertEqual(
            {k: v for k, v in self.client.objects.items() if k != self.key}, artifacts
        )

    def test_conflicting_existing_artifact_cannot_publish_or_be_overwritten(self):
        digest = hashlib.sha256(self.raw).hexdigest()
        identifier = hashlib.sha256((self.source + ":" + digest).encode()).hexdigest()
        key = "manifest-validated/" + self.source + "/" + identifier + ".json"
        self.client.objects[key] = b"synthetic conflicting bytes"
        with self.assertRaisesRegex(
            parser.ContractError, "^artifact_verification_failed$"
        ):
            self.ingest()
        self.connect.assert_not_called()
        self.assertEqual(self.client.objects[key], b"synthetic conflicting bytes")
        self.assertFalse(any(kind == "put" for kind, _ in self.client.requests))

    def test_rejected_partition_or_sensitive_path_has_no_publication_side_effect(self):
        original = json.loads(self.raw)
        for case in self.cases["invalid_manifests"]:
            with self.subTest(case=case["name"]):
                payload = copy.deepcopy(original)
                if case["field"] == "path":
                    payload["records"][0]["path"] = case["value"]
                else:
                    payload[case["field"]] = case["value"]
                raw = json.dumps(payload).encode()
                digest = hashlib.sha256(raw).hexdigest()
                quarantine = (
                    f"manifest-quarantine/{self.source}/{self.day}/{digest}.json"
                )
                # Each rejection starts with a separate input object. A prior
                # case's preserved quarantine is not this case's evidence.
                self.client.objects = {self.key: raw}
                self.client.metadata = {}
                self.client.requests = []
                self.client.bodies = []
                with self.assertRaisesRegex(
                    parser.ContractError, "^" + case["error"] + "$"
                ):
                    self.ingest()
                self.connect.assert_not_called()
                self.assertFalse(self.connection.committed)
                self.assertFalse(hasattr(self.connection, "query"))
                self.assertEqual(self.client.objects, {self.key: raw, quarantine: raw})
                self.assertFalse(
                    any(
                        key.startswith("manifest-validated/")
                        for key in self.client.objects
                    )
                )
                puts = [
                    request for kind, request in self.client.requests if kind == "put"
                ]
                self.assertEqual(len(puts), 1)
                self.assertEqual(puts[0]["Key"], quarantine)
                self.assertEqual(puts[0]["IfNoneMatch"], "*")
                self.assertEqual(
                    self.client.metadata[quarantine],
                    {
                        "ContentType": "application/json",
                        "Metadata": {
                            "reason": "partition_mismatch"
                            if case["error"] == "partition_mismatch"
                            else "manifest_invalid",
                            "data-version": digest,
                        },
                    },
                )
                self.assertTrue(all(stream.closed for stream in self.client.bodies))
                with self.assertRaisesRegex(
                    parser.ContractError, "^" + case["error"] + "$"
                ):
                    self.ingest()
                self.assertEqual(
                    len(
                        [
                            request
                            for kind, request in self.client.requests
                            if kind == "put"
                        ]
                    ),
                    1,
                )
                self.connect.assert_not_called()

    def test_failed_quarantine_never_starts_validation_or_sql_publication(self):
        payload = json.loads(self.raw)
        payload["records"][0]["path"] = "docs/../rejected.md"
        raw = json.dumps(payload).encode()
        self.client.objects = {self.key: raw}
        with patch.object(
            self.client,
            "put_object",
            side_effect=driver_fixtures.S3Error("AccessDenied"),
        ):
            with self.assertRaisesRegex(
                parser.ContractError, "^quarantine_verification_failed$"
            ):
                self.ingest()
        self.assertEqual(self.client.objects, {self.key: raw})
        self.connect.assert_not_called()
        self.assertFalse(self.connection.committed)
        self.assertFalse(hasattr(self.connection, "query"))

    def test_notification_ack_loss_and_wrong_receipt_never_claim_success(self):
        result = self.ingest()
        row = self.claim(result)
        for case in self.cases["notification_outcomes"]:
            with self.subTest(case=case["name"]):
                receipt_id = "0" * 64 if case["wrong_run"] else result["run_id"]
                actual = builder.evaluate_outcome(
                    [row],
                    {"run_id": receipt_id, "state": case["state"]},
                    case["ack"],
                    case["retry"],
                    case["quarantine"],
                )
                self.assertEqual(actual, case["expected"])
        invalid = dict(row, lease_until="synthetic-only-not-consumer-field")
        with self.assertRaisesRegex(ValueError, "^invalid_claim$"):
            builder.validate_claim([invalid])


class OpsflowAcceptanceRegistration(unittest.TestCase):
    def test_acceptance_module_and_fixtures_are_required_by_current_gate(self):
        document = load_contract_document(ROOT)
        leaf = next(
            n
            for n in document["gate_nodes"]
            if n["gate_id"] == "leaf.repository-integrity-regressions"
        )
        self.assertIn("tests.validation.test_opsflow_e2e_acceptance", leaf["argv"])
        public = parse_public_gate_contract(document)
        for path in (
            "tests/validation/test_opsflow_e2e_acceptance.py",
            "tests/fixtures/opsflow-acceptance/cases.json",
        ):
            suites = select_public_suites(public, "changed", (path,))
            roots = public_root_gate_ids(public, suites, changed_paths=(path,))
            self.assertIn("leaf.repository-integrity-regressions", roots)
        registry = json.loads((ROOT / "docs/99.templates/registry.json").read_text())
        profile = next(p for p in registry["profiles"] if p["id"] == "package-readme")
        self.assertIn(
            "tests/fixtures/opsflow-acceptance/README.md", profile["additional_paths"]
        )


if __name__ == "__main__":
    unittest.main()
