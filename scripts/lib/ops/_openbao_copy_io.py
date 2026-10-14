"""W48 protected input snapshots; callers supply authorization, never file records."""

from __future__ import annotations

import hashlib
import os
import re
import ssl
import stat
from contextlib import ExitStack
from dataclasses import dataclass, field
from pathlib import PurePosixPath

MAX_BYTES = 131072


class MigrationError(ValueError):
    """Fixed diagnostic shared with the public API; never include input payloads."""


DIR_FLAGS = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC
FILE_FLAGS = os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC | os.O_NONBLOCK


@dataclass(frozen=True, slots=True)
class ProtectedInput:
    """Exact controller-bound path and public stat metadata; no credential value."""

    root: str
    root_dev: int
    root_ino: int
    root_uid: int
    root_gid: int
    root_mode: int
    relative: str
    uid: int
    gid: int
    mode: int
    size: int


def validate_input(reference: ProtectedInput, *, ca=False):
    if type(reference) is not ProtectedInput:
        raise MigrationError("copy_input_binding_invalid")
    for text, absolute in ((reference.root, True), (reference.relative, False)):
        if not isinstance(text, str) or len(text) > 1024 or "\x00" in text:
            raise MigrationError("copy_input_binding_invalid")
        path = PurePosixPath(text)
        if (
            path.is_absolute() != absolute
            or str(path) != text
            or not path.parts
            or any(part in {".", ".."} for part in path.parts)
            or text == "/"
        ):
            raise MigrationError("copy_input_binding_invalid")
    numbers = (
        reference.root_dev,
        reference.root_ino,
        reference.root_uid,
        reference.root_gid,
        reference.root_mode,
        reference.uid,
        reference.gid,
        reference.mode,
        reference.size,
    )
    if (
        any(type(value) is not int or value < 0 for value in numbers)
        or reference.root_mode > 0o777
        or reference.root_mode & 0o022
        or reference.mode not in ({0o600, 0o640, 0o644} if ca else {0o600, 0o640})
        or not 1 <= reference.size <= MAX_BYTES
    ):
        raise MigrationError("copy_input_binding_invalid")


def _identity(info):
    return (info.st_dev, info.st_ino, info.st_uid, info.st_gid, info.st_mode)


def _signature(info):
    return (
        info.st_dev,
        info.st_ino,
        info.st_uid,
        info.st_gid,
        info.st_mode,
        info.st_nlink,
        info.st_size,
        info.st_mtime_ns,
        info.st_ctime_ns,
    )


@dataclass(frozen=True, slots=True)
class HeldInput:
    """Private bytes never appear in repr; held descriptors are invocation-owned."""

    data: bytes = field(repr=False)
    descriptor: int = field(repr=False)
    parent: int = field(repr=False)
    name: str = field(repr=False)
    signature: tuple = field(repr=False)
    edges: tuple = field(repr=False)

    def check(self):
        try:
            for parent, name, descriptor, expected in self.edges:
                if (
                    _identity(os.fstat(descriptor)) != expected
                    or _identity(os.stat(name, dir_fd=parent, follow_symlinks=False))
                    != expected
                ):
                    raise MigrationError("copy_input_changed")
            current = os.stat(self.name, dir_fd=self.parent, follow_symlinks=False)
            if (
                _signature(os.fstat(self.descriptor)) != self.signature
                or _signature(current) != self.signature
            ):
                raise MigrationError("copy_input_changed")
        except OSError:
            raise MigrationError("copy_input_changed") from None


def _open_directory(parent, name, stack, edges):
    descriptor = os.open(name, DIR_FLAGS, dir_fd=parent)
    stack.callback(os.close, descriptor)
    expected = _identity(os.fstat(descriptor))
    return descriptor, (*edges, (parent, name, descriptor, expected))


def hold_input(reference: ProtectedInput, stack: ExitStack, *, ca=False):
    """Open every component without following links and retain all path edges."""
    validate_input(reference, ca=ca)
    try:
        descriptor = os.open("/", DIR_FLAGS)
        stack.callback(os.close, descriptor)
        edges = ()
        for part in PurePosixPath(reference.root).parts[1:]:
            descriptor, edges = _open_directory(descriptor, part, stack, edges)
        root = os.fstat(descriptor)
        if (
            root.st_dev,
            root.st_ino,
            root.st_uid,
            root.st_gid,
            stat.S_IMODE(root.st_mode),
        ) != (
            reference.root_dev,
            reference.root_ino,
            reference.root_uid,
            reference.root_gid,
            reference.root_mode,
        ):
            raise MigrationError("copy_root_binding_mismatch")
        parts = PurePosixPath(reference.relative).parts
        for part in parts[:-1]:
            descriptor, edges = _open_directory(descriptor, part, stack, edges)
            info = os.fstat(descriptor)
            if info.st_uid != reference.root_uid or stat.S_IMODE(info.st_mode) & 0o022:
                raise MigrationError("copy_directory_unprotected")
        opened = os.open(parts[-1], FILE_FLAGS, dir_fd=descriptor)
        stack.callback(os.close, opened)
        info = os.fstat(opened)
        if (
            not stat.S_ISREG(info.st_mode)
            or info.st_nlink != 1
            or (info.st_uid, info.st_gid, stat.S_IMODE(info.st_mode), info.st_size)
            != (reference.uid, reference.gid, reference.mode, reference.size)
        ):
            raise MigrationError("copy_input_unprotected")
        chunks, remaining = (), reference.size + 1
        while remaining:
            chunk = os.read(opened, min(remaining, 65536))
            if not chunk:
                break
            chunks, remaining = (*chunks, chunk), remaining - len(chunk)
        data = b"".join(chunks)
        held = HeldInput(data, opened, descriptor, parts[-1], _signature(info), edges)
        held.check()
        if len(data) != reference.size:
            raise MigrationError("copy_input_changed")
        return held
    except OSError:
        raise MigrationError("copy_input_unavailable") from None


def token_text(held):
    raw = held.data[:-1] if held.data.endswith(b"\n") else held.data
    if not re.fullmatch(rb"[A-Za-z0-9._-]{1,4096}", raw):
        raise MigrationError("copy_token_invalid")
    return raw.decode("ascii")


def verified_context(held, expected_sha256):
    """Load immutable held certificate bytes, excluding private/mixed PEM blocks."""
    if hashlib.sha256(held.data).hexdigest() != expected_sha256:
        raise MigrationError("copy_ca_binding_mismatch")
    block = rb"-----BEGIN CERTIFICATE-----\s+[A-Za-z0-9+/=\s]+-----END CERTIFICATE-----"
    if not re.fullmatch(rb"\s*(?:" + block + rb"\s*)+", held.data):
        raise MigrationError("copy_ca_invalid")
    try:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.minimum_version = ssl.TLSVersion.TLSv1_2
        context.load_verify_locations(cadata=held.data.decode("ascii"))
        held.check()
        return context
    except (ValueError, UnicodeError, ssl.SSLError):
        raise MigrationError("copy_ca_invalid") from None
