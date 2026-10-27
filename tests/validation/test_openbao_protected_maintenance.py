"""Synthetic protected ceremony tests; never use HOME credentials or endpoints."""

from __future__ import annotations

import base64
import hashlib
import http.server
import importlib.util
import io
import json
import os
import ssl
import stat
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "infra/03-security/openbao/scripts/protected-maintenance.py"
SPEC = importlib.util.spec_from_file_location("protected_maintenance", SOURCE)
M = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = M
SPEC.loader.exec_module(M)

TOKEN = "synthetic-operator"
ROOT_TOKEN = "s." + "r" * 24
OTP = "A" * len(ROOT_TOKEN)
NONCE = "12345678-1234-1234-1234-123456789abc"
CLUSTER = "11111111-2222-3333-4444-555555555555"
ENCODED = (
    base64.b64encode(
        bytes(a ^ b for a, b in zip(ROOT_TOKEN.encode(), OTP.encode(), strict=True))
    )
    .decode()
    .rstrip("=")
)


def pinned_context(path):
    return M.ca_context(path, hashlib.sha256(path.read_bytes()).hexdigest())


def operator():
    return {
        "data": {
            "policies": ["default", "hy-home-operator"],
            "ttl": 3600,
            "creation_ttl": 3600,
            "renewable": True,
            "path": "auth/oidc/oidc/callback",
            "entity_id": "synthetic-operator-entity",
            "meta": {"role": "home-admin"},
        }
    }


def seal():
    return {
        "initialized": True,
        "sealed": False,
        "type": "shamir",
        "n": 3,
        "t": 2,
        "version": "2.6.2",
        "cluster_id": CLUSTER,
    }


def progress(number=0, complete=False, **fields):
    # OpenBao 2.6.2 and 2.7.1 return generate-root-token fields under "data".
    return {
        "data": {
            "started": True,
            "nonce": NONCE,
            "progress": number,
            "required": 2,
            "complete": complete,
            **({"encoded_token": ENCODED} if complete else {}),
            **fields,
        }
    }


def idle():
    return {"data": {"started": False}}


class FakeAPI:
    def __init__(self):
        self.calls = []
        self.token = TOKEN
        self.root_response = {
            "data": {
                "policies": ["root"],
                "path": "auth/token/root",
                "display_name": "root",
                "type": "service",
                "orphan": True,
                "entity_id": "",
                "expire_time": None,
                "ttl": 0,
                "creation_ttl": 0,
                "explicit_max_ttl": 0,
                "num_uses": 0,
                "id": "synthetic-internal-root-id",
            }
        }
        self.responses = [
            operator(),
            seal(),
            idle(),
            progress(otp=OTP, otp_length=len(OTP)),
            progress(1),
            progress(2, True),
            operator(),
        ]

    def root_lookup(self, token):
        self.calls.append(("ROOT_LOOKUP", M.LOOKUP, token))
        return self.root_response

    def request(self, method, path, document=None):
        self.calls.append((method, path, document))
        response = self.responses.pop(0)
        if isinstance(response, BaseException):
            raise response
        return response


class CeremonyTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.directory = Path(self.tmp.name) / "custody"
        self.directory.mkdir(mode=0o700)
        self.api = FakeAPI()
        self.shares = iter(["a" * 64, "b" * 64])

    def tearDown(self):
        self.tmp.cleanup()

    def run_ceremony(self):
        with M.Custody(self.directory) as custody:
            return M.ceremony(self.api, custody, CLUSTER, lambda _: next(self.shares))

    def test_success_preserves_each_response_before_root_delivery(self):
        self.assertEqual(self.run_ceremony(), "DELIVERED")
        self.assertEqual((self.directory / "root.token").read_text(), ROOT_TOKEN)
        for name in ("initialization.json", "update-1.json", "update-2.json"):
            self.assertTrue((self.directory / name).is_file())
            self.assertEqual(
                stat.S_IMODE((self.directory / name).stat().st_mode), 0o600
            )
        self.assertEqual(self.api.calls[-1][:2], ("GET", M.LOOKUP))
        self.assertFalse(any(call[0] == "DELETE" for call in self.api.calls))

    def test_rejects_non_operator_and_root_policy_before_attempt(self):
        for policies in (
            ["root"],
            ["hy-home-operator"],
            ["default", "extra", "hy-home-operator"],
        ):
            with self.subTest(policies=policies):
                self.api = FakeAPI()
                self.api.responses[0]["data"]["policies"] = policies
                with M.Custody(self.directory) as custody:
                    with self.assertRaises(M.Blocked):
                        M.ceremony(self.api, custody, CLUSTER, lambda _: "a" * 64)
                self.assertEqual(len(self.api.calls), 1)
                (self.directory / ".lock").unlink()

    def test_missing_empty_or_wrong_type_operator_entity_never_starts_attempt(self):
        valid = operator()["data"]
        cases = {
            "missing": {
                key: value for key, value in valid.items() if key != "entity_id"
            },
            **{
                label: {**valid, "entity_id": value}
                for label, value in (
                    ("null", None),
                    ("empty", ""),
                    ("boolean", False),
                    ("integer", 7),
                    ("list", []),
                    ("object", {}),
                )
            },
        }
        for label, data in cases.items():
            with self.subTest(case=label):
                self.api = FakeAPI()
                self.api.responses[0] = {"data": data}
                shares = iter(["a" * 64, "b" * 64])
                with tempfile.TemporaryDirectory(dir=self.tmp.name) as directory:
                    with M.Custody(Path(directory)) as custody:
                        with self.assertRaises(M.Blocked):
                            M.ceremony(
                                self.api,
                                custody,
                                CLUSTER,
                                lambda _, shares=shares: next(shares),
                            )
                self.assertEqual(self.api.calls, [("GET", M.LOOKUP, None)])

    def test_operator_outside_home_admin_role_or_with_identity_policy_is_blocked(self):
        valid = operator()["data"]
        cases = {
            "missing meta": {k: v for k, v in valid.items() if k != "meta"},
            "other role": {**valid, "meta": {"role": "reader"}},
            "extra meta": {**valid, "meta": {"role": "home-admin", "x": "1"}},
            "identity policy": {**valid, "identity_policies": ["extra"]},
            "malformed identity policies": {**valid, "identity_policies": "extra"},
        }
        for label, data in cases.items():
            with self.subTest(case=label):
                self.api = FakeAPI()
                self.api.responses[0] = {"data": data}
                with tempfile.TemporaryDirectory(dir=self.tmp.name) as directory:
                    with M.Custody(Path(directory)) as custody:
                        with self.assertRaises(M.Blocked):
                            M.ceremony(self.api, custody, CLUSTER, lambda _: "a" * 64)
                self.assertEqual(self.api.calls, [("GET", M.LOOKUP, None)])
        for empty in (None, []):
            M.check_operator({"data": {**valid, "identity_policies": empty}})

    def test_lost_operator_entity_after_delivery_preserves_root_custody(self):
        self.api.responses[6] = {"data": {**operator()["data"], "entity_id": ""}}
        with self.assertRaises(M.Indeterminate):
            self.run_ceremony()
        self.assertEqual((self.directory / "root.token").read_text(), ROOT_TOKEN)
        self.assertFalse((self.directory / "state.json").exists())
        self.assertFalse(any(call[0] == "DELETE" for call in self.api.calls))

    def test_sealed_cluster_version_or_threshold_mismatch_never_initializes(self):
        for key, value in (
            ("sealed", True),
            ("n", 5),
            ("t", 3),
            ("version", "2.5.0"),
            ("cluster_id", "other"),
        ):
            with self.subTest(key=key):
                self.api = FakeAPI()
                self.api.responses[1][key] = value
                with M.Custody(self.directory) as custody:
                    with self.assertRaises(M.Blocked):
                        M.ceremony(self.api, custody, CLUSTER, lambda _: "a" * 64)
                self.assertFalse(any(call[0] == "POST" for call in self.api.calls))
                (self.directory / ".lock").unlink()

    def test_unwrapped_attempt_status_is_refused_before_any_mutation(self):
        # The pre-fix client read "started" at the top level and so was always
        # BLOCKED against the real data-wrapped response; never accept either.
        for status in ({"started": False}, {"data": None}, {"data": []}):
            with self.subTest(status=status):
                self.api = FakeAPI()
                self.api.responses[2] = status
                with M.Custody(self.directory) as custody:
                    with self.assertRaises(M.Blocked):
                        M.ceremony(self.api, custody, CLUSTER, lambda _: "a" * 64)
                self.assertFalse(any(call[0] == "POST" for call in self.api.calls))
                (self.directory / ".lock").unlink()

    def test_unwrapped_response_after_attempt_start_is_indeterminate(self):
        # Once an attempt exists, a malformed response or an unprovable cancel
        # must exit 2 with custody kept, never 1.
        cases = {
            "initialization": {3: {"nonce": NONCE, "started": True}},
            "update and cancel status": {
                4: {"started": True, "progress": 1},
                5: {"started": True, "nonce": NONCE, "complete": False},
            },
        }
        for name, replacements in cases.items():
            with self.subTest(name=name):
                self.api = FakeAPI()
                self.shares = iter(["a" * 64, "b" * 64])
                for index, value in replacements.items():
                    self.api.responses[index] = value
                with self.assertRaises(M.Indeterminate):
                    self.run_ceremony()
                self.assertTrue((self.directory / "initialization.json").is_file())
                self.assertFalse(any(call[0] == "DELETE" for call in self.api.calls))
                for path in self.directory.iterdir():
                    path.unlink()

    def test_existing_attempt_is_never_cancelled(self):
        self.api.responses[2] = progress(1)
        with self.assertRaises(M.Blocked):
            self.run_ceremony()
        self.assertFalse(any(call[0] in {"POST", "DELETE"} for call in self.api.calls))

    def test_duplicate_share_cancels_only_matching_pending_attempt(self):
        self.shares = iter(["a" * 64, "a" * 64])
        self.api.responses[5:] = [progress(1), None, idle()]
        with self.assertRaises(M.Blocked):
            self.run_ceremony()
        self.assertFalse(any(call[0] in {"POST", "DELETE"} for call in self.api.calls))
        self.assertFalse((self.directory / "root.token").exists())

    def test_other_nonce_is_never_cancelled(self):
        self.shares = iter(["a" * 64, "a" * 64])
        self.api.responses[5:] = [progress(1, nonce="another-attempt")]
        with self.assertRaises(M.Blocked):
            self.run_ceremony()
        self.assertFalse(any(call[0] == "DELETE" for call in self.api.calls))

    def test_final_update_transport_loss_is_indeterminate_and_retained(self):
        self.api.responses[5:] = [M.Indeterminate(), idle()]
        with self.assertRaises(M.Indeterminate):
            self.run_ceremony()
        self.assertTrue((self.directory / "initialization.json").is_file())
        self.assertFalse((self.directory / "root.token").exists())
        self.assertFalse(any(call[0] == "DELETE" for call in self.api.calls))

    def test_decode_failure_retains_completed_encoded_response_without_cancel(self):
        self.api.responses[5]["data"]["encoded_token"] = "broken!"
        with self.assertRaises(M.Indeterminate):
            self.run_ceremony()
        self.assertEqual(
            json.loads((self.directory / "update-2.json").read_text())["data"][
                "encoded_token"
            ],
            "broken!",
        )
        self.assertFalse(any(call[0] == "DELETE" for call in self.api.calls))

    def test_normal_operator_failure_after_delivery_retains_root(self):
        self.api.responses[6] = M.Blocked()
        with self.assertRaises(M.Indeterminate):
            self.run_ceremony()
        self.assertEqual((self.directory / "root.token").read_text(), ROOT_TOKEN)

    def test_custody_write_failure_prevents_second_share_submission(self):
        original = M.Custody.reserve

        def fail(custody, name):
            if name == "update-2.json":
                raise M.Blocked()
            return original(custody, name)

        self.api.responses[5:] = [progress(1), None, idle()]
        with (
            mock.patch.object(M.Custody, "reserve", fail),
            self.assertRaises(M.Blocked),
        ):
            self.run_ceremony()
        self.assertEqual(sum(call[1] == M.UPDATE for call in self.api.calls), 1)


class ProtectedInputsTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_private_fd_reads_bounded_input_without_path_argument(self):
        path = self.root / "synthetic"
        path.write_text(TOKEN + "\n")
        path.chmod(0o600)
        with path.open("rb") as stream:
            self.assertEqual(M.read_secret_fd(stream.fileno()), TOKEN)

    def test_public_multilink_consumed_or_oversized_fd_is_rejected(self):
        path = self.root / "synthetic"
        path.write_text(TOKEN)
        for mode, consumed, linked in (
            (0o644, False, False),
            (0o600, True, False),
            (0o600, False, True),
        ):
            with self.subTest(mode=mode, consumed=consumed, linked=linked):
                path.chmod(mode)
                if linked:
                    os.link(path, self.root / "link")
                with path.open("rb") as stream:
                    if consumed:
                        stream.read(1)
                    with self.assertRaises(M.Blocked):
                        M.read_secret_fd(stream.fileno())
                if linked:
                    (self.root / "link").unlink()
        path.write_text("a" * 4097)
        with path.open("rb") as stream, self.assertRaises(M.Blocked):
            M.read_secret_fd(stream.fileno())

    def test_custody_rejects_symlink_and_non_private_directory(self):
        directory = self.root / "custody"
        directory.mkdir(mode=0o755)
        with self.assertRaises(M.Blocked):
            M.Custody(directory)
        directory.chmod(0o700)
        (self.root / "link").symlink_to(directory)
        with self.assertRaises(M.Blocked):
            M.Custody(self.root / "link")

    def test_custody_rejects_nonempty_directory_and_no_overwrite(self):
        directory = self.root / "custody"
        directory.mkdir(mode=0o700)
        (directory / "root.token").write_text("preserved")
        with self.assertRaises(M.Blocked):
            M.Custody(directory)
        self.assertEqual((directory / "root.token").read_text(), "preserved")

    def test_custody_lock_prevents_concurrent_operation(self):
        directory = self.root / "custody"
        directory.mkdir(mode=0o700)
        with M.Custody(directory), self.assertRaises(M.Blocked):
            M.Custody(directory)

    def test_duplicate_json_and_wrong_base64_xor_lengths_fail_closed(self):
        with self.assertRaises(M.Blocked):
            M.parse_response(b'{"otp":"synthetic", "otp":"other"}')
        for encoded, otp in (("!", OTP), (ENCODED, "short"), (ENCODED + "====", OTP)):
            with self.subTest(encoded=encoded):
                with self.assertRaises(M.Blocked):
                    M.decode_token(encoded, otp)
        self.assertEqual(M.decode_token(ENCODED, OTP), ROOT_TOKEN)

    def test_fd_rejects_pipe_nonascii_newline_and_concurrent_mutation(self):
        read_fd, write_fd = os.pipe()
        try:
            with self.assertRaises(M.Blocked):
                M.read_secret_fd(read_fd)
        finally:
            os.close(read_fd)
            os.close(write_fd)
        path = self.root / "secret"
        for value in (b"\xff", b"token\nother", b"token\r\n"):
            path.write_bytes(value)
            path.chmod(0o600)
            with path.open("rb") as stream, self.assertRaises(M.Blocked):
                M.read_secret_fd(stream.fileno())
        path.write_text(TOKEN)
        original = os.read

        def mutate(descriptor, count):
            result = original(descriptor, count)
            path.write_text("different")
            return result

        with path.open("rb") as stream, mock.patch.object(M.os, "read", mutate):
            with self.assertRaises(M.Blocked):
                M.read_secret_fd(stream.fileno())

    def test_raw_error_json_non_object_or_oversized_json_rejected(self):
        for value in (b"not-json", b"[]", b"null", b'"token"', b"{}" + b" " * 65536):
            with self.subTest(value=value[:10]), self.assertRaises(M.Blocked):
                M.parse_response(value)

    def test_directory_alias_and_reserved_filename_are_rejected(self):
        with self.assertRaises(M.Blocked):
            M.open_directory("relative")
        directory = self.root / "custody"
        directory.mkdir(mode=0o700)
        with M.Custody(directory) as custody:
            with self.assertRaises(M.Blocked):
                custody.reserve("../foreign")
            descriptor = custody.reserve("root.token")
            custody.write(descriptor, "synthetic")
            with self.assertRaises(FileExistsError):
                custody.reserve("root.token")


class TLSFixtureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.root = Path(cls.tmp.name)
        for label, host in (("valid", M.HOST), ("wrong", "wrong.invalid")):
            command = [
                "openssl",
                "req",
                "-x509",
                "-newkey",
                "rsa:2048",
                "-nodes",
                "-keyout",
                str(cls.root / f"{label}.key"),
                "-out",
                str(cls.root / f"{label}.pem"),
                "-days",
                "1",
                "-subj",
                f"/CN={host}",
                "-addext",
                f"subjectAltName=DNS:{host}",
            ]
            subprocess.run(command, check=True, capture_output=True)
            (cls.root / f"{label}.pem").chmod(0o644)
        subprocess.run(
            [
                "openssl",
                "x509",
                "-in",
                str(cls.root / "valid.pem"),
                "-signkey",
                str(cls.root / "valid.key"),
                "-days",
                "-1",
                "-out",
                str(cls.root / "expired.pem"),
            ],
            check=True,
            capture_output=True,
        )
        (cls.root / "expired.pem").chmod(0o644)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def serve(self, certificate="valid", slow=False):
        class Handler(http.server.BaseHTTPRequestHandler):
            def log_message(self, *_):
                pass

            def do_GET(self):
                payload = json.dumps(operator()).encode()
                self.send_response(200)
                self.send_header("Content-Length", str(len(payload)))
                self.end_headers()
                if not slow:
                    self.wfile.write(payload)
                    return
                for byte in payload:
                    try:
                        self.wfile.write(bytes([byte]))
                        self.wfile.flush()
                    except (OSError, ssl.SSLError):
                        break
                    time.sleep(0.08)

        server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        server.daemon_threads = True
        server.handle_error = lambda *_: None
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(
            self.root / f"{certificate}.pem",
            self.root
            / ("valid.key" if certificate == "expired" else f"{certificate}.key"),
        )
        server.socket = context.wrap_socket(server.socket, server_side=True)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(server.server_close)
        self.addCleanup(server.shutdown)
        original = M.PinnedConnection

        def connection(host, _port, **options):
            return original(host, server.server_port, **options)

        patch = mock.patch.object(M, "PinnedConnection", connection)
        patch.start()
        self.addCleanup(patch.stop)

    def test_synthetic_tls_ca_and_fixed_san_success(self):
        self.serve()
        context = pinned_context(self.root / "valid.pem")
        api = M.API(TOKEN, context, "127.0.0.1")
        self.assertEqual(api.request("GET", M.LOOKUP), operator())

    def test_wrong_ca_wrong_hostname_or_expired_cert_fails_closed(self):
        for certificate, trust in (
            ("valid", "wrong"),
            ("wrong", "wrong"),
            ("expired", "expired"),
        ):
            with self.subTest(certificate=certificate):
                self.serve(certificate)
                with self.assertRaises(M.Indeterminate):
                    M.API(
                        TOKEN,
                        pinned_context(self.root / f"{trust}.pem"),
                        "127.0.0.1",
                    ).request("GET", M.LOOKUP)
                self.doCleanups()

    def test_slow_trickle_has_total_deadline_even_when_each_byte_arrives(self):
        self.serve(slow=True)
        started = time.monotonic()
        with (
            mock.patch.object(M, "REQUEST_SECONDS", 0.3),
            self.assertRaises(M.Indeterminate),
        ):
            M.API(
                TOKEN,
                pinned_context(self.root / "valid.pem"),
                "127.0.0.1",
            ).request("GET", M.LOOKUP)
        self.assertLess(time.monotonic() - started, 1.0)

    def test_ca_context_is_immutable_after_original_file_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            ca = Path(directory) / "ca.pem"
            ca.write_bytes((self.root / "valid.pem").read_bytes())
            ca.chmod(0o644)
            context = pinned_context(ca)
            ca.write_bytes((self.root / "wrong.pem").read_bytes())
            self.serve()
            self.assertEqual(
                M.API(TOKEN, context, "127.0.0.1").request("GET", M.LOOKUP), operator()
            )

    def test_ca_alias_hardlink_unsafe_mode_or_private_key_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            ca = base / "ca.pem"
            ca.write_bytes((self.root / "valid.pem").read_bytes())
            ca.chmod(0o644)
            (base / "link").symlink_to(ca)
            with self.assertRaises((M.Blocked, OSError)):
                M.ca_context(base / "link", hashlib.sha256(ca.read_bytes()).hexdigest())
            os.link(ca, base / "hard")
            with self.assertRaises(M.Blocked):
                pinned_context(ca)
            (base / "hard").unlink()
            ca.chmod(0o666)
            with self.assertRaises(M.Blocked):
                pinned_context(ca)
            ca.chmod(0o644)
            ca.write_bytes((self.root / "valid.key").read_bytes())
            with self.assertRaises(M.Blocked):
                pinned_context(ca)


class HTTPTests(unittest.TestCase):
    def connection(self, status=200, payload=b"{}"):
        response = mock.Mock(status=status)
        response.read.return_value = payload
        connection = mock.Mock()
        connection.getresponse.return_value = response
        return connection

    def test_fixed_origin_ignores_proxy_environment_and_sends_only_allowed_api(self):
        connection = self.connection(payload=json.dumps(operator()).encode())
        with mock.patch.object(M, "PinnedConnection", return_value=connection) as ctor:
            with mock.patch.dict(
                os.environ,
                {"HTTPS_PROXY": "http://attacker.invalid", "BAO_TOKEN": "unrelated"},
            ):
                api = M.API(TOKEN, mock.sentinel.context, "127.0.0.1")
                self.assertEqual(api.request("GET", M.LOOKUP), operator())
        self.assertEqual(ctor.call_args.args, ("openbao.hy.home.arpa", 443))
        request = connection.request.call_args
        self.assertEqual(request.args[:2], ("GET", "/v1/auth/token/lookup-self"))
        self.assertEqual(request.kwargs["headers"]["X-Vault-Token"], TOKEN)
        connection.close.assert_called_once()

    def test_redirect_error_or_oversized_response_never_echoes_secret_body(self):
        for status, body in (
            (302, TOKEN.encode()),
            (403, TOKEN.encode()),
            (200, b"a" * 65537),
        ):
            with self.subTest(status=status):
                connection = self.connection(status, body)
                with mock.patch.object(M, "PinnedConnection", return_value=connection):
                    with self.assertRaises((M.Blocked, M.Indeterminate)) as caught:
                        M.API(TOKEN, mock.sentinel.context, "127.0.0.1").request(
                            "GET", M.LOOKUP
                        )
                self.assertNotIn(TOKEN, str(caught.exception))
                connection.close.assert_called_once()

    def test_nonallowlisted_api_refused_before_network(self):
        with mock.patch.object(M, "PinnedConnection") as ctor:
            with self.assertRaises(M.Blocked):
                M.API(TOKEN, mock.sentinel.context, "127.0.0.1").request(
                    "POST", "auth/token/create", {}
                )
        ctor.assert_not_called()

    def test_cli_failure_does_not_print_arguments_or_secret_exception(self):
        output, error = io.StringIO(), io.StringIO()
        with (
            mock.patch.object(sys, "stdout", output),
            mock.patch.object(sys, "stderr", error),
        ):
            result = M.main(["--token", TOKEN])
        self.assertNotEqual(result, 0)
        self.assertNotIn(TOKEN, output.getvalue() + error.getvalue())
        self.assertNotIn("Traceback", output.getvalue() + error.getvalue())

    def test_mutating_http_failure_is_indeterminate_and_204_is_delete_only(self):
        for method, path, document, status in (
            ("POST", M.ATTEMPT, {}, 403),
            ("POST", M.ATTEMPT, {}, 200),
            ("GET", M.LOOKUP, None, 204),
        ):
            with self.subTest(method=method, status=status):
                connection = self.connection(status, b"invalid-json")
                with mock.patch.object(M, "PinnedConnection", return_value=connection):
                    with self.assertRaises(M.Blocked):
                        M.API(TOKEN, mock.sentinel.context, "127.0.0.1").request(
                            method, path, document
                        )
        connection = self.connection(204, b"")
        with mock.patch.object(M, "PinnedConnection", return_value=connection):
            self.assertIsNone(
                M.API(TOKEN, mock.sentinel.context, "127.0.0.1").request(
                    "DELETE", M.ATTEMPT
                )
            )

    def test_invalid_body_shape_refused_before_network(self):
        for method, path, document in (("POST", M.ATTEMPT, None), ("GET", M.SEAL, {})):
            with (
                mock.patch.object(M, "PinnedConnection") as ctor,
                self.assertRaises(M.Blocked),
            ):
                M.API(TOKEN, mock.sentinel.context, "127.0.0.1").request(
                    method, path, document
                )
            ctor.assert_not_called()


class CLITests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.custody = self.root / "custody"
        self.custody.mkdir(mode=0o700)
        self.arguments = [
            "--ca",
            str(self.root / "ca.pem"),
            "--ca-sha256",
            "0" * 64,
            "--custody-directory",
            str(self.custody),
            "--expected-cluster-id",
            CLUSTER,
            "--connect-ip",
            "127.0.0.1",
        ]

    def tearDown(self):
        self.tmp.cleanup()

    def capture(self, arguments, api=None):
        output, error = io.StringIO(), io.StringIO()
        with (
            mock.patch.object(sys, "stdout", output),
            mock.patch.object(sys, "stderr", error),
        ):
            with mock.patch.object(M, "ca_context", return_value=mock.sentinel.context):
                with mock.patch.object(M, "API", return_value=api or FakeAPI()):
                    result = M.main(arguments)
        value = output.getvalue() + error.getvalue()
        for secret in (TOKEN, ROOT_TOKEN, OTP, NONCE, ENCODED):
            self.assertNotIn(secret, value)
        self.assertNotIn("Traceback", value)
        return result, value

    def test_cli_three_distinct_private_fds_deliver_only_public_state(self):
        descriptors = []
        try:
            for name, value in (
                ("operator", TOKEN),
                ("one", "a" * 64),
                ("two", "b" * 64),
            ):
                path = self.root / name
                path.write_text(value)
                path.chmod(0o600)
                descriptors.append(os.open(path, os.O_RDONLY))
            arguments = [
                *self.arguments,
                "--operator-fd",
                str(descriptors[0]),
                "--share-one-fd",
                str(descriptors[1]),
                "--share-two-fd",
                str(descriptors[2]),
            ]
            self.assertEqual(self.capture(arguments), (0, "DELIVERED\n"))
        finally:
            for descriptor in descriptors:
                os.close(descriptor)

    def test_cli_duplicate_partial_stdio_fds_and_invalid_public_contract_fail(self):
        path = self.root / "operator"
        path.write_text(TOKEN)
        path.chmod(0o600)
        with path.open("rb") as stream:
            descriptor = str(stream.fileno())
            for suffix in (
                ["--operator-fd", descriptor],
                ["--operator-fd", "0", "--share-one-fd", "1", "--share-two-fd", "2"],
                [
                    "--operator-fd",
                    descriptor,
                    "--share-one-fd",
                    descriptor,
                    "--share-two-fd",
                    descriptor,
                ],
                ["--expected-cluster-id", "invalid"],
                ["--connect-ip", "attacker.invalid"],
            ):
                with self.subTest(suffix=suffix):
                    self.assertEqual(self.capture(self.arguments + suffix)[0], 1)

    def test_hidden_tty_input_and_uncertain_result_are_redacted(self):
        with mock.patch.object(
            M, "hidden_input", side_effect=[TOKEN, "a" * 64, "b" * 64]
        ):
            self.assertEqual(self.capture(self.arguments)[0], 0)
        other = self.root / "other-custody"
        other.mkdir(mode=0o700)
        arguments = [*self.arguments, "--custody-directory", str(other)]
        api = FakeAPI()
        api.responses[5] = M.Indeterminate()
        api.responses[6] = idle()
        with mock.patch.object(
            M, "hidden_input", side_effect=[TOKEN, "a" * 64, "b" * 64]
        ):
            result, output = self.capture(arguments, api)
        self.assertEqual(result, 2)
        self.assertIn("INDETERMINATE", output)

    def test_getpass_fallback_is_an_error_and_nonascii_secret_fails(self):
        with mock.patch("builtins.open", return_value=io.StringIO()):
            with mock.patch.object(M.getpass, "getpass", return_value=TOKEN):
                self.assertEqual(M.hidden_input("operator"), TOKEN)
        with self.assertRaises(M.Blocked):
            M.validate_secret("é")
        with self.assertRaises(M.Blocked):
            M.validate_secret(None)


if __name__ == "__main__":
    unittest.main()
