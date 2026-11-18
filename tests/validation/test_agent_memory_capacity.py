"""Memory CLI admission and read-only behaviour on isolated fixture stores."""

from __future__ import annotations

import contextlib
import io
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import scripts.lib.ops.memory_cli as memory_cli
from scripts.lib.ops.memory_capacity import CapacityError, MemoryCapacity
from scripts.operations import agent_memory as memory


class MemoryCliCapacityTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.path = Path(temporary.name) / ".workspace-memory" / "memory.sqlite3"

    def cli(self, *args, body=""):
        output, error = io.StringIO(), io.StringIO()
        with (
            mock.patch.object(memory, "store_path", return_value=self.path),
            mock.patch("sys.stdin", io.StringIO(body)),
            contextlib.redirect_stdout(output),
            contextlib.redirect_stderr(error),
        ):
            result = memory_cli.run(list(args), memory)
        return result, output.getvalue(), error.getvalue()

    def initialize(self):
        return MemoryCapacity(self.path).reconcile()

    def test_status_and_missing_search_never_initialize_state(self):
        result, output, _ = self.cli("capacity", "status")
        self.assertEqual(0, result)
        self.assertEqual("unverified", json.loads(output)["inventory_state"])
        self.assertFalse(self.path.parent.exists())
        result, _, _ = self.cli("search", "--query", "needle")
        self.assertEqual(memory.EXIT_UNAVAILABLE, result)
        self.assertFalse(self.path.parent.exists())

    def test_missing_ledger_refuses_put_before_a_store_is_created(self):
        result, _, error = self.cli(
            "put",
            "note",
            "--expected-revision",
            "0",
            "--tier",
            "long-term",
            "--owner",
            "fixture",
            body="synthetic",
        )
        self.assertEqual(memory.EXIT_CAPACITY, result)
        self.assertIn("CAPACITY", error)
        self.assertFalse(self.path.parent.exists())

    def test_put_with_initialized_capacity_and_readonly_search(self):
        self.initialize()
        result, _, error = self.cli(
            "put",
            "note",
            "--expected-revision",
            "0",
            "--tier",
            "long-term",
            "--owner",
            "fixture",
            body="synthetic needle",
        )
        self.assertEqual(0, result, error)
        before = {
            path.name: (path.read_bytes(), path.stat().st_mode)
            for path in self.path.parent.iterdir()
        }
        result, output, error = self.cli("search", "--query", "needle")
        self.assertEqual(0, result, error)
        self.assertEqual([], json.loads(output))
        self.assertEqual(
            before,
            {
                path.name: (path.read_bytes(), path.stat().st_mode)
                for path in self.path.parent.iterdir()
            },
        )

    def test_capacity_status_does_not_modify_existing_files(self):
        self.initialize()
        before = {
            path.name: (path.read_bytes(), path.stat().st_mode)
            for path in self.path.parent.iterdir()
        }
        self.assertEqual(0, self.cli("capacity", "status")[0])
        self.assertEqual(
            before,
            {
                path.name: (path.read_bytes(), path.stat().st_mode)
                for path in self.path.parent.iterdir()
            },
        )

    def test_existing_commands_use_the_same_admitted_store(self):
        self.initialize()
        self.assertEqual(
            0,
            self.cli(
                "put",
                "note",
                "--expected-revision",
                "0",
                "--tier",
                "long-term",
                "--owner",
                "fixture",
                body="synthetic needle",
            )[0],
        )
        self.assertEqual(0, self.cli("get", "note", "--historical")[0])
        self.assertEqual(1, self.cli("get", "note")[0])
        self.assertEqual(0, self.cli("history", "note")[0])
        self.assertEqual(0, self.cli("list", "--all")[0])
        self.assertEqual(0, self.cli("export")[0])
        self.assertEqual(0, self.cli("usage")[0])
        self.assertEqual(
            0,
            self.cli(
                "set-eligibility",
                "note",
                "--expected-revision",
                "1",
                "--owner",
                "fixture",
                "ineligible",
            )[0],
        )
        self.assertEqual(
            memory.EXIT_CONFLICT,
            self.cli(
                "set-eligibility",
                "missing",
                "--expected-revision",
                "0",
                "--owner",
                "fixture",
                "ineligible",
            )[0],
        )

    def test_local_reconciliation_and_value_free_search(self):
        self.assertEqual(0, self.cli("capacity", "reconcile")[0])
        self.assertEqual(
            0,
            self.cli(
                "put",
                "note",
                "--expected-revision",
                "0",
                "--tier",
                "long-term",
                "--owner",
                "fixture",
                body="synthetic",
            )[0],
        )
        result, _, error = self.cli(
            "search", "--query", "private-query-marker", "--limit", "51"
        )
        self.assertEqual(memory.EXIT_UNAVAILABLE, result)
        self.assertNotIn("private-query-marker", error)
        with self.assertRaises(SystemExit):
            self.cli("capacity", "reconcile", "--input", "invented-inventory.json")

    def test_legacy_snapshot_reads_preserve_bytes_and_do_not_create_sidecars(self):
        self.path.parent.mkdir(mode=0o700)
        connection = sqlite3.connect(self.path)
        connection.execute(memory.SCHEMA)
        connection.execute(
            "INSERT INTO revisions VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            (
                "legacy",
                1,
                1,
                "fixture",
                "long-term",
                "fixture",
                "2026-10-13",
                "[]",
                "eligible",
                "internal",
                "preserved original wording",
            ),
        )
        connection.commit()
        connection.close()
        self.path.chmod(0o600)
        before = self.path.read_bytes(), self.path.stat().st_mode
        for arguments in (
            ("get", "legacy", "--historical"),
            ("history", "legacy"),
            ("list", "--all"),
            ("export",),
            ("usage",),
            ("search", "--query", "wording"),
        ):
            with self.subTest(arguments=arguments):
                result, _, error = self.cli(*arguments)
                self.assertEqual(0, result, error)
        self.assertEqual(1, self.cli("get", "legacy")[0])
        self.assertEqual([], json.loads(self.cli("search", "--query", "wording")[1]))
        self.assertEqual(before, (self.path.read_bytes(), self.path.stat().st_mode))
        self.assertEqual([self.path], list(self.path.parent.iterdir()))

    def test_committed_put_recovers_after_capacity_settlement_was_interrupted(self):
        self.initialize()
        args = (
            "put",
            "note",
            "--expected-revision",
            "0",
            "--tier",
            "long-term",
            "--owner",
            "fixture",
            "--request-key",
            "stable-request",
        )
        with mock.patch.object(MemoryCapacity, "settle", side_effect=CapacityError()):
            result, _, _ = self.cli(*args, body="committed once")
        self.assertEqual(memory.EXIT_CAPACITY, result)
        self.assertEqual(
            1, len(MemoryCapacity(self.path).status()["pending_operations"])
        )
        before = self.path.read_bytes()
        result, output, error = self.cli(*args, body="committed once")
        self.assertEqual(0, result, error)
        self.assertEqual(1, json.loads(output)["revision"])
        self.assertEqual(before, self.path.read_bytes())
        self.assertEqual([], MemoryCapacity(self.path).status()["pending_operations"])

    def test_corrupt_capacity_does_not_block_existing_memory_reads(self):
        self.initialize()
        self.assertEqual(
            0,
            self.cli(
                "put",
                "note",
                "--expected-revision",
                "0",
                "--tier",
                "long-term",
                "--owner",
                "fixture",
                body="preserved",
            )[0],
        )
        MemoryCapacity(self.path).path.write_bytes(b"corrupt capacity fixture")
        for arguments in (
            ("get", "note", "--historical"),
            ("history", "note"),
            ("usage",),
            ("search", "--query", "preserved"),
        ):
            with self.subTest(arguments=arguments):
                result, _, error = self.cli(*arguments)
                self.assertEqual(0, result, error)
        self.assertEqual(
            "unverified",
            json.loads(self.cli("usage")[1])["aggregate_capacity"]["inventory_state"],
        )
        self.assertEqual(4, self.cli("capacity", "status")[0])

    def test_wrong_capacity_schema_has_fixed_diagnostics_and_preserves_ledger(self):
        self.initialize()
        path = MemoryCapacity(self.path).path
        connection = sqlite3.connect(path)
        connection.execute("DROP TABLE metadata")
        connection.execute("CREATE TABLE metadata(singleton INTEGER)")
        connection.execute("INSERT INTO metadata VALUES (1)")
        connection.execute("CREATE TABLE private_marker(value TEXT)")
        connection.execute(
            "INSERT INTO private_marker VALUES ('private-diagnostic-marker')"
        )
        connection.commit()
        connection.close()
        before = path.read_bytes()
        for arguments in (("capacity", "status"), ("capacity", "reconcile")):
            result, output, error = self.cli(*arguments)
            self.assertEqual(4, result)
            self.assertEqual("", output)
            self.assertNotIn("Traceback", error)
            self.assertNotIn("private-diagnostic-marker", error)
        self.assertEqual(before, path.read_bytes())

    def test_unknown_pending_put_does_not_write_or_silently_retry(self):
        self.initialize()
        connection = memory.connect(self.path)
        arguments = dict(
            memory_id="note",
            expected_revision=0,
            workspace_id="fixture",
            tier="long-term",
            owner="fixture",
            body="once",
            source_refs=[],
            request_key="pending-request",
        )
        fingerprint = memory.operation_fingerprint(arguments)
        key = (
            "put:"
            + memory.hashlib.sha256(
                ("pending-request" + fingerprint).encode()
            ).hexdigest()
        )
        MemoryCapacity(self.path).reserve(key, fingerprint, 0)
        try:
            with self.assertRaises(memory.MemoryStoreError) as caught:
                memory.put(connection, **arguments)
            self.assertEqual(memory.EXIT_BUSY, caught.exception.code)
            self.assertEqual(
                0, connection.execute("SELECT count(*) FROM revisions").fetchone()[0]
            )
        finally:
            connection.close()

    def test_erase_needs_the_exact_confirmation_and_baseline_commands_work(self):
        self.initialize()
        for memory_id in ("alpha", "beta"):
            result, _, error = self.cli(
                "put",
                memory_id,
                "--expected-revision",
                "0",
                "--tier",
                "long-term",
                "--owner",
                "fixture",
                "--kind",
                "decision",
                body="synthetic",
            )
            self.assertEqual(0, result, error)
        erase = ("erase", "--memory-id", "beta", "--memory-id", "alpha", "--confirm")
        result, _, error = self.cli(*erase, "beta,alpha")
        self.assertEqual(memory.EXIT_UNAVAILABLE, result)
        self.assertIn("--confirm", error)
        self.assertEqual(0, self.cli("get", "alpha", "--historical")[0])
        result, output, error = self.cli(*erase, "alpha,beta")
        self.assertEqual(0, result, error)
        self.assertEqual(["alpha", "beta"], json.loads(output)["erased"])
        self.assertEqual(1, self.cli("get", "alpha", "--historical")[0])
        shown = json.loads(self.cli("baseline", "show")[1])
        self.assertEqual("initial", shown["baseline_id"])
        move = ("baseline", "cutover", "--to", "b2", "--expected")
        self.assertEqual(memory.EXIT_CONFLICT, self.cli(*move, "wrong")[0])
        result, _, error = self.cli(*move, "initial")
        self.assertEqual(0, result, error)
        self.assertEqual("b2", json.loads(self.cli("usage")[1])["baseline_id"])


if __name__ == "__main__":
    unittest.main()
