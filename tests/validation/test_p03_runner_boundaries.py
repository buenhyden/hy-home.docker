"""Pure boundary tests for the P03 native runner fixture."""

from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path
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
    PEER_PROBE_TARGETS,
    WRONG_TOKEN_WAIT_SECONDS,
    code_workflow,
    execution_entity_id,
    full_rehearsal_contract,
    indeterminate_error_facts,
    kernel_confinement_facts,
    native_selection,
    p03_api_script,
    peer_probe_observation,
    refusal_signal_classes,
    run_full_rehearsal,
    runner_timing_environment,
    safe_error_facts,
    safe_execution_id,
    safe_terminal_error_facts,
)
from tests.validation.test_opsflow_native_rehearsal import API_JS as OPSFLOW_API_JS

P03_API_JS = p03_api_script(OPSFLOW_API_JS)
WGET_UNRESOLVED = "wget: bad address 'n8n'\n"
WGET_REFUSED = "wget: can't connect to remote host (10.0.0.3): Connection refused\n"
BODY_SENTINEL = "synthetic-response-body-must-never-escape"


def wget_result(stderr: str, returncode: int = 1):
    return subprocess.CompletedProcess(["wget"], returncode, "", stderr)


def peer_exec(main: str = WGET_UNRESOLVED, worker: str = WGET_REFUSED):
    def exec_result(role, *args, **_kwargs):
        if role != "runner" or args[0] != "wget":
            raise AssertionError("peer probe must run wget in the runner")
        url = args[-1]
        if url.startswith("http://n8n:5678/"):
            return wget_result(main)
        if url.startswith("http://n8n-worker:5678/"):
            return wget_result(worker)
        raise AssertionError("unexpected peer target")

    return exec_result


def unit_workflow_result(workflow_id, _expected, *, wait_seconds):
    if wait_seconds != 330:
        raise AssertionError("candidate wait budget changed")
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
        raise AssertionError("the peer probe no longer runs as a Code node")
    if "recovered" in workflow_id:
        return "1", {"status": "success", "terminal": True, "recoveredResult": True}
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


def mock_rehearsal_case(test, *, registered_early=False, refusal=("http_403",)):
    """A Docker-free case whose wrong-token phase sees `refusal` on its first poll."""
    fixture = Mock()
    fixture.receipt = {}
    fixture.attempt = "unit-only"
    fixture.create_secrets.return_value = {
        "metadata_pg": ("", "metadata"),
        "valkey_server": ("", "valkey"),
        "runner": ("", "runner"),
    }
    fixture.private.return_value = "wrong"
    # No existing Docker networks, so the runner network takes 10.251.0.0/24.
    fixture.client.run.return_value = ""
    state = {"good_runner": False}

    def logs_contain(role, pattern):
        test.assertEqual(("worker", 'Registered runner "'), (role, pattern))
        return registered_early or state["good_runner"]

    fixture.logs_contain.side_effect = logs_contain
    fixture.log_classes.side_effect = lambda role, _patterns: (
        list(refusal) if role == "runner" else []
    )
    fixture.exec.side_effect = lambda _role, *_args: (
        "docker-default (enforce)\n"
        if "attr/current" in _args[-1]
        else "NoNewPrivs:\t1\nSeccomp:\t2\n"
    )
    fixture.exec_result.side_effect = peer_exec()
    fixture.wait_until.side_effect = lambda predicate, *_args: test.assertTrue(
        predicate()
    )
    case = Mock()
    case.fixture = fixture
    case.api.return_value = {"id": "owner"}
    case.import_workflow.side_effect = lambda workflow: workflow["name"]
    case.run_workflow.side_effect = unit_workflow_result
    case.start_workflow.return_value = "2"

    def start_runner(token, *_args, **_kwargs):
        state["good_runner"] = token == "runner"

    case.start_runner.side_effect = start_runner
    return case


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

    def test_runner_without_process_global_is_attributed_to_environment(self):
        # The pinned JS runner's sandbox (js-task-runner.js buildContext) has
        # no `process` global, so an env read fails before any value exists.
        facts = safe_error_facts(
            {"name": "ReferenceError", "message": "process is not defined"}
        )
        self.assertEqual("ReferenceError", facts["error_class"])
        self.assertEqual("environment_access_denied", facts["error_category"])
        facts = safe_error_facts(
            {"name": "Error", "message": "Task execution timed out after 2 seconds"}
        )
        self.assertEqual("task_timeout", facts["error_category"])

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
                "topology": full_rehearsal_contract()["topology"],
            },
            full_rehearsal_contract(),
        )
        self.assertEqual(
            "synthetic_worker_broker_application_controls", FULL_REHEARSAL_SCOPE
        )
        contract = full_rehearsal_contract()
        contract["topology"]["main"]["networks"].append("runner")
        self.assertEqual(
            ["ctl"], full_rehearsal_contract()["topology"]["main"]["networks"]
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
        case = mock_rehearsal_case(self)
        fixture = case.fixture
        with patch("tests.validation._p03_runner_native_fixture.time.sleep"):
            run_full_rehearsal(case)
        self.assertEqual("PARTIAL", fixture.receipt["native"])
        scenarios = fixture.receipt["p03_runner_scenarios"]
        self.assertEqual({"status": "NON_EQUIVALENT"}, scenarios["fixture_equivalence"])
        self.assertEqual(
            {
                "observation": "NOT_REACHABLE",
                "status": "PASS",
                "targets": {
                    "main_ui_api": "name_unresolved",
                    "worker_nonbroker": "refused",
                },
            },
            scenarios["peer_nonbroker_port"],
        )
        self.assertEqual(
            {
                "observation": "REFUSAL_OBSERVED",
                "refusal_signals": {"runner": ["http_403"], "worker": []},
                "registered": False,
                "status": "PASS",
                "wait_bound_seconds": WRONG_TOKEN_WAIT_SECONDS,
            },
            scenarios["wrong_token_registration"],
        )
        self.assertEqual(
            {
                "execution_id": "2",
                "execution_identity": "same",
                "post_stop_accepted": True,
                "status": "PASS",
                "terminal_status": "canceled",
            },
            scenarios["cancellation"],
        )
        for call in case.run_workflow.call_args_list:
            self.assertEqual(330, call.kwargs["wait_seconds"])
        self.assertEqual(330, case.await_execution.call_args.kwargs["wait_seconds"])

    def test_full_rehearsal_runs_the_worker_broker_topology_without_mailpit(self):
        case = mock_rehearsal_case(self)
        fixture = case.fixture
        with patch("tests.validation._p03_runner_native_fixture.time.sleep"):
            run_full_rehearsal(case)
        fixture.create_networks.assert_called_once_with(
            ("ctl", "runner"),
            {
                "runner": (
                    "--subnet",
                    "10.251.0.0/24",
                    "--ip-range",
                    "10.251.0.128/25",
                    "--opt",
                    "com.docker.network.bridge.gateway_mode_ipv4=isolated",
                )
            },
        )
        self.assertEqual("10.251.0.2", case.broker_ip)
        fixture.start_valkey.assert_called_once_with("valkey")
        fixture.start_mailpit.assert_not_called()
        fixture.start_n8n.assert_not_called()
        case.start_main.assert_called_once_with()
        case.start_worker.assert_called_once_with()
        roles = {call.args[0] for call in fixture.logs_contain.call_args_list}
        self.assertEqual({"worker"}, roles)
        self.assertEqual(
            {
                "main": {
                    "executions_mode": "queue",
                    "networks": ["ctl"],
                    "offload_manual_executions_to_workers": True,
                    "task_broker": False,
                },
                "worker": {
                    "broker_listen": "runner_network_fixed_address",
                    "command": "worker",
                    "networks": ["ctl", "runner"],
                    "task_broker": True,
                },
                "runner": {
                    "networks": ["runner"],
                    "task_broker_uri": "http://n8n-worker:5679",
                },
                "runner_network": {
                    "gateway_mode_ipv4": "isolated",
                    "internal": True,
                    "ipam": "free_slash24_with_upper_half_dynamic_range",
                },
                "valkey": {"networks": ["ctl"]},
                "metadata_pg": {"networks": ["ctl"]},
            },
            fixture.receipt["topology"],
        )
        self.assertEqual(
            "synthetic_worker_broker_application_controls", fixture.receipt["scope"]
        )
        differences = fixture.receipt["p03_runner_scenarios"]["fixture_differences"]
        self.assertNotIn("worker_broker_listens_on_all_interfaces", differences)
        self.assertNotIn(
            "runner_network_without_home_ipam_or_gateway_mode", differences
        )
        self.assertIn("shared_internal_ctl_network", differences)

    def test_runner_network_takes_a_free_subnet_in_home_shape(self):
        from tests.validation._p03_runner_native_fixture import (
            free_runner_subnet,
            runner_network_options,
        )

        networks = [
            {"IPAM": {"Config": [{"Subnet": "10.251.0.0/24"}]}},
            {"IPAM": {"Config": [{"Subnet": "10.251.1.0/25"}, {}]}},
            {"IPAM": {"Config": None}},
        ]
        client = Mock()
        client.run.side_effect = lambda *args: (
            "a\nb\nc\n" if args[1] == "ls" else json.dumps(networks)
        )
        subnet = free_runner_subnet(client)
        self.assertEqual("10.251.2.0/24", str(subnet))
        self.assertEqual(
            (
                "--subnet",
                "10.251.2.0/24",
                "--ip-range",
                "10.251.2.128/25",
                "--opt",
                "com.docker.network.bridge.gateway_mode_ipv4=isolated",
            ),
            runner_network_options(subnet),
        )
        networks[0] = {"IPAM": {"Config": [{"Subnet": "10.251.0.0/16"}]}}
        with self.assertRaises(RehearsalFailure):
            free_runner_subnet(client)

    def test_wrong_token_bound_outlasts_the_launcher_grant_token_retries(self):
        # retry.LimitedRetry: 60 s maximum, 5 s between attempts.
        self.assertGreater(WRONG_TOKEN_WAIT_SECONDS, 60 + 5)
        line = (
            "Failed to execute `launch` command: failed to fetch grant token for "
            "launcher: exhausted retries to fetch grant token: gave up retrying "
            "operation `grant-token-fetch` on reaching max retry time 1m0s, last "
            "error: failed to fetch grant token: request to fetch grant token "
            "received status code 403"
        )
        self.assertEqual(["http_403"], refusal_signal_classes(line))

    def test_peer_probe_classifies_network_outcomes_value_free(self):
        self.assertEqual(
            (("main_ui_api", "n8n", 5678), ("worker_nonbroker", "n8n-worker", 5678)),
            PEER_PROBE_TARGETS,
        )
        cases = (
            (wget_result(WGET_UNRESOLVED), "name_unresolved"),
            (wget_result(WGET_REFUSED), "refused"),
            (wget_result("wget: download timed out\n"), "timed_out"),
            (
                wget_result("wget: can't connect to remote host: No route to host\n"),
                "unreachable",
            ),
            (
                wget_result(f"  HTTP/1.1 200 OK\n  X-Body: {BODY_SENTINEL}\n", 0),
                "reachable",
            ),
            (
                wget_result(
                    "wget: server returned error: HTTP/1.1 404 Not Found "
                    + BODY_SENTINEL
                ),
                "reachable",
            ),
            (wget_result("sh: wget: not found\n", 127), "unclassified"),
            (wget_result(BODY_SENTINEL, 0), "unclassified"),
        )
        for result, expected in cases:
            with self.subTest(expected=expected):
                observation = peer_probe_observation(result)
                self.assertEqual(expected, observation)
                self.assertNotIn(BODY_SENTINEL, observation)

    def test_reachable_peer_port_fails_and_keeps_the_receipt_value_free(self):
        for main, worker in (
            (f"  HTTP/1.1 200 OK\n{BODY_SENTINEL}\n", WGET_REFUSED),
            (WGET_UNRESOLVED, "wget: server returned error: HTTP/1.1 404 Not Found\n"),
        ):
            with self.subTest(main=main[:12], worker=worker[:12]):
                case = mock_rehearsal_case(self)
                case.fixture.exec_result.side_effect = peer_exec(main, worker)
                with (
                    patch("tests.validation._p03_runner_native_fixture.time.sleep"),
                    self.assertRaises(RehearsalFailure),
                ):
                    run_full_rehearsal(case)
                scenarios = case.fixture.receipt["p03_runner_scenarios"]
                peer = scenarios["peer_nonbroker_port"]
                self.assertEqual("FAIL", peer["status"])
                self.assertEqual("REACHABLE", peer["observation"])
                self.assertIn("reachable", peer["targets"].values())
                self.assertNotIn(BODY_SENTINEL, json.dumps(case.fixture.receipt))
                self.assertEqual({"status": "NOT_RUN"}, scenarios["cancellation"])

    def test_unclassified_peer_probe_is_a_residual_not_a_pass(self):
        case = mock_rehearsal_case(self)
        case.fixture.exec_result.side_effect = peer_exec(
            "sh: wget: not found\n", WGET_REFUSED
        )
        with patch("tests.validation._p03_runner_native_fixture.time.sleep"):
            run_full_rehearsal(case)
        peer = case.fixture.receipt["p03_runner_scenarios"]["peer_nonbroker_port"]
        self.assertEqual("TEST_RESIDUAL", peer["status"])
        self.assertEqual("UNCLASSIFIED", peer["observation"])

    def test_refusal_signal_classes_are_case_insensitive_and_value_free(self):
        secret = "synthetic-wrong-token"
        self.assertEqual(
            ["forbidden", "http_403", "invalid_token"],
            refusal_signal_classes(
                f"level=error msg=FORBIDDEN status 403: Invalid Token {secret}"
            ),
        )
        self.assertEqual(
            ["http_401", "unauthenticated", "unauthorized"],
            refusal_signal_classes("Unauthorized (401); request unauthenticated"),
        )
        # A timestamp or port that only embeds the status code does not count.
        self.assertEqual(
            [],
            refusal_signal_classes("2026-11-08T12:40:13.401Z listening on 14031"),
        )

    def test_wrong_token_registration_fails_the_rehearsal(self):
        case = mock_rehearsal_case(self, registered_early=True)
        with (
            patch("tests.validation._p03_runner_native_fixture.time.sleep"),
            self.assertRaises(RehearsalFailure),
        ):
            run_full_rehearsal(case)
        wrong = case.fixture.receipt["p03_runner_scenarios"]["wrong_token_registration"]
        self.assertEqual("FAIL", wrong["status"])
        self.assertIs(True, wrong["registered"])

    def test_wrong_token_without_refusal_or_registration_stays_residual(self):
        case = mock_rehearsal_case(self, refusal=())
        clock = iter(range(0, 1000, 5))
        with (
            patch("tests.validation._p03_runner_native_fixture.time.sleep"),
            patch(
                "tests.validation._p03_runner_native_fixture.time.monotonic",
                side_effect=lambda: next(clock),
            ),
        ):
            run_full_rehearsal(case)
        self.assertEqual(
            {
                "observation": "NO_REFUSAL_OR_REGISTRATION_WITHIN_BOUND",
                "refusal_signals": {"runner": [], "worker": []},
                "registered": False,
                "status": "TEST_RESIDUAL",
                "wait_bound_seconds": WRONG_TOKEN_WAIT_SECONDS,
            },
            case.fixture.receipt["p03_runner_scenarios"]["wrong_token_registration"],
        )

    def test_worker_refusal_ignores_signals_already_in_the_worker_log(self):
        case = mock_rehearsal_case(self, refusal=())
        worker_reads = iter((["http_401"], ["http_401"], ["forbidden", "http_401"]))
        case.fixture.log_classes.side_effect = lambda role, _patterns: (
            next(worker_reads) if role == "worker" else []
        )
        with patch("tests.validation._p03_runner_native_fixture.time.sleep"):
            run_full_rehearsal(case)
        wrong = case.fixture.receipt["p03_runner_scenarios"]["wrong_token_registration"]
        self.assertEqual("PASS", wrong["status"])
        self.assertEqual(
            {"runner": [], "worker": ["forbidden"]}, wrong["refusal_signals"]
        )

    def test_case_starts_main_worker_and_runner_in_the_home_topology(self):
        from tests.validation.test_p03_runner_isolation import (
            P03RunnerNativeRehearsal,
        )

        case = P03RunnerNativeRehearsal(
            "test_broker_focused_javascript_python_denials_timeout_and_recovery"
        )
        case.fixture = Mock()
        case.fixture.receipt = {}
        case.secrets = {
            key: ("", Path("/owned") / key)
            for key in ("metadata_n8n", "valkey_n8n", "encryption", "runner")
        }
        case.broker_ip = "10.251.7.2"
        case.start_main()
        case.start_worker()
        case.start_runner(Path("/owned/runner"))
        calls = {call.args[0]: call for call in case.fixture.create.call_args_list}
        self.assertEqual({"main", "worker", "runner"}, set(calls))
        main, worker, runner = calls["main"], calls["worker"], calls["runner"]
        self.assertEqual(("ctl",), main.args[3])
        self.assertEqual(("ctl", "runner"), worker.args[3])
        self.assertEqual(("runner",), runner.args[3])
        self.assertEqual((), main.kwargs.get("command", ()))
        self.assertEqual(("worker",), worker.kwargs["command"])
        for call in (main, worker):
            env = call.kwargs["env"]
            self.assertIn("EXECUTIONS_MODE=queue", env)
            self.assertIn("OFFLOAD_MANUAL_EXECUTIONS_TO_WORKERS=true", env)
            self.assertIn("N8N_RUNNERS_MODE=external", env)
            self.assertIn("N8N_RUNNERS_TASK_TIMEOUT=300", env)
            self.assertIn("N8N_RUNNERS_TASK_REQUEST_TIMEOUT=330", env)
            self.assertNotIn("EXECUTIONS_MODE=regular", env)
            self.assertEqual(main.kwargs["mounts"], call.kwargs["mounts"])
        self.assertFalse(
            any("N8N_RUNNERS_BROKER_LISTEN_ADDRESS" in i for i in main.kwargs["env"])
        )
        self.assertIn(
            "N8N_RUNNERS_BROKER_LISTEN_ADDRESS=10.251.7.2", worker.kwargs["env"]
        )
        self.assertEqual({"runner": "10.251.7.2"}, worker.kwargs["ips"])
        self.assertIn(
            "N8N_RUNNERS_TASK_BROKER_URI=http://n8n-worker:5679", runner.kwargs["env"]
        )
        started = [call.args[0] for call in case.fixture.start.call_args_list]
        self.assertEqual(["main", "worker", "runner"], started)

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
        fixture.client.run.return_value = ""
        fixture.create_secrets.return_value = {
            "metadata_pg": ("", "metadata"),
            "valkey_server": ("", "valkey"),
            "runner": ("", "runner"),
        }
        fixture.private.return_value = "wrong"
        # Wrong-token poll, the post-removal re-check, then the good runner.
        fixture.logs_contain.side_effect = (False, False, True)
        fixture.log_classes.side_effect = lambda role, _patterns: (
            ["forbidden"] if role == "runner" else []
        )
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
