"""Shared agent memory store (SPEC-0234); every case uses a temporary store."""

from __future__ import annotations

import json
import os
import sqlite3
import stat
import subprocess
import sys
import tempfile
import threading
import unittest
from pathlib import Path
from unittest import mock

from scripts.operations import agent_memory as memory

ROOT = Path(__file__).resolve().parents[3]
CLI = ROOT / "scripts/operations/agent_memory.py"
GIT = ["git", "-c", "user.name=Test", "-c", "user.email=t@example.com"]


def write(
    connection: sqlite3.Connection, memory_id: str, expected: int, body: str = "note"
) -> int:
    return memory.put(
        connection,
        memory_id=memory_id,
        expected_revision=expected,
        workspace_id="test",
        tier="long-term",
        owner="claude",
        body=body,
        source_refs=["SPEC-0234"],
    )


class StoreTests(unittest.TestCase):
    def setUp(self) -> None:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.base = Path(directory.name)
        self.path = self.base / ".workspace-memory" / "memory.sqlite3"
        self.connection = memory.connect(self.path)
        self.addCleanup(self.connection.close)

    def rows(self) -> list[tuple]:
        return self.connection.execute(
            "SELECT memory_id, revision, body FROM revisions ORDER BY 1, 2"
        ).fetchall()

    def test_store_is_private_and_uses_wal(self) -> None:
        self.assertEqual(0o700, stat.S_IMODE(self.path.parent.stat().st_mode))
        self.assertEqual(0o600, stat.S_IMODE(self.path.stat().st_mode))
        self.assertEqual(
            "wal", self.connection.execute("PRAGMA journal_mode").fetchone()[0]
        )

    def test_stale_expected_revision_changes_nothing(self) -> None:
        self.assertEqual(1, write(self.connection, "gate", 0, "first"))
        self.assertEqual(2, write(self.connection, "gate", 1, "second"))
        before = self.rows()
        for expected in (0, 1, 3):
            with self.subTest(expected=expected):
                with self.assertRaises(memory.MemoryStoreError) as caught:
                    write(self.connection, "gate", expected, "stale")
                self.assertEqual(memory.EXIT_CONFLICT, caught.exception.code)
                self.assertEqual(before, self.rows())
        self.assertEqual("second", memory.get(self.connection, "gate")["body"])
        self.assertEqual(
            [2, 1], [r["revision"] for r in memory.history(self.connection, "gate", 10)]
        )

    def test_limits_refuse_the_write_and_keep_existing_revisions(self) -> None:
        write(self.connection, "kept", 0, "x" * 10)
        before = self.rows()
        with self.assertRaises(memory.MemoryStoreError) as caught:
            write(self.connection, "big", 0, "x" * (memory.MAX_BODY_BYTES + 1))
        self.assertEqual(memory.EXIT_CAPACITY, caught.exception.code)
        with mock.patch.object(memory, "MAX_TOTAL_BODY_BYTES", 15):
            with self.assertRaisesRegex(
                memory.MemoryStoreError, "MEMORY_CAPACITY_EXCEEDED"
            ):
                write(self.connection, "over", 0, "x" * 6)
        with mock.patch.object(memory, "MAX_REVISIONS", 1):
            with self.assertRaisesRegex(
                memory.MemoryStoreError, "MEMORY_CAPACITY_EXCEEDED"
            ):
                write(self.connection, "over", 0)
        self.assertEqual(before, self.rows())

    def test_concurrent_writers_cannot_both_take_the_last_room(self) -> None:
        write(self.connection, "kept", 0, "x" * 10)
        barrier = threading.Barrier(2)
        outcomes: list[object] = []

        def writer(name: str) -> None:
            connection = memory.connect(self.path)
            try:
                barrier.wait()
                outcomes.append(write(connection, name, 0, "x" * 5))
            except memory.MemoryStoreError as error:
                outcomes.append(error.code)
            finally:
                connection.close()

        with mock.patch.object(memory, "MAX_TOTAL_BODY_BYTES", 15):
            threads = [
                threading.Thread(target=writer, args=(name,)) for name in ("a", "b")
            ]
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()
        self.assertEqual(sorted([1, memory.EXIT_CAPACITY]), sorted(outcomes))
        self.assertEqual(2, len(self.rows()))

    def test_a_full_database_is_reported_and_nothing_is_written(self) -> None:
        write(self.connection, "kept", 0)
        before = self.rows()
        pages = self.connection.execute("PRAGMA page_count").fetchone()[0]
        self.connection.execute(f"PRAGMA max_page_count = {pages}")
        with self.assertRaises(memory.MemoryStoreError) as caught:
            write(self.connection, "huge", 0, "y" * (memory.MAX_BODY_BYTES - 1))
        self.assertEqual(memory.EXIT_FULL, caught.exception.code)
        self.assertEqual(before, self.rows())

    def test_backup_restores_records_and_a_failure_keeps_the_previous_one(self) -> None:
        write(self.connection, "gate", 0, "kept")
        output = self.base / "backup" / "memory.sqlite3"
        output.parent.mkdir()
        memory.backup(self.connection, output)
        good = output.read_bytes()
        self.assertEqual(0o600, stat.S_IMODE(output.stat().st_mode))

        write(self.connection, "gate", 1, "newer")
        failing = mock.MagicMock(wraps=self.connection)
        failing.backup.side_effect = sqlite3.OperationalError("disk I/O error")
        with self.assertRaises(memory.MemoryStoreError) as caught:
            memory.backup(failing, output)
        self.assertEqual(memory.EXIT_BACKUP, caught.exception.code)
        self.assertEqual(good, output.read_bytes())
        self.assertEqual([output], list(output.parent.iterdir()))

        restored = self.base / "restored" / "memory.sqlite3"
        memory.restore(output, restored)
        connection = memory.connect(restored)
        self.addCleanup(connection.close)
        self.assertEqual("kept", memory.get(connection, "gate")["body"])
        with self.assertRaisesRegex(memory.MemoryStoreError, "MEMORY_RESTORE_REFUSED"):
            memory.restore(output, self.path)


class WorktreeStoreTests(unittest.TestCase):
    """Every worktree of one checkout reaches the same store through the CLI."""

    def cli(
        self, cwd: Path, *args: str, body: str = ""
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(CLI), *args],
            cwd=cwd,
            input=body,
            capture_output=True,
            text=True,
            env={**os.environ, "PYTHONPATH": str(ROOT)},
            check=False,
        )

    def test_a_linked_worktree_uses_the_main_checkout_store(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory).resolve()
            main = base / "main"
            main.mkdir()
            subprocess.run([*GIT, "init", "-q"], cwd=main, check=True)
            subprocess.run(
                [*GIT, "commit", "-q", "--allow-empty", "-m", "seed"],
                cwd=main,
                check=True,
            )
            linked = main / ".worktrees" / "feature"
            subprocess.run(
                [*GIT, "worktree", "add", "-q", str(linked)], cwd=main, check=True
            )

            put = (
                "put",
                "shared",
                "--expected-revision",
                "0",
                "--tier",
                "domain",
                "--owner",
                "claude",
            )
            written = self.cli(linked, *put, body="from the worktree")
            self.assertEqual(0, written.returncode, written.stderr)
            self.assertTrue((main / ".workspace-memory" / "memory.sqlite3").is_file())
            self.assertFalse((linked / ".workspace-memory").exists())

            read = self.cli(main, "get", "shared")
            self.assertEqual(0, read.returncode, read.stderr)
            record = json.loads(read.stdout)
            self.assertEqual(
                (1, "from the worktree"), (record["revision"], record["body"])
            )

            stale = self.cli(main, *put, body="lost update")
            self.assertEqual(memory.EXIT_CONFLICT, stale.returncode)
            self.assertIn("MEMORY_REVISION_CONFLICT", stale.stderr)

            subprocess.run(
                [*GIT, "worktree", "remove", str(linked)], cwd=main, check=True
            )
            self.assertEqual(
                "from the worktree",
                json.loads(self.cli(main, "get", "shared").stdout)["body"],
            )

    def test_outside_a_repository_memory_is_unavailable_and_nothing_is_created(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = self.cli(Path(directory), "usage")
            self.assertEqual(memory.EXIT_UNAVAILABLE, result.returncode)
            self.assertIn("MEMORY_UNAVAILABLE", result.stderr)
            self.assertEqual([], list(Path(directory).iterdir()))


if __name__ == "__main__":
    unittest.main()
