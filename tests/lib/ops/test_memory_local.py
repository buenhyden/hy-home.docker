"""Local copy lifecycle accounting without any real memory or backup."""

from __future__ import annotations

import sqlite3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.lib.ops.memory_capacity import COPY_BYTES, CapacityError, MemoryCapacity
from scripts.lib.ops.memory_local import (
    local_copy_guard,
    reconcile_local_copies,
    run_local_copy,
)


class LocalCopyTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name)
        self.path = self.base / ".workspace-memory" / "memory.sqlite3"
        self.manager = MemoryCapacity(self.path)
        self.manager.reconcile(
            {
                "schema_version": 1,
                "complete": True,
                "local_paths": [],
                "external_snapshots": [],
            }
        )
        self.output = self.base / "private" / "copy.sqlite3"
        self.output.parent.mkdir(mode=0o700)

    def test_known_no_io_failure_releases_reservation_without_creating_output(self):
        def refused():
            raise ValueError("synthetic failure before copy")

        for _ in range(10):
            with self.assertRaisesRegex(ValueError, "synthetic failure"):
                run_local_copy(
                    self.manager, "manual-backup", self.path, self.output, refused
                )
        self.assertEqual(0, self.manager.status()["reserved_bytes"])
        self.assertFalse(self.output.exists())

    def test_completed_copy_records_output_and_retains_all_existing_bytes(self):
        run_local_copy(
            self.manager,
            "manual-backup",
            self.path,
            self.output,
            lambda: self.output.touch(mode=0o600),
        )
        self.assertEqual(COPY_BYTES, self.manager.status()["local_backup_bytes"])
        self.assertEqual([], self.manager.status()["pending_operations"])

    def test_interrupted_copy_reconciles_capacity_only_after_producer_has_ended(self):
        temporary = self.output.with_name("." + self.output.name + ".tmp")

        def interrupted():
            self.output.touch(mode=0o600)
            temporary.touch(mode=0o600)
            raise KeyboardInterrupt()

        with self.assertRaises(KeyboardInterrupt):
            run_local_copy(
                self.manager, "manual-backup", self.path, self.output, interrupted
            )
        self.assertEqual(3 * COPY_BYTES, self.manager.status()["reserved_bytes"])
        with local_copy_guard(self.manager):
            with self.assertRaises(CapacityError):
                reconcile_local_copies(self.manager)
        result = reconcile_local_copies(self.manager)
        self.assertEqual(0, result["reserved_bytes"])
        self.assertEqual(2 * COPY_BYTES, result["local_backup_bytes"])
        self.assertTrue(self.output.exists())
        self.assertTrue(temporary.exists())

    def test_restore_charges_the_preexisting_unregistered_backup_source(self):
        self.output.touch(mode=0o600)
        run_local_copy(
            self.manager,
            "restore",
            self.output,
            self.path,
            lambda: self.path.touch(mode=0o600),
        )
        self.assertEqual(COPY_BYTES, self.manager.status()["local_backup_bytes"])
        self.assertTrue(self.output.exists())

    def test_unsafe_retained_copy_keeps_its_pending_reservation(self):
        def interrupted():
            self.output.touch(mode=0o600)
            raise KeyboardInterrupt()

        with self.assertRaises(KeyboardInterrupt):
            run_local_copy(
                self.manager, "manual-backup", self.path, self.output, interrupted
            )
        self.output.chmod(0o644)
        with self.assertRaises(CapacityError):
            reconcile_local_copies(self.manager)
        self.assertEqual(3 * COPY_BYTES, self.manager.status()["reserved_bytes"])

    def test_multiple_interrupted_restores_charge_only_their_own_temporary(self):
        self.output.touch(mode=0o600)
        for index in (1, 2):
            temporary = self.path.with_name(
                "." + self.path.name + ".restore-" + str(index) * 32
            )
            context = {
                "producer": "restore",
                "source": str(self.output),
                "target": str(self.path),
                "temporary": str(temporary),
            }
            self.manager.reserve(
                str(index), str(index) * 64, 3 * COPY_BYTES, context=context
            )
            temporary.touch(mode=0o600)
        result = reconcile_local_copies(self.manager)
        self.assertEqual(0, result["reserved_bytes"])
        self.assertEqual(3 * COPY_BYTES, result["local_backup_bytes"])

    def test_abrupt_process_exit_retains_the_exact_recorded_restore_temporary(self):
        from scripts.operations import agent_memory as memory

        connection = sqlite3.connect(self.output)
        connection.execute(memory.SCHEMA)
        connection.commit()
        connection.close()
        self.output.chmod(0o600)
        program = """import os,sys
from pathlib import Path
from scripts.operations import agent_memory as memory
original = memory.sqlite3.connect
def abrupt(database,*args,**kwargs):
    if Path(str(database)).name.startswith('.memory.sqlite3.restore-'):
        os._exit(17)
    return original(database,*args,**kwargs)
memory.sqlite3.connect=abrupt
memory.restore(Path(sys.argv[1]),Path(sys.argv[2]))
"""
        result = subprocess.run(
            [sys.executable, "-c", program, str(self.output), str(self.path)],
            cwd=Path(__file__).resolve().parents[3],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(17, result.returncode, result.stderr)
        pending = self.manager.status()["pending_operations"]
        self.assertEqual(1, len(pending))
        temporary = Path(pending[0]["context"]["temporary"])
        self.assertEqual(
            [temporary], list(self.path.parent.glob(".memory.sqlite3.restore-*"))
        )
        self.assertTrue(temporary.exists())
        result = reconcile_local_copies(self.manager)
        self.assertEqual(0, result["reserved_bytes"])
        self.assertEqual(2 * COPY_BYTES, result["local_backup_bytes"])
        self.assertFalse(self.path.exists())


if __name__ == "__main__":
    unittest.main()
