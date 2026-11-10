"""Logical memory allocation, using only private temporary fixture stores."""

from __future__ import annotations

import hashlib
import sqlite3
import tempfile
import threading
import unittest
from pathlib import Path
from unittest import mock

from scripts.lib.ops import memory_capacity as capacity


def inventory(**changes):
    return {
        "schema_version": 1,
        "complete": True,
        "local_paths": [],
        "external_snapshots": [],
        **changes,
    }


def fingerprint(value="fixture"):
    return hashlib.sha256(value.encode()).hexdigest()


class CapacityTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name)
        self.path = self.base / ".workspace-memory" / "memory.sqlite3"
        self.manager = capacity.MemoryCapacity(self.path)

    def initialize(self, **changes):
        return self.manager.reconcile(inventory(**changes))

    def test_status_of_missing_ledger_is_read_only_and_growth_is_refused(self):
        self.assertEqual("unverified", self.manager.status()["inventory_state"])
        self.assertFalse(self.path.parent.exists())
        with self.assertRaises(capacity.CapacityError):
            self.manager.reserve("one", fingerprint(), 1)
        self.assertFalse(self.path.parent.exists())

    def test_schema_and_fixed_capacity_are_independent_of_memory_snapshot(self):
        self.initialize()
        status = self.manager.status()
        self.assertEqual(1, status["schema_version"])
        self.assertEqual(1_073_741_824, status["cap_bytes"])
        self.assertEqual("complete", status["inventory_state"])
        self.assertFalse(self.path.exists())
        self.assertEqual(0o600, self.manager.path.stat().st_mode & 0o777)
        self.assertEqual(0o700, self.path.parent.stat().st_mode & 0o777)

    def test_reservation_replay_is_not_another_admission_and_conflicts_stop(self):
        self.initialize()
        first = self.manager.reserve("one", fingerprint(), 32)
        self.assertFalse(first["replay"])
        second = self.manager.reserve("one", fingerprint(), 32)
        self.assertTrue(second["replay"])
        self.assertEqual(32, self.manager.status()["reserved_bytes"])
        with self.assertRaises(capacity.CapacityError):
            self.manager.reserve("one", fingerprint("different"), 32)
        self.manager.settle("one", [], result={"revision": 1})
        replay = self.manager.reserve("one", fingerprint(), 32)
        self.assertEqual("completed", replay["state"])
        self.assertEqual({"revision": 1}, replay["result"])

    def test_pending_reservations_survive_reopen_and_reconcile(self):
        self.initialize()
        self.manager.reserve("uncertain", fingerprint(), 1024)
        reopened = capacity.MemoryCapacity(self.path)
        reopened.reconcile(inventory())
        self.assertEqual(1024, reopened.status()["reserved_bytes"])
        self.assertTrue(reopened.reserve("uncertain", fingerprint(), 1024)["replay"])

    def test_two_writers_cannot_both_reserve_the_last_room(self):
        self.initialize()
        used = self.manager.status()["charged_bytes"]
        room = capacity.TOTAL_BYTES - used
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

    def test_metadata_inventory_charges_each_external_location(self):
        snapshot = {
            "repository_id": "a" * 64,
            "snapshot_id": "b" * 64,
            "location": "state",
            "evidence_ref": "snapshot metadata",
        }
        self.initialize(
            external_snapshots=[snapshot, {**snapshot, "location": "offsite"}]
        )
        self.assertEqual(
            2 * capacity.COPY_BYTES, self.manager.status()["external_bytes"]
        )
        self.manager.reserve("unresolved", fingerprint(), 10)
        generation = self.manager.status()["generation"]
        self.manager.reconcile(
            inventory(
                observed_repositories=[
                    {"repository_id": "a" * 64, "location": location}
                    for location in ("state", "offsite")
                ]
            ),
            expected_generation=generation,
        )
        self.assertEqual(0, self.manager.status()["external_bytes"])
        self.assertEqual(10, self.manager.status()["reserved_bytes"])

    def test_local_backup_is_registered_without_reading_its_body(self):
        directory = self.base / "backup"
        directory.mkdir(mode=0o700)
        backup = directory / "memory.sqlite3"
        backup.write_bytes(b"synthetic")
        backup.chmod(0o600)
        self.initialize(local_paths=[str(backup)])
        self.assertEqual(
            capacity.COPY_BYTES, self.manager.status()["local_backup_bytes"]
        )
        backup.unlink()
        self.manager.reconcile(inventory(local_paths=[str(backup)]))
        self.assertEqual(0, self.manager.status()["local_backup_bytes"])

    def test_unsafe_paths_incomplete_input_and_forged_charges_are_refused(self):
        for bad in (
            inventory(complete=False),
            inventory(extra=True),
            inventory(schema_version=2),
        ):
            with self.subTest(bad=bad), self.assertRaises(capacity.CapacityError):
                self.manager.reconcile(bad)
        victim = self.base / "victim"
        victim.mkdir(mode=0o700)
        linked = self.base / "linked"
        linked.symlink_to(victim)
        with self.assertRaises(capacity.CapacityError):
            self.manager.reconcile(inventory(local_paths=[str(linked / "snapshot")]))
        self.initialize()
        self.manager.reserve("one", fingerprint(), 1)
        with self.assertRaises(capacity.CapacityError):
            self.manager.settle("one", [{"charged_bytes": -1}])

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

    def test_full_and_unknown_inventory_preserve_existing_allocations(self):
        self.initialize()
        before = self.manager.status()
        with self.assertRaises(capacity.CapacityError):
            self.manager.reserve("huge", fingerprint(), capacity.TOTAL_BYTES)
        self.assertEqual(before, self.manager.status())
        with self.assertRaises(capacity.CapacityError):
            self.manager.reserve("bad", "not-a-fingerprint", 1)
        with self.assertRaises(capacity.CapacityError):
            self.manager.reserve("bad", fingerprint(), -1)

    def test_exact_operation_lookup_and_successful_result_reconciliation(self):
        self.assertIsNone(self.manager.operation("job", fingerprint()))
        self.initialize()
        self.assertIsNone(self.manager.operation("job", fingerprint()))
        self.manager.reserve("job", fingerprint(), capacity.COPY_BYTES)
        self.assertEqual(
            "pending", self.manager.operation("job", fingerprint())["state"]
        )
        with self.assertRaises(capacity.CapacityError):
            self.manager.operation("job", fingerprint("other"))
        allocation = capacity.external_allocation(
            {
                "repository_id": "a" * 64,
                "snapshot_id": "b" * 64,
                "location": "state",
                "evidence_ref": "fixed producer metadata",
            }
        )
        self.manager.resolve(
            "job",
            [allocation],
            result={"snapshot": "b" * 64},
            evidence_ref="matching completed operation tag",
        )
        self.assertEqual(
            "completed", self.manager.operation("job", fingerprint())["state"]
        )
        self.assertEqual(capacity.COPY_BYTES, self.manager.status()["external_bytes"])
        self.assertEqual([], self.manager.status()["pending_operations"])
        self.manager.settle("job", [], result={"ignored": True})
        self.assertEqual(capacity.COPY_BYTES, self.manager.status()["external_bytes"])
        with self.assertRaises(capacity.CapacityError):
            self.manager.resolve("job", [], result={}, evidence_ref="")

    def test_oversize_existing_ledger_refuses_growth_without_truncating_it(self):
        self.initialize()
        with self.manager.path.open("ab") as stream:
            stream.truncate(capacity.LEDGER_BYTES + 1)
        before = self.manager.path.read_bytes()
        with self.assertRaises(capacity.CapacityError):
            self.manager.reserve("job", fingerprint(), 0)
        self.assertEqual(before, self.manager.path.read_bytes())

    def test_structurally_invalid_allocation_is_a_sanitized_refusal(self):
        self.initialize()
        connection = sqlite3.connect(self.manager.path)
        connection.execute(
            "INSERT INTO allocations VALUES ('x','external','state',?,'metadata')",
            (capacity.COPY_BYTES,),
        )
        connection.commit()
        connection.close()
        for operation in (
            lambda: self.manager.status(),
            lambda: self.manager.reconcile(inventory()),
            lambda: self.manager.reserve("new", fingerprint(), 0),
        ):
            with self.assertRaises(capacity.CapacityError):
                operation()

    def test_corrupt_local_operation_context_stays_pending_and_is_sanitized(self):
        self.initialize()
        self.manager.reserve("pending", fingerprint(), 1)
        connection = sqlite3.connect(self.manager.path)
        connection.execute(
            "UPDATE operations SET context=? WHERE request_key='pending'",
            ('{"producer":"restore"}',),
        )
        connection.commit()
        connection.close()
        for action in (
            lambda: self.manager.status(),
            lambda: self.manager.reserve("new", fingerprint(), 0),
        ):
            with self.assertRaises(capacity.CapacityError):
                action()
        connection = sqlite3.connect(self.manager.path)
        try:
            self.assertEqual(
                (1, "pending"),
                connection.execute(
                    "SELECT reserved_bytes,state FROM operations WHERE request_key='pending'"
                ).fetchone(),
            )
        finally:
            connection.close()

    def test_deeply_nested_corrupt_context_is_a_sanitized_refusal(self):
        self.initialize()
        self.manager.reserve("pending", fingerprint(), 1)
        connection = sqlite3.connect(self.manager.path)
        connection.execute(
            "UPDATE operations SET context=? WHERE request_key='pending'",
            ("[" * 2000 + "0" + "]" * 2000,),
        )
        connection.commit()
        connection.close()
        with self.assertRaises(capacity.CapacityError):
            self.manager.status()

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
            lambda: self.manager.reconcile(inventory()),
            lambda: self.manager.operation("missing", fingerprint()),
            lambda: self.manager.reserve("new", fingerprint(), 0),
        ):
            with self.subTest(action=action), self.assertRaises(capacity.CapacityError):
                action()
        self.assertEqual(before, self.manager.path.read_bytes())

    def test_invalid_external_metadata_and_settlement_cannot_reduce_reservations(self):
        self.initialize()
        self.manager.reserve("job", fingerprint(), 1)
        base = {
            "repository_id": "a" * 64,
            "snapshot_id": "b" * 64,
            "location": "state",
            "evidence_ref": "metadata",
        }
        for snapshot in (
            {**base, "location": "unknown"},
            {**base, "snapshot_id": "not-an-id"},
            {**base, "evidence_ref": ""},
            {**base, "repository_id": None},
            {**base, "extra": True},
        ):
            with (
                self.subTest(snapshot=snapshot),
                self.assertRaises(capacity.CapacityError),
            ):
                self.manager.reconcile(inventory(external_snapshots=[snapshot]))
        allocation = capacity.external_allocation(base)
        for allocations in (
            [allocation],
            [{**allocation, "charged_bytes": 1}],
            [{**allocation, "resource_key": "bad"}],
            [{**allocation, "kind": "other"}],
        ):
            with (
                self.subTest(allocations=allocations),
                self.assertRaises(capacity.CapacityError),
            ):
                self.manager.settle("job", allocations)
        with self.assertRaises(capacity.CapacityError):
            self.manager.settle("absent", [])
        with self.assertRaises(capacity.CapacityError):
            self.manager.settle("job", [], result={"large": "x" * 5000})
        self.assertEqual(1, self.manager.status()["reserved_bytes"])

    def test_generation_duplicate_inventory_and_oversize_local_files_are_rejected(self):
        self.initialize()
        with self.assertRaises(capacity.CapacityError):
            self.manager.reconcile(inventory(), expected_generation=0)
        self.assertEqual(
            2, self.manager.reconcile(inventory(), expected_generation=1)["generation"]
        )
        directory = self.base / "backup"
        directory.mkdir(mode=0o700)
        path = directory / "copy"
        path.touch(mode=0o600)
        with self.assertRaises(capacity.CapacityError):
            self.manager.reconcile(inventory(local_paths=[str(path), str(path)]))
        with path.open("wb") as stream:
            stream.truncate(capacity.COPY_BYTES + 1)
        with self.assertRaises(capacity.CapacityError):
            self.manager.reconcile(inventory(local_paths=[str(path)]))
        with self.assertRaises(capacity.CapacityError):
            self.manager.reconcile(inventory(local_paths=["relative"]))

    def test_reconciliation_cannot_erase_a_concurrently_settled_backup(self):
        directory = self.base / "backup"
        directory.mkdir(mode=0o700)
        path = directory / "copy"
        path.touch(mode=0o600)
        self.initialize(local_paths=[str(path)])
        self.manager.reserve("job", fingerprint(), capacity.COPY_BYTES)
        path.unlink()
        observed, release, settled = (
            threading.Event(),
            threading.Event(),
            threading.Event(),
        )
        failures = []
        original = Path.exists

        def paused_exists(candidate):
            answer = original(candidate)
            if candidate == path and threading.current_thread().name == "reconcile":
                observed.set()
                if not release.wait(5):
                    raise AssertionError("fixture release missing")
            return answer

        def reconcile():
            try:
                self.manager.reconcile(inventory(local_paths=[str(path)]))
            except Exception as error:
                failures.append(error)

        def settle():
            try:
                path.touch(mode=0o600)
                self.manager.settle("job", [capacity.local_allocation(path)])
                settled.set()
            except Exception as error:
                failures.append(error)

        with mock.patch.object(Path, "exists", paused_exists):
            first = threading.Thread(target=reconcile, name="reconcile")
            first.start()
            self.assertTrue(observed.wait(5))
            second = threading.Thread(target=settle)
            second.start()
            settled_early = settled.wait(0.2)
            release.set()
            first.join(5)
            second.join(5)
        self.assertFalse(first.is_alive())
        self.assertFalse(second.is_alive())
        self.assertEqual([], failures)
        self.assertFalse(settled_early)
        self.assertEqual(
            capacity.COPY_BYTES, self.manager.status()["local_backup_bytes"]
        )


if __name__ == "__main__":
    unittest.main()
