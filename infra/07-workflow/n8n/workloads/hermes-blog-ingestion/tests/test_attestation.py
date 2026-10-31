"""Blog-data attestation: message parity, trust gate, key custody, outcomes."""

import base64
import hashlib
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from cryptography.hazmat.primitives import serialization

WORKLOAD = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WORKLOAD))
sys.path.insert(0, str(Path(__file__).parent))
import producer  # noqa: E402
from publisher import attestation, trust  # noqa: E402
from publisher.delivery import FailureKind, TransportFailure  # noqa: E402
from publisher.gateway_adapter import GatewayAdapter  # noqa: E402
from publisher.http_transport import HttpResponse  # noqa: E402
from publisher.outbox import Outbox  # noqa: E402
from test_trust import KEY, material  # noqa: E402

VECTOR = json.loads(
    (Path(__file__).parent / "fixtures/attestation-vector-v1.json").read_text()
)


def body_of(request):
    return json.dumps(request, ensure_ascii=False).encode()


class MessageTests(unittest.TestCase):
    def test_message_matches_blog_data_vector(self):
        message = attestation.message(body_of(VECTOR["request"]))
        self.assertEqual(base64.b64decode(VECTOR["message_b64"]), message)
        self.assertEqual(VECTOR["message_sha256"], hashlib.sha256(message).hexdigest())

    def test_key_order_and_idempotency_key_do_not_change_the_message(self):
        request = dict(reversed(list(VECTOR["request"].items())))
        request["idempotency_key"] = "another-key"
        self.assertEqual(
            base64.b64decode(VECTOR["message_b64"]),
            attestation.message(body_of(request)),
        )

    def test_any_item_change_changes_the_message(self):
        request = json.loads(json.dumps(VECTOR["request"]))
        request["items"][0]["url"] = "https://example.org/other"
        self.assertNotEqual(
            base64.b64decode(VECTOR["message_b64"]),
            attestation.message(body_of(request)),
        )

    def test_unparseable_body_is_refused(self):
        for raw in (b"\xff", b"[]", b'{"producer":"hermes"}'):
            with self.subTest(raw=raw), self.assertRaises(attestation.AttestationError):
                attestation.message(raw)


class TrustGateTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory(prefix="hermes-attest-", dir="/tmp")
        self.addCleanup(tmp.cleanup)
        self.store = Path(tmp.name) / "producer-keys.json"
        self.key = producer.new_key()
        producer.write_store(self.store, producer.entry(self.key))
        for target, value in (
            ("publisher.trust.TRUST_STORE", self.store),
            ("publisher.trust._runtime_protected", lambda: None),
        ):
            patcher = patch(target, value)
            patcher.start()
            self.addCleanup(patcher.stop)
        self.snapshot, self.evidence = material()

    def test_signed_evidence_yields_the_dispatch_request_bytes(self):
        signature = producer.sign(self.key, self.evidence)
        body, evidence_sha256 = attestation.verified_request(
            self.snapshot, self.evidence, signature
        )
        times = trust.companion.verify(
            self.snapshot.job_id,
            self.snapshot.run_id,
            self.snapshot.candidate,
            self.evidence,
        )
        generated = json.loads(self.snapshot.candidate)["generated_at"]
        # What dispatch sends: the adapter over the staged outbox row.
        box = Outbox(self.store.parent / "private" / "outbox.sqlite")
        self.addCleanup(box.close)
        box.stage(self.snapshot)
        expected = GatewayAdapter(
            times.scheduled_at, generated, times.collected_at
        ).prepare(box.get(KEY))
        self.assertEqual(expected.body, body)
        self.assertEqual(hashlib.sha256(self.evidence).hexdigest(), evidence_sha256)

    def test_unsigned_forged_revoked_or_foreign_evidence_is_refused(self):
        other = producer.new_key()
        _, foreign = material("c" * 32)
        cases = (
            ("signature_missing", self.evidence, None),
            ("signature_invalid", self.evidence, producer.sign(other, self.evidence)),
            ("identity", foreign, producer.sign(self.key, foreign)),
        )
        for code, evidence, signature in cases:
            with self.subTest(code=code), self.assertRaises(trust.TrustError) as caught:
                attestation.verified_request(self.snapshot, evidence, signature)
            self.assertEqual(code, str(caught.exception))
        producer.write_store(
            self.store, producer.entry(self.key, revoked_at="2026-10-01T00:00:00Z")
        )
        with self.assertRaises(trust.TrustError) as caught:
            attestation.verified_request(
                self.snapshot, self.evidence, producer.sign(self.key, self.evidence)
            )
        self.assertEqual("key_revoked", str(caught.exception))


class KeyCustodyTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory(prefix="hermes-attest-key-", dir="/tmp")
        self.addCleanup(tmp.cleanup)
        self.dir = Path(tmp.name)
        self.private = producer.new_key()
        self.path = self.dir / "attestation.pem"
        self.path.write_bytes(
            self.private.private_bytes(
                serialization.Encoding.PEM,
                serialization.PrivateFormat.PKCS8,
                serialization.NoEncryption(),
            )
        )

    def test_owner_or_group_read_only_key_signs_a_verifiable_body(self):
        message = attestation.message(body_of(VECTOR["request"]))
        for mode in (0o400, 0o440, 0o600):
            with self.subTest(mode=oct(mode)):
                self.path.chmod(mode)
                key = attestation.load_signing_key(self.path)
                body = json.loads(attestation.request_body("attest-1", key, message))
                self.assertEqual(
                    {
                        "schema_version": "1.0",
                        "key_id": "attest-1",
                        "algorithm": "ed25519",
                    },
                    {k: v for k, v in body.items() if k != "signature"},
                )
                self.assertRegex(body["signature"], r"^[A-Za-z0-9+/]{86}==$")
                self.private.public_key().verify(
                    base64.b64decode(body["signature"]), message
                )

    def test_exposed_linked_or_unreadable_keys_are_refused(self):
        for mode in (0o644, 0o604, 0o460, 0o660):
            with self.subTest(mode=oct(mode)):
                self.path.chmod(mode)
                with self.assertRaises(attestation.AttestationError):
                    attestation.load_signing_key(self.path)
        self.path.chmod(0o600)
        link = self.dir / "link.pem"
        link.symlink_to(self.path)
        hard = self.dir / "hard.pem"
        os.link(self.path, hard)
        for path in (link, hard, self.dir / "missing.pem"):
            with (
                self.subTest(path=path.name),
                self.assertRaises(attestation.AttestationError),
            ):
                attestation.load_signing_key(path)
        os.unlink(hard)
        self.path.write_text("not a key")
        self.path.chmod(0o600)
        with self.assertRaises(attestation.AttestationError):
            attestation.load_signing_key(self.path)

    def test_group_read_only_for_the_attester_group(self):
        foreign = [g for g in os.getgroups() if g != os.getegid()]
        if not foreign:
            self.skipTest("no supplementary group to test with")
        self.path.chmod(0o440)
        os.chown(self.path, -1, foreign[0])
        with self.assertRaises(attestation.AttestationError):
            attestation.load_signing_key(self.path)
        # Owner-only stays valid whatever the group.
        self.path.chmod(0o400)
        attestation.load_signing_key(self.path)

    def test_writable_or_linked_parent_directory_is_refused(self):
        self.path.chmod(0o600)
        self.dir.chmod(0o777)
        self.addCleanup(self.dir.chmod, 0o700)
        with self.assertRaises(attestation.AttestationError):
            attestation.load_signing_key(self.path)
        self.dir.chmod(0o700)
        alias = Path(tempfile.mkdtemp(prefix="hermes-attest-alias-", dir="/tmp"))
        self.addCleanup(alias.rmdir)
        (alias / "dir").symlink_to(self.dir)
        self.addCleanup((alias / "dir").unlink)
        with self.assertRaises(attestation.AttestationError):
            attestation.load_signing_key(alias / "dir" / "attestation.pem")


class OutcomeTests(unittest.TestCase):
    def test_gateway_answers_map_to_three_outcomes(self):
        cases = {
            201: "attested",
            200: "attested",
            400: "rejected",
            401: "rejected",
            403: "rejected",
            404: "rejected",
            422: "rejected",
            429: "retry",
            500: "retry",
            502: "retry",
            503: "retry",
            504: "retry",
        }
        for status, expected in cases.items():
            with self.subTest(status=status):
                self.assertEqual(
                    expected, attestation.outcome(HttpResponse(status, b"{}"))
                )

    def test_transport_failures_retry_except_credentials_and_tls(self):
        for kind in FailureKind:
            with self.subTest(kind=kind):
                # A certificate failure needs an operator, not the timer.
                stop = (FailureKind.AUTH, FailureKind.TLS)
                expected = "rejected" if kind in stop else "retry"
                self.assertEqual(expected, attestation.outcome(TransportFailure(kind)))


class AttestCliTests(unittest.TestCase):
    """The attest command: producer trust first, then key, then one POST."""

    REPORT = "0f0e0d0c-0b0a-4908-8706-050403020100"

    def setUp(self):
        import test_staging as staging

        tmp = tempfile.TemporaryDirectory(prefix="hermes-attest-cli-", dir="/tmp")
        self.addCleanup(tmp.cleanup)
        self.root = root = Path(tmp.name)
        self.validator, sha = staging.synthetic_validator(root)
        self.producer = producer.new_key()
        store = root / "producer-keys.json"
        producer.write_store(store, producer.entry(self.producer))
        for target, value in (
            ("publisher.candidates.REVIEWED_SHA256", sha),
            ("publisher.trust.TRUST_STORE", store),
            ("publisher.trust._runtime_protected", lambda: None),
        ):
            patcher = patch(target, value)
            patcher.start()
            self.addCleanup(patcher.stop)
        snapshot, self.evidence = material()
        self.job, self.run = snapshot.job_id, snapshot.run_id
        (root / "source" / snapshot.source_ref).parent.mkdir(parents=True)
        (root / "source" / snapshot.source_ref).write_bytes(snapshot.source)
        (root / "exports" / self.job).mkdir(parents=True)
        (root / "exports" / self.job / f"{self.run}.json").write_bytes(
            snapshot.candidate
        )
        (root / "items").mkdir()
        self.evidence_root = root / "evidence"
        self.evidence_root.mkdir()
        self.name = (
            hashlib.sha256(f"{self.job}\0{self.run}".encode()).hexdigest() + ".json"
        )
        (self.evidence_root / self.name).write_bytes(self.evidence)
        self.signer = producer.new_key()
        self.key = root / "attestation.pem"
        self.key.write_bytes(
            self.signer.private_bytes(
                serialization.Encoding.PEM,
                serialization.PrivateFormat.PKCS8,
                serialization.NoEncryption(),
            )
        )
        self.key.chmod(0o600)
        self.auth = root / "attest.header"
        self.auth.write_text("Authorization: Bearer synthetic-attest-token\n")
        self.auth.chmod(0o600)
        self.args = [
            "attest",
            "--exports", str(root / "exports"),
            "--source-root", str(root / "source"),
            "--item-root", str(root / "items"),
            "--validator", str(self.validator),
            "--validator-sha256", sha,
            "--evidence-root", str(self.evidence_root),
            "--job", self.job,
            "--run", self.run,
            "--report-id", self.REPORT,
            "--gateway", "https://blog-export.example.test",
            "--auth-header-file", str(self.auth),
            "--signing-key", str(self.key),
            "--key-id", "attest-1",
        ]  # fmt: skip

    def sign_evidence(self):
        (self.evidence_root / (self.name + ".sig")).write_bytes(
            producer.sign(self.producer, self.evidence)
        )

    def invoke(self, status=201):
        import contextlib
        import io

        from publisher import cli

        sent = []

        def send(transport, request):
            sent.append((transport, request))
            return HttpResponse(status, b"{}")

        out = io.StringIO()
        with (
            patch("publisher.http_transport.HttpTransport.send", send),
            contextlib.redirect_stdout(out),
        ):
            code = cli.main(self.args)
        text = out.getvalue()
        for secret in ("synthetic-attest-token", str(self.root), "PRIVATE KEY"):
            self.assertNotIn(secret, text)
        return code, json.loads(text), sent

    def test_signed_evidence_posts_one_verifiable_attestation(self):
        self.sign_evidence()
        code, result, sent = self.invoke()
        self.assertEqual((0, {"result": "attested", "status": 201}), (code, result))
        ((transport, request),) = sent
        self.assertEqual(
            ("https", "blog-export.example.test", None,
             f"/v1/ingestions/{self.REPORT}/attestations"),
            transport._endpoint,
        )  # fmt: skip
        self.assertEqual(transport._auth_header[1], "Bearer synthetic-attest-token")
        self.assertEqual(request.endpoint_sha256, transport.endpoint_sha256)
        body, _ = attestation.verified_request(
            *material(), producer.sign(self.producer, self.evidence)
        )
        signature = json.loads(request.body)["signature"]
        self.signer.public_key().verify(
            base64.b64decode(signature), attestation.message(body)
        )

    def test_resent_attestation_is_success_and_refusals_stop(self):
        self.sign_evidence()
        self.assertEqual(0, self.invoke(200)[0])
        code, result, _ = self.invoke(422)
        self.assertEqual((1, {"result": "rejected", "status": 422}), (code, result))
        code, result, _ = self.invoke(503)
        self.assertEqual((1, {"result": "retry", "status": 503}), (code, result))

    def test_unsigned_evidence_is_blocked_before_key_or_network(self):
        self.key.chmod(0o644)  # would be refused if it were read
        code, result, sent = self.invoke()
        self.assertEqual(
            (1, {"result": "blocked", "reason": "signature_missing"}), (code, result)
        )
        self.assertEqual([], sent)

    def test_bad_report_id_or_key_is_rejected_without_network(self):
        self.sign_evidence()
        self.args[self.args.index("--report-id") + 1] = "../v1/summary"
        self.assertEqual((1, {"error": "operation_rejected"}, []), self.invoke())
        self.args[self.args.index("--report-id") + 1] = self.REPORT
        self.key.chmod(0o644)
        self.assertEqual((1, {"error": "operation_rejected"}, []), self.invoke())


if __name__ == "__main__":
    unittest.main()
