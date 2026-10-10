"""Exact private regular-file retirement; evidence never substitutes observation.

Apply requires an operator maintenance window: flock coordinates this helper and
its generator, but cannot stop unrelated or hostile writers. No secret contents
or fingerprints are read, logged, copied, or hashed. Tracked files use git rm.
"""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
import re
import stat
import subprocess
import sys
import unicodedata
from contextlib import contextmanager
from datetime import UTC, datetime, timedelta
from pathlib import Path, PurePosixPath

CHECKS = frozenset({"source", "runtime", "jobs", "backup_restore", "external"})
PROTECTED = frozenset(
    {"labs", ".git", "98.archive", ".backup", ".retired", "history", "audit"}
)
CANONICAL_SMTP = "secrets/communication/smtp/smtp_password.txt"
# Exact current cryptographic IDs remain protected even if a receipt relabels its path.
PROTECTED_IDS = frozenset(
    {
        "IAM-005",
        "SUPA-005",
        "SUPA-006",
        "SUPA-008",
        "SUPA-010",
        "STRG-008",
        "STRG-009",
        "AUTO-003",
        "AUTO-005",
        "AUTO-014",
        "AUTO-020",
        "AI-005",
        "CACHE-024",
        "COMM-002",
        "COMM-003",  # SMTP01 owns the single canonical cutover/deletion route.
        "PG-020",
    }
)
FILE_FIELDS = ("dev", "ino", "size", "mtime_ns", "ctime_ns", "mode", "nlink")
DIR_FIELDS = ("dev", "ino", "mode", "ctime_ns")
DIR_FLAGS = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC
FILE_FLAGS = os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC | os.O_NONBLOCK
MAX_MANIFEST = 1024 * 1024


def _snapshot(info, fields):
    return {name: getattr(info, "st_" + name) for name in fields}


def identity(path: Path):
    return _snapshot(Path(path).lstat(), FILE_FIELDS)


def _exact_root(root, forbidden_identity=None):
    raw = os.fspath(root)
    path = Path(raw)
    if path.anchor != "/" or raw != str(path) or ".." in path.parts:
        raise ValueError("invalid_root")
    fd = os.open("/", DIR_FLAGS)
    try:
        _check_external_ancestor(fd, forbidden_identity)
        for part in path.parts[1:]:
            next_fd = os.open(part, DIR_FLAGS, dir_fd=fd)
            os.close(fd)
            fd = next_fd
            _check_external_ancestor(fd, forbidden_identity)
        return path, fd
    except BaseException:
        os.close(fd)
        raise


def _check_external_ancestor(fd, forbidden_identity):
    info = os.fstat(fd)
    if (
        forbidden_identity is not None
        and (info.st_dev, info.st_ino) == forbidden_identity
    ):
        raise ValueError("manifest_must_be_external")


def _allowed(row):
    if not isinstance(row, dict):
        raise ValueError("invalid_entry")
    name, identifier = row.get("path"), row.get("id")
    if not isinstance(name, str) or not isinstance(identifier, str):
        raise ValueError("invalid_material_path_or_id")
    if not re.fullmatch(r"[A-Z][A-Z0-9]{1,15}-[0-9]{3,6}", identifier):
        raise ValueError("invalid_material_id")
    path = PurePosixPath(name)
    parts = path.parts
    invalid = (
        not isinstance(name, str)
        or path.is_absolute()
        or str(path) != name
        or ".." in parts
        or "\\" in name
        or any(unicodedata.category(c).startswith("C") for c in name)
        or len(parts) < 2
        or parts[0] not in {"secrets", "infra", "docs"}
        or row.get("scope") != "root"
        or row.get("kind")
        not in {"legacy-secret", "duplicate-secret", "optional-material"}
    )
    protected = (
        any(
            part in PROTECTED or part.startswith((".backup-", ".retired"))
            for part in parts
        )
        or name.startswith(("secrets/backup/", "secrets/certs/", "secrets/security/"))
        or path.name
        in {"common-optimizations.yml", "common-optimizations.exceptions.json"}
        or name
        in {
            CANONICAL_SMTP,
            "secrets/db/legacy-app/service_password.txt",
            "secrets/communication/supabase/supabase_smtp_password.txt",
        }
        or row.get("id") in PROTECTED_IDS
        or str(row.get("id", "")).startswith(("SEC-", "BKP-", "LAB-"))
    )
    tokens = re.split(r"[^a-z0-9]+", name.lower())
    crypto = {
        "key",
        "keys",
        "jwt",
        "fernet",
        "unseal",
        "encryption",
        "encrypt",
        "identity",
        "identities",
        "ca",
        "tls",
        "certificate",
        "certificates",
        "keystore",
        "truststore",
        "snapshot",
        "audit",
        "history",
        "cookie",
    }
    if (
        invalid
        or protected
        or any(token in crypto for token in tokens)
        or path.suffix.lower() in {".pem", ".key", ".p12", ".pfx", ".jks", ".keystore"}
    ):
        raise ValueError("protected_or_invalid_path")
    return path


def _walk(root, path):
    root_path, fd = _exact_root(root)
    parents = [
        {"path": str(root_path), "identity": _snapshot(os.fstat(fd), DIR_FIELDS)}
    ]
    try:
        current = root_path
        for part in path.parts[:-1]:
            next_fd = os.open(part, DIR_FLAGS, dir_fd=fd)
            os.close(fd)
            fd = next_fd
            current = current / part
            parents.append(
                {"path": str(current), "identity": _snapshot(os.fstat(fd), DIR_FIELDS)}
            )
        return fd, parents
    except BaseException:
        os.close(fd)
        raise


def parent_identities(root: Path, path: Path):
    relative = PurePosixPath(path)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError("invalid_relative_path")
    fd, parents = _walk(root, relative)
    os.close(fd)
    return parents


def _observe(root, path):
    try:
        fd, parents = _walk(root, path)
    except FileNotFoundError:
        # A safely traversed missing ancestor means the exact target is absent.
        return None, []
    try:
        try:
            info = os.stat(path.name, dir_fd=fd, follow_symlinks=False)
        except FileNotFoundError:
            return None, parents
        if not stat.S_ISREG(info.st_mode):
            raise ValueError("non_regular_file")
        return _snapshot(info, FILE_FIELDS), parents
    finally:
        os.close(fd)


def _tracked(root, path):
    # Ignore caller Git overrides; the exact top-level index owns tracked status.
    git_boundary = any(
        (ancestor / ".git").exists() for ancestor in (root, *root.parents)
    )
    if not git_boundary:
        return False
    environment = {
        key: value for key, value in os.environ.items() if not key.startswith("GIT_")
    }
    top = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "--show-toplevel"],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
        check=False,
        env=environment,
    )
    if top.returncode != 0 or Path(top.stdout.strip()) != root:
        raise ValueError("git_root_check_failed")
    result = subprocess.run(
        ["git", "-C", str(root), "ls-files", "--error-unmatch", "--", str(path)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
        env=environment,
    )
    if result.returncode not in {0, 1}:
        raise ValueError("git_tracking_check_failed")
    return result.returncode == 0


def _fresh(value, now):
    try:
        stamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return stamp.tzinfo is not None and timedelta(0) <= now - stamp <= timedelta(
            hours=1
        )
    except (AttributeError, TypeError, ValueError):
        return False


def _text(value):
    return isinstance(value, str) and bool(value.strip())


def _reasons(row, now):
    missing = []
    if row.get("decision") != "delete":
        missing.append("explicit_delete_decision")
    if row.get("consumers") != []:
        missing.append("consumers_present_or_unknown")
    if row.get("recovery_required") is not False:
        missing.append("recovery_dependency")
    checked, evidence = row.get("checked", {}), row.get("evidence", {})
    if not isinstance(checked, dict) or any(
        checked.get(key) is not True for key in CHECKS
    ):
        missing.append("consumer_checks")
    if not isinstance(evidence, dict) or any(
        not _text(evidence.get(key)) for key in CHECKS
    ):
        missing.append("consumer_evidence_refs")
    if not _text(row.get("owner")) or not _text(row.get("evidence_ref")):
        missing.append("owner_evidence")
    if not _fresh(row.get("reviewed_at"), now):
        missing.append("stale_review")
    maintenance = row.get("maintenance", {})
    if (
        not isinstance(maintenance, dict)
        or maintenance.get("writers_stopped") is not True
        or not _text(maintenance.get("evidence_ref"))
        or not _text(maintenance.get("owner"))
    ):
        missing.append("maintenance_not_confirmed")
    if isinstance(maintenance, dict) and not _fresh(
        maintenance.get("reviewed_at"), now
    ):
        missing.append("stale_maintenance")
    return missing


def inspect_plan(root: Path, rows: list, now=None):
    root, root_fd = _exact_root(root)
    os.close(root_fd)
    now = now or datetime.now(UTC)
    if (
        not isinstance(now, datetime)
        or now.tzinfo is None
        or not isinstance(rows, list)
        or len(rows) > 4096
    ):
        raise ValueError("invalid_input")
    seen, result = set(), []
    for row in rows:
        path = _allowed(row)
        if str(path) in seen:
            raise ValueError("duplicate_target")
        seen.add(str(path))
        missing = _reasons(row, now)
        if _tracked(root, path):
            missing.append("git_tracked_target")
        actual, parents = _observe(root, path)
        if actual is not None:
            if actual != row.get("identity"):
                missing.append("file_identity_changed")
            if parents != row.get("parents"):
                missing.append("parent_identity_changed")
            if actual["nlink"] != 1:
                missing.append("shared_inode_requires_separate_review")
        result.append(
            {
                "path": str(path),
                "eligible": not missing,
                "reasons": missing,
                "present": actual is not None,
            }
        )
    return result


def _private_info(info, mode):
    return info.st_uid == os.getuid() and stat.S_IMODE(info.st_mode) == mode


@contextmanager
def retirement_lock(root: Path):
    _, fd = _exact_root(root)
    info = os.fstat(fd)
    os.close(fd)
    digest = hashlib.sha256(f"{info.st_dev}:{info.st_ino}".encode("ascii")).hexdigest()
    directory = Path("/tmp") / f"cln01-retirement-{os.getuid()}-{digest}"
    try:
        directory.mkdir(mode=0o700)
    except FileExistsError:
        pass
    directory_fd = os.open(directory, DIR_FLAGS)
    lock_fd = None
    try:
        if not _private_info(os.fstat(directory_fd), 0o700):
            raise ValueError("unsafe_lock_directory")
        lock_fd = os.open(
            "lock",
            os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW | os.O_CLOEXEC | os.O_NONBLOCK,
            0o600,
            dir_fd=directory_fd,
        )
        info = os.fstat(lock_fd)
        if (
            not stat.S_ISREG(info.st_mode)
            or info.st_nlink != 1
            or not _private_info(info, 0o600)
        ):
            raise ValueError("unsafe_lock_file")
        fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        yield
    finally:
        if lock_fd is not None:
            os.close(lock_fd)
        os.close(directory_fd)


def load_manifest(root: Path, path: Path):
    root_path, root_fd = _exact_root(root)
    root_info = os.fstat(root_fd)
    root_identity = (root_info.st_dev, root_info.st_ino)
    os.close(root_fd)
    path = Path(path)
    if not path.is_absolute() or path == root_path or root_path in path.parents:
        raise ValueError("manifest_must_be_external")
    _, parent_fd = _exact_root(path.parent, forbidden_identity=root_identity)
    file_fd = None
    try:
        if not _private_info(os.fstat(parent_fd), 0o700):
            raise ValueError("unsafe_manifest_directory")
        file_fd = os.open(path.name, FILE_FLAGS, dir_fd=parent_fd)
        info = os.fstat(file_fd)
        if (
            not stat.S_ISREG(info.st_mode)
            or info.st_nlink != 1
            or not _private_info(info, 0o600)
            or info.st_size > MAX_MANIFEST
        ):
            raise ValueError("unsafe_manifest_file")
        raw = os.read(file_fd, MAX_MANIFEST + 1)
        if len(raw) > MAX_MANIFEST or _snapshot(
            os.fstat(file_fd), FILE_FIELDS
        ) != _snapshot(info, FILE_FIELDS):
            raise ValueError("manifest_changed")
        document = json.loads(raw)
        if not isinstance(document, dict) or not isinstance(
            document.get("entries"), list
        ):
            raise ValueError("invalid_manifest")
        entries = []
        for row in document["entries"]:
            if not isinstance(row, dict):
                raise ValueError("invalid_entry")
            entries.append(
                {
                    **row,
                    "maintenance": row.get(
                        "maintenance", document.get("maintenance", {})
                    ),
                }
            )
        return {**document, "entries": entries}
    finally:
        if file_fd is not None:
            os.close(file_fd)
        os.close(parent_fd)


class PartialFailure(ValueError):
    """Sanitized structured receipt of a partially applied batch."""

    def __init__(self, results):
        super().__init__("partial_retirement_failure")
        self.results = results


def _open_handles(root, rows, plan):
    handles = []
    try:
        for row, item in zip(rows, plan, strict=True):
            if not item["present"]:
                actual, _ = _observe(root, _allowed(row))
                if actual is not None:
                    raise ValueError("absent_target_reappeared_before_apply")
                handles.append(None)
                continue
            path = _allowed(row)
            fd, parents = _walk(root, path)
            handles.append((fd, path, parents))
            if parents != row["parents"]:
                raise ValueError("parent_changed_before_apply")
            info = os.stat(path.name, dir_fd=fd, follow_symlinks=False)
            if _snapshot(info, FILE_FIELDS) != row["identity"]:
                raise ValueError("file_changed_before_apply")
        return handles
    except BaseException:
        for handle in handles:
            if handle is not None:
                os.close(handle[0])
        raise


def _unlink_regular(root, row, handle, parent_updates):
    fd, path, expected = handle
    check_fd, current = _walk(root, path)
    os.close(check_fd)
    adjusted = [
        {**parent, "identity": parent_updates.get(parent["path"], parent["identity"])}
        for parent in expected
    ]
    if (
        current != adjusted
        or _snapshot(os.fstat(fd), DIR_FIELDS) != current[-1]["identity"]
    ):
        raise ValueError("parent_changed_before_unlink")
    target_fd = os.open(path.name, FILE_FLAGS, dir_fd=fd)
    try:
        info = os.fstat(target_fd)
        actual = _snapshot(info, FILE_FIELDS)
        path_info = os.stat(path.name, dir_fd=fd, follow_symlinks=False)
        if (
            not stat.S_ISREG(info.st_mode)
            or actual != row["identity"]
            or info.st_nlink != 1
            or _snapshot(path_info, FILE_FIELDS) != actual
        ):
            raise ValueError("file_changed_before_unlink")
        os.unlink(path.name, dir_fd=fd)
        try:
            parent_updates[expected[-1]["path"]] = _snapshot(os.fstat(fd), DIR_FIELDS)
            if os.fstat(target_fd).st_nlink != 0:
                return "deleted-identity-unconfirmed"
            try:
                os.stat(path.name, dir_fd=fd, follow_symlinks=False)
            except FileNotFoundError:
                pass
            else:
                return "deleted-identity-unconfirmed"
            os.fsync(fd)
        except OSError:
            return "deleted-durability-unknown"
        return "deleted"
    finally:
        os.close(target_fd)


def apply_plan(root: Path, rows: list, now=None):
    with retirement_lock(root):
        plan = inspect_plan(root, rows, now)
        if any(not item["eligible"] for item in plan):
            raise ValueError("plan_not_eligible")
        handles = _open_handles(root, rows, plan)
        results, parent_updates = [], {}
        try:
            for index, (row, item, handle) in enumerate(
                zip(rows, plan, handles, strict=True)
            ):
                try:
                    if not item["present"]:
                        actual, _ = _observe(root, _allowed(row))
                        if actual is not None:
                            raise ValueError("absent_target_reappeared_before_result")
                        outcome = "already-absent"
                    else:
                        outcome = _unlink_regular(root, row, handle, parent_updates)
                except (ValueError, OSError):
                    outcome = "failed"
                results.append({"path": row["path"], "result": outcome})
                if outcome not in {"deleted", "already-absent"}:
                    results.extend(
                        {"path": rest["path"], "result": "not-attempted"}
                        for rest in rows[index + 1 :]
                    )
                    raise PartialFailure(results)
            return results
        finally:
            for handle in handles:
                if handle is not None:
                    os.close(handle[0])


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args(argv)
    try:
        rows = load_manifest(args.root, args.manifest)["entries"]
        result = (
            apply_plan(args.root, rows) if args.apply else inspect_plan(args.root, rows)
        )
        print(
            json.dumps(
                {"applied": args.apply, "entries": result}, ensure_ascii=True, indent=2
            )
        )
        return 0 if args.apply or all(item["eligible"] for item in result) else 2
    except PartialFailure as error:
        print(
            json.dumps(
                {"applied": True, "entries": error.results},
                ensure_ascii=True,
                indent=2,
            )
        )
        return 2
    except (ValueError, OSError, KeyError, TypeError):
        print(
            "Retirement blocked; recheck the receipt and partial file state. No secret values are printed.",
            file=sys.stderr,
        )
        return 2
