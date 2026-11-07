"""Pure boundary tests for the P03 native runner fixture."""

from __future__ import annotations

import json
import unittest
from unittest.mock import Mock, patch

from tests.validation import _p03_runner_outcomes as runner_outcomes
from tests.validation._opsflow_native_fixture import RehearsalFailure
from tests.validation._opsflow_native_inputs import N8N_ID
from tests.validation._p03_runner_native_fixture import (
    CANCEL_JS,
    CONTROLLED_EXECUTION_TIMEOUT,
    FULL_REHEARSAL_SCOPE,
    NATIVE_CONTEXT_ENV,
    NATIVE_FLAG,
    NATIVE_IMAGE_ENV,
    code_workflow,
    execution_entity_id,
    full_rehearsal_contract,
    indeterminate_error_facts,
    kernel_confinement_facts,
    native_selection,
    p03_api_script,
    run_full_rehearsal,
    runner_timing_environment,
    safe_error_facts,
    safe_execution_id,
    safe_terminal_error_facts,
)
from tests.validation.test_opsflow_native_rehearsal import API_JS as OPSFLOW_API_JS

P03_API_JS = p03_api_script(OPSFLOW_API_JS)


class RunnerNativeBoundaryTests(unittest.TestCase):
    def test_outcome_helpers_remain_explicit_legacy_reexports(self):
        self.assertIs(safe_error_facts, runner_outcomes.safe_error_facts)
        self.assertIs(
            safe_terminal_error_facts, runner_outcomes.safe_terminal_error_facts
        )
        self.assertIs(
            indeterminate_error_facts, runner_outcomes.indeterminate_error_facts
        )

    def test_native_selection_is_closed_and_rejects_context_overrides(self):
        self.assertIsNone(native_selection({}))
        self.assertEqual(
            (N8N_ID, "default"),
            native_selection(
                {
                    NATIVE_FLAG: "1",
                    NATIVE_IMAGE_ENV: N8N_ID,
                    NATIVE_CONTEXT_ENV: "default",
                }
            ),
        )
        for environment in (
            {NATIVE_FLAG: "1"},
            {
                NATIVE_FLAG: "1",
                NATIVE_IMAGE_ENV: "sha256:" + "0" * 64,
                NATIVE_CONTEXT_ENV: "default",
            },
            {NATIVE_FLAG: "1", NATIVE_IMAGE_ENV: N8N_ID, NATIVE_CONTEXT_ENV: "remote"},
            {
                NATIVE_FLAG: "1",
                NATIVE_IMAGE_ENV: N8N_ID,
                NATIVE_CONTEXT_ENV: "default",
                "DOCKER_HOST": "tcp://127.0.0.1:2375",
            },
        ):
            with (
                self.subTest(environment=environment),
                self.assertRaises(RehearsalFailure),
            ):
                native_selection(environment)

    def test_code_workflows_are_bounded_and_contain_one_code_node(self):
        cases = {
            "javaScript": "return [{json:{runner:'javascript'}}];",
            "pythonNative": "return [{'json': {'runner': 'python'}}]",
        }
        for language, code in cases.items():
            workflow = code_workflow(f"p03-{language}", language, code)
            self.assertIs(workflow["active"], False)
            self.assertEqual(
                {
                    "executionOrder": "v1",
                    "saveDataErrorExecution": "all",
                    "saveDataSuccessExecution": "all",
                    "saveManualExecutions": True,
                },
                workflow["settings"],
            )
            node = next(n for n in workflow["nodes"] if n["name"] == "Code")
            self.assertEqual(language, node["parameters"]["language"])
        controlled = code_workflow(
            "p03-timeout",
            "javaScript",
            "await new Promise(resolve=>setTimeout(resolve,15000)); return [];",
            execution_timeout=2,
        )
        self.assertEqual(2, controlled["settings"]["executionTimeout"])
        for language, code in (
            ("shell", "bad"),
            ("javaScript", ""),
            ("pythonNative", "x" * 4097),
        ):
            with self.subTest(language=language), self.assertRaises(ValueError):
                code_workflow("p03", language, code)
        for execution_timeout in (0, 31, True):
            with (
                self.subTest(execution_timeout=execution_timeout),
                self.assertRaises(ValueError),
            ):
                code_workflow(
                    "p03-timeout",
                    "javaScript",
                    "return [];",
                    execution_timeout=execution_timeout,
                )

    def test_execution_shapes_and_kernel_facts_are_value_free_and_closed(self):
        self.assertEqual("17", safe_execution_id(17))
        for value in (True, None, "", "bad/id", "x" * 129):
            with self.subTest(value=value), self.assertRaises(RehearsalFailure):
                safe_execution_id(value)
        self.assertEqual(
            {
                "no_new_privileges_enforced": True,
                "seccomp_filter_enforced": True,
                "apparmor_profile_enforced": True,
            },
            kernel_confinement_facts(
                "NoNewPrivs:\t1\nSeccomp:\t2\n", "docker-default (enforce)\n"
            ),
        )
        self.assertIn("const response=await opsflowFetch", P03_API_JS)
        self.assertIn("responseShape,dataType", P03_API_JS)
        self.assertNotIn("call('/rest/executions/'", P03_API_JS)
        with self.assertRaises(ValueError):
            p03_api_script("changed")
        self.assertEqual("17", execution_entity_id({"id": 17, "data": "x"}, "17"))
        self.assertEqual(
            "17",
            execution_entity_id({"data": {"id": 17, "data": "x"}}, "17"),
        )
        for payload in (
            {"data": "x"},
            {"id": 18, "data": "x"},
            {"id": 17, "data": {}},
        ):
            with self.subTest(payload=payload), self.assertRaises(RehearsalFailure):
                execution_entity_id(payload, "17")

    def test_error_classifier_returns_only_allowlisted_value_free_facts(self):
        sentinel = "synthetic-token-must-never-escape"
        cases = (
            (
                {
                    "name": "NodeOperationError",
                    "message": f"EvalError: Code generation from strings disallowed {sentinel}",
                    "stack": sentinel,
                },
                {
                    "error_class": "NodeOperationError",
                    "error_category": "code_generation_blocked",
                },
            ),
            (
                {"cause": {"name": "TimeoutError", "message": sentinel}},
                {
                    "error_class": "TimeoutError",
                    "error_category": "task_timeout",
                },
            ),
            (
                {"name": f"Unknown{sentinel}", "description": sentinel},
                {"error_class": "other", "error_category": "unclassified"},
            ),
            (None, {"error_class": "unknown", "error_category": "absent"}),
        )
        for payload, expected in cases:
            with self.subTest(payload=payload):
                facts = safe_error_facts(payload)
                self.assertEqual(expected, facts)
                self.assertNotIn(sentinel, json.dumps(facts, sort_keys=True))
        self.assertIn("errorClass,errorCategory", P03_API_JS)
        self.assertNotIn("errorMessage", P03_API_JS)

    def test_runner_import_denials_are_attributed_to_module_access(self):
        # Exact denial texts of the pinned runner image (n8n 2.43.6):
        # js-task-runner/errors/disallowed-module.error.js and the Python
        # runner's constants.py import messages.
        denied = (
            "Module 'node:fs' is disallowed",
            "Import of standard library module 'os' is disallowed. "
            "Allowed stdlib modules: none",
            "Import of external package 'requests' is disallowed. "
            "Allowed external packages: none",
            "Relative imports are disallowed.",
        )
        for message in denied:
            with self.subTest(message=message):
                facts = safe_error_facts({"name": "UserError", "message": message})
                self.assertEqual("module_access_denied", facts["error_category"])
        not_module = (
            "Access to name '__builtins__' is disallowed, because it can be used "
            "to bypass security restrictions.",
            "name 'open' is not defined",
        )
        for message in not_module:
            with self.subTest(message=message):
                facts = safe_error_facts({"name": "NameError", "message": message})
                self.assertNotEqual("module_access_denied", facts["error_category"])

    def test_earlier_runner_layer_denials_count_for_file_scenarios(self):
        # Owner decision 2026-11-08: the pinned Python runner removes `open`
        # from builtins and the JS runner denies `node:fs`, so a file probe is
        # refused before its read; that earlier denial is accepted.
        from tests.validation import _p03_runner_native_fixture as fixture

        facts = safe_error_facts(
            {"name": "NameError", "message": "name 'open' is not defined"}
        )
        self.assertEqual("builtin_denied", facts["error_category"])
        file_scenarios = {
            "python_fixture_secret_file_denied": "builtin_denied",
            "python_candidate_secret_file_denied": "builtin_denied",
            "python_host_path_denied": "builtin_denied",
            "python_docker_socket_denied": "builtin_denied",
            "javascript_candidate_secret_file_denied": "module_access_denied",
        }
        filesystem = {"filesystem_access_denied", "filesystem_not_mounted"}
        for name, earlier in file_scenarios.items():
            with self.subTest(scenario=name):
                self.assertEqual(
                    filesystem | {earlier},
                    set(fixture.SCENARIO_ALLOWED_CATEGORIES[name]),
                )
        self.assertEqual(
            filesystem | {"builtin_denied"}, set(fixture.ANCESTOR_ALLOWED_CATEGORIES)
        )
        for name in ("javascript_module_denied", "python_module_denied"):
            self.assertEqual(
                {"module_access_denied"},
                set(fixture.SCENARIO_ALLOWED_CATEGORIES[name]),
            )
        self.assertEqual(
            {"environment_access_denied"},
            set(fixture.SCENARIO_ALLOWED_CATEGORIES["javascript_environment_denied"]),
        )

    def test_candidate_diagnostic_timing_is_bounded(self):
        self.assertEqual(
            (
                "N8N_RUNNERS_TASK_TIMEOUT=300",
                "N8N_RUNNERS_TASK_REQUEST_TIMEOUT=330",
                "N8N_RUNNERS_GRANT_TOKEN_TTL=120",
            ),
            runner_timing_environment(300, 330),
        )
        for task_timeout, request_timeout in (
            (0, 10),
            (10, 9),
            (601, 601),
            (True, 10),
        ):
            with (
                self.subTest(
                    task_timeout=task_timeout, request_timeout=request_timeout
                ),
                self.assertRaises(ValueError),
            ):
                runner_timing_environment(task_timeout, request_timeout)

    def test_full_scope_uses_candidate_timing_and_supported_cancel_route(self):
        self.assertEqual(
            {
                "scope": FULL_REHEARSAL_SCOPE,
                "candidate_timing": {
                    "task_timeout_seconds": 300,
                    "request_timeout_seconds": 330,
                    "grant_token_ttl_seconds": 120,
                    "auto_shutdown_timeout_seconds": 0,
                },
                "controlled_workflow_timeout_seconds": CONTROLLED_EXECUTION_TIMEOUT,
            },
            full_rehearsal_contract(),
        )
        self.assertIn("/rest/executions/' + encodeURIComponent(id) + '/stop", CANCEL_JS)
        self.assertIn("method: 'POST'", CANCEL_JS)
        self.assertNotIn("executions-current", CANCEL_JS)
        self.assertNotIn("method: 'DELETE'", CANCEL_JS)

    def test_terminal_error_attribution_rejects_generic_failures(self):
        self.assertEqual(
            {
                "error_class": "NodeOperationError",
                "error_category": "module_access_denied",
                "attributed": True,
            },
            safe_terminal_error_facts(
                {
                    "status": "error",
                    "errorClass": "NodeOperationError",
                    "errorCategory": "module_access_denied",
                },
                frozenset({"module_access_denied"}),
            ),
        )
        for payload in (
            {"status": "success", "errorClass": "unknown", "errorCategory": "absent"},
            {
                "status": "error",
                "errorClass": "unknown",
                "errorCategory": "unclassified",
            },
            {"status": "error", "errorClass": "made-up", "errorCategory": "made-up"},
            {
                "status": "error",
                "errorClass": "NodeOperationError",
                "errorCategory": "task_timeout",
            },
        ):
            with self.subTest(payload=payload), self.assertRaises(RehearsalFailure):
                safe_terminal_error_facts(payload, frozenset({"module_access_denied"}))
        self.assertIn("runnerResult,recoveredResult", P03_API_JS)

    def test_full_rehearsal_orchestration_unit_does_not_claim_fixture_equivalence(self):
        fixture = Mock()
        fixture.receipt = {}
        fixture.attempt = "unit-only"
        fixture.create_secrets.return_value = {
            "metadata_pg": ("", "metadata"),
            "runner": ("", "runner"),
        }
        fixture.private.return_value = "wrong"
        fixture.logs_contain.side_effect = (False, True)
        fixture.exec.side_effect = lambda _role, *_args: (
            "docker-default (enforce)\n"
            if "attr/current" in _args[-1]
            else "NoNewPrivs:\t1\nSeccomp:\t2\n"
        )
        fixture.wait_until.side_effect = lambda predicate, *_args: self.assertTrue(
            predicate()
        )
        case = Mock()
        case.fixture = fixture
        case.api.return_value = {"id": "owner"}
        case.import_workflow.side_effect = lambda workflow: workflow["name"]

        def run_workflow(workflow_id, _expected, *, wait_seconds):
            self.assertEqual(330, wait_seconds)
            if "timeout" in workflow_id:
                return "1", {"status": "canceled", "terminal": True}
            if "ancestor environment" in workflow_id:
                return "1", {
                    "status": "error",
                    "terminal": True,
                    "errorClass": "PermissionError",
                    "errorCategory": "filesystem_access_denied",
                }
            if "peer port" in workflow_id:
                return "1", {
                    "status": "error",
                    "terminal": True,
                    "errorClass": "TypeError",
                    "errorCategory": "request_error",
                }
            if "recovered" in workflow_id:
                return "1", {
                    "status": "success",
                    "terminal": True,
                    "recoveredResult": True,
                }
            if "javascript_ok" in workflow_id or "python_ok" in workflow_id:
                return "1", {
                    "status": "success",
                    "terminal": True,
                    "runnerResult": "javascript"
                    if "javascript_ok" in workflow_id
                    else "python",
                }
            category = (
                "environment_access_denied"
                if "environment_denied" in workflow_id
                else "filesystem_not_mounted"
                if any(
                    marker in workflow_id
                    for marker in ("secret_file", "host_path", "docker_socket")
                )
                else "module_access_denied"
            )
            return "1", {
                "status": "error",
                "terminal": True,
                "errorClass": "NodeOperationError",
                "errorCategory": category,
            }

        case.run_workflow.side_effect = run_workflow
        case.start_workflow.return_value = "2"
        with patch("tests.validation._p03_runner_native_fixture.time.sleep"):
            run_full_rehearsal(case)
        self.assertEqual("PARTIAL", fixture.receipt["native"])
        self.assertEqual(
            {"status": "NON_EQUIVALENT"},
            fixture.receipt["p03_runner_scenarios"]["fixture_equivalence"],
        )
        self.assertFalse(
            fixture.receipt["p03_runner_scenarios"]["peer_nonbroker_port"]["attributed"]
        )
        self.assertEqual(
            {
                "observation": "NOT_OBSERVED_WITHIN_3S",
                "status": "TEST_RESIDUAL",
            },
            fixture.receipt["p03_runner_scenarios"]["wrong_token_registration"],
        )
        self.assertEqual(
            {
                "execution_id": "2",
                "execution_identity": "same",
                "post_stop_accepted": True,
                "status": "PASS",
                "terminal_status": "canceled",
            },
            fixture.receipt["p03_runner_scenarios"]["cancellation"],
        )
        for call in case.run_workflow.call_args_list:
            self.assertEqual(330, call.kwargs["wait_seconds"])
        self.assertEqual(330, case.await_execution.call_args.kwargs["wait_seconds"])

    def test_execution_can_remain_running_past_thirty_polls_within_candidate_budget(
        self,
    ):
        from tests.validation.test_p03_runner_isolation import (
            P03RunnerNativeRehearsal,
        )

        case = P03RunnerNativeRehearsal(
            "test_broker_focused_javascript_python_denials_timeout_and_recovery"
        )
        case.fixture = Mock()
        case.fixture.receipt = {}
        case.api = Mock(
            side_effect=[
                {"id": "17", "status": "running", "terminal": False} for _ in range(31)
            ]
            + [{"id": "17", "status": "success", "terminal": True}]
        )

        def wait_until(predicate, _message, seconds):
            self.assertEqual(330, seconds)
            for _ in range(31):
                self.assertFalse(predicate())
            self.assertTrue(predicate())

        case.fixture.wait_until.side_effect = wait_until
        terminal = case.await_execution("17", "success", wait_seconds=330)
        self.assertEqual("success", terminal["status"])
        self.assertEqual(32, case.api.call_count)

    def test_incremental_receipt_preserves_completed_stages_on_unknown_denial(self):
        fixture = Mock()
        fixture.receipt = {}
        fixture.attempt = "injected-error"
        fixture.create_secrets.return_value = {
            "metadata_pg": ("", "metadata"),
            "runner": ("", "runner"),
        }
        fixture.private.return_value = "wrong"
        fixture.logs_contain.side_effect = (False, True)
        fixture.wait_until.side_effect = lambda predicate, *_args: self.assertTrue(
            predicate()
        )
        fixture.exec.side_effect = lambda _role, *_args: (
            "docker-default (enforce)\n"
            if "attr/current" in _args[-1]
            else "NoNewPrivs:\t1\nSeccomp:\t2\n"
        )
        case = Mock()
        case.fixture = fixture
        case.api.return_value = {"id": "owner"}
        case.import_workflow.side_effect = lambda workflow: workflow["name"]
        case.run_workflow.side_effect = (
            (
                "11",
                {
                    "status": "success",
                    "terminal": True,
                    "runnerResult": "javascript",
                },
            ),
            (
                "12",
                {
                    "status": "success",
                    "terminal": True,
                    "runnerResult": "python",
                },
            ),
            (
                "13",
                {
                    "status": "error",
                    "terminal": True,
                    "errorClass": "other",
                    "errorCategory": "unclassified",
                },
            ),
        )
        with (
            patch("tests.validation._p03_runner_native_fixture.time.sleep"),
            self.assertRaises(RehearsalFailure),
        ):
            run_full_rehearsal(case)
        scenarios = fixture.receipt["p03_runner_scenarios"]
        self.assertEqual(
            {
                "execution_id": "11",
                "functional_result": "javascript",
                "status": "PASS",
                "terminal_status": "success",
            },
            scenarios["javascript_ok"],
        )
        self.assertEqual(
            {
                "execution_id": "12",
                "functional_result": "python",
                "status": "PASS",
                "terminal_status": "success",
            },
            scenarios["python_ok"],
        )
        self.assertEqual(
            {
                "attributed": False,
                "error_category": "unclassified",
                "error_class": "unknown",
                "execution_id": "13",
                "status": "FAIL",
                "terminal_status": "error",
            },
            scenarios["javascript_module_denied"],
        )
        self.assertEqual(
            {"status": "NOT_RUN"}, scenarios["javascript_environment_denied"]
        )


if __name__ == "__main__":
    unittest.main()
