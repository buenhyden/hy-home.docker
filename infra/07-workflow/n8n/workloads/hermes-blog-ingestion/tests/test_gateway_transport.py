"""Offline replay boundary tests; no live n8n or Gateway is exercised."""

import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from publisher.delivery import DispatchRequest, FailureKind, TransportFailure
from publisher.gateway_adapter import DESTINATION, REVISION

KEY = ("6eabd835f969", "a" * 32)
SOURCE_SHA = "c" * 64
BODY = json.dumps(
    {
        "job_id": KEY[0],
        "run_id": KEY[1],
        "source_sha256": SOURCE_SHA,
        "idempotency_key": hashlib.sha256((KEY[0] + ":" + KEY[1]).encode()).hexdigest(),
    }
).encode()
BODY_SHA = hashlib.sha256(BODY).hexdigest()
ENDPOINT_SHA = "e" * 64
REQUEST = DispatchRequest(
    KEY, SOURCE_SHA, BODY_SHA, REVISION, DESTINATION, BODY, ENDPOINT_SHA
)


class Box:
    def __init__(self):
        self.row = dict(
            job_id=KEY[0],
            run_id=KEY[1],
            source_sha256=SOURCE_SHA,
            body_sha256=BODY_SHA,
            request_body=BODY,
            contract_revision=REVISION,
            destination=DESTINATION,
            endpoint_sha256=ENDPOINT_SHA,
            status="uncertain",
        )

    def get(self, key):
        if key != KEY:
            raise ValueError("private secret")
        return self.row.copy()

    def get_unverified_evidence(self, key):
        return None


class Network:
    endpoint_sha256 = ENDPOINT_SHA

    def __init__(self):
        self.sent = []

    def send(self, request):
        self.sent.append(request)
        return "synthetic response"


class GatewayTransportTests(unittest.TestCase):
    def setUp(self):
        # Exercise the isolated replay state machine, not Hermes dispatch authorization.
        gate = patch("publisher.policy.evidence_required", return_value=False)
        gate.start()
        self.addCleanup(gate.stop)
        self.box = Box()
        self.network = Network()

    def transport(self, **kwargs):
        from publisher.gateway_transport import GatewayReplayTransport

        return GatewayReplayTransport(self.box, self.network, **kwargs)

    def test_real_adapter_outbox_replays_lost_receipt_using_pinned_schema(self):
        import jsonschema
        from publisher.candidates import Snapshot
        from publisher.delivery import process_one
        from publisher.gateway_adapter import GatewayAdapter
        from publisher.gateway_transport import GatewayReplayTransport
        from publisher.http_transport import HttpResponse
        from publisher.outbox import Outbox

        fixtures = Path(__file__).parent / "fixtures"
        request_schema = json.loads(
            (fixtures / "ingestion-v1.schema.json").read_bytes()
        )
        receipt_schema = json.loads(
            (fixtures / "responses-v1.schema.json").read_bytes()
        )["definitions"]["receipt"]
        report_id = "12345678-1234-1234-1234-123456789abc"
        source = b"synthetic original report\n"
        source_ref = "cron/output/6eabd835f969/report.md"
        candidate = {
            "job_id": KEY[0],
            "run_id": KEY[1],
            "report_kind": "strategy-news",
            "generated_at": "2026-10-30T00:01:00Z",
            "source_ref": source_ref,
            "source_sha256": hashlib.sha256(source).hexdigest(),
            "items": [{"title": "Example", "summary": "synthetic", "source_url": None}],
        }
        adapter = GatewayAdapter(
            scheduled_at="2026-10-30T00:00:00Z",
            generated_at="2026-10-30T00:01:00Z",
            collected_at="2026-10-30T00:02:00Z",
        )

        class SyntheticGateway:
            endpoint_sha256 = ENDPOINT_SHA

            def __init__(self):
                self.saved = {}
                self.requests = []

            def send(self, request):
                body = json.loads(request.body)
                jsonschema.validate(
                    body, request_schema, format_checker=jsonschema.FormatChecker()
                )
                self.requests.append(request.body)
                identity = body["idempotency_key"]
                if identity not in self.saved:
                    self.saved[identity] = request.body
                    raise TransportFailure(FailureKind.AMBIGUOUS)
                if self.saved[identity] != request.body:
                    raise AssertionError("same key with changed body")
                receipt = dict(
                    id=report_id,
                    persisted=True,
                    duplicate=True,
                    status="received",
                    candidate_count=len(body["items"]),
                    status_url=f"/v1/ingestions/{report_id}",
                )
                jsonschema.validate(receipt, receipt_schema)
                return HttpResponse(
                    200, json.dumps(receipt).encode(), "application/json"
                )

        with tempfile.TemporaryDirectory(dir="/tmp") as tmp:
            path = Path(tmp) / "private" / "outbox.sqlite"
            gateway = SyntheticGateway()
            box = Outbox(path)
            box.stage(
                Snapshot(*KEY, json.dumps(candidate).encode(), source_ref, source)
            )
            transport = GatewayReplayTransport(
                box, gateway, allow_idempotent_replay=True
            )
            self.assertEqual(
                process_one(box, KEY, adapter, transport, now=100), "uncertain"
            )
            self.assertEqual(len(gateway.saved), 1)
            box.close()
            box = Outbox(path)
            transport = GatewayReplayTransport(
                box, gateway, allow_idempotent_replay=True
            )
            self.assertEqual(
                process_one(box, KEY, adapter, transport, now=200), "delivered"
            )
            self.assertEqual(gateway.requests[0], gateway.requests[1])
            self.assertEqual(len(gateway.saved), 1)
            self.assertEqual(box.get(KEY)["receipt"]["gateway_report_id"], report_id)
            box.close()
            box = Outbox(path)
            self.assertEqual(box.get(KEY)["receipt"]["gateway_report_id"], report_id)
            box.close()

    def test_replay_rejects_missing_or_malformed_endpoint_binding(self):
        from publisher.gateway_transport import GatewayReplayTransport

        for digest in (None, "", "a" * 63, "g" * 64):
            network = Network()
            network.endpoint_sha256 = digest
            with self.subTest(digest=digest), self.assertRaises(ValueError):
                GatewayReplayTransport(self.box, network)
        with self.assertRaises(ValueError):
            GatewayReplayTransport(self.box, object())

    def test_null_or_different_request_binding_never_reaches_transport(self):
        from dataclasses import replace

        relay = self.transport(allow_idempotent_replay=True)
        for endpoint in (None, "f" * 64):
            self.box.row["endpoint_sha256"] = endpoint
            with self.subTest(endpoint=endpoint), self.assertRaises(TransportFailure):
                relay.reconcile(replace(REQUEST, endpoint_sha256=endpoint))
        self.assertEqual(self.network.sent, [])

    def test_transport_endpoint_cannot_change_after_construction(self):
        relay = self.transport(allow_idempotent_replay=True)
        self.network.endpoint_sha256 = "f" * 64
        with self.assertRaises(TransportFailure):
            relay.reconcile(REQUEST)
        self.assertEqual(self.network.sent, [])

    def test_replay_requires_explicit_true_and_uncertain_bound_record(self):
        with self.assertRaises(TransportFailure) as error:
            self.transport().reconcile(REQUEST)
        self.assertEqual(error.exception.kind, FailureKind.AMBIGUOUS)
        self.assertEqual(self.network.sent, [])
        self.assertEqual(
            self.transport(allow_idempotent_replay=True).reconcile(REQUEST),
            "synthetic response",
        )
        self.assertEqual(self.network.sent, [REQUEST])
        self.box.row["status"] = "pending"
        with self.assertRaises(TransportFailure):
            self.transport(allow_idempotent_replay=True).reconcile(REQUEST)
        self.assertEqual(len(self.network.sent), 1)

    def test_lost_response_replay_uses_bound_bytes_after_restart_and_budget(self):
        from publisher.candidates import Snapshot
        from publisher.delivery import (
            BoundRequest,
            Outcome,
            OutcomeKind,
            Receipt,
            process_one,
        )
        from publisher.gateway_transport import GatewayReplayTransport
        from publisher.outbox import Outbox

        class Adapter:
            idempotent_writes = True

            def prepare(self, snapshot):
                body = json.dumps(
                    {
                        "job_id": snapshot["job_id"],
                        "run_id": snapshot["run_id"],
                        "source_sha256": snapshot["source_sha256"],
                        "idempotency_key": hashlib.sha256(
                            (KEY[0] + ":" + KEY[1]).encode()
                        ).hexdigest(),
                    }
                ).encode()
                return BoundRequest(REVISION, DESTINATION, body)

            def interpret(self, response, request):
                return Outcome(
                    OutcomeKind.DURABLE,
                    Receipt(
                        request.key, request.source_sha256, request.body_sha256, True
                    ),
                )

        class Flaky:
            endpoint_sha256 = ENDPOINT_SHA

            def __init__(self):
                self.bodies = []
                self.always_fail = False

            def send(self, request):
                self.bodies.append(request.body)
                if len(self.bodies) == 1 or self.always_fail:
                    raise TransportFailure(FailureKind.AMBIGUOUS)
                return "synthetic persisted"

        with tempfile.TemporaryDirectory(dir="/tmp") as tmp:
            path = Path(tmp) / "private" / "outbox.sqlite"
            box = Outbox(path)
            box.stage(Snapshot(*KEY, b"candidate", "synthetic", b"source"))
            adapter, network = Adapter(), Flaky()
            transport = GatewayReplayTransport(
                box, network, allow_idempotent_replay=True
            )
            self.assertEqual(
                process_one(box, KEY, adapter, transport, now=100), "uncertain"
            )
            box.close()
            box = Outbox(path)
            transport = GatewayReplayTransport(
                box, network, allow_idempotent_replay=True
            )
            self.assertEqual(
                process_one(box, KEY, adapter, transport, now=200), "delivered"
            )
            self.assertEqual(network.bodies[0], network.bodies[1])
            self.assertEqual(
                process_one(box, KEY, adapter, transport, now=300), "delivered"
            )
            self.assertEqual(len(network.bodies), 2)
            box.close()

        with tempfile.TemporaryDirectory(dir="/tmp") as tmp:
            box = Outbox(Path(tmp) / "private" / "outbox.sqlite")
            box.stage(Snapshot(*KEY, b"candidate", "synthetic", b"source"))
            network = Flaky()
            network.always_fail = True
            transport = GatewayReplayTransport(
                box, network, allow_idempotent_replay=True
            )
            for now in (100, 200, 300):
                self.assertEqual(
                    process_one(box, KEY, adapter, transport, now=now, max_attempts=2),
                    "uncertain",
                )
            self.assertEqual(len(network.bodies), 2)
            box.close()

    def test_send_requires_sending_bound_record(self):
        self.box.row["status"] = "sending"
        self.assertEqual(self.transport().send(REQUEST), "synthetic response")
        self.assertEqual(self.network.sent, [REQUEST])
        self.box.row["status"] = "uncertain"
        with self.assertRaises(TransportFailure) as error:
            self.transport().send(REQUEST)
        self.assertEqual(error.exception.kind, FailureKind.NOT_SENT)
        self.assertEqual(len(self.network.sent), 1)

    def test_replay_rejects_changed_persisted_binding(self):
        for field, value in (
            ("job_id", "other"),
            ("run_id", "other"),
            ("source_sha256", "d" * 64),
            ("body_sha256", "d" * 64),
            ("request_body", b"changed"),
            ("contract_revision", "other"),
            ("destination", "other"),
        ):
            with self.subTest(field=field):
                old = self.box.row[field]
                self.box.row[field] = value
                with self.assertRaises(TransportFailure) as error:
                    self.transport(allow_idempotent_replay=True).reconcile(REQUEST)
                self.assertEqual(error.exception.kind, FailureKind.AMBIGUOUS)
                self.box.row[field] = old
        self.assertEqual(self.network.sent, [])

    def test_replay_rejects_changed_request_or_invalid_json_identity(self):
        from dataclasses import replace

        for request in (
            replace(REQUEST, key=("other", KEY[1])),
            replace(REQUEST, body=BODY + b" "),
            replace(REQUEST, contract_revision="other"),
            replace(REQUEST, destination="other"),
        ):
            with (
                self.subTest(request=repr(request)),
                self.assertRaises(TransportFailure),
            ):
                self.transport(allow_idempotent_replay=True).reconcile(request)
        # Even an internally consistent persisted body must contain the correct key.
        for update in (
            {"job_id": "other"},
            {"run_id": "other"},
            {"source_sha256": "f" * 64},
            {"idempotency_key": "f" * 64},
        ):
            obj = json.loads(BODY)
            obj.update(update)
            body = json.dumps(obj).encode()
            sha = hashlib.sha256(body).hexdigest()
            self.box.row.update(request_body=body, body_sha256=sha)
            with self.subTest(update=update), self.assertRaises(TransportFailure):
                self.transport(allow_idempotent_replay=True).reconcile(
                    replace(REQUEST, body=body, body_sha256=sha)
                )
        self.assertEqual(self.network.sent, [])
