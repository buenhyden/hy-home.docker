from __future__ import annotations

import contextlib
import dataclasses
import io
import os
import pathlib
import select
import shutil
import signal
import subprocess
import tempfile
import threading
import traceback
import unittest
from unittest import mock

import yaml

from scripts.lib.gate import ci_gate_contract as contract
from scripts.lib.gate import ci_gate_adapters as adapters
from scripts.validation import ci_gate_runner as runner

ROOT = pathlib.Path(__file__).resolve().parents[2]


REAL_SUBPROCESS_RUN = subprocess.run
REAL_SHUTIL_RMTREE = shutil.rmtree


def _leaf(
    gate_id: str,
    *,
    entrypoint: str = "scripts/validation/leaf.py",
    argv: tuple[str, ...] = (),
) -> contract.GateNode:
    return contract.GateNode(
        gate_id=gate_id,
        kind=contract.GateKind.LEAF,
        suite_key=gate_id.removeprefix("leaf."),
        entrypoint=pathlib.PurePosixPath(entrypoint),
        argv=argv,
        cwd=pathlib.PurePosixPath("."),
        allowed_env_keys=(),
        timeout_minutes=1,
        opaque=True,
        children=(),
    )


def _setup(gate_id: str) -> contract.GateNode:
    return contract.GateNode(
        gate_id=gate_id,
        kind=contract.GateKind.SETUP,
        suite_key=None,
        entrypoint=pathlib.PurePosixPath("scripts/validation/setup.sh"),
        argv=(),
        cwd=pathlib.PurePosixPath("."),
        allowed_env_keys=(),
        timeout_minutes=1,
        opaque=False,
        children=(),
    )


def _registry() -> contract.GateRegistry:
    nodes = (
        contract.GateNode(
            gate_id="local.test",
            kind=contract.GateKind.AGGREGATE,
            suite_key=None,
            entrypoint=None,
            argv=(),
            cwd=None,
            allowed_env_keys=(),
            timeout_minutes=None,
            opaque=False,
            children=(
                "setup.repo-python-dependencies",
                "leaf.repo-contracts",
                "leaf.repo-contracts",
            ),
        ),
        _setup("setup.repo-python-dependencies"),
        _leaf("leaf.repo-contracts"),
    )
    return contract.GateRegistry(
        nodes=nodes,
        job_roots=(
            contract.JobRoot(
                ".github/workflows/ci-quality.yml",
                "validation-changed",
                "local.test",
                "required-quality",
            ),
        ),
        public_roots=("local.test",),
    )


def _invocation(
    gate_id: str,
    entrypoint: str,
    *,
    cwd: str = ".",
    allowed_env_keys: tuple[str, ...] = (),
) -> runner.GateInvocation:
    return runner.GateInvocation(
        gate_id=gate_id,
        entrypoint=pathlib.PurePosixPath(entrypoint),
        argv=(),
        cwd=pathlib.PurePosixPath(cwd),
        allowed_env_keys=allowed_env_keys,
        timeout_seconds=60,
    )


def _real_public_plan(
    selected_suites: tuple[str, ...],
    environ: dict[str, str],
) -> tuple[
    runner.GateInvocation,
    ...,
]:
    root = pathlib.Path(__file__).resolve().parents[2]
    document = contract.load_contract_document(root)
    gates = contract.parse_gate_registry(document, ".github/workflow-contract.yml")
    public = contract.parse_public_gate_contract(document)
    return runner.build_public_validation_plan(
        gates,
        contract.public_root_gate_ids(public, selected_suites),
        public,
        selected_suites,
        runner.derive_execution_context(environ),
    )


def build_public_plan(
    profile: str, context: runner.ExecutionContext
) -> tuple[runner.GateInvocation, ...]:
    root = pathlib.Path(__file__).resolve().parents[2]
    document = contract.load_contract_document(root)
    gates = contract.parse_gate_registry(document, ".github/workflow-contract.yml")
    public = contract.parse_public_gate_contract(document)
    selected = contract.select_public_suites(public, profile, ())
    return runner.build_public_validation_plan(
        gates,
        contract.public_root_gate_ids(public, selected),
        public,
        selected,
        context,
        profile=profile,
    )


def _rebind_diff_gate(
    gates: contract.GateRegistry,
    entrypoint: pathlib.PurePosixPath,
    argv: tuple[str, ...] = (),
) -> contract.GateRegistry:
    return dataclasses.replace(
        gates,
        nodes=tuple(
            dataclasses.replace(node, entrypoint=entrypoint, argv=argv)
            if node.gate_id == "leaf.local-diff-hygiene"
            else node
            for node in gates.nodes
        ),
    )


class CiGateRunnerContractTests(unittest.TestCase):
    def test_every_public_plan_has_unique_canonical_invocations(self) -> None:
        cases = (
            ("changed", runner.ExecutionContext.LOCAL),
            ("changed", runner.ExecutionContext.PULL_REQUEST),
            ("full", runner.ExecutionContext.LOCAL),
            ("full", runner.ExecutionContext.PUSH),
            ("full", runner.ExecutionContext.WORKFLOW_DISPATCH),
        )
        for profile, context in cases:
            with self.subTest(profile=profile, context=context):
                plan = build_public_plan(profile, context)
                keys = [
                    runner.canonical_invocation_key(
                        ROOT, item, profile=profile, context=context
                    )
                    for item in plan
                ]
                self.assertEqual(len(keys), len(set(keys)))

    def test_required_runner_interfaces_are_exact(self) -> None:
        self.assertEqual(
            (
                "gate_id",
                "entrypoint",
                "argv",
                "cwd",
                "allowed_env_keys",
                "timeout_seconds",
            ),
            tuple(field.name for field in dataclasses.fields(runner.GateInvocation)),
        )

    def test_build_plan_preserves_order_and_deduplicates_gate_ids(self) -> None:
        plan = runner.build_execution_plan(
            _registry(),
            "ci",
            None,
            True,
        )
        self.assertEqual(
            (
                "setup.repo-python-dependencies",
                "leaf.repo-contracts",
            ),
            tuple(invocation.gate_id for invocation in plan),
        )

    def test_unknown_profile_and_gate_fail_closed(self) -> None:
        with self.assertRaises(contract.GateContractError) as profile_error:
            runner.build_execution_plan(
                _registry(),
                "unknown",
                None,
                True,
            )
        self.assertEqual("ci-gate-profile-unknown", profile_error.exception.code)
        with self.assertRaises(contract.GateContractError) as gate_error:
            runner.build_execution_plan(
                _registry(),
                "ci",
                "leaf.unknown",
                False,
            )
        self.assertEqual(
            "ci-gate-selection-unreachable",
            gate_error.exception.code,
        )

    def test_fake_executor_receives_each_leaf_once_in_order(self) -> None:
        seen: list[str] = []
        plan = runner.build_execution_plan(
            _registry(),
            "ci",
            None,
            True,
        )
        result = runner.execute_execution_plan(
            pathlib.Path.cwd(),
            plan,
            environ={"PATH": "/usr/bin", "GIT_DIR": "/tmp/hostile"},
            executor=lambda invocation: seen.append(invocation.gate_id) or 0,
        )
        self.assertEqual(0, result)
        self.assertEqual(
            ["setup.repo-python-dependencies", "leaf.repo-contracts"],
            seen,
        )

    def test_nonzero_fake_child_is_propagated_and_stops_plan(self) -> None:
        seen: list[str] = []

        def execute(invocation: runner.GateInvocation) -> int:
            seen.append(invocation.gate_id)
            return 17

        self.assertEqual(
            17,
            runner.execute_execution_plan(
                pathlib.Path.cwd(),
                (
                    _invocation("leaf.first", "first.py"),
                    _invocation("leaf.second", "second.py"),
                ),
                {"PATH": "/usr/bin"},
                executor=execute,
            ),
        )
        self.assertEqual(["leaf.first"], seen)

    def test_list_and_dry_run_are_deterministic_and_value_free(self) -> None:
        plan = runner.build_execution_plan(
            _registry(),
            "ci",
            None,
            True,
        )
        rendered = runner.render_execution_plan(plan)
        self.assertEqual(rendered, runner.render_execution_plan(plan))
        self.assertEqual(
            (
                "setup.repo-python-dependencies\tscripts/validation/setup.sh",
                "leaf.repo-contracts\tscripts/validation/leaf.py",
            ),
            rendered,
        )
        self.assertNotIn("hostile-secret-value", "\n".join(rendered))

    def test_cli_rejects_obsolete_and_unknown_arguments(self) -> None:
        for arguments in (
            ["--profile", "full", "--gate", "leaf.repo-contracts"],
            ["--profile", "full", "--all"],
            ["--profile", "full", "--list"],
            ["--profile", "full", "--dry-run"],
        ):
            with self.subTest(arguments=arguments):
                stderr = io.StringIO()
                with mock.patch("sys.stderr", stderr):
                    result = runner.main(arguments)
                self.assertEqual(2, result)
                self.assertIn("ci-gate-cli-arguments", stderr.getvalue())
        stderr = io.StringIO()
        root = pathlib.Path(__file__).resolve().parents[2]
        with (
            mock.patch("sys.stderr", stderr),
            mock.patch.dict(
                os.environ, {"HYHOME_CI_GATE_ROOT": str(root)}, clear=False
            ),
        ):
            self.assertEqual(1, runner.main(["--profile", "local-harness"]))
        self.assertIn("ci-gate-profile-unknown", stderr.getvalue())

    def test_full_explain_is_deterministic_and_does_not_execute(self) -> None:
        root = pathlib.Path(__file__).resolve().parents[2]
        public = contract.parse_public_gate_contract(
            contract.load_contract_document(ROOT)
        )
        plan = _real_public_plan(public.suite_names, {})
        expected = runner.render_public_validation_plan(
            plan,
            public,
            public.suite_names,
            runner.ExecutionContext.LOCAL,
        )
        with (
            mock.patch.object(runner, "execute_execution_plan") as execute,
            mock.patch("sys.stdout", new_callable=io.StringIO) as stdout,
            mock.patch.dict(
                os.environ, {"HYHOME_CI_GATE_ROOT": str(root)}, clear=False
            ),
        ):
            self.assertEqual(0, runner.main(["--profile", "full", "--explain"]))
        execute.assert_not_called()
        self.assertEqual(expected, tuple(stdout.getvalue().splitlines()))

    def test_standalone_validator_explain_and_fake_execution_have_exact_parity(
        self,
    ) -> None:
        root = pathlib.Path(__file__).resolve().parents[2]
        suites = contract.parse_public_gate_contract(
            contract.load_contract_document(ROOT)
        )
        selected = ("agent-governance",)
        plan = _real_public_plan(selected, {})
        explained = runner.render_public_validation_plan(
            plan, suites, selected, runner.ExecutionContext.LOCAL
        )
        explained_paths = tuple(line.split("\t", 1)[1] for line in explained)
        executed: list[pathlib.PurePosixPath] = []
        result = runner.execute_execution_plan(
            root,
            plan,
            {"PATH": os.defpath},
            executor=lambda invocation: executed.append(invocation.entrypoint) or 0,
        )
        validator_paths = {
            item.entrypoint
            for item in suites.validators
            if item.suite in selected and "local" in item.contexts
        }
        executed_validators = tuple(
            path.as_posix() for path in executed if path in validator_paths
        )
        self.assertEqual(0, result)
        self.assertEqual(explained_paths, executed_validators)
        self.assertEqual(
            1,
            executed_validators.count(
                "scripts/validation/check-agent-governance-contract.py"
            ),
        )

    def test_public_validator_missing_or_duplicate_invocation_fails_closed(
        self,
    ) -> None:
        suites = contract.parse_public_gate_contract(
            contract.load_contract_document(ROOT)
        )
        selected = suites.suite_names
        plan = _real_public_plan(selected, {})
        validator_path = next(
            item.entrypoint
            for item in suites.validators
            if "local" in item.contexts
        )
        invocation = next(item for item in plan if item.entrypoint == validator_path)
        mutations = (
            tuple(item for item in plan if item is not invocation),
            (*plan, invocation),
        )
        for mutated in mutations:
            with (
                self.subTest(size=len(mutated)),
                self.assertRaises(contract.GateContractError) as raised,
            ):
                runner.validate_public_execution_parity(
                    suites,
                    selected,
                    mutated,
                    runner.ExecutionContext.LOCAL,
                )
            self.assertEqual("ci-gate-public-execution-parity", raised.exception.code)
        duplicate_ownership = dataclasses.replace(
            suites,
            validators=(*suites.validators, suites.validators[0]),
        )
        with self.assertRaises(contract.GateContractError) as raised:
            runner.validate_public_execution_parity(
                duplicate_ownership,
                selected,
                plan,
                runner.ExecutionContext.LOCAL,
            )
        self.assertEqual("ci-gate-public-execution-parity", raised.exception.code)

    def test_real_execution_contexts_filter_only_their_admitted_leaves(self) -> None:
        root = pathlib.Path(__file__).resolve().parents[2]
        document = contract.load_contract_document(root)
        public = contract.parse_public_gate_contract(document)
        suites = public
        changed = contract.select_public_suites(
            public, "changed", ("scripts/validation/example.py",)
        )
        full = contract.select_public_suites(public, "full", ())
        contexts = {
            "local-changed": (changed, {}),
            "local-full": (full, {}),
            "pull_request": (
                changed,
                {
                    "CI": "true",
                    "GITHUB_ACTIONS": "true",
                    "EVENT_NAME": "pull_request",
                    "PR_BASE_SHA": "a" * 40,
                    "PR_TITLE": "Task 12",
                    "HEAD_REF": "task-12",
                },
            ),
            "push": (
                full,
                {
                    "CI": "true",
                    "GITHUB_ACTIONS": "true",
                    "EVENT_NAME": "push",
                    "PUSH_BEFORE_SHA": "b" * 40,
                },
            ),
            "initial_push": (
                full,
                {
                    "GITHUB_ACTIONS": "true",
                    "EVENT_NAME": "push",
                    "PUSH_BEFORE_SHA": "0" * 40,
                },
            ),
            "workflow_dispatch": (
                full,
                {
                    "CI": "true",
                    "GITHUB_ACTIONS": "true",
                    "EVENT_NAME": "workflow_dispatch",
                },
            ),
        }
        plans = {
            name: _real_public_plan(selected, environ)
            for name, (selected, environ) in contexts.items()
        }
        for name, (selected, environ) in contexts.items():
            context = runner.derive_execution_context(environ)
            explained = runner.render_public_validation_plan(
                plans[name], suites, selected, context
            )
            executed: list[pathlib.PurePosixPath] = []
            self.assertEqual(
                0,
                runner.execute_execution_plan(
                    root,
                    plans[name],
                    {"PATH": os.defpath},
                    executor=lambda invocation: (
                        executed.append(invocation.entrypoint) or 0
                    ),
                ),
            )
            explained_paths = tuple(line.split("\t", 1)[1] for line in explained)
            # Count every validator path, not only eligible paths: otherwise a
            # hidden ineligible invocation can evade this explain comparison.
            validator_paths = {
                item.entrypoint
                for item in suites.validators
            }
            self.assertEqual(
                explained_paths,
                tuple(path.as_posix() for path in executed if path in validator_paths),
            )
        gates = contract.parse_gate_registry(document, ".github/workflow-contract.yml")
        for name in ("local-changed", "local-full"):
            gate_ids = {item.gate_id for item in plans[name]}
            with self.subTest(context=name):
                self.assertFalse(any(item.startswith("setup.") for item in gate_ids))
                self.assertFalse(gate_ids & runner._LOCAL_EXCLUDED_GATE_IDS)
                self.assertNotIn(
                    pathlib.PurePosixPath("scripts/hardening/check-all-hardening.sh"),
                    {item.entrypoint for item in plans[name]},
                )
        self.assertIn(
            "leaf.git-flow-contract",
            {item.gate_id for item in plans["pull_request"]},
        )
        for name in ("push", "initial_push", "workflow_dispatch"):
            self.assertNotIn(
                "leaf.git-flow-contract",
                {item.gate_id for item in plans[name]},
            )

    def test_local_full_plan_excludes_ci_only_hardening(self) -> None:
        public = contract.parse_public_gate_contract(
            contract.load_contract_document(ROOT)
        )
        plan = _real_public_plan(public.suite_names, {})
        self.assertNotIn(
            pathlib.PurePosixPath("scripts/hardening/check-all-hardening.sh"),
            {item.entrypoint for item in plan},
        )

    def test_base_plan_rejects_runtime_validator_rebind(self) -> None:
        root = pathlib.Path(__file__).resolve().parents[2]
        document = contract.load_contract_document(root)
        gates = contract.parse_gate_registry(document, ".github/workflow-contract.yml")
        public = contract.parse_public_gate_contract(document)
        public_paths = {item.entrypoint for item in public.validators}
        manifest = yaml.safe_load(
            (root / "scripts/manifest.yaml").read_text(encoding="utf-8")
        )
        manual_paths = tuple(
            pathlib.PurePosixPath(row["path"])
            for row in manifest["files"]
            if row.get("kind") == "validator"
            and pathlib.PurePosixPath(row["path"]) not in public_paths
        )
        self.assertTrue(manual_paths)
        forbidden_paths = (
            *manual_paths,
            pathlib.PurePosixPath(
                "scripts/operations/rehearse-sample-service-delivery.sh"
            ),
            pathlib.PurePosixPath("scripts/validation/run-ci-gate.py"),
            pathlib.PurePosixPath("scripts/validation/run-ci-precommit.sh"),
            pathlib.PurePosixPath(
                "scripts/validation/run-agent-precommit-all-files.sh"
            ),
        )
        # These exact pairs are registered internal gate invocations rather than
        # validator rebinds, so the parity check admits them by design. Every
        # other (path, argv) combination below must still be rejected, which is
        # what keeps `run-ci-precommit.sh` from being reachable with arguments.
        admitted_pairs = {
            (runner._INTERNAL_ADAPTER_PATH, ("check-diff-hygiene",)),
            (pathlib.PurePosixPath("scripts/validation/run-ci-precommit.sh"), ()),
        }
        self.assertTrue(
            admitted_pairs.issubset(
                {
                    (path, argv)
                    for path in forbidden_paths
                    for argv in ((), ("check-diff-hygiene",))
                }
                | {(runner._INTERNAL_ADAPTER_PATH, ("check-diff-hygiene",))}
            )
        )
        for context in runner.ExecutionContext:
            for path in forbidden_paths:
                for argv in ((), ("check-diff-hygiene",)):
                    if (path, argv) in admitted_pairs:
                        continue
                    with self.subTest(context=context, path=path, argv=argv):
                        with self.assertRaises(contract.GateContractError) as raised:
                            runner.build_public_validation_plan(
                                _rebind_diff_gate(gates, path, argv),
                                contract.public_root_gate_ids(
                                    public, public.suite_names
                                ),
                                public,
                                public.suite_names,
                                context,
                            )
                        self.assertEqual(
                            "ci-gate-public-execution-parity", raised.exception.code
                        )

    def test_internal_adapters_require_exact_argv_and_context(self) -> None:
        root = pathlib.Path(__file__).resolve().parents[2]
        document = contract.load_contract_document(root)
        gates = contract.parse_gate_registry(document, ".github/workflow-contract.yml")
        public = contract.parse_public_gate_contract(document)
        roots = contract.public_root_gate_ids(public, public.suite_names)
        for context, argv in (
            (runner.ExecutionContext.LOCAL, ("check-diff-hygiene", "--write")),
            (runner.ExecutionContext.LOCAL, ("run-unittest", "tests.lib.ops", "-v")),
            (runner.ExecutionContext.LOCAL, ("run-unittest", "-v")),
            (runner.ExecutionContext.LOCAL, ("run-zizmor-sarif",)),
            (runner.ExecutionContext.LOCAL, ("install-playwright",)),
            (runner.ExecutionContext.PUSH, ("check-git-flow",)),
            (runner.ExecutionContext.WORKFLOW_DISPATCH, ("verify-metadata-base",)),
            (runner.ExecutionContext.PULL_REQUEST, ("publish-qa-recommendations",)),
        ):
            with self.subTest(context=context, argv=argv):
                with self.assertRaises(contract.GateContractError) as raised:
                    runner.build_public_validation_plan(
                        _rebind_diff_gate(gates, runner._INTERNAL_ADAPTER_PATH, argv),
                        roots,
                        public,
                        public.suite_names,
                        context,
                    )
                self.assertEqual(
                    "ci-gate-public-execution-parity", raised.exception.code
                )
        duplicate_invocations = (
            (runner.ExecutionContext.PULL_REQUEST, ("check-git-flow",)),
            (runner.ExecutionContext.PUSH, ("run-zizmor-sarif",)),
            (runner.ExecutionContext.WORKFLOW_DISPATCH, ("install-playwright",)),
        )
        for context, argv in duplicate_invocations:
            with self.subTest(context=context, argv=argv):
                with self.assertRaises(contract.GateContractError) as raised:
                    runner.build_public_validation_plan(
                        _rebind_diff_gate(
                            gates, runner._INTERNAL_ADAPTER_PATH, argv
                        ),
                        roots,
                        public,
                        public.suite_names,
                        context,
                    )
                self.assertEqual(
                    "ci-gate-invocation-duplicate", raised.exception.code
                )

        unique_argv = (
            "run-unittest",
            "tests.validation.test_ci_gate_runner.UniqueAdmissionProbe",
            "-v",
        )
        plan = runner.build_public_validation_plan(
            _rebind_diff_gate(gates, runner._INTERNAL_ADAPTER_PATH, unique_argv),
            roots,
            public,
            public.suite_names,
            runner.ExecutionContext.LOCAL,
        )
        self.assertIn(
            ("leaf.local-diff-hygiene", runner._INTERNAL_ADAPTER_PATH, unique_argv),
            {(item.gate_id, item.entrypoint, item.argv) for item in plan},
        )

    def test_final_parity_and_explain_reject_hidden_or_mutated_invocations(
        self,
    ) -> None:
        suites = contract.parse_public_gate_contract(
            contract.load_contract_document(ROOT)
        )
        plan = _real_public_plan(suites.suite_names, {})
        forbidden = [
            _invocation("leaf.injected", item.entrypoint.as_posix())
            for item in suites.validators
            if "local" not in item.contexts
        ]
        forbidden.extend(
            dataclasses.replace(_invocation("leaf.injected", path), argv=argv)
            for path, argv in (
                ("scripts/validation/run-ci-gate.py", ("--profile", "full")),
                (
                    "scripts/operations/rehearse-sample-service-delivery.sh",
                    ("rehearse",),
                ),
                ("scripts/knowledge/generate-llm-wiki.py", ("--write",)),
                ("scripts/validation/report-provider-hook-parity.sh", ()),
                ("scripts/lib/gate/ci_gate_adapters.py", ("run-zizmor-sarif",)),
            )
        )
        for invocation in forbidden:
            for validate in (
                lambda candidate: runner.validate_public_execution_parity(
                    suites,
                    suites.suite_names,
                    candidate,
                    runner.ExecutionContext.LOCAL,
                ),
                lambda candidate: runner.render_public_validation_plan(
                    candidate,
                    suites,
                    suites.suite_names,
                    runner.ExecutionContext.LOCAL,
                ),
            ):
                with self.subTest(invocation=invocation, validate=validate):
                    with self.assertRaises(contract.GateContractError) as raised:
                        validate((*plan, invocation))
                    self.assertEqual(
                        "ci-gate-public-execution-parity", raised.exception.code
                    )

    def test_runtime_rebind_fails_before_cli_execution(self) -> None:
        document = contract.load_contract_document(pathlib.Path.cwd())
        for node in document["gate_nodes"]:
            if node["gate_id"] == "leaf.local-diff-hygiene":
                node["entrypoint"] = (
                    "scripts/operations/check-compose-core-readiness.sh"
                )
                node["argv"] = []
        with (
            mock.patch.object(runner, "load_contract_document", return_value=document),
            mock.patch.object(runner, "execute_execution_plan") as execute,
            mock.patch.dict(os.environ, {"PATH": os.defpath}, clear=True),
            mock.patch("sys.stderr", new_callable=io.StringIO) as stderr,
        ):
            self.assertEqual(1, runner.main(["--profile", "full"]))
        execute.assert_not_called()
        self.assertIn("ci-gate-public-execution-parity", stderr.getvalue())

    def test_malformed_execution_context_fails_closed(self) -> None:
        invalid = (
            {"EVENT_NAME": "push"},
            {"GITHUB_ACTIONS": "true", "EVENT_NAME": "schedule"},
            {
                "GITHUB_ACTIONS": "true",
                "EVENT_NAME": "pull_request",
                "PR_BASE_SHA": "a" * 40,
            },
            {"GITHUB_ACTIONS": "true", "EVENT_NAME": "push"},
            {
                "GITHUB_ACTIONS": "true",
                "EVENT_NAME": "pull_request",
                "PR_BASE_SHA": "0" * 40,
                "PR_TITLE": "Task 12",
                "HEAD_REF": "task-12",
            },
            {
                "GITHUB_ACTIONS": "true",
                "EVENT_NAME": "push",
                "PUSH_BEFORE_SHA": "invalid",
            },
            {
                "GITHUB_ACTIONS": "true",
                "EVENT_NAME": "workflow_dispatch",
                "PUSH_BEFORE_SHA": "a" * 40,
            },
        )
        for environ in invalid:
            with (
                self.subTest(environ=environ),
                self.assertRaises(contract.GateContractError) as raised,
            ):
                runner.derive_execution_context(environ)
            self.assertEqual("ci-gate-execution-context", raised.exception.code)

    def test_metadata_base_policy_reaches_the_real_adapter(self) -> None:
        root = pathlib.Path(__file__).resolve().parents[2]
        for label, environ, expected_base in (
            (
                "pull_request",
                {
                    "GITHUB_ACTIONS": "true",
                    "EVENT_NAME": "pull_request",
                    "PR_BASE_SHA": "a" * 40,
                    "PR_TITLE": "Task 12",
                    "HEAD_REF": "task-12",
                    "PATH": os.defpath,
                },
                "a" * 40,
            ),
            (
                "push",
                {
                    "GITHUB_ACTIONS": "true",
                    "EVENT_NAME": "push",
                    "PUSH_BEFORE_SHA": "b" * 40,
                    "PATH": os.defpath,
                },
                "b" * 40,
            ),
        ):
            with self.subTest(label=label):
                plan = _real_public_plan(
                    runner.public_suite_names(),
                    environ,
                )
                invocation = next(
                    item for item in plan if item.gate_id == "leaf.repo-metadata-base"
                )
                with tempfile.TemporaryDirectory(dir="/tmp") as directory:
                    child = runner._child_environment(
                        root,
                        pathlib.Path(directory),
                        invocation,
                        "python",
                        environ,
                        python_bootstrap=pathlib.Path(directory),
                    )
                self.assertEqual(expected_base, child["TEMPLATE_GATE_BASE"])
                for name in (
                    "check-document-metadata.py",
                    "check-document-corpus-lifecycle.py",
                ):
                    validator = next(
                        item for item in plan if item.entrypoint.name == name
                    )
                    with tempfile.TemporaryDirectory(dir="/tmp") as directory:
                        validator_child = runner._child_environment(
                            root,
                            pathlib.Path(directory),
                            validator,
                            "python",
                            environ,
                            python_bootstrap=pathlib.Path(directory),
                        )
                    self.assertEqual(
                        expected_base, validator_child["TEMPLATE_GATE_BASE"]
                    )
                with mock.patch.object(
                    adapters,
                    "_run_child",
                    return_value=subprocess.CompletedProcess((), 0),
                ) as run_child:
                    self.assertEqual(
                        0,
                        adapters.run_adapter(root, ("verify-metadata-base",), child),
                    )
                self.assertEqual(2, run_child.call_count)

        for label, environ in (
            (
                "initial_push",
                {
                    "GITHUB_ACTIONS": "true",
                    "EVENT_NAME": "push",
                    "PUSH_BEFORE_SHA": "0" * 40,
                },
            ),
            (
                "workflow_dispatch",
                {
                    "GITHUB_ACTIONS": "true",
                    "EVENT_NAME": "workflow_dispatch",
                },
            ),
        ):
            with self.subTest(label=label):
                plan = _real_public_plan(
                    runner.public_suite_names(),
                    environ,
                )
                self.assertNotIn(
                    "leaf.repo-metadata-base",
                    {item.gate_id for item in plan},
                )
                metadata = next(
                    item
                    for item in plan
                    if item.entrypoint
                    == pathlib.PurePosixPath(
                        "scripts/validation/check-document-metadata.py"
                    )
                )
                self.assertEqual(("--mode", "check-active"), metadata.argv)
                self.assertEqual((), metadata.allowed_env_keys)
