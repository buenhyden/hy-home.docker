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


class PublicSuiteModelTests(unittest.TestCase):
    def test_supply_chain_full_plan_and_explain_preserve_check_capability(self) -> None:
        root = pathlib.Path(__file__).resolve().parents[2]
        document = contract.load_contract_document(root)
        gates = contract.parse_gate_registry(document, ".github/workflow-contract.yml")
        public = contract.parse_public_gate_contract(document)
        selected = ("repository-integrity",)
        plan = runner.build_public_validation_plan(
            gates,
            contract.public_root_gate_ids(public, selected),
            public,
            selected,
            runner.ExecutionContext.LOCAL,
            profile="full",
        )
        path = pathlib.PurePosixPath("scripts/validation/check-supply-chain-policy.py")
        actual = next(item for item in plan if item.entrypoint == path)
        expected = next(
            item
            for item in gates.nodes
            if item.gate_id == "leaf.supply-chain-deterministic-policy"
        )
        self.assertEqual(("--check",), actual.argv)
        self.assertEqual(expected.argv, actual.argv)
        self.assertTrue(
            any(
                str(path) in line
                for line in runner.render_public_validation_plan(
                    plan,
                    public,
                    selected,
                    runner.ExecutionContext.LOCAL,
                    profile="full",
                )
            )
        )
        for argv in (
            (),
            ("--help",),
            ("--write",),
            ("--oci-archive-config-digest", "archive"),
        ):
            with self.subTest(argv=argv):
                changed = tuple(
                    dataclasses.replace(item, argv=argv)
                    if item.entrypoint == path
                    else item
                    for item in plan
                )
                with self.assertRaises(contract.GateContractError):
                    runner.render_public_validation_plan(
                        changed,
                        public,
                        selected,
                        runner.ExecutionContext.LOCAL,
                        profile="full",
                    )

    def test_ci_bootstraps_declared_dependencies_before_runner_import(self) -> None:
        root = pathlib.Path(__file__).resolve().parents[2]
        jobs = yaml.safe_load((root / ".github/workflows/ci-quality.yml").read_text())[
            "jobs"
        ]
        for name, job in jobs.items():
            steps = job["steps"]
            runner_index = next(
                i
                for i, step in enumerate(steps)
                if "scripts/validation/run-ci-gate.py" in step.get("run", "")
            )
            bootstrap = [
                i
                for i, step in enumerate(steps)
                if step.get("run") == contract.CI_DEPENDENCY_BOOTSTRAP
            ]
            self.assertEqual(len(bootstrap), 1, name)
            self.assertLess(bootstrap[0], runner_index)
        # No package installation: explicitly expose the already-installed site
        # dependencies to an otherwise clean interpreter, then import the runner.
        result = subprocess.run(
            [
                "python3",
                "-B",
                "-S",
                "-c",
                "import site, sys; site.main(); sys.path.insert(0, sys.argv[1]); "
                "import scripts.validation.ci_gate_runner",
                str(root),
            ],
            cwd=root,
            capture_output=True,
            text=True,
            timeout=10,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_validator_argument_rebinding_fails_loader_plan_and_explain(self) -> None:
        root = pathlib.Path(__file__).resolve().parents[2]
        document = contract.load_contract_document(root)
        gates = contract.parse_gate_registry(document, ".github/workflow-contract.yml")
        public = contract.parse_public_gate_contract(document)
        path = pathlib.PurePosixPath("scripts/validation/check-document-links.py")
        original_plan = _real_public_plan(("document-graph",), {})
        for argv in (
            ("--help",),
            ("--root", "/tmp"),
            ("--write",),
            ("--mode", "traceability"),
            (),
        ):
            with self.subTest(argv=argv):
                rebound = dataclasses.replace(
                    public,
                    validators=tuple(
                        dataclasses.replace(item, argv=argv)
                        if item.entrypoint == path
                        else item
                        for item in public.validators
                    ),
                )
                with self.assertRaises(contract.GateContractError):
                    runner.build_public_validation_plan(
                        gates,
                        contract.public_root_gate_ids(public, ("document-graph",)),
                        rebound,
                        ("document-graph",),
                        runner.ExecutionContext.LOCAL,
                    )
                plan = tuple(
                    dataclasses.replace(item, argv=argv)
                    if item.entrypoint == path
                    else item
                    for item in original_plan
                )
                with self.assertRaises(contract.GateContractError):
                    runner.render_public_validation_plan(
                        plan,
                        rebound,
                        ("document-graph",),
                        runner.ExecutionContext.LOCAL,
                    )

    def test_runner_reads_the_closed_public_suite_model(self) -> None:
        self.assertEqual(
            (
                "agent-governance",
                "document-contract",
                "document-graph",
                "document-lifecycle",
                "operations",
                "repository-integrity",
            ),
            runner.public_suite_names(),
        )

    def test_full_explain_maps_each_atomic_validator_exactly_once(self) -> None:
        public = contract.parse_public_gate_contract(
            contract.load_contract_document(ROOT)
        )
        plan = _real_public_plan(public.suite_names, {})
        lines = runner.render_public_validation_plan(
            plan,
            public,
            public.suite_names,
            runner.ExecutionContext.LOCAL,
        )
        rendered_paths = tuple(line.split("\t", 1)[1] for line in lines)
        expected_paths = tuple(
            validator.entrypoint.as_posix()
            for validator in public.validators
            if "local" in validator.contexts
        )
        self.assertCountEqual(expected_paths, rendered_paths)
        self.assertEqual(len(expected_paths), len(set(rendered_paths)))

    def test_full_plan_routes_task5_regressions_through_their_public_owner(
        self,
    ) -> None:
        expected_by_suite = {
            "agent-governance": {
                "tests.lib.agent_governance.test_agent_governance_contract",
                "tests.validation.test_provider_hook_parity",
                "tests.validation.test_provider_native_surfaces",
                "tests.validation.test_provider_surface_renderer",
                "tests.validation.test_stop_gate_deferred_paths",
            },
            "document-lifecycle": {
                "tests.validation.test_generate_llm_wiki",
                "tests.validation.test_security_automation_readiness",
                "tests.validation.test_workspace_governance_migration",
            },
            "operations": {
                "tests.validation.test_postgres_logical_upgrade_rehearsal",
                "tests.lib.supply_chain.test_grype_db_seed",
                "tests.validation.test_compose_core_readiness",
                "tests.validation.test_sample_service_delivery_rehearsal",
                "tests.lib.supply_chain.test_supply_chain_policy",
                "tests.validation.test_supply_chain_secure_output",
                "tests.validation.test_supply_chain_wrapper",
            },
            "repository-integrity": {
                "tests.lib.test_surface_ownership",
                "tests.validation.test_agentic_audit_semantic_freshness",
                "tests.validation.test_audit_criterion_contract",
                "tests.validation.test_reference_stage_repo_contract",
                "tests.validation.test_script_manifest",
                "tests.validation.test_tech_stack_version_contract",
                "tests.validation.test_validator_entrypoints",
            },
        }
        task5_modules = set().union(*expected_by_suite.values())
        for suite, expected in expected_by_suite.items():
            with self.subTest(suite=suite):
                plan = _real_public_plan((suite,), {})
                actual = {
                    module
                    for invocation in plan
                    if invocation.entrypoint == runner._INTERNAL_ADAPTER_PATH
                    and invocation.argv[:1] == ("run-unittest",)
                    and invocation.argv[-1:] == ("-v",)
                    for module in invocation.argv[1:-1]
                }
                self.assertEqual(expected, actual & task5_modules)

    def test_validator_ownership_is_derived_from_the_workflow_contract(self) -> None:
        document = contract.load_contract_document(ROOT)
        public = contract.parse_public_gate_contract(document)
        declared = document["public_gate"]["validators"]
        actual = {
            item.entrypoint.as_posix(): item.suite for item in public.validators
        }
        self.assertEqual(
            {item["entrypoint"]: item["suite"] for item in declared}, actual
        )
        self.assertEqual(len(actual), len(set(actual)))

        manifest = yaml.safe_load(
            (ROOT / "scripts/manifest.yaml").read_text(encoding="utf-8")
        )
        forbidden = {"public_suites", "execution_argv", "execution_contexts"}
        self.assertFalse(
            any(forbidden.intersection(row) for row in manifest["files"])
        )
