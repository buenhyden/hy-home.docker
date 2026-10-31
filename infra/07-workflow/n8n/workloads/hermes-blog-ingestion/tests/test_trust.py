"""Producer authentication negatives and gate consistency on synthetic keys."""

import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

WORKLOAD = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WORKLOAD))
sys.path.insert(0, str(Path(__file__).parent))
import producer  # noqa: E402
from publisher import trust  # noqa: E402
from publisher.candidates import Snapshot  # noqa: E402
from publisher.delivery import (  # noqa: E402
    DispatchRequest,
    TransportFailure,
    process_one,
)
from publisher.gateway_adapter import DESTINATION, REVISION  # noqa: E402
from publisher.gateway_transport import GatewayReplayTransport  # noqa: E402
from publisher.outbox import Outbox, OutboxError  # noqa: E402

FIXTURES = Path(__file__).parent / "fixtures"
PROTECTED = trust._protected
RUNTIME = trust._runtime_protected
KEY = ("6eabd835f969", "b" * 32)


def material(run=KEY[1]):
    source = b"# synthetic report\n"
    data = json.loads((FIXTURES / "companion-candidate-v1.json").read_bytes())
    data.update(
        run_id=run,
        source_ref=f"cron/output/{KEY[0]}/{run[:8]}.md",
        source_sha256=hashlib.sha256(source).hexdigest(),
    )
    candidate = json.dumps(data).encode()
    evidence = json.loads((FIXTURES / "companion-evidence-v1.json").read_bytes())
    evidence.update(run_id=run, candidate_sha256=hashlib.sha256(candidate).hexdigest())
    return (
        Snapshot(KEY[0], run, candidate, data["source_ref"], source),
        json.dumps(evidence).encode(),
    )


class TrustTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory(prefix="hermes-trust-", dir="/tmp")
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.key = producer.new_key()
        self.store = self.root / "producer-keys.json"
        self.admit(producer.entry(self.key))
        for target, value in (
            ("publisher.trust.TRUST_STORE", self.store),
            # Temporary stores are owned by the test account; protection has its
            # own tests below.
            ("publisher.trust._runtime_protected", lambda: None),
        ):
            patcher = patch(target, value)
            patcher.start()
            self.addCleanup(patcher.stop)
        self.box = Outbox(self.root / "private" / "outbox.sqlite")
        self.addCleanup(lambda: self.box.close())
        self.snapshot, self.evidence = material()

    def admit(self, *entries):
        producer.write_store(self.store, *entries)

    def stage(self, evidence=None, signature=None):
        evidence = self.evidence if evidence is None else evidence
        return self.box.stage_with_unverified_evidence(
            self.snapshot, evidence, signature
        )

    def assert_rejected(self, code):
        with self.assertRaises(trust.TrustError) as caught:
            trust.authorize(self.box, KEY)
        self.assertEqual(str(caught.exception), code)

    def test_signed_evidence_authorizes_and_survives_restart(self):
        self.stage(signature=producer.sign(self.key, self.evidence))
        first = trust.authorize(self.box, KEY)
        self.assertEqual(first.key_id, "synthetic-producer")
        self.assertEqual(first.times.collected_at, "2026-10-30T09:01:10.250+09:00")
        self.box.close()
        self.box = Outbox(self.root / "private" / "outbox.sqlite")
        self.assertEqual(trust.authorize(self.box, KEY), first)

    def test_unsigned_same_account_json_is_not_trusted(self):
        self.stage()
        self.assert_rejected("signature_missing")

    def test_empty_tracked_store_blocks_every_job(self):
        tracked = json.loads(
            (WORKLOAD / "publisher" / "producer-keys.json").read_text()
        )
        self.assertEqual(
            tracked, {"schema_version": "hermes-producer-keys/1", "keys": []}
        )
        self.admit()
        self.stage(signature=producer.sign(self.key, self.evidence))
        self.assert_rejected("untrusted_key")

    def test_forgery_and_tampering_are_rejected(self):
        other = producer.new_key()
        tampered = self.evidence.replace(b"synthetic/1", b"synthetic/9", 1)
        cases = (
            ("signature_invalid", self.evidence, producer.sign(other, self.evidence)),
            ("signature_invalid", tampered, producer.sign(self.key, self.evidence)),
            (
                "untrusted_key",
                self.evidence,
                producer.sign(other, self.evidence, "nobody"),
            ),
            ("signature_invalid", self.evidence, b'{"schema_version":"x"}'),
            ("invalid_json", self.evidence, b"\xff"),
        )
        for code, evidence, signature in cases:
            with self.subTest(code=code):
                self.setUp()
                self.stage(evidence, signature)
                self.assert_rejected(code)

    def test_signed_evidence_for_another_run_or_candidate_is_rejected(self):
        _, other_run = material("c" * 32)
        changed = json.loads(self.evidence)
        changed["candidate_sha256"] = "0" * 64
        changed = json.dumps(changed).encode()
        for code, evidence in (("identity", other_run), ("candidate_digest", changed)):
            with self.subTest(code=code):
                self.setUp()
                self.stage(evidence, producer.sign(self.key, evidence))
                self.assert_rejected(code)

    def test_key_lifecycle_and_scope(self):
        cases = (
            ("key_revoked", {"revoked_at": "2026-10-31T00:00:00Z"}),
            ("key_expired", {"not_after": "2026-02-01T00:00:00Z"}),
            ("key_expired", {"not_before": "2098-01-01T00:00:00Z"}),
            ("key_scope", {"jobs": ["25674fbc0bf3"]}),
        )
        for code, overrides in cases:
            with self.subTest(code=code):
                self.setUp()
                self.admit(producer.entry(self.key, **overrides))
                self.stage(signature=producer.sign(self.key, self.evidence))
                self.assert_rejected(code)

    def test_store_writable_by_this_account_is_not_a_trust_anchor(self):
        with self.assertRaises(trust.TrustError) as caught:
            PROTECTED(self.store)
        self.assertEqual(str(caught.exception), "store_unprotected")

    def test_every_signature_check_requires_the_protected_runtime(self):
        self.stage(signature=producer.sign(self.key, self.evidence))
        with patch("publisher.trust._runtime_protected", RUNTIME):
            # This suite is neither isolated nor run from a protected install.
            with self.assertRaises(trust.TrustError) as caught:
                trust.authorize(self.box, KEY)
        self.assertIn(
            str(caught.exception), ("interpreter_unisolated", "store_unprotected")
        )

    def test_only_root_owned_unshared_paths_are_protected(self):
        import stat
        from types import SimpleNamespace

        def check(uid, owner, mode):
            info = SimpleNamespace(st_uid=owner, st_mode=stat.S_IFREG | mode)
            with (
                patch("os.getuid", return_value=uid),
                patch("os.lstat", return_value=info),
                patch("os.access", return_value=False),
            ):
                PROTECTED(Path("/opt/x/publisher/trust.py"))

        check(1000, 0, 0o755)
        # Another non-root account (the Hermes producer) could rewrite it.
        for uid, owner, mode in (
            (1000, 1001, 0o755),
            (1000, 0, 0o775),
            (1000, 0, 0o757),
            (0, 0, 0o755),
        ):
            with self.subTest(uid=uid, owner=owner, mode=oct(mode)):
                with self.assertRaises(trust.TrustError) as caught:
                    check(uid, owner, mode)
                self.assertEqual(str(caught.exception), "store_unprotected")

    def test_runtime_check_covers_interpreter_path_and_every_loaded_module(self):
        import sys

        from cryptography.hazmat.primitives.asymmetric import ed25519

        paths = set(trust._runtime_paths())
        self.assertIn(Path(sys.executable).resolve(), paths)
        self.assertIn(Path(ed25519.__file__).resolve(), paths)
        self.assertIn(Path(trust.__file__).resolve(), paths)
        self.assertIn(trust.TRUST_STORE, paths)
        for entry in sys.path:
            if entry and Path(entry).exists():
                self.assertIn(Path(entry).resolve(), paths)

    def test_verify_install_reports_store_and_runtime_without_values(self):
        import contextlib
        import io

        from publisher import cli

        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(cli.main(["verify-install"]), 0)
        self.assertEqual(
            json.loads(out.getvalue()), {"keys": 1, "runtime": "protected"}
        )
        out = io.StringIO()
        with (
            patch("publisher.trust._runtime_protected", RUNTIME),
            contextlib.redirect_stdout(out),
        ):
            self.assertEqual(cli.main(["verify-install"]), 1)
        self.assertIn(
            json.loads(out.getvalue())["error"],
            ("interpreter_unisolated", "store_unprotected"),
        )

    def test_malformed_or_ambiguous_store_fails_closed(self):
        good = producer.entry(self.key)
        for code, entries in (
            ("store_invalid", (good, good)),
            ("store_invalid", (good, dict(good, key_id="alias"))),
            ("store_invalid", (dict(good, revoked_at="soon"),)),
            ("store_invalid", (dict(good, not_after=good["not_before"]),)),
            ("store_invalid", (dict(good, algorithm="rsa"),)),
            ("invalid_base64", (dict(good, public_key="AAAA"),)),
        ):
            with self.subTest(code=code):
                self.setUp()
                self.admit(*entries)
                self.stage(signature=producer.sign(self.key, self.evidence))
                self.assert_rejected(code)
        self.store.unlink()
        self.assert_rejected("store_unavailable")

    def test_pre_signature_outbox_migrates_and_stays_blocked(self):
        import sqlite3

        self.stage()
        self.box.close()
        path = self.root / "private" / "outbox.sqlite"
        db = sqlite3.connect(path)
        db.execute("ALTER TABLE unverified_evidence DROP COLUMN signature")
        db.commit()
        db.close()
        self.box = Outbox(path)
        self.assertIsNone(self.box.get_evidence_signature(KEY))
        self.assert_rejected("signature_missing")

    def test_signature_is_immutable_once_staged(self):
        self.stage()
        with self.assertRaises(OutboxError):
            self.stage(signature=producer.sign(self.key, self.evidence))

    def test_revocation_after_binding_closes_every_gate(self):
        self.stage(signature=producer.sign(self.key, self.evidence))
        body = self.box.bind_request(KEY, REVISION, b"{}", destination=DESTINATION)
        self.admit(producer.entry(self.key, revoked_at="2026-10-31T00:00:00Z"))
        with self.assertRaisesRegex(OutboxError, "^evidence_unverified$"):
            self.box.bind_request(KEY, REVISION, body, destination=DESTINATION)
        self.assertEqual(process_one(self.box, KEY, object(), object()), "blocked")

        sent = []

        class Network:
            endpoint_sha256 = "e" * 64

            def send(self, request):
                sent.append(request)

        replay = GatewayReplayTransport(
            self.box, Network(), allow_idempotent_replay=True
        )
        request = DispatchRequest(
            KEY,
            self.box.get(KEY)["source_sha256"],
            hashlib.sha256(body).hexdigest(),
            REVISION,
            DESTINATION,
            body,
            "e" * 64,
            hashlib.sha256(self.evidence).hexdigest(),
        )
        with self.assertRaises(TransportFailure):
            replay.reconcile(request)
        self.assertEqual(sent, [])


if __name__ == "__main__":
    unittest.main()
