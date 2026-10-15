#!/usr/bin/env python3
"""Shared agent memory: one SQLite store for every worktree and provider."""

from __future__ import annotations

import argparse
import datetime as dt
import fcntl
import hashlib
import json
import os
import sqlite3
import stat
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts.lib.ops.memory_sources import REVIEW_STATES, reuse_state  # noqa: E402

SCHEMA_VERSION = 2
STORE_DIRECTORY = ".workspace-memory"
STORE_NAME = "memory.sqlite3"
TIERS = ("short-term", "long-term", "domain")
ELIGIBILITY = ("eligible", "ineligible")
SENSITIVITY = ("public", "internal")
# Logical limits, checked inside the write transaction.
MAX_BODY_BYTES = 16 * 1024
MAX_REVISIONS = 10_000
MAX_TOTAL_BODY_BYTES = 32 * 1024 * 1024
TIER_BODY_BYTES = {
    "short-term": 8 * 1024 * 1024,
    "long-term": 16 * 1024 * 1024,
    "domain": 16 * 1024 * 1024,
}
MAX_DOMAIN_BODY_BYTES = 8 * 1024 * 1024
MAX_METADATA_BYTES = 16 * 1024
MAX_TOTAL_METADATA_BYTES = 8 * 1024 * 1024
MAX_CONFLICTS = 10_000
MAX_DATABASE_BYTES = 64 * 1024 * 1024
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
SIDECARS = (
    "CREATE TABLE IF NOT EXISTS provenance (memory_id TEXT NOT NULL, revision INTEGER NOT NULL,"
    " metadata TEXT NOT NULL, request_key TEXT UNIQUE, fingerprint TEXT NOT NULL,"
    " PRIMARY KEY (memory_id, revision))",
    "CREATE TABLE IF NOT EXISTS conflicts (conflict_id INTEGER PRIMARY KEY, memory_id TEXT NOT NULL,"
    " expected_revision INTEGER NOT NULL, current_revision INTEGER NOT NULL, metadata TEXT NOT NULL, body TEXT NOT NULL)",
)


class MemoryStoreError(Exception):
    """A refused memory operation with its CLI exit code."""

    def __init__(self, code: int, message: str, **details: object) -> None:
        super().__init__(message)
        self.code = code
        self.details = details


def _common_dir(cwd: Path) -> Path | None:
    try:
        common = subprocess.run(
            ["git", "rev-parse", "--path-format=absolute", "--git-common-dir"],
            cwd=cwd,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None
    return Path(common).resolve()


def store_path(cwd: Path | None = None) -> Path:
    """Resolve the script's shared store only from the same repository."""
    own = _common_dir(Path(__file__).resolve().parent)
    here = _common_dir(Path.cwd() if cwd is None else cwd)
    if own is None or here is None:
        raise MemoryStoreError(
            EXIT_UNAVAILABLE, "MEMORY_UNAVAILABLE: no Git repository"
        )
    if own != here:
        raise MemoryStoreError(
            EXIT_UNAVAILABLE,
            "MEMORY_UNAVAILABLE: run the CLI of the repository you are in",
        )
    if own.name != ".git" or not own.is_dir():
        raise MemoryStoreError(EXIT_UNAVAILABLE, "MEMORY_UNAVAILABLE: no main checkout")
    return own.parent / STORE_DIRECTORY / STORE_NAME


def _refuse_symlink(path: Path) -> None:
    if path.is_symlink():
        raise MemoryStoreError(
            EXIT_UNAVAILABLE, f"MEMORY_UNAVAILABLE: {path} is a symbolic link"
        )


def _create_private(path: Path) -> None:
    os.close(os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600))


def _private_directory(path: Path) -> None:
    _refuse_symlink(path)
    path.mkdir(mode=0o700, exist_ok=True)
    _refuse_symlink(path)
    os.chmod(path, 0o700)


def connect(path: Path) -> sqlite3.Connection:
    _private_directory(path.parent)
    _refuse_symlink(path)
    try:
        _create_private(path)
    except FileExistsError:
        pass
    connection = sqlite3.connect(
        path, timeout=BUSY_TIMEOUT_MS / 1000, isolation_level=None
    )
    connection.row_factory = sqlite3.Row
    connection.execute(f"PRAGMA busy_timeout = {BUSY_TIMEOUT_MS}")
    # Rollback journal: WAL needs the WAL-reset fix this host's SQLite lacks.
    connection.execute("PRAGMA journal_mode = DELETE")
    page_size = connection.execute("PRAGMA page_size").fetchone()[0]
    connection.execute(f"PRAGMA max_page_count = {MAX_DATABASE_BYTES // page_size}")
    connection.execute(SCHEMA)
    for statement in SIDECARS:
        connection.execute(statement)
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


def _view(
    connection: sqlite3.Connection, row: sqlite3.Row, cwd: Path | None = None
) -> dict[str, object]:
    record = _record(row)
    metadata = connection.execute(
        "SELECT metadata FROM provenance WHERE memory_id=? AND revision=?",
        (row["memory_id"], row["revision"]),
    ).fetchone()
    provenance = (
        json.loads(metadata[0])
        if metadata
        else {
            "review_state": "needs-review",
            "domain_id": "legacy" if row["tier"] == "domain" else None,
        }
    )
    state = reuse_state(
        provenance["review_state"], record["source_refs"], cwd or Path.cwd()
    )
    record["provenance"] = {**provenance, "reuse_state": state}
    return record


def get(
    connection: sqlite3.Connection,
    memory_id: str,
    *,
    current_only: bool = False,
    cwd: Path | None = None,
) -> dict[str, object] | None:
    row = _current(connection, memory_id)
    if row is None:
        return None
    record = _view(connection, row, cwd)
    return (
        None
        if current_only
        and (
            record["eligibility"] != "eligible"
            or record["provenance"]["reuse_state"] != "current"
        )
        else record
    )


def history(
    connection: sqlite3.Connection, memory_id: str, limit: int
) -> list[dict[str, object]]:
    rows = connection.execute(
        "SELECT * FROM revisions WHERE memory_id = ? ORDER BY revision DESC LIMIT ?",
        (memory_id, max(1, min(limit, MAX_HISTORY))),
    )
    return [{**_view(connection, row), "historical": True} for row in rows]


def current_records(
    connection: sqlite3.Connection, tier: str | None, everything: bool
) -> list[dict[str, object]]:
    rows = connection.execute(
        "SELECT r.* FROM revisions r JOIN (SELECT memory_id, max(revision) AS top"
        " FROM revisions GROUP BY memory_id) c"
        " ON r.memory_id = c.memory_id AND r.revision = c.top ORDER BY r.memory_id"
    )
    records = [
        _view(connection, row) for row in rows if tier is None or row["tier"] == tier
    ]
    return [
        r
        for r in records
        if everything
        or (
            r["eligibility"] == "eligible"
            and r["provenance"]["reuse_state"] == "current"
        )
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
            "tier_body_bytes": TIER_BODY_BYTES,
            "domain_body_bytes": MAX_DOMAIN_BODY_BYTES,
            "max_metadata_bytes": MAX_METADATA_BYTES,
            "max_total_metadata_bytes": MAX_TOTAL_METADATA_BYTES,
            "max_conflicts": MAX_CONFLICTS,
            "database_page_bytes": MAX_DATABASE_BYTES,
            "journal_backup_temporary_bytes": MAX_DATABASE_BYTES,
        },
        "conflicts": connection.execute("SELECT count(*) FROM conflicts").fetchone()[0],
        "metadata_bytes": _metadata_bytes(connection),
        "conflict_body_bytes": connection.execute(
            "SELECT coalesce(sum(length(CAST(body AS BLOB))),0) FROM conflicts"
        ).fetchone()[0],
        "sqlite_version": sqlite3.sqlite_version,
        "database_page_limit": connection.execute("PRAGMA max_page_count").fetchone()[
            0
        ],
    }


def _metadata_bytes(connection: sqlite3.Connection) -> int:
    revision_bytes = sum(
        sum(len(str(row[c]).encode()) for c in COLUMNS if c != "body")
        for row in connection.execute("SELECT * FROM revisions")
    )
    sidecar_bytes = connection.execute(
        "SELECT coalesce(sum(length(CAST(metadata AS BLOB))+256),0) FROM (SELECT metadata FROM provenance UNION ALL SELECT metadata FROM conflicts)"
    ).fetchone()[0]
    return revision_bytes + sidecar_bytes


def _has_room(
    connection: sqlite3.Connection,
    metadata: str,
    size: int,
    tier: str,
    domain_id: str | None,
    conflict: bool = False,
) -> bool:
    rows = connection.execute(
        "SELECT tier, body, p.metadata FROM revisions r LEFT JOIN provenance p USING(memory_id,revision)"
    ).fetchall()
    conflicts = connection.execute("SELECT body, metadata FROM conflicts").fetchall()
    bodies = [(r["tier"], r["body"], json.loads(r["metadata"] or "{}")) for r in rows]
    bodies += [
        (json.loads(r["metadata"])["tier"], r["body"], json.loads(r["metadata"]))
        for r in conflicts
    ]
    # Count a conservative envelope allowance as well as duplicated SQL metadata.
    metadata_size = 2 * len(metadata.encode()) + 512
    pages = connection.execute("PRAGMA page_count").fetchone()[0]
    page_size = connection.execute("PRAGMA page_size").fetchone()[0]
    return (
        pages * page_size <= MAX_DATABASE_BYTES
        and size <= MAX_BODY_BYTES
        and metadata_size <= MAX_METADATA_BYTES
        and _metadata_bytes(connection) + metadata_size <= MAX_TOTAL_METADATA_BYTES
        and (conflict or len(rows) + 1 <= MAX_REVISIONS)
        and (not conflict or len(conflicts) + 1 <= MAX_CONFLICTS)
        and sum(len(b.encode()) for _, b, _ in bodies) + size <= MAX_TOTAL_BODY_BYTES
        and sum(len(b.encode()) for t, b, _ in bodies if t == tier) + size
        <= TIER_BODY_BYTES[tier]
        and (
            tier != "domain"
            or sum(
                len(b.encode())
                for t, b, m in bodies
                if t == tier and m.get("domain_id", "legacy") == domain_id
            )
            + size
            <= MAX_DOMAIN_BODY_BYTES
        )
    )


def put(
    connection: sqlite3.Connection,
    *,
    memory_id: str,
    expected_revision: int,
    workspace_id: str,
    tier: str,
    owner: str,
    body: str,
    source_refs: list[object],
    sensitivity: str = "internal",
    eligibility: str = "eligible",
    request_key: str | None = None,
    review_state: str = "candidate",
    domain_id: str | None = None,
    cwd: Path | None = None,
) -> int:
    size = len(body.encode("utf-8"))
    if (
        not 1 <= len(memory_id) <= 128
        or expected_revision < 0
        or tier not in TIERS
        or sensitivity not in SENSITIVITY
        or eligibility not in ELIGIBILITY
        or review_state not in REVIEW_STATES
        or not owner
        or len(owner) > 128
        or not workspace_id
        or len(workspace_id) > 4096
        or (request_key is not None and not 1 <= len(request_key) <= 128)
        or (
            domain_id is not None
            and (tier != "domain" or not 1 <= len(domain_id) <= 128)
        )
    ):
        raise MemoryStoreError(
            EXIT_UNAVAILABLE, "MEMORY_INVALID: invalid record metadata"
        )
    domain_id = (domain_id or "legacy") if tier == "domain" else None
    metadata = json.dumps(
        dict(
            review_state=review_state,
            domain_id=domain_id,
            tier=tier,
            owner=owner,
            source_refs=source_refs,
            sensitivity=sensitivity,
            eligibility=eligibility,
            workspace_id=workspace_id,
            memory_id=memory_id,
            expected_revision=expected_revision,
            request_key=request_key,
        ),
        sort_keys=True,
        ensure_ascii=False,
        separators=(",", ":"),
    )
    fingerprint = hashlib.sha256((metadata + "\0" + body).encode()).hexdigest()
    try:
        # The write lock makes revision, identity and quota checks atomic.
        connection.execute("BEGIN IMMEDIATE")
        try:
            row = _current(connection, memory_id)
            current = 0 if row is None else row["revision"]
            prior = (
                None
                if request_key is None
                else connection.execute(
                    "SELECT memory_id, revision, fingerprint FROM provenance WHERE request_key=?",
                    (request_key,),
                ).fetchone()
            )
            if prior is not None and prior["fingerprint"] == fingerprint:
                connection.execute("COMMIT")
                return prior["revision"]
            if current != expected_revision or prior is not None:
                stored = False
                if _has_room(connection, metadata, size, tier, domain_id, True):
                    try:
                        connection.execute(
                            "INSERT INTO conflicts (memory_id,expected_revision,current_revision,metadata,body) VALUES (?,?,?,?,?)",
                            (memory_id, expected_revision, current, metadata, body),
                        )
                        connection.execute("COMMIT")
                        stored = True
                    except sqlite3.OperationalError as error:
                        if "full" not in str(error).lower():
                            raise
                if connection.in_transaction:
                    connection.execute("ROLLBACK")
                raise MemoryStoreError(
                    EXIT_CONFLICT,
                    f"MEMORY_REVISION_CONFLICT: {memory_id} is at revision {current}, not {expected_revision}",
                    stored=stored,
                    current_revision=current,
                    expected_revision=expected_revision,
                    reason="request-identity"
                    if prior is not None
                    else "stale-revision",
                )
            if not _has_room(connection, metadata, size, tier, domain_id):
                raise MemoryStoreError(
                    EXIT_CAPACITY, "MEMORY_CAPACITY_EXCEEDED: store limit reached"
                )
            if (
                review_state == "current"
                and reuse_state(review_state, source_refs, cwd or Path.cwd())
                != "current"
            ):
                raise MemoryStoreError(
                    EXIT_UNAVAILABLE,
                    "MEMORY_INVALID: current requires reviewed, matching source pins",
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
            connection.execute(
                "INSERT INTO provenance (memory_id,revision,metadata,request_key,fingerprint) VALUES (?,?,?,?,?)",
                (memory_id, current + 1, metadata, request_key, fingerprint),
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
    return current + 1


def backup(connection: sqlite3.Connection, output: Path) -> None:
    store = Path(connection.execute("PRAGMA database_list").fetchone()[2])
    descriptor = os.open(store, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        try:
            fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as error:
            raise MemoryStoreError(
                EXIT_BACKUP,
                "MEMORY_BACKUP_FAILED: another backup is running; previous backup kept",
            ) from error
        _backup(connection, output)
    finally:
        os.close(descriptor)


def _backup(connection: sqlite3.Connection, output: Path) -> None:
    output = output.absolute()
    store = Path(connection.execute("PRAGMA database_list").fetchone()[2]).resolve()
    if output.resolve() in {
        store,
        store.with_name(store.name + "-journal"),
        store.with_name(store.name + "-wal"),
    }:
        raise MemoryStoreError(
            EXIT_BACKUP, "MEMORY_BACKUP_FAILED: the output is the store itself"
        )
    if output.parent.resolve() != output.parent or not output.parent.is_dir():
        raise MemoryStoreError(
            EXIT_BACKUP, f"MEMORY_BACKUP_FAILED: {output.parent} is not a directory"
        )
    directory = output.parent.stat()
    if directory.st_uid != os.geteuid():
        raise MemoryStoreError(
            EXIT_BACKUP, f"MEMORY_BACKUP_FAILED: {output.parent} is not owned by you"
        )
    if stat.S_IMODE(directory.st_mode) & 0o077:
        raise MemoryStoreError(
            EXIT_BACKUP, f"MEMORY_BACKUP_FAILED: {output.parent} is not 0700"
        )
    temporary = output.with_name(f".{output.name}.tmp")
    try:
        if store.stat().st_size > MAX_DATABASE_BYTES:
            raise OSError("store exceeds database byte ceiling")
        if output.is_symlink():
            raise OSError("backup output is a symbolic link")
        temporary.unlink(missing_ok=True)
        # The file exists as 0600 before SQLite writes a byte into it, and a
        # link planted at this name is refused rather than followed.
        _create_private(temporary)
        target = sqlite3.connect(temporary)
        try:
            connection.backup(target)
            if target.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
                raise sqlite3.DatabaseError("backup failed integrity_check")
            if temporary.stat().st_size > MAX_DATABASE_BYTES:
                raise sqlite3.DatabaseError("backup exceeds database byte ceiling")
            _validate_snapshot(target)
        finally:
            target.close()
        os.replace(temporary, output)
    except (OSError, sqlite3.Error, MemoryStoreError) as error:
        temporary.unlink(missing_ok=True)
        temporary.with_name(temporary.name + "-journal").unlink(missing_ok=True)
        raise MemoryStoreError(
            EXIT_BACKUP, f"MEMORY_BACKUP_FAILED: {error}; previous backup kept"
        ) from error


def _schema(connection: sqlite3.Connection) -> set[tuple[str, ...]]:
    return set(
        connection.execute("SELECT type, name, tbl_name, sql FROM sqlite_master")
    )


def _validate_snapshot(connection: sqlite3.Connection) -> None:
    expected = sqlite3.connect(":memory:")
    try:
        expected.execute(SCHEMA)
        legacy = _schema(expected)
        for statement in SIDECARS:
            expected.execute(statement)
        observed = _schema(connection)
        if observed not in (legacy, _schema(expected)):
            raise MemoryStoreError(
                EXIT_BACKUP,
                "MEMORY_RESTORE_REFUSED: backup schema differs from the store schema",
            )
        if connection.execute(
            "SELECT 1 FROM revisions WHERE schema_version NOT IN (1,2) OR revision < 1 LIMIT 1"
        ).fetchone():
            raise MemoryStoreError(
                EXIT_BACKUP, "MEMORY_BACKUP_FAILED: invalid revision identity"
            )
        if (
            observed != legacy
            and connection.execute(
                "SELECT 1 FROM provenance p LEFT JOIN revisions r USING(memory_id,revision) WHERE r.memory_id IS NULL "
                "UNION ALL SELECT 1 FROM revisions r LEFT JOIN provenance p USING(memory_id,revision) WHERE r.schema_version=2 AND p.memory_id IS NULL LIMIT 1"
            ).fetchone()
        ):
            raise MemoryStoreError(
                EXIT_BACKUP, "MEMORY_BACKUP_FAILED: missing revision provenance"
            )
    finally:
        expected.close()


def restore(source: Path, path: Path) -> None:
    """Publish a complete restored store exclusively; never replace a live store."""
    if (
        source.is_symlink()
        or source.parent.resolve() != source.parent.absolute()
        or not source.is_file()
        or source.stat().st_size > MAX_DATABASE_BYTES
    ):
        raise MemoryStoreError(
            EXIT_BACKUP, "MEMORY_RESTORE_REFUSED: unsafe backup input"
        )
    try:
        backup_db = sqlite3.connect(source.absolute().as_uri() + "?mode=ro", uri=True)
    except sqlite3.Error as error:
        raise MemoryStoreError(
            EXIT_BACKUP, f"MEMORY_RESTORE_REFUSED: cannot open backup: {error}"
        ) from error
    try:
        if backup_db.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
            raise MemoryStoreError(
                EXIT_BACKUP, "MEMORY_RESTORE_REFUSED: backup failed integrity_check"
            )
        _validate_snapshot(backup_db)
        _private_directory(path.parent)
        if path.exists() or path.is_symlink():
            raise MemoryStoreError(
                EXIT_CONFLICT, f"MEMORY_RESTORE_REFUSED: {path} exists"
            )
        descriptor, name = tempfile.mkstemp(
            prefix=f".{path.name}.restore-", dir=path.parent
        )
        os.close(descriptor)
        temporary = Path(name)
        try:
            # mkstemp creates the copy privately before SQLite opens it.
            target = sqlite3.connect(temporary)
            try:
                backup_db.backup(target)
            finally:
                target.close()
            try:
                os.link(temporary, path, follow_symlinks=False)
            except FileExistsError as error:
                raise MemoryStoreError(
                    EXIT_CONFLICT, f"MEMORY_RESTORE_REFUSED: {path} exists"
                ) from error
        finally:
            temporary.unlink(missing_ok=True)
            temporary.with_name(temporary.name + "-journal").unlink(missing_ok=True)
    except (OSError, sqlite3.Error) as error:
        raise MemoryStoreError(
            EXIT_BACKUP, f"MEMORY_RESTORE_FAILED: {error}; no store was left"
        ) from error
    finally:
        backup_db.close()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    commands = parser.add_subparsers(dest="command", required=True)
    get_parser = commands.add_parser("get")
    get_parser.add_argument("memory_id")
    get_parser.add_argument(
        "--historical",
        action="store_true",
        help="include preserved, noncurrent context",
    )
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
    put_parser.add_argument("--request-key")
    put_parser.add_argument(
        "--review-state", choices=REVIEW_STATES, default="candidate"
    )
    put_parser.add_argument("--domain-id")
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
        existing_identity = connection.execute(
            "SELECT workspace_id FROM revisions LIMIT 1"
        ).fetchone()
        workspace_id = (
            existing_identity[0] if existing_identity else path.parent.parent.as_posix()
        )
        result: object
        if arguments.command == "get":
            result = get(
                connection, arguments.memory_id, current_only=not arguments.historical
            )
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
                body=sys.stdin.read(MAX_BODY_BYTES + 1),
                source_refs=[
                    json.loads(ref) if ref.startswith("{") else ref
                    for ref in arguments.source_ref
                ],
                sensitivity=arguments.sensitivity,
                request_key=arguments.request_key,
                review_state=arguments.review_state,
                domain_id=arguments.domain_id,
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
                review_state="withdrawn"
                if arguments.eligibility == "ineligible"
                else "candidate",
                domain_id=row["provenance"]["domain_id"],
            )
            result = {"memory_id": arguments.memory_id, "revision": revision}
    except MemoryStoreError as error:
        print(error, file=sys.stderr)
        if error.details:
            print(json.dumps(error.details, sort_keys=True), file=sys.stderr)
        return error.code
    except (OSError, sqlite3.Error, ValueError, TypeError) as error:
        print(f"MEMORY_UNAVAILABLE: {type(error).__name__}", file=sys.stderr)
        return EXIT_UNAVAILABLE
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
