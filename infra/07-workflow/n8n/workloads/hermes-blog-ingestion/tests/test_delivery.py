"""Synthetic state-machine evidence, never Gateway API compatibility."""

import contextlib
import hashlib
import io
import sys
import tempfile
import unittest
from importlib import import_module
from pathlib import Path

WORKLOAD = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WORKLOAD))

Snapshot = import_module("publisher.candidates").Snapshot
Outbox = import_module("publisher.outbox").Outbox

KEY = ("6eabd835f969", "a" * 32)
SOURCE = b"original synthetic report private-source-marker"
BODY = b"synthetic request; not a Gateway fixture"


class SyntheticGateway:
    """In-memory durable-effect model; no HTTP or actual API assumptions."""

    def __init__(self):
        self.rows = {}
        self.operations = []
        self.failure = None
        self.lose_response = False
        self.response = None

    def send(self, request):
        from publisher.delivery import FailureKind, TransportFailure

        self.operations.append("send")
        if self.failure:
            raise self.failure
        prior = self.rows.get(request.key)
        if prior and prior != request.body_sha256:
            return ("conflict", None)
        self.rows[request.key] = request.body_sha256
        if self.lose_response:
            self.lose_response = False
            raise TransportFailure(FailureKind.AMBIGUOUS)
        return self.response if self.response is not None else ("persisted", request)

    def reconcile(self, request):
        self.operations.append("reconcile")
        if self.failure:
            raise self.failure
        if request.key in self.rows:
            return ("persisted", request)
        return ("absent", None)


class SyntheticAdapter:
    idempotent_writes = True

    def __init__(self):
        self.body = BODY
        self.destination = "synthetic_gateway"
        self.revision = "synthetic_v1"
        self.bad_receipt = None

    def prepare(self, snapshot):
        from publisher.delivery import BoundRequest

        return BoundRequest(self.revision, self.destination, self.body)

    def interpret(self, response, request):
        from publisher.delivery import Outcome, OutcomeKind, Receipt

        if not isinstance(response, tuple):
            return Outcome(OutcomeKind.UNKNOWN)
        kind, _ = response
        if kind == "persisted":
            receipt = self.bad_receipt or Receipt(
                request.key, request.source_sha256, request.body_sha256, True
            )
            return Outcome(OutcomeKind.DURABLE, receipt)
        return Outcome(
            {
                "conflict": OutcomeKind.CONFLICT,
                "rejected": OutcomeKind.REJECTED,
                "absent": OutcomeKind.ABSENT,
            }[kind]
        )


class DeliveryTests(unittest.TestCase):
    def test_request_repr_redacts_body_but_preserves_identity(self):
        from publisher.delivery import BoundRequest, DispatchRequest

        marker = b"private request body marker"
        bound = BoundRequest("revision", "destination", marker)
        dispatch = DispatchRequest(
            KEY, "a" * 64, "b" * 64, "revision", "destination", marker
        )
        for request in (bound, dispatch):
            with self.subTest(kind=type(request).__name__):
                self.assertNotIn(marker.decode(), repr(request))
                self.assertIn("destination", repr(request))
                self.assertEqual(request.body, marker)

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="hermes-delivery-", dir="/tmp")
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "private" / "outbox.sqlite"
        self.box = Outbox(self.path)
        self.addCleanup(lambda: self.box.close())
        self.snapshot = Snapshot(
            *KEY, b"synthetic candidate", "cron/output/synthetic.md", SOURCE
        )
        self.box.stage(self.snapshot)
        self.adapter = SyntheticAdapter()
        self.gateway = SyntheticGateway()

    def process(self, now=100, **kwargs):
        from publisher.delivery import process_one

        return process_one(self.box, KEY, self.adapter, self.gateway, now=now, **kwargs)

    def uncertain(self):
        self.gateway.lose_response = True
        self.assertEqual(self.process(), "uncertain")

    def test_missing_contract_cannot_dispatch_or_mark_delivered(self):
        from publisher.delivery import process_one

        self.assertEqual(process_one(self.box, KEY, now=100), "blocked")
        self.assertEqual(self.box.get(KEY)["status"], "awaiting_contract")
        self.assertEqual(self.gateway.rows, {})

    def test_durable_receipt_delivers_once_and_retains_original(self):
        self.assertEqual(self.process(), "delivered")
        self.assertEqual(self.process(now=200), "delivered")
        self.assertEqual(len(self.gateway.rows), 1)
        self.assertEqual(self.gateway.operations, ["send"])
        self.assertEqual(self.box.get(KEY)["source"], SOURCE)
        self.assertIs(self.box.get(KEY)["receipt"]["persisted"], True)

    def test_gateway_report_id_is_retained_across_restart(self):
        from publisher.delivery import Receipt

        report_id = "12345678-1234-1234-1234-123456789abc"
        self.adapter.bad_receipt = Receipt(
            KEY,
            hashlib.sha256(SOURCE).hexdigest(),
            hashlib.sha256(BODY).hexdigest(),
            True,
            gateway_report_id=report_id,
        )
        self.assertEqual(self.process(), "delivered")
        self.box.close()
        self.box = Outbox(self.path)
        self.assertEqual(self.box.get(KEY)["receipt"]["gateway_report_id"], report_id)
        self.assertEqual(self.process(now=200), "delivered")
        self.assertEqual(self.gateway.operations, ["send"])

    def test_invalid_gateway_report_id_never_marks_delivered(self):
        from publisher.delivery import Receipt

        self.adapter.bad_receipt = Receipt(
            KEY,
            hashlib.sha256(SOURCE).hexdigest(),
            hashlib.sha256(BODY).hexdigest(),
            True,
            gateway_report_id="invalid-secret-value",
        )
        self.assertEqual(self.process(), "uncertain")
        self.assertIsNone(self.box.get(KEY)["receipt"])

    def test_lost_response_reconciles_without_duplicate_effect(self):
        self.uncertain()
        self.assertEqual(len(self.gateway.rows), 1)
        self.assertEqual(self.process(now=200), "delivered")
        self.assertEqual(self.gateway.operations, ["send", "reconcile"])
        self.assertEqual(len(self.gateway.rows), 1)

    def test_changed_or_broken_adapter_preserves_uncertain_write(self):
        self.uncertain()
        original = self.box.get(KEY)["request_body"]
        self.adapter.destination = "different_gateway"
        self.assertEqual(self.process(now=200), "uncertain")
        self.assertEqual(self.gateway.operations, ["send"])
        self.assertEqual(self.box.get(KEY)["request_body"], original)

        def broken_prepare(snapshot):
            raise ValueError("synthetic adapter failure")

        self.adapter.prepare = broken_prepare
        self.assertEqual(self.process(now=300), "uncertain")
        self.assertEqual(self.gateway.operations, ["send"])
        self.assertEqual(self.box.get(KEY)["request_body"], original)

    def test_reconcile_rejection_or_conflict_preserves_uncertainty(self):
        self.uncertain()
        self.gateway.reconcile = lambda request: ("rejected", None)
        self.assertEqual(self.process(now=200), "uncertain")
        self.gateway.reconcile = lambda request: ("conflict", None)
        self.assertEqual(self.process(now=300), "uncertain")
        self.assertEqual(len(self.gateway.rows), 1)

    def test_alternating_prepare_failures_are_bounded_and_recover(self):
        self.uncertain()
        original = self.box.get(KEY)["request_body"]
        prepare = self.adapter.prepare

        def broken_prepare(snapshot):
            raise ValueError("synthetic adapter failure")

        for _ in range(30):
            self.adapter.prepare = prepare
            self.adapter.destination = "different_gateway"
            self.assertEqual(self.process(now=200), "uncertain")
            self.adapter.prepare = broken_prepare
            self.assertEqual(self.process(now=200), "uncertain")
        codes = [event["code"] for event in self.box.events(KEY)]
        self.assertEqual(codes.count("request_conflict"), 1)
        self.assertEqual(codes.count("adapter_error"), 1)
        self.assertEqual(self.box.get(KEY)["request_body"], original)
        self.assertEqual(self.gateway.operations, ["send"])
        self.adapter.prepare = prepare
        self.adapter.destination = "synthetic_gateway"
        self.assertEqual(self.process(now=200), "delivered")
        self.assertEqual(self.gateway.operations, ["send", "reconcile"])

    def test_repeated_adapter_failure_records_once_and_recovers(self):
        self.uncertain()
        original = self.box.get(KEY)["request_body"]
        self.adapter.destination = "different_gateway"
        self.assertEqual(self.process(now=200), "uncertain")
        event_count = len(self.box.events(KEY))
        for _ in range(30):
            self.assertEqual(self.process(now=200), "uncertain")
        self.assertEqual(len(self.box.events(KEY)), event_count)
        self.assertEqual(self.box.get(KEY)["request_body"], original)
        self.assertEqual(self.gateway.operations, ["send"])
        self.adapter.destination = "synthetic_gateway"
        self.assertEqual(self.process(now=200), "delivered")
        self.assertEqual(self.gateway.operations, ["send", "reconcile"])

    def test_restart_preserves_uncertainty_and_attempt_budget(self):
        self.uncertain()
        self.box.close()
        self.box = Outbox(self.path)
        self.assertEqual(self.box.get(KEY)["attempts"], 1)
        self.assertEqual(self.process(now=200), "delivered")
        self.assertEqual(self.box.get(KEY)["attempts"], 2)

    def test_crash_in_sending_recovers_to_reconciliation(self):
        self.box.bind_request(
            KEY, "synthetic_v1", BODY, destination="synthetic_gateway"
        )
        self.box.transition(KEY, "awaiting_contract", "pending")
        self.box.transition(KEY, "pending", "sending", attempts=1)
        self.assertEqual(self.process(now=200), "pending")
        self.assertEqual(self.gateway.operations, ["reconcile"])
        self.assertEqual(self.box.get(KEY)["source"], SOURCE)

    def test_not_found_reconciliation_resends_only_next_operation(self):
        from publisher.delivery import FailureKind, TransportFailure

        self.gateway.failure = TransportFailure(FailureKind.AMBIGUOUS)
        self.assertEqual(self.process(), "uncertain")
        self.gateway.failure = None
        self.assertEqual(self.process(now=200), "pending")
        self.assertEqual(self.gateway.rows, {})
        self.assertEqual(self.process(now=300), "delivered")
        self.assertEqual(self.gateway.operations, ["send", "reconcile", "send"])

    def test_without_idempotency_guarantee_absent_stays_uncertain(self):
        from publisher.delivery import FailureKind, TransportFailure

        self.gateway.failure = TransportFailure(FailureKind.AMBIGUOUS)
        self.assertEqual(self.process(), "uncertain")
        self.gateway.failure = None
        self.adapter.idempotent_writes = False
        self.assertEqual(self.process(now=200), "uncertain")
        self.assertEqual(self.gateway.rows, {})

    def test_proven_no_send_uses_persistent_delayed_retry(self):
        from publisher.delivery import FailureKind, TransportFailure

        self.gateway.failure = TransportFailure(FailureKind.NOT_SENT)
        self.assertEqual(self.process(base_delay=10), "pending")
        self.assertEqual(self.box.get(KEY)["next_attempt"], 110)
        self.gateway.failure = None
        self.assertEqual(self.process(now=109), "deferred")
        self.assertEqual(self.gateway.rows, {})
        self.assertEqual(self.process(now=110), "delivered")

    def test_uncertain_outage_exhaustion_preserves_uncertain(self):
        from publisher.delivery import FailureKind, TransportFailure

        self.gateway.failure = TransportFailure(FailureKind.AMBIGUOUS)
        self.assertEqual(self.process(max_attempts=2), "uncertain")
        self.assertEqual(self.process(now=200, max_attempts=2), "uncertain")
        self.assertEqual(self.process(now=300, max_attempts=2), "uncertain")
        self.assertEqual(self.gateway.operations, ["send", "reconcile"])
        self.assertEqual(self.box.get(KEY)["attempts"], 2)
        self.assertEqual(self.box.events(KEY)[-1]["code"], "retry_exhausted")

    def test_proven_no_send_exhaustion_is_failed(self):
        from publisher.delivery import FailureKind, TransportFailure

        self.gateway.failure = TransportFailure(FailureKind.NOT_SENT)
        self.assertEqual(self.process(max_attempts=1), "failed")
        self.assertEqual(self.process(now=200, max_attempts=1), "failed")
        self.assertEqual(self.gateway.rows, {})

    def test_auth_tls_conflict_are_terminal_and_value_free(self):
        from publisher.delivery import FailureKind, TransportFailure

        for kind in (FailureKind.AUTH, FailureKind.TLS, FailureKind.CONFLICT):
            with self.subTest(kind=kind):
                other = (*KEY[:1], kind.value.ljust(32, "a"))
                self.box.stage(
                    Snapshot(*other, b"candidate", f"source/{kind.value}", b"report")
                )
                self.gateway.failure = TransportFailure(kind)
                from publisher.delivery import process_one

                self.assertEqual(
                    process_one(self.box, other, self.adapter, self.gateway, now=100),
                    "failed",
                )
                self.assertEqual(
                    process_one(self.box, other, self.adapter, self.gateway, now=200),
                    "failed",
                )
                self.assertEqual(self.box.get(other)["status"], "failed")
        self.assertEqual(self.gateway.rows, {})

    def test_remote_same_key_different_body_is_failed(self):
        self.gateway.rows[KEY] = "f" * 64
        self.assertEqual(self.process(), "failed")
        self.assertEqual(self.gateway.rows[KEY], "f" * 64)

    def test_receipts_require_exact_identity_digests_and_persistence(self):
        from publisher.delivery import Receipt

        body_sha = hashlib.sha256(BODY).hexdigest()
        source_sha = hashlib.sha256(SOURCE).hexdigest()
        bad = [
            Receipt(("wrong", KEY[1]), source_sha, body_sha, True),
            Receipt(KEY, "0" * 64, body_sha, True),
            Receipt(KEY, source_sha, "0" * 64, True),
            Receipt(KEY, source_sha, body_sha, False),
            Receipt(KEY, source_sha, body_sha, 1),
        ]
        for index, receipt in enumerate(bad):
            with self.subTest(index=index):
                if index:
                    self.box.close()
                    self.path = (
                        Path(self.tmp.name) / f"private{index}" / "outbox.sqlite"
                    )
                    self.box = Outbox(self.path)
                    self.box.stage(self.snapshot)
                self.adapter.bad_receipt = receipt
                self.assertEqual(self.process(), "uncertain")
                self.assertIsNone(self.box.get(KEY)["receipt"])

    def test_arbitrary_success_status_or_html_is_never_delivery(self):
        for index, response in enumerate(
            (200, 202, "<html>login</html>", {"status": "ok"})
        ):
            with self.subTest(response=response):
                if index:
                    self.box.close()
                    self.path = (
                        Path(self.tmp.name) / f"success{index}" / "outbox.sqlite"
                    )
                    self.box = Outbox(self.path)
                    self.box.stage(self.snapshot)
                self.gateway.response = response
                self.assertEqual(self.process(), "uncertain")

    def test_changed_request_revision_or_destination_never_sends(self):
        from publisher.delivery import FailureKind, TransportFailure

        self.gateway.failure = TransportFailure(FailureKind.NOT_SENT)
        self.assertEqual(self.process(), "pending")
        self.gateway.failure = None
        self.adapter.destination = "different_gateway"
        self.assertEqual(self.process(now=200), "failed")
        self.assertEqual(self.gateway.rows, {})
        self.assertEqual(self.box.get(KEY)["request_body"], BODY)

    def test_unexpected_transport_error_has_no_payload_in_logs_or_events(self):
        self.gateway.failure = RuntimeError("secret-token-marker private-source-marker")
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            self.assertEqual(self.process(), "uncertain")
        self.assertEqual(out.getvalue() + err.getvalue(), "")
        self.assertNotIn("secret-token-marker", repr(self.box.events(KEY)))
        self.assertNotIn("private-source-marker", repr(self.box.events(KEY)))

    def test_budget_and_clock_invalid_before_dispatch(self):
        for kwargs in (
            {"max_attempts": 0},
            {"base_delay": -1},
            {"now": float("nan")},
            {"max_delay": float("inf")},
            {"max_attempts": True},
        ):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                now = kwargs.get("now", 100)
                self.process(**dict(kwargs, now=now))
        self.assertEqual(self.gateway.rows, {})

    def test_stale_cas_cannot_overwrite_terminal_receipt(self):
        self.assertEqual(self.process(), "delivered")
        self.assertFalse(self.box.transition(KEY, "sending", "uncertain", code="stale"))
        self.assertEqual(self.box.get(KEY)["status"], "delivered")
        self.assertIs(self.box.get(KEY)["receipt"]["persisted"], True)

    def test_another_connection_lock_prevents_dispatch(self):
        from publisher.outbox import OutboxError

        other = Outbox(self.path)
        self.addCleanup(other.close)
        with other.delivery_lock():
            with self.assertRaisesRegex(OutboxError, "delivery_locked"):
                self.process()
        self.assertEqual(self.gateway.rows, {})


if __name__ == "__main__":
    unittest.main()
