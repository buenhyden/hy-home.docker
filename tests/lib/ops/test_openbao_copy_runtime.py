"""Bounded real transport/file tests using generated loopback TLS and fake values."""

from __future__ import annotations

import contextlib
import hashlib
import http.server
import io
import json
import os
import socket
import ssl
import subprocess
import tempfile
import threading
import time
import unittest
from dataclasses import replace
from pathlib import Path
from unittest.mock import patch

from scripts.lib.ops import openbao_consumer_migration as migration
from tests.lib.ops.test_openbao_consumer_migration import row

MARKER = b"synthetic-private-marker\n"


def certificates(folder, *, hostname="localhost"):
    """Generate ephemeral synthetic certificate material; never inspect host keys."""
    subprocess.run(
        [
            "openssl",
            "req",
            "-x509",
            "-newkey",
            "rsa:2048",
            "-nodes",
            "-keyout",
            str(folder / "key.pem"),
            "-out",
            str(folder / "ca.pem"),
            "-days",
            "1",
            "-subj",
            "/CN=" + hostname,
            "-addext",
            "subjectAltName=DNS:" + hostname,
            "-addext",
            "basicConstraints=critical,CA:TRUE",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=True,
        timeout=10,
    )
    pem = (folder / "ca.pem").read_bytes()
    for name in ("ca.pem", "key.pem"):
        (folder / name).chmod(0o600)
    return hashlib.sha256(pem).hexdigest()


class Server:
    """One local HTTPS origin with declarative responses and bounded shutdown."""

    def __init__(self, folder):
        owner = self
        self.calls = []
        self.value = None
        self.version = 0
        self.mode = "normal"
        self.responses = {}
        self.wire = None

        class Handler(http.server.BaseHTTPRequestHandler):
            def log_message(self, *_):
                pass

            def do_GET(self):
                self.reply("GET")

            def do_POST(self):
                self.reply("POST")

            def reply(self, method):
                size = int(self.headers.get("Content-Length", "0"))
                raw = self.rfile.read(size) if size else b""
                owner.calls.append(
                    (method, self.path, raw, self.headers["X-Vault-Token"])
                )
                if owner.wire is not None:
                    self.connection.sendall(owner.wire)
                    return
                if owner.mode == "headers_slow":
                    self.connection.sendall(b"HTTP/1.1 200 OK\r\nX-Slow: ")
                    for _ in range(30):
                        time.sleep(0.03)
                        try:
                            self.connection.sendall(b"x")
                        except OSError:
                            break
                    return
                if (
                    owner.mode == "readback_forbidden"
                    and owner.version
                    and "/metadata/" in self.path
                ):
                    self.send_response(403)
                    self.send_header("Content-Type", "application/json")
                    self.send_header("Content-Length", "13")
                    self.end_headers()
                    self.wfile.write(b'{"errors":[]}')
                    return
                response = owner.responses.get((method, self.path))
                if response is not None:
                    status, body = response
                elif self.path.endswith("/config"):
                    status, body = (
                        200,
                        {
                            "data": {
                                "max_versions": 10,
                                "cas_required": True,
                                "delete_version_after": "0s",
                            }
                        },
                    )
                elif "/metadata/" in self.path:
                    status, body = (
                        (404, {"errors": []})
                        if not owner.version
                        else (
                            200,
                            {
                                "data": {
                                    "current_version": owner.version,
                                    "versions": {
                                        str(owner.version): {
                                            "deletion_time": "",
                                            "destroyed": False,
                                        }
                                    },
                                }
                            },
                        )
                    )
                elif method == "GET":
                    status, body = (
                        (404, {"errors": []})
                        if not owner.version
                        else (
                            200,
                            {
                                "data": {
                                    "data": {"value": owner.value},
                                    "metadata": {
                                        "version": owner.version,
                                        "deletion_time": "",
                                        "destroyed": False,
                                    },
                                }
                            },
                        )
                    )
                else:
                    payload = json.loads(raw)
                    if payload["options"]["cas"] != 0 or owner.version:
                        status, body = 400, {"errors": ["synthetic-private-marker"]}
                    elif owner.mode in {"race_equal", "race_different"}:
                        owner.value = (
                            payload["data"]["value"]
                            if owner.mode == "race_equal"
                            else "different"
                        )
                        owner.version = 2
                        status, body = 400, {"errors": ["synthetic-private-marker"]}
                    else:
                        owner.value = payload["data"]["value"]
                        owner.version = 1
                        if owner.mode == "lost_write":
                            self.connection.shutdown(socket.SHUT_RDWR)
                            return
                        status, body = (
                            200,
                            {
                                "data": {
                                    "version": 1,
                                    "deletion_time": "",
                                    "destroyed": False,
                                }
                            },
                        )
                encoded = body if isinstance(body, bytes) else json.dumps(body).encode()
                if owner.mode == "chunked":
                    self.connection.sendall(
                        b"HTTP/1.1 "
                        + str(status).encode()
                        + b" OK\r\nContent-Type: application/json\r\nTransfer-Encoding: chunked\r\n\r\n"
                    )
                    self.connection.sendall(
                        format(len(encoded), "x").encode()
                        + b"\r\n"
                        + encoded
                        + b"\r\n0\r\n\r\n"
                    )
                    return
                self.send_response(status)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(encoded)))
                if 300 <= status < 400:
                    self.send_header("Location", "https://unapproved.example/")
                self.end_headers()
                try:
                    if owner.mode == "body_slow":
                        for byte in encoded:
                            self.wfile.write(bytes([byte]))
                            self.wfile.flush()
                            time.sleep(0.03)
                    else:
                        self.wfile.write(encoded)
                except OSError:
                    pass

        self.server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.server.daemon_threads = True
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ctx.load_cert_chain(folder / "ca.pem", folder / "key.pem")
        self.server.socket = ctx.wrap_socket(self.server.socket, server_side=True)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.origin = f"https://localhost:{self.server.server_port}"

    def close(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)


class RuntimeCopyTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="p06-synthetic-")
        self.folder = Path(self.temporary.name)
        self.ca_hash = certificates(self.folder)
        (self.folder / "secrets/db/dev-pg").mkdir(parents=True)
        for name in ("secrets", "secrets/db", "secrets/db/dev-pg"):
            (self.folder / name).chmod(0o700)
        self.source = self.folder / row().source_path
        self.source.write_bytes(MARKER)
        self.source.chmod(0o600)
        for name in ("copy.token", "metadata.token"):
            (self.folder / name).write_bytes(("synthetic-" + name).encode())
            (self.folder / name).chmod(0o600)
        self.server = Server(self.folder)
        self.addCleanup(self.temporary.cleanup)
        self.addCleanup(self.server.close)

    def input(self, name):
        root_stat = self.folder.stat()
        info = (self.folder / name).stat()
        return migration.ProtectedInput(
            str(self.folder),
            root_stat.st_dev,
            root_stat.st_ino,
            root_stat.st_uid,
            root_stat.st_gid,
            0o700,
            name,
            info.st_uid,
            info.st_gid,
            0o600,
            info.st_size,
        )

    def plan(self):
        return migration.CopyPlan(
            "synthetic-consumer",
            (row(),),
            (self.input(row().source_path),),
            self.server.origin,
            "127.0.0.1",
            self.input("copy.token"),
            self.input("metadata.token"),
            self.input("ca.pem"),
            self.ca_hash,
            migration.CopyBudget(0.3, 0.3, 2.0),
        )

    def execute(self, plan=None, authorize=None):
        return migration.execute_copy(
            plan or self.plan(), authorize=authorize or (lambda _: True)
        )

    def test_create_preserves_exact_bytes_and_only_cas_zero(self):
        result = self.execute()
        self.assertEqual("COMPLETE", result.status)
        self.assertEqual(
            ("CREATED", 1), (result.items[0].status, result.items[0].kv_version)
        )
        self.assertEqual(MARKER, self.server.value.encode())
        self.assertEqual(MARKER, self.source.read_bytes())
        posts = [
            json.loads(raw)
            for method, _, raw, _ in self.server.calls
            if method == "POST"
        ]
        self.assertEqual(
            [{"options": {"cas": 0}, "data": {"value": MARKER.decode()}}], posts
        )

    def test_equal_noop_different_conflict_and_no_write(self):
        self.server.version = 3
        for value, status in ((MARKER.decode(), "NOOP"), ("different", "CONFLICT")):
            with self.subTest(value=value):
                self.server.value = value
                self.server.calls.clear()
                result = self.execute()
                self.assertEqual(status, result.items[0].status)
                self.assertFalse(
                    any(method == "POST" for method, *_ in self.server.calls)
                )

    def test_lost_write_readback_reconciles_without_retry(self):
        self.server.mode = "lost_write"
        result = self.execute()
        self.assertEqual("RECONCILED_EQUAL", result.items[0].status)
        self.assertEqual(1, sum(method == "POST" for method, *_ in self.server.calls))

    def test_404_alone_deleted_destroyed_forbidden_missing_mount_never_create(self):
        metadata = "/v1/secret/metadata/" + row().kv_path
        config = "/v1/secret/config"
        for path, response in (
            (metadata, (403, {"errors": []})),
            (config, (404, {"errors": []})),
            (
                metadata,
                (
                    200,
                    {
                        "data": {
                            "current_version": 1,
                            "versions": {
                                "1": {"deletion_time": "yesterday", "destroyed": False}
                            },
                        }
                    },
                ),
            ),
            (
                metadata,
                (
                    200,
                    {
                        "data": {
                            "current_version": 1,
                            "versions": {"1": {"deletion_time": "", "destroyed": True}},
                        }
                    },
                ),
            ),
        ):
            with self.subTest(path=path, response=response):
                self.server.responses = {("GET", path): response}
                self.server.calls.clear()
                result = self.execute()
                self.assertEqual("UNRESOLVED", result.items[0].status)
                self.assertFalse(
                    any(method == "POST" for method, *_ in self.server.calls)
                )

    def test_authorization_is_out_of_band_and_precedes_private_reads(self):
        plan = self.plan()
        with patch("os.open", side_effect=AssertionError("no private I/O")):
            result = self.execute(plan, lambda _: False)
        self.assertEqual("BLOCKED", result.status)
        self.assertEqual("copy_not_authorized", result.diagnostic)
        self.assertEqual([], self.server.calls)

    def test_failures_never_return_secret_markers(self):
        path = "/v1/secret/data/" + row().kv_path
        for raw in (
            b'{"data":{},"data":{"value":"synthetic-private-marker"}}',
            b'{"data":NaN}',
            b'{"value":"synthetic-private-marker"}',
            b"x" * 131073,
        ):
            with self.subTest(raw=raw[:30]):
                self.server.responses = {("GET", path): (200, raw)}
                output = io.StringIO()
                with (
                    contextlib.redirect_stdout(output),
                    contextlib.redirect_stderr(output),
                ):
                    result = self.execute()
                self.assertNotIn(
                    "synthetic-private-marker", repr(result) + output.getvalue()
                )
                self.assertNotEqual("COMPLETE", result.status)

    def test_redirect_and_ambient_proxy_are_never_used(self):
        path = "/v1/secret/data/" + row().kv_path
        with patch.dict(
            os.environ,
            {
                "HTTPS_PROXY": "https://wrong.example",
                "HTTP_PROXY": "http://wrong.example",
            },
        ):
            self.assertEqual("COMPLETE", self.execute().status)
        self.server.responses = {("GET", path): (307, {"errors": []})}
        self.server.calls.clear()
        self.assertEqual("UNRESOLVED", self.execute().items[0].status)
        self.assertEqual(1, len(self.server.calls))

    def test_whole_deadline_bounds_slow_headers(self):
        self.server.mode = "headers_slow"
        plan = replace(self.plan(), budget=migration.CopyBudget(0.1, 0.15, 0.2))
        start = time.monotonic()
        result = self.execute(plan)
        self.assertLess(time.monotonic() - start, 0.7)
        self.assertNotEqual("COMPLETE", result.status)

    def test_source_token_ca_symlinks_hardlinks_owner_mode_fifo_and_size(self):
        for name in (row().source_path, "copy.token", "metadata.token", "ca.pem"):
            target = self.folder / name
            for kind in ("symlink", "hardlink", "mode", "owner", "size", "fifo"):
                with self.subTest(name=name, kind=kind):
                    plan = self.plan()
                    data = target.read_bytes()
                    if kind == "symlink":
                        backup = target.with_name(target.name + ".real")
                        target.rename(backup)
                        target.symlink_to(backup)
                    elif kind == "hardlink":
                        backup = target.with_name(target.name + ".link")
                        os.link(target, backup)
                    elif kind == "mode":
                        target.chmod(0o644)
                    elif kind == "owner":
                        refs = tuple(
                            replace(item, uid=item.uid + 1)
                            if item.relative == name
                            else item
                            for item in plan.sources
                        )
                        plan = replace(plan, sources=refs)
                        if name != row().source_path:
                            field = {
                                "copy.token": "copy_token",
                                "metadata.token": "metadata_token",
                                "ca.pem": "ca",
                            }[name]
                            plan = replace(
                                plan,
                                **{
                                    field: replace(
                                        getattr(plan, field), uid=os.getuid() + 1
                                    )
                                },
                            )
                    elif kind == "size":
                        target.write_bytes(data + b"x")
                    else:
                        target.unlink()
                        os.mkfifo(target, 0o600)
                    self.server.calls.clear()
                    result = self.execute(plan)
                    self.assertEqual("BLOCKED", result.status)
                    self.assertEqual([], self.server.calls)
                    if kind in {"symlink", "fifo"}:
                        target.unlink()
                    if kind == "symlink":
                        backup.rename(target)
                    elif kind == "hardlink":
                        backup.unlink()
                    else:
                        target.write_bytes(data)
                    target.chmod(0o600)

    def test_parent_symlink_and_ca_hash_and_hostname_fail_closed(self):
        plan = self.plan()
        real = self.folder / "secrets-real"
        (self.folder / "secrets").rename(real)
        (self.folder / "secrets").symlink_to(real)
        self.assertEqual("BLOCKED", self.execute(plan).status)
        (self.folder / "secrets").unlink()
        real.rename(self.folder / "secrets")
        self.assertEqual(
            "BLOCKED", self.execute(replace(self.plan(), ca_sha256="0" * 64)).status
        )
        result = self.execute(
            replace(
                self.plan(),
                origin=self.server.origin.replace("localhost", "wrong.example"),
            )
        )
        self.assertNotEqual("COMPLETE", result.status)

    def test_partial_preserves_earlier_version_and_source(self):
        second = replace(
            row("PG-034"),
            kv_path="hy-home/dev/synthetic/second",
            source_path="secrets/db/dev-pg/second.txt",
        )
        (self.folder / second.source_path).write_bytes(MARKER)
        (self.folder / second.source_path).chmod(0o600)
        self.server.responses = {
            ("GET", "/v1/secret/data/" + second.kv_path): (403, {"errors": []})
        }
        plan = replace(
            self.plan(),
            selections=(row(), second),
            sources=(self.input(row().source_path), self.input(second.source_path)),
        )
        result = self.execute(plan)
        self.assertEqual("PARTIAL", result.status)
        self.assertEqual(
            ("CREATED", 1), (result.items[0].status, result.items[0].kv_version)
        )
        self.assertEqual(MARKER, self.source.read_bytes())

    def test_cas_race_is_readback_only_equal_or_conflict(self):
        for mode, expected in (
            ("race_equal", "RECONCILED_EQUAL"),
            ("race_different", "CONFLICT"),
        ):
            with self.subTest(mode=mode):
                self.server.mode, self.server.version = mode, 0
                self.server.calls.clear()
                result = self.execute()
                self.assertEqual(expected, result.items[0].status)
                self.assertEqual(2, result.items[0].kv_version)
                self.assertEqual(
                    1, sum(method == "POST" for method, *_ in self.server.calls)
                )

    def test_known_created_version_survives_failed_readback(self):
        self.server.mode = "readback_forbidden"
        result = self.execute()
        self.assertEqual("PARTIAL", result.status)
        self.assertEqual(
            ("UNRESOLVED", 1),
            (result.items[0].status, result.items[0].accepted_version),
        )
        self.assertEqual(1, sum(method == "POST" for method, *_ in self.server.calls))
        self.assertIsNone(result.items[0].kv_version)
        self.assertTrue(result.items[0].write_attempted)
        self.assertEqual(MARKER, self.source.read_bytes())

    def test_body_deadline_chunked_and_no_dns(self):
        with patch("socket.getaddrinfo", side_effect=AssertionError("ambient DNS")):
            self.server.mode = "chunked"
            self.assertEqual("COMPLETE", self.execute().status)
        self.server.mode = "body_slow"
        plan = replace(self.plan(), budget=migration.CopyBudget(0.1, 0.15, 0.2))
        start = time.monotonic()
        self.assertNotEqual("COMPLETE", self.execute(plan).status)
        self.assertLess(time.monotonic() - start, 0.7)

    def test_empty_oversize_binary_malformed_tokens_and_bad_binding_precede_network(
        self,
    ):
        for data in (b"", b"x" * (migration.MAX_BYTES + 1), b"\xff"):
            with self.subTest(kind=len(data)):
                self.source.write_bytes(data)
                result = self.execute()
                self.assertEqual("BLOCKED", result.status)
                self.assertEqual([], self.server.calls)
        self.source.write_bytes(MARKER)
        for data in (b"token\r\n", b"token value", b"token\nsecond", b"x" * 4097):
            (self.folder / "copy.token").write_bytes(data)
            self.assertEqual("BLOCKED", self.execute().status)
            self.assertEqual([], self.server.calls)
        (self.folder / "copy.token").write_bytes(b"synthetic-copy.token")
        for plan in (
            replace(self.plan(), origin="http://localhost"),
            replace(self.plan(), origin="https://u:p@localhost"),
            replace(self.plan(), connect_ip="localhost"),
            replace(self.plan(), budget=migration.CopyBudget(0.3, 0.3, float("nan"))),
            replace(
                self.plan(),
                selections=(replace(row(), destination_status="BLOCKED_P01"),),
            ),
        ):
            with self.subTest(plan=plan.origin):
                self.assertEqual("BLOCKED", self.execute(plan).status)
                self.assertEqual([], self.server.calls)

    def test_mutation_rebind_during_read_is_detected_for_all_private_inputs(self):
        real_read = os.read
        for name in (row().source_path, "copy.token", "metadata.token", "ca.pem"):
            target = self.folder / name
            for kind in ("mutate", "rebind"):
                with self.subTest(name=name, kind=kind):
                    plan = self.plan()
                    original, info = target.read_bytes(), target.stat()
                    triggered = []

                    def reader(
                        descriptor,
                        amount,
                        *,
                        info=info,
                        triggered=triggered,
                        kind=kind,
                        target=target,
                        original=original,
                    ):
                        data = real_read(descriptor, amount)
                        current = os.fstat(descriptor)
                        if current.st_ino == info.st_ino and not triggered:
                            triggered.append(True)
                            if kind == "mutate":
                                target.write_bytes(original)
                            else:
                                replacement = target.with_name(target.name + ".new")
                                replacement.write_bytes(original)
                                replacement.chmod(0o600)
                                replacement.replace(target)
                        return data

                    with patch("os.read", side_effect=reader):
                        self.assertEqual("BLOCKED", self.execute(plan).status)
                    self.assertEqual([True], triggered)
                    self.assertEqual([], self.server.calls)
                    target.write_bytes(original)
                    target.chmod(0o600)

    def test_json_depth_and_version_shapes_are_fail_closed(self):
        path = "/v1/secret/data/" + row().kv_path
        nested = {"value": "synthetic-private-marker"}
        for _ in range(14):
            nested = {"deep": nested}
        cases = [nested]
        for version in (None, True, 0, "1"):
            cases.append(
                {
                    "data": {
                        "data": {"value": MARKER.decode()},
                        "metadata": {
                            "version": version,
                            "deletion_time": "",
                            "destroyed": False,
                        },
                    }
                }
            )
        for document in cases:
            self.server.responses = {("GET", path): (200, document)}
            self.server.calls.clear()
            result = self.execute()
            self.assertEqual("UNRESOLVED", result.items[0].status)
            self.assertFalse(any(method == "POST" for method, *_ in self.server.calls))

    def test_malformed_http_headers_body_chunks_and_content_type(self):
        prefix = b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n"
        packets = (
            b"not-http\r\n\r\n",
            prefix + b"Content-Length: 2\r\nContent-Length: 2\r\n\r\n{}",
            prefix + b"Content-Length: 2\r\nTransfer-Encoding: chunked\r\n\r\n{}",
            prefix + b"Content-Length: 131073\r\n\r\n",
            prefix + b"Content-Length: 99\r\n\r\n{}",
            prefix + b" Bad: folded\r\n\r\n{}",
            prefix + b"X-Large: " + b"x" * 5000 + b"\r\n\r\n{}",
            prefix + b"Transfer-Encoding: unsupported\r\n\r\n{}",
            prefix + b"Transfer-Encoding: chunked\r\n\r\ngarbage\r\n",
            prefix + b"Transfer-Encoding: chunked\r\n\r\n30000\r\n",
            prefix + b"Transfer-Encoding: chunked\r\n\r\n2\r\n{}bad",
            prefix
            + b"Transfer-Encoding: chunked\r\n\r\n0\r\nTrailer: unapproved\r\n\r\n",
            b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: 2\r\n\r\n{}",
            prefix + b"Content-Length: wrong\r\n\r\n{}",
            prefix + b"Connection: close\r\n\r\n" + b"x" * 131073,
        )
        for packet in packets:
            with self.subTest(packet=packet[:90]):
                self.server.wire = packet
                self.server.calls.clear()
                result = self.execute()
                self.assertEqual("UNRESOLVED", result.items[0].status)
                self.assertEqual(1, len(self.server.calls))

    def test_wrong_ca_and_mixed_pem_fail_closed(self):
        with tempfile.TemporaryDirectory(prefix="p06-wrong-ca-") as temporary:
            folder = Path(temporary)
            certificates(folder)
            original = (self.folder / "ca.pem").read_bytes()
            wrong = (folder / "ca.pem").read_bytes()
            for data in (
                wrong,
                original + (folder / "key.pem").read_bytes(),
                b"invalid-cert",
            ):
                (self.folder / "ca.pem").write_bytes(data)
                result = self.execute(
                    replace(self.plan(), ca_sha256=hashlib.sha256(data).hexdigest())
                )
                self.assertNotEqual("COMPLETE", result.status)
                self.assertEqual([], self.server.calls)
            (self.folder / "ca.pem").write_bytes(original)

    def test_direct_transport_request_boundary_and_private_repr(self):
        from contextlib import ExitStack

        from scripts.lib.ops._openbao_copy_io import hold_input, verified_context
        from scripts.lib.ops._openbao_copy_transport import CopyTransport

        plan = self.plan()
        with ExitStack() as stack:
            held = hold_input(plan.ca, stack, ca=True)
            context = verified_context(held, self.ca_hash)
            self.assertNotIn("BEGIN CERTIFICATE", repr(held))
            path = "/v1/secret/data/" + row().kv_path
            transport = CopyTransport(
                plan.origin,
                plan.connect_ip,
                plan.budget,
                context,
                (path,),
                time.monotonic() + 2,
                lambda: None,
            )
            for method, chosen, token in (
                ("DELETE", path, "token"),
                ("POST", "/v1/secret/metadata/hy-home/x", "token"),
                ("GET", path, "bad\r\ntoken"),
                ("GET", "/unbound", "token"),
            ):
                with self.assertRaises(migration.MigrationError):
                    transport.request(method, chosen, token)
            with self.assertRaises(migration.MigrationError):
                CopyTransport(
                    plan.origin,
                    plan.connect_ip,
                    plan.budget,
                    context,
                    ("/unsafe\r\npath",),
                    time.monotonic() + 2,
                    lambda: None,
                )
            with self.assertRaises(migration.MigrationError):
                unsafe_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
                unsafe_context.check_hostname = False
                CopyTransport(
                    plan.origin,
                    plan.connect_ip,
                    plan.budget,
                    unsafe_context,
                    (path,),
                    time.monotonic() + 2,
                    lambda: None,
                )
        self.assertEqual([], self.server.calls)

    def test_callbacks_never_authenticate_records_or_leak_diagnostics(self):
        plan = self.plan()

        def bad_controller(_):
            raise migration.MigrationError("synthetic-private-marker")

        for callback in (
            None,
            lambda _: {"approved": True},
            lambda _: 1,
            bad_controller,
        ):
            result = (
                self.execute(plan, callback)
                if callback
                else migration.execute_copy(plan, authorize=callback)
            )
            self.assertEqual("BLOCKED", result.status)
            self.assertEqual("copy_not_authorized", result.diagnostic)
            self.assertEqual([], self.server.calls)
        result = migration.execute_copy({"approved": True}, authorize=lambda _: True)
        self.assertEqual("BLOCKED", result.status)

    def test_held_root_parent_permission_changes_are_detected(self):
        from contextlib import ExitStack

        from scripts.lib.ops._openbao_copy_io import hold_input

        for target in (self.folder, self.folder / "secrets"):
            with self.subTest(kind=target.name), ExitStack() as stack:
                held = hold_input(self.input(row().source_path), stack)
                target.chmod(0o770)
                try:
                    with self.assertRaises(migration.MigrationError):
                        held.check()
                finally:
                    target.chmod(0o700)


if __name__ == "__main__":
    unittest.main()
