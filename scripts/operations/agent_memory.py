#!/usr/bin/env python3
"""Shared agent memory: one SQLite store for every worktree and provider.

The store lives at `<main checkout>/.workspace-memory/memory.sqlite3`, found
through `git rev-parse --git-common-dir`, so every linked worktree uses the
same file. This CLI is its only writer. Every update names the revision it
expects; a stale one is refused and nothing changes. Limits are logical: the
CLI refuses a write that would cross them and never removes existing
revisions. No filesystem quota enforces them.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sqlite3
import subprocess
import sys
from pathlib import Path

SCHEMA_VERSION = 1
STORE_DIRECTORY = ".workspace-memory"
STORE_NAME = "memory.sqlite3"
TIERS = ("short-term", "long-term", "domain")
ELIGIBILITY = ("eligible", "ineligible")
SENSITIVITY = ("public", "internal")
# Logical limits, checked inside the write transaction.
MAX_BODY_BYTES = 16 * 1024
MAX_REVISIONS = 10_000
MAX_TOTAL_BODY_BYTES = 32 * 1024 * 1024
MAX_HISTORY = 50
BUSY_TIMEOUT_MS = 5_000

EXIT_UNAVAILABLE = 2
EXIT_CONFLICT = 3
EXIT_CAPACITY = 4
EXIT_BUSY = 5
EXIT_FULL = 6
EXIT_BACKUP = 7

SCHEMA = f"""
CREATE TABLE IF NOT EXISTS revisions (
    memory_id TEXT NOT NULL CHECK (length(memory_id) BETWEEN 1 AND 128),
    revision INTEGER NOT NULL CHECK (revision >= 1),
    schema_version INTEGER NOT NULL,
    workspace_id TEXT NOT NULL,
    tier TEXT NOT NULL CHECK (tier IN {TIERS}),
    owner TEXT NOT NULL,
    created_at TEXT NOT NULL,
    source_refs TEXT NOT NULL,
    eligibility TEXT NOT NULL CHECK (eligibility IN {ELIGIBILITY}),
    sensitivity TEXT NOT NULL CHECK (sensitivity IN {SENSITIVITY}),
    body TEXT NOT NULL,
    PRIMARY KEY (memory_id, revision)
)
"""
COLUMNS = (
    "memory_id",
    "revision",
    "schema_version",
    "workspace_id",
    "tier",
    "owner",
    "created_at",
    "source_refs",
    "eligibility",
    "sensitivity",
    "body",
)


class MemoryStoreError(Exception):
    """A refused memory operation with its CLI exit code."""

    def __init__(self, code: int, message: str) -> None:
        super().__init__(message)
        self.code = code


def store_path(cwd: Path | None = None) -> Path:
    """The one store of the main checkout that owns this Git repository."""
    try:
        common = subprocess.run(
            ["git", "rev-parse", "--path-format=absolute", "--git-common-dir"],
            cwd=cwd,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError) as error:
        raise MemoryStoreError(
            EXIT_UNAVAILABLE, "MEMORY_UNAVAILABLE: no Git repository"
        ) from error
    common_dir = Path(common)
    if common_dir.name != ".git" or not common_dir.is_dir():
        raise MemoryStoreError(EXIT_UNAVAILABLE, "MEMORY_UNAVAILABLE: no main checkout")
    return common_dir.parent / STORE_DIRECTORY / STORE_NAME


def connect(path: Path) -> sqlite3.Connection:
    path.parent.mkdir(mode=0o700, exist_ok=True)
    os.chmod(path.parent, 0o700)
    if not path.exists():
        path.touch(mode=0o600)
    connection = sqlite3.connect(
        path, timeout=BUSY_TIMEOUT_MS / 1000, isolation_level=None
    )
    connection.row_factory = sqlite3.Row
    connection.execute(f"PRAGMA busy_timeout = {BUSY_TIMEOUT_MS}")
    connection.execute("PRAGMA journal_mode = WAL")
    connection.execute(SCHEMA)
    return connection


def _record(row: sqlite3.Row) -> dict[str, object]:
    record = {key: row[key] for key in COLUMNS}
    record["source_refs"] = json.loads(row["source_refs"])
    return record


def _current(connection: sqlite3.Connection, memory_id: str) -> sqlite3.Row | None:
    return connection.execute(
        "SELECT * FROM revisions WHERE memory_id = ? ORDER BY revision DESC LIMIT 1",
        (memory_id,),
    ).fetchone()


def get(connection: sqlite3.Connection, memory_id: str) -> dict[str, object] | None:
    row = _current(connection, memory_id)
    return None if row is None else _record(row)


def history(
    connection: sqlite3.Connection, memory_id: str, limit: int
) -> list[dict[str, object]]:
    rows = connection.execute(
        "SELECT * FROM revisions WHERE memory_id = ? ORDER BY revision DESC LIMIT ?",
        (memory_id, max(1, min(limit, MAX_HISTORY))),
    )
    return [_record(row) for row in rows]


def current_records(
    connection: sqlite3.Connection, tier: str | None, everything: bool
) -> list[dict[str, object]]:
    rows = connection.execute(
        "SELECT r.* FROM revisions r JOIN (SELECT memory_id, max(revision) AS top"
        " FROM revisions GROUP BY memory_id) c"
        " ON r.memory_id = c.memory_id AND r.revision = c.top ORDER BY r.memory_id"
    )
    return [
        _record(row)
        for row in rows
        if (tier is None or row["tier"] == tier)
        and (everything or row["eligibility"] == "eligible")
    ]


def usage(connection: sqlite3.Connection) -> dict[str, object]:
    revisions, body_bytes = connection.execute(
        "SELECT count(*), coalesce(sum(length(CAST(body AS BLOB))), 0) FROM revisions"
    ).fetchone()
    return {
        "revisions": revisions,
        "body_bytes": body_bytes,
        "limits": {
            "kind": "logical",
            "max_body_bytes": MAX_BODY_BYTES,
            "max_revisions": MAX_REVISIONS,
            "max_total_body_bytes": MAX_TOTAL_BODY_BYTES,
        },
        "sqlite_version": sqlite3.sqlite_version,
    }


def put(
    connection: sqlite3.Connection,
    *,
    memory_id: str,
    expected_revision: int,
    workspace_id: str,
    tier: str,
    owner: str,
    body: str,
    source_refs: list[str],
    sensitivity: str = "internal",
    eligibility: str = "eligible",
) -> int:
    """Commit one new revision, or change nothing."""
    size = len(body.encode("utf-8"))
    if size > MAX_BODY_BYTES:
        raise MemoryStoreError(
            EXIT_CAPACITY,
            f"MEMORY_CAPACITY_EXCEEDED: body {size} > {MAX_BODY_BYTES} bytes",
        )
    try:
        # BEGIN IMMEDIATE takes the single write lock first, so the limit
        # check and the insert see the same totals as every other writer.
        connection.execute("BEGIN IMMEDIATE")
        try:
            row = _current(connection, memory_id)
            current = 0 if row is None else row["revision"]
            if current != expected_revision:
                raise MemoryStoreError(
                    EXIT_CONFLICT,
                    f"MEMORY_REVISION_CONFLICT: {memory_id} is at revision {current}, not {expected_revision}",
                )
            revisions, body_bytes = connection.execute(
                "SELECT count(*), coalesce(sum(length(CAST(body AS BLOB))), 0) FROM revisions"
            ).fetchone()
            if (
                revisions + 1 > MAX_REVISIONS
                or body_bytes + size > MAX_TOTAL_BODY_BYTES
            ):
                raise MemoryStoreError(
                    EXIT_CAPACITY, "MEMORY_CAPACITY_EXCEEDED: store limit reached"
                )
            connection.execute(
                f"INSERT INTO revisions ({', '.join(COLUMNS)}) VALUES ({', '.join('?' * len(COLUMNS))})",
                (
                    memory_id,
                    current + 1,
                    SCHEMA_VERSION,
                    workspace_id,
                    tier,
                    owner,
                    dt.datetime.now(dt.UTC).isoformat(timespec="seconds"),
                    json.dumps(source_refs),
                    eligibility,
                    sensitivity,
                    body,
                ),
            )
            connection.execute("COMMIT")
        except BaseException:
            if connection.in_transaction:
                connection.execute("ROLLBACK")
            raise
    except sqlite3.OperationalError as error:
        text = str(error).lower()
        if "locked" in text or "busy" in text:
            raise MemoryStoreError(
                EXIT_BUSY, "MEMORY_STORE_BUSY: another writer holds the store"
            ) from error
        if "full" in text:
            raise MemoryStoreError(
                EXIT_FULL, "MEMORY_STORE_FULL: no space; nothing was written"
            ) from error
        raise
    try:
        connection.execute("PRAGMA wal_checkpoint(PASSIVE)")
    except sqlite3.Error as error:
        print(
            f"MEMORY_CHECKPOINT_DEFERRED: {error}; the revision is committed",
            file=sys.stderr,
        )
    return current + 1


def backup(connection: sqlite3.Connection, output: Path) -> None:
    """Refresh one backup file; a failure keeps the previous good backup."""
    output = output.absolute()
    temporary = output.with_name(f".{output.name}.tmp")
    try:
        temporary.unlink(missing_ok=True)
        target = sqlite3.connect(temporary)
        try:
            connection.backup(target)
            if target.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
                raise sqlite3.DatabaseError("backup failed integrity_check")
        finally:
            target.close()
        os.chmod(temporary, 0o600)
        os.replace(temporary, output)
    except (OSError, sqlite3.Error) as error:
        temporary.unlink(missing_ok=True)
        raise MemoryStoreError(
            EXIT_BACKUP, f"MEMORY_BACKUP_FAILED: {error}; previous backup kept"
        ) from error


def restore(source: Path, path: Path) -> None:
    """Rebuild a missing store from a backup; an existing store is never replaced."""
    if path.exists():
        raise MemoryStoreError(EXIT_CONFLICT, f"MEMORY_RESTORE_REFUSED: {path} exists")
    backup_db = sqlite3.connect(f"file:{source}?mode=ro", uri=True)
    try:
        if backup_db.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
            raise MemoryStoreError(
                EXIT_BACKUP, "MEMORY_RESTORE_REFUSED: backup failed integrity_check"
            )
        connection = connect(path)
        try:
            backup_db.backup(connection)
        finally:
            connection.close()
    finally:
        backup_db.close()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    commands = parser.add_subparsers(dest="command", required=True)
    get_parser = commands.add_parser("get")
    get_parser.add_argument("memory_id")
    history_parser = commands.add_parser("history")
    history_parser.add_argument("memory_id")
    history_parser.add_argument("--limit", type=int, default=10)
    list_parser = commands.add_parser("list")
    list_parser.add_argument("--tier", choices=TIERS)
    list_parser.add_argument(
        "--all", action="store_true", help="include ineligible records"
    )
    put_parser = commands.add_parser(
        "put", help="write a new revision; body is read from stdin"
    )
    put_parser.add_argument("memory_id")
    put_parser.add_argument("--expected-revision", type=int, required=True)
    put_parser.add_argument("--tier", choices=TIERS, required=True)
    put_parser.add_argument("--owner", required=True)
    put_parser.add_argument("--source-ref", action="append", default=[])
    put_parser.add_argument("--sensitivity", choices=SENSITIVITY, default="internal")
    eligibility_parser = commands.add_parser("set-eligibility")
    eligibility_parser.add_argument("memory_id")
    eligibility_parser.add_argument("--expected-revision", type=int, required=True)
    eligibility_parser.add_argument("--owner", required=True)
    eligibility_parser.add_argument("eligibility", choices=ELIGIBILITY)
    commands.add_parser("usage")
    commands.add_parser("export", help="current records as JSON")
    backup_parser = commands.add_parser("backup")
    backup_parser.add_argument("--output", type=Path, required=True)
    restore_parser = commands.add_parser("restore", help="rebuild a missing store")
    restore_parser.add_argument("--input", type=Path, required=True)
    arguments = parser.parse_args(argv)

    try:
        path = store_path()
        if arguments.command == "restore":
            restore(arguments.input, path)
            return 0
        connection = connect(path)
        workspace_id = path.parent.parent.as_posix()
        result: object
        if arguments.command == "get":
            result = get(connection, arguments.memory_id)
            if result is None:
                print(f"MEMORY_NOT_FOUND: {arguments.memory_id}", file=sys.stderr)
                return 1
        elif arguments.command == "history":
            result = history(connection, arguments.memory_id, arguments.limit)
        elif arguments.command in {"list", "export"}:
            tier = getattr(arguments, "tier", None)
            result = current_records(
                connection, tier, arguments.command == "export" or arguments.all
            )
        elif arguments.command == "usage":
            result = usage(connection)
        elif arguments.command == "backup":
            backup(connection, arguments.output)
            result = {"backup": arguments.output.as_posix()}
        elif arguments.command == "put":
            revision = put(
                connection,
                memory_id=arguments.memory_id,
                expected_revision=arguments.expected_revision,
                workspace_id=workspace_id,
                tier=arguments.tier,
                owner=arguments.owner,
                body=sys.stdin.read(),
                source_refs=arguments.source_ref,
                sensitivity=arguments.sensitivity,
            )
            result = {"memory_id": arguments.memory_id, "revision": revision}
        else:
            row = get(connection, arguments.memory_id)
            if row is None:
                raise MemoryStoreError(
                    EXIT_CONFLICT,
                    f"MEMORY_REVISION_CONFLICT: {arguments.memory_id} does not exist",
                )
            revision = put(
                connection,
                memory_id=arguments.memory_id,
                expected_revision=arguments.expected_revision,
                workspace_id=workspace_id,
                tier=str(row["tier"]),
                owner=arguments.owner,
                body=str(row["body"]),
                source_refs=list(row["source_refs"]),  # type: ignore[arg-type]
                sensitivity=str(row["sensitivity"]),
                eligibility=arguments.eligibility,
            )
            result = {"memory_id": arguments.memory_id, "revision": revision}
    except MemoryStoreError as error:
        print(error, file=sys.stderr)
        return error.code
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
