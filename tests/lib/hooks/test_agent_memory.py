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

    def test_store_is_private_and_uses_a_rollback_journal(self) -> None:
        self.assertEqual(0o700, stat.S_IMODE(self.path.parent.stat().st_mode))
        self.assertEqual(0o600, stat.S_IMODE(self.path.stat().st_mode))
        self.assertEqual(
            "delete", self.connection.execute("PRAGMA journal_mode").fetchone()[0]
        )

    def test_a_symbolic_link_store_or_directory_is_refused(self) -> None:
        victim = self.base / "victim"
        victim.mkdir()
        linked_directory = self.base / "linked" / ".workspace-memory"
        linked_directory.parent.mkdir()
        linked_directory.symlink_to(victim)
        linked_file = self.base / "dangling" / ".workspace-memory" / "memory.sqlite3"
        linked_file.parent.mkdir(parents=True)
        linked_file.symlink_to(victim / "planted.sqlite3")
        for path in (linked_directory / "memory.sqlite3", linked_file):
            with self.subTest(path=path):
                with self.assertRaisesRegex(
                    memory.MemoryStoreError, "symbolic link"
                ):
                    memory.connect(path)
        self.assertEqual([], list(victim.iterdir()))

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
        output.parent.mkdir(mode=0o700)
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

    def test_backup_refuses_the_store_and_unsafe_directories(self) -> None:
        write(self.connection, "gate", 0)
        for name in ("memory.sqlite3", "memory.sqlite3-journal", "memory.sqlite3-wal"):
            with self.subTest(output=name):
                with self.assertRaisesRegex(memory.MemoryStoreError, "store itself"):
                    memory.backup(self.connection, self.path.parent / name)
        shared = self.base / "shared"
        shared.mkdir()
        os.chmod(shared, 0o755)
        private = self.base / "private"
        private.mkdir(mode=0o700)
        linked = self.base / "linked"
        linked.symlink_to(private)
        for directory, reason in ((shared, "not 0700"), (linked, "not a directory")):
            with self.subTest(directory=directory):
                with self.assertRaisesRegex(memory.MemoryStoreError, reason):
                    memory.backup(self.connection, directory / "memory.sqlite3")
        self.assertEqual([], list(shared.iterdir()))
        self.assertEqual([], list(private.iterdir()))

    def test_backup_never_follows_a_link_planted_at_its_temporary_name(self) -> None:
        write(self.connection, "gate", 0)
        directory = self.base / "backup"
        directory.mkdir(mode=0o700)
        victim = self.base / "victim.sqlite3"
        victim.write_text("untouched")
        temporary = directory / ".memory.sqlite3.tmp"
        temporary.symlink_to(victim)
        real_connect = sqlite3.connect
        modes: list[int] = []

        def observed(database: object, *args: object, **kwargs: object):
            if Path(str(database)) == temporary:
                modes.append(stat.S_IMODE(os.lstat(temporary).st_mode))
            return real_connect(database, *args, **kwargs)

        with mock.patch.object(memory.sqlite3, "connect", side_effect=observed):
            memory.backup(self.connection, directory / "memory.sqlite3")
        # The temporary file is already private when SQLite opens it.
        self.assertEqual([0o600], modes)
        self.assertEqual("untouched", victim.read_text())
        output = directory / "memory.sqlite3"
        self.assertFalse(output.is_symlink())
        self.assertEqual(0o600, stat.S_IMODE(output.stat().st_mode))

    def test_restore_checks_the_schema_and_leaves_no_partial_store(self) -> None:
        write(self.connection, "gate", 0, "kept")
        directory = self.base / "odd?name#dir%"
        directory.mkdir(mode=0o700)
        output = directory / "memory.sqlite3"
        memory.backup(self.connection, output)
        restored = self.base / "restored" / "memory.sqlite3"
        memory.restore(output, restored)
        connection = memory.connect(restored)
        self.addCleanup(connection.close)
        self.assertEqual("kept", memory.get(connection, "gate")["body"])

        tampered = self.base / "tampered.sqlite3"
        database = sqlite3.connect(tampered)
        database.execute(memory.SCHEMA)
        database.execute(
            "CREATE TRIGGER wipe AFTER INSERT ON revisions BEGIN"
            " DELETE FROM revisions; END"
        )
        database.commit()
        database.close()
        target = self.base / "fresh" / "memory.sqlite3"
        with self.assertRaisesRegex(memory.MemoryStoreError, "schema differs"):
            memory.restore(tampered, target)
        self.assertFalse(target.exists())

        failing = self.base / "failing" / "memory.sqlite3"
        real_connect = sqlite3.connect

        def failing_source(database: object, *args: object, **kwargs: object):
            connection = real_connect(database, *args, **kwargs)
            if not kwargs.get("uri"):
                return connection
            source = mock.MagicMock(wraps=connection)
            source.backup.side_effect = sqlite3.OperationalError("boom")
            return source

        with mock.patch.object(memory.sqlite3, "connect", side_effect=failing_source):
            with self.assertRaisesRegex(memory.MemoryStoreError, "no store was left"):
                memory.restore(output, failing)
        self.assertEqual([], list(failing.parent.iterdir()))


class WorktreeStoreTests(unittest.TestCase):
    """Every worktree of one checkout reaches the same store through the CLI."""

    def cli(
        self, cwd: Path, *args: str, body: str = "", script: Path | None = None
    ) -> subprocess.CompletedProcess[str]:
        # Each checkout runs its own copy of the CLI, as an agent session does.
        if script is None:
            script = cwd / "scripts/operations/agent_memory.py"
            if not script.is_file():
                script = CLI
        return subprocess.run(
            [sys.executable, str(script), *args],
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
            (main / "scripts/operations").mkdir(parents=True)
            (main / "scripts/operations/agent_memory.py").write_bytes(CLI.read_bytes())
            subprocess.run([*GIT, "init", "-q"], cwd=main, check=True)
            subprocess.run([*GIT, "add", "."], cwd=main, check=True)
            subprocess.run(
                [*GIT, "commit", "-q", "-m", "seed"],
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

    def test_another_repository_never_gets_a_second_store(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            other = Path(directory).resolve()
            subprocess.run([*GIT, "init", "-q"], cwd=other, check=True)
            result = self.cli(other, "usage", script=CLI)
            self.assertEqual(memory.EXIT_UNAVAILABLE, result.returncode)
            self.assertIn("run the CLI of the repository you are in", result.stderr)
            self.assertFalse((other / ".workspace-memory").exists())


if __name__ == "__main__":
    unittest.main()
