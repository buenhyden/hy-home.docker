"""Persistent, conservative logical allocation for managed memory storage."""

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
MAX_INVENTORY_ENTRIES = 4096
_HEX = re.compile(r"[0-9a-f]{64}\Z")
_KEY = re.compile(r"[A-Za-z0-9_.:-]{1,128}\Z")
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


def local_allocation(path: Path) -> dict:
    """Validate metadata only; a managed copy consumes one full copy allowance."""
    path = path.absolute()
    _directory(path.parent)
    observed = _regular(path)
    if observed.st_size > COPY_BYTES:
        raise CapacityError("MEMORY_CAPACITY_COPY_TOO_LARGE: growth refused")
    return {
        "resource_key": "local:" + str(path),
        "kind": "local",
        "location": str(path),
        "charged_bytes": COPY_BYTES,
        "evidence_ref": "verified regular-file metadata",
    }


def validate_backup_destination(store: Path, output: Path) -> None:
    """Protect the memory and independent accounting controls from a copy."""
    store, output = store.resolve(), output.absolute()
    controls = {
        name + suffix
        for name in (store.name, "capacity.sqlite3")
        for suffix in ("", "-journal", "-wal", "-shm")
    }
    controls |= {"capacity.lock", "backup.lock", "copy.lock"}
    if output.resolve() in {store.with_name(name) for name in controls} or (
        output.parent.resolve() == store.parent
        and (
            output.name.startswith("." + store.name + ".restore-")
            or output.name.startswith("." + store.name + ".tmp")
        )
    ):
        raise CapacityError(
            "MEMORY_BACKUP_FAILED: the output is the store itself or its accounting control"
        )
    if output.parent.resolve() != output.parent or not output.parent.is_dir():
        raise CapacityError("MEMORY_BACKUP_FAILED: output parent is not a directory")
    observed = output.parent.stat()
    if observed.st_uid != os.geteuid():
        raise CapacityError("MEMORY_BACKUP_FAILED: output parent is not owned by you")
    if stat.S_IMODE(observed.st_mode) & 0o077:
        raise CapacityError("MEMORY_BACKUP_FAILED: output parent is not 0700")


def validate_copy_context(memory_path: Path, context: dict) -> None:
    if (
        not isinstance(context, dict)
        or set(context) != {"producer", "source", "target", "temporary"}
        or not isinstance(context.get("producer"), str)
        or context.get("producer") not in {"manual-backup", "restore"}
        or any(
            not isinstance(context[key], str)
            or not Path(context[key]).is_absolute()
            or len(context[key]) > 4096
            for key in ("source", "target", "temporary")
        )
    ):
        raise CapacityError("MEMORY_CAPACITY_INVALID: operation context refused")
    source, target, temporary = (
        Path(context[key]) for key in ("source", "target", "temporary")
    )
    if context["producer"] == "manual-backup":
        if source != memory_path or temporary != target.with_name(
            "." + target.name + ".tmp"
        ):
            raise CapacityError()
        validate_backup_destination(memory_path, target)
    else:
        prefix = "." + memory_path.name + ".restore-"
        if (
            target != memory_path
            or temporary.parent != memory_path.parent
            or not temporary.name.startswith(prefix)
            or not re.fullmatch(r"[0-9a-f]{32}", temporary.name[len(prefix) :])
        ):
            raise CapacityError()
        validate_backup_destination(memory_path, source)


def external_allocation(snapshot: dict) -> dict:
    if not isinstance(snapshot, dict) or set(snapshot) != {
        "repository_id",
        "snapshot_id",
        "location",
        "evidence_ref",
    }:
        raise CapacityError()
    repository, identity, location, evidence = (
        snapshot[key]
        for key in ("repository_id", "snapshot_id", "location", "evidence_ref")
    )
    if (
        not isinstance(repository, str)
        or not _HEX.fullmatch(repository)
        or not isinstance(identity, str)
        or not _HEX.fullmatch(identity)
        or not isinstance(location, str)
        or location not in {"state", "offsite"}
        or not isinstance(evidence, str)
        or not 1 <= len(evidence) <= 512
    ):
        raise CapacityError()
    return {
        "resource_key": f"external:{location}:{repository}:{identity}",
        "kind": "external",
        "location": location,
        "charged_bytes": COPY_BYTES,
        "evidence_ref": evidence,
    }


def _allocation(value: dict) -> dict:
    if not isinstance(value, dict) or set(value) != {
        "resource_key",
        "kind",
        "location",
        "charged_bytes",
        "evidence_ref",
    }:
        raise CapacityError()
    if (
        any(
            not isinstance(value[key], str)
            for key in ("resource_key", "kind", "location", "evidence_ref")
        )
        or type(value["charged_bytes"]) is not int
    ):
        raise CapacityError()
    if value["kind"] == "local":
        actual = local_allocation(Path(value["location"]))
    elif value["kind"] == "external":
        pieces = value["resource_key"].split(":")
        if len(pieces) != 4 or pieces[0] != "external":
            raise CapacityError()
        actual = external_allocation(
            {
                "location": pieces[1],
                "repository_id": pieces[2],
                "snapshot_id": pieces[3],
                "evidence_ref": value["evidence_ref"],
            }
        )
    else:
        raise CapacityError()
    if (
        actual["resource_key"] != value["resource_key"]
        or actual["charged_bytes"] != value["charged_bytes"]
    ):
        raise CapacityError()
    return actual


def _stored_allocation(value: dict) -> dict:
    """Validate accounting structure without reading any retained file body."""
    if (
        not isinstance(value, dict)
        or set(value)
        != {"resource_key", "kind", "location", "charged_bytes", "evidence_ref"}
        or any(
            not isinstance(value[key], str)
            for key in ("resource_key", "kind", "location", "evidence_ref")
        )
        or type(value["charged_bytes"]) is not int
        or value["charged_bytes"] != COPY_BYTES
        or not 1 <= len(value["evidence_ref"]) <= 512
    ):
        raise CapacityError()
    if value["kind"] == "external":
        parts = value["resource_key"].split(":")
        if len(parts) != 4 or parts[0] != "external" or parts[1] != value["location"]:
            raise CapacityError()
        external_allocation(
            {
                "repository_id": parts[2],
                "snapshot_id": parts[3],
                "location": parts[1],
                "evidence_ref": value["evidence_ref"],
            }
        )
    elif (
        value["kind"] != "local"
        or not Path(value["location"]).is_absolute()
        or value["resource_key"] != "local:" + value["location"]
    ):
        raise CapacityError()
    return value


class MemoryCapacity:
    def __init__(self, memory_path: Path):
        self.memory_path = Path(memory_path).absolute()
        self.path = self.memory_path.parent / "capacity.sqlite3"
        self.lock_path = self.path.with_name("capacity.lock")

    def _context(self, encoded):
        context = json.loads(encoded or "null")
        if context is not None:
            validate_copy_context(self.memory_path, context)
        return context

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
        allocations = [
            _stored_allocation(dict(row))
            for row in connection.execute(
                "SELECT * FROM allocations ORDER BY resource_key"
            )
        ]
        reserved = connection.execute(
            "SELECT coalesce(sum(reserved_bytes),0) FROM operations WHERE state='pending'"
        ).fetchone()[0]
        allocated = sum(row["charged_bytes"] for row in allocations)
        return {
            "schema_version": 1,
            "generation": metadata["generation"],
            "inventory_state": metadata["inventory_state"],
            "cap_bytes": TOTAL_BYTES,
            "base_bytes": BASE_BYTES,
            "charged_bytes": BASE_BYTES + allocated,
            "reserved_bytes": reserved,
            "available_bytes": max(0, TOTAL_BYTES - BASE_BYTES - allocated - reserved),
            "local_backup_bytes": sum(
                row["charged_bytes"] for row in allocations if row["kind"] == "local"
            ),
            "external_bytes": sum(
                row["charged_bytes"] for row in allocations if row["kind"] == "external"
            ),
            "allocations": allocations,
            "pending_operations": [
                {
                    "request_key": row["request_key"],
                    "reserved_bytes": row["reserved_bytes"],
                    "state": row["state"],
                    "context": self._context(row["context"]),
                }
                for row in connection.execute(
                    "SELECT request_key,reserved_bytes,state,context FROM operations WHERE state='pending' ORDER BY request_key"
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
            IndexError,
            RecursionError,
        ) as error:
            raise CapacityError() from error

    def reconcile(
        self, inventory: dict, *, expected_generation: int | None = None
    ) -> dict:
        if (
            not isinstance(inventory, dict)
            or set(inventory)
            not in (
                {"schema_version", "complete", "local_paths", "external_snapshots"},
                {
                    "schema_version",
                    "complete",
                    "local_paths",
                    "external_snapshots",
                    "observed_repositories",
                },
            )
            or type(inventory["schema_version"]) is not int
            or inventory["schema_version"] != 1
            or inventory["complete"] is not True
        ):
            raise CapacityError()
        paths, snapshots = inventory["local_paths"], inventory["external_snapshots"]
        if (
            not isinstance(paths, list)
            or not isinstance(snapshots, list)
            or len(paths) + len(snapshots) > MAX_INVENTORY_ENTRIES
        ):
            raise CapacityError()
        allocations = [external_allocation(snapshot) for snapshot in snapshots]
        observed = inventory.get(
            "observed_repositories",
            [
                {"repository_id": row["repository_id"], "location": row["location"]}
                for row in snapshots
            ],
        )
        if not isinstance(observed, list) or len(observed) > MAX_INVENTORY_ENTRIES:
            raise CapacityError()
        observed_scopes = set()
        for repository in observed:
            if (
                not isinstance(repository, dict)
                or set(repository) != {"repository_id", "location"}
                or not isinstance(repository["repository_id"], str)
                or not _HEX.fullmatch(repository["repository_id"])
                or repository["location"] not in ("state", "offsite")
            ):
                raise CapacityError()
            observed_scopes.add((repository["location"], repository["repository_id"]))
        if any(
            (row["location"], row["repository_id"]) not in observed_scopes
            for row in snapshots
        ):
            raise CapacityError(
                "MEMORY_CAPACITY_INCOMPLETE: external repository not observed"
            )
        paths = tuple(paths)
        if any(
            not isinstance(value, str) or not Path(value).is_absolute()
            for value in paths
        ):
            raise CapacityError()
        with self._connection(create=True) as connection:
            # Stat and replacement share the reservation/settlement lock. A
            # settled copy must not disappear between a stale stat and DELETE.
            for value in paths:
                path = Path(value)
                _directory(path.parent)
                if path.exists() or path.is_symlink():
                    allocations.append(local_allocation(path))
            keys = [row["resource_key"] for row in allocations]
            if len(keys) != len(set(keys)):
                raise CapacityError()
            metadata = connection.execute(
                "SELECT * FROM metadata WHERE singleton=1"
            ).fetchone()
            generation = 0 if metadata is None else metadata["generation"]
            if expected_generation is not None and expected_generation != generation:
                raise CapacityError("MEMORY_CAPACITY_CONFLICT: inventory changed")
            previous = [
                _stored_allocation(dict(row))
                for row in connection.execute("SELECT * FROM allocations")
            ]
            previous_external = [row for row in previous if row["kind"] == "external"]
            for allocation in previous_external:
                parts = allocation["resource_key"].split(":")
                if (parts[1], parts[2]) not in observed_scopes:
                    raise CapacityError(
                        "MEMORY_CAPACITY_INCOMPLETE: previous external repository not observed"
                    )
            local_keys = {
                row["resource_key"] for row in previous if row["kind"] == "local"
            }
            if not local_keys <= {"local:" + path for path in paths}:
                raise CapacityError(
                    "MEMORY_CAPACITY_INCOMPLETE: previous resources omitted"
                )
            connection.execute("DELETE FROM allocations")
            for allocation in allocations:
                self._upsert(connection, allocation)
            connection.execute(
                "INSERT OR REPLACE INTO metadata VALUES (1,1,?,'complete')",
                (generation + 1,),
            )
            result = self._status(connection)
        return result

    @staticmethod
    def _upsert(connection, allocation):
        connection.execute(
            "INSERT OR REPLACE INTO allocations VALUES (?,?,?,?,?)",
            tuple(
                allocation[key]
                for key in (
                    "resource_key",
                    "kind",
                    "location",
                    "charged_bytes",
                    "evidence_ref",
                )
            ),
        )

    def reserve(
        self,
        request_key: str,
        fingerprint: str,
        reserved_bytes: int,
        *,
        context: dict | None = None,
    ) -> dict:
        if context is not None:
            validate_copy_context(self.memory_path, context)
        encoded_context = json.dumps(context, sort_keys=True, allow_nan=False)
        if len(encoded_context.encode()) > 16384:
            raise CapacityError()
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
                    or previous["context"] != encoded_context
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
                "INSERT INTO operations VALUES (?,?,?,'pending',NULL,?)",
                (request_key, fingerprint, reserved_bytes, encoded_context),
            )
            connection.execute(
                "UPDATE metadata SET generation=generation+1 WHERE singleton=1"
            )
            return {"state": "pending", "replay": False, "result": None}

    def operation(self, request_key: str, fingerprint: str) -> dict | None:
        """Look up an exact operation without refreshing inventory or reserving again."""
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

    def resolve(
        self,
        request_key: str,
        allocations: list[dict],
        *,
        result: dict,
        evidence_ref: str,
    ) -> dict:
        """Settle only a caller-verified result; the producer owns the metadata proof."""
        if not isinstance(evidence_ref, str) or not 1 <= len(evidence_ref) <= 512:
            raise CapacityError()
        return self.settle(
            request_key,
            allocations,
            result={**result, "reconciliation_evidence": evidence_ref},
        )

    def settle(
        self, request_key: str, allocations: list[dict], *, result: dict | None = None
    ) -> dict:
        if (
            not isinstance(allocations, list)
            or len(allocations) > MAX_INVENTORY_ENTRIES
        ):
            raise CapacityError()
        try:
            validated = [_allocation(value) for value in allocations]
            encoded = json.dumps(result, sort_keys=True, allow_nan=False)
            if len(encoded.encode()) > 4096:
                raise CapacityError()
        except (OSError, ValueError, TypeError, KeyError, RecursionError) as error:
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
            increase = 0
            for allocation in validated:
                previous = connection.execute(
                    "SELECT charged_bytes FROM allocations WHERE resource_key=?",
                    (allocation["resource_key"],),
                ).fetchone()
                increase += max(
                    0,
                    allocation["charged_bytes"]
                    - (0 if previous is None else previous[0]),
                )
            if increase > operation["reserved_bytes"]:
                raise CapacityError(
                    "MEMORY_CAPACITY_CONFLICT: result exceeds reservation"
                )
            for allocation in validated:
                self._upsert(connection, allocation)
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
