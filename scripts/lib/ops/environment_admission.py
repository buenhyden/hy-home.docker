"""Shared pending/live admission for existing environment runners.

Reservations are logical accounting, not filesystem quotas or a Docker ACL.
The production store is shared by this user's entrypoints on one host; actual
daemon identity scopes service inventories, while numeric reservations span
all daemon/workspace keys. Consumers prove owned resource absence on release.
"""

from __future__ import annotations

import contextlib
import hashlib
import json
import math
import os
import pwd
import re
import sqlite3
import stat
import subprocess
import time
import uuid
from pathlib import Path

NUMERIC = ("cpus", "memory_bytes", "disk_bytes")
ACTIVE = ("intent", "running")
NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,127}\Z")
IDENTITY = ("pid", "start_ticks", "boot_id", "pgid")


class AdmissionError(ValueError):
    """A boundary that cannot safely admit, update or release a run."""


def process_identity(pid=None):
    """Return Linux process identity; absence and unreadability stay distinct."""
    pid = os.getpid() if pid is None else pid
    if type(pid) is not int or pid <= 0:
        raise AdmissionError("invalid_process_identity")
    try:
        # comm may contain spaces and parentheses; fields after its last ')' are stable.
        fields = Path(f"/proc/{pid}/stat").read_text().rsplit(")", 1)[1].split()
    except FileNotFoundError:
        return None
    except (OSError, IndexError):
        raise AdmissionError("process_identity_unavailable") from None
    try:
        boot_id = Path("/proc/sys/kernel/random/boot_id").read_text().strip()
        if not boot_id:
            raise AdmissionError("process_identity_unavailable")
        return {
            "pid": pid,
            "start_ticks": int(fields[19]),
            "boot_id": boot_id,
            "pgid": int(fields[2]),
        }
    except (OSError, ValueError, IndexError):
        raise AdmissionError("process_identity_unavailable") from None


def process_status(identity):
    """Observe the recorded leader only; this does not prove group absence."""
    try:
        expected = _identity(identity)
        actual = process_identity(expected["pid"])
        if actual is None or any(
            actual[key] != expected[key] for key in ("pid", "start_ticks", "boot_id")
        ):
            return "absent"
        return "alive" if actual["pgid"] == expected["pgid"] else "unknown"
    except AdmissionError:
        return "unknown"


def _identity(value):
    if not isinstance(value, dict) or set(value) != set(IDENTITY):
        raise AdmissionError("invalid_process_identity")
    if any(
        type(value[key]) is not int or value[key] <= 0
        for key in ("pid", "start_ticks", "pgid")
    ):
        raise AdmissionError("invalid_process_identity")
    if not isinstance(value["boot_id"], str) or not value["boot_id"]:
        raise AdmissionError("invalid_process_identity")
    return dict(value)


def _amount(value, *, positive=False, integral=False):
    try:
        finite = type(value) in (int, float) and math.isfinite(value)
    except OverflowError:
        finite = False
    if not finite:
        raise AdmissionError("invalid_numeric_budget")
    if value < 0 or (positive and value == 0) or (integral and int(value) != value):
        raise AdmissionError("invalid_numeric_budget")
    return int(value) if integral else value


def _budget(value, *, limits=False, observed=False, strict=False):
    keys = NUMERIC if observed else (*NUMERIC, "runtime_seconds")
    if not isinstance(value, dict) or set(value) - set(keys):
        raise AdmissionError("invalid_budget")
    if (not observed or strict) and set(value) != set(keys):
        raise AdmissionError("incomplete_budget")
    return {
        key: _amount(
            value.get(key, 0),
            positive=limits or key == "runtime_seconds",
            integral=key.endswith("_bytes"),
        )
        for key in keys
    }


def _strings(values, *, names=False):
    if not isinstance(values, (list, tuple, set, frozenset)) or len(values) > 10000:
        raise AdmissionError("invalid_selection")
    if any(
        not isinstance(value, str)
        or not value
        or len(value) > 512
        or "\0" in value
        or (names and not NAME.fullmatch(value))
        for value in values
    ):
        raise AdmissionError("invalid_selection")
    return sorted(set(values))


def _text(value):
    if not isinstance(value, str) or not value or len(value) > 4096 or "\0" in value:
        raise AdmissionError("invalid_binding")
    return value


def _project(value):
    if value is not None and (
        not isinstance(value, str)
        or not re.fullmatch(r"[a-z0-9][a-z0-9_-]{0,127}", value)
    ):
        raise AdmissionError("invalid_admission_project")
    return value


def _private_directory(path):
    """Create beneath verified non-symlink ancestors, retaining descriptor binding."""
    path = Path(path)
    if not path.is_absolute() or ".." in path.parts:
        raise AdmissionError("unsafe_state_directory")
    descriptor = os.open("/", os.O_RDONLY | os.O_DIRECTORY)
    try:
        for index, component in enumerate(path.parts[1:]):
            try:
                following = os.open(
                    component,
                    os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                    dir_fd=descriptor,
                )
            except FileNotFoundError:
                try:
                    os.mkdir(component, 0o700, dir_fd=descriptor)
                except FileExistsError:
                    pass
                following = os.open(
                    component,
                    os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                    dir_fd=descriptor,
                )
            os.close(descriptor)
            descriptor = following
            found = os.fstat(descriptor)
            if (
                found.st_uid not in (0, os.getuid())
                and not found.st_mode & stat.S_ISVTX
            ):
                raise AdmissionError("foreign_state_directory")
            writable = stat.S_IMODE(found.st_mode) & 0o022
            if writable and not found.st_mode & stat.S_ISVTX:
                raise AdmissionError("unsafe_state_directory")
            if index == len(path.parts) - 2:
                if found.st_uid != os.getuid() or stat.S_IMODE(found.st_mode) & 0o077:
                    raise AdmissionError("state_directory_not_private")
    except OSError:
        raise AdmissionError("state_directory_unavailable") from None
    finally:
        os.close(descriptor)


def _json(value):
    try:
        encoded = json.dumps(
            value, sort_keys=True, separators=(",", ":"), allow_nan=False
        )
    except (TypeError, ValueError, RecursionError):
        raise AdmissionError("invalid_record_metadata") from None
    if len(encoded.encode()) > 65536:
        raise AdmissionError("record_metadata_too_large")
    return encoded


class Admission:
    """Internal/test constructor; production consumers use host_admission."""

    def __init__(
        self,
        state_dir,
        *,
        namespace,
        workspace_id,
        inventory,
        limits,
        observe=None,
        inventory_key="home",
        kind_limits=None,
        binding_id=None,
        daemon_id=None,
        strict_observation=False,
    ):
        self.namespace = _text(namespace)
        self.workspace_id = _text(workspace_id)
        self.binding_id = _text(binding_id or workspace_id)
        self.daemon_id = None if daemon_id is None else _text(daemon_id)
        self.inventory_key = _text(inventory_key)
        self.inventory = _strings(inventory, names=True)
        self.limits = _budget(limits, limits=True)
        self.kind_limits = dict(kind_limits or {})
        for name, value in self.kind_limits.items():
            _text(name)
            if type(value) is not int or value < 1:
                raise AdmissionError("invalid_kind_limit")
        self.observe = observe
        self.strict_observation = strict_observation
        self.recovery_only = False
        directory = Path(state_dir)
        _private_directory(directory)
        namespace_dir = directory / hashlib.sha256(namespace.encode()).hexdigest()
        _private_directory(namespace_dir)
        self.path = namespace_dir / "admission.sqlite3"
        try:
            descriptor = os.open(
                self.path, os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o600
            )
            try:
                found = os.fstat(descriptor)
                if (
                    not stat.S_ISREG(found.st_mode)
                    or found.st_uid != os.getuid()
                    or found.st_mode & 0o077
                ):
                    raise AdmissionError("unsafe_admission_database")
            finally:
                os.close(descriptor)
        except OSError:
            raise AdmissionError("admission_database_unavailable") from None

    @contextlib.contextmanager
    def _transaction(self):
        connection = None
        try:
            _private_directory(self.path.parent)
            found = self.path.lstat()
            if (
                not stat.S_ISREG(found.st_mode)
                or found.st_uid != os.getuid()
                or found.st_mode & 0o077
            ):
                raise AdmissionError("unsafe_admission_database")
            connection = sqlite3.connect(self.path, timeout=10, isolation_level=None)
            connection.execute("PRAGMA synchronous=FULL")
            connection.execute("PRAGMA secure_delete=ON")
            connection.execute("BEGIN IMMEDIATE")
            tables = {
                name
                for (name,) in connection.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
                )
            }
            if (tables and tables != {"runs", "policy"}) or (
                self.recovery_only and not tables
            ):
                raise AdmissionError("incomplete_admission_state")
            if not tables:
                connection.execute(
                    "CREATE TABLE runs (token TEXT PRIMARY KEY, record TEXT NOT NULL)"
                )
                connection.execute(
                    "CREATE TABLE policy (key TEXT PRIMARY KEY, value TEXT NOT NULL)"
                )
            yield connection
            connection.execute("COMMIT")
        except (sqlite3.Error, OSError, json.JSONDecodeError):
            raise AdmissionError("admission_state_unavailable") from None
        finally:
            if connection is not None:
                if connection.in_transaction:
                    connection.execute("ROLLBACK")
                connection.close()

    @staticmethod
    def _record(token, raw):
        try:
            if not isinstance(raw, str) or len(raw.encode()) > 65536:
                raise AdmissionError("invalid_admission_record")
            value = json.loads(raw)
            required = {
                "token",
                "workspace_id",
                "binding_id",
                "daemon_id",
                "inventory_key",
                "kind",
                "state",
                "services",
                "budget",
                "resources",
                "owner",
                "identity",
                "project",
                "created_at",
                "expires_at",
                "metadata",
            }
            if (
                not isinstance(value, dict)
                or not required <= value.keys()
                or value.keys() != required
                or not re.fullmatch(r"[0-9a-f]{32}", token)
            ):
                raise AdmissionError("invalid_admission_record")
            if value["token"] != token or value["state"] not in ACTIVE:
                raise AdmissionError("invalid_admission_record")
            for key in ("workspace_id", "binding_id", "inventory_key", "kind"):
                _text(value[key])
            _strings(value["services"], names=True)
            _strings(value["resources"])
            _budget(value["budget"])
            for key in ("created_at", "expires_at"):
                _amount(value[key], positive=True)
            if value["expires_at"] <= value["created_at"]:
                raise AdmissionError("invalid_admission_deadline")
            if value["daemon_id"] is not None:
                _text(value["daemon_id"])
            _project(value["project"])
            _identity(value["owner"])
            if value["identity"] is not None:
                _identity(value["identity"])
            if not isinstance(value["metadata"], dict):
                raise AdmissionError("invalid_admission_record")
            _json(value)
            return value
        except (KeyError, TypeError, json.JSONDecodeError):
            raise AdmissionError("invalid_admission_record") from None

    @classmethod
    def _active(cls, connection):
        records = [
            cls._record(token, raw)
            for token, raw in connection.execute("SELECT token,record FROM runs")
        ]
        return records

    def _owned(self, connection, token):
        found = connection.execute(
            "SELECT record FROM runs WHERE token=?", (token,)
        ).fetchone()
        if found is None:
            raise AdmissionError("unknown_lease_token")
        record = self._record(token, found[0])
        if record["workspace_id"] != self.workspace_id:
            raise AdmissionError("foreign_lease_token")
        if self.daemon_id is not None and record["daemon_id"] != self.daemon_id:
            raise AdmissionError("foreign_daemon_lease_token")
        return record

    @staticmethod
    def _save(connection, record):
        connection.execute(
            "INSERT OR REPLACE INTO runs VALUES (?,?)", (record["token"], _json(record))
        )

    def _policy(self, connection, active):
        policy = {
            key: json.loads(value)
            for key, value in connection.execute("SELECT key,value FROM policy")
        }
        budget = {key: self.limits[key] for key in NUMERIC}
        if active and policy.get("limits", budget) != budget:
            raise AdmissionError("active_budget_policy_mismatch")
        inventories = policy.get("inventories", {})
        if not isinstance(inventories, dict):
            raise AdmissionError("invalid_inventory_policy")
        same_inventory = any(
            row["inventory_key"] == self.inventory_key for row in active
        )
        if same_inventory and inventories.get(self.inventory_key) != self.inventory:
            raise AdmissionError("active_inventory_mismatch")
        current_keys = {row["inventory_key"] for row in active} | {self.inventory_key}
        inventories = {
            key: value for key, value in inventories.items() if key in current_keys
        }
        kind_limits = policy.get("kind_limits", {})
        if not isinstance(kind_limits, dict) or any(
            type(value) is not int or value < 1 for value in kind_limits.values()
        ):
            raise AdmissionError("invalid_kind_policy")
        for kind, limit in self.kind_limits.items():
            if active and kind in kind_limits and kind_limits[kind] != limit:
                raise AdmissionError("active_kind_policy_mismatch")
            kind_limits[kind] = limit
        inventories[self.inventory_key] = self.inventory
        for key, value in {
            "limits": budget,
            "inventories": inventories,
            "kind_limits": kind_limits,
        }.items():
            connection.execute(
                "INSERT OR REPLACE INTO policy VALUES (?,?)", (key, _json(value))
            )
        return kind_limits

    def _observed(self):
        observed = self.observe() if self.observe else {}
        if not isinstance(observed, dict):
            raise AdmissionError("invalid_resource_observation")
        if self.strict_observation and "budget" not in observed:
            raise AdmissionError("incomplete_resource_observation")
        services = _strings(observed.get("services", []), names=True)
        if set(services) - set(self.inventory):
            raise AdmissionError("unknown_observed_service")
        budget = _budget(
            observed.get("budget", {}), observed=True, strict=self.strict_observation
        )
        resources = _strings(observed.get("resources", []))
        kinds = observed.get("kind_counts", {})
        if not isinstance(kinds, dict) or any(
            type(v) is not int or v < 0 for v in kinds.values()
        ):
            raise AdmissionError("invalid_kind_observation")
        # Reservations of running inventory services, already inside `budget`;
        # a compose-start replaces them in place instead of adding (see admit).
        raw = observed.get("service_budget", {})
        if not isinstance(raw, dict) or set(raw) - set(services):
            raise AdmissionError("invalid_service_budget_observation")
        in_place = {}
        for name, value in raw.items():
            if not isinstance(value, dict) or set(value) - {"cpus", "memory_bytes"}:
                raise AdmissionError("invalid_service_budget_observation")
            in_place[name] = {
                key: _amount(value.get(key, 0), integral=key == "memory_bytes")
                for key in ("cpus", "memory_bytes")
            }
        for key in ("cpus", "memory_bytes"):
            if sum(item[key] for item in in_place.values()) > budget[key]:
                raise AdmissionError("invalid_service_budget_observation")
        return services, budget, resources, kinds, in_place

    def admit(
        self,
        *,
        services=(),
        budget,
        kind,
        owner=None,
        resources=(),
        project=None,
        fill_disk=False,
    ):
        if self.recovery_only:
            raise AdmissionError("recovery_handle_is_release_only")
        if type(fill_disk) is not bool:
            raise AdmissionError("invalid_disk_reservation_mode")
        selected = _strings(services, names=True)
        if set(selected) - set(self.inventory):
            raise AdmissionError("unknown_selected_service")
        requested = _budget(budget)
        project = _project(project)
        kind = _text(kind)
        resources = _strings(resources)
        if requested["runtime_seconds"] > self.limits["runtime_seconds"]:
            raise AdmissionError("runtime_budget_exceeded")
        owner = _identity(owner) if owner is not None else process_identity()
        if owner is None:
            raise AdmissionError("owner_identity_unavailable")
        with self._transaction() as connection:
            active = self._active(connection)
            kinds = self._policy(connection, active)
            observed, used, held, observed_kinds, in_place = self._observed()
            if kind == "compose-start":
                # Compose recreates a running selected service in place, so its
                # running reservation is replaced by the request, not added.
                used = dict(used)
                for key in ("cpus", "memory_bytes"):
                    used[key] -= sum(
                        in_place[name][key] for name in selected if name in in_place
                    )
            if fill_disk:
                available = (
                    self.limits["disk_bytes"]
                    - used["disk_bytes"]
                    - sum(row["budget"]["disk_bytes"] for row in active)
                )
                if available < requested["disk_bytes"]:
                    raise AdmissionError("disk_bytes_budget_exceeded")
                requested["disk_bytes"] = available
            union = set(selected) | set(observed)
            for record in active:
                if record["inventory_key"] == self.inventory_key:
                    union.update(record["services"])
            if self.inventory and union >= set(self.inventory):
                raise AdmissionError("complete_inventory_start_refused")
            if set(resources) & (
                set(held) | {key for row in active for key in row["resources"]}
            ):
                raise AdmissionError("resource_already_reserved")
            for key in NUMERIC:
                total = (
                    used[key]
                    + requested[key]
                    + sum(row["budget"][key] for row in active)
                )
                if total > self.limits[key]:
                    raise AdmissionError(f"{key}_budget_exceeded")
            if (
                kind in kinds
                and 1
                + observed_kinds.get(kind, 0)
                + sum(row["kind"] == kind for row in active)
                > kinds[kind]
            ):
                raise AdmissionError("kind_budget_exceeded")
            now = time.time()
            record = {
                "token": uuid.uuid4().hex,
                "workspace_id": self.workspace_id,
                "binding_id": self.binding_id,
                "daemon_id": self.daemon_id,
                "inventory_key": self.inventory_key,
                "kind": kind,
                "state": "intent",
                "services": selected,
                "budget": requested,
                "resources": resources,
                "owner": owner,
                "identity": None,
                "project": project,
                "created_at": now,
                "expires_at": now + requested["runtime_seconds"],
                "metadata": {},
            }
            self._save(connection, record)
            return record

    def attach(self, lease_token, identity=None, **facts):
        if self.recovery_only:
            raise AdmissionError("recovery_handle_is_release_only")
        identity = None if identity is None else _identity(identity)
        with self._transaction() as connection:
            record = self._owned(connection, lease_token)
            if record["identity"] is not None and record["identity"] != identity:
                raise AdmissionError("process_identity_already_bound")
            self._facts(record, facts)
            record.update(state="running", identity=identity)
            self._save(connection, record)
            return record

    @staticmethod
    def _facts(record, facts):
        if set(facts) & {
            "token",
            "workspace_id",
            "binding_id",
            "daemon_id",
            "inventory_key",
            "kind",
            "state",
            "services",
            "budget",
            "resources",
            "owner",
            "identity",
            "created_at",
            "expires_at",
            "metadata",
        }:
            raise AdmissionError("reserved_record_field")
        record["metadata"] = {**record["metadata"], **facts}
        _json(record)

    def update(self, lease_token, **facts):
        if self.recovery_only:
            raise AdmissionError("recovery_handle_is_release_only")
        with self._transaction() as connection:
            record = self._owned(connection, lease_token)
            self._facts(record, facts)
            self._save(connection, record)
            return record

    def release(self, lease_token, verify):
        with self._transaction() as connection:
            record = self._owned(connection, lease_token)
            if (
                record["identity"] is not None
                and process_status(record["identity"]) != "absent"
            ):
                return False
            if verify(record) is not True:
                return False
            connection.execute("DELETE FROM runs WHERE token=?", (lease_token,))
            return True

    def records(self):
        with self._transaction() as connection:
            return self._active(connection)


def host_state_directory():
    """Return the fixed UID-bound state path without creating or changing it."""
    try:
        return Path(pwd.getpwuid(os.getuid()).pw_dir) / ".hy-home-execution"
    except (KeyError, OSError):
        raise AdmissionError("host_binding_unavailable") from None


def _host_binding(root, daemon_id):
    root = Path(root)
    daemon_id = _text(daemon_id)
    try:
        resolved = root.resolve(strict=True)
    except OSError:
        raise AdmissionError("invalid_workspace_binding") from None
    if not root.is_absolute() or resolved != root:
        raise AdmissionError("invalid_workspace_binding")
    try:
        found = subprocess.run(
            [
                "git",
                "-C",
                str(root),
                "rev-parse",
                "--path-format=absolute",
                "--git-common-dir",
            ],
            check=True,
            capture_output=True,
            text=True,
            timeout=10,
        ).stdout.strip()
        common = Path(found).resolve(strict=True)
        machine = Path("/etc/machine-id").read_text().strip()
        if not machine or not common.is_dir():
            raise AdmissionError("host_binding_unavailable")
        directory = host_state_directory()
    except (OSError, subprocess.SubprocessError):
        raise AdmissionError("host_binding_unavailable") from None
    return root, common, directory, f"host:{machine}", daemon_id


def host_admission(
    root,
    *,
    daemon_id,
    inventory,
    limits,
    observe,
    inventory_key="home",
    kind_limits=None,
):
    """Bind this user's entrypoints to one host store; daemon keys scope services.

    daemon_id is the caller's actual engine observation, never a CLI state-dir.
    Numeric accounting spans daemons, but not other users or unsanctioned commands.
    """
    if not callable(observe):
        raise AdmissionError("resource_observer_required")
    root, common, directory, namespace, daemon_id = _host_binding(root, daemon_id)
    return Admission(
        directory,
        namespace=namespace,
        workspace_id=str(common),
        binding_id=str(root),
        daemon_id=daemon_id,
        inventory_key=f"{daemon_id}:{_text(inventory_key)}",
        inventory=inventory,
        limits=limits,
        observe=observe,
        kind_limits=kind_limits,
        strict_observation=True,
    )


def recovery_admission(root, *, daemon_id):
    """Open only existing host ownership records, without Compose inputs or budgets."""
    root, common, directory, namespace, daemon_id = _host_binding(root, daemon_id)
    path = (
        directory / hashlib.sha256(namespace.encode()).hexdigest() / "admission.sqlite3"
    )
    if not path.is_file():
        raise AdmissionError("admission_recovery_state_missing")
    handle = object.__new__(Admission)
    handle.namespace, handle.workspace_id = namespace, str(common)
    handle.binding_id, handle.daemon_id = str(root), daemon_id
    handle.path, handle.recovery_only = path, True
    # No inferred resource limits exist on this release-only handle.
    handle.inventory, handle.limits, handle.kind_limits = [], None, {}
    handle.inventory_key, handle.observe, handle.strict_observation = "", None, True
    return handle
