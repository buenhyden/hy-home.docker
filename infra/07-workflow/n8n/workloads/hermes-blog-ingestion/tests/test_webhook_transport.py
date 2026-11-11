"""Hermes' fixed webhook transport is bounded and policy pinned."""

from __future__ import annotations

import importlib
import io
import json
import os
import signal
import socket
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
from unittest import mock

PLUGIN_DIR = Path(__file__).resolve().parents[1] / "hermes-plugin"
sys.path.insert(0, str(PLUGIN_DIR))
transport = importlib.import_module("webhook_transport")


APPROVED = "https://n8n.hy.home.arpa/webhook/hermes-blog-ingestion"


def answer(address: str):
    family = socket.AF_INET6 if ":" in address else socket.AF_INET
    return (family, socket.SOCK_STREAM, socket.IPPROTO_TCP, "", (address, 443))


class AuthorityAndPolicyTests(unittest.TestCase):
    def test_exact_endpoint_is_the_only_authority(self):
        endpoint = transport.validate_endpoint(APPROVED)
        self.assertEqual(
            (endpoint.hostname, endpoint.port, endpoint.target),
            ("n8n.hy.home.arpa", 443, "/webhook/hermes-blog-ingestion"),
        )
        for bad in (
            APPROVED + "/",
            APPROVED + "?next=1",
            APPROVED + "#fragment",
            APPROVED.replace("https", "http", 1),
            APPROVED.replace("n8n.", "user@n8n.", 1),
            APPROVED.replace("n8n.hy.home.arpa", "n8n.hy.home.arpa:443"),
            APPROVED.replace("n8n.hy.home.arpa", "other.example"),
            APPROVED.replace("hermes-blog-ingestion", "other"),
            APPROVED.replace("/webhook", "\\webhook"),
            APPROVED + "\nX-Test: yes",
        ):
            with (
                self.subTest(url=repr(bad)),
                self.assertRaises(transport.TransportFailure),
            ):
                transport.validate_endpoint(bad)

    def test_policy_is_required_and_bounded(self):
        for value in ("", "  ", "not-an-address", "0.0.0.0/0", "::/0"):
            with (
                self.subTest(value=value),
                self.assertRaises(transport.TransportFailure),
            ):
                transport.parse_address_policy(value)
        policy = transport.parse_address_policy("10.250.1.128/32, 10.250.1.0/24")
        self.assertEqual(len(policy), 2)
        with self.assertRaises(transport.TransportFailure):
            transport.parse_address_policy(",".join(["10.0.0.1"] * 33))
        with self.assertRaises(transport.TransportFailure):
            transport.parse_address_policy("1" * (transport.MAX_POLICY_LENGTH + 1))

    def test_all_dns_answers_must_be_approved(self):
        endpoint = transport.validate_endpoint(APPROVED)
        policy = transport.parse_address_policy("10.250.1.0/24")
        for addresses in (
            ["10.250.1.128", "192.0.2.4"],
            ["169.254.169.254"],
            ["127.0.0.1"],
            ["0.0.0.0"],
        ):
            with (
                self.subTest(addresses=addresses),
                self.assertRaises(transport.TransportFailure),
            ):
                transport.resolve_pinned(
                    endpoint,
                    policy,
                    resolver=lambda *_args, values=addresses, **_kwargs: [
                        answer(value) for value in values
                    ],
                )

    def test_private_internal_answer_is_allowed_only_by_policy(self):
        endpoint = transport.validate_endpoint(APPROVED)
        resolved = transport.resolve_pinned(
            endpoint,
            transport.parse_address_policy("10.250.1.128/32"),
            resolver=lambda *_a, **_k: [answer("10.250.1.128")],
        )
        self.assertEqual(resolved, "10.250.1.128")

    def test_dns_errors_empty_and_malformed_answers_fail_closed(self):
        endpoint = transport.validate_endpoint(APPROVED)
        policy = transport.parse_address_policy("10.250.1.128/32")

        def failed(*_args, **_kwargs):
            raise OSError

        for resolver in (failed, lambda *_a, **_k: [], lambda *_a, **_k: [(1,)]):
            with (
                self.subTest(resolver=resolver),
                self.assertRaises(transport.TransportFailure),
            ):
                transport.resolve_pinned(endpoint, policy, resolver=resolver)

    def test_each_attempt_resolves_again_and_rebinding_is_rejected(self):
        endpoint = transport.validate_endpoint(APPROVED)
        policy = transport.parse_address_policy("10.250.1.128/32")
        answers = iter(([answer("10.250.1.128")], [answer("192.0.2.9")]))

        def resolver(*_args, **_kwargs):
            return next(answers)

        self.assertEqual(
            transport.resolve_pinned(endpoint, policy, resolver=resolver),
            "10.250.1.128",
        )
        with self.assertRaises(transport.TransportFailure):
            transport.resolve_pinned(endpoint, policy, resolver=resolver)


class BoundariesTests(unittest.TestCase):
    def test_parent_death_guard_is_linux_only_and_fails_closed(self):
        for value in (None, True, 0, 1):
            with (
                self.subTest(value=value),
                self.assertRaises(transport.TransportFailure) as error,
            ):
                transport._arm_parent_death(value)
            self.assertEqual(error.exception.reason, "parent_guard_unavailable")
        with (
            mock.patch.object(transport.sys, "platform", "other"),
            self.assertRaises(transport.TransportFailure) as error,
        ):
            transport._arm_parent_death(123)
        self.assertEqual(error.exception.reason, "parent_guard_unavailable")

    def test_parent_death_guard_arms_kernel_and_rejects_parent_race(self):
        prctl = mock.Mock(return_value=0)
        library = mock.Mock(prctl=prctl)
        with (
            mock.patch.object(transport.ctypes, "CDLL", return_value=library),
            mock.patch.object(transport.os, "getppid", return_value=123),
        ):
            transport._arm_parent_death(123)
        prctl.assert_called_once_with(1, signal.SIGKILL, 0, 0, 0)

        prctl.return_value = 1
        with (
            mock.patch.object(transport.ctypes, "CDLL", return_value=library),
            self.assertRaises(transport.TransportFailure) as error,
        ):
            transport._arm_parent_death(123)
        self.assertEqual(error.exception.reason, "parent_guard_unavailable")

        prctl.return_value = 0
        with (
            mock.patch.object(transport.ctypes, "CDLL", return_value=library),
            mock.patch.object(transport.os, "getppid", return_value=999),
            mock.patch.object(transport.os, "getpid", return_value=456),
            mock.patch.object(transport.os, "kill") as kill,
            mock.patch.object(transport.os, "_exit", side_effect=SystemExit(2)),
            self.assertRaises(SystemExit),
        ):
            transport._arm_parent_death(123)
        kill.assert_called_once_with(456, signal.SIGKILL)

    def test_sigterm_handler_reaps_then_preserves_default_termination(self):
        process = mock.Mock()
        installed = {}

        def install(signum, handler):
            installed[signum] = handler

        with (
            mock.patch.object(
                transport.signal, "getsignal", return_value=signal.SIG_DFL
            ),
            mock.patch.object(transport.signal, "signal", side_effect=install),
            mock.patch.object(transport, "_kill_owned_process") as reap,
            mock.patch.object(transport.os, "getpid", return_value=789),
            mock.patch.object(transport.os, "kill") as terminate,
        ):
            previous = transport._install_termination_handlers(process)
            handler = installed[signal.SIGTERM]
            handler(signal.SIGTERM, None)
        self.assertEqual(previous, {signal.SIGTERM: signal.SIG_DFL})
        reap.assert_called_once_with(process)
        terminate.assert_called_once_with(789, signal.SIGTERM)

    def test_request_limit_is_checked_before_dns(self):
        resolver = mock.Mock()
        with self.assertRaises(transport.TransportFailure) as error:
            transport.send_once(
                APPROVED,
                b"x" * (transport.MAX_REQUEST_BYTES + 1),
                "synthetic",
                "10.250.1.128/32",
                timeout=1,
                resolver=resolver,
            )
        self.assertEqual(error.exception.reason, "request_too_large")
        resolver.assert_not_called()

    def test_child_has_empty_environment_and_no_secret_or_body_in_argv(self):
        process = mock.Mock(pid=999)
        process.communicate.return_value = (
            json.dumps(
                {
                    "ok": True,
                    "status": 201,
                    "body": "e30=",
                    "content_type": "application/json",
                }
            ).encode(),
            b"",
        )
        process.returncode = 0
        with mock.patch.object(
            transport.subprocess, "Popen", return_value=process
        ) as popen:
            result = transport.post(
                APPROVED,
                b"private body",
                "synthetic-secret",
                "10.250.1.128/32",
                timeout=1,
            )
        self.assertEqual((result.status, result.body), (201, b"{}"))
        call = popen.call_args
        self.assertEqual(call.kwargs["env"], {})
        self.assertNotIn("synthetic-secret", repr(call.args[0]))
        self.assertNotIn("private body", repr(call.args[0]))
        sent = process.communicate.call_args.kwargs["input"]
        self.assertIn(b"synthetic-secret", sent)

    def test_timeout_and_interrupt_kill_only_the_owned_child_group(self):
        for failure in (
            subprocess.TimeoutExpired(["child"], 0.01),
            KeyboardInterrupt(),
            SystemExit(23),
        ):
            process = mock.Mock(pid=4242)
            process.communicate.side_effect = [failure, (b"", b"")]
            process.wait.return_value = 0
            with (
                self.subTest(failure=type(failure).__name__),
                mock.patch.object(transport.subprocess, "Popen", return_value=process),
                mock.patch.object(transport.os, "killpg") as killpg,
            ):
                with self.assertRaises(
                    (transport.TransportFailure, KeyboardInterrupt, SystemExit)
                ):
                    transport.post(
                        APPROVED,
                        b"{}",
                        "synthetic",
                        "10.250.1.128/32",
                        timeout=0.01,
                    )
                killpg.assert_called_once_with(4242, transport.signal.SIGKILL)
                process.wait.assert_called()

    def test_real_sigterm_reaps_child_before_any_side_effect(self):
        with tempfile.TemporaryDirectory(dir="/tmp") as tmp:
            child_pid_path = Path(tmp) / "child.pid"
            side_effect_path = Path(tmp) / "side-effect"
            plugin_dir = str(PLUGIN_DIR)
            child_code = (
                "import os,pathlib,sys,time;"
                f"sys.path.insert(0,{plugin_dir!r});"
                "import webhook_transport as transport;"
                "transport._arm_parent_death(int(sys.argv[1]));"
                "pathlib.Path(sys.argv[2]).write_text(str(os.getpid()));"
                "time.sleep(2);"
                "pathlib.Path(sys.argv[3]).write_text('unexpected')"
            )
            parent_code = (
                "import os,sys;"
                f"sys.path.insert(0,{plugin_dir!r});"
                "import webhook_transport as transport;"
                f"command=[sys.executable,'-I','-c',{child_code!r},"
                f"str(os.getpid()),{str(child_pid_path)!r},{str(side_effect_path)!r}];"
                "transport._child_command=lambda *_args: command;"
                "transport.post(transport.APPROVED_WEBHOOK_URL,b'{}','synthetic',"
                "'10.250.1.128/32',timeout=10)"
            )
            parent = subprocess.Popen(
                [sys.executable, "-I", "-c", parent_code],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                env={},
                cwd="/",
                close_fds=True,
            )
            try:
                deadline = time.monotonic() + 5
                while (
                    not child_pid_path.exists()
                    and parent.poll() is None
                    and time.monotonic() < deadline
                ):
                    time.sleep(0.01)
                self.assertTrue(child_pid_path.exists(), "child did not become ready")
                child_pid = int(child_pid_path.read_text())
                os.kill(parent.pid, signal.SIGTERM)
                self.assertEqual(parent.wait(timeout=5), -signal.SIGTERM)

                deadline = time.monotonic() + 5
                while time.monotonic() < deadline:
                    try:
                        os.kill(child_pid, 0)
                    except ProcessLookupError:
                        break
                    time.sleep(0.01)
                else:
                    self.fail("owned child PID was not reaped after parent SIGTERM")
                time.sleep(2.1)
                self.assertFalse(side_effect_path.exists())
            finally:
                if parent.poll() is None:
                    parent.kill()
                    parent.wait(timeout=5)

    def test_real_timeout_reaps_the_owned_child(self):
        with tempfile.TemporaryDirectory(dir="/tmp") as tmp:
            marker = Path(tmp) / "pid"
            command = [
                sys.executable,
                "-c",
                (
                    "import os,pathlib,time;"
                    f"pathlib.Path({str(marker)!r}).write_text(str(os.getpid()));"
                    "time.sleep(5)"
                ),
            ]
            with mock.patch.object(transport, "_child_command", return_value=command):
                with self.assertRaises(transport.TransportFailure) as error:
                    transport.post(
                        APPROVED,
                        b"{}",
                        "synthetic",
                        "10.250.1.128/32",
                        timeout=0.2,
                    )
            self.assertEqual(error.exception.reason, "timeout")
            pid = int(marker.read_text())
            with self.assertRaises(ProcessLookupError):
                os.kill(pid, 0)

    def test_malformed_child_output_is_value_free(self):
        process = mock.Mock(pid=999, returncode=0)
        process.communicate.return_value = (b"synthetic-secret", b"private body")
        with mock.patch.object(transport.subprocess, "Popen", return_value=process):
            with self.assertRaises(transport.TransportFailure) as error:
                transport.post(
                    APPROVED,
                    b"private body",
                    "synthetic-secret",
                    "10.250.1.128/32",
                    timeout=1,
                )
        self.assertNotIn("synthetic-secret", str(error.exception))
        self.assertNotIn("private body", str(error.exception))

    def test_non_object_child_output_is_rejected_as_protocol_failure(self):
        process = mock.Mock(pid=999, returncode=0)
        process.communicate.return_value = (b"[]", b"")
        with mock.patch.object(transport.subprocess, "Popen", return_value=process):
            with self.assertRaises(transport.TransportFailure) as error:
                transport.post(
                    APPROVED,
                    b"{}",
                    "synthetic",
                    "10.250.1.128/32",
                    timeout=1,
                )
        self.assertEqual(error.exception.reason, "transport_protocol")

    def test_child_failure_reason_is_closed_and_retryability_is_preserved(self):
        for result, reason, retryable in (
            ({"ok": False, "reason": "dns", "retryable": True}, "dns", True),
            (
                {"ok": False, "reason": "private-detail", "retryable": True},
                "transport_failure",
                True,
            ),
        ):
            process = mock.Mock(pid=999, returncode=2)
            process.communicate.return_value = (json.dumps(result).encode(), b"")
            with mock.patch.object(transport.subprocess, "Popen", return_value=process):
                with self.assertRaises(transport.TransportFailure) as error:
                    transport.post(
                        APPROVED,
                        b"{}",
                        "synthetic",
                        "10.250.1.128/32",
                        timeout=1,
                    )
            self.assertEqual(error.exception.reason, reason)
            self.assertEqual(error.exception.retryable, retryable)

    def test_invalid_inputs_do_not_spawn_a_child(self):
        with mock.patch.object(transport.subprocess, "Popen") as popen:
            for body, token, policy, timeout in (
                (b"x" * (transport.MAX_REQUEST_BYTES + 1), "x", "10.0.0.1", 1),
                (b"{}", "", "10.0.0.1", 1),
                (b"{}", "x\r\ny", "10.0.0.1", 1),
                (b"{}", "x", "", 1),
                (b"{}", "x", "10.0.0.1", 0),
                (b"{}", "x", "10.0.0.1", 46),
            ):
                with (
                    self.subTest(token=repr(token), timeout=timeout),
                    self.assertRaises(transport.TransportFailure),
                ):
                    transport.post(
                        APPROVED,
                        body,
                        token,
                        policy,
                        timeout=timeout,
                    )
            popen.assert_not_called()


class ChildProtocolTests(unittest.TestCase):
    def invoke(self, request, *, result=None, failure=None):
        stdin = mock.Mock(buffer=io.BytesIO(json.dumps(request).encode()))
        stdout = io.StringIO()
        patcher = (
            mock.patch.object(transport, "send_once", side_effect=failure)
            if failure is not None
            else mock.patch.object(transport, "send_once", return_value=result)
        )
        with (
            mock.patch.object(transport.sys, "stdin", stdin),
            mock.patch.object(transport.sys, "stdout", stdout),
            patcher,
        ):
            status = transport._child_main()
        return status, json.loads(stdout.getvalue())

    def request(self):
        return {
            "url": APPROVED,
            "body": "e30=",
            "token": "synthetic",
            "policy": "10.250.1.128/32",
            "timeout": 1,
        }

    def test_child_success_emits_only_bounded_protocol_fields(self):
        status, result = self.invoke(
            self.request(),
            result=transport.Response(201, b"{}", "application/json"),
        )
        self.assertEqual(status, 0)
        self.assertEqual(
            result,
            {
                "ok": True,
                "status": 201,
                "body": "e30=",
                "content_type": "application/json",
            },
        )

    def test_child_failure_and_malformed_input_are_value_free(self):
        status, result = self.invoke(
            self.request(),
            failure=transport.TransportFailure("tls"),
        )
        self.assertEqual((status, result["reason"]), (2, "tls"))
        status, result = self.invoke({"body": "not-base64"}, result=None)
        self.assertEqual((status, result["reason"]), (2, "transport_protocol"))


class TlsFixtureTests(unittest.TestCase):
    class Handler(BaseHTTPRequestHandler):
        records: ClassVar[list[tuple[str, bytes, str | None]]] = []
        response_status = 302
        response_body = b"opaque"
        declared_length: int | None = None

        def log_message(self, *_args):
            pass

        def do_POST(self):
            body = self.rfile.read(int(self.headers["Content-Length"]))
            self.records.append(
                (self.path, body, self.headers.get("X-Hermes-Ingest-Token"))
            )
            self.send_response(self.response_status)
            self.send_header(
                "Content-Length",
                str(self.declared_length or len(self.response_body)),
            )
            self.send_header("Location", "https://other.example/steal")
            self.end_headers()
            self.wfile.write(self.response_body)

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory(dir="/tmp")
        cls.cert = str(Path(cls.tmp.name) / "cert.pem")
        cls.key = str(Path(cls.tmp.name) / "key.pem")
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
                    cls.key,
                    "-out",
                    cls.cert,
                    "-days",
                    "1",
                    "-subj",
                    "/CN=n8n.hy.home.arpa",
                    "-addext",
                    "subjectAltName=DNS:n8n.hy.home.arpa",
                ],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except FileNotFoundError:
            cls.tmp.cleanup()
            raise unittest.SkipTest("openssl unavailable") from None
        try:
            cls.server = ThreadingHTTPServer(("127.0.0.1", 0), cls.Handler)
        except PermissionError:
            cls.tmp.cleanup()
            raise unittest.SkipTest("loopback socket creation denied") from None
        server_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        server_context.minimum_version = ssl.TLSVersion.TLSv1_2
        server_context.load_cert_chain(cls.cert, cls.key)
        cls.server.socket = server_context.wrap_socket(
            cls.server.socket, server_side=True
        )
        cls.server.daemon_threads = True
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()
        cls.tmp.cleanup()

    def setUp(self):
        self.Handler.records.clear()
        self.Handler.response_status = 302
        self.Handler.response_body = b"opaque"
        self.Handler.declared_length = None
        self.context = ssl.create_default_context(cafile=self.cert)

    def connector(self, _ip, _port, hostname, timeout, context):
        raw = socket.create_connection(("127.0.0.1", self.server.server_port), timeout)
        return context.wrap_socket(raw, server_hostname=hostname)

    def test_exact_post_tls_hostname_and_redirect_is_not_followed(self):
        response = transport.send_once(
            APPROVED,
            b"private body",
            "synthetic",
            "10.250.1.128/32",
            timeout=2,
            resolver=lambda *_a, **_k: [answer("10.250.1.128")],
            connector=self.connector,
            context=self.context,
        )
        self.assertEqual((response.status, response.body), (302, b"opaque"))
        self.assertEqual(
            self.Handler.records,
            [("/webhook/hermes-blog-ingestion", b"private body", "synthetic")],
        )

    def test_hostname_verification_failure_sends_no_request(self):
        with self.assertRaises(transport.TransportFailure) as error:
            transport.send_once(
                APPROVED,
                b"private body",
                "synthetic",
                "10.250.1.128/32",
                timeout=2,
                resolver=lambda *_a, **_k: [answer("10.250.1.128")],
                connector=self.connector,
                context=ssl.create_default_context(),
            )
        self.assertEqual(error.exception.reason, "tls")
        self.assertEqual(self.Handler.records, [])

    def test_oversize_response_is_rejected(self):
        self.Handler.declared_length = transport.MAX_RESPONSE_BYTES + 1
        with self.assertRaises(transport.TransportFailure) as error:
            transport.send_once(
                APPROVED,
                b"{}",
                "synthetic",
                "10.250.1.128/32",
                timeout=2,
                resolver=lambda *_a, **_k: [answer("10.250.1.128")],
                connector=self.connector,
                context=self.context,
            )
        self.assertEqual(error.exception.reason, "response_too_large")


if __name__ == "__main__":
    unittest.main()
