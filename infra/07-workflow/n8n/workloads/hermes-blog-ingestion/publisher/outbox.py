"""Private SQLite snapshots, immutable request binding and audited transitions."""

import fcntl
import hashlib
import json
import math
import os
import re
import sqlite3
import stat
import time
from contextlib import contextmanager
from pathlib import Path

from .files import InputError, open_directory

TRANSITIONS = {
    "awaiting_contract": {"pending", "failed"},
    "pending": {"sending", "failed"},
    "sending": {"delivered", "uncertain", "failed", "pending"},
    "uncertain": {"delivered", "pending", "failed", "uncertain"},
    "delivered": set(),
    "failed": set(),
}


class OutboxError(ValueError):
    """Value-free operational diagnostic."""


def _sha(raw):
    return hashlib.sha256(raw).hexdigest()


def valid_gateway_report_id(value):
    """Accept only the published Gateway receipt identifier format."""
    return isinstance(value, str) and re.fullmatch(r"[a-f0-9-]{36}", value) is not None


def _snapshot_digest(snapshot):
    digest = hashlib.sha256()
    values = (
        snapshot.job_id.encode(),
        snapshot.run_id.encode(),
        snapshot.candidate,
        snapshot.source_ref.encode(),
        snapshot.source,
        *(part for ref, raw in snapshot.ideas for part in (ref.encode(), raw)),
    )
    for value in values:
        digest.update(len(value).to_bytes(8, "big"))
        digest.update(value)
    return digest.hexdigest()


def _check_private(info, directory=False):
    valid_type = stat.S_ISDIR(info.st_mode) if directory else stat.S_ISREG(info.st_mode)
    if (
        not valid_type
        or info.st_uid != os.getuid()
        or stat.S_IMODE(info.st_mode) != (0o700 if directory else 0o600)
        or (not directory and info.st_nlink != 1)
    ):
        raise OutboxError("unsafe_outbox")


def _private_file(directory, name):
    flags = os.O_RDWR | os.O_NOFOLLOW | os.O_CLOEXEC | os.O_NONBLOCK
    try:
        descriptor = os.open(
            name, flags | os.O_CREAT | os.O_EXCL, 0o600, dir_fd=directory
        )
    except FileExistsError:
        descriptor = os.open(name, flags, dir_fd=directory)
    try:
        _check_private(os.fstat(descriptor))
    except BaseException:
        os.close(descriptor)
        raise
    return descriptor


class Outbox:
    def __init__(self, path):
        path = Path(path).absolute()
        self._db, self._dir, self._lock_fd, self._locked = None, None, None, False
        if path.name in ("", ".", ".."):
            raise OutboxError("unsafe_outbox")
        # /tmp carries a host harness marker; its private synthetic subdirectories
        # are explicitly admitted. Nested repositories remain forbidden.
        if any(
            (parent / ".git").exists()
            for parent in path.parents
            if parent != Path("/tmp")
        ):
            raise OutboxError("repository_outbox")
        try:
            with open_directory(path.parent.parent) as parent:
                try:
                    os.mkdir(path.parent.name, 0o700, dir_fd=parent)
                except FileExistsError:
                    pass
            with open_directory(path.parent) as directory:
                _check_private(os.fstat(directory), directory=True)
                for suffix in ("-journal", "-wal", "-shm"):
                    try:
                        info = os.stat(
                            path.name + suffix, dir_fd=directory, follow_symlinks=False
                        )
                    except FileNotFoundError:
                        continue
                    _check_private(info)
                self._dir = os.dup(directory)
                descriptor = _private_file(directory, path.name)
                try:
                    inode = os.fstat(descriptor)
                    self._db = sqlite3.connect(
                        f"/proc/self/fd/{self._dir}/{path.name}", timeout=5
                    )
                    current = os.stat(
                        path.name, dir_fd=directory, follow_symlinks=False
                    )
                    if (inode.st_dev, inode.st_ino) != (current.st_dev, current.st_ino):
                        raise OutboxError("unsafe_outbox")
                finally:
                    os.close(descriptor)
                self._lock_fd = _private_file(directory, ".delivery.lock")
            self._db.row_factory = sqlite3.Row
            self._db.execute("PRAGMA journal_mode=DELETE")
            self._db.execute("PRAGMA synchronous=FULL")
            self._db.executescript("""
                CREATE TABLE IF NOT EXISTS records (
                    job_id TEXT, run_id TEXT, candidate BLOB NOT NULL, source_ref TEXT NOT NULL,
                    source BLOB NOT NULL, candidate_sha256 TEXT NOT NULL, source_sha256 TEXT NOT NULL,
                    snapshot_sha256 TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'awaiting_contract',
                    attempts INTEGER NOT NULL DEFAULT 0, next_attempt REAL NOT NULL DEFAULT 0,
                    contract_revision TEXT, request_body BLOB, body_sha256 TEXT, receipt TEXT,
                    destination TEXT,
                    PRIMARY KEY(job_id,run_id));
                CREATE UNIQUE INDEX IF NOT EXISTS source_identity
                    ON records(job_id,source_ref,source_sha256);
                CREATE TABLE IF NOT EXISTS ideas (
                    job_id TEXT, run_id TEXT, ordinal INTEGER, ref TEXT, content BLOB,
                    PRIMARY KEY(job_id,run_id,ordinal));
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY, job_id TEXT, run_id TEXT, status TEXT,
                    code TEXT, digest TEXT, created REAL);
                CREATE TABLE IF NOT EXISTS conflicts (
                    job_id TEXT NOT NULL, run_id TEXT NOT NULL,
                    code TEXT NOT NULL, digest TEXT NOT NULL,
                    PRIMARY KEY(job_id,run_id,code,digest));
                INSERT OR IGNORE INTO conflicts(job_id,run_id,code,digest)
                    SELECT job_id,run_id,code,digest FROM events
                    WHERE status='conflict'
                      AND code IN ('identity_conflict','source_identity_conflict')
                      AND job_id IS NOT NULL AND run_id IS NOT NULL AND digest IS NOT NULL;
            """)
            columns = {
                row["name"] for row in self._db.execute("PRAGMA table_info(records)")
            }
            if "endpoint_sha256" not in columns:
                self._db.execute("ALTER TABLE records ADD COLUMN endpoint_sha256 TEXT")
                self._db.commit()
        except (OSError, sqlite3.Error, InputError):
            self.close()
            raise OutboxError("unsafe_outbox") from None
        except BaseException:
            self.close()
            raise

    def close(self):
        if self._db is not None:
            self._db.close()
            self._db = None
        for name in ("_lock_fd", "_dir"):
            descriptor = getattr(self, name, None)
            if descriptor is not None:
                os.close(descriptor)
                setattr(self, name, None)

    @contextmanager
    def _transaction(self):
        try:
            self._db.execute("BEGIN IMMEDIATE")
            yield
            self._db.commit()
        except BaseException:
            self._db.rollback()
            raise

    def _event(self, key, status, code=None, digest=None):
        self._db.execute(
            "INSERT INTO events(job_id,run_id,status,code,digest,created) VALUES(?,?,?,?,?,?)",
            (*key, status, code, digest, time.time()),
        )

    def _conflict(self, key, code, digest):
        inserted = self._db.execute(
            "INSERT OR IGNORE INTO conflicts(job_id,run_id,code,digest) VALUES(?,?,?,?)",
            (*key, code, digest),
        ).rowcount
        if inserted:
            self._event(key, "conflict", code, digest)

    def stage(self, snapshot):
        key = (snapshot.job_id, snapshot.run_id)
        digest = _snapshot_digest(snapshot)
        with self._transaction():
            prior = self._db.execute(
                "SELECT snapshot_sha256 FROM records WHERE job_id=? AND run_id=?", key
            ).fetchone()
            if prior:
                if prior["snapshot_sha256"] == digest:
                    return "duplicate"
                self._conflict(key, "identity_conflict", digest)
                return "conflict"
            prior_source = self._db.execute(
                "SELECT run_id FROM records WHERE job_id=? AND source_ref=? AND source_sha256=?",
                (snapshot.job_id, snapshot.source_ref, _sha(snapshot.source)),
            ).fetchone()
            if prior_source:
                self._conflict(key, "source_identity_conflict", digest)
                return "conflict"
            self._db.execute(
                """INSERT INTO records
                (job_id,run_id,candidate,source_ref,source,candidate_sha256,source_sha256,snapshot_sha256)
                VALUES(?,?,?,?,?,?,?,?)""",
                (
                    *key,
                    snapshot.candidate,
                    snapshot.source_ref,
                    snapshot.source,
                    _sha(snapshot.candidate),
                    _sha(snapshot.source),
                    digest,
                ),
            )
            self._db.executemany(
                "INSERT INTO ideas VALUES(?,?,?,?,?)",
                (
                    (*key, index, ref, raw)
                    for index, (ref, raw) in enumerate(snapshot.ideas)
                ),
            )
            self._event(key, "awaiting_contract", "staged", digest)
        return "staged"

    def get(self, key):
        row = self._db.execute(
            "SELECT * FROM records WHERE job_id=? AND run_id=?", key
        ).fetchone()
        if row is None:
            raise OutboxError("record_missing")
        result = dict(row)
        result["ideas"] = tuple(
            (r["ref"], r["content"])
            for r in self._db.execute(
                "SELECT ref,content FROM ideas WHERE job_id=? AND run_id=? ORDER BY ordinal",
                key,
            )
        )
        if result["receipt"] is not None:
            result["receipt"] = json.loads(result["receipt"])
        return result

    def keys(self, status=None):
        if status is None:
            rows = self._db.execute(
                "SELECT job_id,run_id FROM records ORDER BY job_id,run_id"
            )
        else:
            rows = self._db.execute(
                "SELECT job_id,run_id FROM records WHERE status=? ORDER BY job_id,run_id",
                (status,),
            )
        return [tuple(row) for row in rows]

    def counts(self):
        counts = dict(
            self._db.execute("SELECT status,count(*) FROM records GROUP BY status")
        )
        conflicts = self._db.execute("SELECT count(*) FROM conflicts").fetchone()[0]
        if conflicts:
            counts["conflict"] = conflicts
        return counts

    def events(self, key):
        return [
            dict(row)
            for row in self._db.execute(
                "SELECT status,code,digest,created FROM events WHERE job_id=? AND run_id=? ORDER BY id",
                key,
            )
        ]

    def bind_request(
        self,
        key,
        contract_revision,
        body,
        *,
        destination="unconfigured",
        endpoint_sha256=None,
    ):
        if not isinstance(body, bytes) or not body or len(body) > 32 * 1024 * 1024:
            raise OutboxError("invalid_request")
        if not isinstance(contract_revision, str) or not re.fullmatch(
            r"[A-Za-z0-9._:/@+-]{1,256}", contract_revision
        ):
            raise OutboxError("invalid_revision")
        if not isinstance(destination, str) or not re.fullmatch(
            r"[a-z][a-z0-9_]{0,63}", destination
        ):
            raise OutboxError("invalid_destination")
        if endpoint_sha256 is not None and (
            not isinstance(endpoint_sha256, str)
            or not re.fullmatch(r"[a-f0-9]{64}", endpoint_sha256)
        ):
            raise OutboxError("invalid_endpoint_binding")
        with self._transaction():
            row = self.get(key)
            if row["request_body"] is not None:
                if (
                    row["contract_revision"] != contract_revision
                    or row["request_body"] != body
                    or row["destination"] != destination
                    or row["endpoint_sha256"] != endpoint_sha256
                ):
                    raise OutboxError("request_conflict")
                return row["request_body"]
            self._db.execute(
                "UPDATE records SET contract_revision=?,request_body=?,body_sha256=?,destination=?,endpoint_sha256=? WHERE job_id=? AND run_id=?",
                (
                    contract_revision,
                    body,
                    _sha(body),
                    destination,
                    endpoint_sha256,
                    *key,
                ),
            )
            self._event(key, row["status"], "request_bound", _sha(body))
        return body

    def transition(
        self,
        key,
        expected,
        target,
        *,
        attempts=None,
        next_attempt=None,
        code=None,
        receipt=None,
    ):
        if target not in TRANSITIONS.get(expected, set()):
            raise OutboxError("invalid_transition")
        if code is not None and (
            not isinstance(code, str) or not re.fullmatch(r"[a-z_]{1,64}", code)
        ):
            raise OutboxError("invalid_code")
        if attempts is not None and (type(attempts) is not int or attempts < 0):
            raise OutboxError("invalid_attempts")
        if next_attempt is not None and (
            not isinstance(next_attempt, (int, float))
            or not math.isfinite(next_attempt)
            or next_attempt < 0
        ):
            raise OutboxError("invalid_deadline")
        with self._transaction():
            row = self.get(key)
            if row["status"] != expected:
                return False
            if receipt is not None or target == "delivered":
                required = dict(
                    job_id=key[0],
                    run_id=key[1],
                    source_sha256=row["source_sha256"],
                    body_sha256=row["body_sha256"],
                    persisted=True,
                )
                if isinstance(receipt, dict) and "gateway_report_id" in receipt:
                    if not valid_gateway_report_id(receipt["gateway_report_id"]):
                        raise OutboxError("invalid_receipt")
                    required["gateway_report_id"] = receipt["gateway_report_id"]
                if (
                    not isinstance(receipt, dict)
                    or receipt != required
                    or receipt.get("persisted") is not True
                    or row["request_body"] is None
                ):
                    raise OutboxError("invalid_receipt")
            receipt_json = (
                None
                if receipt is None
                else json.dumps(receipt, separators=(",", ":"), allow_nan=False)
            )
            self._db.execute(
                """UPDATE records SET status=?,attempts=?,next_attempt=?,receipt=?
                WHERE job_id=? AND run_id=? AND status=?""",
                (
                    target,
                    row["attempts"] if attempts is None else attempts,
                    row["next_attempt"] if next_attempt is None else next_attempt,
                    json.dumps(row["receipt"])
                    if receipt_json is None and row["receipt"] is not None
                    else receipt_json,
                    *key,
                    expected,
                ),
            )
            self._event(key, target, code)
        return True

    @contextmanager
    def delivery_lock(self):
        if self._locked:
            raise OutboxError("delivery_locked")
        try:
            fcntl.flock(self._lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise OutboxError("delivery_locked") from None
        self._locked = True
        try:
            yield
        finally:
            self._locked = False
            fcntl.flock(self._lock_fd, fcntl.LOCK_UN)

    def recover_sending(self):
        if not self._locked:
            raise OutboxError("delivery_lock_required")
        keys = self.keys("sending")
        for key in keys:
            self.transition(key, "sending", "uncertain", code="crash_recovered")
        return len(keys)
