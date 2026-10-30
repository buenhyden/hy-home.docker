"""Durable synthetic SQLite staging and recovery evidence."""

import concurrent.futures
import dataclasses
import os
import tempfile
import threading
import unittest
from pathlib import Path
from unittest.mock import patch

from test_staging import JOB, RUN, fixture, synthetic_validator


class OutboxTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="hermes-outbox-", dir="/tmp")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.validator, self.validator_sha = synthetic_validator(self.root)
        patcher = patch("publisher.candidates.REVIEWED_SHA256", self.validator_sha)
        patcher.start()
        self.addCleanup(patcher.stop)
        fixture(self.root)

    def snapshot(self):
        from publisher.candidates import load_candidate, load_validator

        return load_candidate(
            self.root / "exports",
            JOB,
            f"{RUN}.json",
            self.root / "source",
            self.root / "items",
            load_validator(self.validator, self.validator_sha),
        )

    def box(self):
        from publisher.outbox import Outbox

        box = Outbox(self.root / "private" / "outbox.sqlite")
        self.addCleanup(box.close)
        return box

    def test_restart_exact_deduplication_and_permissions(self):
        box = self.box()
        snap = self.snapshot()
        self.assertEqual(box.stage(snap), "staged")
        box.close()
        box = self.box()
        self.assertEqual(box.stage(snap), "duplicate")
        row = box.get((JOB, RUN))
        self.assertEqual(row["candidate"], snap.candidate)
        self.assertEqual(row["source"], snap.source)
        self.assertEqual(row["status"], "awaiting_contract")
        self.assertEqual(box.counts(), {"awaiting_contract": 1})
        self.assertEqual(os.stat(self.root / "private").st_mode & 0o777, 0o700)
        self.assertEqual(
            os.stat(self.root / "private/outbox.sqlite").st_mode & 0o777, 0o600
        )

    def test_conflict_keeps_original_and_conflict_history(self):
        box, snap = self.box(), self.snapshot()
        box.stage(snap)
        changed = dataclasses.replace(snap, candidate=snap.candidate + b"\n")
        self.assertEqual(box.stage(changed), "conflict")
        self.assertEqual(box.get((JOB, RUN))["candidate"], snap.candidate)
        self.assertEqual(box.events((JOB, RUN))[-1]["code"], "identity_conflict")

    def test_same_source_with_different_run_quarantines_provenance_conflict(self):
        box, snap = self.box(), self.snapshot()
        box.stage(snap)
        other = dataclasses.replace(snap, run_id="b" * 32)
        self.assertEqual(box.stage(other), "conflict")
        self.assertEqual(box.keys(), [(JOB, RUN)])
        self.assertEqual(
            box.events((JOB, "b" * 32))[-1]["code"], "source_identity_conflict"
        )
        next_day = dataclasses.replace(
            other, source_ref=snap.source_ref.replace("30_", "31_")
        )
        self.assertEqual(box.stage(next_day), "staged")

    def test_conflicts_survive_restart_without_duplicate_events_or_record_changes(self):
        box, snap = self.box(), self.snapshot()
        key = (JOB, RUN)
        box.stage(snap)
        box.bind_request(key, "synthetic-v1", b"original")
        box.transition(key, "awaiting_contract", "failed", code="synthetic_failure")
        original = box.get(key)
        changed = dataclasses.replace(snap, candidate=snap.candidate + b"changed")
        other = dataclasses.replace(snap, run_id="b" * 32)
        for _ in range(3):
            self.assertEqual(box.stage(changed), "conflict")
            self.assertEqual(box.stage(other), "conflict")
        self.assertEqual(box.counts(), {"failed": 1, "conflict": 2})
        self.assertEqual(len(box.events(key)), 4)
        self.assertEqual(len(box.events((JOB, other.run_id))), 1)
        box.close()
        box = self.box()
        self.assertEqual(box.counts(), {"failed": 1, "conflict": 2})
        self.assertEqual(box.stage(changed), "conflict")
        self.assertEqual(box.stage(other), "conflict")
        self.assertEqual(len(box.events(key)), 4)
        self.assertEqual(len(box.events((JOB, other.run_id))), 1)
        self.assertEqual(box.get(key), original)
        another = dataclasses.replace(snap, candidate=snap.candidate + b"other")
        self.assertEqual(box.stage(another), "conflict")
        self.assertEqual(box.counts()["conflict"], 3)

    def test_existing_database_migrates_conflict_events(self):
        box, snap = self.box(), self.snapshot()
        box.stage(snap)
        changed = dataclasses.replace(snap, candidate=snap.candidate + b"changed")
        box.stage(changed)
        box._db.execute("DROP TABLE conflicts")
        box._db.execute(
            "INSERT INTO events(job_id,run_id,status,code,digest,created) "
            "SELECT job_id,run_id,status,code,digest,created FROM events "
            "WHERE status='conflict'"
        )
        box._db.commit()
        box.close()
        box = self.box()
        self.assertEqual(box.counts(), {"awaiting_contract": 1, "conflict": 1})
        self.assertEqual(box.stage(changed), "conflict")
        self.assertEqual(len(box.events((JOB, RUN))), 3)

    def test_simultaneous_scans_record_one_conflict(self):
        from publisher.outbox import Outbox

        box, snap = self.box(), self.snapshot()
        box.stage(snap)
        box.close()
        changed = dataclasses.replace(snap, candidate=snap.candidate + b"changed")
        barrier = threading.Barrier(2)
        path = self.root / "private" / "outbox.sqlite"

        def scan():
            local = Outbox(path)
            try:
                barrier.wait(timeout=5)
                return local.stage(changed)
            finally:
                local.close()

        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            futures = [executor.submit(scan) for _ in range(2)]
            self.assertEqual(
                [future.result(timeout=10) for future in futures],
                ["conflict", "conflict"],
            )
        box = self.box()
        self.assertEqual(box.counts(), {"awaiting_contract": 1, "conflict": 1})
        self.assertEqual(len(box.events((JOB, RUN))), 2)

    def test_compare_and_set_and_terminal_state_protection(self):
        from publisher.outbox import OutboxError

        box = self.box()
        box.stage(self.snapshot())
        key = (JOB, RUN)
        self.assertTrue(box.transition(key, "awaiting_contract", "pending"))
        self.assertFalse(box.transition(key, "awaiting_contract", "pending"))
        self.assertTrue(box.transition(key, "pending", "sending", attempts=1))
        self.assertTrue(box.transition(key, "sending", "failed", code="auth_rejected"))
        with self.assertRaises(OutboxError):
            box.transition(key, "failed", "pending")
        self.assertEqual(box.keys("failed"), [key])

    def test_request_binding_cannot_be_replaced_after_restart(self):
        from publisher.outbox import OutboxError

        box = self.box()
        box.stage(self.snapshot())
        key = (JOB, RUN)
        self.assertEqual(
            box.bind_request(key, "synthetic-v1", b'{"test":1}'), b'{"test":1}'
        )
        box.close()
        box = self.box()
        self.assertEqual(
            box.bind_request(key, "synthetic-v1", b'{"test":1}'), b'{"test":1}'
        )
        with self.assertRaisesRegex(OutboxError, "^request_conflict$"):
            box.bind_request(key, "synthetic-v1", b'{"test":2}')

    def test_sending_recovery_requires_delivery_lock(self):
        from publisher.outbox import OutboxError

        box = self.box()
        box.stage(self.snapshot())
        key = (JOB, RUN)
        box.transition(key, "awaiting_contract", "pending")
        box.transition(key, "pending", "sending")
        box.close()
        box = self.box()
        with self.assertRaisesRegex(OutboxError, "^delivery_lock_required$"):
            box.recover_sending()
        with box.delivery_lock():
            self.assertEqual(box.recover_sending(), 1)
        self.assertEqual(box.get(key)["status"], "uncertain")
        self.assertEqual(box.events(key)[-1]["code"], "crash_recovered")

    def test_symlink_db_directory_hardlink_and_public_dir_rejected(self):
        from publisher.outbox import Outbox, OutboxError

        private = self.root / "private"
        private.mkdir(mode=0o700)
        target = self.root / "target.sqlite"
        target.touch(mode=0o600)
        db = private / "outbox.sqlite"
        db.symlink_to(target)
        with self.assertRaises(OutboxError):
            Outbox(db)
        db.unlink()
        os.link(target, db)
        with self.assertRaises(OutboxError):
            Outbox(db)
        db.unlink()
        private.chmod(0o755)
        with self.assertRaises(OutboxError):
            Outbox(db)
        private.rmdir()
        private.symlink_to(self.root)
        with self.assertRaises(OutboxError):
            Outbox(db)

    def test_reject_repository_destination(self):
        from publisher.outbox import Outbox, OutboxError

        repo = self.root / "repo"
        repo.mkdir()
        (repo / ".git").mkdir()
        with self.assertRaisesRegex(OutboxError, "^repository_outbox$"):
            Outbox(repo / "private" / "outbox.sqlite")

    def test_request_destination_binding_and_record_identity_cannot_drift(self):
        from publisher.outbox import OutboxError

        box = self.box()
        box.stage(self.snapshot())
        key = (JOB, RUN)
        box.bind_request(
            key, "synthetic-v1", b'{"test":1}', destination="synthetic_gateway"
        )
        self.assertEqual(box.get(key)["destination"], "synthetic_gateway")
        with self.assertRaisesRegex(OutboxError, "^request_conflict$"):
            box.bind_request(
                key, "synthetic-v1", b'{"test":1}', destination="other_gateway"
            )

    def test_database_sidecar_symlink_rejected_without_touching_target(self):
        from publisher.outbox import Outbox, OutboxError

        private = self.root / "private"
        private.mkdir(mode=0o700)
        target = self.root / "target"
        target.write_bytes(b"preserved")
        (private / "outbox.sqlite-journal").symlink_to(target)
        with self.assertRaises(OutboxError):
            Outbox(private / "outbox.sqlite")
        self.assertEqual(target.read_bytes(), b"preserved")

    def test_delivery_lock_excludes_second_controller(self):
        from publisher.outbox import OutboxError

        first, second = self.box(), self.box()
        with first.delivery_lock():
            with self.assertRaisesRegex(OutboxError, "^delivery_locked$"):
                with second.delivery_lock():
                    self.fail("second controller acquired lock")

    def test_transition_rejects_unbounded_or_unsanitized_metadata(self):
        from publisher.outbox import OutboxError

        box = self.box()
        box.stage(self.snapshot())
        key = (JOB, RUN)
        for kwargs in (
            {"code": "secret=synthetic"},
            {"attempts": -1},
            {"next_attempt": float("nan")},
            {"next_attempt": -1},
        ):
            with self.subTest(kwargs=kwargs), self.assertRaises(OutboxError):
                box.transition(key, "awaiting_contract", "pending", **kwargs)
        self.assertEqual(box.get(key)["status"], "awaiting_contract")

    def test_delivered_requires_bound_matching_minimal_durable_receipt(self):
        from publisher.outbox import OutboxError

        box = self.box()
        box.stage(self.snapshot())
        key = (JOB, RUN)
        box.bind_request(key, "synthetic-v1", b"{}")
        box.transition(key, "awaiting_contract", "pending")
        box.transition(key, "pending", "sending")
        row = box.get(key)
        receipt = dict(
            job_id=JOB,
            run_id=RUN,
            source_sha256=row["source_sha256"],
            body_sha256=row["body_sha256"],
            persisted=True,
        )
        for bad in (
            None,
            dict(receipt, persisted=False),
            dict(receipt, body_sha256="0" * 64),
            dict(receipt, credential="synthetic-only"),
        ):
            with self.subTest(bad=bad), self.assertRaises(OutboxError):
                box.transition(key, "sending", "delivered", receipt=bad)
        self.assertTrue(box.transition(key, "sending", "delivered", receipt=receipt))
        self.assertEqual(box.get(key)["receipt"], receipt)


if __name__ == "__main__":
    unittest.main()
