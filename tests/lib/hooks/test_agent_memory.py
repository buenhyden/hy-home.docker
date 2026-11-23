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

from scripts.lib.ops.memory_capacity import MemoryCapacity
from scripts.operations import agent_memory as memory


def initialize_capacity(path):
    MemoryCapacity(path).reconcile()


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
        initialize_capacity(self.path)
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
            initialize_capacity(main / ".workspace-memory" / "memory.sqlite3")
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
            initialize_capacity(main / ".workspace-memory" / "memory.sqlite3")
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


def reviewed(state, source_refs, cwd):
    # Treat the stated review state as the source-pin result, so the D06
    # applicability rules are tested without a Git fixture.
    return state


class RecordSemanticsTests(unittest.TestCase):
    """D06 kind, validity, supersession, baseline, export and erase."""

    def setUp(self) -> None:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.path = Path(directory.name) / ".workspace-memory" / "memory.sqlite3"
        initialize_capacity(self.path)
        self.connection = memory.connect(self.path)
        self.addCleanup(self.connection.close)
        patcher = mock.patch.object(memory, "reuse_state", reviewed)
        patcher.start()
        self.addCleanup(patcher.stop)

    def put(self, memory_id, expected=0, **extra):
        return memory.put(
            self.connection,
            memory_id=memory_id,
            expected_revision=expected,
            workspace_id="test",
            tier=extra.pop("tier", "long-term"),
            owner="claude",
            body=extra.pop("body", f"{memory_id} body"),
            source_refs=["SPEC-0212"],
            review_state=extra.pop("review_state", "current"),
            **extra,
        )

    def state(self, memory_id, as_of=None):
        record = memory.get(self.connection, memory_id, as_of=as_of)
        return record["provenance"]["reuse_state"]

    def test_kind_is_separate_from_the_tier_and_legacy_kind_is_derived(self):
        self.put("decided", kind="decision")
        self.put("brief", tier="short-term")
        decided = memory.get(self.connection, "decided")
        self.assertEqual(("decision", "long-term"), (decided["kind"], decided["tier"]))
        brief = memory.get(self.connection, "brief")
        self.assertEqual("session-context", brief["kind"])
        with self.assertRaises(memory.MemoryStoreError):
            self.put("bad", kind="task-status")

    def test_validity_window_limits_reuse_at_the_evaluation_time(self):
        self.put(
            "window",
            observed_at="2026-11-01T00:00:00+09:00",
            valid_from="2026-11-10T00:00:00Z",
            valid_until="2026-11-20T00:00:00Z",
        )
        record = memory.get(self.connection, "window")
        self.assertEqual("2026-10-31T15:00:00+00:00", record["observed_at"])
        for as_of, expected in (
            ("2026-11-09T00:00:00Z", "outside-validity"),
            ("2026-11-15T00:00:00Z", "current"),
            ("2026-11-20T00:00:00Z", "outside-validity"),
        ):
            with self.subTest(as_of=as_of):
                self.assertEqual(expected, self.state("window", as_of))
        self.assertIsNone(
            memory.get(
                self.connection,
                "window",
                current_only=True,
                as_of="2026-11-21T00:00:00Z",
            )
        )
        for bad in (
            {"valid_from": "2026-11-10"},
            {
                "valid_from": "2026-11-20T00:00:00Z",
                "valid_until": "2026-11-10T00:00:00Z",
            },
            {"observed_at": "yesterday"},
        ):
            with self.subTest(bad=bad), self.assertRaises(memory.MemoryStoreError):
                self.put("invalid", **bad)

    def test_supersession_hides_the_older_record_and_links_back(self):
        self.put("old")
        self.put("new", supersedes=["old"])
        self.assertEqual("superseded", self.state("old"))
        self.assertEqual(["new"], memory.get(self.connection, "old")["invalidated_by"])
        self.assertEqual(["old"], memory.get(self.connection, "new")["supersedes"])
        current = memory.current_records(self.connection, None, False)
        self.assertEqual(["new"], [r["memory_id"] for r in current])
        for target in (["missing"], ["self"]):
            with (
                self.subTest(target=target),
                self.assertRaises(memory.MemoryStoreError),
            ):
                self.put("self", supersedes=target)
        # Withdrawing the newer record makes the older one reusable again.
        self.put("new", 1, supersedes=["old"], eligibility="ineligible")
        self.assertEqual("current", self.state("old"))

    def test_baseline_cutover_leaves_earlier_records_out_of_default_reads(self):
        self.put("before", request_key="same-request")
        self.assertEqual(
            "initial", memory.get(self.connection, "before")["baseline_id"]
        )
        with self.assertRaises(memory.MemoryStoreError) as stale:
            memory.cutover(self.connection, expected="other", baseline_id="b2")
        self.assertEqual(memory.EXIT_CONFLICT, stale.exception.code)
        memory.cutover(self.connection, expected="initial", baseline_id="b2")
        self.assertEqual("other-baseline", self.state("before"))
        self.assertEqual([], memory.current_records(self.connection, None, False))
        self.assertEqual(1, len(memory.current_records(self.connection, None, True)))
        self.put("after")
        self.assertEqual("b2", memory.get(self.connection, "after")["baseline_id"])
        # The request digest binds the baseline, so the old key now conflicts.
        with self.assertRaises(memory.MemoryStoreError) as replay:
            self.put("before", 1, request_key="same-request")
        self.assertEqual("request-identity", replay.exception.details["reason"])

    def test_selected_export_and_erase_touch_only_the_named_records(self):
        self.put("keep")
        self.put("drop")
        self.put("drop", 1, body="second")
        with self.assertRaises(memory.MemoryStoreError):
            self.put("drop", 0, body="stale writer")
        exported = memory.export_selected(self.connection, ["drop"], True)
        self.assertEqual([2, 1], [r["revision"] for r in exported])
        latest = memory.export_selected(self.connection, ["drop"], False)
        self.assertEqual([2], [r["revision"] for r in latest])
        with self.assertRaises(memory.MemoryStoreError):
            memory.export_selected(self.connection, ["absent"], False)
        result = memory.erase(self.connection, ["drop", "absent"])
        self.assertEqual(["drop"], result["erased"])
        self.assertEqual(["absent"], result["missing"])
        self.assertEqual(
            {"revisions": 2, "provenance": 2, "conflicts": 1}, result["deleted_rows"]
        )
        for table in ("revisions", "provenance", "conflicts"):
            count = self.connection.execute(
                f"SELECT count(*) FROM {table} WHERE memory_id='drop'"
            ).fetchone()[0]
            self.assertEqual(0, count, table)
        self.assertIsNotNone(memory.get(self.connection, "keep"))

    def test_an_existing_store_needs_an_explicit_migration_to_write(self):
        legacy = self.path.with_name("legacy.sqlite3")
        connection = sqlite3.connect(legacy)
        connection.execute(memory.SCHEMA)
        values = ("old", 1, 2, "w", "long-term", "o", "2026-10-13", "[]")
        connection.execute(
            "INSERT INTO revisions VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            (*values, "eligible", "internal", "kept"),
        )
        connection.commit()
        connection.close()
        connection = memory.connect(legacy)
        self.addCleanup(connection.close)
        before = [tuple(r) for r in connection.execute("SELECT * FROM revisions")]
        self.assertTrue(memory.usage(connection)["migration_required"])
        write = dict(
            memory_id="new",
            expected_revision=0,
            workspace_id="w",
            tier="long-term",
            owner="o",
            body="x",
            source_refs=[],
        )
        with self.assertRaises(memory.MemoryStoreError) as refused:
            memory._put(connection, **write)
        self.assertIn("MIGRATION_REQUIRED", str(refused.exception))
        self.assertTrue(memory.migrate(connection)["migrated"])
        self.assertFalse(memory.migrate(connection)["migrated"])
        after = [tuple(r) for r in connection.execute("SELECT * FROM revisions")]
        self.assertEqual(before, after)
        self.assertEqual(1, memory._put(connection, **write))

    def test_usage_reports_the_enforced_page_limit_to_readers(self):
        reader = sqlite3.connect(self.path.absolute().as_uri() + "?mode=ro", uri=True)
        self.addCleanup(reader.close)
        page_size = reader.execute("PRAGMA page_size").fetchone()[0]
        report = memory.usage(reader)
        self.assertEqual(
            memory.MAX_DATABASE_BYTES // page_size, report["database_page_limit"]
        )
        self.assertEqual(3, report["schema_version"])
        self.assertFalse(report["migration_required"])

    def test_an_unresolved_conflict_leaves_default_reads_until_a_new_revision(
        self,
    ):
        self.put("shared")
        with self.assertRaises(memory.MemoryStoreError):
            self.put("shared", body="stale writer")
        self.assertEqual("conflicted", self.state("shared"))
        self.assertIsNone(memory.get(self.connection, "shared", current_only=True))
        self.assertEqual([], memory.current_records(self.connection, None, False))
        self.put("shared", expected=1, body="reconciled")
        self.assertEqual("current", self.state("shared"))

    def test_request_values_are_typed_and_finite(self):
        self.put("typed")
        # True equals 1 in Python; the typed request must still refuse it.
        for bad in (
            {"expected": True},
            {"source_refs": [{"weight": float("nan")}]},
        ):
            with self.subTest(bad=bad), self.assertRaises(memory.MemoryStoreError):
                memory.put(
                    self.connection,
                    memory_id="typed",
                    expected_revision=bad.get("expected", 1),
                    workspace_id="test",
                    tier="long-term",
                    owner="claude",
                    body="typed again",
                    source_refs=bad.get("source_refs", ["SPEC-0212"]),
                )
        self.assertEqual(1, len(memory.history(self.connection, "typed", 10)))


class SourceStateTests(unittest.TestCase):
    """D09 source states: current, changed, unavailable, content_expired."""

    def test_each_source_reference_reports_its_state(self):
        from scripts.lib.ops import memory_sources as sources

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            source = root / "source.md"
            source.write_text("reviewed")
            subprocess.run([*GIT, "init", "-q"], cwd=root, check=True)
            subprocess.run([*GIT, "add", "."], cwd=root, check=True)
            subprocess.run([*GIT, "commit", "-qm", "seed"], cwd=root, check=True)
            revision = subprocess.run(
                [*GIT, "rev-parse", "HEAD"],
                cwd=root,
                capture_output=True,
                text=True,
                check=True,
            ).stdout.strip()
            pin = dict(
                kind="repository-file",
                path="source.md",
                revision=revision,
                hash_algorithm="sha256",
                digest=hashlib.sha256(b"reviewed").hexdigest(),
                context="synthetic",
            )
            expired = {
                "kind": "session-events",
                "event_ids": ["e1"],
                "content_expires_at": "2026-11-01T00:00:00+00:00",
            }
            as_of = "2026-11-24T00:00:00+00:00"
            self.assertEqual("current", sources.source_state(pin, root, as_of))
            self.assertEqual(
                "content_expired", sources.source_state(expired, root, as_of)
            )
            self.assertEqual(
                "current",
                sources.source_state(
                    {**expired, "content_expires_at": "2026-12-01T00:00:00+00:00"},
                    root,
                    as_of,
                ),
            )
            self.assertEqual("unavailable", sources.source_state("SPEC", root, as_of))
            source.write_text("edited")
            self.assertEqual("changed", sources.source_state(pin, root, as_of))
            source.unlink()
            self.assertEqual("unavailable", sources.source_state(pin, root, as_of))
            # Session events never make a record reusable on their own.
            self.assertEqual(
                "needs-review", sources.reuse_state("current", [expired], root)
            )


if __name__ == "__main__":
    unittest.main()
