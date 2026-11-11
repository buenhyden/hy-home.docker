"""Fixed-authority HTTPS transport for the Hermes research webhook.

The parent validates the route and address policy before loading credentials.
Network work runs in an isolated child so a stalled resolver, TLS handshake, or
body read remains bounded.  The child receives credentials through stdin, uses
an empty environment, connects to one vetted address, and keeps the reviewed
hostname for TLS verification and the HTTP Host header.
"""

from __future__ import annotations

import base64
import ctypes
import http.client
import ipaddress
import json
import math
import os
import signal
import socket
import ssl
import subprocess
import sys
import time
import unicodedata
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlsplit

APPROVED_WEBHOOK_URL = "https://n8n.hy.home.arpa/webhook/hermes-blog-ingestion"
MAX_REQUEST_BYTES = 4 * 1024 * 1024
MAX_RESPONSE_BYTES = 1024 * 1024
MAX_REQUEST_TIMEOUT = 45.0
MAX_CREDENTIAL_LENGTH = 4096
MAX_POLICY_LENGTH = 4096
CHUNK = 64 * 1024
MAX_POLICY_ENTRIES = 32
_MAX_CHILD_INPUT = math.ceil(MAX_REQUEST_BYTES * 4 / 3) + 64 * 1024
_METADATA_ADDRESSES = frozenset(
    {
        ipaddress.ip_address("169.254.169.254"),
        ipaddress.ip_address("100.100.100.200"),
        ipaddress.ip_address("fd00:ec2::254"),
    }
)


class TransportFailure(Exception):
    """A value-free transport result safe for the plugin response and ledger."""

    def __init__(self, reason: str, *, retryable: bool = False):
        super().__init__(reason)
        self.reason = reason
        self.retryable = retryable


@dataclass(frozen=True)
class Endpoint:
    hostname: str
    port: int
    target: str


@dataclass(frozen=True)
class Response:
    status: int
    body: bytes
    content_type: str


def validate_endpoint(url: str) -> Endpoint:
    """Accept only the exact reviewed origin and webhook path."""
    if not isinstance(url, str) or url != APPROVED_WEBHOOK_URL:
        raise TransportFailure("disallowed_url")
    if any(
        char == "\\" or char.isspace() or unicodedata.category(char) in {"Cc", "Cf"}
        for char in url
    ):
        raise TransportFailure("disallowed_url")
    try:
        parts = urlsplit(url)
        port = parts.port or 443
    except ValueError:
        raise TransportFailure("disallowed_url") from None
    if (
        parts.scheme != "https"
        or parts.hostname != "n8n.hy.home.arpa"
        or port != 443
        or parts.netloc != "n8n.hy.home.arpa"
        or parts.path != "/webhook/hermes-blog-ingestion"
        or parts.query
        or parts.fragment
        or parts.username is not None
        or parts.password is not None
    ):
        raise TransportFailure("disallowed_url")
    return Endpoint(parts.hostname, port, parts.path)


Network = ipaddress.IPv4Network | ipaddress.IPv6Network
Address = ipaddress.IPv4Address | ipaddress.IPv6Address


def parse_address_policy(value: str) -> tuple[Network, ...]:
    """Parse an independently trusted IP/CIDR allowlist; an empty policy closes."""
    if not isinstance(value, str) or len(value) > MAX_POLICY_LENGTH:
        raise TransportFailure("missing_address_policy")
    entries = [item for group in value.split(",") for item in group.split()]
    if not entries:
        raise TransportFailure("missing_address_policy")
    if len(entries) > MAX_POLICY_ENTRIES:
        raise TransportFailure("invalid_address_policy")
    networks: list[Network] = []
    try:
        for entry in entries:
            network = ipaddress.ip_network(entry, strict=False)
            if network.prefixlen == 0:
                raise ValueError
            networks.append(network)
    except ValueError:
        raise TransportFailure("invalid_address_policy") from None
    return tuple(networks)


def _normalized_address(value: str) -> Address:
    address = ipaddress.ip_address(value)
    mapped = getattr(address, "ipv4_mapped", None)
    return mapped or address


def _safe_destination(address: Address) -> bool:
    return not (
        address in _METADATA_ADDRESSES
        or address.is_loopback
        or address.is_link_local
        or address.is_multicast
        or address.is_unspecified
        or address.is_reserved
    )


def _in_policy(
    address: Address,
    policy: Iterable[Network],
) -> bool:
    return any(
        address.version == network.version and address in network for network in policy
    )


def resolve_pinned(
    endpoint: Endpoint,
    policy: tuple[Network, ...],
    *,
    resolver: Callable = socket.getaddrinfo,
) -> str:
    """Resolve once, require every answer to be safe/approved, and pin one answer."""
    try:
        infos = resolver(
            endpoint.hostname,
            endpoint.port,
            type=socket.SOCK_STREAM,
            proto=socket.IPPROTO_TCP,
        )
    except OSError:
        raise TransportFailure("dns", retryable=True) from None
    addresses: list[Address] = []
    try:
        for info in infos:
            address = _normalized_address(info[4][0])
            if address not in addresses:
                addresses.append(address)
    except (IndexError, TypeError, ValueError):
        raise TransportFailure("dns", retryable=True) from None
    if not addresses:
        raise TransportFailure("dns", retryable=True)
    if not all(
        _safe_destination(address) and _in_policy(address, policy)
        for address in addresses
    ):
        raise TransportFailure("address_not_allowed")
    return str(addresses[0])


def _tls_context() -> ssl.SSLContext:
    context = ssl.create_default_context()
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    return context


def _tls_connect(
    ip: str,
    port: int,
    hostname: str,
    timeout: float,
    context: ssl.SSLContext,
):
    raw = socket.create_connection((ip, port), timeout)
    try:
        return context.wrap_socket(raw, server_hostname=hostname)
    except BaseException:
        raw.close()
        raise


class _PinnedHTTPSConnection(http.client.HTTPSConnection):
    def __init__(self, endpoint, ip, timeout, connector, context):
        super().__init__(
            endpoint.hostname,
            endpoint.port,
            timeout=timeout,
            context=context,
        )
        self._pinned_ip = ip
        self._connector = connector

    def connect(self):
        self.sock = self._connector(
            self._pinned_ip,
            self.port,
            self.host,
            self.timeout,
            self._context,
        )


def _remaining(deadline: float, monotonic: Callable[[], float]) -> float:
    remaining = deadline - monotonic()
    if remaining <= 0:
        raise TransportFailure("timeout", retryable=True)
    return remaining


def _read_response(response, connection, deadline, monotonic) -> bytes:
    length = response.getheader("Content-Length")
    if length:
        try:
            parsed_length = int(length)
            if parsed_length < 0:
                raise TransportFailure("invalid_response")
            if parsed_length > MAX_RESPONSE_BYTES:
                raise TransportFailure("response_too_large")
        except ValueError:
            raise TransportFailure("invalid_response") from None
    chunks: list[bytes] = []
    total = 0
    while True:
        if connection.sock is not None:
            connection.sock.settimeout(_remaining(deadline, monotonic))
        chunk = response.read(CHUNK)
        if not chunk:
            return b"".join(chunks)
        total += len(chunk)
        if total > MAX_RESPONSE_BYTES:
            raise TransportFailure("response_too_large")
        chunks.append(chunk)


def send_once(
    url: str,
    body: bytes,
    token: str,
    policy_text: str,
    *,
    timeout: float,
    resolver: Callable = socket.getaddrinfo,
    connector: Callable = _tls_connect,
    context: ssl.SSLContext | None = None,
    monotonic: Callable[[], float] = time.monotonic,
) -> Response:
    """Perform one pinned request. Tests inject resolver/connector, never a URL."""
    endpoint = validate_endpoint(url)
    if not isinstance(body, bytes) or len(body) > MAX_REQUEST_BYTES:
        raise TransportFailure("request_too_large")
    if (
        not isinstance(token, str)
        or not token
        or len(token) > MAX_CREDENTIAL_LENGTH
        or "\r" in token
        or "\n" in token
    ):
        raise TransportFailure("invalid_credential")
    if not isinstance(timeout, (int, float)) or not (
        0 < timeout <= MAX_REQUEST_TIMEOUT
    ):
        raise TransportFailure("invalid_timeout")
    policy = parse_address_policy(policy_text)
    deadline = monotonic() + float(timeout)
    ip = resolve_pinned(endpoint, policy, resolver=resolver)
    connection = _PinnedHTTPSConnection(
        endpoint,
        ip,
        _remaining(deadline, monotonic),
        connector,
        context or _tls_context(),
    )
    response = None
    try:
        connection.request(
            "POST",
            endpoint.target,
            body=body,
            headers={
                "Content-Type": "application/json",
                "X-Hermes-Ingest-Token": token,
            },
        )
        if connection.sock is not None:
            connection.sock.settimeout(_remaining(deadline, monotonic))
        response = connection.getresponse()
        raw = _read_response(response, connection, deadline, monotonic)
        return Response(
            response.status,
            raw,
            response.getheader("Content-Type", ""),
        )
    except TransportFailure:
        raise
    except ssl.SSLError:
        raise TransportFailure("tls") from None
    except TimeoutError:
        raise TransportFailure("timeout", retryable=True) from None
    except OSError:
        raise TransportFailure("network", retryable=True) from None
    finally:
        if response is not None:
            response.close()
        connection.close()


def _child_command(parent_pid: int) -> list[str]:
    return [
        os.path.realpath(sys.executable),
        "-I",
        str(Path(__file__).resolve()),
        "--child",
        str(parent_pid),
    ]


def _arm_parent_death(expected_parent_pid: int) -> None:
    """Kill the transport child if its exact parent exits on this Linux host."""
    if (
        sys.platform != "linux"
        or not isinstance(expected_parent_pid, int)
        or isinstance(expected_parent_pid, bool)
        or expected_parent_pid <= 1
    ):
        raise TransportFailure("parent_guard_unavailable")
    libc = ctypes.CDLL(None, use_errno=True)
    prctl = libc.prctl
    prctl.argtypes = [
        ctypes.c_int,
        ctypes.c_ulong,
        ctypes.c_ulong,
        ctypes.c_ulong,
        ctypes.c_ulong,
    ]
    prctl.restype = ctypes.c_int
    if prctl(1, signal.SIGKILL, 0, 0, 0) != 0:  # PR_SET_PDEATHSIG
        raise TransportFailure("parent_guard_unavailable")
    if os.getppid() != expected_parent_pid:
        os.kill(os.getpid(), signal.SIGKILL)
        os._exit(2)


def _kill_owned_process(process: subprocess.Popen) -> None:
    try:
        os.killpg(process.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    try:
        process.wait(timeout=2)
    except (ProcessLookupError, subprocess.TimeoutExpired):
        pass
    for stream in (process.stdin, process.stdout):
        if stream is not None:
            stream.close()


def _install_termination_handlers(
    process: subprocess.Popen,
) -> dict[int, signal.Handlers]:
    """Reap the owned child before preserving the caller's SIGTERM behavior."""
    previous: dict[int, signal.Handlers] = {}

    def terminate(signum: int, frame) -> None:
        _kill_owned_process(process)
        prior = previous[signum]
        signal.signal(signum, prior)
        if prior == signal.SIG_DFL:
            os.kill(os.getpid(), signum)
        elif prior != signal.SIG_IGN:
            prior(signum, frame)

    try:
        previous[signal.SIGTERM] = signal.getsignal(signal.SIGTERM)
        signal.signal(signal.SIGTERM, terminate)
    except ValueError:
        previous.clear()
    return previous


def _restore_termination_handlers(previous: dict[int, signal.Handlers]) -> None:
    for signum, handler in previous.items():
        signal.signal(signum, handler)


def post(
    url: str,
    body: bytes,
    token: str,
    policy_text: str,
    *,
    timeout: float,
) -> Response:
    """Run one request in an owned process group with no inherited environment."""
    validate_endpoint(url)
    if not isinstance(body, bytes) or len(body) > MAX_REQUEST_BYTES:
        raise TransportFailure("request_too_large")
    if (
        not isinstance(token, str)
        or not token
        or len(token) > MAX_CREDENTIAL_LENGTH
        or "\r" in token
        or "\n" in token
    ):
        raise TransportFailure("invalid_credential")
    parse_address_policy(policy_text)
    if not isinstance(timeout, (int, float)) or not (
        0 < timeout <= MAX_REQUEST_TIMEOUT
    ):
        raise TransportFailure("invalid_timeout")
    request = json.dumps(
        {
            "url": url,
            "body": base64.b64encode(body).decode("ascii"),
            "token": token,
            "policy": policy_text,
            "timeout": float(timeout),
        },
        separators=(",", ":"),
    ).encode("utf-8")
    process = subprocess.Popen(
        _child_command(os.getpid()),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        env={},
        cwd="/",
        close_fds=True,
        start_new_session=True,
    )
    previous_handlers = _install_termination_handlers(process)
    try:
        try:
            stdout, _ = process.communicate(input=request, timeout=float(timeout))
        except subprocess.TimeoutExpired:
            _kill_owned_process(process)
            raise TransportFailure("timeout", retryable=True) from None
        except BaseException:
            _kill_owned_process(process)
            raise
    finally:
        _restore_termination_handlers(previous_handlers)
    try:
        result = json.loads(stdout.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise TransportFailure("transport_protocol") from None
    if not isinstance(result, dict):
        raise TransportFailure("transport_protocol")
    if process.returncode != 0 or result.get("ok") is not True:
        reason = result.get("reason")
        if not isinstance(reason, str) or reason not in {
            "address_not_allowed",
            "disallowed_url",
            "dns",
            "invalid_address_policy",
            "invalid_credential",
            "invalid_response",
            "network",
            "request_too_large",
            "response_too_large",
            "timeout",
            "tls",
        }:
            reason = "transport_failure"
        raise TransportFailure(reason, retryable=bool(result.get("retryable")))
    try:
        raw = base64.b64decode(result["body"], validate=True)
        status = int(result["status"])
        content_type = str(result.get("content_type", ""))
    except (KeyError, TypeError, ValueError):
        raise TransportFailure("transport_protocol") from None
    if len(raw) > MAX_RESPONSE_BYTES or not (100 <= status <= 599):
        raise TransportFailure("transport_protocol")
    return Response(status, raw, content_type)


def _child_main(expected_parent_pid: int | None = None) -> int:
    try:
        if expected_parent_pid is not None:
            _arm_parent_death(expected_parent_pid)
        raw = sys.stdin.buffer.read(_MAX_CHILD_INPUT + 1)
        if len(raw) > _MAX_CHILD_INPUT:
            raise TransportFailure("request_too_large")
        request = json.loads(raw.decode("utf-8"))
        body = base64.b64decode(request["body"], validate=True)
        response = send_once(
            request["url"],
            body,
            request["token"],
            request["policy"],
            timeout=request["timeout"],
        )
        result = {
            "ok": True,
            "status": response.status,
            "body": base64.b64encode(response.body).decode("ascii"),
            "content_type": response.content_type,
        }
        status = 0
    except TransportFailure as error:
        result = {
            "ok": False,
            "reason": error.reason,
            "retryable": error.retryable,
        }
        status = 2
    except (KeyError, TypeError, ValueError, UnicodeDecodeError, json.JSONDecodeError):
        result = {"ok": False, "reason": "transport_protocol", "retryable": False}
        status = 2
    sys.stdout.write(json.dumps(result, separators=(",", ":")))
    return status


if __name__ == "__main__":
    if (
        len(sys.argv) != 3
        or sys.argv[1] != "--child"
        or not sys.argv[2].isdecimal()
        or int(sys.argv[2]) <= 1
    ):
        raise SystemExit(2)
    raise SystemExit(_child_main(int(sys.argv[2])))
