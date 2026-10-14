"""Protected no-replace custody for one OpenBao Raft snapshot attempt."""

from __future__ import annotations

import ctypes
import errno
import hmac
import json
import os
import re
import stat
import types
from pathlib import Path

ARTIFACT = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}")
RENAME_NOREPLACE = 1


def _signature(info):
    return (
        (info.st_dev, info.st_ino, info.st_mode),
        (info.st_uid, info.st_gid, info.st_nlink),
        (info.st_size, info.st_mtime_ns, info.st_ctime_ns),
    )


def _open_directory(path, blocked):
    path = Path(path)
    if not path.is_absolute() or any(part in {".", ".."} for part in path.parts):
        raise blocked()
    descriptor = os.open("/", os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC)
    try:
        for component in path.parts[1:]:
            following = os.open(
                component,
                os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC,
                dir_fd=descriptor,
            )
            os.close(descriptor)
            descriptor = following
        return descriptor
    except OSError:
        os.close(descriptor)
        raise blocked() from None


def _private_file(info, links=1):
    return (
        stat.S_ISREG(info.st_mode)
        and info.st_uid == os.getuid()
        and info.st_nlink == links
        and stat.S_IMODE(info.st_mode) == 0o600
    )


def _safe_name(name, blocked):
    if (
        isinstance(name, str)
        and not name.startswith(".")
        and not name.endswith(".receipt.json")
        and ARTIFACT.fullmatch(name)
    ):
        return name
    raise blocked()


def _write_all(descriptor, raw):
    while raw:
        count = os.write(descriptor, raw)
        if count <= 0:
            raise OSError()
        raw = raw[count:]


def rename_noreplace(directory, source, target):
    try:
        rename = ctypes.CDLL(None, use_errno=True).renameat2
    except (AttributeError, OSError):
        raise OSError(errno.ENOSYS, os.strerror(errno.ENOSYS)) from None
    rename.argtypes = (
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_uint,
    )
    rename.restype = ctypes.c_int
    result = rename(
        directory,
        os.fsencode(source),
        directory,
        os.fsencode(target),
        RENAME_NOREPLACE,
    )
    if result != 0:
        number = ctypes.get_errno()
        raise OSError(number, os.strerror(number))


class ArtifactDirectory:
    def __init__(
        self,
        path,
        archive,
        blocked,
        indeterminate,
        validate_archive,
        rename=rename_noreplace,
    ):
        self.path = Path(path)
        self.Blocked = blocked
        self.Indeterminate = indeterminate
        self.validate_archive = validate_archive
        self.rename_noreplace = rename
        self.fd = _open_directory(self.path, blocked)
        self.archive = archive
        info = os.fstat(self.fd)
        self.identity = (info.st_dev, info.st_ino)
        self.descriptors = {}
        self.attempt = None
        self.state = "EMPTY"
        try:
            self.recheck()
        except BaseException:
            self.close()
            raise

    def recheck(self):
        current = _open_directory(self.path, self.Blocked)
        try:
            held = os.fstat(self.fd)
            reopened = os.fstat(current)
            if (
                held.st_uid != os.getuid()
                or stat.S_IMODE(held.st_mode) != 0o700
                or (held.st_dev, held.st_ino) != self.identity
                or (reopened.st_dev, reopened.st_ino) != self.identity
            ):
                raise self.Blocked()
        finally:
            os.close(current)

    def _binding(self, key, name, links=1):
        descriptor = self.descriptors[key]
        held = os.fstat(descriptor)
        named = os.stat(name, dir_fd=self.fd, follow_symlinks=False)
        if not _private_file(held, links) or (held.st_dev, held.st_ino) != (
            named.st_dev,
            named.st_ino,
        ):
            raise self.Blocked()
        return held

    def _absent(self, name):
        try:
            os.stat(name, dir_fd=self.fd, follow_symlinks=False)
        except FileNotFoundError:
            return
        raise self.Blocked()

    def reserve_attempt(self, name):
        if self.attempt is not None:
            raise self.Blocked()
        name = _safe_name(name, self.Blocked)
        names = {
            "lock": "." + name + ".attempt",
            "final": name,
            "partial": "." + name + ".partial",
            "receipt_final": name + ".receipt.json",
            "receipt_partial": "." + name + ".receipt.json.partial",
        }
        self.recheck()
        self._absent(names["final"])
        self._absent(names["receipt_final"])
        for key in ("lock", "partial", "receipt_partial"):
            descriptor = os.open(
                names[key],
                os.O_RDWR | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC,
                0o600,
                dir_fd=self.fd,
            )
            self.descriptors[key] = descriptor
            os.fchmod(descriptor, 0o600)
            if not _private_file(os.fstat(descriptor)):
                raise self.Blocked()
            os.fsync(descriptor)
        os.fsync(self.fd)
        self.attempt = types.SimpleNamespace(**names)
        self.state = "RESERVED"
        self.recheck_attempt()
        return self.attempt

    def recheck_attempt(self):
        self.recheck()
        if self.state == "COMPLETE":
            self._absent(self.attempt.lock)
        else:
            self._binding("lock", self.attempt.lock)
        if self.state == "RESERVED":
            self._binding("partial", self.attempt.partial)
            self._binding("receipt_partial", self.attempt.receipt_partial)
            self._absent(self.attempt.final)
            self._absent(self.attempt.receipt_final)
        elif self.state in {"SNAPSHOT", "RECEIPT", "COMPLETE"}:
            self._binding("partial", self.attempt.final)
            if self.state == "SNAPSHOT":
                self._binding("receipt_partial", self.attempt.receipt_partial)
                self._absent(self.attempt.receipt_final)
            else:
                self._binding("receipt_partial", self.attempt.receipt_final)
        else:
            raise self.Blocked()

    @property
    def snapshot_fd(self):
        if self.state != "RESERVED":
            raise self.Blocked()
        return self.descriptors["partial"]

    def publish_snapshot(self, validation, expected_digest):
        self.recheck_attempt()
        descriptor = self.snapshot_fd
        if (
            _signature(os.fstat(descriptor)) != validation["signature"]
            or validation["size"] != os.fstat(descriptor).st_size
            or not hmac.compare_digest(validation["sha256"], expected_digest)
        ):
            raise self.Indeterminate()
        try:
            os.fsync(descriptor)
            self._binding("partial", self.attempt.partial)
            self._absent(self.attempt.final)
            self.rename_noreplace(self.fd, self.attempt.partial, self.attempt.final)
            self.state = "SNAPSHOT"
            self.recheck_attempt()
            final_validation = self.validate_archive(descriptor, self.archive)
            same_snapshot = final_validation["size"] == validation[
                "size"
            ] and hmac.compare_digest(final_validation["sha256"], validation["sha256"])
            if not same_snapshot:
                raise self.Indeterminate()
            os.fsync(descriptor)
            os.fsync(self.fd)
            self.recheck_attempt()
        except (self.Blocked, OSError, KeyboardInterrupt):
            raise self.Indeterminate() from None
        final = os.fstat(descriptor)
        return {
            "artifact": self.attempt.final,
            "dev": final.st_dev,
            "ino": final.st_ino,
            "uid": final.st_uid,
            "mode": format(stat.S_IMODE(final.st_mode), "04o"),
            "size": final.st_size,
        }

    def publish_receipt(self, receipt):
        if self.state != "SNAPSHOT":
            raise self.Blocked()
        descriptor = self.descriptors["receipt_partial"]
        raw = json.dumps(receipt, sort_keys=True, separators=(",", ":"))
        raw = (raw + "\n").encode("ascii")
        try:
            snapshot = self.validate_archive(self.descriptors["partial"], self.archive)
            if not hmac.compare_digest(snapshot["sha256"], receipt["sha256"]):
                raise self.Indeterminate()
            os.lseek(descriptor, 0, os.SEEK_SET)
            os.ftruncate(descriptor, 0)
            _write_all(descriptor, raw)
            os.fsync(descriptor)
            self.recheck_attempt()
            self._binding("receipt_partial", self.attempt.receipt_partial)
            self._absent(self.attempt.receipt_final)
            self.rename_noreplace(
                self.fd, self.attempt.receipt_partial, self.attempt.receipt_final
            )
            self.state = "RECEIPT"
            self.recheck_attempt()
            if not self._receipt_bound(descriptor, raw, snapshot):
                raise self.Indeterminate()
            os.fsync(descriptor)
            os.fsync(self.fd)
            self.recheck_attempt()
            if not self._receipt_bound(descriptor, raw, snapshot):
                raise self.Indeterminate()
            self._binding("lock", self.attempt.lock)
            os.unlink(self.attempt.lock, dir_fd=self.fd)
            self.state = "COMPLETE"
            self.recheck_attempt()
            os.fsync(self.fd)
        except (self.Blocked, OSError, KeyboardInterrupt):
            raise self.Indeterminate() from None

    def _receipt_bound(self, descriptor, raw, snapshot):
        receipt_ok = os.pread(descriptor, len(raw) + 1, 0) == raw
        snapshot_info = os.fstat(self.descriptors["partial"])
        return receipt_ok and _signature(snapshot_info) == snapshot["signature"]

    def close(self):
        failed = False
        for descriptor in tuple(self.descriptors.values()):
            try:
                os.close(descriptor)
            except OSError:
                failed = True
        self.descriptors = {}
        if self.fd is not None:
            try:
                os.close(self.fd)
            except OSError:
                failed = True
            self.fd = None
        if failed:
            raise OSError()

    def __enter__(self):
        return self

    def __exit__(self, _kind, _error, _traceback):
        try:
            self.close()
        except OSError:
            raise self.Indeterminate() from None
        return False
