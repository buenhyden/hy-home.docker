import json
import shutil
import subprocess
import unittest
from pathlib import Path
from unittest import mock

from tests.validation import test_opsflow_native_rehearsal as native_rehearsal
from tests.validation._opsflow_native_evidence import (
    BODY_FETCH_FAILURE_JS,
    body_fetch_failure_facts,
)
from tests.validation._opsflow_native_ownership import (
    NODE_STATUS_PROBE_SCRIPT,
    n8n_health_probe,
    node_status_probe,
)
from tests.validation.test_opsflow_native_rehearsal import (
    API_JS,
    MAILPIT_JS,
)

NO_ERROR = {"name": "none", "code_source": "none", "code": "none"}
NODE = shutil.which("node")


class NativeHealthProbeTests(unittest.TestCase):
    @staticmethod
    def result(payload, *, returncode=0, stderr=""):
        return subprocess.CompletedProcess(
            [], returncode, json.dumps(payload) + "\n", stderr
        )

    def node_failure(self, expression):
        self.assertIsNotNone(NODE)
        return subprocess.run(
            [NODE, "-e", BODY_FETCH_FAILURE_JS + "\nopsflowExit(" + expression + ");"],
            text=True,
            capture_output=True,
            check=False,
            timeout=5,
        )

    def test_calibrated_status_client_is_shared_and_discards_bodies(self):
        execute = mock.Mock(
            return_value=self.result({"results": [{"status": 204, "error": NO_ERROR}]})
        )
        ready, facts = node_status_probe(execute, "http://mailpit:8025/readyz")
        self.assertTrue(ready)
        self.assertEqual(204, facts["results"][0]["status"])
        args = execute.call_args.args
        self.assertEqual("http://mailpit:8025/readyz", args[-1])
        script = args[2]
        self.assertEqual(NODE_STATUS_PROBE_SCRIPT, script)
        self.assertIn("require('node:http')", script)
        self.assertIn("response.destroy()", script)
        timeout_branch = script.split("const timer = setTimeout", 1)[1].split(
            "}, 2000)", 1
        )[0]
        self.assertIn("request.destroy(error)", timeout_branch)
        self.assertIn("finish({status: null, error: describe(error)})", timeout_branch)
        for forbidden in ("fetch(", ".text(", ".json(", "process.env"):
            self.assertNotIn(forbidden, script)

        fixture = Path("tests/validation/_opsflow_native_fixture.py").read_text()
        self.assertNotIn("fetch('http://127.0.0.1:5679/healthz')", fixture)
        self.assertNotIn("fetch('http://mailpit:8025/readyz')", fixture)
        self.assertGreaterEqual(fixture.count("node_status_probe("), 2)
        body_consumers = Path(
            "tests/validation/test_opsflow_native_rehearsal.py"
        ).read_text()
        self.assertIn("const r=await opsflowFetch(base+path", body_consumers)
        self.assertIn(
            "opsflowFetch('http://mailpit:8025/api/v1/messages')", body_consumers
        )

    def test_main_readiness_requires_exact_2xx_and_preserves_error_source(self):
        execute = mock.Mock(
            return_value=self.result(
                {
                    "results": [
                        {"status": 200, "error": NO_ERROR},
                        {"status": 204, "error": NO_ERROR},
                    ]
                }
            )
        )
        ready, facts = n8n_health_probe(execute)
        self.assertTrue(ready)
        self.assertEqual(200, facts["liveness_status"])
        self.assertEqual(204, facts["readiness_status"])
        self.assertEqual("none", facts["readiness_error_source"])

        execute.return_value = self.result(
            {
                "results": [
                    {"status": 200, "error": NO_ERROR},
                    {"status": 503, "error": NO_ERROR},
                ]
            }
        )
        ready, facts = n8n_health_probe(execute)
        self.assertFalse(ready)
        self.assertEqual(503, facts["readiness_status"])

        execute.return_value = self.result(
            {
                "results": [
                    {
                        "status": None,
                        "error": {
                            "name": "Error",
                            "code_source": "error_code",
                            "code": "connection_refused",
                        },
                    },
                    {
                        "status": None,
                        "error": {
                            "name": "TypeError",
                            "code_source": "cause_code",
                            "code": "connection_reset",
                        },
                    },
                ]
            }
        )
        ready, facts = n8n_health_probe(execute)
        self.assertFalse(ready)
        self.assertEqual("connection_refused", facts["liveness_error"])
        self.assertEqual("error_code", facts["liveness_error_source"])
        self.assertEqual("Error", facts["liveness_error_name"])
        self.assertEqual("connection_reset", facts["readiness_error"])
        self.assertEqual("cause_code", facts["readiness_error_source"])
        self.assertEqual("TypeError", facts["readiness_error_name"])

    def test_malformed_failed_and_unreviewed_targets_fail_closed(self):
        malformed = {
            "results": [{"status": 200, "error": NO_ERROR, "body": "withheld"}]
        }
        ready, facts = node_status_probe(
            lambda *_: self.result(malformed), "http://mailpit:8025/readyz"
        )
        self.assertFalse(ready)
        self.assertFalse(facts["output_valid"])
        self.assertNotIn("withheld", json.dumps(facts))

        duplicate = '{"results":[],"results":[]}'
        ready, facts = node_status_probe(
            lambda *_: subprocess.CompletedProcess([], 0, duplicate, ""),
            "http://mailpit:8025/readyz",
        )
        self.assertFalse(ready)
        self.assertFalse(facts["output_valid"])

        invalid_payloads = (
            {"extra": [], "results": []},
            {"results": []},
            {"results": [{"status": 200, "error": {"name": "none"}}]},
            {
                "results": [
                    {
                        "status": 200,
                        "error": {
                            "name": "Error",
                            "code_source": "error_code",
                            "code": "unreviewed",
                        },
                    }
                ]
            },
            {"results": [{"status": True, "error": NO_ERROR}]},
        )
        for payload in invalid_payloads:
            with self.subTest(payload=payload):
                ready, facts = node_status_probe(
                    lambda *_, payload=payload: self.result(payload),
                    "http://mailpit:8025/readyz",
                )
                self.assertFalse(ready)
                self.assertEqual("invalid_output", facts["probe_error"])

        ready, facts = node_status_probe(
            lambda *_: self.result({}, returncode=125, stderr="withheld"),
            "http://mailpit:8025/readyz",
        )
        self.assertFalse(ready)
        self.assertEqual("exec_failed", facts["probe_error"])
        self.assertNotIn("withheld", json.dumps(facts))

        execute = mock.Mock()
        ready, facts = node_status_probe(execute, "http://example.invalid/")
        self.assertFalse(ready)
        self.assertEqual("target_rejected", facts["probe_error"])
        execute.assert_not_called()

    def test_timeout_is_closed_and_cancellation_propagates(self):
        def timeout(*_):
            raise subprocess.TimeoutExpired(["/usr/bin/docker", "exec"], 2)

        ready, facts = node_status_probe(timeout, "http://127.0.0.1:5679/healthz")
        self.assertFalse(ready)
        self.assertTrue(facts["exec_timed_out"])
        self.assertEqual("exec_timeout", facts["probe_error"])
        ready, facts = n8n_health_probe(timeout)
        self.assertFalse(ready)
        self.assertEqual("exec_timeout", facts["liveness_error"])
        self.assertEqual("none", facts["readiness_error_source"])

        for cancellation in (KeyboardInterrupt(), SystemExit(2)):
            with self.subTest(cancellation=type(cancellation).__name__):
                with self.assertRaises(type(cancellation)):
                    node_status_probe(
                        mock.Mock(side_effect=cancellation),
                        "http://127.0.0.1:5679/healthz",
                    )

    def test_body_fetch_failure_facts_distinguish_closed_causes(self):
        cases = (
            (
                "n8n_api",
                {
                    "kind": "http_status",
                    "status": 503,
                    "error": NO_ERROR,
                },
            ),
            (
                "mailpit_capture",
                {
                    "kind": "fetch_unavailable",
                    "status": None,
                    "error": {
                        "name": "ReferenceError",
                        "code_source": "error_name",
                        "code": "other",
                    },
                },
            ),
            (
                "n8n_api",
                {
                    "kind": "transport",
                    "status": None,
                    "error": {
                        "name": "Error",
                        "code_source": "error_code",
                        "code": "connection_refused",
                    },
                },
            ),
            (
                "mailpit_capture",
                {
                    "kind": "transport",
                    "status": None,
                    "error": {
                        "name": "TypeError",
                        "code_source": "cause_code",
                        "code": "connection_reset",
                    },
                },
            ),
            (
                "n8n_api",
                {
                    "kind": "response_invalid",
                    "status": None,
                    "error": {
                        "name": "SyntaxError",
                        "code_source": "error_name",
                        "code": "other",
                    },
                },
            ),
        )
        for consumer, failure in cases:
            with self.subTest(consumer=consumer, kind=failure["kind"]):
                result = subprocess.CompletedProcess(
                    [], 1, json.dumps({"failure": failure}), ""
                )
                self.assertEqual(
                    {"consumer": consumer, **failure},
                    body_fetch_failure_facts(result, consumer),
                )

    def test_real_node_uncoded_errors_are_unknown_and_codes_are_transport(self):
        cases = (
            ("new Error()", "unknown", "none", "other"),
            ("new TypeError()", "unknown", "none", "other"),
            (
                "Object.assign(new Error(),{code:'ECONNREFUSED'})",
                "transport",
                "error_code",
                "connection_refused",
            ),
            (
                "Object.assign(new TypeError(),{cause:{code:'ECONNRESET'}})",
                "transport",
                "cause_code",
                "connection_reset",
            ),
        )
        for expression, kind, source, code in cases:
            with self.subTest(expression=expression):
                facts = body_fetch_failure_facts(
                    self.node_failure(expression), "n8n_api"
                )
                self.assertEqual(kind, facts["kind"])
                self.assertEqual(source, facts["error"]["code_source"])
                self.assertEqual(code, facts["error"]["code"])

    def test_real_node_response_invalid_names_are_closed(self):
        cases = (
            ("new SyntaxError()", "SyntaxError", "other"),
            ("new TypeError()", "TypeError", "other"),
            (
                "Object.assign(new Error(),{name:'AbortError'})",
                "AbortError",
                "timeout",
            ),
        )
        for expression, name, code in cases:
            with self.subTest(name=name):
                marked = (
                    "Object.assign(" + expression + ",{opsflowResponseInvalid:true})"
                )
                facts = body_fetch_failure_facts(
                    self.node_failure(marked), "mailpit_capture"
                )
                self.assertEqual("response_invalid", facts["kind"])
                self.assertEqual(name, facts["error"]["name"])
                self.assertEqual("error_name", facts["error"]["code_source"])
                self.assertEqual(code, facts["error"]["code"])

    def test_body_fetch_failure_output_is_strict_and_scripts_share_encoder(self):
        marker = "raw-secret-marker"
        malformed = (
            subprocess.CompletedProcess([], 1, '{"failure":{},"failure":{}}', ""),
            subprocess.CompletedProcess(
                [], 1, json.dumps({"failure": {}, "raw": marker}), ""
            ),
            subprocess.CompletedProcess([], 1, "x" * 4097, ""),
            subprocess.CompletedProcess([], 1, marker, marker),
            subprocess.CompletedProcess([], 0, "{}", ""),
        )
        for result in malformed:
            with self.subTest(size=len(result.stdout), stderr=bool(result.stderr)):
                facts = body_fetch_failure_facts(result, "n8n_api")
                self.assertEqual("invalid_output", facts["kind"])
                self.assertNotIn(marker, json.dumps(facts))
        with self.assertRaises(ValueError):
            body_fetch_failure_facts(malformed[0], "unreviewed")

        impossible = {
            "failure": {
                "kind": "fetch_unavailable",
                "status": None,
                "error": {
                    "name": "ReferenceError",
                    "code_source": "error_code",
                    "code": "other",
                },
            }
        }
        facts = body_fetch_failure_facts(
            self.result(impossible, returncode=1), "n8n_api"
        )
        self.assertEqual("invalid_output", facts["kind"])

        self.assertTrue(API_JS.startswith(BODY_FETCH_FAILURE_JS))
        self.assertTrue(MAILPIT_JS.startswith(BODY_FETCH_FAILURE_JS))
        for script in (API_JS, MAILPIT_JS):
            self.assertIn("opsflowFetch", script)
            self.assertIn("opsflowJson", script)
            self.assertIn("opsflowExit", script)
            for forbidden in ("error.message", "error.stack", "process.env"):
                self.assertNotIn(forbidden, script)
        self.assertIn("/rest/workflows/", API_JS)
        self.assertIn("/api/v1/messages", MAILPIT_JS)
        self.assertIn("opsflowRequireOk(q)", MAILPIT_JS)

    def test_body_fetch_consumers_propagate_cancellation(self):
        native_case = native_rehearsal.OpsflowN8nNativeRehearsal
        case = native_case.__new__(native_case)
        case.fixture = mock.Mock()
        case.secrets = {"owner": ("synthetic", Path("unused"))}
        case.email = "owner@opsflow.invalid"
        for method, arguments in ((case.api, ("workflows",)), (case.capture, ("run",))):
            for cancellation in (KeyboardInterrupt(), SystemExit(2)):
                with self.subTest(
                    method=method.__name__, error=type(cancellation).__name__
                ):
                    case.fixture.exec_result.side_effect = cancellation
                    with self.assertRaises(type(cancellation)):
                        method(*arguments)


if __name__ == "__main__":
    unittest.main()
