"""Host-only, metadata-bound admission for memory-containing Restic jobs.

The admission is an accidental-bypass guard for registered entrypoints, not
authentication against an operator who can run arbitrary Docker commands.
"""

from __future__ import annotations

import contextlib
import fcntl
import hashlib
import json
import os
import re
import resource
import secrets
import stat
import subprocess
import tempfile
import uuid
from pathlib import Path

from scripts.lib.ops.memory_capacity import (
    CapacityError,
    MemoryCapacity,
    validate_backup_destination,
)
from scripts.lib.ops.memory_local import reconcile_local_copies

MEMORY_EXPORT = "/src/state/exports/agent-memory.sqlite3"
SNAPSHOT_BYTES = 64 * 1024 * 1024
MAX_OUTPUT_BYTES = 4 * 1024 * 1024
MAX_SNAPSHOTS = 4096
HEX_ID = re.compile(r"[0-9a-f]{64}\Z")
SIZE_LINE = re.compile(r"^R2 repository size: ([0-9]+) bytes$", re.MULTILINE)


class BackupError(Exception):
    """A sanitized refusal; a pending reservation must stay charged."""

    code = 4


def _default_runner(argv, *, input=None, timeout=60):
    # Anonymous files bound capture without retaining private diagnostics or
    # buffering an unbounded child's output in Python memory.
    with tempfile.TemporaryFile() as output:
        result = subprocess.run(
            argv,
            input=None if input is None else input.encode(),
            stdout=output,
            stderr=subprocess.DEVNULL,
            timeout=timeout,
            check=False,
            preexec_fn=_capture_limit,
        )
        output.seek(0)
        captured = output.read(MAX_OUTPUT_BYTES + 1)
    if len(captured) > MAX_OUTPUT_BYTES:
        raise BackupError("MEMORY_BACKUP_REFUSED: output exceeded its bound")
    return subprocess.CompletedProcess(argv, result.returncode, captured.decode(), "")


def _capture_limit():
    """Bound capture files too; failure stays an uncertain reserved operation."""
    _, hard = resource.getrlimit(resource.RLIMIT_FSIZE)
    ceiling = (
        MAX_OUTPUT_BYTES
        if hard == resource.RLIM_INFINITY
        else min(hard, MAX_OUTPUT_BYTES)
    )
    resource.setrlimit(resource.RLIMIT_FSIZE, (ceiling, ceiling))


class DockerMetadata:
    def __init__(self, memory_path, runner=None):
        self.root = Path(memory_path).absolute().parent.parent
        self.runner = runner or _default_runner
        self.compose = [
            "docker",
            "compose",
            "--project-directory",
            str(self.root),
            "--profile",
            "backup",
        ]
        self.config = None
        self.snapshots = {"state": [], "offsite": []}
        self.repositories = {}
        self.offsite = False

    def call(self, argv, *, input=None, writing=False):
        try:
            result = self.runner(argv, input=input, timeout=14400 if writing else 60)
            output = result.stdout
            if not isinstance(output, str) or len(output.encode()) > MAX_OUTPUT_BYTES:
                raise BackupError("MEMORY_BACKUP_REFUSED: invalid metadata output")
            if result.returncode:
                error = BackupError(
                    "MEMORY_BACKUP_REFUSED: backup metadata or operation failed"
                )
                # The pre-existing R2 size metric remains observable even if
                # its physical-size guard refused the copy.
                match = SIZE_LINE.search(output)
                error.offsite_repo_bytes = int(match[1]) if match else None
                raise error
            return output
        except (OSError, UnicodeError, subprocess.SubprocessError) as error:
            raise BackupError(
                "MEMORY_BACKUP_REFUSED: transport unavailable; reservation retained"
            ) from error

    def json(self, argv):
        try:
            return json.loads(self.call(argv))
        except (ValueError, RecursionError) as error:
            raise BackupError("MEMORY_BACKUP_REFUSED: invalid metadata") from error

    def command(self, location, *arguments):
        service = "restic" if location == "state" else "restic-offsite"
        prefix = [*self.compose, "run", "--rm", "--no-deps", service, "cmd"]
        return [*prefix, *(["state"] if location == "state" else []), *arguments]

    def load_config(self):
        config = self.json(
            [*self.compose, "config", "--format", "json", "restic", "restic-offsite"]
        )
        try:
            services = config["services"]
            environment = services["restic-offsite"]["environment"]
            account = environment.get("BACKUP_OFFSITE_R2_ACCOUNT_ID")
            bucket = environment.get("BACKUP_OFFSITE_R2_BUCKET")
            if bool(account) != bool(bucket):
                raise ValueError("partial offsite configuration")
            volumes = services["restic"]["volumes"]
            exports = [
                row["source"]
                for row in volumes
                if row["target"] == "/src/state/exports"
            ]
            if len(exports) != 1 or not Path(exports[0]).is_absolute():
                raise ValueError("missing export location")
        except (KeyError, TypeError, ValueError) as error:
            raise BackupError(
                "MEMORY_BACKUP_REFUSED: incomplete backup configuration"
            ) from error
        self.config = config
        self.offsite = bool(account and bucket)
        return Path(exports[0]) / "agent-memory.sqlite3"

    def has_memory(self, location, snapshot_id):
        output = self.call(
            self.command(location, "ls", "--json", snapshot_id, MEMORY_EXPORT)
        )
        seen = False
        try:
            lines = [json.loads(line) for line in output.splitlines() if line.strip()]
            if not lines or any(not isinstance(row, dict) for row in lines):
                raise ValueError("missing snapshot listing")
            for row in lines:
                if row.get("path") != MEMORY_EXPORT:
                    continue
                size = row.get("size")
                if (
                    row.get("type") != "file"
                    or type(size) is not int
                    or not 0 < size <= SNAPSHOT_BYTES
                    or seen
                ):
                    raise ValueError("invalid memory export metadata")
                seen = True
        except (ValueError, TypeError, RecursionError) as error:
            raise BackupError(
                "MEMORY_BACKUP_REFUSED: memory snapshot metadata unavailable"
            ) from error
        return seen

    def collect(self):
        export = self.load_config()
        external = []
        for location in ("state", "offsite") if self.offsite else ("state",):
            repository = self.json(self.command(location, "cat", "config"))
            repository_id = (
                repository.get("id") if isinstance(repository, dict) else None
            )
            if not isinstance(repository_id, str) or not HEX_ID.fullmatch(
                repository_id
            ):
                raise BackupError("MEMORY_BACKUP_REFUSED: invalid repository identity")
            self.repositories[location] = repository_id
            snapshots = self.json(self.command(location, "snapshots", "--json"))
            if not isinstance(snapshots, list) or len(snapshots) > MAX_SNAPSHOTS:
                raise BackupError(
                    "MEMORY_BACKUP_REFUSED: incomplete snapshot inventory"
                )
            seen = set()
            for snapshot in snapshots:
                if not isinstance(snapshot, dict):
                    raise BackupError(
                        "MEMORY_BACKUP_REFUSED: invalid snapshot metadata"
                    )
                identity, tree = snapshot.get("id"), snapshot.get("tree")
                if (
                    not isinstance(identity, str)
                    or not HEX_ID.fullmatch(identity)
                    or identity in seen
                    or not isinstance(tree, str)
                    or not HEX_ID.fullmatch(tree)
                ):
                    raise BackupError(
                        "MEMORY_BACKUP_REFUSED: invalid snapshot identity"
                    )
                seen.add(identity)
                tags = snapshot.get("tags", [])
                if not isinstance(tags, list):
                    raise BackupError("MEMORY_BACKUP_REFUSED: invalid snapshot tags")
                original = snapshot.get("original")
                if original is not None and (
                    not isinstance(original, str) or not HEX_ID.fullmatch(original)
                ):
                    raise BackupError(
                        "MEMORY_BACKUP_REFUSED: invalid original snapshot identity"
                    )
                if "hyhome-state" not in tags:
                    continue
                if not self.has_memory(location, identity):
                    continue
                self.snapshots[location].append(
                    {"id": identity, "tree": tree, "tags": tags, "original": original}
                )
                external.append(
                    {
                        "repository_id": repository_id,
                        "snapshot_id": identity,
                        "location": location,
                        "evidence_ref": f"restic-metadata:{repository_id}:{identity}",
                    }
                )
        return export, external


def _known_local_paths(memory_path):
    try:
        status = MemoryCapacity(memory_path).status()
    except CapacityError:
        return []
    return [
        row["location"]
        for row in status.get("allocations", [])
        if row.get("kind") == "local"
    ]


def _validated_legacy_paths(memory_path, legacy_outputs):
    legacy_paths = []
    for value in legacy_outputs:
        path = Path(value)
        if not path.is_absolute():
            raise BackupError("MEMORY_BACKUP_REFUSED: unsafe legacy backup location")
        try:
            validate_backup_destination(Path(memory_path), path)
        except CapacityError as error:
            raise BackupError(
                "MEMORY_BACKUP_REFUSED: unsafe legacy backup location"
            ) from error
        legacy_paths.append(str(path))
    return legacy_paths


def _inventory(memory_path, transport, legacy_outputs=()):
    legacy_paths = _validated_legacy_paths(memory_path, legacy_outputs)
    export, external = transport.collect()
    paths = {str(export)}
    manual = Path.home() / "backups/agent-memory/memory.sqlite3"
    if manual.parent.exists():
        paths.add(str(manual))
    paths.update(_known_local_paths(memory_path))
    paths.update(legacy_paths)
    return {
        "schema_version": 1,
        "complete": True,
        "local_paths": sorted(paths),
        "external_snapshots": external,
        "observed_repositories": [
            {"repository_id": repository_id, "location": location}
            for location, repository_id in sorted(transport.repositories.items())
        ],
    }


def inventory(memory_path, *, runner=None):
    """Produce complete metadata inventory from the fixed configured producers."""
    return _inventory(memory_path, DockerMetadata(memory_path, runner))


def reconcile_backups(
    memory_path, *, runner=None, expected_generation=None, legacy_outputs=()
):
    """Reconcile confirmed results; absence never proves a stopped Docker job."""
    _validated_legacy_paths(memory_path, legacy_outputs)
    ledger = MemoryCapacity(memory_path)
    generation = (
        ledger.status().get("generation", 0)
        if expected_generation is None
        else expected_generation
    )
    if not Path(memory_path).absolute().parent.exists():
        # First adoption cannot race a registered producer: none can reserve
        # against a missing ledger. Recollect below under the producer lock.
        ledger.reconcile(
            _inventory(
                memory_path, DockerMetadata(memory_path, runner), legacy_outputs
            ),
            expected_generation=generation,
        )
        generation = ledger.status()["generation"]
    with _backup_lock(memory_path):
        transport = DockerMetadata(memory_path, runner)
        terminal = _assert_no_live_writers(transport)
        observed = _inventory(memory_path, transport, legacy_outputs)
        ledger.reconcile(observed, expected_generation=generation)
        reconcile_local_copies(ledger)
        resolved = []
        for operation in ledger.status().get("pending_operations", []):
            key = operation["request_key"]
            for target in ("state", "offsite") if transport.offsite else ("state",):
                try:
                    previous = ledger.operation(key, _fingerprint(transport, target))
                except CapacityError:
                    continue
                if previous is None or previous["state"] != "pending":
                    continue
                name = _container_name(transport, key)
                if not _successful_terminal(terminal, name, target, key):
                    continue
                proof = _confirmed_snapshots(transport, target, key, observed)
                if proof is None:
                    continue
                result = {
                    "result": "CAPACITY_RECONCILED",
                    "target": target,
                    "request_key": key,
                    "snapshot_count": len(proof),
                }
                ledger.resolve(
                    key,
                    proof,
                    result=result,
                    evidence_ref=f"terminal owned container {name}; complete snapshot metadata",
                )
                _cleanup_terminal(transport, name)
                resolved.append(key)
        return {**ledger.status(), "resolved_operations": resolved}


def _confirmed_snapshots(transport, target, key, observed):
    if target == "state":
        tag = "memory-op-" + hashlib.sha256(key.encode()).hexdigest()
        identities = {
            row["id"] for row in transport.snapshots["state"] if tag in row["tags"]
        }
        if not identities:
            return None
    else:
        sources = {row["id"] for row in transport.snapshots["state"]}
        remote = {
            row["original"] or row["id"] for row in transport.snapshots["offsite"]
        }
        if not sources <= remote:
            return None
        identities = {
            row["id"]
            for row in transport.snapshots["offsite"]
            if (row["original"] or row["id"]) in sources
        }
    return [
        _allocation(row)
        for row in observed["external_snapshots"]
        if row["location"] == target and row["snapshot_id"] in identities
    ]


def _allocation(row):
    return {
        "resource_key": f"external:{row['location']}:{row['repository_id']}:{row['snapshot_id']}",
        "kind": "external",
        "location": row["location"],
        "charged_bytes": SNAPSHOT_BYTES,
        "evidence_ref": row["evidence_ref"],
    }


def run_backup(memory_path, target, *, request_key=None, runner=None):
    """Reserve once, run one fixed producer, then settle confirmed snapshots."""
    if target not in {"state", "offsite"}:
        raise BackupError("MEMORY_BACKUP_REFUSED: unsupported backup target")
    request_key = request_key or f"backup-{uuid.uuid4().hex}"
    if not isinstance(request_key, str) or not re.fullmatch(
        r"[A-Za-z0-9_.:-]{1,128}", request_key
    ):
        raise BackupError("MEMORY_BACKUP_REFUSED: invalid request identity")
    if MemoryCapacity(memory_path).status().get("inventory_state") != "complete":
        raise BackupError(
            "MEMORY_BACKUP_REFUSED: capacity inventory unverified; reconcile before growth"
        )
    with _backup_lock(memory_path):
        return _run_backup(memory_path, target, request_key, runner)


@contextlib.contextmanager
def _backup_lock(memory_path):
    directory = Path(memory_path).absolute().parent
    descriptor = None
    try:
        observed = directory.stat()
        if (
            directory.resolve() != directory
            or observed.st_uid != os.geteuid()
            or stat.S_IMODE(observed.st_mode) != 0o700
        ):
            raise BackupError("MEMORY_BACKUP_REFUSED: unsafe coordinator directory")
        descriptor = os.open(
            directory / "backup.lock", os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o600
        )
        observed = os.fstat(descriptor)
        if (
            not stat.S_ISREG(observed.st_mode)
            or observed.st_nlink != 1
            or observed.st_uid != os.geteuid()
            or stat.S_IMODE(observed.st_mode) != 0o600
        ):
            raise BackupError("MEMORY_BACKUP_REFUSED: unsafe coordinator lock")
        fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
        yield
    except OSError as error:
        raise BackupError(
            "MEMORY_BACKUP_REFUSED: coordinator unavailable or busy"
        ) from error
    finally:
        if descriptor is not None:
            os.close(descriptor)


def _fingerprint(transport, target):
    return hashlib.sha256(
        json.dumps(
            {
                "root": str(transport.root),
                "target": target,
                "repositories": transport.repositories,
            },
            sort_keys=True,
        ).encode()
    ).hexdigest()


def _owner(transport):
    return hashlib.sha256(str(transport.root).encode()).hexdigest()


def _container_name(transport, request_key):
    request_digest = hashlib.sha256(request_key.encode()).hexdigest()
    return f"hyhome-memory-{_owner(transport)[:16]}-{request_digest[:16]}"


def _assert_no_live_writers(transport):
    output = transport.call(
        [
            "docker",
            "container",
            "ls",
            "--all",
            "--filter",
            "label=hyhome.memory.owner=" + _owner(transport),
            "--format",
            "{{json .Names}}",
        ]
    )
    terminal = {}
    for line in output.splitlines():
        try:
            name = json.loads(line)
        except ValueError as error:
            raise BackupError(
                "MEMORY_BACKUP_REFUSED: container inventory unavailable"
            ) from error
        if not isinstance(name, str) or not re.fullmatch(
            r"hyhome-memory-[0-9a-f]{16}-[0-9a-f]{16}", name
        ):
            raise BackupError("MEMORY_BACKUP_REFUSED: unknown coordinator container")
        labels = transport.json(
            ["docker", "inspect", "--format", "{{json .Config.Labels}}", name]
        )
        state = transport.json(
            ["docker", "inspect", "--format", "{{json .State}}", name]
        )
        if (
            not isinstance(labels, dict)
            or labels.get("hyhome.memory.owner") != _owner(transport)
            or labels.get("hyhome.memory.target") not in {"state", "offsite"}
        ):
            raise BackupError("MEMORY_BACKUP_REFUSED: coordinator ownership unknown")
        request = labels.get("hyhome.memory.request", "")
        if not isinstance(request, str) or not HEX_ID.fullmatch(request):
            raise BackupError("MEMORY_BACKUP_REFUSED: coordinator ownership unknown")
        expected = f"hyhome-memory-{_owner(transport)[:16]}-{request[:16]}"
        if (
            name != expected
            or not isinstance(state, dict)
            or state.get("Status") not in {"exited", "dead"}
            or state.get("Running") is not False
        ):
            raise BackupError(
                "MEMORY_BACKUP_REFUSED: earlier coordinator is active or unknown"
            )
        terminal[name] = {"labels": labels, "state": state}
    return terminal


def _successful_terminal(terminal, name, target, request_key):
    if (
        name not in terminal
        or terminal[name]["labels"]["hyhome.memory.target"] != target
        or terminal[name]["labels"]["hyhome.memory.request"]
        != hashlib.sha256(request_key.encode()).hexdigest()
    ):
        return False
    state = terminal[name]["state"]
    return (
        state.get("Status") == "exited"
        and type(state.get("ExitCode")) is int
        and state["ExitCode"] == 0
        and state.get("OOMKilled") is False
        and state.get("Dead") is False
        and state.get("Error") == ""
    )


def _cleanup_terminal(transport, name):
    # Never force-stop or remove volumes. Only a label-validated terminal
    # container of this exact request reaches this call.
    transport.call(["docker", "container", "rm", name])


def _pending_backup(ledger, transport):
    for operation in ledger.status().get("pending_operations", []):
        for target in ("state", "offsite") if transport.offsite else ("state",):
            try:
                previous = ledger.operation(
                    operation["request_key"], _fingerprint(transport, target)
                )
            except CapacityError:
                continue
            if previous is not None and previous["state"] == "pending":
                return True
    return False


def _run_backup(memory_path, target, request_key, runner):
    ledger = MemoryCapacity(memory_path)
    generation = ledger.status()["generation"]
    transport = DockerMetadata(memory_path, runner)
    terminal = _assert_no_live_writers(transport)
    before = _inventory(memory_path, transport)
    if target == "offsite" and not transport.offsite:
        raise BackupError("MEMORY_BACKUP_REFUSED: offsite is not configured")
    ledger.reconcile(before, expected_generation=generation)
    # Snapshot identities, not trees, consume allocation. Existing exact
    # original identities are already charged; identical trees alone never
    # prove that a distinct source snapshot was copied.
    copied = {row["original"] or row["id"] for row in transport.snapshots["offsite"]}
    pending = (
        1
        if target == "state"
        else sum(row["id"] not in copied for row in transport.snapshots["state"])
    )
    fingerprint = _fingerprint(transport, target)
    previous_operation = ledger.operation(request_key, fingerprint)
    if previous_operation is not None:
        if previous_operation["state"] == "completed":
            name = _container_name(transport, request_key)
            if name in terminal:
                _cleanup_terminal(transport, name)
            return previous_operation["result"]
        raise BackupError(
            "MEMORY_BACKUP_REFUSED: earlier operation is unresolved; reconcile its result"
        )
    if _pending_backup(ledger, transport):
        raise BackupError(
            "MEMORY_BACKUP_REFUSED: an earlier backup is unresolved; reconcile its result"
        )
    reservation = ledger.reserve(request_key, fingerprint, pending * SNAPSHOT_BYTES)
    if reservation["state"] == "completed":
        return reservation["result"]
    if reservation.get("replay"):
        raise BackupError(
            "MEMORY_BACKUP_REFUSED: earlier operation is unresolved; reconcile its result"
        )
    # The exact target/request admission is generated only after the durable
    # reservation. Neither token nor command output is exposed in evidence.
    request_digest = hashlib.sha256(request_key.encode()).hexdigest()
    admission = (
        f"HYHOME_MEMORY_BUDGET_V1 {target} {request_digest} {secrets.token_hex(32)}\n"
    )
    digest = hashlib.sha256(admission.encode()).hexdigest()
    service, action = (
        ("restic", "budget-backup")
        if target == "state"
        else ("restic-offsite", "budget-copy")
    )
    argv = [
        *transport.compose,
        "run",
        "--no-deps",
        "-T",
        "--name",
        _container_name(transport, request_key),
        "--label",
        "hyhome.memory.owner=" + _owner(transport),
        "--label",
        "hyhome.memory.request=" + request_digest,
        "--label",
        "hyhome.memory.target=" + target,
        "--env",
        f"HYHOME_MEMORY_ADMISSION_SHA256={digest}",
        service,
        action,
    ]
    output = transport.call(argv, input=admission, writing=True)
    terminal = _assert_no_live_writers(transport)
    name = _container_name(transport, request_key)
    if not _successful_terminal(terminal, name, target, request_key):
        raise BackupError(
            "MEMORY_BACKUP_REFUSED: exact terminal operation receipt missing; reservation retained"
        )
    after = _inventory(memory_path, DockerMetadata(memory_path, runner))
    previous = {
        _allocation(row)["resource_key"] for row in before["external_snapshots"]
    }
    added = [
        _allocation(row)
        for row in after["external_snapshots"]
        if _allocation(row)["resource_key"] not in previous
    ]
    if any(row["location"] != target for row in added):
        raise BackupError(
            "MEMORY_BACKUP_REFUSED: concurrent snapshot change; reservation retained"
        )
    result = {
        "target": target,
        "request_key": request_key,
        "snapshot_count": len(added),
        "result": "PASS",
    }
    match = SIZE_LINE.search(output)
    if target == "offsite":
        if not match:
            raise BackupError(
                "MEMORY_BACKUP_REFUSED: offsite size observation missing; reservation retained"
            )
        result["offsite_repo_bytes"] = int(match[1])
    ledger.settle(request_key, added, result=result)
    _cleanup_terminal(transport, name)
    return result
