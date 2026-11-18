"""Persistent logical allocation and request ledger for the shared memory store."""

from __future__ import annotations

import contextlib
import fcntl
import hashlib
import json
import os
import re
import sqlite3
import stat
from pathlib import Path

TOTAL_BYTES = 1_073_741_824
COPY_BYTES = 64 * 1024 * 1024
LEDGER_BYTES = 1024 * 1024
BASE_BYTES = 2 * COPY_BYTES + 2 * LEDGER_BYTES
_HEX = re.compile(r"[0-9a-f]{64}\Z")
_KEY = re.compile(r"[A-Za-z0-9_.:-]{1,128}\Z")
# The allocations table stays in the schema so existing ledgers keep opening;
# backup copies are no longer charged and reconciliation empties it.
_SCHEMA = """
CREATE TABLE metadata (
 singleton INTEGER PRIMARY KEY CHECK(singleton=1),
 schema_version INTEGER NOT NULL CHECK(schema_version=1),
 generation INTEGER NOT NULL,
 inventory_state TEXT NOT NULL CHECK(inventory_state='complete')
);
CREATE TABLE allocations (
 resource_key TEXT PRIMARY KEY, kind TEXT NOT NULL, location TEXT NOT NULL,
 charged_bytes INTEGER NOT NULL CHECK(charged_bytes>=0), evidence_ref TEXT NOT NULL
);
CREATE TABLE operations (
 request_key TEXT PRIMARY KEY, fingerprint TEXT NOT NULL,
 reserved_bytes INTEGER NOT NULL CHECK(reserved_bytes>=0),
 state TEXT NOT NULL CHECK(state IN ('pending','completed')), result TEXT, context TEXT
);
"""


class CapacityError(Exception):
    """Refuse growth without printing private input or raw database errors."""

    code = 4

    def __init__(self, message="MEMORY_CAPACITY_UNVERIFIED: growth refused"):
        super().__init__(message)


def _regular(path: Path) -> os.stat_result:
    observed = path.lstat()
    if (
        not stat.S_ISREG(observed.st_mode)
        or observed.st_nlink != 1
        or observed.st_uid != os.geteuid()
        or stat.S_IMODE(observed.st_mode) != 0o600
    ):
        raise CapacityError("MEMORY_CAPACITY_UNSAFE_PATH: growth refused")
    return observed


def _directory(path: Path) -> None:
    if not path.is_absolute() or path != path.absolute() or ".." in path.parts:
        raise CapacityError("MEMORY_CAPACITY_UNSAFE_PATH: growth refused")
    current = Path(path.anchor)
    for part in path.parts[1:]:
        current = current / part
        if not stat.S_ISDIR(current.lstat().st_mode):
            raise CapacityError("MEMORY_CAPACITY_UNSAFE_PATH: growth refused")
    observed = path.stat()
    if observed.st_uid != os.geteuid() or stat.S_IMODE(observed.st_mode) != 0o700:
        raise CapacityError("MEMORY_CAPACITY_UNSAFE_PATH: growth refused")


class MemoryCapacity:
    def __init__(self, memory_path: Path):
        self.memory_path = Path(memory_path).absolute()
        self.path = self.memory_path.parent / "capacity.sqlite3"
        self.lock_path = self.path.with_name("capacity.lock")

    def _validate(self, *, ledger=True):
        _directory(self.path.parent)
        if any(
            path.exists() or path.is_symlink()
            for database in (self.path, self.memory_path)
            for path in (
                database.with_name(database.name + "-wal"),
                database.with_name(database.name + "-shm"),
            )
        ):
            raise CapacityError(
                "MEMORY_CAPACITY_UNSAFE_PATH: unexpected SQLite sidecar"
            )
        if ledger:
            if _regular(self.path).st_size > LEDGER_BYTES:
                raise CapacityError("MEMORY_CAPACITY_EXISTING_LIMIT: growth refused")
        for path in (
            self.path.with_name(self.path.name + "-journal"),
            self.memory_path,
            self.memory_path.with_name(self.memory_path.name + "-journal"),
        ):
            if path.exists() or path.is_symlink():
                observed = _regular(path)
                ceiling = (
                    LEDGER_BYTES if path.name.startswith("capacity.") else COPY_BYTES
                )
                if observed.st_size > ceiling:
                    raise CapacityError(
                        "MEMORY_CAPACITY_EXISTING_LIMIT: growth refused"
                    )

    @contextlib.contextmanager
    def _connection(self, *, create=False):
        try:
            if create and not self.path.parent.exists():
                self.path.parent.mkdir(mode=0o700)
            self._validate(ledger=not create or self.path.exists())
            descriptor = os.open(
                self.lock_path, os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o600
            )
            try:
                _regular(self.lock_path)
                if self.lock_path.stat().st_size:
                    raise CapacityError("MEMORY_CAPACITY_UNSAFE_PATH: growth refused")
                fcntl.flock(descriptor, fcntl.LOCK_EX)
                self._validate(ledger=not create or self.path.exists())
                missing = not self.path.exists()
                if missing and not create:
                    raise CapacityError()
                if missing:
                    os.close(
                        os.open(
                            self.path,
                            os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                            0o600,
                        )
                    )
                connection = sqlite3.connect(self.path, timeout=5, isolation_level=None)
                connection.row_factory = sqlite3.Row
                try:
                    connection.execute("PRAGMA journal_mode=DELETE")
                    page_size = connection.execute("PRAGMA page_size").fetchone()[0]
                    connection.execute(
                        f"PRAGMA max_page_count={LEDGER_BYTES // page_size}"
                    )
                    if missing:
                        connection.executescript(_SCHEMA)
                    if (
                        connection.execute("PRAGMA integrity_check").fetchone()[0]
                        != "ok"
                    ):
                        raise CapacityError()
                    connection.execute("BEGIN IMMEDIATE")
                    try:
                        yield connection
                        connection.execute("COMMIT")
                    except BaseException:
                        if connection.in_transaction:
                            connection.execute("ROLLBACK")
                        raise
                finally:
                    connection.close()
            finally:
                os.close(descriptor)
        except (
            OSError,
            sqlite3.Error,
            ValueError,
            TypeError,
            KeyError,
            IndexError,
            RecursionError,
        ) as error:
            raise CapacityError() from error

    def _status(self, connection):
        metadata = connection.execute(
            "SELECT * FROM metadata WHERE singleton=1"
        ).fetchone()
        if metadata is None or metadata["schema_version"] != 1:
            raise CapacityError()
        reserved = connection.execute(
            "SELECT coalesce(sum(reserved_bytes),0) FROM operations WHERE state='pending'"
        ).fetchone()[0]
        return {
            "schema_version": 1,
            "generation": metadata["generation"],
            "inventory_state": metadata["inventory_state"],
            "cap_bytes": TOTAL_BYTES,
            "base_bytes": BASE_BYTES,
            "charged_bytes": BASE_BYTES,
            "reserved_bytes": reserved,
            "available_bytes": max(0, TOTAL_BYTES - BASE_BYTES - reserved),
            "legacy_allocations": connection.execute(
                "SELECT count(*) FROM allocations"
            ).fetchone()[0],
            "pending_operations": [
                {
                    "request_key": row["request_key"],
                    "reserved_bytes": row["reserved_bytes"],
                    "state": row["state"],
                }
                for row in connection.execute(
                    "SELECT request_key,reserved_bytes,state FROM operations WHERE state='pending' ORDER BY request_key"
                )
            ],
        }

    def status(self) -> dict:
        if not self.path.exists() and not self.path.is_symlink():
            return {
                "schema_version": 1,
                "cap_bytes": TOTAL_BYTES,
                "inventory_state": "unverified",
            }
        try:
            self._validate()
            connection = sqlite3.connect(self.path.as_uri() + "?mode=ro", uri=True)
            connection.row_factory = sqlite3.Row
            try:
                connection.execute("BEGIN")
                return self._status(connection)
            finally:
                connection.close()
        except (
            OSError,
            sqlite3.Error,
            ValueError,
            TypeError,
            KeyError,
            IndexError,
            RecursionError,
        ) as error:
            raise CapacityError() from error

    def reconcile(self, *, expected_generation: int | None = None) -> dict:
        """Adopt the ledger and drop allocations left by retired backup copies."""
        with self._connection(create=True) as connection:
            metadata = connection.execute(
                "SELECT * FROM metadata WHERE singleton=1"
            ).fetchone()
            generation = 0 if metadata is None else metadata["generation"]
            if expected_generation is not None and expected_generation != generation:
                raise CapacityError("MEMORY_CAPACITY_CONFLICT: inventory changed")
            connection.execute("DELETE FROM allocations")
            connection.execute(
                "INSERT OR REPLACE INTO metadata VALUES (1,1,?,'complete')",
                (generation + 1,),
            )
            return self._status(connection)

    def reserve(self, request_key: str, fingerprint: str, reserved_bytes: int) -> dict:
        if (
            not isinstance(request_key, str)
            or not _KEY.fullmatch(request_key)
            or not isinstance(fingerprint, str)
            or not _HEX.fullmatch(fingerprint)
            or type(reserved_bytes) is not int
            or reserved_bytes < 0
        ):
            raise CapacityError("MEMORY_CAPACITY_INVALID: reservation refused")
        if not self.path.exists():
            raise CapacityError()
        with self._connection() as connection:
            status = self._status(connection)
            previous = connection.execute(
                "SELECT * FROM operations WHERE request_key=?", (request_key,)
            ).fetchone()
            if previous is not None:
                if (
                    previous["fingerprint"] != fingerprint
                    or previous["reserved_bytes"] != reserved_bytes
                ):
                    raise CapacityError(
                        "MEMORY_CAPACITY_CONFLICT: request identity differs"
                    )
                return {
                    "state": previous["state"],
                    "replay": True,
                    "result": json.loads(previous["result"] or "null"),
                }
            if (
                status["charged_bytes"] + status["reserved_bytes"] + reserved_bytes
                > TOTAL_BYTES
            ):
                raise CapacityError("MEMORY_CAPACITY_EXCEEDED: growth refused")
            connection.execute(
                "INSERT INTO operations VALUES (?,?,?,'pending',NULL,'null')",
                (request_key, fingerprint, reserved_bytes),
            )
            connection.execute(
                "UPDATE metadata SET generation=generation+1 WHERE singleton=1"
            )
            return {"state": "pending", "replay": False, "result": None}

    def operation(self, request_key: str, fingerprint: str) -> dict | None:
        """Look up an exact operation without reserving again."""
        if not self.path.exists():
            return None
        try:
            self._validate()
            connection = sqlite3.connect(self.path.as_uri() + "?mode=ro", uri=True)
            connection.row_factory = sqlite3.Row
            try:
                connection.execute("BEGIN")
                self._status(connection)
                row = connection.execute(
                    "SELECT * FROM operations WHERE request_key=?", (request_key,)
                ).fetchone()
                if row is None:
                    return None
                if row["fingerprint"] != fingerprint:
                    raise CapacityError(
                        "MEMORY_CAPACITY_CONFLICT: request identity differs"
                    )
                return {
                    "state": row["state"],
                    "replay": True,
                    "result": json.loads(row["result"] or "null"),
                }
            finally:
                connection.close()
        except (
            OSError,
            sqlite3.Error,
            ValueError,
            TypeError,
            IndexError,
            RecursionError,
        ) as error:
            raise CapacityError() from error

    def resolve(self, request_key: str, *, result: dict, evidence_ref: str) -> dict:
        """Settle only a caller-verified result."""
        if not isinstance(evidence_ref, str) or not 1 <= len(evidence_ref) <= 512:
            raise CapacityError()
        return self.settle(
            request_key, result={**result, "reconciliation_evidence": evidence_ref}
        )

    def settle(self, request_key: str, *, result: dict | None = None) -> dict:
        try:
            encoded = json.dumps(result, sort_keys=True, allow_nan=False)
            if len(encoded.encode()) > 4096:
                raise CapacityError()
        except (ValueError, TypeError, RecursionError) as error:
            raise CapacityError() from error
        with self._connection() as connection:
            self._status(connection)
            operation = connection.execute(
                "SELECT * FROM operations WHERE request_key=?", (request_key,)
            ).fetchone()
            if operation is None:
                raise CapacityError("MEMORY_CAPACITY_CONFLICT: reservation missing")
            if operation["state"] == "completed":
                return {
                    "state": "completed",
                    "result": json.loads(operation["result"] or "null"),
                }
            connection.execute(
                "UPDATE operations SET state='completed',result=? WHERE request_key=?",
                (encoded, request_key),
            )
            connection.execute(
                "UPDATE metadata SET generation=generation+1 WHERE singleton=1"
            )
            return {"state": "completed", "result": result}


def operation_fingerprint(value: object) -> str:
    return hashlib.sha256(
        json.dumps(
            value, sort_keys=True, separators=(",", ":"), allow_nan=False
        ).encode()
    ).hexdigest()
