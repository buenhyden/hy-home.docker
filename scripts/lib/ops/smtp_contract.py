"""SMTP01 fail-closed source/retirement contract; receipts are facts, not authority."""

from __future__ import annotations

import argparse
import ctypes
import errno
import fcntl
import hashlib
import json
import os
import re
import secrets
import socket
import stat
import subprocess
from contextlib import ExitStack, contextmanager
from copy import deepcopy
from datetime import UTC, datetime, timedelta
from pathlib import Path

CANONICAL = "smtp_password"
OLD = "supabase_smtp_password"
CANONICAL_PATH = "secrets/communication/smtp/smtp_password.txt"
OLD_PATH = "secrets/communication/supabase/supabase_smtp_password.txt"
METADATA_PATH = "secrets/SENSITIVE_ENV_VARS.md"
LOCK_PATH = "secrets/.smtp01-retirement.lock"
ALIAS_HEADER = b"| Retired ID | Canonical ID |\n| --- | --- |\n"
ALIAS_ROW = b"| COMM-003 | COMM-002 |\n"
MAX_PROOF_BYTES = 32_768
PROOF_OPERATION = "retire-supabase-smtp"
PROOF_TARGET = "COMM-003"
PROOF_KEYS = frozenset(
    {
        "host",
        "git_sha",
        "source_sha256",
        "old_mount_consumers",
        "job_backup_external_verified",
        "canonical_restore_mapping_verified",
        "consumer_creation_quiesced",
        "source_private_mutation_quiesced",
        "root_identity",
        "operation",
        "target",
        "observation_id",
        "approval_record",
        "observed_at",
        "expires_at",
    }
)
_SAFE_PROOF_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:/-]{0,127}\Z")
_UTC_TIMESTAMP = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z\Z")


class ContractError(ValueError):
    """A fixed, non-sensitive failure code."""


def grants(service):
    """Validate grant shapes and distinct source/target ownership."""
    items = service.get("secrets", [])
    if not isinstance(items, list):
        raise ContractError("invalid_secret_reference")
    sources, targets, result = set(), set(), []
    for item in items:
        if isinstance(item, str):
            source = target = item
        elif isinstance(item, dict):
            source = item.get("source")
            target = item.get("target", source)
        else:
            raise ContractError("invalid_secret_reference")
        if (
            not isinstance(source, str)
            or not source
            or not isinstance(target, str)
            or not target
        ):
            raise ContractError("invalid_secret_reference")
        if source in sources or target in targets:
            raise ContractError("duplicate_secret_reference")
        sources.add(source)
        targets.add(target)
        result.append((source, target))
    return result


def unify(model):
    out = deepcopy(model)
    definitions = out.get("secrets", {})
    if not isinstance(definitions, dict):
        raise ContractError("canonical_secret_drift")
    for name, expected in ((CANONICAL, CANONICAL_PATH), (OLD, OLD_PATH)):
        if name == OLD and name not in definitions:
            continue
        entry = definitions.get(name)
        if not isinstance(entry, dict) or entry.get("file") not in (
            expected,
            "./" + expected,
        ):
            raise ContractError(
                "canonical_secret_drift" if name == CANONICAL else "old_secret_drift"
            )
    for name, entry in definitions.items():
        if not isinstance(entry, dict):
            raise ContractError("invalid_secret_definition")
        filename = entry.get("file")
        if filename in (CANONICAL_PATH, "./" + CANONICAL_PATH) and name != CANONICAL:
            raise ContractError("duplicate_secret_source")
        if filename in (OLD_PATH, "./" + OLD_PATH) and name != OLD:
            raise ContractError("duplicate_secret_source")
    services = out.get("services", {})
    if not isinstance(services, dict):
        raise ContractError("invalid_services")
    for service in services.values():
        if not isinstance(service, dict):
            raise ContractError("invalid_service")
        grants(service)
        if "secrets" not in service:
            continue
        rewritten = []
        for item in service["secrets"]:
            if item == OLD:
                item = {"source": CANONICAL, "target": OLD}
            elif isinstance(item, dict) and item["source"] == OLD:
                item = dict(item, source=CANONICAL)
                item.setdefault("target", OLD)
            rewritten.append(item)
        service["secrets"] = rewritten
        grants(service)
    definitions.pop(OLD, None)
    return out


def summarize(model):
    changed = unify(model)
    return {
        "canonical_file": CANONICAL_PATH,
        "retired_file": OLD_PATH,
        "changed_services": [
            name
            for name, service in changed.get("services", {}).items()
            if service != model["services"][name]
        ],
        "source_definition_removed": OLD in model.get("secrets", {}),
        "applied": False,
        "native_smtp_verified": False,
    }


def metadata_retired(data):
    """Remove only the exact retired value row; preserve every other byte."""
    rows, retired, canonical, aliases = [], 0, 0, 0
    for line in data.splitlines(keepends=True):
        cells = [cell.strip().strip(b"*`").strip() for cell in line.split(b"|")]
        identifier = cells[1] if len(cells) > 2 else b""
        if identifier == b"COMM-002":
            if len(cells) != 10:
                raise ContractError("metadata_canonical_drift")
            canonical += 1
            if cells[6] != CANONICAL_PATH.encode():
                raise ContractError("metadata_canonical_drift")
        if len(cells) == 10 and identifier == b"COMM-003":
            retired += 1
            if cells[6] != OLD_PATH.encode():
                raise ContractError("metadata_retired_drift")
            continue
        if identifier == b"COMM-003":
            if len(cells) != 4 or cells[2] != b"COMM-002":
                raise ContractError("metadata_alias_drift")
            aliases += 1
        rows.append(line)
    if canonical != 1 or retired > 1 or aliases > 1:
        raise ContractError("metadata_ownership_drift")
    result = b"".join(rows)
    if not aliases:
        separator = b"" if not result or result.endswith(b"\n") else b"\n"
        result += separator + b"\n" + ALIAS_HEADER + ALIAS_ROW
    return result


def _identity(info):
    return (info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns, info.st_ctime_ns)


def _directory(root, relative, stack):
    """Walk and retain directory descriptors; never follow symlink parents."""
    flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    if any(path.is_symlink() for path in (Path(root), *Path(root).parents)):
        raise ContractError("unsafe_root_path")
    fd = os.open(root, flags)
    stack.callback(os.close, fd)
    for part in Path(relative).parts:
        fd = os.open(part, flags, dir_fd=fd)
        stack.callback(os.close, fd)
    return fd


def root_identity(root):
    """Return public filesystem identity; never resolves private file content."""
    with ExitStack() as stack:
        info = os.fstat(_directory(Path(root).absolute(), "", stack))
        return {"st_dev": info.st_dev, "st_ino": info.st_ino}


@contextmanager
def retirement_lock(root, expected_identity=None):
    """SMTP01 cooperative exclusive lock on this exact root.

    The persistent lock is nofollow, owner-only and single-link. Quiescence
    receipts remain necessary for actors that do not honor this protocol.
    """
    root = Path(root).absolute()
    with ExitStack() as stack:
        rootfd = _directory(root, "", stack)
        info = os.fstat(rootfd)
        identity = {"st_dev": info.st_dev, "st_ino": info.st_ino}
        if expected_identity is not None and identity != expected_identity:
            raise ContractError("root_identity_mismatch")
        parent = os.open(
            "secrets", os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=rootfd
        )
        stack.callback(os.close, parent)
        fd = os.open(
            Path(LOCK_PATH).name,
            os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW | os.O_NONBLOCK,
            0o600,
            dir_fd=parent,
        )
        stack.callback(os.close, fd)
        lock = os.fstat(fd)
        if (
            not stat.S_ISREG(lock.st_mode)
            or lock.st_nlink != 1
            or stat.S_IMODE(lock.st_mode) != 0o600
            or lock.st_uid != os.geteuid()
        ):
            raise ContractError("unsafe_lock_file")
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise ContractError("retirement_lock_busy") from None
        named = os.stat(Path(LOCK_PATH).name, dir_fd=parent, follow_symlinks=False)
        if (named.st_dev, named.st_ino) != (lock.st_dev, lock.st_ino):
            raise ContractError("retirement_lock_replaced")
        if root_identity(root) != identity:
            raise ContractError("root_identity_mismatch")
        yield identity
        named = os.stat(Path(LOCK_PATH).name, dir_fd=parent, follow_symlinks=False)
        if (named.st_dev, named.st_ino) != (lock.st_dev, lock.st_ino):
            raise ContractError("retirement_lock_replaced")
        if root_identity(root) != identity:
            raise ContractError("root_identity_mismatch")


def _snapshot(parent, name, stack, required=True):
    try:
        fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=parent)
    except FileNotFoundError:
        if required:
            raise ContractError("required_file_missing") from None
        return None
    stack.callback(os.close, fd)
    info = os.fstat(fd)
    if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
        raise ContractError("unsafe_file_type")
    with os.fdopen(os.dup(fd), "rb") as stream:
        content = stream.read()
    if _identity(info) != _identity(os.fstat(fd)):
        raise ContractError("concurrent_file_change")
    return (fd, _identity(info), content)


def _unchanged(parent, name, snapshot):
    if _identity(os.stat(name, dir_fd=parent, follow_symlinks=False)) != snapshot[1]:
        raise ContractError("concurrent_file_change")
    os.lseek(snapshot[0], 0, os.SEEK_SET)
    with os.fdopen(os.dup(snapshot[0]), "rb") as stream:
        current = stream.read()
    if current != snapshot[2] or _identity(os.fstat(snapshot[0])) != snapshot[1]:
        raise ContractError("concurrent_file_change")


def _source_documents(root):
    import yaml

    from scripts.lib.document_governance.operations_catalog import _ComposeLoader

    pending, hashes, documents = ["docker-compose.yml"], {}, []
    while pending:
        relative = pending.pop()
        if relative in hashes:
            continue
        path = root / relative
        if not path.is_relative_to(root) or ".." in path.relative_to(root).parts:
            raise ContractError("unsafe_compose_path")
        if any(part.is_symlink() for part in (path, *path.parents)):
            raise ContractError("unsafe_compose_path")
        data = path.read_bytes()
        hashes[relative] = hashlib.sha256(data).hexdigest()
        try:
            document = yaml.load(data, Loader=_ComposeLoader)
        except yaml.YAMLError:
            raise ContractError("invalid_compose_document") from None
        if not isinstance(document, dict):
            raise ContractError("invalid_compose_document")
        if relative != "docker-compose.yml":
            definitions = document.get("secrets", {})
            if not isinstance(definitions, dict):
                raise ContractError("invalid_secret_definition")
            for _name, entry in definitions.items():
                filename = entry.get("file") if isinstance(entry, dict) else None
                if isinstance(filename, str):
                    resolved = Path(os.path.abspath(path.parent / filename))
                    if resolved in (root / CANONICAL_PATH, root / OLD_PATH):
                        raise ContractError("included_smtp_redefinition")
        documents.append(document)
        for include in document.get("include", []):
            item = (
                include
                if isinstance(include, str)
                else (include.get("path") if isinstance(include, dict) else None)
            )
            if not isinstance(item, str):
                raise ContractError("unsafe_compose_path")
            resolved = path.parent / item
            pending.append(str(resolved.relative_to(root)))
    return hashes, documents


def _validate_source_documents(documents):
    root_document = documents[0]
    unified = unify(root_document)
    if unified != root_document:
        raise ContractError("source_cutover_pending")
    auth_seen = False
    for document in documents:
        if OLD_PATH in json.dumps(document):
            raise ContractError("source_cutover_pending")
        if OLD in document.get("secrets", {}):
            raise ContractError("source_cutover_pending")
        definitions = document.get("secrets", {})
        if not isinstance(definitions, dict):
            raise ContractError("invalid_secret_definition")
        if document is not root_document:
            for name, entry in definitions.items():
                filename = entry.get("file") if isinstance(entry, dict) else None
                if name == CANONICAL or filename in (
                    CANONICAL_PATH,
                    "./" + CANONICAL_PATH,
                    OLD_PATH,
                    "./" + OLD_PATH,
                ):
                    raise ContractError("included_smtp_redefinition")
        services = document.get("services", {})
        if not isinstance(services, dict):
            raise ContractError("invalid_services")
        for name, service in services.items():
            if not isinstance(service, dict):
                raise ContractError("invalid_service")
            for source, target in grants(service):
                if source == OLD:
                    raise ContractError("source_cutover_pending")
                if name == "auth" and source == CANONICAL and target == OLD:
                    auth_seen = True
    if not auth_seen:
        raise ContractError("auth_alias_missing")


def source_hashes(root):
    """Hash only public root and included Compose source, never secret files."""
    root = Path(root)
    hashes, documents = _source_documents(root)
    _validate_source_documents(documents)
    return hashes


def _run(arguments, root=None):
    return subprocess.run(
        arguments, cwd=root, check=True, capture_output=True, timeout=30
    ).stdout


def _now():
    return datetime.now(UTC)


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ContractError("audit_receipt_invalid")
        result[key] = value
    return result


def _unsafe_proof_file(before, opened):
    return (
        not stat.S_ISREG(opened.st_mode)
        or opened.st_nlink != 1
        or opened.st_uid != os.geteuid()
        or stat.S_IMODE(opened.st_mode) != 0o600
        or opened.st_size > MAX_PROOF_BYTES
        or _identity(before) != _identity(opened)
    )


def _proof_bytes(root, proof):
    path = Path(proof)
    root = Path(root).absolute()
    if (
        not path.is_absolute()
        or any(part in (".", "..") for part in path.parts)
        or path.is_relative_to(root)
        or not path.name
    ):
        raise ContractError("unsafe_audit_receipt")
    with ExitStack() as stack:
        parent = _directory(Path("/"), path.parent.relative_to("/"), stack)
        parent_info = os.fstat(parent)
        if (
            parent_info.st_uid != os.geteuid()
            or stat.S_IMODE(parent_info.st_mode) != 0o700
        ):
            raise ContractError("unsafe_audit_receipt")
        before = os.stat(path.name, dir_fd=parent, follow_symlinks=False)
        if not stat.S_ISREG(before.st_mode):
            raise ContractError("unsafe_audit_receipt")
        try:
            fd = os.open(
                path.name,
                os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK,
                dir_fd=parent,
            )
        except OSError:
            raise ContractError("unsafe_audit_receipt") from None
        stack.callback(os.close, fd)
        opened = os.fstat(fd)
        if _unsafe_proof_file(before, opened):
            raise ContractError("unsafe_audit_receipt")
        chunks, size = [], 0
        while True:
            chunk = os.read(fd, min(8192, MAX_PROOF_BYTES + 1 - size))
            if not chunk:
                break
            chunks.append(chunk)
            size += len(chunk)
            if size > MAX_PROOF_BYTES:
                raise ContractError("unsafe_audit_receipt")
        after = os.fstat(fd)
        named = os.stat(path.name, dir_fd=parent, follow_symlinks=False)
        if _identity(opened) != _identity(after) or _identity(after) != _identity(
            named
        ):
            raise ContractError("audit_receipt_changed")
        return b"".join(chunks)


def _proof_time(value):
    if not isinstance(value, str) or not _UTC_TIMESTAMP.fullmatch(value):
        raise ContractError("audit_receipt_invalid")
    try:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)
    except ValueError:
        raise ContractError("audit_receipt_invalid") from None


def _proof_receipt(root, proof):
    try:
        receipt = json.loads(
            _proof_bytes(root, proof), object_pairs_hook=_unique_object
        )
    except (json.JSONDecodeError, UnicodeDecodeError):
        raise ContractError("audit_receipt_invalid") from None
    if not isinstance(receipt, dict) or set(receipt) != PROOF_KEYS:
        raise ContractError("audit_receipt_invalid")
    for field in ("observation_id", "approval_record"):
        value = receipt[field]
        if not isinstance(value, str) or not _SAFE_PROOF_ID.fullmatch(value):
            raise ContractError("audit_receipt_invalid")
    observed = _proof_time(receipt["observed_at"])
    expires = _proof_time(receipt["expires_at"])
    now = _now()
    if (
        observed > now + timedelta(seconds=30)
        or now - observed > timedelta(minutes=5)
        or expires <= observed
        or now >= expires
        or expires - now < timedelta(minutes=5)
        or expires - observed > timedelta(minutes=15)
    ):
        raise ContractError("audit_receipt_stale")
    return receipt


def verify_proof(root, proof):
    receipt = _proof_receipt(root, proof)
    revision = _run(["git", "rev-parse", "HEAD"], root).decode().strip()
    try:
        _run(["git", "diff", "--quiet", "HEAD", "--"], root)
        _run(["git", "diff", "--cached", "--quiet"], root)
    except subprocess.SubprocessError:
        raise ContractError("tracked_source_dirty") from None
    if (
        receipt["operation"] != PROOF_OPERATION
        or receipt["target"] != PROOF_TARGET
        or receipt.get("host") != socket.gethostname()
        or receipt.get("git_sha") != revision
        or receipt.get("source_sha256") != source_hashes(root)
        or receipt.get("old_mount_consumers") != []
        or receipt.get("job_backup_external_verified") is not True
        or receipt.get("canonical_restore_mapping_verified") is not True
        or receipt.get("consumer_creation_quiesced") is not True
        or receipt.get("source_private_mutation_quiesced") is not True
        or receipt.get("root_identity") != root_identity(root)
    ):
        raise ContractError("audit_receipt_stale")
    identifiers = _run(["docker", "ps", "-aq"]).decode().split()
    if not identifiers:
        return
    # Mount-only output: no environment, labels, logs or credential payloads.
    payload = _run(["docker", "inspect", "--format", "{{json .Mounts}}", *identifiers])
    old = (Path(root) / OLD_PATH).absolute()
    for line in payload.splitlines():
        for mount in json.loads(line):
            if mount.get("Type") != "bind":
                continue
            source = Path(mount.get("Source", "")).absolute()
            if source == old or source == old.parent:
                raise ContractError("old_runtime_mount")
            if old.is_relative_to(source):
                raise ContractError("old_runtime_parent_mount")


def _rename_noreplace(parent, source, target):
    """Linux atomic rename that never overwrites a newly raced name."""
    library = ctypes.CDLL(None, use_errno=True)
    rename = getattr(library, "renameat2", None)
    if rename is None:
        raise ContractError("atomic_restore_unavailable")
    rename.argtypes = (
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_uint,
    )
    rename.restype = ctypes.c_int
    if rename(parent, os.fsencode(source), parent, os.fsencode(target), 1):
        raise OSError(ctypes.get_errno(), "atomic name transition failed")


def _quarantine_remove(parent, name, snapshot, on_mutation=None):
    """Validate the moved inode; preserve it if restore conflicts."""
    temporary = ".smtp-quarantine-" + secrets.token_hex(16)
    _rename_noreplace(parent, name, temporary)
    if on_mutation:
        on_mutation()
    try:
        moved = os.stat(temporary, dir_fd=parent, follow_symlinks=False)
        # Rename legitimately changes ctime. All other identity fields and the
        # complete content must match, and the descriptor must name this inode.
        if _identity(moved)[:-1] != snapshot[1][:-1]:
            raise ContractError("concurrent_file_change")
        adjusted = (snapshot[0], _identity(moved), snapshot[2])
        _unchanged(parent, temporary, adjusted)
        os.unlink(temporary, dir_fd=parent)
        os.fsync(parent)
    except (OSError, ContractError):
        try:
            _rename_noreplace(parent, temporary, name)
            os.fsync(parent)
        except OSError:
            raise ContractError("quarantine_restore_conflict") from None
        raise


def _remove_empty_directory(superparent, name, original):
    current = os.stat(name, dir_fd=superparent, follow_symlinks=False)
    expected = os.fstat(original)
    if (current.st_dev, current.st_ino) != (expected.st_dev, expected.st_ino):
        raise ContractError("concurrent_directory_change")
    try:
        os.rmdir(name, dir_fd=superparent)
    except OSError as error:
        if error.errno not in (errno.ENOTEMPTY, errno.EEXIST):
            raise


def _publish_metadata(parent, snapshot, updated, on_mutation=None):
    """Publish under the SMTP01 lock without replacing a raced name."""
    staged = ".smtp-retirement-" + secrets.token_hex(16)
    displaced = ".smtp-metadata-quarantine-" + secrets.token_hex(16)
    fd = os.open(
        staged,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
        0o600,
        dir_fd=parent,
    )
    moved = published = False
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(updated)
            stream.flush()
            os.fsync(stream.fileno())
        _unchanged(parent, "SENSITIVE_ENV_VARS.md", snapshot)
        _rename_noreplace(parent, "SENSITIVE_ENV_VARS.md", displaced)
        moved = True
        if on_mutation:
            on_mutation()
        info = os.stat(displaced, dir_fd=parent, follow_symlinks=False)
        if _identity(info)[:-1] != snapshot[1][:-1]:
            raise ContractError("concurrent_metadata_change")
        adjusted = (snapshot[0], _identity(info), snapshot[2])
        _unchanged(parent, displaced, adjusted)
        _rename_noreplace(parent, staged, "SENSITIVE_ENV_VARS.md")
        published = True
        os.fsync(parent)
        os.unlink(displaced, dir_fd=parent)
        moved = False
        os.fsync(parent)
    except (OSError, ContractError):
        if moved and not published:
            try:
                _rename_noreplace(parent, displaced, "SENSITIVE_ENV_VARS.md")
                moved = False
                os.fsync(parent)
            except OSError:
                raise ContractError("metadata_restore_conflict") from None
        raise
    finally:
        try:
            os.unlink(staged, dir_fd=parent)
        except FileNotFoundError:
            pass


def _old_absent(root, stack):
    try:
        parent = _directory(root, Path(OLD_PATH).parent, stack)
    except FileNotFoundError:
        return
    try:
        os.stat(Path(OLD_PATH).name, dir_fd=parent, follow_symlinks=False)
    except FileNotFoundError:
        return
    raise ContractError("old_name_recreated")


def _metadata_matches(parent, updated, stack):
    snapshot = _snapshot(parent, "SENSITIVE_ENV_VARS.md", stack)
    if snapshot[2] != updated or stat.S_IMODE(os.fstat(snapshot[0]).st_mode) != 0o600:
        raise ContractError("concurrent_metadata_change")
    _unchanged(parent, "SENSITIVE_ENV_VARS.md", snapshot)


def _retirement_inputs(root, stack):
    canonical_parent = _directory(root, Path(CANONICAL_PATH).parent, stack)
    canonical = _snapshot(canonical_parent, Path(CANONICAL_PATH).name, stack)
    if not canonical[2]:
        raise ContractError("empty_canonical")
    metadata_parent = _directory(root, "secrets", stack)
    metadata = _snapshot(metadata_parent, "SENSITIVE_ENV_VARS.md", stack)
    old_superparent = old_parent = old = None
    try:
        old_superparent = _directory(root, Path(OLD_PATH).parent.parent, stack)
        old_parent = _directory(root, Path(OLD_PATH).parent, stack)
        old = _snapshot(old_parent, Path(OLD_PATH).name, stack, required=False)
    except FileNotFoundError:
        pass
    return (
        canonical_parent,
        canonical,
        metadata_parent,
        metadata,
        old_superparent,
        old_parent,
        old,
    )


def _inputs_unchanged(
    canonical_parent, canonical, metadata_parent, metadata, old_parent, old
):
    _unchanged(canonical_parent, Path(CANONICAL_PATH).name, canonical)
    _unchanged(metadata_parent, "SENSITIVE_ENV_VARS.md", metadata)
    if old:
        _unchanged(old_parent, Path(OLD_PATH).name, old)


def _retire_name(root, proof, verifier, stack, inputs, updated, on_mutation):
    (
        canonical_parent,
        canonical,
        metadata_parent,
        _,
        old_superparent,
        old_parent,
        old,
    ) = inputs
    _unchanged(canonical_parent, Path(CANONICAL_PATH).name, canonical)
    verifier(root, proof)
    if old:
        _unchanged(old_parent, Path(OLD_PATH).name, old)
        _quarantine_remove(old_parent, Path(OLD_PATH).name, old, on_mutation)
    _old_absent(root, stack)
    verifier(root, proof)
    if old_parent is not None:
        _remove_empty_directory(old_superparent, Path(OLD_PATH).parent.name, old_parent)
    _old_absent(root, stack)
    _metadata_matches(metadata_parent, updated, stack)


def retire(
    root,
    apply=False,
    proof=None,
    verifier=verify_proof,
    before_commit=None,
    on_mutation=None,
):
    """Return (exit status, public summary); apply requires current audit facts."""
    root = Path(root).absolute()
    with ExitStack() as stack:
        if apply:
            stack.enter_context(retirement_lock(root))
        inputs = _retirement_inputs(root, stack)
        _, canonical, metadata_parent, metadata, _, old_parent, old = inputs
        updated = metadata_retired(metadata[2])
        equal = old[2] == canonical[2] if old else None
        if equal is False:
            raise ContractError("password_mismatch")
        pending = old is not None or updated != metadata[2]
        summary = {
            "status": "pending" if pending else "already_retired",
            "equal": equal,
            "applied": False,
        }
        if not apply or not pending:
            return (1 if pending else 0), summary
        if proof is None:
            raise ContractError("audit_receipt_required")
        verifier(root, proof)
        _inputs_unchanged(*inputs[:4], old_parent, old)
        if before_commit:
            before_commit()
        _inputs_unchanged(*inputs[:4], old_parent, old)
        if updated != metadata[2]:
            _publish_metadata(metadata_parent, metadata, updated, on_mutation)
        _metadata_matches(metadata_parent, updated, stack)
        _retire_name(root, proof, verifier, stack, inputs, updated, on_mutation)
        return 0, {"status": "retired", "equal": equal, "applied": True}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--retire", action="store_true")
    mode.add_argument("--retire-check", action="store_true")
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--proof", type=Path)
    args = parser.parse_args(argv)
    mutated = False

    def mark_mutation():
        nonlocal mutated
        mutated = True

    try:
        status, summary = retire(
            args.root, args.retire, args.proof, on_mutation=mark_mutation
        )
        print(json.dumps(summary, sort_keys=True))
        return status
    except (
        ValueError,
        OSError,
        TypeError,
        KeyError,
        subprocess.SubprocessError,
        ImportError,
    ):
        summary = (
            {"status": "unsafe_after_mutation", "applied": True, "completed": False}
            if mutated
            else {"status": "unsafe", "applied": False}
        )
        print(json.dumps(summary, sort_keys=True))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
