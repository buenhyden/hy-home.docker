"""Isolated bounded HTTP transport, without Gateway interpretation or wiring."""

import base64
import hashlib
import json
import math
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from urllib.parse import urlsplit

from . import policy
from .delivery import FailureKind, TransportFailure

_LIMIT = 1024 * 1024
_NAME = re.compile(r"[!#$%&'*+.^_`|~0-9A-Za-z-]+\Z")
_HOST = re.compile(r"[A-Za-z0-9.-]+\Z")

# The isolated child receives all sensitive data on stdin, never on its command
# line. Parent timeout covers DNS, TLS, request, headers, and body collection.
_CHILD = r"""
import base64, http.client, json, ssl, sys
try:
    p = json.loads(sys.stdin.buffer.read())
    cls = http.client.HTTPSConnection if p['scheme'] == 'https' else http.client.HTTPConnection
    kw = {'timeout': p['timeout']}
    if p['scheme'] == 'https':
        kw['context'] = ssl.create_default_context()
    c = cls(p['host'], p['port'], **kw)
    try:
        try:
            c.connect()
        except ssl.SSLCertVerificationError:
            print('{"error":"tls"}')
            sys.exit(0)
        except Exception:
            print('{"error":"not_sent"}')
            sys.exit(0)
        headers = {p['name']: p['value']}
        if p['content_type'] is not None:
            headers['Content-Type'] = p['content_type']
        c.request('POST', p['path'], body=base64.b64decode(p['body'], validate=True), headers=headers)
        r = c.getresponse()
        if r.length is not None and r.length > p['max_bytes']:
            raise ValueError()
        b = r.read(p['max_bytes'] + 1)
        if len(b) > p['max_bytes'] or r.length not in (None, 0):
            raise ValueError()
        ct = r.getheader('Content-Type')
        if ct and (len(ct) > 256 or any(ord(x) < 32 or ord(x) > 126 for x in ct)):
            ct = None
        print(json.dumps({'status': r.status, 'body': base64.b64encode(b).decode('ascii'), 'content_type': ct}))
    finally:
        c.close()
except Exception:
    sys.exit(1)
"""


@dataclass(frozen=True)
class HttpResponse:
    status: int
    body: bytes = field(repr=False)
    content_type: str | None = field(default=None, repr=False)


def _parse_endpoint(value, allow_loopback_http):
    if (
        not isinstance(value, str)
        or not value
        or any(ord(c) <= 32 or ord(c) >= 127 for c in value)
        or "\\" in value
    ):
        raise ValueError("invalid_endpoint")
    try:
        parsed = urlsplit(value)
        host, port = parsed.hostname, parsed.port
    except ValueError:
        raise ValueError("invalid_endpoint") from None
    if (
        parsed.scheme not in ("http", "https")
        or not host
        or parsed.username is not None
        or parsed.password is not None
        or parsed.query
        or parsed.fragment
        or "?" in value
        or "#" in value
        or not parsed.path.startswith("/")
        or not (host == "::1" or _HOST.fullmatch(host))
    ):
        raise ValueError("invalid_endpoint")
    if parsed.scheme == "http" and not (
        allow_loopback_http is True and host in ("127.0.0.1", "::1")
    ):
        raise ValueError("invalid_endpoint")
    return parsed.scheme, host, port, parsed.path


def _auth(pair):
    try:
        if not isinstance(pair, tuple) or len(pair) != 2:
            raise ValueError
        name, value = pair
        if (
            not isinstance(name, str)
            or not _NAME.fullmatch(name)
            or name.lower()
            in (
                "host",
                "content-length",
                "transfer-encoding",
                "connection",
                "content-type",
            )
            or not isinstance(value, str)
            or not value
            or len(value) > 4096
            or any(ord(c) < 32 or ord(c) > 126 for c in value)
        ):
            raise ValueError
        return name, value
    except Exception:
        raise TransportFailure(FailureKind.AUTH) from None


@dataclass(frozen=True, init=False, repr=False)
class HttpTransport:
    """Fixed endpoint, with pre-resolved in-memory auth and no replay.

    The deadline covers the spawned child's network operation. Python cannot
    interrupt process creation itself; this class performs no credential I/O.
    """

    _endpoint: tuple
    _destination: str
    _auth_header: tuple
    _timeout: float
    _max_bytes: int
    _content_type: str | None

    def __init__(
        self,
        *,
        endpoint,
        destination,
        auth,
        timeout=10,
        max_bytes=_LIMIT,
        content_type=None,
        allow_loopback_http=False,
    ):
        parsed = _parse_endpoint(endpoint, allow_loopback_http)
        if (
            not isinstance(destination, str)
            or not re.fullmatch(r"[A-Za-z0-9_.-]{1,128}", destination)
            or type(timeout) not in (int, float)
            or not math.isfinite(timeout)
            or not 0 < timeout <= 60
            or type(max_bytes) is not int
            or not 1 <= max_bytes <= _LIMIT
            or content_type not in (None, "application/json")
        ):
            raise ValueError("invalid_configuration")
        object.__setattr__(self, "_endpoint", parsed)
        object.__setattr__(self, "_destination", destination)
        object.__setattr__(self, "_auth_header", _auth(auth))
        object.__setattr__(self, "_timeout", timeout)
        object.__setattr__(self, "_max_bytes", max_bytes)
        object.__setattr__(self, "_content_type", content_type)

    @property
    def endpoint_sha256(self):
        # Hash the validated, exact network target; credentials are never included.
        return hashlib.sha256(
            json.dumps(self._endpoint, separators=(",", ":")).encode("ascii")
        ).hexdigest()

    def send(self, request):
        if (
            not isinstance(request.key, tuple)
            or len(request.key) != 2
            or (policy.evidence_required(request.key[0]) and not request.trust)
            or request.destination != self._destination
            or request.endpoint_sha256 != self.endpoint_sha256
            or not isinstance(request.body, bytes)
            or len(request.body) > self._max_bytes
        ):
            raise TransportFailure(FailureKind.NOT_SENT)
        name, value = self._auth_header
        scheme, host, port, path = self._endpoint
        payload = json.dumps(
            {
                "scheme": scheme,
                "host": host,
                "port": port,
                "path": path,
                "name": name,
                "value": value,
                "body": base64.b64encode(request.body).decode("ascii"),
                "timeout": self._timeout,
                "max_bytes": self._max_bytes,
                "content_type": self._content_type,
            }
        ).encode("ascii")
        try:
            result = subprocess.run(
                # The resolved target is what trust checks; a venv bin/python
                # link is not. The child needs only the standard library.
                [os.path.realpath(sys.executable), "-I", "-c", _CHILD],
                input=payload,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                timeout=self._timeout,
                env={},
                check=False,
            )
            if result.returncode:
                raise ValueError
            answer = json.loads(result.stdout)
            if answer == {"error": "tls"}:
                raise TransportFailure(FailureKind.TLS)
            if answer == {"error": "not_sent"}:
                raise TransportFailure(FailureKind.NOT_SENT)
            if (
                set(answer) != {"status", "body", "content_type"}
                or type(answer["status"]) is not int
                or not 100 <= answer["status"] <= 599
            ):
                raise ValueError
            body = base64.b64decode(answer["body"], validate=True)
            if len(body) > self._max_bytes:
                raise ValueError
            ct = answer["content_type"]
            if ct is not None and (
                not isinstance(ct, str)
                or len(ct) > 256
                or any(ord(c) < 32 or ord(c) > 126 for c in ct)
            ):
                raise ValueError
            return HttpResponse(answer["status"], body, ct)
        except TransportFailure:
            raise
        except Exception:
            raise TransportFailure(FailureKind.AMBIGUOUS) from None

    def reconcile(self, request):
        raise TransportFailure(FailureKind.AMBIGUOUS)
