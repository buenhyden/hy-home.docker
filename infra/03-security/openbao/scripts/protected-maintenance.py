"""Protected, authenticated, operator-run HOME quorum ceremony.

This client neither upgrades OpenBao nor issues snapshot credentials. Independent
custody, two share holders and the exact maintenance approval remain prerequisites.
Response loss can leave an issued credential: retained custody means uncertainty,
never proof of cancellation or revocation. Python does not promise memory erasure.
"""

from __future__ import annotations

import argparse
import base64
import binascii
import fcntl
import getpass
import hashlib
import hmac
import http.client
import ipaddress
import json
import math
import os
import re
import socket
import ssl
import stat
import sys
import threading
import time
import warnings
from pathlib import Path

HOST = "openbao.hy.home.arpa"
ATTEMPT = "sys/generate-root-token/attempt"
UPDATE = "sys/generate-root-token/update"
LOOKUP = "auth/token/lookup-self"
SEAL = "sys/seal-status"
LIMIT = 65536
REQUEST_SECONDS = 20
UUID = re.compile(r"[a-f0-9]{8}(?:-[a-f0-9]{4}){3}-[a-f0-9]{12}")
CERTIFICATE = re.compile(
    rb"-----BEGIN CERTIFICATE-----\s+[A-Za-z0-9+/=\s]+-----END CERTIFICATE-----"
)


class Blocked(Exception):
    """No credential, server response, path or inner exception is exposed."""


class Indeterminate(Blocked):
    """A protected response or credential may exist; preserve owned custody."""


def unique_fields(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise Blocked()
        result = {**result, key: value}
    return result


def parse_response(raw):
    if len(raw) > LIMIT:
        raise Blocked()
    depth, quoted, escaped = 0, False, False
    for byte in raw:
        if quoted:
            if escaped:
                escaped = False
            elif byte == 92:
                escaped = True
            elif byte == 34:
                quoted = False
        elif byte == 34:
            quoted = True
        elif byte in (123, 91):
            depth += 1
            if depth > 16:
                raise Blocked()
        elif byte in (125, 93):
            depth -= 1
    try:
        value = json.loads(raw, object_pairs_hook=unique_fields)
    except (ValueError, TypeError, UnicodeError, RecursionError):
        raise Blocked() from None
    if not isinstance(value, dict):
        raise Blocked()
    pending, nodes = (value,), 0
    while pending:
        node, pending = pending[-1], pending[:-1]
        nodes += 1
        if nodes > 2048 or (isinstance(node, float) and not math.isfinite(node)):
            raise Blocked()
        if isinstance(node, dict):
            pending = (*pending, *node.values())
        elif isinstance(node, list):
            pending = (*pending, *node)
    return value


def open_directory(path):
    """Bind every component with dirfd/no-follow; refuse path aliases."""
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
    except BaseException:
        os.close(descriptor)
        raise


def private_file(info):
    return (
        stat.S_ISREG(info.st_mode)
        and info.st_uid == os.getuid()
        and info.st_nlink == 1
        and stat.S_IMODE(info.st_mode) == 0o600
    )


def read_secret_fd(descriptor):
    before = os.fstat(descriptor)
    if not private_file(before) or not 1 <= before.st_size <= 4096:
        raise Blocked()
    if os.lseek(descriptor, 0, os.SEEK_CUR) != 0:
        raise Blocked()
    raw = os.read(descriptor, 4097)
    after = os.fstat(descriptor)
    if (before.st_mtime_ns, before.st_ctime_ns, before.st_size) != (
        after.st_mtime_ns,
        after.st_ctime_ns,
        after.st_size,
    ) or len(raw) != before.st_size:
        raise Blocked()
    try:
        secret = raw.decode("ascii").removesuffix("\n")
    except UnicodeError:
        raise Blocked() from None
    return validate_secret(secret)


def validate_secret(value):
    if not isinstance(value, str) or not re.fullmatch(r"[!-~]{1,4096}", value):
        raise Blocked()
    return value


def hidden_input(label):
    with warnings.catch_warnings():
        warnings.simplefilter("error", getpass.GetPassWarning)
        # Requiring a controlling terminal prevents getpass's stdin fallback.
        with open("/dev/tty", "w+") as terminal:
            return validate_secret(getpass.getpass(label + ": ", stream=terminal))


def ca_context(path, expected_sha256):
    if not isinstance(expected_sha256, str) or not re.fullmatch(
        r"[a-f0-9]{64}", expected_sha256
    ):
        raise Blocked()
    path = Path(path)
    parent = open_directory(path.parent)
    descriptor = None
    try:
        descriptor = os.open(
            path.name, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=parent
        )
        before = os.fstat(descriptor)
        if (
            not stat.S_ISREG(before.st_mode)
            or before.st_nlink != 1
            or before.st_uid not in {0, os.getuid()}
            or stat.S_IMODE(before.st_mode) not in {0o600, 0o640, 0o644}
            or not 1 <= before.st_size <= 1048576
        ):
            raise Blocked()
        raw = os.read(descriptor, 1048577)
        after = os.fstat(descriptor)
        if (
            before.st_ino,
            before.st_dev,
            before.st_size,
            before.st_mtime_ns,
            before.st_ctime_ns,
            before.st_mode,
            before.st_uid,
            before.st_nlink,
        ) != (
            after.st_ino,
            after.st_dev,
            after.st_size,
            after.st_mtime_ns,
            after.st_ctime_ns,
            after.st_mode,
            after.st_uid,
            after.st_nlink,
        ) or len(raw) != before.st_size:
            raise Blocked()
        if not hmac.compare_digest(hashlib.sha256(raw).hexdigest(), expected_sha256):
            raise Blocked()
        certificates = CERTIFICATE.findall(raw)
        if not certificates or CERTIFICATE.sub(b"", raw).strip():
            raise Blocked()
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.minimum_version = ssl.TLSVersion.TLSv1_2
        context.load_verify_locations(cadata=raw.decode("ascii"))
        return context  # OpenSSL owns the parsed trust store; source cannot alter it.
    finally:
        if descriptor is not None:
            os.close(descriptor)
        os.close(parent)


class Custody:
    """An operator-provisioned empty private directory, retained on all failures."""

    def __init__(self, directory):
        self.fd = open_directory(directory)
        self.lock = None
        self.open_files = frozenset()
        self.mutation_started = False
        try:
            info = os.fstat(self.fd)
            if info.st_uid != os.getuid() or stat.S_IMODE(info.st_mode) != 0o700:
                raise Blocked()
            if os.listdir(self.fd):
                raise Blocked()
            self.lock = self.reserve(".lock")
            fcntl.flock(self.lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BaseException:
            self.close()
            raise

    def reserve(self, name):
        if name not in {
            ".lock",
            "initialization.json",
            "update-1.json",
            "update-2.json",
            "root.token",
            "state.json",
        }:
            raise Blocked()
        descriptor = os.open(
            name,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC,
            0o600,
            dir_fd=self.fd,
        )
        self.open_files = self.open_files | {descriptor}
        os.fchmod(descriptor, 0o600)
        if not private_file(os.fstat(descriptor)):
            raise Blocked()
        os.fsync(descriptor)
        os.fsync(self.fd)
        return descriptor

    def write(self, descriptor, value):
        raw = (
            value.encode("ascii")
            if isinstance(value, str)
            else json.dumps(value).encode("ascii")
        )
        if len(raw) > LIMIT:
            raise Blocked()
        while raw:
            count = os.write(descriptor, raw)
            if count <= 0:
                raise Blocked()
            raw = raw[count:]
        os.fsync(descriptor)
        os.close(descriptor)
        self.open_files = self.open_files - {descriptor}
        os.fsync(self.fd)

    def close(self):
        for descriptor in self.open_files:
            os.close(descriptor)
        self.open_files = frozenset()
        os.close(self.fd)

    def __enter__(self):
        return self

    def __exit__(self, _kind, error, _traceback):
        try:
            self.close()
        except OSError:
            if isinstance(error, Indeterminate):
                return False
            if self.mutation_started:
                raise Indeterminate() from None
            if error is None:
                raise Blocked() from None
        return False


class PinnedConnection(http.client.HTTPSConnection):
    """Numeric gateway connection; authenticated TLS still names the fixed origin."""

    def __init__(self, host, port, *, connect_ip, context, timeout):
        super().__init__(host, port, context=context, timeout=timeout)
        self.connect_ip = ipaddress.ip_address(connect_ip)
        self.deadline = time.monotonic() + timeout
        self.transport_socket = None

    def connect(self):
        family = socket.AF_INET if self.connect_ip.version == 4 else socket.AF_INET6
        self.sock = socket.socket(family, socket.SOCK_STREAM)
        self.transport_socket = self.sock
        self.sock.settimeout(max(0.001, self.deadline - time.monotonic()))
        self.sock.connect((str(self.connect_ip), self.port))
        self.sock = self._context.wrap_socket(
            self.sock, server_hostname=self.host, do_handshake_on_connect=False
        )
        self.transport_socket = self.sock
        self.sock.settimeout(max(0.001, self.deadline - time.monotonic()))
        self.sock.do_handshake()

    def abort(self):
        if self.transport_socket is not None:
            try:
                self.transport_socket.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            self.transport_socket.close()


class API:
    def __init__(self, token, context, connect_ip, *, lookup_only=False):
        self.token = validate_secret(token)
        self.context = context
        self.connect_ip = str(ipaddress.ip_address(connect_ip))
        self.lookup_only = lookup_only

    def root_lookup(self, token):
        return API(token, self.context, self.connect_ip, lookup_only=True).request(
            "GET", LOOKUP
        )

    def request(self, method, path, document=None):
        if self.lookup_only and (method, path) != ("GET", LOOKUP):
            raise Blocked()
        if (method, path) not in {
            ("GET", LOOKUP),
            ("GET", SEAL),
            ("GET", ATTEMPT),
            ("POST", ATTEMPT),
            ("POST", UPDATE),
            ("DELETE", ATTEMPT),
        }:
            raise Blocked()
        if (method == "POST" and not isinstance(document, dict)) or (
            method != "POST" and document is not None
        ):
            raise Blocked()
        connection = PinnedConnection(
            HOST,
            443,
            connect_ip=self.connect_ip,
            context=self.context,
            timeout=REQUEST_SECONDS,
        )
        timer = threading.Timer(REQUEST_SECONDS, connection.abort)
        timer.daemon = True
        deadline = time.monotonic() + REQUEST_SECONDS
        timer.start()
        try:
            connection.request(
                method,
                "/v1/" + path,
                body=json.dumps(document) if document is not None else None,
                headers={
                    "X-Vault-Token": self.token,
                    "Content-Type": "application/json",
                },
            )
            response = connection.getresponse()
            # No redirect, proxy, HTTP fallback or server-provided next-hop exists.
            if response.status not in ({200, 204} if method == "DELETE" else {200}):
                raise Blocked()
            raw = response.read(LIMIT + 1)
            if time.monotonic() >= deadline:
                raise Indeterminate()
            return None if response.status == 204 else parse_response(raw)
        except (OSError, ssl.SSLError, http.client.HTTPException, ValueError):
            raise Indeterminate() from None
        except Blocked:
            if method in {"POST", "DELETE"}:
                raise Indeterminate() from None
            raise
        finally:
            timer.cancel()
            connection.close()


def check_operator(response):
    data = response.get("data", {})
    if (
        not isinstance(data, dict)
        or data.get("policies")
        not in (["default", "hy-home-operator"], ["hy-home-operator", "default"])
        or type(data.get("ttl")) is not int
        or not 1 <= data["ttl"] <= 14400
        or type(data.get("creation_ttl")) is not int
        or not 1 <= data["creation_ttl"] <= 3600
        or type(data.get("renewable")) is not bool
        or data.get("path") != "auth/oidc/oidc/callback"
    ):
        raise Blocked()


def check_root(response):
    data = response.get("data", {})
    expected = {
        "policies": ["root"],
        "path": "auth/token/root",
        "display_name": "root",
        "type": "service",
        "orphan": True,
        "entity_id": "",
        "expire_time": None,
    }
    if not isinstance(data, dict) or any(
        data.get(key) != value for key, value in expected.items()
    ):
        raise Blocked()
    if data.get("orphan") is not True or data.get("renewable", False) is not False:
        raise Blocked()
    for key in ("ttl", "creation_ttl", "explicit_max_ttl", "num_uses"):
        if type(data.get(key)) is not int or data[key] != 0:
            raise Blocked()
    if data.get("namespace_path", "") != "" or not isinstance(data.get("id"), str):
        raise Blocked()
    # SSC self lookup returns an internal ID; the fresh authenticated request
    # proves the decoded credential, so do not equate internal and external IDs.
    validate_secret(data["id"])


def check_seal(response, cluster):
    if (
        response.get("initialized") is not True
        or response.get("sealed") is not False
        or response.get("type") != "shamir"
        or type(response.get("n")) is not int
        or response["n"] != 3
        or type(response.get("t")) is not int
        or response["t"] != 2
        or response.get("version")
        not in {"2.6.2", "2.7.1", "2.7.1+hyhome.go1.27.2.net0.60.0.r1"}
        or response.get("cluster_id") != cluster
    ):
        raise Blocked()


def check_progress(response, nonce, count, complete):
    if (
        response.get("started") is not True
        or response.get("nonce") != nonce
        or type(response.get("required")) is not int
        or response["required"] != 2
        or type(response.get("progress")) is not int
        or response["progress"] != count
        or response.get("complete") is not complete
        or response.get("pgp_fingerprint", "") != ""
    ):
        raise Blocked()


def decode_token(encoded, otp):
    if not isinstance(encoded, str) or not re.fullmatch(
        r"[A-Za-z0-9+/]+={0,2}", encoded
    ):
        raise Blocked()
    try:
        raw = base64.b64decode(encoded + "=" * (-len(encoded) % 4), validate=True)
        pad = otp.encode("ascii")
        if len(raw) != len(pad) or not 1 <= len(raw) <= 4096:
            raise Blocked()
        token = bytes(a ^ b for a, b in zip(raw, pad, strict=True)).decode("ascii")
    except (ValueError, UnicodeError, binascii.Error):
        raise Blocked() from None
    return validate_secret(token)


def cancel_owned_pending(api, nonce):
    """At most three bounded requests; foreign or completed attempts are untouched."""
    current = api.request("GET", ATTEMPT)
    if current.get("started") is False:
        return False  # Could be a completed attempt; cancellation is not proven.
    if current.get("nonce") != nonce or current.get("complete") is not False:
        raise Indeterminate()
    api.request("DELETE", ATTEMPT)
    after = api.request("GET", ATTEMPT)
    if after.get("started") is not False:
        raise Indeterminate()
    return True


def ceremony(api, custody, cluster, share_input):
    check_operator(api.request("GET", LOOKUP))
    check_seal(api.request("GET", SEAL), cluster)
    if api.request("GET", ATTEMPT).get("started") is not False:
        raise Blocked()
    shares = tuple(validate_secret(share_input(number)) for number in (1, 2))
    if len({api.token, *shares}) != 3:
        raise Blocked()
    initialization_file = custody.reserve("initialization.json")
    nonce, complete, final_submitted = None, False, False
    try:
        custody.mutation_started = True
        initialization = api.request("POST", ATTEMPT, {})
        custody.write(initialization_file, initialization)
        nonce = initialization.get("nonce")
        if not isinstance(nonce, str) or not UUID.fullmatch(nonce):
            raise Indeterminate()
        check_progress(initialization, nonce, 0, False)
        otp = initialization.get("otp")
        if (
            not isinstance(otp, str)
            or not re.fullmatch(r"[A-Za-z0-9]{1,4096}", otp)
            or type(initialization.get("otp_length")) is not int
            or len(otp) != initialization["otp_length"]
        ):
            raise Blocked()
        for number in (1, 2):
            response_file = custody.reserve(f"update-{number}.json")
            share = shares[number - 1]
            final_submitted = number == 2
            response = api.request("POST", UPDATE, {"key": share, "nonce": nonce})
            custody.write(response_file, response)
            complete = number == 2 and response.get("complete") is True
            check_progress(response, nonce, number, number == 2)
        root_file = custody.reserve("root.token")
        root_token = decode_token(response.get("encoded_token"), otp)
        custody.write(root_file, root_token)
        check_root(api.root_lookup(root_token))
        check_operator(api.request("GET", LOOKUP))
        state_file = custody.reserve("state.json")
        custody.write(state_file, {"state": "DELIVERED", "operator_healthy": True})
        return "DELIVERED"
    except BaseException:
        # Never turn a lost final response or completed encoded credential into
        # a cancellation receipt. Retained responses permit operator recovery.
        if nonce is not None and not complete:
            try:
                cancelled = cancel_owned_pending(api, nonce)
                if cancelled and not final_submitted:
                    raise Blocked() from None
            except Indeterminate:
                raise Indeterminate() from None
            except Blocked:
                raise
            except BaseException:
                raise Indeterminate() from None
        raise Indeterminate() from None


class PrivateArgumentParser(argparse.ArgumentParser):
    def error(self, _message):
        raise Blocked()  # argparse normally echoes unknown secret-bearing argv.


def main(arguments=None):
    parser = PrivateArgumentParser(description=__doc__)
    parser.add_argument("--ca", required=True)
    parser.add_argument("--ca-sha256", required=True)
    parser.add_argument("--custody-directory", required=True)
    parser.add_argument("--expected-cluster-id", required=True)
    parser.add_argument("--connect-ip", required=True)
    for name in ("operator-fd", "share-one-fd", "share-two-fd"):
        parser.add_argument("--" + name, type=int)
    try:
        options = parser.parse_args(arguments)
        if not UUID.fullmatch(options.expected_cluster_id):
            raise Blocked()
        ipaddress.ip_address(options.connect_ip)
        context = ca_context(options.ca, options.ca_sha256)
        descriptors = (options.operator_fd, options.share_one_fd, options.share_two_fd)
        if any(value is not None for value in descriptors):
            if any(value is None or value < 3 for value in descriptors):
                raise Blocked()
            identities = {
                (os.fstat(fd).st_dev, os.fstat(fd).st_ino) for fd in descriptors
            }
            if len(identities) != 3:
                raise Blocked()
            token, one, two = tuple(read_secret_fd(fd) for fd in descriptors)

            def share_input(number):
                return (one, two)[number - 1]
        else:
            token = hidden_input("OIDC operator token")

            def share_input(number):
                return hidden_input(f"Share holder {number}")

        with Custody(options.custody_directory) as custody:
            state = ceremony(
                API(token, context, options.connect_ip),
                custody,
                options.expected_cluster_id,
                share_input,
            )
        try:
            print(state, flush=True)
        except OSError:
            raise Indeterminate() from None
        return 0
    except Indeterminate:
        print(
            "INDETERMINATE: preserve protected custody; operator recovery required",
            file=sys.stderr,
        )
        return 2
    except (
        Blocked,
        OSError,
        ValueError,
        EOFError,
        KeyboardInterrupt,
        getpass.GetPassWarning,
    ):
        print(
            "BLOCKED: no completion claimed; preserve protected custody",
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
