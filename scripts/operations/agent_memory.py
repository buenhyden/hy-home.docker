#!/usr/bin/env python3
"""Shared agent memory: one SQLite store for every worktree and provider."""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import sqlite3
import subprocess
import sys
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts.lib.ops.memory_capacity import (  # noqa: E402
    CapacityError,
    MemoryCapacity,
    operation_fingerprint,
)
from scripts.lib.ops.memory_sources import (  # noqa: E402
    REVIEW_STATES,
    reuse_state,
    run_git,
)

SCHEMA_VERSION = 3
STORE_DIRECTORY = ".workspace-memory"
STORE_NAME = "memory.sqlite3"
TIERS = ("short-term", "long-term", "domain")
# D06 record kind is a meaning axis; the tier stays the retention budget axis.
KINDS = ("session-context", "decision", "experience")
TIER_KIND = {
    "short-term": "session-context",
    "long-term": "experience",
    "domain": "experience",
}
INITIAL_BASELINE = "initial"
MAX_SUPERSEDES = 16
MAX_ERASE = 100
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
META = (
    "CREATE TABLE IF NOT EXISTS store_meta (key TEXT PRIMARY KEY, value TEXT NOT NULL)"
)
SIDECARS = (
    "CREATE TABLE IF NOT EXISTS provenance (memory_id TEXT NOT NULL, revision INTEGER NOT NULL,"
    " metadata TEXT NOT NULL, request_key TEXT UNIQUE, fingerprint TEXT NOT NULL,"
    " PRIMARY KEY (memory_id, revision))",
    "CREATE TABLE IF NOT EXISTS conflicts (conflict_id INTEGER PRIMARY KEY, memory_id TEXT NOT NULL,"
    " expected_revision INTEGER NOT NULL, current_revision INTEGER NOT NULL, metadata TEXT NOT NULL, body TEXT NOT NULL)",
)


MIGRATION_REQUIRED = (
    "MEMORY_MIGRATION_REQUIRED: run `agent_memory.py migrate` once to add schema 3"
)


class MemoryStoreError(Exception):
    """A refused memory operation with its CLI exit code."""

    def __init__(self, code: int, message: str, **details: object) -> None:
        super().__init__(message)
        self.code = code
        self.details = details


def _common_dir(cwd: Path) -> Path | None:
    try:
        common = os.fsdecode(
            run_git(
                ("rev-parse", "--path-format=absolute", "--git-common-dir"), cwd
            ).stdout.strip()
        )
    except (
        OSError,
        subprocess.CalledProcessError,
        subprocess.TimeoutExpired,
        UnicodeError,
    ):
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
    connection.execute("BEGIN IMMEDIATE")
    try:
        new_store = not _table_exists(connection, "revisions")
        connection.execute(SCHEMA)
        for statement in SIDECARS:
            connection.execute(statement)
        # Only a brand-new store starts at schema 3; an existing one migrates
        # through the explicit `migrate` command.
        if new_store:
            _initialize_meta(connection)
        connection.execute("COMMIT")
    except BaseException:
        connection.execute("ROLLBACK")
        raise
    return connection


def _table_exists(connection: sqlite3.Connection, name: str) -> bool:
    return (
        connection.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (name,)
        ).fetchone()
        is not None
    )


def _initialize_meta(connection: sqlite3.Connection) -> None:
    connection.execute(META)
    connection.executemany(
        "INSERT OR IGNORE INTO store_meta VALUES (?, ?)",
        (("schema_version", str(SCHEMA_VERSION)), ("baseline_id", INITIAL_BASELINE)),
    )


def _meta(connection: sqlite3.Connection) -> dict[str, str] | None:
    if not _table_exists(connection, "store_meta"):
        return None
    return dict(connection.execute("SELECT key, value FROM store_meta").fetchall())


def current_baseline(connection: sqlite3.Connection) -> str:
    return (_meta(connection) or {}).get("baseline_id", INITIAL_BASELINE)


def _write(connection: sqlite3.Connection, action):
    """Run one short write transaction and map SQLite failures to exit codes."""
    try:
        connection.execute("BEGIN IMMEDIATE")
        try:
            result = action()
            connection.execute("COMMIT")
            return result
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


def migrate(connection: sqlite3.Connection) -> dict[str, object]:
    """Add schema-3 store metadata; existing revisions stay byte-for-byte."""

    def action():
        before = _meta(connection)
        _initialize_meta(connection)
        return {
            "schema_version": SCHEMA_VERSION,
            "baseline_id": current_baseline(connection),
            "migrated": before is None,
        }

    return _write(connection, action)


def cutover(
    connection: sqlite3.Connection, *, expected: str, baseline_id: str
) -> dict[str, object]:
    """Move the store to a new baseline; earlier records leave default reads."""
    if not 1 <= len(baseline_id) <= 128 or baseline_id == expected:
        raise MemoryStoreError(EXIT_UNAVAILABLE, "MEMORY_INVALID: invalid baseline")

    def action():
        meta = _meta(connection)
        if meta is None:
            raise MemoryStoreError(EXIT_UNAVAILABLE, MIGRATION_REQUIRED)
        if meta["baseline_id"] != expected:
            raise MemoryStoreError(
                EXIT_CONFLICT,
                f"MEMORY_REVISION_CONFLICT: baseline is {meta['baseline_id']}, not {expected}",
            )
        connection.execute(
            "UPDATE store_meta SET value=? WHERE key='baseline_id'", (baseline_id,)
        )
        return {"baseline_id": baseline_id, "previous_baseline_id": expected}

    return _write(connection, action)


def erase(connection: sqlite3.Connection, memory_ids: list[str]) -> dict[str, object]:
    """Delete every revision, provenance row and conflict of the named records."""
    ids = sorted(set(memory_ids))
    if not ids or len(ids) > MAX_ERASE or any(not 1 <= len(i) <= 128 for i in ids):
        raise MemoryStoreError(EXIT_UNAVAILABLE, "MEMORY_INVALID: invalid erase set")
    # Overwrite freed pages; the journal, filesystem and SSD may still hold copies.
    connection.execute("PRAGMA secure_delete = ON")
    marks = ",".join("?" * len(ids))

    def action():
        found = [
            row[0]
            for row in connection.execute(
                f"SELECT DISTINCT memory_id FROM revisions WHERE memory_id IN ({marks})",
                ids,
            )
        ]
        counts = {
            table: connection.execute(
                f"DELETE FROM {table} WHERE memory_id IN ({marks})", ids
            ).rowcount
            for table in ("revisions", *sorted(_sidecars(connection)))
        }
        return {
            "erased": found,
            "missing": [i for i in ids if i not in found],
            "deleted_rows": counts,
            "residue": "SQLite pages are overwritten; journal, filesystem and"
            " storage-device copies are not proven erased",
        }

    return _write(connection, action)


def _timestamp(value: str | None, name: str) -> str | None:
    if value is None:
        return None
    try:
        parsed = dt.datetime.fromisoformat(value)
    except (TypeError, ValueError):
        parsed = None
    if parsed is None or parsed.tzinfo is None:
        raise MemoryStoreError(
            EXIT_UNAVAILABLE, f"MEMORY_INVALID: {name} needs an ISO time with a zone"
        )
    return parsed.astimezone(dt.UTC).isoformat(timespec="seconds")


def _context(connection: sqlite3.Connection, as_of: str | None) -> dict[str, object]:
    """Baseline, evaluation time and reverse supersession links for one read."""
    baseline = current_baseline(connection)
    superseded_by: dict[str, list[str]] = {}
    if "provenance" in _sidecars(connection):
        rows = connection.execute(
            "SELECT r.memory_id, r.eligibility, p.metadata FROM revisions r"
            " JOIN (SELECT memory_id, max(revision) AS top FROM revisions GROUP BY memory_id) c"
            " ON r.memory_id = c.memory_id AND r.revision = c.top"
            " LEFT JOIN provenance p ON p.memory_id = r.memory_id AND p.revision = r.revision"
        )
        for memory_id, eligibility, metadata in rows:
            meta = json.loads(metadata or "{}")
            if (
                eligibility == "eligible"
                and meta.get("baseline_id", INITIAL_BASELINE) == baseline
            ):
                for target in meta.get("supersedes", []):
                    superseded_by.setdefault(target, []).append(memory_id)
    return {
        "baseline": baseline,
        "as_of": _timestamp(as_of, "as_of")
        or dt.datetime.now(dt.UTC).isoformat(timespec="seconds"),
        "superseded_by": superseded_by,
    }


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
    connection: sqlite3.Connection,
    row: sqlite3.Row,
    cwd: Path | None = None,
    context: dict[str, object] | None = None,
) -> dict[str, object]:
    context = context or _context(connection, None)
    record = _record(row)
    metadata = (
        connection.execute(
            "SELECT metadata FROM provenance WHERE memory_id=? AND revision=?",
            (row["memory_id"], row["revision"]),
        ).fetchone()
        if "provenance" in _sidecars(connection)
        else None
    )
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
    record.update(
        kind=provenance.get("kind") or TIER_KIND[row["tier"]],
        baseline_id=provenance.get("baseline_id", INITIAL_BASELINE),
        observed_at=provenance.get("observed_at") or row["created_at"],
        valid_from=provenance.get("valid_from"),
        valid_until=provenance.get("valid_until"),
        supersedes=list(provenance.get("supersedes", [])),
        invalidated_by=list(context["superseded_by"].get(row["memory_id"], [])),
    )
    # A reviewed record is reusable only in the current baseline, inside its
    # validity window and while no current record supersedes it.
    if state == "current":
        as_of = context["as_of"]
        if record["baseline_id"] != context["baseline"]:
            state = "other-baseline"
        elif record["invalidated_by"]:
            state = "superseded"
        elif (record["valid_from"] and as_of < record["valid_from"]) or (
            record["valid_until"] and as_of >= record["valid_until"]
        ):
            state = "outside-validity"
    record["provenance"] = {**provenance, "reuse_state": state}
    return record


def get(
    connection: sqlite3.Connection,
    memory_id: str,
    *,
    current_only: bool = False,
    cwd: Path | None = None,
    as_of: str | None = None,
) -> dict[str, object] | None:
    row = _current(connection, memory_id)
    if row is None:
        return None
    record = _view(connection, row, cwd, _context(connection, as_of))
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
    context = _context(connection, None)
    return [
        {**_view(connection, row, None, context), "historical": True} for row in rows
    ]


def export_selected(
    connection: sqlite3.Connection, memory_ids: list[str], include_history: bool
) -> list[dict[str, object]]:
    """Export named records, their current revision or every revision."""
    context = _context(connection, None)
    records, missing = [], []
    for memory_id in sorted(set(memory_ids)):
        rows = connection.execute(
            "SELECT * FROM revisions WHERE memory_id = ? ORDER BY revision DESC"
            + ("" if include_history else " LIMIT 1"),
            (memory_id,),
        ).fetchall()
        if not rows:
            missing.append(memory_id)
        records += [_view(connection, row, None, context) for row in rows]
    if missing:
        raise MemoryStoreError(
            1, "MEMORY_NOT_FOUND: no record for " + ", ".join(missing)
        )
    return records


def current_records(
    connection: sqlite3.Connection,
    tier: str | None,
    everything: bool,
    as_of: str | None = None,
) -> list[dict[str, object]]:
    rows = connection.execute(
        "SELECT r.* FROM revisions r JOIN (SELECT memory_id, max(revision) AS top"
        " FROM revisions GROUP BY memory_id) c"
        " ON r.memory_id = c.memory_id AND r.revision = c.top ORDER BY r.memory_id"
    )
    context = _context(connection, as_of)
    records = [
        _view(connection, row, None, context)
        for row in rows
        if tier is None or row["tier"] == tier
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
    sidecars = _sidecars(connection)
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
            "journal_temporary_bytes": MAX_DATABASE_BYTES,
        },
        "conflicts": connection.execute("SELECT count(*) FROM conflicts").fetchone()[0]
        if "conflicts" in sidecars
        else 0,
        "metadata_bytes": _metadata_bytes(connection),
        "conflict_body_bytes": connection.execute(
            "SELECT coalesce(sum(length(CAST(body AS BLOB))),0) FROM conflicts"
        ).fetchone()[0]
        if "conflicts" in sidecars
        else 0,
        "sqlite_version": sqlite3.sqlite_version,
        # The limit every writing connection applies, not this reader's default.
        "database_page_limit": MAX_DATABASE_BYTES
        // connection.execute("PRAGMA page_size").fetchone()[0],
        "database_pages": connection.execute("PRAGMA page_count").fetchone()[0],
        "schema_version": int((_meta(connection) or {}).get("schema_version", 2)),
        "baseline_id": current_baseline(connection),
        "migration_required": _meta(connection) is None,
    }


def conflict_counts(connection: sqlite3.Connection) -> dict[str, int]:
    """Unresolved stored conflicts per record, for recall to flag."""
    if "conflicts" not in _sidecars(connection):
        return {}
    return dict(
        connection.execute(
            "SELECT memory_id, count(*) FROM conflicts GROUP BY memory_id"
        ).fetchall()
    )


def _sidecars(connection: sqlite3.Connection) -> set[str]:
    return {
        row[0]
        for row in connection.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name IN ('provenance','conflicts')"
        )
    }


def _metadata_bytes(connection: sqlite3.Connection) -> int:
    revision_bytes = sum(
        sum(len(str(row[c]).encode()) for c in COLUMNS if c != "body")
        for row in connection.execute("SELECT * FROM revisions")
    )
    tables = _sidecars(connection)
    union = " UNION ALL ".join(
        f"SELECT metadata FROM {table}" for table in sorted(tables)
    )
    sidecar_bytes = (
        connection.execute(
            f"SELECT coalesce(sum(length(CAST(metadata AS BLOB))+256),0) FROM ({union})"
        ).fetchone()[0]
        if union
        else 0
    )
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


def _put(
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
    kind: str | None = None,
    observed_at: str | None = None,
    valid_from: str | None = None,
    valid_until: str | None = None,
    supersedes: list[str] | tuple[str, ...] = (),
    cwd: Path | None = None,
) -> int:
    size = len(body.encode("utf-8"))
    kind = kind or TIER_KIND.get(tier)
    observed_at = _timestamp(observed_at, "observed_at")
    valid_from = _timestamp(valid_from, "valid_from")
    valid_until = _timestamp(valid_until, "valid_until")
    supersedes = sorted(set(supersedes))
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
        or kind not in KINDS
        or (valid_from and valid_until and valid_from >= valid_until)
        or len(supersedes) > MAX_SUPERSEDES
        or any(not 1 <= len(s) <= 128 or s == memory_id for s in supersedes)
    ):
        raise MemoryStoreError(
            EXIT_UNAVAILABLE, "MEMORY_INVALID: invalid record metadata"
        )
    domain_id = (domain_id or "legacy") if tier == "domain" else None
    fields = dict(
        kind=kind,
        observed_at=observed_at,
        valid_from=valid_from,
        valid_until=valid_until,
        supersedes=supersedes,
    )

    def describe(baseline_id: str) -> str:
        return json.dumps(
            dict(
                fields,
                baseline_id=baseline_id,
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

    try:
        # The write lock makes revision, identity and quota checks atomic.
        connection.execute("BEGIN IMMEDIATE")
        try:
            meta = _meta(connection)
            if meta is None:
                raise MemoryStoreError(EXIT_UNAVAILABLE, MIGRATION_REQUIRED)
            # The request digest binds the baseline too, so a retry after a
            # cutover is a different request.
            metadata = describe(meta["baseline_id"])
            fingerprint = hashlib.sha256((metadata + "\0" + body).encode()).hexdigest()
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
            if any(_current(connection, target) is None for target in supersedes):
                raise MemoryStoreError(
                    EXIT_UNAVAILABLE, "MEMORY_INVALID: supersedes an unknown record"
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


def put(connection: sqlite3.Connection, **arguments) -> int:
    path = Path(connection.execute("PRAGMA database_list").fetchone()[2])
    manager = MemoryCapacity(path)
    identity = arguments.get("request_key")
    inputs = {key: value for key, value in arguments.items() if key != "cwd"}
    fingerprint = operation_fingerprint(inputs)
    key = "put:" + (
        hashlib.sha256((identity + fingerprint).encode()).hexdigest()
        if identity
        else uuid.uuid4().hex
    )
    try:
        admission = manager.reserve(key, fingerprint, 0)
        if admission["replay"]:
            if admission["state"] != "completed":
                prior = (
                    None
                    if identity is None
                    else connection.execute(
                        "SELECT revision FROM provenance WHERE request_key=?",
                        (identity,),
                    ).fetchone()
                )
                if prior is None:
                    raise MemoryStoreError(
                        EXIT_BUSY, "MEMORY_STORE_BUSY: unresolved memory operation"
                    )
                revision = _put(connection, **arguments)
                manager.resolve(
                    key,
                    result={"revision": revision},
                    evidence_ref="committed matching memory request provenance",
                )
                return revision
            result = admission["result"]
            if "error_code" in result:
                raise MemoryStoreError(
                    result["error_code"], result["message"], **result["details"]
                )
            return result["revision"]
        try:
            revision = _put(connection, **arguments)
        except MemoryStoreError as error:
            manager.settle(
                key,
                result={
                    "error_code": error.code,
                    "message": str(error),
                    "details": error.details,
                },
            )
            raise
        manager.settle(key, result={"revision": revision})
        return revision
    except CapacityError as error:
        raise MemoryStoreError(EXIT_CAPACITY, str(error)) from error


def main(argv: list[str] | None = None) -> int:
    from scripts.lib.ops.memory_cli import run

    return run(argv, sys.modules[__name__])


if __name__ == "__main__":
    raise SystemExit(main())
