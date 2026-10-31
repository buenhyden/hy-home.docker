"""Guarded source fetcher: SSRF refusals, redirects, caps, classification."""

import hashlib
import io
import socket
import ssl
import sys
import unittest
from datetime import UTC, datetime
from pathlib import Path

WORKLOAD = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WORKLOAD))
from publisher import source_fetch  # noqa: E402
from publisher.source_fetch import FetchFailure, fetch  # noqa: E402

PUBLIC = "93.184.216.34"


def answer(*addrs):
    return [
        (socket.AF_INET6 if ":" in a else socket.AF_INET, 1, 6, "", (a, 443))
        for a in addrs
    ]


def resolver(table=None, default=(PUBLIC,)):
    seen = []

    def resolve(host, port, *args, **kwargs):
        seen.append(host)
        return answer(*(table or {}).get(host, default))

    resolve.seen = seen
    return resolve


def http(status, body=b"", **headers):
    head = (
        f"HTTP/1.1 {status} X\r\nContent-Length: {len(body)}\r\nConnection: close\r\n"
    )
    head += "".join(f"{k.replace('_', '-')}: {v}\r\n" for k, v in headers.items())
    return head.encode() + b"\r\n" + body


class FakeSock:
    def __init__(self, response):
        self.response = response
        self.sent = b""

    def sendall(self, data):
        self.sent += data

    def makefile(self, *args, **kwargs):
        return io.BytesIO(self.response)

    def settimeout(self, value):
        pass

    def close(self):
        pass


def connector(*responses):
    """Return (connect, calls); each connect pops the next canned response."""
    queue = list(responses)
    calls = []

    def connect(ip, port, server_hostname, timeout):
        calls.append((ip, port, server_hostname, timeout))
        item = queue.pop(0)
        if isinstance(item, Exception):
            raise item
        sock = FakeSock(item)
        calls[-1] += (sock,)
        return sock

    return connect, calls


def refused(test, url, reason, transient=False, **kw):
    with test.assertRaises(FetchFailure) as ctx:
        fetch(url, **kw)
    test.assertEqual(ctx.exception.reason, reason)
    test.assertEqual(ctx.exception.transient, transient)


class GuardTests(unittest.TestCase):
    def test_rejects_non_https(self):
        connect, calls = connector()
        refused(
            self, "http://example.com/", "scheme", resolve=resolver(), connect=connect
        )
        self.assertEqual(calls, [])

    def test_rejects_private_loopback_linklocal_and_zone(self):
        for host in (
            "10.0.0.1",
            "127.0.0.1",
            "169.254.1.1",
            "[::1]",
            "[fd00::1]",
            "[::ffff:10.0.0.1]",
        ):
            connect, calls = connector()
            with self.subTest(host=host):
                refused(self, f"https://{host}/", "address", connect=connect)
                self.assertEqual(calls, [])
        for host in ("n8n.hy.home.arpa", "hy.home.arpa", "N8N.HY.HOME.ARPA."):
            resolve = resolver()
            with self.subTest(host=host):
                refused(self, f"https://{host}/", "zone", resolve=resolve)
                self.assertEqual(resolve.seen, [])

    def test_any_non_global_address_in_answer_rejects(self):
        resolve = resolver({"mixed.example": (PUBLIC, "10.0.0.5")})
        connect, calls = connector(http(200, b"x"))
        refused(
            self, "https://mixed.example/", "address", resolve=resolve, connect=connect
        )
        self.assertEqual(calls, [])

    def test_userinfo_and_overlong_and_whitespace_urls_rejected(self):
        for url in (
            "https://user:pw@example.com/",
            "https://example.com/" + "a" * 2048,
            "https://example.com/a b",
            "https://example.com/a\x00b",
        ):
            with self.subTest(url=url[:40]):
                refused(self, url, "url", resolve=resolver())

    def test_connects_to_vetted_ip_with_sni_name_and_single_lookup(self):
        resolve = resolver()
        connect, calls = connector(http(200, b"hi"))
        fetch("https://example.com/p", resolve=resolve, connect=connect)
        self.assertEqual(resolve.seen, ["example.com"])
        ip, port, name, timeout, sock = calls[0]
        self.assertEqual((ip, port, name), (PUBLIC, 443, "example.com"))
        self.assertLessEqual(timeout, 20)
        self.assertIn(b"Host: example.com\r\n", sock.sent)
        self.assertIn(b"User-Agent: hy-home-attester/1\r\n", sock.sent)
        self.assertTrue(sock.sent.startswith(b"GET /p HTTP/1.1"))


class RedirectTests(unittest.TestCase):
    def test_redirect_hop_to_private_is_refused(self):
        connect, calls = connector(http(302, Location="https://10.1.2.3/"))
        refused(
            self, "https://example.com/", "address", resolve=resolver(), connect=connect
        )
        self.assertEqual(len(calls), 1)

    def test_redirect_hop_to_http_or_zone_is_refused(self):
        connect, _ = connector(http(301, Location="http://example.com/"))
        refused(
            self, "https://example.com/", "scheme", resolve=resolver(), connect=connect
        )
        connect, _ = connector(http(301, Location="https://n8n.hy.home.arpa/"))
        refused(
            self, "https://example.com/", "zone", resolve=resolver(), connect=connect
        )

    def test_relative_redirect_is_followed_and_final_url_recorded(self):
        connect, calls = connector(http(307, Location="/next?a=1"), http(200, b"ok"))
        result = fetch("https://example.com/start", resolve=resolver(), connect=connect)
        self.assertEqual(result.final_url, "https://example.com/next?a=1")
        self.assertEqual(len(calls), 2)

    def test_redirect_re_resolves_every_hop(self):
        resolve = resolver()
        connect, _ = connector(
            http(302, Location="https://other.example/"), http(200, b"ok")
        )
        fetch("https://example.com/", resolve=resolve, connect=connect)
        self.assertEqual(resolve.seen, ["example.com", "other.example"])

    def test_more_than_five_redirects(self):
        connect, _ = connector(*[http(302, Location="/again")] * 6)
        refused(
            self,
            "https://example.com/",
            "redirects",
            resolve=resolver(),
            connect=connect,
        )

    def test_five_redirects_are_allowed(self):
        connect, _ = connector(*[http(302, Location="/again")] * 5, http(200, b"ok"))
        self.assertEqual(
            fetch("https://example.com/", resolve=resolver(), connect=connect).status,
            200,
        )

    def test_redirect_without_location_is_permanent(self):
        connect, _ = connector(http(302))
        refused(
            self, "https://example.com/", "status", resolve=resolver(), connect=connect
        )

    def test_redirect_to_userinfo_url_is_refused(self):
        connect, _ = connector(http(302, Location="https://u:p@example.com/"))
        refused(
            self, "https://example.com/", "url", resolve=resolver(), connect=connect
        )


class UrlEncodingTests(unittest.TestCase):
    def test_korean_path_is_fetched_percent_encoded(self):
        connect, calls = connector(http(200, b"ok"))
        result = fetch(
            "https://ko.wikipedia.org/wiki/한국?q=한#frag",
            resolve=resolver(),
            connect=connect,
        )
        want = "/wiki/%ED%95%9C%EA%B5%AD?q=%ED%95%9C"
        self.assertTrue(calls[0][-1].sent.startswith(f"GET {want} HTTP/1.1".encode()))
        self.assertEqual(result.final_url, f"https://ko.wikipedia.org{want}")

    def test_existing_escapes_are_kept(self):
        connect, _ = connector(http(200, b"ok"))
        result = fetch(
            "https://example.com/a%20b/c%2Fd", resolve=resolver(), connect=connect
        )
        self.assertEqual(result.final_url, "https://example.com/a%20b/c%2Fd")

    def test_idna_host_is_encoded(self):
        resolve = resolver()
        connect, calls = connector(http(200, b"ok"))
        result = fetch("https://bücher.example/", resolve=resolve, connect=connect)
        self.assertEqual(result.final_url, "https://xn--bcher-kva.example/")
        self.assertEqual(calls[0][2], "xn--bcher-kva.example")

    def test_redirect_location_with_raw_utf8_is_decoded(self):
        raw = http(302).replace(
            b"\r\n\r\n", b"\r\nLocation: /wiki/" + "한".encode() + b"\r\n\r\n", 1
        )
        connect, _ = connector(raw, http(200, b"ok"))
        result = fetch("https://example.com/", resolve=resolver(), connect=connect)
        self.assertEqual(result.final_url, "https://example.com/wiki/%ED%95%9C")

    def test_undecodable_redirect_location_is_permanent(self):
        raw = http(302).replace(b"\r\n\r\n", b"\r\nLocation: /\xff\xfe\r\n\r\n", 1)
        connect, _ = connector(raw)
        refused(
            self, "https://example.com/", "url", resolve=resolver(), connect=connect
        )

    def test_overlong_label_and_format_chars_are_permanent(self):
        for url in (
            "https://" + "a" * 64 + ".com/",
            "https://exa\u00admple.com/",
            "https://example.com/a\u200bb",
            "https://example.com/a\u0085b",
        ):
            with self.subTest(url=url[:30]):
                refused(self, url, "url", resolve=resolver())

    def test_encoded_form_over_2048_is_rejected(self):
        refused(self, "https://example.com/" + "한" * 300, "url", resolve=resolver())


class DeadlineTests(unittest.TestCase):
    def test_slow_drip_body_hits_total_deadline(self):
        clock = {"t": 0.0}

        class Slow(io.BytesIO):
            def read(self, n=-1):
                clock["t"] += 10
                return super().read(n)

        class SlowSock(FakeSock):
            def makefile(self, *args, **kwargs):
                return Slow(self.response)

        def connect(ip, port, name, timeout):
            return SlowSock(http(200, b"a" * 200_000))

        refused(
            self,
            "https://example.com/",
            "timeout",
            True,
            resolve=resolver(),
            connect=connect,
            monotonic=lambda: clock["t"],
        )

    def test_deadline_spans_hops_and_connect_gets_remaining_time(self):
        clock = {"t": 0.0}
        seen = []

        def connect(ip, port, name, timeout):
            seen.append(timeout)
            clock["t"] += 15
            return FakeSock(http(302, Location="/next"))

        refused(
            self,
            "https://example.com/",
            "timeout",
            True,
            resolve=resolver(),
            connect=connect,
            monotonic=lambda: clock["t"],
        )
        self.assertEqual(seen, [20.0, 5.0])


class OutcomeTests(unittest.TestCase):
    def test_body_over_2_mib(self):
        connect, _ = connector(http(200, b"a" * (2 * 1024 * 1024 + 1)))
        refused(
            self, "https://example.com/", "size", resolve=resolver(), connect=connect
        )

    def test_body_at_2_mib_is_accepted(self):
        connect, _ = connector(http(200, b"a" * (2 * 1024 * 1024)))
        result = fetch("https://example.com/", resolve=resolver(), connect=connect)
        self.assertEqual(len(result.body), 2 * 1024 * 1024)

    def test_unbounded_body_without_content_length_is_capped(self):
        raw = b"HTTP/1.1 200 OK\r\nConnection: close\r\n\r\n" + b"a" * (
            2 * 1024 * 1024 + 10
        )
        connect, _ = connector(raw)
        refused(
            self, "https://example.com/", "size", resolve=resolver(), connect=connect
        )

    def test_transient_failures(self):
        cases = [
            ("timeout", TimeoutError("t")),
            ("connect", ConnectionRefusedError()),
            ("status", http(503)),
            ("status", http(500)),
            ("status", http(429)),
        ]
        for reason, item in cases:
            connect, _ = connector(item)
            with self.subTest(reason=reason):
                refused(
                    self,
                    "https://example.com/",
                    reason,
                    True,
                    resolve=resolver(),
                    connect=connect,
                )

    def test_dns_failure_is_transient(self):
        def resolve(*a, **k):
            raise socket.gaierror(-2, "nope")

        refused(self, "https://example.com/", "dns", True, resolve=resolve)

    def test_permanent_failures(self):
        for item, reason in (
            (http(404), "status"),
            (http(403), "status"),
            (ssl.SSLCertVerificationError("bad"), "tls"),
        ):
            connect, _ = connector(item)
            with self.subTest(reason=reason):
                refused(
                    self,
                    "https://example.com/",
                    reason,
                    False,
                    resolve=resolver(),
                    connect=connect,
                )

    def test_success_records_final_url_sha_and_utc_millis(self):
        body = b"<html>hello</html>"
        connect, _ = connector(http(200, body, Content_Type="text/html; charset=utf-8"))
        moment = datetime(2026, 5, 6, 7, 8, 9, 123999, tzinfo=UTC)
        result = fetch(
            "https://example.com/a",
            resolve=resolver(),
            connect=connect,
            now=lambda: moment,
        )
        self.assertEqual(result.fetched_at, "2026-05-06T07:08:09.123Z")
        self.assertEqual(result.sha256, hashlib.sha256(body).hexdigest())
        self.assertEqual(
            (result.final_url, result.status, result.body),
            ("https://example.com/a", 200, body),
        )
        self.assertEqual(result.content_type, "text/html; charset=utf-8")

    def test_default_clock_is_utc_millis(self):
        connect, _ = connector(http(200, b"x"))
        result = fetch("https://example.com/", resolve=resolver(), connect=connect)
        self.assertRegex(result.fetched_at, r"^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\.\d{3}Z$")

    def test_fetch_signature_has_no_relaxing_parameter(self):
        names = set(
            source_fetch.fetch.__code__.co_varnames[
                : source_fetch.fetch.__code__.co_argcount
                + source_fetch.fetch.__code__.co_kwonlyargcount
            ]
        )
        self.assertEqual(names, {"url", "resolve", "connect", "now", "monotonic"})


if __name__ == "__main__":
    unittest.main()
