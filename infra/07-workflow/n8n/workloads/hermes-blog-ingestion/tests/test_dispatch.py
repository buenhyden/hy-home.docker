"""Dispatch CLI against a synthetic loopback Gateway; no real n8n or server B."""

import contextlib
import functools
import hashlib
import io
import json
import os
import sys
import tempfile
import threading
import time
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import ClassVar
from unittest.mock import patch

WORKLOAD = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WORKLOAD))
from publisher import cli  # noqa: E402
from publisher.candidates import Snapshot  # noqa: E402
from publisher.delivery import process_one  # noqa: E402
from publisher.http_transport import HttpTransport  # noqa: E402
from publisher.outbox import Outbox  # noqa: E402

FIXTURES = Path(__file__).parent / "fixtures"
sys.path.insert(0, str(Path(__file__).parent))
import producer  # noqa: E402

KEY = ("6eabd835f969", "b" * 32)
TOKEN = "synthetic-token"
REPORT_ID = "12345678-1234-1234-1234-123456789abc"


def snapshot_and_evidence():
    source = b"# synthetic report\n"
    ref = "cron/output/6eabd835f969/2026-10-30_09-00-00.md"
    data = json.loads((FIXTURES / "companion-candidate-v1.json").read_bytes())
    data.update(source_ref=ref, source_sha256=hashlib.sha256(source).hexdigest())
    candidate = json.dumps(data).encode()
    evidence = json.loads((FIXTURES / "companion-evidence-v1.json").read_bytes())
    evidence["candidate_sha256"] = hashlib.sha256(candidate).hexdigest()
    return Snapshot(*KEY, candidate, ref, source), json.dumps(evidence).encode()


class Gateway(BaseHTTPRequestHandler):
    mode = "created"
    bodies: ClassVar[list] = []

    def log_message(self, *args):
        pass

    def do_POST(self):
        body = self.rfile.read(int(self.headers["Content-Length"]))
        self.bodies.append(body)
        if self.mode == "drop":
            self.close_connection = True
            return
        if self.headers.get("Authorization") != "Bearer " + TOKEN:
            status, reply = 401, {"error": "UNAUTHORIZED"}
        elif self.mode == "unauthorized":
            status, reply = 401, {"error": "UNAUTHORIZED"}
        elif self.mode == "forbidden":
            status, reply = 403, {"error": "FORBIDDEN"}
        elif self.mode == "conflict":
            status, reply = 409, {"error": "CONFLICT"}
        elif self.mode == "unavailable":
            status, reply = 503, {"error": "UNAVAILABLE"}
        else:
            status = 200 if self.mode == "duplicate" else 201
            reply = dict(
                id=REPORT_ID,
                persisted=True,
                duplicate=status == 200,
                status="received",
                candidate_count=len(json.loads(body)["items"]),
                status_url="/v1/ingestions/" + REPORT_ID,
            )
        raw = json.dumps(reply).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)


class DispatchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            cls.server = ThreadingHTTPServer(("127.0.0.1", 0), Gateway)
        except PermissionError:
            raise unittest.SkipTest("loopback socket creation denied") from None
        cls.server.daemon_threads = True
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def setUp(self):
        tmp = tempfile.TemporaryDirectory(prefix="hermes-dispatch-", dir="/tmp")
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.outbox = self.root / "private" / "outbox.sqlite"
        self.auth = self.root / "auth"
        self.auth.write_text("Authorization: Bearer " + TOKEN + "\n")
        self.auth.chmod(0o600)
        Gateway.mode = "created"
        Gateway.bodies = []
        self.snapshot, self.evidence = snapshot_and_evidence()

    def stage(self, evidence=None, signature=None):
        box = Outbox(self.outbox)
        try:
            if evidence is None:
                box.stage(self.snapshot)
            else:
                box.stage_with_unverified_evidence(self.snapshot, evidence, signature)
        finally:
            box.close()

    def record(self):
        box = Outbox(self.outbox)
        try:
            return box.get(KEY)
        finally:
            box.close()

    def dispatch(self, *extra, endpoint=None):
        out = io.StringIO()
        endpoint = endpoint or f"http://127.0.0.1:{self.server.server_port}/webhook/x"
        argv = [
            "dispatch",
            "--outbox",
            str(self.outbox),
            "--endpoint",
            endpoint,
            "--auth-header-file",
            str(self.auth),
            *extra,
        ]
        with contextlib.redirect_stdout(out):
            code = cli.main(argv)
        return code, json.loads(out.getvalue())

    def trust_key(self):
        """Admit a synthetic producer key through a temporary key store."""
        self.key = producer.new_key()
        store = self.root / "producer-keys.json"
        producer.write_store(store, producer.entry(self.key))
        for target, value in (
            ("publisher.trust.TRUST_STORE", store),
            ("publisher.trust._runtime_protected", lambda: None),
        ):
            patcher = patch(target, value)
            patcher.start()
            self.addCleanup(patcher.stop)

    def open_gate(self):
        """Signed evidence by an admitted key, the only production path."""
        self.trust_key()
        for target, value in (
            (
                "publisher.cli.HttpTransport",
                functools.partial(HttpTransport, allow_loopback_http=True),
            ),
        ):
            patcher = patch(target, value)
            patcher.start()
            self.addCleanup(patcher.stop)
        self.stage(self.evidence, producer.sign(self.key, self.evidence))

    def test_verified_shape_is_still_blocked_without_touching_credentials(self):
        self.stage(self.evidence)
        os.unlink(self.auth)
        self.assertEqual(self.dispatch(), (0, {"blocked": 1}))
        self.assertEqual(Gateway.bodies, [])
        self.assertEqual(self.record()["status"], "awaiting_contract")

    def test_evidence_never_opens_dispatch_or_reads_credentials(self):
        tampered = json.loads(self.evidence)
        tampered["items"][0]["http_status"] = 404
        cases = (
            ("valid", self.evidence),
            ("invalid", json.dumps(tampered).encode()),
            ("missing", None),
        )
        for name, evidence in cases:
            with self.subTest(evidence=name):
                self.setUp()
                gate = patch("publisher.policy.evidence_required", lambda job: False)
                gate.start()
                self.addCleanup(gate.stop)
                self.stage(evidence)
                os.unlink(self.auth)
                self.assertEqual(self.dispatch(), (0, {"blocked": 1}))
                self.assertEqual(Gateway.bodies, [])
                self.assertEqual(self.record()["status"], "awaiting_contract")
                gate.stop()

    def test_created_receipt_is_durable_and_not_resent(self):
        self.open_gate()
        self.assertEqual(self.dispatch(), (0, {"delivered": 1}))
        record = self.record()
        self.assertEqual(record["receipt"]["gateway_report_id"], REPORT_ID)
        self.assertEqual(record["request_body"], Gateway.bodies[0])
        key = hashlib.sha256((KEY[0] + ":" + KEY[1]).encode()).hexdigest()
        self.assertEqual(json.loads(Gateway.bodies[0])["idempotency_key"], key)
        self.assertEqual(self.dispatch(), (0, {}))
        self.assertEqual(len(Gateway.bodies), 1)

    def test_permanent_rejection_after_lost_response_is_not_replayed(self):
        for mode in ("conflict", "forbidden", "unauthorized"):
            with self.subTest(mode=mode):
                self.setUp()
                Gateway.mode = "drop"
                self.open_gate()
                now = [time.time()]
                clock = patch(
                    "publisher.cli.process_one",
                    lambda *a, now=now, **k: process_one(*a, now=now[0], **k),
                )
                clock.start()
                self.addCleanup(clock.stop)
                self.assertEqual(self.dispatch(), (1, {"uncertain": 1}))
                Gateway.mode = mode
                for _ in range(3):
                    now[0] += 7200
                    self.assertEqual(
                        self.dispatch("--allow-replay"), (1, {"uncertain": 1})
                    )
                self.assertEqual(len(Gateway.bodies), 2)
                clock.stop()

    def test_permanent_errors_are_never_retried(self):
        for mode, token in (
            ("created", "wrong"),
            ("forbidden", TOKEN),
            ("conflict", TOKEN),
        ):
            with self.subTest(mode=mode):
                self.setUp()
                self.auth.write_text("Authorization: Bearer " + token)
                Gateway.mode = mode
                self.open_gate()
                self.assertEqual(self.dispatch(), (1, {"failed": 1}))
                self.assertEqual(self.dispatch(), (0, {}))
                self.assertEqual(len(Gateway.bodies), 1)

    def test_outage_and_lost_response_reconcile_only_with_replay(self):
        for mode in ("unavailable", "drop"):
            with self.subTest(mode=mode):
                self.setUp()
                Gateway.mode = mode
                self.open_gate()
                self.assertEqual(self.dispatch(), (1, {"uncertain": 1}))
                now = [time.time() + 3600]
                clock = patch(
                    "publisher.cli.process_one",
                    lambda *a, now=now, **k: process_one(*a, now=now[0], **k),
                )
                clock.start()
                self.addCleanup(clock.stop)
                self.assertEqual(self.dispatch(), (1, {"uncertain": 1}))
                self.assertEqual(len(Gateway.bodies), 1)
                self.assertEqual(self.dispatch("--allow-replay"), (0, {"deferred": 1}))
                now[0] += 3600
                Gateway.mode = "duplicate"
                self.assertEqual(self.dispatch("--allow-replay"), (0, {"delivered": 1}))
                clock.stop()
                self.assertEqual(Gateway.bodies[0], Gateway.bodies[1])

    def test_replay_boundary_consumes_the_trust_decision(self):
        from publisher import trust
        from publisher.delivery import DispatchRequest, TransportFailure
        from publisher.gateway_transport import GatewayReplayTransport

        Gateway.mode = "drop"
        self.open_gate()
        self.assertEqual(self.dispatch(), (1, {"uncertain": 1}))
        endpoint = f"http://127.0.0.1:{self.server.server_port}/webhook/x"
        box = Outbox(self.outbox)
        self.addCleanup(box.close)
        row = box.get(KEY)
        http = HttpTransport(
            endpoint=endpoint,
            destination="n8n_hermes_ingestion",
            auth=("Authorization", "Bearer " + TOKEN),
            allow_loopback_http=True,
            content_type="application/json",
        )
        replay = GatewayReplayTransport(box, http, allow_idempotent_replay=True)
        request = DispatchRequest(
            KEY,
            row["source_sha256"],
            row["body_sha256"],
            row["contract_revision"],
            row["destination"],
            row["request_body"],
            row["endpoint_sha256"],
            trust.authorize(box, KEY).evidence_sha256,
        )
        Gateway.mode = "duplicate"
        self.assertEqual(replay.reconcile(request).status, 200)
        self.assertEqual(len(Gateway.bodies), 2)
        producer.write_store(
            self.root / "producer-keys.json",
            producer.entry(self.key, revoked_at="2026-10-31T00:00:00Z"),
        )
        with self.assertRaises(TransportFailure):
            replay.reconcile(request)
        self.assertEqual(len(Gateway.bodies), 2)
        # The CLI keeps the trust-blocked in-flight record visible.
        self.assertEqual(self.dispatch("--allow-replay"), (1, {"uncertain": 1}))
        self.assertEqual(len(Gateway.bodies), 2)

    def test_timeouts_nest_from_gateway_to_proxy(self):
        workflow = json.loads((WORKLOAD / "workflow.json").read_text())
        gateway = next(
            n["parameters"]["options"]["timeout"]
            for n in workflow["nodes"]
            if n["type"] == "n8n-nodes-base.httpRequest"
        )
        execution = workflow["settings"]["executionTimeout"] * 1000
        self.assertLess(gateway, execution)
        self.assertLess(execution, cli.HTTP_TIMEOUT * 1000)
        self.assertLess(cli.HTTP_TIMEOUT, 60)
        # Retry belongs to the Publisher; the workflow must not add its own.
        self.assertFalse(any(n.get("retryOnFail") for n in workflow["nodes"]))

    def test_credential_file_must_be_private(self):
        self.open_gate()
        # The link target stays private, so only O_NOFOLLOW can reject it.
        linked = self.root / "linked"
        linked.symlink_to(self.auth)
        self.assert_rejected(linked)
        self.auth.chmod(0o644)
        self.assert_rejected(self.auth)

    def test_credential_directory_must_not_be_shared(self):
        self.open_gate()
        self.root.chmod(0o777)
        self.addCleanup(self.root.chmod, 0o700)
        self.assert_rejected(self.auth)

    def assert_rejected(self, auth):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = cli.main(
                [
                    "dispatch",
                    "--outbox",
                    str(self.outbox),
                    "--endpoint",
                    "http://127.0.0.1:1/x",
                    "--auth-header-file",
                    str(auth),
                ]
            )
        self.assertEqual(code, 1)
        self.assertEqual(out.getvalue().strip(), '{"error":"operation_rejected"}')


if __name__ == "__main__":
    unittest.main()
