"""Bounded validator for native OpenBao Raft snapshot archives."""

from __future__ import annotations

import base64
import binascii
import gzip
import hashlib
import json
import os
import re
import stat
import tarfile
from pathlib import Path

MAX_COMPRESSED = 32 * 1024 * 1024
MAX_UNPACKED = 128 * 1024 * 1024
MAX_METADATA = 8192
MAX_HASHES = 8192
MAX_SEALED = 8192
ORDER = ("meta.json", "state.bin", "SHA256SUMS", "SHA256SUMS.sealed")
HASH_LINE = re.compile(r"[a-f0-9]{64}  (meta\.json|state\.bin)")
UINT64_MAX = (1 << 64) - 1


class ArchiveBlocked(Exception):
    pass


def _signature(info):
    return (
        (info.st_dev, info.st_ino, info.st_mode),
        (info.st_uid, info.st_gid, info.st_nlink),
        (info.st_size, info.st_mtime_ns, info.st_ctime_ns),
    )


def _unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ArchiveBlocked()
        result[key] = value
    return result


def _json(raw):
    if not 1 <= len(raw) <= MAX_METADATA:
        raise ArchiveBlocked()
    try:
        value = json.loads(
            raw,
            object_pairs_hook=_unique,
            parse_constant=lambda _value: (_ for _ in ()).throw(ArchiveBlocked()),
        )
    except (ArchiveBlocked, ValueError, TypeError, UnicodeError, RecursionError):
        raise ArchiveBlocked() from None
    pending = [(value, 0)]
    nodes = 0
    while pending:
        node, depth = pending.pop()
        nodes += 1
        if nodes > 256 or depth > 8:
            raise ArchiveBlocked()
        if isinstance(node, dict):
            pending.extend((item, depth + 1) for item in node.values())
        elif isinstance(node, list):
            pending.extend((item, depth + 1) for item in node)
    return value


def _text(value):
    return (
        isinstance(value, str)
        and 1 <= len(value) <= 512
        and all(32 <= ord(character) <= 126 for character in value)
    )


def _uint(value, *, positive=False):
    return type(value) is int and (1 if positive else 0) <= value <= UINT64_MAX


def _metadata(raw, state_size):
    value = _json(raw)
    keys = {
        "Version",
        "ID",
        "Index",
        "Term",
        "Peers",
        "Configuration",
        "ConfigurationIndex",
        "Size",
    }
    if not isinstance(value, dict) or set(value) != keys:
        raise ArchiveBlocked()
    if (
        type(value["Version"]) is not int
        or value["Version"] not in {0, 1}
        or not _text(value["ID"])
        or not _uint(value["Index"], positive=True)
        or not _uint(value["Term"], positive=True)
        or not _uint(value["ConfigurationIndex"])
        or value["ConfigurationIndex"] > value["Index"]
        or type(value["Size"]) is not int
        or value["Size"] != state_size
    ):
        raise ArchiveBlocked()
    peers = value["Peers"]
    if peers is not None:
        if not isinstance(peers, str) or len(peers) > MAX_METADATA:
            raise ArchiveBlocked()
        try:
            base64.b64decode(peers, validate=True)
        except (ValueError, binascii.Error):
            raise ArchiveBlocked() from None
    configuration = value["Configuration"]
    if not isinstance(configuration, dict) or set(configuration) != {"Servers"}:
        raise ArchiveBlocked()
    servers = configuration["Servers"]
    if not isinstance(servers, list) or not 1 <= len(servers) <= 64:
        raise ArchiveBlocked()
    identities = set()
    addresses = set()
    for server in servers:
        if (
            not isinstance(server, dict)
            or set(server) != {"Suffrage", "ID", "Address"}
            or type(server["Suffrage"]) is not int
            or server["Suffrage"] not in {0, 1, 2}
            or not _text(server["ID"])
            or not _text(server["Address"])
            or server["ID"] in identities
            or server["Address"] in addresses
        ):
            raise ArchiveBlocked()
        identities.add(server["ID"])
        addresses.add(server["Address"])
    return value


class _LimitedReader:
    def __init__(self, stream):
        self.stream = stream
        self.count = 0

    def read(self, size=-1):
        remaining = MAX_UNPACKED - self.count
        if size < 0 or size > remaining + 1:
            size = remaining + 1
        raw = self.stream.read(size)
        self.count += len(raw)
        if self.count > MAX_UNPACKED:
            raise ArchiveBlocked()
        return raw


def _member(archive, member, maximum, *, retain):
    if not 1 <= member.size <= maximum:
        raise ArchiveBlocked()
    stream = archive.extractfile(member)
    if stream is None:
        raise ArchiveBlocked()
    digest = hashlib.sha256()
    chunks = []
    count = 0
    while True:
        raw = stream.read(min(65536, maximum - count + 1))
        if not raw:
            break
        count += len(raw)
        if count > maximum:
            raise ArchiveBlocked()
        digest.update(raw)
        if retain:
            chunks.append(raw)
    if count != member.size:
        raise ArchiveBlocked()
    return (b"".join(chunks) if retain else count), digest.hexdigest()


def _compressed_digest(descriptor, size):
    digest = hashlib.sha256()
    offset = 0
    while offset < size:
        raw = os.pread(descriptor, min(65536, size - offset), offset)
        if not raw:
            raise ArchiveBlocked()
        digest.update(raw)
        offset += len(raw)
    return digest.hexdigest()


def validate_archive(descriptor):
    before = os.fstat(descriptor)
    if not stat.S_ISREG(before.st_mode) or not 1 <= before.st_size <= MAX_COMPRESSED:
        raise ArchiveBlocked()
    digest = _compressed_digest(descriptor, before.st_size)
    duplicate = os.dup(descriptor)
    try:
        os.lseek(duplicate, 0, os.SEEK_SET)
        with os.fdopen(duplicate, "rb", closefd=True) as source:
            duplicate = None
            limited = _LimitedReader(gzip.GzipFile(fileobj=source))
            bodies = {}
            hashes = {}
            names = []
            limits = {
                "meta.json": MAX_METADATA,
                "state.bin": MAX_UNPACKED,
                "SHA256SUMS": MAX_HASHES,
                "SHA256SUMS.sealed": MAX_SEALED,
            }
            try:
                with tarfile.open(fileobj=limited, mode="r|") as archive:
                    for member in archive:
                        if (
                            member.name not in ORDER
                            or member.name in bodies
                            or not member.isreg()
                            or Path(member.name).name != member.name
                            or stat.S_IMODE(member.mode) != 0o600
                            or member.pax_headers
                        ):
                            raise ArchiveBlocked()
                        names.append(member.name)
                        bodies[member.name], hashes[member.name] = _member(
                            archive,
                            member,
                            limits[member.name],
                            retain=member.name != "state.bin",
                        )
                while trailing := limited.read(65536):
                    if any(trailing):
                        raise ArchiveBlocked()
            except (OSError, EOFError, tarfile.TarError, gzip.BadGzipFile):
                raise ArchiveBlocked() from None
        if tuple(names) != ORDER or not bodies["SHA256SUMS.sealed"]:
            raise ArchiveBlocked()
        lines = bodies["SHA256SUMS"].decode("ascii").splitlines()
        if len(lines) != 2 or any(not HASH_LINE.fullmatch(line) for line in lines):
            raise ArchiveBlocked()
        expected = {
            f"{hashes['meta.json']}  meta.json",
            f"{hashes['state.bin']}  state.bin",
        }
        if set(lines) != expected:
            raise ArchiveBlocked()
        metadata = _metadata(bodies["meta.json"], bodies["state.bin"])
        after = os.fstat(descriptor)
        if _signature(before) != _signature(after):
            raise ArchiveBlocked()
        return {
            "sha256": digest,
            "size": before.st_size,
            "state_size": bodies["state.bin"],
            "metadata": metadata,
            "signature": _signature(after),
        }
    except (OSError, ValueError, UnicodeError, json.JSONDecodeError):
        raise ArchiveBlocked() from None
    finally:
        if duplicate is not None:
            os.close(duplicate)
