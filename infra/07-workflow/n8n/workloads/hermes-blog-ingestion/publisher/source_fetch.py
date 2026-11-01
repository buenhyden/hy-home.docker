"""SSRF-guarded fetch of a report source for the attester.

The attester runs next to LAN and Docker networks that must stay unreachable,
so every hop is vetted before any byte leaves: https only, no userinfo, not the
home zone, and every resolved address globally routable. The connection goes to
the vetted IP (no second lookup) with the name kept for SNI and Host. The guard
has no switch; tests inject only `resolve`, `connect`, `now` and `monotonic`.

The 20 s limit bounds the whole fetch: the socket is wrapped so every send and
recv re-arms its timeout from the one deadline, which covers headers and body
across all hops. `getaddrinfo` has no timeout in the stdlib and the TLS
handshake only gets the remaining time as its socket timeout, so those two
steps are bounded per operation, not by the deadline.
"""

import hashlib
import http.client
import io
import ipaddress
import os
import socket
import ssl
import time
import unicodedata
from dataclasses import dataclass
from datetime import UTC, datetime
from urllib.parse import quote, urljoin, urlsplit, urlunsplit

MAX_BYTES = 2 * 1024 * 1024
MAX_REDIRECTS = 5
MAX_URL = 2048
TIMEOUT = 20.0
# Internal names are refused before DNS; the site sets its own zone.
ZONE = os.environ.get("HERMES_INTERNAL_ZONE", "hy.home.arpa").lower().rstrip(".")
REDIRECTS = (301, 302, 303, 307, 308)
CHUNK = 64 * 1024
_SAFE = "/%:@!$&'()*+,;=-._~"
USER_AGENT = "hy-home-attester/1"


class FetchFailure(Exception):
    def __init__(self, reason, transient=False):
        super().__init__(reason)
        self.reason = reason
        self.transient = transient


@dataclass(frozen=True)
class FetchResult:
    final_url: str
    status: int
    sha256: str
    fetched_at: str
    content_type: str
    body: bytes


def tls_context():
    """Verifying client context; TLS 1.2 is the oldest protocol accepted."""
    context = ssl.create_default_context()
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    return context


def _tls_connect(ip, port, server_hostname, timeout):
    context = tls_context()
    raw = socket.create_connection((ip, port), timeout)
    try:
        return context.wrap_socket(raw, server_hostname=server_hostname)
    except BaseException:
        raw.close()
        raise


class _DeadlineSock:
    """Socket wrapper: each send/recv is limited by the time left to the deadline."""

    def __init__(self, sock, deadline, monotonic):
        self._sock = sock
        self._deadline = deadline
        self._monotonic = monotonic

    def _arm(self):
        left = self._deadline - self._monotonic()
        if left <= 0:
            raise TimeoutError("fetch deadline")
        self._sock.settimeout(max(0.001, left))

    def sendall(self, data):
        self._arm()
        self._sock.sendall(data)

    def recv_into(self, buffer, nbytes=0):
        self._arm()
        return self._sock.recv_into(buffer, nbytes)

    def makefile(self, mode="rb", buffering=None):
        return io.BufferedReader(_Raw(self))

    def settimeout(self, value):
        pass

    def close(self):
        self._sock.close()


class _Raw(io.RawIOBase):
    def __init__(self, sock):
        self._wrapped = sock

    def readable(self):
        return True

    def readinto(self, buffer):
        return self._wrapped.recv_into(buffer)


class _Connection(http.client.HTTPSConnection):
    """HTTPS to a vetted IP; Host and SNI keep the original name."""

    def __init__(self, host, port, ip, connect, deadline, monotonic):
        super().__init__(host, port, timeout=_remaining(deadline, monotonic))
        self._ip = ip
        self._connect = connect
        self._deadline = deadline
        self._monotonic = monotonic

    def connect(self):
        sock = self._connect(self._ip, self.port, self.host, self.timeout)
        self.sock = _DeadlineSock(sock, self._deadline, self._monotonic)


def _utc_millis(moment):
    moment = moment.astimezone(UTC)
    return moment.strftime("%Y-%m-%dT%H:%M:%S.") + f"{moment.microsecond // 1000:03d}Z"


_NO_GLOBAL_V6 = tuple(
    ipaddress.ip_network(n) for n in ("::/96", "64:ff9b::/96", "64:ff9b:1::/48")
)


def _is_global(value):
    address = ipaddress.ip_address(value)
    if getattr(address, "ipv4_mapped", None):
        address = address.ipv4_mapped
    elif address.version == 6 and any(address in net for net in _NO_GLOBAL_V6):
        return False  # IPv4-compatible and NAT64 forms embed an unvetted IPv4
    return address.is_global


def _canonical(url):
    """Return the ASCII form of url (IDNA host, percent-encoded path/query, no fragment)."""
    if any(c.isspace() or unicodedata.category(c) in ("Cc", "Cf") for c in url):
        raise FetchFailure("url")
    try:
        parts = urlsplit(url)
        host, port = parts.hostname, parts.port
    except ValueError:
        raise FetchFailure("url") from None
    if parts.scheme != "https":
        raise FetchFailure("scheme")
    if not host or "@" in parts.netloc:
        raise FetchFailure("url")
    try:
        ipaddress.ip_address(host)
        netloc = f"[{host}]" if ":" in host else host
    except ValueError:
        try:
            netloc = host.encode("idna").decode("ascii")
        except UnicodeError:
            raise FetchFailure("url") from None
    if port:
        netloc += f":{port}"
    path = quote(parts.path, safe=_SAFE)
    query = quote(parts.query, safe=_SAFE + "?")
    canonical = urlunsplit(("https", netloc, path, query, ""))
    if len(canonical) > MAX_URL:
        raise FetchFailure("url")
    return canonical


def _vet(url, resolve):
    """Return (canonical url, host, port, first vetted IP) or raise FetchFailure."""
    url = _canonical(url)
    parts = urlsplit(url)
    host, port = parts.hostname.rstrip("."), parts.port
    if host == ZONE or host.endswith("." + ZONE):
        raise FetchFailure("zone")
    try:
        addresses = [str(ipaddress.ip_address(host))]
    except ValueError:
        try:
            infos = resolve(host, port or 443, type=socket.SOCK_STREAM)
        except OSError:
            raise FetchFailure("dns", True) from None
        addresses = [info[4][0] for info in infos]
        if not addresses:
            raise FetchFailure("dns", True) from None
    try:
        vetted = all(_is_global(a) for a in addresses)
    except ValueError:
        vetted = False
    if not vetted:
        raise FetchFailure("address")
    # ponytail: first vetted address only, no fallback to the others.
    return url, host, port or 443, addresses[0]


def _remaining(deadline, monotonic):
    left = deadline - monotonic()
    if left <= 0:
        raise FetchFailure("timeout", True)
    return left


def _get(host, port, ip, target, connect, deadline, monotonic):
    conn = _Connection(host, port, ip, connect, deadline, monotonic)
    try:
        conn.request(
            "GET",
            target,
            headers={"User-Agent": USER_AGENT, "Accept-Encoding": "identity"},
        )
        response = conn.getresponse()
        status = response.status
        location = response.getheader("Location")
        content_type = response.getheader("Content-Type", "")
        if status >= 300:
            return status, location, content_type, b""
        length = response.getheader("Content-Length")
        if length and length.isdigit() and int(length) > MAX_BYTES:
            raise FetchFailure("size")
        chunks, total = [], 0
        while True:
            chunk = response.read(CHUNK)
            if not chunk:
                break
            total += len(chunk)
            if total > MAX_BYTES:
                raise FetchFailure("size")
            chunks.append(chunk)
        return status, location, content_type, b"".join(chunks)
    finally:
        conn.close()


def _redirect_target(base, location):
    """Join a Location against base; http.client decoded its bytes as latin-1."""
    try:
        location = location.encode("latin-1").decode("utf-8")
    except UnicodeError:
        raise FetchFailure("url") from None
    try:
        return urljoin(base, location)
    except ValueError:  # e.g. an unterminated IPv6 literal
        raise FetchFailure("url") from None


def fetch(
    url, *, resolve=socket.getaddrinfo, connect=None, now=None, monotonic=time.monotonic
):
    connect = connect or _tls_connect
    now = now or (lambda: datetime.now(UTC))
    deadline = monotonic() + TIMEOUT
    for _ in range(MAX_REDIRECTS + 1):
        url, host, port, ip = _vet(url, resolve)
        parts = urlsplit(url)
        target = (parts.path or "/") + (f"?{parts.query}" if parts.query else "")
        try:
            status, location, content_type, body = _get(
                host, port, ip, target, connect, deadline, monotonic
            )
        except FetchFailure:
            raise
        except ssl.SSLError:
            raise FetchFailure("tls") from None
        except TimeoutError:
            raise FetchFailure("timeout", True) from None
        except (OSError, http.client.HTTPException):
            raise FetchFailure("connect", True) from None
        if status in REDIRECTS:
            if not location:
                raise FetchFailure("status")
            url = _redirect_target(url, location)
            continue
        if status == 429 or status >= 500:
            raise FetchFailure("status", True)
        if status >= 300 or status < 200:
            raise FetchFailure("status")
        return FetchResult(
            final_url=url,
            status=status,
            sha256=hashlib.sha256(body).hexdigest(),
            fetched_at=_utc_millis(now()),
            content_type=content_type,
            body=body,
        )
    raise FetchFailure("redirects")
