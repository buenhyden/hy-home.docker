"""Blog-data attestation/2: vector parity, body shape, key custody, outcomes."""

import base64
import hashlib
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

from cryptography.hazmat.primitives import serialization

WORKLOAD = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WORKLOAD))
sys.path.insert(0, str(Path(__file__).parent))
import producer  # noqa: E402
from publisher import attestation  # noqa: E402
from publisher.delivery import FailureKind, TransportFailure  # noqa: E402
from publisher.http_transport import HttpResponse  # noqa: E402

V = json.loads(
    (Path(__file__).parent / "fixtures/attestation-v2.vectors.json").read_text()
)
EVIDENCE = V["evidence_sha256"]
REQUEST = attestation._canonical(
    {k: v for k, v in V["request"].items() if k != "idempotency_key"}
)
PUBLIC = serialization.load_pem_public_key(V["public_key_pem"].encode())
ITEMS = V["cases"][0]["body"]["verified_items"]


class MessageTests(unittest.TestCase):
    def test_request_fixture_matches_content_sha256(self):
        self.assertEqual(V["content_sha256"], hashlib.sha256(REQUEST).hexdigest())

    def test_vectors_match_blog_data(self):
        checked = 0
        for case in V["cases"]:
            if "signed_json" not in case:
                continue  # forged/tampered: only the Gateway can judge the signature
            with self.subTest(case=case["name"]):
                items = case["body"]["verified_items"]
                signed = attestation.message(REQUEST, items, EVIDENCE)
                self.assertEqual(
                    case["signed_json"].encode(), signed[len(attestation.PREFIX) :]
                )
                self.assertEqual(
                    case["message_sha256"], hashlib.sha256(signed).hexdigest()
                )
                PUBLIC.verify(base64.b64decode(case["signature_base64"]), signed)
                checked += 1
        self.assertEqual(5, checked)

    def test_idempotency_key_stays_out_and_a_foreign_fingerprint_is_refused(self):
        with_key = attestation._canonical(V["request"])
        with self.assertRaises(attestation.AttestationError) as caught:
            attestation.message(with_key, ITEMS, EVIDENCE)
        self.assertEqual("fingerprint", str(caught.exception))
        for raw in (b"\xff", b"[]", b'{"producer":"hermes"}'):
            with self.subTest(raw=raw), self.assertRaises(attestation.AttestationError):
                attestation.message(raw, ITEMS, EVIDENCE)

    def test_unsorted_or_duplicate_items_rejected_locally(self):
        a, b = ITEMS
        for items in ([b, a], [a, a]):
            with (
                self.subTest(items=items),
                self.assertRaises(attestation.AttestationError),
            ):
                attestation.message(REQUEST, items, EVIDENCE)

    def test_malformed_items_or_evidence_rejected_locally(self):
        a = ITEMS[0]
        bad = (
            [{**a, "fetched_at": "2026-10-30 09:15:00"}],
            [{**a, "final_url": "http://example.org/"}],
            [{**a, "final_url": "https://user@example.org/"}],
            [{**a, "final_url": "https://example.org/a b"}],
            [{**a, "extra": 1}],
            [{"item_id": "x", "fetched_at": a["fetched_at"]}],
            [dict(a, item_id=f"i{n:03}") for n in range(101)],
        )
        for items in bad:
            with (
                self.subTest(items=items[:1]),
                self.assertRaises(attestation.AttestationError),
            ):
                attestation.message(REQUEST, items, EVIDENCE)
        for evidence in ("A" * 64, "a" * 63, None):
            with (
                self.subTest(evidence=evidence),
                self.assertRaises(attestation.AttestationError),
            ):
                attestation.message(REQUEST, ITEMS, evidence)

    def test_lone_surrogates_raise_attestation_error(self):
        raw = json.dumps(
            {
                **{k: v for k, v in V["request"].items() if k != "idempotency_key"},
                "source_text": "\\ud800",
            }
        ).encode()
        raw = raw.replace(b"\\\\ud800", b"\\ud800")
        self.assertIn(b"\\ud800", raw)
        with self.assertRaises(attestation.AttestationError):
            attestation.message(raw, ITEMS, EVIDENCE)
        items = [{**ITEMS[0], "item_id": "item-\ud800"}]
        with self.assertRaises(attestation.AttestationError):
            attestation.message(REQUEST, items, EVIDENCE)
        with self.assertRaises(attestation.AttestationError):
            attestation.request_body("k", producer.new_key(), b"", items, EVIDENCE)

    def test_empty_list_and_fire_id_null(self):
        signed = attestation.message(REQUEST, [], EVIDENCE)
        self.assertIn(b'"fire_id":null', signed)
        self.assertIn(b'"verified_items":[]', signed)


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
        message = attestation.message(REQUEST, ITEMS, EVIDENCE)
        for mode in (0o400, 0o440, 0o600):
            with self.subTest(mode=oct(mode)):
                self.path.chmod(mode)
                key = attestation.load_signing_key(self.path)
                body = json.loads(
                    attestation.request_body("attest-1", key, message, ITEMS, EVIDENCE)
                )
                self.assertEqual(
                    {
                        "schema_version",
                        "key_id",
                        "algorithm",
                        "signature",
                        "verified_items",
                        "evidence_sha256",
                    },
                    set(body),
                )
                self.assertEqual(
                    ("2.0", "attest-1", "ed25519", ITEMS, EVIDENCE),
                    (
                        body["schema_version"],
                        body["key_id"],
                        body["algorithm"],
                        body["verified_items"],
                        body["evidence_sha256"],
                    ),
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
            409: "rejected",
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


if __name__ == "__main__":
    unittest.main()
