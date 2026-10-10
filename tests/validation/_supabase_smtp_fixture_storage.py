"""Private storage primitives and public synthetic inputs for SMTP rehearsal."""

from __future__ import annotations

import os
import re
import stat
from pathlib import Path

PUBLIC_SYNTHETIC_SMTP_PASSWORD = "public-synthetic-smtp-password-for-isolated-rehearsal"
PUBLIC_SYNTHETIC_WRONG_SMTP_PASSWORD = (
    "public-synthetic-wrong-smtp-password-for-isolated-rehearsal"
)
PUBLIC_SYNTHETIC_DB_PASSWORD = "public-synthetic-db-password-for-isolated-rehearsal"
PUBLIC_SYNTHETIC_JWT = "public-synthetic-jwt-for-isolated-rehearsal-only"
PUBLIC_SYNTHETIC_SIGNUP_PASSWORD = (
    "public-synthetic-signup-password-for-isolated-rehearsal"
)
PUBLIC_SYNTHETIC_SIGNUP_EMAILS = tuple(
    f"public-synthetic-signup-{index}@example.com" for index in range(1, 9)
)

_BASENAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}\Z", re.ASCII)


def _validate_inputs(name: str, content: str, mode: int) -> bytes:
    if not isinstance(name, str) or not _BASENAME.fullmatch(name):
        raise ValueError("synthetic fixture file name must be a safe basename")
    if not isinstance(content, str):
        raise TypeError("synthetic fixture content must be text")
    if isinstance(mode, bool) or not isinstance(mode, int) or not 0 <= mode <= 0o777:
        raise ValueError("synthetic fixture file mode is invalid")
    return content.encode("utf-8")


def _verify_private_directory(descriptor: int) -> None:
    metadata = os.fstat(descriptor)
    if (
        not stat.S_ISDIR(metadata.st_mode)
        or metadata.st_uid != os.geteuid()
        or stat.S_IMODE(metadata.st_mode) != 0o700
    ):
        raise PermissionError("synthetic fixture directory is not private")


def _open_exclusive(directory: Path, name: str) -> tuple[int, int]:
    directory_flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC
    directory_fd = os.open(directory, directory_flags)
    try:
        _verify_private_directory(directory_fd)
        file_flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC
        file_fd = os.open(name, file_flags, 0o600, dir_fd=directory_fd)
    except BaseException:
        os.close(directory_fd)
        raise
    return directory_fd, file_fd


def _verify_created_file(descriptor: int, mode: int) -> None:
    metadata = os.fstat(descriptor)
    if (
        not stat.S_ISREG(metadata.st_mode)
        or metadata.st_uid != os.geteuid()
        or metadata.st_nlink != 1
        or stat.S_IMODE(metadata.st_mode) != mode
    ):
        raise PermissionError("synthetic fixture file metadata is invalid")


def _write_all(descriptor: int, content: bytes) -> None:
    remaining = memoryview(content)
    while remaining:
        written = os.write(descriptor, remaining)
        if written <= 0:
            raise OSError("synthetic fixture write did not progress")
        remaining = remaining[written:]


def write_exclusive(directory: Path, name: str, content: str, mode: int) -> Path:
    """Create one owned fixture file without following or replacing paths."""

    encoded = _validate_inputs(name, content, mode)
    directory_fd, file_fd = _open_exclusive(directory, name)
    try:
        # Set the final mode through the owned descriptor before any bytes are
        # written; the caller's umask must not change this fixture contract.
        os.fchmod(file_fd, mode)
        _verify_created_file(file_fd, mode)
        _write_all(file_fd, encoded)
        os.fsync(file_fd)
    except BaseException:
        os.close(file_fd)
        os.unlink(name, dir_fd=directory_fd)
        os.close(directory_fd)
        raise
    os.close(file_fd)
    os.close(directory_fd)
    return directory / name
