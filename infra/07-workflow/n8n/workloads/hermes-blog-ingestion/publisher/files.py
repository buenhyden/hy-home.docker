"""Bounded, stable reads beneath explicit directory descriptors."""

import os
import stat
from contextlib import contextmanager
from pathlib import Path, PurePosixPath

FILE_LIMIT = 8 * 1024 * 1024
BATCH_LIMIT = 32 * 1024 * 1024
DIR_FLAGS = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC


class InputError(ValueError):
    """Static diagnostic code; never embeds a path or source content."""


def relative_parts(reference):
    if not isinstance(reference, str) or not reference or "\\" in reference:
        raise InputError("unsafe_path")
    path = PurePosixPath(reference)
    if path.is_absolute() or any(p in ("", ".", "..") for p in reference.split("/")):
        raise InputError("unsafe_path")
    return path.parts


@contextmanager
def open_directory(path):
    """Pin every absolute directory component; symlink ancestors fail closed."""
    path = Path(path)
    if ".." in path.parts:
        raise InputError("unsafe_path")
    absolute = path.absolute()
    descriptor = os.open("/", DIR_FLAGS)
    try:
        for part in absolute.parts[1:]:
            child = os.open(part, DIR_FLAGS, dir_fd=descriptor)
            os.close(descriptor)
            descriptor = child
        yield descriptor
    except FileNotFoundError:
        raise InputError("directory_missing") from None
    except OSError:
        raise InputError("unsafe_directory") from None
    finally:
        os.close(descriptor)


def _fingerprint(info):
    return (info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns, info.st_ctime_ns)


def safe_read(root, reference, *, limit=FILE_LIMIT):
    """Read regular bytes without following any component or reading a FIFO."""
    parts = relative_parts(reference)
    try:
        with open_directory(root) as base:
            descriptor = os.dup(base)
            try:
                for part in parts[:-1]:
                    child = os.open(part, DIR_FLAGS, dir_fd=descriptor)
                    os.close(descriptor)
                    descriptor = child
                flags = os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC | os.O_NONBLOCK
                leaf = os.open(parts[-1], flags, dir_fd=descriptor)
                try:
                    before = os.fstat(leaf)
                    if not stat.S_ISREG(before.st_mode):
                        raise InputError("unsafe_file")
                    if before.st_size > limit:
                        raise InputError("file_limit")
                    chunks, total = [], 0
                    while block := os.read(leaf, min(65536, limit + 1 - total)):
                        total += len(block)
                        if total > limit:
                            raise InputError("file_limit")
                        chunks.append(block)
                    if _fingerprint(before) != _fingerprint(os.fstat(leaf)):
                        raise InputError("file_changed")
                    return b"".join(chunks)
                finally:
                    os.close(leaf)
            finally:
                os.close(descriptor)
    except OSError:
        raise InputError("unsafe_file") from None
