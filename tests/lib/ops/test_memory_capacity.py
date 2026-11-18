"""Memory capacity ledger, using only private temporary fixture stores."""

from __future__ import annotations

import hashlib
import sqlite3
import tempfile
import threading
import unittest
from pathlib import Path

from scripts.lib.ops import memory_capacity as capacity


def fingerprint(value="fixture"):
    return hashlib.sha256(value.encode()).hexdigest()


class CapacityTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name)
        self.path = self.base / ".workspace-memory" / "memory.sqlite3"
        self.manager = capacity.MemoryCapacity(self.path)

    def initialize(self):
        return self.manager.reconcile()

    def test_status_of_missing_ledger_is_read_only_and_growth_is_refused(self):
        self.assertEqual("unverified", self.manager.status()["inventory_state"])
        self.assertFalse(self.path.parent.exists())
        with self.assertRaises(capacity.CapacityError):
            self.manager.reserve("one", fingerprint(), 1)
        self.assertFalse(self.path.parent.exists())

    def test_reconcile_adopts_a_private_ledger_with_the_fixed_base(self):
        status = self.initialize()
        self.assertEqual("complete", status["inventory_state"])
        self.assertEqual(1_073_741_824, status["cap_bytes"])
        self.assertEqual(capacity.BASE_BYTES, status["charged_bytes"])
        self.assertEqual(0o600, self.manager.path.stat().st_mode & 0o777)
        self.assertEqual(0o700, self.path.parent.stat().st_mode & 0o777)
        self.assertFalse(self.path.exists())

    def test_reconcile_drops_allocations_left_by_retired_backups(self):
        self.initialize()
        connection = sqlite3.connect(self.manager.path)
        connection.execute(
            "INSERT INTO allocations VALUES ('external:state:a:b','external','state',?,'metadata')",
            (capacity.COPY_BYTES,),
        )
        connection.commit()
        connection.close()
        # Legacy rows are no longer charged, so writes are not blocked.
        self.assertEqual(1, self.manager.status()["legacy_allocations"])
        self.assertEqual(capacity.BASE_BYTES, self.manager.status()["charged_bytes"])
        generation = self.manager.status()["generation"]
        status = self.manager.reconcile(expected_generation=generation)
        self.assertEqual(0, status["legacy_allocations"])
        with self.assertRaises(capacity.CapacityError):
            self.manager.reconcile(expected_generation=generation)

    def test_reservation_replay_is_not_another_admission_and_conflicts_stop(self):
        self.initialize()
        first = self.manager.reserve("one", fingerprint(), 32)
        self.assertFalse(first["replay"])
        second = self.manager.reserve("one", fingerprint(), 32)
        self.assertTrue(second["replay"])
        self.assertEqual(32, self.manager.status()["reserved_bytes"])
        with self.assertRaises(capacity.CapacityError):
            self.manager.reserve("one", fingerprint("different"), 32)
        self.manager.settle("one", result={"revision": 1})
        replay = self.manager.reserve("one", fingerprint(), 32)
        self.assertEqual("completed", replay["state"])
        self.assertEqual({"revision": 1}, replay["result"])
        self.assertEqual(
            "completed", self.manager.operation("one", fingerprint())["state"]
        )
        with self.assertRaises(capacity.CapacityError):
            self.manager.operation("one", fingerprint("other"))

    def test_resolution_needs_evidence_and_a_reservation(self):
        self.initialize()
        self.manager.reserve("job", fingerprint(), 1)
        with self.assertRaises(capacity.CapacityError):
            self.manager.resolve("job", result={}, evidence_ref="")
        resolved = self.manager.resolve(
            "job", result={"revision": 2}, evidence_ref="matching provenance"
        )
        self.assertEqual("completed", resolved["state"])
        with self.assertRaises(capacity.CapacityError):
            self.manager.settle("absent", result={})

    def test_pending_reservations_survive_reopen_and_reconcile(self):
        self.initialize()
        self.manager.reserve("uncertain", fingerprint(), 1024)
        reopened = capacity.MemoryCapacity(self.path)
        reopened.reconcile()
        self.assertEqual(1024, reopened.status()["reserved_bytes"])
        self.assertTrue(reopened.reserve("uncertain", fingerprint(), 1024)["replay"])

    def test_two_writers_cannot_both_reserve_the_last_room(self):
        self.initialize()
        room = capacity.TOTAL_BYTES - self.manager.status()["charged_bytes"]
        barrier = threading.Barrier(2)
        results = []

        def contender(key):
            barrier.wait()
            try:
                capacity.MemoryCapacity(self.path).reserve(key, fingerprint(key), room)
                results.append("admitted")
            except capacity.CapacityError:
                results.append("refused")

        threads = [
            threading.Thread(target=contender, args=(key,)) for key in ("a", "b")
        ]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join(5)
            self.assertFalse(thread.is_alive())
        self.assertCountEqual(["admitted", "refused"], results)

    def test_invalid_reservation_input_is_refused(self):
        self.initialize()
        for key, value, size in (
            ("bad key", fingerprint(), 1),
            ("ok", "not-hex", 1),
            ("ok", fingerprint(), -1),
            ("ok", fingerprint(), True),
        ):
            with self.subTest(key=key, size=size):
                with self.assertRaises(capacity.CapacityError):
                    self.manager.reserve(key, value, size)

    def test_oversize_existing_ledger_refuses_growth_without_truncating_it(self):
        self.initialize()
        with self.manager.path.open("ab") as stream:
            stream.truncate(capacity.LEDGER_BYTES + 1)
        before = self.manager.path.read_bytes()
        with self.assertRaises(capacity.CapacityError):
            self.manager.reserve("job", fingerprint(), 0)
        self.assertEqual(before, self.manager.path.read_bytes())

    def test_corrupt_or_linked_ledger_and_lock_are_never_reinitialized(self):
        self.initialize()
        before = self.manager.path.read_bytes()
        self.manager.path.write_bytes(b"not sqlite")
        with self.assertRaises(capacity.CapacityError):
            self.manager.reserve("one", fingerprint(), 1)
        self.assertEqual(b"not sqlite", self.manager.path.read_bytes())
        self.manager.path.write_bytes(before)
        target = self.base / "lock-victim"
        target.write_text("untouched")
        self.manager.lock_path.unlink()
        self.manager.lock_path.symlink_to(target)
        with self.assertRaises(capacity.CapacityError):
            self.manager.reserve("one", fingerprint(), 1)
        self.assertEqual("untouched", target.read_text())

    def test_valid_sqlite_with_wrong_metadata_schema_is_refused_without_changes(self):
        self.initialize()
        connection = sqlite3.connect(self.manager.path)
        connection.execute("DROP TABLE metadata")
        connection.execute("CREATE TABLE metadata(singleton INTEGER)")
        connection.execute("INSERT INTO metadata VALUES (1)")
        connection.commit()
        connection.close()
        before = self.manager.path.read_bytes()
        for action in (
            lambda: self.manager.status(),
            lambda: self.manager.reconcile(),
            lambda: self.manager.operation("missing", fingerprint()),
            lambda: self.manager.reserve("new", fingerprint(), 0),
        ):
            with self.subTest(action=action), self.assertRaises(capacity.CapacityError):
                action()
        self.assertEqual(before, self.manager.path.read_bytes())


if __name__ == "__main__":
    unittest.main()
