"""Dependency-free anchored, bounded regular-file access shared by document consumers."""

from __future__ import annotations

import errno
import os
import pathlib
import re
import stat

MAX_FILE_BYTES = 10_000_000


class OperationsAuthorityError(ValueError):
    def __init__(self, code: str, message: str) -> None:
        self.code = code
        super().__init__(message)


def _safe_relative(value: object, label: str) -> pathlib.PurePosixPath:
    if not isinstance(value, str) or not value:
        raise OperationsAuthorityError("path-invalid", f"{label} must be nonempty")
    path = pathlib.PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or path.as_posix() != value:
        raise OperationsAuthorityError("path-invalid", f"unsafe {label}: {value}")
    return path


def _open_anchored_regular(
    root: pathlib.Path, relative: pathlib.PurePosixPath
) -> tuple[int, int, os.stat_result]:
    """Open and identify a regular file relative to an anchored root descriptor."""

    relative = _safe_relative(relative.as_posix(), "input path")
    directory_flags = (
        os.O_RDONLY
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_DIRECTORY", 0)
        | getattr(os, "O_NOFOLLOW", 0)
    )
    file_flags = (
        os.O_RDONLY
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NOFOLLOW", 0)
        | getattr(os, "O_NONBLOCK", 0)
    )
    directory_descriptor: int | None = None
    descriptor: int | None = None
    try:
        held_root = re.fullmatch(r"/proc/self/fd/(0|[1-9][0-9]*)", root.as_posix())
        if held_root is None:
            directory_descriptor = os.open(root, directory_flags)
        else:
            # The gate owns this already-open root. Duplicate its descriptor;
            # never resolve the proc link or relax no-follow for child paths.
            directory_descriptor = os.dup(int(held_root[1]))
            if not stat.S_ISDIR(os.fstat(directory_descriptor).st_mode):
                raise OperationsAuthorityError(
                    "root-invalid", "held root is not a directory"
                )
        for part in relative.parts[:-1]:
            component = os.stat(
                part, dir_fd=directory_descriptor, follow_symlinks=False
            )
            if stat.S_ISLNK(component.st_mode):
                raise OperationsAuthorityError(
                    "symlink-invalid", f"symlink input: {relative}"
                )
            if not stat.S_ISDIR(component.st_mode):
                raise OperationsAuthorityError(
                    "file-not-regular", f"non-directory component: {relative}"
                )
            next_descriptor = os.open(
                part, directory_flags, dir_fd=directory_descriptor
            )
            opened = os.fstat(next_descriptor)
            if (component.st_dev, component.st_ino) != (opened.st_dev, opened.st_ino):
                os.close(next_descriptor)
                raise OperationsAuthorityError(
                    "file-raced", f"changed before read: {relative}"
                )
            os.close(directory_descriptor)
            directory_descriptor = next_descriptor
        path_stat = os.stat(
            relative.name, dir_fd=directory_descriptor, follow_symlinks=False
        )
        if stat.S_ISLNK(path_stat.st_mode):
            raise OperationsAuthorityError(
                "symlink-invalid", f"symlink input: {relative}"
            )
        if not stat.S_ISREG(path_stat.st_mode):
            raise OperationsAuthorityError(
                "file-not-regular", f"not regular: {relative}"
            )
        descriptor = os.open(relative.name, file_flags, dir_fd=directory_descriptor)
        opened = os.fstat(descriptor)
        if not stat.S_ISREG(opened.st_mode) or (opened.st_dev, opened.st_ino) != (
            path_stat.st_dev,
            path_stat.st_ino,
        ):
            raise OperationsAuthorityError(
                "file-raced", f"changed before read: {relative}"
            )
        return directory_descriptor, descriptor, opened
    except OperationsAuthorityError:
        if descriptor is not None:
            os.close(descriptor)
        if directory_descriptor is not None:
            os.close(directory_descriptor)
        raise
    except OSError as error:
        if descriptor is not None:
            os.close(descriptor)
        if directory_descriptor is not None:
            os.close(directory_descriptor)
        code = "symlink-invalid" if error.errno in {errno.ELOOP} else "file-unreadable"
        raise OperationsAuthorityError(code, f"{relative}: {error}") from error


def read_bounded_regular(
    root: pathlib.Path,
    relative: pathlib.PurePosixPath,
    *,
    max_bytes: int = MAX_FILE_BYTES,
) -> bytes:
    """Read one regular file without following symlinks or accepting races."""
    if isinstance(max_bytes, bool) or not isinstance(max_bytes, int) or max_bytes < 1:
        raise OperationsAuthorityError(
            "bounds-invalid", "max_bytes must be a positive integer"
        )
    effective_max_bytes = min(max_bytes, MAX_FILE_BYTES)
    relative = _safe_relative(relative.as_posix(), "input path")
    directory_descriptor, descriptor, before = _open_anchored_regular(root, relative)
    try:
        identity = (before.st_dev, before.st_ino)
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = os.read(descriptor, min(65_536, effective_max_bytes + 1 - total))
            if not chunk:
                break
            chunks.append(chunk)
            total += len(chunk)
            if total > effective_max_bytes:
                raise OperationsAuthorityError(
                    "file-too-large", f"bound exceeded: {relative}"
                )
        after = os.fstat(descriptor)
        if (
            identity != (after.st_dev, after.st_ino)
            or before.st_size != after.st_size
            or before.st_mtime_ns != after.st_mtime_ns
        ):
            raise OperationsAuthorityError(
                "file-raced", f"changed during read: {relative}"
            )
        return b"".join(chunks)
    finally:
        os.close(descriptor)
        os.close(directory_descriptor)
