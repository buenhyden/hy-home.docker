#!/usr/bin/env python3
"""Save one authenticated OpenBao Raft snapshot into protected local custody."""

from __future__ import annotations

import argparse
import getpass
import hashlib
import hmac
import http.client
import ipaddress
import json
import os
import re
import ssl
import stat
import sys
import threading
import time
import types
from datetime import UTC, datetime
from pathlib import Path

HOST = "openbao.hy.home.arpa"
PARENT_NAME = "protected-maintenance.py"
PARENT_SHA256 = "085132049f60173fc9fde14e20c9f09d0f4e423d35dd3285c1e9c4053e898d04"
ARCHIVE_NAME = "protected-snapshot-archive.py"
ARCHIVE_SHA256 = "48ff7d0e0ee6e39b00c5105df5fa20891b70ac5e0e820715aad0b675ab028868"
ARCHIVE_API = ("ArchiveBlocked", "MAX_COMPRESSED", "validate_archive")
CUSTODY_NAME = "protected-snapshot-custody.py"
CUSTODY_SHA256 = "fd266cdd46d950cc8d6cc8704497fd1454bd51c47f1c4b071b24cfbf79bba724"
POLICY = "backup-snapshot"
PERIOD = 720 * 60 * 60
MAX_COMPRESSED = 32 * 1024 * 1024
REQUEST_SECONDS = 300
TTL_MARGIN = 60
VERSIONS = frozenset({"2.6.2", "2.7.1+hyhome.go1.27.3.net0.60.0.r1"})
LOOKUP = "auth/token/lookup-self"
RENEW = "auth/token/renew-self"
SEAL = "sys/seal-status"
SNAPSHOT = "sys/storage/raft/snapshot"
ROUTES = frozenset({("GET", LOOKUP), ("POST", RENEW), ("GET", SEAL), ("GET", SNAPSHOT)})
ARTIFACT = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}")
UUID = re.compile(r"[a-f0-9]{8}(?:-[a-f0-9]{4}){3}-[a-f0-9]{12}")


class Blocked(Exception):
    pass


class Indeterminate(Blocked):
    pass


def _signature(info):
    return (
        (info.st_dev, info.st_ino, info.st_mode),
        (info.st_uid, info.st_gid, info.st_nlink),
        (info.st_size, info.st_mtime_ns, info.st_ctime_ns),
    )


def _load_public(name, expected_sha256, required, module_name):
    source_directory = Path(__file__).absolute().parent
    directory = _open_directory(source_directory)
    descriptor = None
    try:
        descriptor = os.open(
            name, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=directory
        )
        before = os.fstat(descriptor)
        if (
            not stat.S_ISREG(before.st_mode)
            or before.st_nlink != 1
            or before.st_uid not in {0, os.getuid()}
            or before.st_size < 1
            or before.st_size > 1024 * 1024
            or stat.S_IMODE(before.st_mode) & 0o022
        ):
            raise Blocked()
        raw = os.read(descriptor, before.st_size + 1)
        after = os.fstat(descriptor)
        named = os.stat(name, dir_fd=directory, follow_symlinks=False)
        if (
            len(raw) != before.st_size
            or _signature(before) != _signature(after)
            or (after.st_dev, after.st_ino) != (named.st_dev, named.st_ino)
            or not hmac.compare_digest(hashlib.sha256(raw).hexdigest(), expected_sha256)
        ):
            raise Blocked()
        namespace = {
            "__builtins__": __builtins__,
            "__file__": str(source_directory / name),
            "__name__": module_name,
        }
        exec(compile(raw, namespace["__file__"], "exec"), namespace)
        if any(item not in namespace for item in required):
            raise Blocked()
        module = types.SimpleNamespace(**namespace)
        info = os.fstat(directory)
        module.source_identity = (info.st_dev, info.st_ino)
        return module
    except (OSError, SyntaxError, ValueError, TypeError):
        raise Blocked() from None
    finally:
        if descriptor is not None:
            os.close(descriptor)
        os.close(directory)


def load_parent():
    parent = _load_public(
        PARENT_NAME,
        PARENT_SHA256,
        (
            "HOST",
            "Blocked",
            "PinnedConnection",
            "ca_context",
            "hidden_input",
            "open_directory",
            "parse_response",
            "read_secret_fd",
            "validate_secret",
        ),
        "_protected_snapshot_parent",
    )
    if parent.HOST != HOST:
        raise Blocked()
    return parent


def load_archive():
    return _load_public(
        ARCHIVE_NAME, ARCHIVE_SHA256, ARCHIVE_API, "_protected_snapshot_archive"
    )


def load_custody():
    return _load_public(
        CUSTODY_NAME,
        CUSTODY_SHA256,
        ("ArtifactDirectory", "rename_noreplace"),
        "_snapshot_custody",
    )


def shared_source_identity(*modules):
    identities = {module.source_identity for module in modules}
    if len(identities) != 1:
        raise Blocked()
    expected = identities.pop()
    directory = _open_directory(Path(__file__).absolute().parent)
    try:
        info = os.fstat(directory)
        current = (info.st_dev, info.st_ino)
    finally:
        os.close(directory)
    if current != expected:
        raise Blocked()
    return current


def validate_version(version):
    if version not in VERSIONS:
        raise Blocked()


def _trusted(parent, name, *arguments):
    try:
        return getattr(parent, name)(*arguments)
    except parent.Blocked:
        raise Blocked() from None


def check_lookup(response, minimum_ttl=0):
    data = response.get("data") if isinstance(response, dict) else None
    if not isinstance(data, dict):
        raise Blocked()
    exact = (
        type(data.get("policies")) is list
        and data["policies"] == [POLICY]
        # 2.6.2 and 2.7.1 omit both fields from lookup-self; if present they must match.
        and data.get("token_policies", [POLICY]) == [POLICY]
        and data.get("identity_policies", []) == []
        and data.get("renewable") is True
        and data.get("orphan") is True
        and data.get("type") == "service"
        and type(data.get("period")) is int
        and data["period"] == PERIOD
        and type(data.get("creation_ttl")) is int
        and data["creation_ttl"] == PERIOD
        and type(data.get("ttl")) is int
        and minimum_ttl < data["ttl"] <= PERIOD
        and type(data.get("explicit_max_ttl")) is int
        and data["explicit_max_ttl"] == 0
    )
    if not exact:
        raise Blocked()


def check_renewal(response, token):
    auth = response.get("auth") if isinstance(response, dict) else None
    if not isinstance(auth, dict):
        raise Blocked()
    exact = (
        isinstance(auth.get("client_token"), str)
        and hmac.compare_digest(auth["client_token"], token)
        and type(auth.get("policies")) is list
        and auth["policies"] == [POLICY]
        and type(auth.get("token_policies")) is list
        and auth["token_policies"] == [POLICY]
        and auth.get("renewable") is True
        and auth.get("orphan") is True
        and auth.get("token_type") == "service"
        and type(auth.get("lease_duration")) is int
        and 1 <= auth["lease_duration"] <= PERIOD
    )
    if not exact:
        raise Blocked()


def check_seal(response, cluster, version):
    validate_version(version)
    if (
        not isinstance(response, dict)
        or response.get("initialized") is not True
        or response.get("sealed") is not False
        or response.get("type") != "shamir"
        or response.get("storage_type") != "raft"
        or response.get("cluster_id") != cluster
        or response.get("version") != version
    ):
        raise Blocked()


def validate_headers(response, maximum=MAX_COMPRESSED):
    if response.status != 200:
        raise Blocked()
    headers = response.getheaders()
    if (
        len(headers) > 64
        or sum(len(name) + len(value) for name, value in headers) > 16384
    ):
        raise Blocked()
    fields = {}
    for raw_name, raw_value in headers:
        name = raw_name.lower()
        fields[name] = (*fields.get(name, ()), raw_value.strip())
    if "location" in fields:
        raise Blocked()
    lengths = fields.get("content-length", ())
    encodings = fields.get("transfer-encoding", ())
    if bool(lengths) == bool(encodings) or len(lengths) > 1 or len(encodings) > 1:
        raise Blocked()
    if encodings:
        if encodings != ("chunked",):
            raise Blocked()
        return None
    try:
        length = int(lengths[0], 10)
    except (IndexError, ValueError):
        raise Blocked() from None
    if str(length) != lengths[0] or not 0 <= length <= maximum:
        raise Blocked()
    return length


def validate_archive(descriptor, archive=None):
    archive = load_archive() if archive is None else archive
    try:
        return archive.validate_archive(descriptor)
    except archive.ArchiveBlocked:
        raise Blocked() from None


def _safe_name(name):
    if (
        isinstance(name, str)
        and not name.startswith(".")
        and not name.endswith(".receipt.json")
        and ARTIFACT.fullmatch(name)
    ):
        return name
    raise Blocked()


class ArtifactDirectory:
    def __new__(cls, path, archive=None, custody=None):
        custody = load_custody() if custody is None else custody
        archive = load_archive() if archive is None else archive
        return custody.ArtifactDirectory(
            path,
            archive,
            Blocked,
            Indeterminate,
            validate_archive,
            custody.rename_noreplace,
        )


def _open_directory(path):
    path = Path(path)
    if not path.is_absolute() or any(part in {".", ".."} for part in path.parts):
        raise Blocked()
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
        raise Blocked() from None


def _write_all(descriptor, raw):
    while raw:
        count = os.write(descriptor, raw)
        if count <= 0:
            raise OSError()
        raw = raw[count:]


def check_output_aliases(artifacts, ca_identity, ca_parent_identity, source_identity):
    artifacts.recheck()
    if artifacts.identity in {ca_identity, ca_parent_identity, source_identity}:
        raise Blocked()


def check_role_aliases(
    artifacts, token_fd, ca_identity, ca_parent_identity, source_identity=None
):
    check_output_aliases(
        artifacts, ca_identity, ca_parent_identity, source_identity or (-1, -1)
    )
    token = os.fstat(token_fd)
    token_identity = (token.st_dev, token.st_ino)
    if token_identity in {
        ca_identity,
        ca_parent_identity,
        artifacts.identity,
        source_identity,
    }:
        raise Blocked()
    for name in os.listdir(artifacts.fd):
        info = os.stat(name, dir_fd=artifacts.fd, follow_symlinks=False)
        if (info.st_dev, info.st_ino) == token_identity:
            raise Blocked()


def verify_completion(artifacts, token_fd, token_before):
    try:
        if token_fd is not None and _signature(os.fstat(token_fd)) != token_before:
            raise Indeterminate()
        artifacts.recheck_attempt()
    except (Blocked, OSError, KeyboardInterrupt):
        raise Indeterminate() from None


def _ca_identity(path):
    path = Path(path)
    parent = _open_directory(path.parent)
    descriptor = None
    try:
        descriptor = os.open(
            path.name, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=parent
        )
        info = os.fstat(descriptor)
        if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
            raise Blocked()
        return (info.st_dev, info.st_ino), (
            os.fstat(parent).st_dev,
            os.fstat(parent).st_ino,
        )
    finally:
        if descriptor is not None:
            os.close(descriptor)
        os.close(parent)


class SnapshotAPI:
    def __init__(self, parent, token, context, connect_ip, timeout=REQUEST_SECONDS):
        self.parent = parent
        self.token = _trusted(parent, "validate_secret", token)
        self.context = context
        self.connect_ip = str(ipaddress.ip_address(connect_ip))
        self.deadline = time.monotonic() + timeout

    def _connection(self):
        return self.parent.PinnedConnection(
            HOST,
            443,
            connect_ip=self.connect_ip,
            context=self.context,
            timeout=self._remaining(self.deadline),
        )

    def _request(self, method, path, document=None, destination=None):
        if (method, path) not in ROUTES or (path == SNAPSHOT) != (
            destination is not None
        ):
            raise Blocked()
        if (method == "POST") != (document is not None):
            raise Blocked()
        connection = self._connection()
        remaining = self._remaining(self.deadline)
        timer = threading.Timer(remaining, connection.abort)
        timer.daemon = True
        effect_started = False
        timer.start()
        try:
            body = json.dumps(document) if document is not None else None
            if method == "POST" or path == SNAPSHOT:
                effect_started = True
            connection.request(
                method,
                "/v1/" + path,
                body=body,
                headers={
                    "X-Vault-Token": self.token,
                    "Accept": "application/octet-stream"
                    if path == SNAPSHOT
                    else "application/json",
                    "Content-Type": "application/json",
                },
            )
            response = connection.getresponse()
            length = validate_headers(
                response, MAX_COMPRESSED if path == SNAPSHOT else 65536
            )
            if destination is not None:
                return self._stream(response, destination, length, self.deadline)
            raw = self._read(response, 65536, length, self.deadline)
            return _trusted(self.parent, "parse_response", raw)
        except Indeterminate:
            raise
        except Blocked:
            if effect_started:
                raise Indeterminate() from None
            raise
        except KeyboardInterrupt:
            if effect_started:
                raise Indeterminate() from None
            raise Blocked() from None
        except (OSError, ssl.SSLError, http.client.HTTPException, ValueError):
            raise Indeterminate() from None
        finally:
            timer.cancel()
            try:
                connection.close()
            except OSError:
                if effect_started:
                    raise Indeterminate() from None
                raise Blocked() from None

    def _remaining(self, deadline):
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise Indeterminate()
        return remaining

    def _read(self, response, maximum, length, deadline):
        chunks, count = [], 0
        while True:
            if getattr(response, "fp", None) is not None:
                response.fp.raw._sock.settimeout(max(0.001, self._remaining(deadline)))
            raw = response.read(min(65536, maximum - count + 1))
            if not raw:
                break
            count += len(raw)
            if count > maximum:
                raise Blocked()
            chunks.append(raw)
        if length is not None and count != length:
            raise Indeterminate()
        self._remaining(deadline)
        return b"".join(chunks)

    def _stream(self, response, destination, length, deadline):
        digest = hashlib.sha256()
        count = 0
        while True:
            if getattr(response, "fp", None) is not None:
                response.fp.raw._sock.settimeout(max(0.001, self._remaining(deadline)))
            raw = response.read(min(65536, MAX_COMPRESSED - count + 1))
            if not raw:
                break
            count += len(raw)
            if count > MAX_COMPRESSED:
                raise Blocked()
            _write_all(destination, raw)
            digest.update(raw)
        if not count or (length is not None and count != length):
            raise Indeterminate()
        self._remaining(deadline)
        return response.status, count, digest.hexdigest()

    def lookup(self):
        return self._request("GET", LOOKUP)

    def renew(self):
        return self._request("POST", RENEW, {"increment": "720h"})

    def seal(self):
        return self._request("GET", SEAL)

    def snapshot(self, descriptor):
        return self._request("GET", SNAPSHOT, destination=descriptor)


def receipt_document(record, *, cluster, version, digest, when=None):
    if not isinstance(digest, str) or not re.fullmatch(r"[a-f0-9]{64}", digest):
        raise Blocked()
    moment = time.time() if when is None else when
    return {
        **record,
        "cluster_id": cluster,
        "version": version,
        "sha256": digest,
        "http_status": 200,
        "saved_at_utc": datetime.fromtimestamp(moment, UTC).isoformat(),
    }


def save_snapshot(
    api, artifacts, name, token, cluster, version, clock=time.time, attempt=None
):
    validate_version(version)
    if not UUID.fullmatch(cluster):
        raise Blocked()
    attempt = artifacts.reserve_attempt(name) if attempt is None else attempt
    if attempt is not artifacts.attempt:
        raise Blocked()
    artifacts.recheck_attempt()
    check_lookup(api.lookup())
    try:
        check_renewal(api.renew(), token)
    except (Blocked, KeyboardInterrupt):
        raise Indeterminate() from None
    check_lookup(api.lookup(), REQUEST_SECONDS + TTL_MARGIN)
    check_seal(api.seal(), cluster, version)
    artifacts.recheck_attempt()
    descriptor = artifacts.snapshot_fd
    try:
        status, count, digest = api.snapshot(descriptor)
        os.fsync(descriptor)
        if status != 200 or os.fstat(descriptor).st_size != count:
            raise Indeterminate()
        validation = validate_archive(descriptor, artifacts.archive)
        record = artifacts.publish_snapshot(validation, digest)
        receipt = receipt_document(
            record, cluster=cluster, version=version, digest=digest, when=clock()
        )
        artifacts.publish_receipt(receipt)
        return receipt
    except (Blocked, OSError, KeyboardInterrupt):
        raise Indeterminate() from None


class PrivateArgumentParser(argparse.ArgumentParser):
    def error(self, _message):
        raise Blocked()


def main(arguments=None):
    parser = PrivateArgumentParser(description=__doc__)
    parser.add_argument("--ca", required=True)
    parser.add_argument("--ca-sha256", required=True)
    parser.add_argument("--output-directory", required=True)
    parser.add_argument("--artifact-name", required=True)
    parser.add_argument("--expected-cluster-id", required=True)
    parser.add_argument("--expected-version", required=True)
    parser.add_argument("--connect-ip", required=True)
    parser.add_argument("--token-fd", type=int)
    potential_effect = False
    try:
        parent = load_parent()
        archive = load_archive()
        custody = load_custody()
        source_identity = shared_source_identity(parent, archive, custody)
        options = parser.parse_args(arguments)
        _safe_name(options.artifact_name)
        validate_version(options.expected_version)
        if not UUID.fullmatch(options.expected_cluster_id):
            raise Blocked()
        ipaddress.ip_address(options.connect_ip)
        context = _trusted(parent, "ca_context", options.ca, options.ca_sha256)
        ca_identity, ca_parent_identity = _ca_identity(options.ca)
        with ArtifactDirectory(options.output_directory, archive, custody) as artifacts:
            check_output_aliases(
                artifacts,
                ca_identity,
                ca_parent_identity,
                source_identity,
            )
            attempt = artifacts.reserve_attempt(options.artifact_name)
            if options.token_fd is not None:
                if options.token_fd < 3:
                    raise Blocked()
                token_fd = options.token_fd
                token_before = _signature(os.fstat(token_fd))
                check_role_aliases(
                    artifacts,
                    token_fd,
                    ca_identity,
                    ca_parent_identity,
                    source_identity,
                )
                token = _trusted(parent, "read_secret_fd", token_fd)
            else:
                token_fd = None
                token = _trusted(parent, "hidden_input", "Snapshot token")
                token_before = None
            potential_effect = True
            save_snapshot(
                SnapshotAPI(parent, token, context, options.connect_ip),
                artifacts,
                options.artifact_name,
                token,
                options.expected_cluster_id,
                options.expected_version,
                attempt=attempt,
            )
            verify_completion(artifacts, token_fd, token_before)
        try:
            print("SAVED", flush=True)
        except OSError:
            raise Indeterminate() from None
        return 0
    except Indeterminate:
        print(
            "INDETERMINATE: preserve protected snapshot names; operator review required",
            file=sys.stderr,
        )
        return 2
    except KeyboardInterrupt:
        if potential_effect:
            print(
                "INDETERMINATE: preserve protected snapshot names; operator review required",
                file=sys.stderr,
            )
            return 2
        print(
            "BLOCKED: no snapshot completion claimed; preserve protected custody",
            file=sys.stderr,
        )
        return 1
    except (
        Blocked,
        OSError,
        ValueError,
        EOFError,
        getpass.GetPassWarning,
    ):
        print(
            "BLOCKED: no snapshot completion claimed; preserve protected custody",
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
