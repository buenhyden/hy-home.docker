"""Shared agent memory store (SPEC-0236); every case uses a temporary store."""

from __future__ import annotations

import hashlib
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
        source_refs=["SPEC-0236"],
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

    def test_the_rollback_journal_is_private(self) -> None:
        self.connection.execute("BEGIN IMMEDIATE")
        self.addCleanup(self.connection.execute, "ROLLBACK")
        self.connection.execute("PRAGMA user_version = 1")
        journal = self.path.with_name(self.path.name + "-journal")
        self.assertEqual(0o600, stat.S_IMODE(journal.stat().st_mode))

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
                with self.assertRaisesRegex(memory.MemoryStoreError, "symbolic link"):
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

    def test_request_identity_replays_only_the_same_semantic_write(self) -> None:
        arguments = dict(
            memory_id="retry",
            expected_revision=0,
            workspace_id="test",
            tier="long-term",
            owner="claude",
            body="kept",
            source_refs=[],
            request_key="request-1",
            review_state="candidate",
        )
        self.assertEqual(1, memory.put(self.connection, **arguments))
        self.assertEqual(1, memory.put(self.connection, **arguments))
        with self.assertRaises(memory.MemoryStoreError) as caught:
            memory.put(self.connection, **{**arguments, "owner": "codex"})
        self.assertEqual(memory.EXIT_CONFLICT, caught.exception.code)
        self.assertTrue(caught.exception.details["stored"])
        self.assertEqual(1, caught.exception.details["current_revision"])
        self.assertEqual(0, caught.exception.details["expected_revision"])
        self.assertEqual(
            1, self.connection.execute("SELECT count(*) FROM conflicts").fetchone()[0]
        )
        for changed in (
            {"body": "different"},
            {"source_refs": ["other"]},
            {"expected_revision": 1},
            {"tier": "short-term"},
            {"workspace_id": "other"},
            {"review_state": "needs-review"},
        ):
            with self.subTest(changed=changed):
                with self.assertRaises(memory.MemoryStoreError):
                    memory.put(self.connection, **{**arguments, **changed})
        self.assertEqual(1, len(self.rows()))

    def test_conflict_reports_no_room_without_losing_either_revision(self) -> None:
        write(self.connection, "kept", 0, "first")
        with mock.patch.object(memory, "MAX_TOTAL_BODY_BYTES", 5):
            with self.assertRaises(memory.MemoryStoreError) as caught:
                write(self.connection, "kept", 0, "incoming")
        self.assertFalse(caught.exception.details["stored"])
        self.assertEqual("first", memory.get(self.connection, "kept")["body"])

    def test_reconnect_reapplies_the_page_limit(self) -> None:
        other = memory.connect(self.path)
        try:
            self.assertEqual(
                memory.MAX_DATABASE_BYTES
                // other.execute("PRAGMA page_size").fetchone()[0],
                other.execute("PRAGMA max_page_count").fetchone()[0],
            )
        finally:
            other.close()

    def test_tier_domain_and_metadata_limits_keep_old_revisions(self) -> None:
        arguments = dict(
            memory_id="domain",
            expected_revision=0,
            workspace_id="test",
            tier="domain",
            domain_id="sqlite",
            owner="claude",
            body="sixsix",
            source_refs=[],
            review_state="candidate",
        )
        with mock.patch.object(memory, "MAX_DOMAIN_BODY_BYTES", 5):
            with self.assertRaises(memory.MemoryStoreError):
                memory.put(self.connection, **arguments)
        with mock.patch.dict(memory.TIER_BODY_BYTES, {"domain": 5}):
            with self.assertRaises(memory.MemoryStoreError):
                memory.put(self.connection, **arguments)
        with mock.patch.object(memory, "MAX_METADATA_BYTES", 5):
            with self.assertRaises(memory.MemoryStoreError):
                memory.put(self.connection, **arguments)
        self.assertEqual([], self.rows())

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

    def test_backup_serializes_competing_copies_and_preserves_conflicts(self) -> None:
        write(self.connection, "kept", 0)
        with self.assertRaises(memory.MemoryStoreError):
            write(self.connection, "kept", 0, "incoming")
        output = self.base / "backup" / "memory.sqlite3"
        output.parent.mkdir(mode=0o700)
        memory.backup(self.connection, output)
        before = output.read_bytes()
        started, release = threading.Event(), threading.Event()
        failures: list[Exception] = []

        def first_backup() -> None:
            connection = memory.connect(self.path)
            wrapped = mock.MagicMock(wraps=connection)

            def paused(target: sqlite3.Connection) -> None:
                started.set()
                if not release.wait(5):
                    raise AssertionError("backup test did not release")
                connection.backup(target)

            wrapped.backup.side_effect = paused
            try:
                memory.backup(wrapped, output)
            except Exception as error:
                failures.append(error)
            finally:
                connection.close()

        thread = threading.Thread(target=first_backup)
        thread.start()
        try:
            self.assertTrue(started.wait(5))
            with self.assertRaisesRegex(memory.MemoryStoreError, "another backup"):
                memory.backup(self.connection, output)
            self.assertEqual(before, output.read_bytes())
        finally:
            release.set()
            thread.join(5)
        self.assertEqual([], failures)
        self.assertFalse(thread.is_alive())
        target = self.base / "restored" / "memory.sqlite3"
        memory.restore(output, target)
        restored = memory.connect(target)
        try:
            self.assertEqual(
                "incoming", restored.execute("SELECT body FROM conflicts").fetchone()[0]
            )
            self.assertEqual("note", memory.get(restored, "kept")["body"])
        finally:
            restored.close()

    def test_schema_one_records_remain_exact_and_need_review(self) -> None:
        legacy = self.base / "legacy" / "memory.sqlite3"
        legacy.parent.mkdir()
        connection = sqlite3.connect(legacy)
        connection.execute(memory.SCHEMA)
        values = (
            "old",
            1,
            1,
            "original-workspace",
            "domain",
            "claude",
            "2026-10-13",
            '["native-claude-memory:approved-once"]',
            "eligible",
            "internal",
            "preserve every byte",
        )
        connection.execute(
            f"INSERT INTO revisions VALUES ({','.join('?' * len(values))})", values
        )
        connection.commit()
        connection.close()
        connection = memory.connect(legacy)
        try:
            self.assertEqual(
                values, tuple(connection.execute("SELECT * FROM revisions").fetchone())
            )
            self.assertIsNone(memory.get(connection, "old", current_only=True))
            record = memory.get(connection, "old")
            self.assertEqual(1, record["schema_version"])
            self.assertEqual("needs-review", record["provenance"]["reuse_state"])
            self.assertEqual(
                "preserve every byte", memory.history(connection, "old", 1)[0]["body"]
            )
        finally:
            connection.close()

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

    def test_backup_refuses_a_directory_another_user_owns(self) -> None:
        directory = self.base / "theirs"
        directory.mkdir(mode=0o700)
        with mock.patch.object(memory.os, "geteuid", return_value=os.geteuid() + 1):
            with self.assertRaisesRegex(memory.MemoryStoreError, "not owned"):
                memory.backup(self.connection, directory / "memory.sqlite3")
        self.assertEqual([], list(directory.iterdir()))

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

    def _backup_file(self) -> Path:
        write(self.connection, "gate", 0, "kept")
        directory = self.base / "backup"
        directory.mkdir(mode=0o700, exist_ok=True)
        output = directory / "memory.sqlite3"
        memory.backup(self.connection, output)
        return output

    def test_restore_publishes_atomically_and_never_replaces_a_store(self) -> None:
        output = self._backup_file()
        target = self.base / "race" / "memory.sqlite3"
        real_connect = sqlite3.connect
        seen: list[bool] = []

        def racing(database: object, *args: object, **kwargs: object):
            if not kwargs.get("uri") and str(database) != ":memory:":
                # The store path stays absent while the copy is built, and a
                # session creating it meanwhile must win.
                seen.append(target.exists())
                target.write_text("other session")
            return real_connect(database, *args, **kwargs)

        with mock.patch.object(memory.sqlite3, "connect", side_effect=racing):
            with self.assertRaisesRegex(memory.MemoryStoreError, "exists"):
                memory.restore(output, target)
        self.assertEqual([False], seen)
        self.assertEqual("other session", target.read_text())
        self.assertEqual([target], list(target.parent.iterdir()))

    def test_restore_reports_a_permission_failure(self) -> None:
        output = self._backup_file()
        target = self.base / "denied" / "memory.sqlite3"
        with mock.patch.object(
            memory, "_private_directory", side_effect=PermissionError("denied")
        ):
            with self.assertRaisesRegex(
                memory.MemoryStoreError, "MEMORY_RESTORE_FAILED"
            ):
                memory.restore(output, target)
        self.assertFalse(target.exists())


class WorktreeStoreTests(unittest.TestCase):
    """Every worktree of one checkout reaches the same store through the CLI."""

    def cli(
        self,
        cwd: Path,
        *args: str,
        body: str = "",
        script: Path | None = None,
        environment: dict[str, str] | None = None,
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
            env={
                **os.environ,
                "PYTHONPATH": str(ROOT),
                **({} if environment is None else environment),
            },
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

            read = self.cli(main, "get", "shared", "--historical")
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
                json.loads(self.cli(main, "get", "shared", "--historical").stdout)[
                    "body"
                ],
            )

    def test_current_retrieval_checks_the_callers_worktree_and_safe_sources(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory).resolve()
            main = base / "main"
            (main / "scripts/operations").mkdir(parents=True)
            (main / "scripts/operations/agent_memory.py").write_bytes(CLI.read_bytes())
            source = main / "source.md"
            source.write_text("older source")
            subprocess.run([*GIT, "init", "-q"], cwd=main, check=True)
            subprocess.run([*GIT, "add", "."], cwd=main, check=True)
            subprocess.run([*GIT, "commit", "-qm", "seed"], cwd=main, check=True)
            older_revision = subprocess.run(
                [*GIT, "rev-parse", "HEAD"],
                cwd=main,
                capture_output=True,
                text=True,
                check=True,
            ).stdout.strip()
            source.write_text("reviewed source")
            subprocess.run([*GIT, "add", "source.md"], cwd=main, check=True)
            subprocess.run(
                [*GIT, "commit", "-qm", "review source"], cwd=main, check=True
            )
            reviewed_revision = subprocess.run(
                [*GIT, "rev-parse", "HEAD"],
                cwd=main,
                capture_output=True,
                text=True,
                check=True,
            ).stdout.strip()
            linked = base / "linked"
            subprocess.run(
                [*GIT, "worktree", "add", "-q", str(linked)], cwd=main, check=True
            )
            reference = dict(
                kind="repository-file",
                path="source.md",
                revision=reviewed_revision,
                hash_algorithm="sha256",
                digest=hashlib.sha256(source.read_bytes()).hexdigest(),
                context="synthetic regression",
            )
            args = [
                "put",
                "current",
                "--expected-revision",
                "0",
                "--tier",
                "long-term",
                "--owner",
                "reviewer",
                "--review-state",
                "current",
                "--source-ref",
                json.dumps(reference),
            ]
            written = self.cli(main, *args, body="reviewed claim")
            self.assertEqual(0, written.returncode, written.stderr)
            self.assertEqual(0, self.cli(linked, "get", "current").returncode)
            (linked / "source.md").write_text("changed branch source")
            self.assertEqual(1, self.cli(linked, "get", "current").returncode)
            self.assertEqual([], json.loads(self.cli(linked, "list").stdout))
            preserved = json.loads(
                self.cli(linked, "get", "current", "--historical").stdout
            )
            self.assertEqual("needs-review", preserved["provenance"]["reuse_state"])
            self.assertEqual("reviewed claim", preserved["body"])
            self.assertEqual(0, self.cli(main, "get", "current").returncode)
            (linked / "source.md").unlink()
            (linked / "source.md").symlink_to(source)
            self.assertEqual(1, self.cli(linked, "get", "current").returncode)
            (linked / "source.md").unlink()
            os.mkfifo(linked / "source.md")
            fifo = subprocess.run(
                [
                    sys.executable,
                    str(linked / "scripts/operations/agent_memory.py"),
                    "get",
                    "current",
                ],
                cwd=linked,
                capture_output=True,
                text=True,
                timeout=2,
                check=False,
                env={**os.environ, "PYTHONPATH": str(ROOT)},
            )
            self.assertEqual(1, fifo.returncode, fifo.stderr)
            from scripts.lib.ops.memory_sources import source_is_current

            self.assertTrue(source_is_current(reference, main))
            self.assertFalse(
                source_is_current({**reference, "revision": "0" * 40}, main)
            )
            self.assertFalse(
                source_is_current({**reference, "revision": older_revision}, main)
            )
            blob = subprocess.run(
                [*GIT, "rev-parse", f"{reviewed_revision}:source.md"],
                cwd=main,
                capture_output=True,
                text=True,
                check=True,
            ).stdout.strip()
            self.assertTrue(
                source_is_current(
                    {**reference, "hash_algorithm": "git-blob", "digest": blob}, main
                )
            )
            self.assertFalse(
                source_is_current(
                    {**reference, "hash_algorithm": "git-blob", "digest": "f" * 40},
                    main,
                )
            )
            pathspec = main / ":(glob)*"
            pathspec.write_text("reviewed source")
            self.assertFalse(
                source_is_current({**reference, "path": pathspec.name}, main)
            )

            for path in (
                "../outside",
                ".workspace-memory/memory.sqlite3",
                ".claude/agent-memory/context.md",
            ):
                with (
                    self.subTest(path=path),
                    mock.patch("scripts.lib.ops.memory_sources.os.open") as opened,
                ):
                    self.assertFalse(
                        source_is_current({**reference, "path": path}, linked)
                    )
                    opened.assert_not_called()

    def test_source_pin_ignores_ambient_git_state_and_replace_refs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory).resolve()
            main = base / "main"
            main.mkdir()
            source = main / "source.md"
            source.write_text("reviewed source")
            subprocess.run([*GIT, "init", "-q"], cwd=main, check=True)
            subprocess.run([*GIT, "add", "source.md"], cwd=main, check=True)
            subprocess.run([*GIT, "commit", "-qm", "reviewed"], cwd=main, check=True)
            reviewed_revision = subprocess.run(
                [*GIT, "rev-parse", "HEAD"],
                cwd=main,
                capture_output=True,
                text=True,
                check=True,
            ).stdout.strip()
            reference = {
                "kind": "repository-file",
                "path": "source.md",
                "revision": reviewed_revision,
                "hash_algorithm": "sha256",
                "digest": hashlib.sha256(source.read_bytes()).hexdigest(),
                "context": "synthetic git boundary regression",
            }

            source.write_text("replacement source")
            subprocess.run([*GIT, "add", "source.md"], cwd=main, check=True)
            subprocess.run([*GIT, "commit", "-qm", "replacement"], cwd=main, check=True)
            replacement = subprocess.run(
                [*GIT, "rev-parse", "HEAD"],
                cwd=main,
                capture_output=True,
                text=True,
                check=True,
            ).stdout.strip()
            subprocess.run(
                [*GIT, "reset", "-q", "--hard", reviewed_revision],
                cwd=main,
                check=True,
            )
            subprocess.run(
                [*GIT, "replace", reviewed_revision, replacement],
                cwd=main,
                check=True,
            )

            foreign = base / "foreign"
            foreign.mkdir()
            (foreign / "source.md").write_text("foreign source")
            subprocess.run([*GIT, "init", "-q"], cwd=foreign, check=True)
            subprocess.run([*GIT, "add", "source.md"], cwd=foreign, check=True)
            subprocess.run([*GIT, "commit", "-qm", "foreign"], cwd=foreign, check=True)
            poisoned = {
                "GIT_DIR": str(foreign / ".git"),
                "GIT_WORK_TREE": str(foreign),
                "GIT_COMMON_DIR": str(foreign / ".git"),
                "GIT_INDEX_FILE": str(foreign / ".git/index"),
                "GIT_OBJECT_DIRECTORY": str(foreign / ".git/objects"),
                "GIT_ALTERNATE_OBJECT_DIRECTORIES": str(foreign / ".git/objects"),
                "GIT_CONFIG_COUNT": "1",
                "GIT_CONFIG_KEY_0": "core.bare",
                "GIT_CONFIG_VALUE_0": "true",
            }
            from scripts.lib.ops.memory_sources import source_is_current

            with mock.patch.dict(os.environ, poisoned):
                self.assertTrue(source_is_current(reference, main))

    def test_source_pin_fails_closed_when_git_times_out(self) -> None:
        reference = {
            "kind": "repository-file",
            "path": "source.md",
            "revision": "1" * 40,
            "hash_algorithm": "sha256",
            "digest": "2" * 64,
            "context": "synthetic timeout regression",
        }
        from scripts.lib.ops.memory_sources import source_is_current

        with mock.patch(
            "scripts.lib.ops.memory_sources.subprocess.run",
            side_effect=subprocess.TimeoutExpired(["git"], 5),
        ):
            self.assertFalse(source_is_current(reference, ROOT))

    def test_source_pin_requires_the_full_sha256_commit_id(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory).resolve()
            source = repository / "source.md"
            source.write_text("reviewed sha256 source")
            subprocess.run(
                [*GIT, "init", "-q", "--object-format=sha256"],
                cwd=repository,
                check=True,
            )
            subprocess.run([*GIT, "add", "source.md"], cwd=repository, check=True)
            subprocess.run(
                [*GIT, "commit", "-qm", "reviewed"], cwd=repository, check=True
            )
            revision = subprocess.run(
                [*GIT, "rev-parse", "HEAD"],
                cwd=repository,
                capture_output=True,
                text=True,
                check=True,
            ).stdout.strip()
            self.assertEqual(64, len(revision))
            reference = {
                "kind": "repository-file",
                "path": "source.md",
                "revision": revision,
                "hash_algorithm": "sha256",
                "digest": hashlib.sha256(source.read_bytes()).hexdigest(),
                "context": "synthetic sha256 oid regression",
            }
            from scripts.lib.ops.memory_sources import source_is_current

            self.assertTrue(source_is_current(reference, repository))
            self.assertFalse(
                source_is_current({**reference, "revision": revision[:40]}, repository)
            )

    def test_source_pin_never_lazy_fetches_a_missing_tree(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory).resolve()
            complete = base / "complete"
            partial = base / "partial"
            complete.mkdir()
            partial.mkdir()
            source = complete / "source.md"
            source.write_text("reviewed source")
            subprocess.run([*GIT, "init", "-q"], cwd=complete, check=True)
            subprocess.run([*GIT, "add", "source.md"], cwd=complete, check=True)
            subprocess.run(
                [*GIT, "commit", "-qm", "reviewed"], cwd=complete, check=True
            )
            revision = subprocess.run(
                [*GIT, "rev-parse", "HEAD"],
                cwd=complete,
                capture_output=True,
                text=True,
                check=True,
            ).stdout.strip()
            tree = subprocess.run(
                [*GIT, "rev-parse", "HEAD^{tree}"],
                cwd=complete,
                capture_output=True,
                text=True,
                check=True,
            ).stdout.strip()
            blob = subprocess.run(
                [*GIT, "rev-parse", "HEAD:source.md"],
                cwd=complete,
                capture_output=True,
                text=True,
                check=True,
            ).stdout.strip()
            commit = subprocess.run(
                [*GIT, "cat-file", "commit", revision],
                cwd=complete,
                capture_output=True,
                check=True,
            ).stdout

            subprocess.run([*GIT, "init", "-q"], cwd=partial, check=True)
            subprocess.run(
                [*GIT, "hash-object", "-t", "commit", "-w", "--stdin"],
                cwd=partial,
                input=commit,
                capture_output=True,
                check=True,
            )
            subprocess.run(
                [*GIT, "update-ref", "refs/heads/main", revision],
                cwd=partial,
                check=True,
            )
            subprocess.run(
                [*GIT, "symbolic-ref", "HEAD", "refs/heads/main"],
                cwd=partial,
                check=True,
            )
            subprocess.run(
                [
                    *GIT,
                    "update-index",
                    "--add",
                    "--info-only",
                    "--cacheinfo",
                    f"100644,{blob},source.md",
                ],
                cwd=partial,
                check=True,
            )
            (partial / "source.md").write_text("reviewed source")
            for key, value in (
                ("remote.origin.promisor", "true"),
                ("remote.origin.partialclonefilter", "tree:0"),
                ("extensions.partialClone", "origin"),
                ("protocol.ext.allow", "always"),
            ):
                subprocess.run([*GIT, "config", key, value], cwd=partial, check=True)
            marker = base / "remote-invoked"
            helper = base / "remote-helper"
            helper.write_text(
                "#!/usr/bin/python3\n"
                "from pathlib import Path\n"
                f"Path({str(marker)!r}).touch()\n"
                "raise SystemExit(1)\n"
            )
            helper.chmod(0o700)
            subprocess.run(
                [*GIT, "config", "remote.origin.url", f"ext::{helper}"],
                cwd=partial,
                check=True,
            )
            self.assertFalse((partial / ".git/objects" / tree[:2] / tree[2:]).exists())
            reference = {
                "kind": "repository-file",
                "path": "source.md",
                "revision": revision,
                "hash_algorithm": "sha256",
                "digest": hashlib.sha256(source.read_bytes()).hexdigest(),
                "context": "synthetic no-lazy-fetch regression",
            }
            from scripts.lib.ops.memory_sources import source_is_current

            self.assertFalse(source_is_current(reference, partial))
            self.assertFalse(marker.exists())

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
            poisoned = {
                "GIT_DIR": str(other / ".git"),
                "GIT_WORK_TREE": str(other),
                "GIT_INDEX_FILE": str(other / ".git/index"),
                "GIT_OBJECT_DIRECTORY": str(other / ".git/objects"),
            }
            result = self.cli(other, "usage", script=CLI, environment=poisoned)
            self.assertEqual(memory.EXIT_UNAVAILABLE, result.returncode)
            self.assertFalse((other / ".workspace-memory").exists())


if __name__ == "__main__":
    unittest.main()
