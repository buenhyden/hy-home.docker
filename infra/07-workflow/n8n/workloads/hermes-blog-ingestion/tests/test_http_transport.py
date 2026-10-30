"""Offline HTTP transport tests; no Gateway compatibility is implied."""

import ssl
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import ClassVar
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from publisher.delivery import DispatchRequest, FailureKind, TransportFailure

REQUEST = DispatchRequest(
    ("job", "run"), "a" * 64, "b" * 64, "test", "local", b"private payload"
)


class HttpTransportTests(unittest.TestCase):
    def transport(self, **kwargs):
        from publisher.http_transport import HttpTransport

        options = dict(
            endpoint="https://example.test/ingest",
            destination="local",
            auth=("X-Test-Auth", "fake-token"),
            timeout=0.3,
        )
        options.update(kwargs)
        return HttpTransport(**options)

    def test_invalid_auth_destination_and_body_never_start_process(self):
        with patch("publisher.http_transport.subprocess.run") as run:
            for options in (
                {"destination": "other"},
                {"auth": ("X-Test", "bad\r\nheader")},
                {"auth": None},
                {"max_bytes": 3},
            ):
                with (
                    self.subTest(options=repr(options)),
                    self.assertRaises(TransportFailure),
                ):
                    self.transport(**options).send(REQUEST)
            run.assert_not_called()

    def test_invalid_configuration(self):
        for options in (
            {"timeout": 0},
            {"timeout": float("inf")},
            {"max_bytes": 1048577},
            {"endpoint": "http://localhost/"},
            {"endpoint": "https://user:pass@example.com/"},
            {"endpoint": "https://example.com/?token=x"},
            {"endpoint": "https://example.com/#frag"},
        ):
            with self.subTest(options=options), self.assertRaises(ValueError):
                self.transport(**options)

    def test_total_deadline_terminates_slow_process(self):
        with patch("publisher.http_transport._CHILD", "import time; time.sleep(5)"):
            start = time.monotonic()
            with self.assertRaises(TransportFailure) as error:
                self.transport().send(REQUEST)
        self.assertEqual(error.exception.kind, FailureKind.AMBIGUOUS)
        self.assertLess(time.monotonic() - start, 2)

    def test_deadline_covers_dns_headers_and_response_body(self):
        from publisher.http_transport import _CHILD

        prefix = """
import http.client, time
class Response:
    status = 200
    length = None
    def read(self, n):
        if STAGE == 'body': time.sleep(5)
        return b'body'
    def getheader(self, name): return None
class Connection:
    def __init__(self, *args, **kwargs): pass
    def connect(self):
        if STAGE == 'dns': time.sleep(5)
    def request(self, *args, **kwargs): pass
    def getresponse(self):
        if STAGE == 'headers': time.sleep(5)
        return Response()
    def close(self): pass
http.client.HTTPSConnection = Connection
"""
        for stage in ("dns", "headers", "body"):
            with (
                self.subTest(stage=stage),
                patch(
                    "publisher.http_transport._CHILD",
                    "STAGE = " + repr(stage) + "\n" + prefix + _CHILD,
                ),
            ):
                start = time.monotonic()
                with self.assertRaises(TransportFailure) as error:
                    self.transport().send(REQUEST)
                self.assertEqual(error.exception.kind, FailureKind.AMBIGUOUS)
                self.assertLess(time.monotonic() - start, 2)

    def test_tls_failure_is_classified_before_http_request(self):
        from publisher.http_transport import _CHILD

        prefix = """
import http.client, ssl
class Connection:
    def __init__(self, *args, **kwargs): pass
    def connect(self): raise ssl.SSLCertVerificationError('fake-token')
    def request(self, *args, **kwargs): raise AssertionError()
    def close(self): pass
http.client.HTTPSConnection = Connection
"""
        with patch("publisher.http_transport._CHILD", prefix + _CHILD):
            with self.assertRaises(TransportFailure) as error:
                self.transport().send(REQUEST)
        self.assertEqual(error.exception.kind, FailureKind.TLS)
        self.assertNotIn("fake-token", str(error.exception))

    def test_connect_failure_is_not_sent_but_request_failure_is_ambiguous(self):
        from publisher.http_transport import _CHILD

        prefix = """
import http.client
class Connection:
    def __init__(self, *args, **kwargs): pass
    def connect(self):
        if STAGE == 'connect': raise OSError('private-token')
    def request(self, *args, **kwargs): raise OSError('private-token')
    def close(self): pass
http.client.HTTPSConnection = Connection
"""
        for stage, kind in (
            ("connect", FailureKind.NOT_SENT),
            ("request", FailureKind.AMBIGUOUS),
        ):
            with (
                self.subTest(stage=stage),
                patch(
                    "publisher.http_transport._CHILD",
                    "STAGE = " + repr(stage) + "\n" + prefix + _CHILD,
                ),
            ):
                with self.assertRaises(TransportFailure) as error:
                    self.transport().send(REQUEST)
                self.assertEqual(error.exception.kind, kind)
                self.assertNotIn("private-token", str(error.exception))

    def test_proven_connect_failure_schedules_retry_in_outbox(self):
        from publisher.candidates import Snapshot
        from publisher.delivery import BoundRequest, process_one
        from publisher.http_transport import _CHILD
        from publisher.outbox import Outbox

        class Adapter:
            idempotent_writes = False

            def prepare(self, snapshot):
                return BoundRequest("test", "local", b"payload")

        prefix = """
import http.client
class Connection:
    def __init__(self, *args, **kwargs): pass
    def connect(self): raise ConnectionRefusedError()
    def close(self): pass
http.client.HTTPSConnection = Connection
"""
        key = ("6eabd835f969", "a" * 32)
        with tempfile.TemporaryDirectory(dir="/tmp") as tmp:
            box = Outbox(Path(tmp) / "private" / "box.sqlite")
            try:
                box.stage(Snapshot(*key, b"candidate", "source", b"report"))
                with patch("publisher.http_transport._CHILD", prefix + _CHILD):
                    result = process_one(
                        box, key, Adapter(), self.transport(), now=100, base_delay=10
                    )
                self.assertEqual(result, "pending")
                self.assertEqual(box.get(key)["next_attempt"], 110)
                self.assertEqual(box.get(key)["attempts"], 1)
            finally:
                box.close()

    def test_opaque_http_response_and_no_secrets_in_command(self):
        fake = subprocess.CompletedProcess(
            [], 0, b'{"status":403,"body":"eHg=","content_type":"text/plain"}', b""
        )
        with patch("publisher.http_transport.subprocess.run", return_value=fake) as run:
            response = self.transport().send(REQUEST)
        self.assertEqual((response.status, response.body), (403, b"xx"))
        self.assertNotIn("fake-token", repr(run.call_args.args))
        self.assertNotIn("private payload", repr(run.call_args.args))
        self.assertNotIn("fake-token", repr(response))

    def test_unexpected_child_failure_and_reconcile_ambiguous(self):
        fake = subprocess.CompletedProcess(
            [], 1, b"private payload fake-token", b"fake-token"
        )
        with patch("publisher.http_transport.subprocess.run", return_value=fake):
            with self.assertRaises(TransportFailure) as error:
                self.transport().send(REQUEST)
        self.assertEqual(error.exception.kind, FailureKind.AMBIGUOUS)
        self.assertNotIn("fake-token", str(error.exception))
        with patch("publisher.http_transport.subprocess.run") as run:
            with self.assertRaises(TransportFailure) as error:
                self.transport().reconcile(REQUEST)
            self.assertEqual(error.exception.kind, FailureKind.AMBIGUOUS)
            run.assert_not_called()


class LoopbackTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        class Handler(BaseHTTPRequestHandler):
            records: ClassVar[list] = []

            def log_message(self, *args):
                pass

            def do_POST(self):
                body = self.rfile.read(int(self.headers["Content-Length"]))
                self.records.append((self.path, body, self.headers.get("X-Test")))
                self.send_response(302)
                self.send_header("Location", "/other")
                self.end_headers()
                self.wfile.write(b"opaque")

        cls.handler = Handler
        try:
            cls.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        except PermissionError:
            raise unittest.SkipTest("loopback socket creation denied") from None
        cls.server.daemon_threads = True
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def test_exact_post_and_redirect_never_followed(self):
        from publisher.http_transport import HttpTransport

        self.handler.records.clear()
        endpoint = f"http://127.0.0.1:{self.server.server_port}/ingest"
        transport = HttpTransport(
            endpoint=endpoint,
            destination="local",
            auth=("X-Test", "fake-token"),
            allow_loopback_http=True,
        )
        response = transport.send(REQUEST)
        self.assertEqual((response.status, response.body), (302, b"opaque"))
        self.assertEqual(
            self.handler.records, [("/ingest", REQUEST.body, "fake-token")]
        )

    def test_untrusted_tls_does_not_send_auth(self):
        from publisher.http_transport import HttpTransport

        with tempfile.TemporaryDirectory(dir="/tmp") as tmp:
            cert, key = str(Path(tmp) / "cert.pem"), str(Path(tmp) / "key.pem")
            try:
                subprocess.run(
                    [
                        "openssl",
                        "req",
                        "-x509",
                        "-newkey",
                        "rsa:2048",
                        "-nodes",
                        "-keyout",
                        key,
                        "-out",
                        cert,
                        "-days",
                        "1",
                        "-subj",
                        "/CN=127.0.0.1",
                    ],
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            except FileNotFoundError:
                self.skipTest("openssl unavailable")
            server = ThreadingHTTPServer(("127.0.0.1", 0), self.handler)
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            context.minimum_version = ssl.TLSVersion.TLSv1_2
            context.load_cert_chain(cert, key)
            server.socket = context.wrap_socket(server.socket, server_side=True)
            server.daemon_threads = True
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            self.handler.records.clear()
            try:
                endpoint = f"https://127.0.0.1:{server.server_port}/ingest"
                transport = HttpTransport(
                    endpoint=endpoint,
                    destination="local",
                    auth=("X-Test", "fake-token"),
                )
                with self.assertRaises(TransportFailure) as error:
                    transport.send(REQUEST)
                self.assertEqual(error.exception.kind, FailureKind.TLS)
                self.assertEqual(self.handler.records, [])
            finally:
                server.shutdown()
                server.server_close()
                thread.join()


if __name__ == "__main__":
    unittest.main()
