"""Private, bounded records with per-key process locks and atomic replacement."""

import fcntl
import hashlib
import os
import secrets
import stat
from contextlib import contextmanager
from pathlib import Path

MAX_RECORD = 4 * 1024 * 1024


class RecordError(ValueError):
    """Value-free record failure."""


def _check_file(info):
    if (
        not stat.S_ISREG(info.st_mode)
        or info.st_uid != os.geteuid()
        or stat.S_IMODE(info.st_mode) != 0o600
        or info.st_nlink != 1
    ):
        raise RecordError("unsafe_record")


class PrivateRecords:
    """A directory owned by the executing account, never a symlink."""

    def __init__(self, path):
        path = Path(path).absolute()
        if len(path.parts) < 2:
            raise RecordError("unsafe_directory")
        fd = os.open("/", os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC)
        parent_fd = None
        try:
            for index, part in enumerate(path.parts[1:]):
                if index == len(path.parts) - 2:
                    parent_fd = os.dup(fd)
                try:
                    child = os.open(
                        part,
                        os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC,
                        dir_fd=fd,
                    )
                except FileNotFoundError:
                    os.mkdir(part, 0o700, dir_fd=fd)
                    child = os.open(
                        part,
                        os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC,
                        dir_fd=fd,
                    )
                os.close(fd)
                fd = child
            info = os.fstat(fd)
            if info.st_uid != os.geteuid() or stat.S_IMODE(info.st_mode) != 0o700:
                raise RecordError("unsafe_directory")
            self.fd = fd
            self.parent_fd = parent_fd
            self.basename = path.name
            self._lock = None
            self._check_root()
        except BaseException:
            os.close(fd)
            if parent_fd is not None:
                os.close(parent_fd)
            raise

    def close(self):
        os.close(self.fd)
        os.close(self.parent_fd)

    def _check_root(self):
        opened = os.fstat(self.fd)
        entry = os.stat(self.basename, dir_fd=self.parent_fd, follow_symlinks=False)
        if (
            not stat.S_ISDIR(entry.st_mode)
            or entry.st_uid != os.geteuid()
            or stat.S_IMODE(entry.st_mode) != 0o700
            or (opened.st_dev, opened.st_ino) != (entry.st_dev, entry.st_ino)
        ):
            raise RecordError("directory_changed")

    @staticmethod
    def _name(name):
        if not isinstance(name, str) or not name or "/" in name or name in (".", ".."):
            raise RecordError("invalid_record")
        return name

    @contextmanager
    def lock(self, key):
        self._check_root()
        name = ".lock-" + hashlib.sha256(key.encode("utf-8")).hexdigest()
        descriptor = os.open(
            name,
            os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW | os.O_CLOEXEC | os.O_NONBLOCK,
            0o600,
            dir_fd=self.fd,
        )
        try:
            _check_file(os.fstat(descriptor))
            fcntl.flock(descriptor, fcntl.LOCK_EX)
            self._lock = (name, descriptor)
            self._check_lock()
            yield
        finally:
            self._lock = None
            os.close(descriptor)

    def _check_lock(self):
        self._check_root()
        if self._lock is None:
            return
        name, descriptor = self._lock
        opened = os.fstat(descriptor)
        entry = os.stat(name, dir_fd=self.fd, follow_symlinks=False)
        _check_file(opened)
        _check_file(entry)
        if (opened.st_dev, opened.st_ino) != (entry.st_dev, entry.st_ino):
            raise RecordError("lock_changed")

    def read(self, name, limit=MAX_RECORD):
        self._check_lock()
        name = self._name(name)
        try:
            fd = os.open(
                name,
                os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC | os.O_NONBLOCK,
                dir_fd=self.fd,
            )
        except FileNotFoundError:
            return None
        try:
            before = os.fstat(fd)
            _check_file(before)
            if before.st_size > limit:
                raise RecordError("record_too_large")
            chunks, total = [], 0
            while True:
                part = os.read(fd, min(65536, limit + 1 - total))
                if not part:
                    break
                chunks.append(part)
                total += len(part)
                if total > limit:
                    raise RecordError("record_too_large")
            after = os.fstat(fd)
            path = os.stat(name, dir_fd=self.fd, follow_symlinks=False)
            fields = ("st_dev", "st_ino", "st_size", "st_mtime_ns", "st_ctime_ns")
            if (
                any(
                    getattr(before, x) != getattr(after, x)
                    or getattr(after, x) != getattr(path, x)
                    for x in fields
                )
                or total != after.st_size
            ):
                raise RecordError("record_changed")
            self._check_lock()
            return b"".join(chunks)
        finally:
            os.close(fd)

    def create(self, name, raw):
        """Create an immutable record once; True if created, False on an identical replay.

        The bytes are complete before the name appears (link of a synced temporary),
        and an existing record is never replaced: different bytes raise record_conflict.
        """
        self._check_lock()
        name = self._name(name)
        if not isinstance(raw, bytes) or len(raw) > MAX_RECORD:
            raise RecordError("invalid_record")
        temp = ".tmp-" + secrets.token_hex(16)
        descriptor = os.open(
            temp,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC,
            0o600,
            dir_fd=self.fd,
        )
        try:
            with os.fdopen(descriptor, "wb") as stream:
                stream.write(raw)
                stream.flush()
                os.fsync(stream.fileno())
            self._check_lock()
            try:
                os.link(temp, name, src_dir_fd=self.fd, dst_dir_fd=self.fd)
            except FileExistsError:
                pass
            else:
                os.unlink(temp, dir_fd=self.fd)
                os.fsync(self.fd)
                self._check_lock()
                return True
        finally:
            try:
                os.unlink(temp, dir_fd=self.fd)
            except FileNotFoundError:
                pass
        if self.read(name) != raw:
            raise RecordError("record_conflict")
        return False

    def write(self, name, raw):
        self._check_lock()
        name = self._name(name)
        if not isinstance(raw, bytes) or len(raw) > MAX_RECORD:
            raise RecordError("invalid_record")
        # Never replace an unsafe existing path.
        try:
            _check_file(os.stat(name, dir_fd=self.fd, follow_symlinks=False))
        except FileNotFoundError:
            pass
        temp = ".tmp-" + secrets.token_hex(16)
        descriptor = os.open(
            temp,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC,
            0o600,
            dir_fd=self.fd,
        )
        try:
            with os.fdopen(descriptor, "wb") as stream:
                stream.write(raw)
                stream.flush()
                os.fsync(stream.fileno())
            self._check_lock()
            os.replace(temp, name, src_dir_fd=self.fd, dst_dir_fd=self.fd)
            os.fsync(self.fd)
            self._check_lock()
        finally:
            try:
                os.unlink(temp, dir_fd=self.fd)
            except FileNotFoundError:
                pass
