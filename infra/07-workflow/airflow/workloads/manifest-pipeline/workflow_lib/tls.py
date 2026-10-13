"""Fail-closed delivery of a protected CA bundle to optional TLS drivers."""

from __future__ import annotations

import fcntl
import os
import re
import ssl
import stat

from .manifest import ContractError

MAX_CA_BYTES = 1024 * 1024
_PEM_CERTIFICATE = re.compile(
    rb"-----BEGIN CERTIFICATE-----\r?\n[A-Za-z0-9+/=\r\n]+?"
    rb"-----END CERTIFICATE-----"
)


def _absolute_parts(path):
    if not isinstance(path, str) or not path.startswith("/") or "\x00" in path:
        raise ValueError("ca_path")
    parts = path.split("/")[1:]
    if not parts or any(part in ("", ".", "..") for part in parts):
        raise ValueError("ca_path")
    return parts


def _directory_fd(parts, allowed_owners, expected_group, effective_groups):
    flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC
    fd = os.open("/", flags)
    try:
        for index, name in enumerate(parts):
            child = os.open(name, flags, dir_fd=fd)
            os.close(fd)
            fd = child
            info = os.fstat(fd)
            mode = stat.S_IMODE(info.st_mode)
            trusted_tmp = (
                index == 0 and name == "tmp" and info.st_uid == 0 and mode == 0o1777
            )
            if info.st_uid not in {0, os.geteuid()} or (
                mode & 0o022 and not trusted_tmp
            ):
                raise ValueError("ca_parent")
            if index == len(parts) - 1:
                if info.st_uid not in allowed_owners or mode not in (0o700, 0o750):
                    raise ValueError("ca_directory")
                expected_group = (
                    info.st_gid if expected_group is None else expected_group
                )
                if (
                    info.st_gid != expected_group
                    or expected_group not in effective_groups
                ):
                    raise ValueError("ca_directory_group")
        return fd, expected_group
    except Exception:
        os.close(fd)
        raise


def _signature(info):
    return (
        info.st_dev,
        info.st_ino,
        info.st_size,
        info.st_mtime_ns,
        info.st_ctime_ns,
        info.st_mode,
        info.st_uid,
        info.st_gid,
        info.st_nlink,
    )


def _bounded_read(fd, maximum):
    chunks = []
    offset = 0
    while offset <= maximum:
        chunk = os.pread(fd, min(65536, maximum + 1 - offset), offset)
        if not chunk:
            break
        chunks.append(chunk)
        offset += len(chunk)
    return b"".join(chunks)


def _ca_bytes(path, expected_directory):
    parts = _absolute_parts(path)
    directory_parts = _absolute_parts(expected_directory)
    if parts[:-1] != directory_parts or parts[-1] != "ca.pem":
        raise ValueError("ca_path")
    allowed_owners = {0, os.geteuid()}
    effective_groups = {os.getegid(), *os.getgroups()}
    parent_fd, expected_group = _directory_fd(
        directory_parts, allowed_owners, None, effective_groups
    )
    source_fd = None
    try:
        parent_identity = os.fstat(parent_fd)
        source_fd = os.open(
            "ca.pem",
            os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK | os.O_CLOEXEC,
            dir_fd=parent_fd,
        )
        before = os.fstat(source_fd)
        if (
            not stat.S_ISREG(before.st_mode)
            or before.st_nlink != 1
            or before.st_uid not in allowed_owners
            or before.st_gid != expected_group
            or stat.S_IMODE(before.st_mode) not in (0o600, 0o640)
            or not 1 <= before.st_size <= MAX_CA_BYTES
        ):
            raise ValueError("ca_file")
        raw = _bounded_read(source_fd, MAX_CA_BYTES)
        after = os.fstat(source_fd)
        if (
            not raw
            or len(raw) > MAX_CA_BYTES
            or _signature(before) != _signature(after)
        ):
            raise ValueError("ca_changed")
        current_fd, _ = _directory_fd(
            directory_parts, allowed_owners, expected_group, effective_groups
        )
        try:
            current_parent = os.fstat(current_fd)
            current_file = os.stat("ca.pem", dir_fd=current_fd, follow_symlinks=False)
            if (parent_identity.st_dev, parent_identity.st_ino) != (
                current_parent.st_dev,
                current_parent.st_ino,
            ) or _signature(after) != _signature(current_file):
                raise ValueError("ca_path_changed")
        finally:
            os.close(current_fd)
        return raw
    finally:
        if source_fd is not None:
            os.close(source_fd)
        os.close(parent_fd)


def _validate_ca_pem(raw):
    matches = list(_PEM_CERTIFICATE.finditer(raw))
    if not matches:
        raise ValueError("ca_pem")
    position = 0
    for match in matches:
        if raw[position : match.start()].strip():
            raise ValueError("ca_pem")
        position = match.end()
    if raw[position:].strip():
        raise ValueError("ca_pem")
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.load_verify_locations(cadata=raw.decode("ascii"))


def _write_all(fd, raw):
    view = memoryview(raw)
    offset = 0
    while offset < len(view):
        written = os.write(fd, view[offset:])
        if written <= 0:
            raise OSError("memfd_write")
        offset += written


class PinnedCA:
    """An explicitly owned, sealed snapshot of validated CA bytes."""

    __slots__ = ("_fd", "path")

    def __init__(self, fd):
        self._fd = fd
        self.path = f"/proc/self/fd/{fd}"

    def __repr__(self):
        return "<sealed opsflow CA>"

    def close(self):
        fd = self._fd
        if fd is None:
            return
        self._fd = None
        try:
            os.close(fd)
        except Exception:
            raise ContractError("tls_ca_close_failed") from None


def _sealed_ca(raw):
    names = (
        "F_ADD_SEALS",
        "F_GET_SEALS",
        "F_SEAL_WRITE",
        "F_SEAL_GROW",
        "F_SEAL_SHRINK",
        "F_SEAL_SEAL",
    )
    if not hasattr(os, "memfd_create") or not all(
        hasattr(fcntl, name) for name in names
    ):
        raise ValueError("memfd_unavailable")
    flags = getattr(os, "MFD_CLOEXEC", None)
    allow_sealing = getattr(os, "MFD_ALLOW_SEALING", None)
    if flags is None or allow_sealing is None:
        raise ValueError("memfd_unavailable")
    fd = os.memfd_create("opsflow-ca", flags | allow_sealing)
    try:
        _write_all(fd, raw)
        os.lseek(fd, 0, os.SEEK_SET)
        os.fchmod(fd, 0o400)
        seals = (
            fcntl.F_SEAL_WRITE
            | fcntl.F_SEAL_GROW
            | fcntl.F_SEAL_SHRINK
            | fcntl.F_SEAL_SEAL
        )
        fcntl.fcntl(fd, fcntl.F_ADD_SEALS, seals)
        if fcntl.fcntl(fd, fcntl.F_GET_SEALS) & seals != seals:
            raise ValueError("memfd_seals")
        info = os.fstat(fd)
        if (
            not stat.S_ISREG(info.st_mode)
            or stat.S_IMODE(info.st_mode) != 0o400
            or info.st_size != len(raw)
        ):
            raise ValueError("memfd_identity")
        path = f"/proc/self/fd/{fd}"
        probe = os.open(path, os.O_RDONLY | os.O_CLOEXEC)
        try:
            if _bounded_read(probe, MAX_CA_BYTES) != raw:
                raise ValueError("memfd_readback")
        finally:
            os.close(probe)
        return PinnedCA(fd)
    except Exception:
        os.close(fd)
        raise


def pin_ca(path, *, expected_directory):
    """Return a sealed snapshot after protected-path and certificate validation."""
    try:
        raw = _ca_bytes(path, expected_directory)
        _validate_ca_pem(raw)
        return _sealed_ca(raw)
    except Exception:
        raise ContractError("tls_ca_rejected") from None
