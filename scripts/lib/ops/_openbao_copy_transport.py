"""Exact-origin bounded HTTPS for W48; no environment proxies, DNS or redirects."""

from __future__ import annotations

import ipaddress
import json
import math
import re
import socket
import ssl
import threading
import time
from dataclasses import dataclass
from urllib.parse import urlsplit

from scripts.lib.ops._openbao_copy_io import MAX_BYTES, MigrationError


@dataclass(frozen=True, slots=True)
class CopyBudget:
    connect: float
    read: float
    total: float


def _dns_hostname(hostname):
    if not isinstance(hostname, str) or not 1 <= len(hostname) <= 253:
        return False
    try:
        ipaddress.ip_address(hostname)
    except ValueError:
        pass
    else:
        return False
    return all(
        re.fullmatch(r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?", label)
        for label in hostname.split(".")
    )


def validate_endpoint(origin, connect_ip, budget):
    if type(origin) is not str or len(origin) > 267:
        raise MigrationError("copy_endpoint_invalid")
    try:
        url = urlsplit(origin)
        port = url.port or 443
        address = ipaddress.ip_address(connect_ip)
        if (
            url.scheme != "https"
            or not _dns_hostname(url.hostname)
            or url.username is not None
            or url.password is not None
            or url.path
            or url.query
            or url.fragment
            or origin != f"https://{url.hostname}" + (f":{port}" if url.port else "")
            or not 1 <= port <= 65535
        ):
            raise ValueError
    except (ValueError, TypeError):
        raise MigrationError("copy_endpoint_invalid") from None
    if (
        type(budget) is not CopyBudget
        or any(
            type(value) not in {float, int}
            or not math.isfinite(value)
            or not 0 < value <= 60
            for value in (budget.connect, budget.read, budget.total)
        )
        or budget.total < max(budget.connect, budget.read)
    ):
        raise MigrationError("copy_budget_invalid")
    return url.hostname, port, address


def _remaining(deadline):
    remaining = deadline - time.monotonic()
    if remaining <= 0:
        raise MigrationError("copy_deadline_exceeded")
    return remaining


def _read_exact(stream, amount):
    parts, remaining = (), amount
    while remaining:
        part = stream.read(min(remaining, 65536))
        if not part:
            raise MigrationError("copy_response_incomplete")
        parts, remaining = (*parts, part), remaining - len(part)
    return b"".join(parts)


def _headers(stream):
    status_line = stream.readline(4097)
    if not re.fullmatch(rb"HTTP/1\.[01] [1-5][0-9]{2} [^\r\n]*\r\n", status_line):
        raise MigrationError("copy_response_invalid")
    status, total, headers = int(status_line.split(b" ")[1]), len(status_line), {}
    while True:
        line = stream.readline(4097)
        total += len(line)
        if len(line) > 4096 or total > 32768 or not line.endswith(b"\r\n"):
            raise MigrationError("copy_response_bounds")
        if line == b"\r\n":
            return status, headers
        match = re.fullmatch(
            rb"([!#$%&'*+.^_`|~0-9A-Za-z-]+):[ \t]*([^\r\n]*)\r\n", line
        )
        if not match:
            raise MigrationError("copy_response_invalid")
        key, value = match.group(1).lower(), match.group(2).strip()
        if key in headers:
            raise MigrationError("copy_response_invalid")
        headers = {**headers, key: value}


def _body(stream, headers):
    if b"content-length" in headers and b"transfer-encoding" in headers:
        raise MigrationError("copy_response_invalid")
    if b"transfer-encoding" in headers:
        if headers[b"transfer-encoding"].lower() != b"chunked":
            raise MigrationError("copy_response_invalid")
        data, chunks = b"", 0
        while True:
            line = stream.readline(128)
            if not re.fullmatch(rb"[0-9A-Fa-f]{1,8}\r\n", line):
                raise MigrationError("copy_response_invalid")
            size = int(line.strip(), 16)
            chunks += 1
            if len(data) + size > MAX_BYTES or chunks > 4096:
                raise MigrationError("copy_response_bounds")
            if not size:
                if stream.readline(3) != b"\r\n":
                    raise MigrationError("copy_response_invalid")
                return data
            data += _read_exact(stream, size)
            if _read_exact(stream, 2) != b"\r\n":
                raise MigrationError("copy_response_invalid")
    length = headers.get(b"content-length")
    if length is not None:
        if not re.fullmatch(rb"[0-9]{1,9}", length) or int(length) > MAX_BYTES:
            raise MigrationError("copy_response_bounds")
        return _read_exact(stream, int(length))
    data = stream.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise MigrationError("copy_response_bounds")
    return data


class CopyTransport:
    """One immutable TLS context and one whole-wave budget; no write retry."""

    def __init__(
        self, origin, connect_ip, budget, context, allowed_paths, deadline, check_inputs
    ):
        self.hostname, self.port, self.address = validate_endpoint(
            origin, connect_ip, budget
        )
        self.budget, self.context = budget, context
        self.paths, self.deadline = frozenset(allowed_paths), deadline
        self.check_inputs = check_inputs
        if not callable(check_inputs) or any(
            not isinstance(path, str)
            or not re.fullmatch(
                r"/v1/[A-Za-z0-9_-]{1,64}/(?:config|(?:data|metadata)/[A-Za-z0-9][A-Za-z0-9_./-]{0,255})",
                path,
            )
            or any(part in {".", "..", ""} for part in path.split("/")[1:])
            for path in self.paths
        ):
            raise MigrationError("copy_request_not_bound")
        if not context.check_hostname or context.verify_mode != ssl.CERT_REQUIRED:
            raise MigrationError("copy_tls_invalid")

    def request(self, method, path, token, payload=None):
        if method not in {"GET", "POST"} or path not in self.paths:
            raise MigrationError("copy_request_not_bound")
        if method == "POST" and "/data/" not in path:
            raise MigrationError("copy_request_not_bound")
        if not isinstance(token, str) or not re.fullmatch(
            r"[A-Za-z0-9._-]{1,4096}", token
        ):
            raise MigrationError("copy_token_invalid")
        self.check_inputs()
        remaining = _remaining(self.deadline)
        family = socket.AF_INET6 if self.address.version == 6 else socket.AF_INET
        connection = socket.socket(family, socket.SOCK_STREAM)

        def interrupt():
            try:
                connection.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass

        timer = threading.Timer(remaining, interrupt)
        timer.daemon = True
        timer.start()
        try:
            connection.settimeout(min(self.budget.connect, _remaining(self.deadline)))
            connection.connect((str(self.address), self.port))
            connection = self.context.wrap_socket(
                connection, server_hostname=self.hostname, do_handshake_on_connect=False
            )
            connection.do_handshake()
            connection.settimeout(min(self.budget.read, _remaining(self.deadline)))
            body = (
                b""
                if payload is None
                else json.dumps(
                    payload, ensure_ascii=True, separators=(",", ":")
                ).encode("ascii")
            )
            if len(body) > MAX_BYTES * 6 + 1024:
                raise MigrationError("copy_request_bounds")
            host = f"{self.hostname}:{self.port}"
            head = (
                f"{method} {path} HTTP/1.1\r\nHost: {host}\r\nX-Vault-Token: {token}\r\n"
                f"Content-Type: application/json\r\nContent-Length: {len(body)}\r\nConnection: close\r\n\r\n"
            ).encode("ascii")
            connection.sendall(head + body)
            with connection.makefile("rb") as stream:
                status, headers = _headers(stream)
                if 300 <= status < 400:
                    raise MigrationError("copy_redirect_denied")
                if (
                    headers.get(b"content-type", b"").split(b";", 1)[0].strip().lower()
                    != b"application/json"
                ):
                    raise MigrationError("copy_response_invalid")
                raw = _body(stream, headers)
            _remaining(self.deadline)
            from scripts.lib.ops.openbao_consumer_migration import parse_public_json

            try:
                document = parse_public_json(raw)
            except MigrationError:
                raise MigrationError("copy_response_invalid") from None
            return status, document
        except (OSError, ssl.SSLError, ValueError, UnicodeError):
            raise MigrationError("copy_transport_failed") from None
        finally:
            timer.cancel()
            connection.close()
