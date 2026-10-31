"""SSRF-guarded fetch of a report source for the attester.

The attester runs next to LAN and Docker networks that must stay unreachable,
so every hop is vetted before any byte leaves: https only, no userinfo, not the
home zone, and every resolved address globally routable. The connection goes to
the vetted IP (no second lookup) with the name kept for SNI and Host. The guard
has no switch; tests inject only `resolve`, `connect` and `now`.
"""

import hashlib
import http.client
import ipaddress
import socket
import ssl
from dataclasses import dataclass
from datetime import UTC, datetime
from urllib.parse import urljoin, urlsplit

MAX_BYTES = 2 * 1024 * 1024
MAX_REDIRECTS = 5
MAX_URL = 2048
TIMEOUT = 20.0
ZONE = "hy.home.arpa"
REDIRECTS = (301, 302, 303, 307, 308)
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


def _tls_connect(ip, port, server_hostname, timeout):
    context = ssl.create_default_context()
    raw = socket.create_connection((ip, port), timeout)
    try:
        return context.wrap_socket(raw, server_hostname=server_hostname)
    except BaseException:
        raw.close()
        raise


class _Connection(http.client.HTTPSConnection):
    """HTTPS to a vetted IP; Host and SNI keep the original name."""

    def __init__(self, host, port, ip, connect, timeout):
        super().__init__(host, port, timeout=timeout)
        self._ip = ip
        self._connect = connect

    def connect(self):
        self.sock = self._connect(self._ip, self.port, self.host, self.timeout)


def _utc_millis(moment):
    moment = moment.astimezone(UTC)
    return moment.strftime("%Y-%m-%dT%H:%M:%S.") + f"{moment.microsecond // 1000:03d}Z"


def _is_global(value):
    address = ipaddress.ip_address(value)
    if getattr(address, "ipv4_mapped", None):
        address = address.ipv4_mapped
    return address.is_global


def _vet(url, resolve):
    """Return (host, port, first vetted IP) or raise FetchFailure."""
    if len(url) > MAX_URL or any(
        c.isspace() or ord(c) < 32 or ord(c) == 127 for c in url
    ):
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
    host = host.lower().rstrip(".")
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
    return host, port or 443, addresses[0]


def _get(host, port, ip, target, connect, deadline_timeout):
    conn = _Connection(host, port, ip, connect, deadline_timeout)
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
        if status in REDIRECTS or status >= 300:
            return status, location, content_type, b""
        length = response.getheader("Content-Length")
        if length and length.isdigit() and int(length) > MAX_BYTES:
            raise FetchFailure("size")
        body = response.read(MAX_BYTES + 1)
        if len(body) > MAX_BYTES:
            raise FetchFailure("size")
        return status, location, content_type, body
    finally:
        conn.close()


def fetch(url, *, resolve=socket.getaddrinfo, connect=None, now=None):
    connect = connect or _tls_connect
    now = now or (lambda: datetime.now(UTC))
    for _ in range(MAX_REDIRECTS + 1):
        host, port, ip = _vet(url, resolve)
        parts = urlsplit(url)
        target = (parts.path or "/") + (f"?{parts.query}" if parts.query else "")
        try:
            status, location, content_type, body = _get(
                host, port, ip, target, connect, TIMEOUT
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
            url = urljoin(url, location)
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
