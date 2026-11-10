"""Capacity admission and metadata reconciliation for local SQLite copies."""

from __future__ import annotations

import contextlib
import fcntl
import os
import uuid
from pathlib import Path

from scripts.lib.ops.memory_capacity import (
    COPY_BYTES,
    CapacityError,
    MemoryCapacity,
    _directory,
    _regular,
    local_allocation,
    operation_fingerprint,
    validate_copy_context,
)


@contextlib.contextmanager
def local_copy_guard(manager: MemoryCapacity):
    """A local SQLite copy spawns no child; this lock spans its whole I/O."""
    path = manager.path.parent / "copy.lock"
    descriptor = None
    try:
        _directory(path.parent)
        descriptor = os.open(path, os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o600)
        if _regular(path).st_size:
            raise CapacityError()
        fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
        yield
    except BlockingIOError as error:
        raise CapacityError(
            "MEMORY_COPY_BUSY: another backup or restore is running"
        ) from error
    except OSError as error:
        raise CapacityError() from error
    finally:
        if descriptor is not None:
            os.close(descriptor)


def _local_results(manager: MemoryCapacity, context: dict) -> list[dict]:
    validate_copy_context(manager.memory_path, context)
    source, target = Path(context["source"]), Path(context["target"])
    temporary = Path(context["temporary"])
    paths = {
        source,
        target,
        temporary,
        temporary.with_name(temporary.name + "-journal"),
    }
    allocations = []
    for path in sorted(paths):
        if path == manager.memory_path:
            continue
        if path.exists() or path.is_symlink():
            allocations.append(local_allocation(path))
    return allocations


def run_local_copy(
    manager: MemoryCapacity,
    producer: str,
    source: Path,
    target: Path,
    action,
    *,
    temporary: Path | None = None,
) -> None:
    """Record a local copy's paths before I/O, retaining uncertainty on interruption."""
    if temporary is None:
        temporary = (
            target.with_name("." + target.name + ".tmp")
            if producer == "manual-backup"
            else target.with_name("." + target.name + ".restore-" + uuid.uuid4().hex)
        )
    context = {
        "producer": producer,
        "source": str(source.absolute()),
        "target": str(target.absolute()),
        "temporary": str(temporary.absolute()),
    }
    with local_copy_guard(manager):
        if producer == "restore":
            local_allocation(source)
        key = producer + ":" + uuid.uuid4().hex
        manager.reserve(
            key, operation_fingerprint(context), 3 * COPY_BYTES, context=context
        )
        try:
            action()
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as original:
            try:
                manager.settle(
                    key,
                    _local_results(manager, context),
                    result={"operation_outcome": "failed"},
                )
            except CapacityError as accounting_error:
                # Unreadable or unsafe retained files keep the reservation;
                # preserve the primary operation failure and its accounting cause.
                raise original from accounting_error
            raise
        manager.settle(
            key,
            _local_results(manager, context),
            result={"operation_outcome": "completed"},
        )


def reconcile_local_copies(manager: MemoryCapacity) -> dict:
    """Reconcile capacity only after no registered local copy can finish late."""
    with local_copy_guard(manager):
        for operation in manager.status().get("pending_operations", []):
            context = operation.get("context")
            if not isinstance(context, dict) or context.get("producer") not in {
                "manual-backup",
                "restore",
            }:
                continue
            allocations = _local_results(manager, context)
            manager.resolve(
                operation["request_key"],
                allocations,
                result={"operation_outcome": "unknown", "capacity_only": True},
                evidence_ref="inactive local copy producer lock and complete retained-file metadata",
            )
    return manager.status()
