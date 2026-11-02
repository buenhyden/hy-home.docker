"""Public-interface proof for the P03 owned-isolated model registration utility."""

import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile
import threading
import unittest
import urllib.request
from contextlib import redirect_stderr, redirect_stdout
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from unittest.mock import patch

from scripts.lib.ops._notebook_models_http import ApiError, OpenNotebookClient
from scripts.lib.ops.notebook_models import (
    ModelPolicy,
    PolicyError,
    apply_policy,
    plan_policy,
    verify_policy,
)
from tests.lib.ops.test_notebook_models import POLICY
from tests.validation._p03_notebook_effects import measured_restore_counts
from tests.validation._p03_notebook_native import (
    NOTEBOOK_IMAGE,
    SURREALDB_IMAGE,
    DockerNotebookRuntime,
    NotebookNativeLifecycle,
)
from tests.validation._p03_notebook_readiness import (
    NativeSelectionError,
    inspect_cached_images,
    native_selection,
)
from tests.validation._p03_owned_docker import NativeFixtureError

ROOT = Path(__file__).resolve().parents[2]
CLI = ROOT / "scripts/operations/notebook-models.py"
FIXTURE_POLICY = ROOT / "tests/fixtures/p03_models/notebook-model-policy.json"


class _ApiState:
    def __init__(self):
        self.password = "synthetic-password"
        self.credentials = []
        self.models = []
        self.defaults = {"default_tools_model": "model:preserved"}
        self.requests = []
        self.redirect = False
        self.large = False
        self.duplicate_response = False


class _Handler(BaseHTTPRequestHandler):
    server_version = "P03Fixture/1"

    def log_message(self, _format, *_args):
        return

    @property
    def state(self):
        return self.server.state

    def _read_json(self):
        length = int(self.headers.get("Content-Length", "0"))
        return json.loads(self.rfile.read(length)) if length else None

    def _send(self, status, document):
        body = json.dumps(document).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _authorize(self):
        expected = f"Bearer {self.state.password}"
        if self.headers.get("Authorization") != expected:
            self._send(401, {"detail": "private fixture detail"})
            return False
        return True

    def do_GET(self):
        if not self._authorize():
            return
        self.state.requests.append(("GET", self.path, None))
        if self.state.redirect and self.path.startswith("/api/credentials"):
            self.send_response(302)
            self.send_header("Location", "/api/models")
            self.end_headers()
        elif self.state.large and self.path.startswith("/api/credentials"):
            self._send(200, ["x" * (1024 * 1024 + 1)])
        elif self.path == "/api/credentials?provider=ollama":
            self._send(200, self.state.credentials)
        elif self.path == "/api/models":
            if self.state.duplicate_response:
                body = b'{"model":"first","model":"second"}'
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
            else:
                self._send(200, self.state.models)
        elif self.path == "/api/models/defaults":
            self._send(200, self.state.defaults)
        else:
            self._send(404, {"detail": "not found"})

    def do_POST(self):
        if not self._authorize():
            return
        payload = self._read_json()
        self.state.requests.append(("POST", self.path, payload))
        if self.path == "/api/credentials":
            credential = {
                "id": "credential:p03",
                "name": payload["name"],
                "provider": payload["provider"],
                "modalities": payload["modalities"],
                "base_url": payload["base_url"],
                "has_api_key": False,
                "model_count": 0,
                "created": "synthetic",
                "updated": "synthetic",
            }
            self.state.credentials.append(credential)
            self._send(201, credential)
            return
        if self.path == "/api/credentials/credential:p03/register-models":
            for index, desired in enumerate(payload["models"], 1):
                self.state.models.append(
                    {
                        "id": f"model:p03_{index}",
                        "name": desired["name"],
                        "provider": desired["provider"],
                        "type": desired["model_type"],
                        "credential": "credential:p03",
                        "created": "synthetic",
                        "updated": "synthetic",
                    }
                )
            self._send(200, {"created": 2, "existing": 0})
            return
        self._send(404, {"detail": "not found"})

    def do_PUT(self):
        if not self._authorize():
            return
        payload = self._read_json()
        self.state.requests.append(("PUT", self.path, payload))
        if self.path == "/api/models/defaults":
            self.state.defaults.update(payload)
            self._send(200, self.state.defaults)
        else:
            self._send(404, {"detail": "not found"})


class _ServerTestCase(unittest.TestCase):
    def setUp(self):
        self.state = _ApiState()
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), _Handler)
        self.server.state = self.state
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.addCleanup(self.server.server_close)
        self.addCleanup(self.server.shutdown)
        host, port = self.server.server_address
        self.endpoint = f"http://{host}:{port}"
        self.policy = ModelPolicy.from_document(POLICY)

    def client(self, password=None):
        return OpenNotebookClient(
            self.endpoint,
            password or self.state.password,
            total_seconds=10,
        )


class NotebookModelsHttpTests(_ServerTestCase):
    def test_plan_apply_verify_through_pinned_api_shapes(self):
        planned = plan_policy(self.policy, self.client(), "a" * 64)
        self.assertEqual(planned["result"], "CHANGE_REQUIRED")
        self.assertTrue(all(row[0] == "GET" for row in self.state.requests))

        applied = apply_policy(
            self.policy,
            self.client(),
            "a" * 64,
            owned_isolated=True,
        )
        self.assertEqual(applied["result"], "PASS")
        self.assertEqual(self.state.defaults["default_tools_model"], "model:preserved")
        self.assertNotIn(self.state.password, json.dumps(applied))
        self.assertEqual(
            verify_policy(self.policy, self.client(), "a" * 64)["result"], "PASS"
        )

    def test_wrong_password_redirect_and_large_response_are_value_free_errors(self):
        for prepare in (
            lambda: self.client("wrong-password"),
            self._redirecting_client,
            self._large_client,
        ):
            with self.subTest(prepare=prepare), self.assertRaises(ApiError) as raised:
                plan_policy(self.policy, prepare(), "b" * 64)
            self.assertNotIn("private fixture detail", str(raised.exception))
            self.state.redirect = False
            self.state.large = False

    def test_http_errors_preserve_only_status_for_policy_decisions(self):
        with self.assertRaises(ApiError) as auth:
            self.client("wrong-password").get("/api/models")
        self.assertEqual(auth.exception.code, "api_http_error")
        self.assertEqual(auth.exception.status, 401)
        self.assertEqual(str(auth.exception), "api_http_error")
        self.assertNotIn("private fixture detail", repr(auth.exception))

        with self.assertRaises(ApiError) as missing_scope:
            self.client().post(
                "/api/search",
                {"notebook_id": "notebook:missing", "query": "scope"},
            )
        self.assertEqual(missing_scope.exception.status, 404)

    def test_duplicate_json_response_members_are_rejected(self):
        self.state.duplicate_response = True
        with self.assertRaisesRegex(ApiError, "api_response_invalid"):
            self.client().get("/api/models")

    def _redirecting_client(self):
        self.state.redirect = True
        return self.client()

    def _large_client(self):
        self.state.large = True
        return self.client()

    def test_external_userinfo_path_query_and_fragment_endpoints_are_rejected(self):
        endpoints = (
            "https://example.com",
            "http://user@127.0.0.1:5055",
            "http://127.0.0.1:5055/api",
            "http://127.0.0.1:5055?query=yes",
            "http://127.0.0.1:5055#fragment",
        )
        for endpoint in endpoints:
            with self.subTest(endpoint=endpoint), self.assertRaises(PolicyError):
                OpenNotebookClient(endpoint, "synthetic", total_seconds=10)

    def test_non_ascii_control_and_non_string_request_paths_are_rejected(self):
        client = self.client()
        for path in ("/api/modèles", "/api/models\n", None):
            with (
                self.subTest(path=path),
                self.assertRaisesRegex(ApiError, "api_request_refused"),
            ):
                client.get(path)

    def test_client_disables_environment_proxies_and_rejects_invalid_budgets(self):
        with patch(
            "scripts.lib.ops._notebook_models_http.urllib.request.build_opener"
        ) as build_opener:
            build_opener.return_value = object()
            OpenNotebookClient(self.endpoint, "synthetic", total_seconds=10)
        handlers = build_opener.call_args.args
        self.assertTrue(
            any(isinstance(item, urllib.request.ProxyHandler) for item in handlers)
        )
        proxy = next(
            item for item in handlers if isinstance(item, urllib.request.ProxyHandler)
        )
        self.assertEqual(proxy.proxies, {})

        for endpoint, budget in (
            (None, 10),
            (self.endpoint, True),
            (self.endpoint, float("nan")),
        ):
            with (
                self.subTest(endpoint=endpoint, budget=budget),
                self.assertRaises(PolicyError),
            ):
                OpenNotebookClient(endpoint, "synthetic", total_seconds=budget)

    def test_drip_response_cannot_outlive_the_total_budget(self):
        class Headers:
            @staticmethod
            def get_content_type():
                return "application/json"

        class DripResponse:
            status = 200
            headers = Headers()

            def __init__(self, clock):
                self.clock = clock

            def __enter__(self):
                return self

            def __exit__(self, *_args):
                return False

            def read(self, _limit):
                self.clock.now += 0.6
                return b" "

        class Clock:
            now = 0.0

            def __call__(self):
                return self.now

        class Opener:
            def __init__(self, clock):
                self.clock = clock

            def open(self, _request, timeout):
                self.assert_timeout = timeout
                return DripResponse(self.clock)

        clock = Clock()
        client = OpenNotebookClient(
            self.endpoint,
            "synthetic",
            total_seconds=1,
            clock=clock,
            opener=Opener(clock),
        )
        with self.assertRaisesRegex(ApiError, "api_budget_exhausted"):
            client.get("/api/models")


class NotebookModelsCliTests(_ServerTestCase):
    def setUp(self):
        super().setUp()
        self.tmp = tempfile.TemporaryDirectory(prefix="p03 notebook cli ")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.policy_file = self.root / "policy.json"
        self.policy_file.write_bytes(FIXTURE_POLICY.read_bytes())
        self.password_file = self.root / "password"
        self.password_file.write_text(self.state.password + "\n")
        self.password_file.chmod(0o600)
        self.receipt = self.root / "receipt.json"

    def run_cli(self, command, *extra):
        return subprocess.run(
            [
                sys.executable,
                str(CLI),
                command,
                "--endpoint",
                self.endpoint,
                "--policy",
                str(self.policy_file),
                "--password-file",
                str(self.password_file),
                *extra,
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
            env={"PATH": os.environ.get("PATH", "")},
        )

    def test_plan_apply_verify_and_atomic_receipt(self):
        planned = self.run_cli("plan", "--receipt", str(self.receipt))
        self.assertEqual(planned.returncode, 0, planned.stderr)
        self.assertEqual(json.loads(planned.stdout)["result"], "CHANGE_REQUIRED")
        self.assertEqual(json.loads(self.receipt.read_text())["mode"], "plan")

        refused = self.run_cli("apply", "--receipt", str(self.receipt))
        self.assertEqual(refused.returncode, 2)
        self.assertFalse(any(row[0] == "POST" for row in self.state.requests))

        applied = self.run_cli(
            "apply", "--owned-isolated", "--receipt", str(self.receipt)
        )
        self.assertEqual(applied.returncode, 0, applied.stderr)
        self.assertEqual(json.loads(applied.stdout)["result"], "PASS")
        self.assertEqual(json.loads(self.receipt.read_text())["mode"], "apply")

        verified = self.run_cli("verify", "--receipt", str(self.receipt))
        self.assertEqual(verified.returncode, 0, verified.stderr)
        self.assertEqual(json.loads(verified.stdout)["result"], "PASS")
        combined = planned.stdout + applied.stdout + verified.stdout
        self.assertNotIn(self.state.password, combined)

    def test_insecure_password_bad_arguments_and_api_errors_are_sanitized(self):
        self.password_file.chmod(0o644)
        failed = self.run_cli("plan", "--receipt", str(self.receipt))
        self.assertEqual(failed.returncode, 2)
        self.assertNotIn(self.state.password, failed.stderr)
        self.password_file.chmod(0o600)
        self.password_file.write_text("wrong-password\n")
        failed = self.run_cli("plan", "--receipt", str(self.receipt))
        self.assertEqual(failed.returncode, 2)
        self.assertNotIn("private fixture detail", failed.stderr)
        bad = self.run_cli("plan", "--SENSITIVE-VALUE")
        self.assertEqual(bad.returncode, 2)
        self.assertNotIn("SENSITIVE-VALUE", bad.stderr)

    def test_cli_main_cancellation_and_fixed_failure_do_not_leak_values(self):
        spec = importlib.util.spec_from_file_location("p03_notebook_models_cli", CLI)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        arguments = [
            "plan",
            "--endpoint",
            self.endpoint,
            "--policy",
            str(self.policy_file),
            "--password-file",
            str(self.password_file),
            "--receipt",
            str(self.receipt),
        ]
        stdout = io.StringIO()
        stderr = io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            self.assertEqual(module.main(arguments), 0)
            with patch.object(module, "load_policy", side_effect=KeyboardInterrupt):
                self.assertEqual(module.main(arguments), 130)
            with patch.object(
                module,
                "read_password_file",
                side_effect=PolicyError("PRIVATE_DETAIL"),
            ):
                self.assertEqual(module.main(arguments), 2)
        self.assertNotIn("PRIVATE_DETAIL", stdout.getvalue() + stderr.getvalue())
        self.assertNotIn(self.state.password, stdout.getvalue() + stderr.getvalue())

    def test_cli_rejects_external_endpoint_before_password_access(self):
        spec = importlib.util.spec_from_file_location("p03_notebook_models_cli", CLI)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        arguments = [
            "plan",
            "--endpoint",
            "https://external.invalid",
            "--policy",
            str(self.policy_file),
            "--password-file",
            str(self.password_file),
        ]
        with patch.object(module, "read_password_file") as password_reader:
            self.assertEqual(module.main(arguments), 2)
        password_reader.assert_not_called()


class NotebookNativeReadinessTests(unittest.TestCase):
    def test_prerequisite_census_uses_exact_inspect_and_never_pulls_or_runs(self):
        calls = []

        def run(command, **kwargs):
            calls.append((command, kwargs))
            if command[1:3] == ["context", "show"]:
                return subprocess.CompletedProcess(
                    command, 0, stdout="default\n", stderr=""
                )
            if command[1:3] == ["info", "--format"]:
                return subprocess.CompletedProcess(
                    command, 0, stdout="engine-id|28.5.1\n", stderr=""
                )
            if command[-1] == NOTEBOOK_IMAGE:
                return subprocess.CompletedProcess(
                    command, 0, stdout="sha256:x\n", stderr=""
                )
            return subprocess.CompletedProcess(
                command, 1, stdout="", stderr="Error: No such image"
            )

        readiness = inspect_cached_images(run=run)
        self.assertEqual(readiness.result, "NOT_RUN")
        self.assertEqual(readiness.missing, ("surrealdb_2_7_0",))
        image_calls = [call for call in calls if call[0][1:3] == ["image", "inspect"]]
        self.assertEqual(
            [call[0][-1] for call in image_calls], [NOTEBOOK_IMAGE, SURREALDB_IMAGE]
        )
        for command, kwargs in image_calls:
            self.assertEqual(command[:3], ["docker", "image", "inspect"])
            self.assertNotIn("pull", command)
            self.assertNotIn("run", command)
            self.assertEqual(kwargs["timeout"], 10)

    def test_nonzero_engine_permission_and_context_are_not_cache_misses(self):
        def denied(command, **_kwargs):
            return subprocess.CompletedProcess(
                command, 1, stdout="", stderr="permission denied"
            )

        self.assertEqual(
            inspect_cached_images(run=denied).blocked, ("docker_permission",)
        )

        def remote(command, **_kwargs):
            return subprocess.CompletedProcess(command, 0, stdout="remote\n", stderr="")

        self.assertEqual(
            inspect_cached_images(run=remote).blocked, ("docker_context_refused",)
        )

    def test_permission_failure_is_not_reported_as_a_cache_miss(self):
        def denied(_command, **_kwargs):
            raise PermissionError("docker socket denied")

        readiness = inspect_cached_images(run=denied)

        self.assertEqual(readiness.result, "BLOCKED")
        self.assertEqual(readiness.blocked, ("docker_permission",))
        self.assertEqual(readiness.missing, ())

    def test_engine_timeout_and_os_error_are_not_reported_as_cache_misses(self):
        failures = (
            subprocess.TimeoutExpired(["docker"], 10),
            OSError("engine unavailable"),
        )
        for failure in failures:

            def unavailable(_command, failure=failure, **_kwargs):
                raise failure

            with self.subTest(failure=type(failure).__name__):
                readiness = inspect_cached_images(run=unavailable)
                self.assertEqual(readiness.result, "BLOCKED")
                self.assertEqual(readiness.missing, ())
                self.assertEqual(readiness.blocked, ("docker_unavailable",))

    def test_native_selection_requires_exact_opt_in_without_docker_overrides(self):
        selected = {
            "P03_NOTEBOOK_NATIVE_REHEARSAL": "1",
            "P03_NOTEBOOK_NATIVE_CONTEXT": "default",
        }
        self.assertEqual(native_selection(selected), "default")
        for rejected in (
            {},
            {**selected, "P03_NOTEBOOK_NATIVE_CONTEXT": "other"},
            {**selected, "DOCKER_HOST": "tcp://external.invalid"},
        ):
            with (
                self.subTest(rejected=rejected),
                self.assertRaises(NativeSelectionError),
            ):
                native_selection(rejected)

    def test_full_lifecycle_orders_protocol_data_restart_and_matching_restore(self):
        class FakeBackend:
            def __init__(self):
                self.calls = []

            def call(self, name, result=None):
                self.calls.append(name)
                return result

            def prepare(self):
                return self.call("prepare")

            def start_primary(self):
                return self.call("start_primary")

            def verify_auth_rejection(self):
                return self.call("verify_auth_rejection")

            def register_models(self):
                return self.call("register_models")

            def verify_protocol_rejections(self):
                return self.call("verify_protocol_rejections")

            def seed_and_query(self):
                return self.call(
                    "seed_and_query",
                    {
                        "notebooks": 1,
                        "sources": 1,
                        "sessions": 1,
                        "chat_messages": 2,
                        "text_results": 1,
                        "vector_results": 1,
                        "embedding_dimensions": 768,
                    },
                )

            def interrupt_dependency_and_recover(self):
                return self.call("interrupt_dependency_and_recover")

            def restart_app_and_verify(self):
                return self.call(
                    "restart_app_and_verify",
                    {
                        "notebooks": 1,
                        "sources": 1,
                        "sessions": 1,
                        "chat_messages": 2,
                        "text_results": 1,
                        "vector_results": 1,
                        "embedding_dimensions": 768,
                    },
                )

            def backup_consistent_set(self):
                return self.call(
                    "backup_consistent_set",
                    {
                        "components": (
                            "application_volume",
                            "database_volume",
                            "encryption_key",
                        )
                    },
                )

            def restore_isolated_and_verify(self, expected):
                self.calls.append(("restore_isolated_and_verify", dict(expected)))
                return dict(expected)

            def cleanup(self):
                return self.call("cleanup")

        backend = FakeBackend()
        receipt = NotebookNativeLifecycle(backend).run()

        self.assertEqual(receipt["native"], "PASS")
        self.assertEqual(receipt["embedding_dimensions"], 768)
        self.assertEqual(
            receipt["backup_components"],
            ["application_volume", "database_volume", "encryption_key"],
        )
        self.assertEqual(receipt["restore_matches_source"], True)
        self.assertEqual(
            backend.calls,
            [
                "prepare",
                "start_primary",
                "verify_auth_rejection",
                "register_models",
                "verify_protocol_rejections",
                "seed_and_query",
                "interrupt_dependency_and_recover",
                "restart_app_and_verify",
                "backup_consistent_set",
                (
                    "restore_isolated_and_verify",
                    {
                        "notebooks": 1,
                        "sources": 1,
                        "sessions": 1,
                        "chat_messages": 2,
                        "text_results": 1,
                        "vector_results": 1,
                        "embedding_dimensions": 768,
                    },
                ),
                "cleanup",
            ],
        )

    def test_restored_counts_are_measured_and_require_session_and_dimension(self):
        measured = measured_restore_counts(
            [{"id": "notebook:p03"}],
            [{"id": "source:p03"}],
            {"id": "chat_session:p03", "messages": [{}, {}]},
            session_id="chat_session:p03",
            expected_chat_tail=(),
            text_results=1,
            vector_results=1,
            embedding_dimensions=768,
        )
        self.assertEqual(measured["sessions"], 1)
        self.assertEqual(measured["embedding_dimensions"], 768)
        for session, dimension in (({}, 768), ({"messages": [{}, {}]}, 0)):
            with (
                self.subTest(session=session, dimension=dimension),
                self.assertRaises(NativeFixtureError),
            ):
                measured_restore_counts(
                    [{}],
                    [{}],
                    session,
                    session_id="chat_session:p03",
                    expected_chat_tail=(),
                    text_results=1,
                    vector_results=1,
                    embedding_dimensions=dimension,
                )

    def test_native_stack_plan_is_internal_pull_free_and_immutable(self):
        class FakeOwned:
            def __init__(self):
                self.calls = []

            def create_network(self, name):
                self.calls.append(("network", name))

            def create_volume(self, name):
                self.calls.append(("volume", name))

            def create_container(self, name, *arguments):
                self.calls.append(("container", name, arguments))

            def cleanup(self):
                self.calls.append(("cleanup",))

        runtime = DockerNotebookRuntime(sleep=lambda _seconds: None)
        owned = FakeOwned()
        runtime._owned = owned
        with tempfile.TemporaryDirectory(prefix="p03 stack ") as directory:
            runtime.root = Path(directory)
            metadata = runtime.root.stat(follow_symlinks=False)
            runtime._root_identity = (metadata.st_dev, metadata.st_ino, metadata.st_uid)
            events = runtime.root / "events"
            events.mkdir()
            (runtime.root / "ollama_protocol.py").write_text("synthetic")
            runtime._create_primitives(
                runtime.app_volume, runtime.db_volume, runtime.network
            )
            runtime._create_stack(
                "primary", runtime.app_volume, runtime.db_volume, runtime.network
            )
            runtime.cleanup()

        creates = [call for call in owned.calls if call[0] == "container"]
        self.assertEqual(len(creates), 3)
        self.assertTrue(all("--pull=never" in call[2] for call in creates))
        self.assertTrue(any(NOTEBOOK_IMAGE in call[2] for call in creates))
        self.assertTrue(any(SURREALDB_IMAGE in call[2] for call in creates))

    def test_native_cleanup_failure_is_not_reported_as_pass(self):
        class FailingOwned:
            @staticmethod
            def cleanup():
                raise NativeFixtureError("native_cleanup_incomplete")

        runtime = DockerNotebookRuntime()
        runtime._owned = FailingOwned()
        with tempfile.TemporaryDirectory(prefix="p03 cleanup ") as directory:
            runtime.root = Path(directory)
            metadata = runtime.root.stat(follow_symlinks=False)
            runtime._root_identity = (
                metadata.st_dev,
                metadata.st_ino,
                metadata.st_uid,
            )
            with self.assertRaisesRegex(
                NativeFixtureError, "native_cleanup_incomplete"
            ):
                runtime.cleanup()
            self.assertIsNone(runtime.root)

    def test_restore_rejects_tampered_backup_key_metadata_and_value(self):
        runtime = DockerNotebookRuntime()
        with tempfile.TemporaryDirectory(prefix="p03 key ") as directory:
            runtime.root = Path(directory)
            backup = runtime.root / "backup"
            backup.mkdir()
            key = backup / "encryption-key"
            key.write_text(runtime.encryption_key, encoding="utf-8")
            key.chmod(0o644)
            with self.assertRaisesRegex(
                NativeFixtureError, "backup_key_metadata_invalid"
            ):
                runtime._backup_encryption_key()
            key.chmod(0o600)
            key.write_text("synthetic-wrong-key", encoding="utf-8")
            with self.assertRaisesRegex(NativeFixtureError, "backup_key_mismatch"):
                runtime._backup_encryption_key()
