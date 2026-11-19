from __future__ import annotations

import dataclasses
import json
import pathlib
import subprocess
import unittest
from unittest import mock

import yaml

from scripts.lib.gate import ci_gate_contract as contract
from scripts.validation import ci_gate_runner as runner

ROOT = pathlib.Path(__file__).resolve().parents[2]


class PreparedCandidatePlanTests(unittest.TestCase):
    def setUp(self) -> None:
        self.document = contract.load_contract_document(ROOT)
        self.gates = contract.parse_gate_registry(self.document, "contract")
        self.public = contract.parse_public_gate_contract(self.document)
        self.environment = {
            "GITHUB_SHA": "a" * 40,
            "PR_BASE_SHA": "b" * 40,
            "PR_HEAD_SHA": "c" * 40,
        }
        self.paths = ("docs/README.md",)
        self.suites = contract.select_public_suites(self.public, "changed", self.paths)
        self.roots = contract.public_root_gate_ids(
            self.public, self.suites, changed_paths=self.paths
        )
        self.plan = runner.build_public_validation_plan(
            self.gates,
            self.roots,
            self.public,
            self.suites,
            runner.ExecutionContext.PULL_REQUEST,
            root=ROOT,
        )

    def encoded(self):
        return runner.prepare_candidate_plan(
            ROOT,
            self.document,
            self.environment,
            self.paths,
            self.suites,
            self.roots,
            self.plan,
        )

    def restored(self, payload, digest):
        with mock.patch.object(
            runner, "collect_changed_paths", return_value=self.paths
        ):
            return runner.restore_candidate_plan(
                ROOT,
                self.document,
                self.gates,
                self.public,
                self.environment,
                payload,
                digest,
            )

    def test_shared_plan_is_consumed_without_replanning(self) -> None:
        payload, digest = self.encoded()
        with mock.patch.object(
            runner,
            "build_public_validation_plan",
            side_effect=AssertionError("replanned"),
        ):
            self.assertEqual(
                (self.paths, self.suites, self.roots, self.plan),
                self.restored(payload, digest),
            )

    def test_tampered_or_stale_plan_is_refused(self) -> None:
        payload, digest = self.encoded()
        for changed_payload, changed_digest in (
            (payload + " ", digest),
            (payload, "0" * 64),
        ):
            with (
                self.subTest(payload=changed_payload[-10:]),
                self.assertRaises(contract.GateContractError),
            ):
                self.restored(changed_payload, changed_digest)
        self.environment["GITHUB_SHA"] = "d" * 40
        with self.assertRaises(contract.GateContractError):
            self.restored(payload, digest)

    def test_self_rehashed_missing_or_forged_selection_is_refused(self) -> None:
        import hashlib

        payload, _ = self.encoded()
        for key, value in (
            ("plan", []),
            ("changed_paths", []),
            ("changed_paths", None),
            ("selected_suites", []),
            ("contract_sha256", "0" * 64),
        ):
            data = json.loads(payload)
            data[key] = value
            changed = json.dumps(data, sort_keys=True, separators=(",", ":"))
            digest = hashlib.sha256(changed.encode()).hexdigest()
            with self.subTest(key=key), self.assertRaises(contract.GateContractError):
                self.restored(changed, digest)

    def test_unknown_or_rebound_invocation_is_refused(self) -> None:
        import hashlib

        payload, _ = self.encoded()
        for key, value in (
            ("gate_id", "leaf.unknown"),
            ("argv", ["--help"]),
            ("allowed_env_keys", ["SECRET_TOKEN"]),
        ):
            data = json.loads(payload)
            data["plan"][0][key] = value
            changed = json.dumps(data, sort_keys=True, separators=(",", ":"))
            with self.subTest(key=key), self.assertRaises(contract.GateContractError):
                self.restored(changed, hashlib.sha256(changed.encode()).hexdigest())

    def test_valid_empty_diff_has_an_empty_shared_plan(self) -> None:
        self.paths = ()
        self.suites = contract.select_public_suites(self.public, "changed", self.paths)
        self.roots = contract.public_root_gate_ids(
            self.public, self.suites, changed_paths=self.paths
        )
        self.plan = runner.build_public_validation_plan(
            self.gates,
            self.roots,
            self.public,
            self.suites,
            runner.ExecutionContext.PULL_REQUEST,
            root=ROOT,
        )
        self.assertEqual(((), (), (), ()), self.restored(*self.encoded()))

    def test_missing_malformed_and_oversized_producer_output_is_refused(self) -> None:
        import hashlib

        for payload in ("", "[]", '{"plan":null}', " " * 262_145):
            with (
                self.subTest(size=len(payload)),
                self.assertRaises(contract.GateContractError),
            ):
                self.restored(payload, hashlib.sha256(payload.encode()).hexdigest())

    def test_late_manifest_and_contract_change_invalidates_plan(self) -> None:
        import tempfile

        payload, digest = self.encoded()
        self.document = {**self.document, "changed-contract": True}
        with self.assertRaises(contract.GateContractError):
            self.restored(payload, digest)
        self.document = contract.load_contract_document(ROOT)
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            (root / "scripts").mkdir()
            (root / "scripts/manifest.yaml").write_text("different manifest")
            with self.assertRaises(contract.GateContractError):
                runner.restore_candidate_plan(
                    root,
                    self.document,
                    self.gates,
                    self.public,
                    self.environment,
                    payload,
                    digest,
                )

    def test_plan_input_manifest_must_be_bounded_regular_and_not_a_symlink(
        self,
    ) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            (root / "scripts").mkdir()
            manifest = root / "scripts/manifest.yaml"
            for kind in ("missing", "symlink", "oversized"):
                if kind == "symlink":
                    manifest.symlink_to(ROOT / "scripts/manifest.yaml")
                elif kind == "oversized":
                    manifest.unlink()
                    with manifest.open("wb") as handle:
                        handle.truncate(1_048_577)
                with (
                    self.subTest(kind=kind),
                    self.assertRaises(contract.GateContractError),
                ):
                    runner.prepare_candidate_plan(
                        root,
                        self.document,
                        self.environment,
                        self.paths,
                        self.suites,
                        self.roots,
                        self.plan,
                    )

    def test_candidate_cli_reuses_plan_and_requires_producer_output(self) -> None:
        import contextlib
        import io

        payload, digest = self.encoded()
        environment = {
            **self.environment,
            "GITHUB_ACTIONS": "true",
            "GITHUB_EVENT_NAME": "pull_request",
            "CI_GATE_REQUIRE_PREPARED_PLAN": "true",
            "CI_GATE_PREPARED_PLAN": payload,
            "CI_GATE_PREPARED_PLAN_SHA256": digest,
        }
        with (
            mock.patch.object(
                runner, "_authenticated_execution_environment", return_value=environment
            ),
            mock.patch.object(runner, "validate_gate_registry", return_value=()),
            mock.patch.object(runner, "validate_rule_owners", return_value=()),
            mock.patch.object(runner, "collect_changed_paths", return_value=self.paths),
            mock.patch.object(
                runner,
                "build_public_validation_plan",
                side_effect=AssertionError("replanned"),
            ),
            contextlib.redirect_stdout(io.StringIO()) as output,
        ):
            self.assertEqual(
                0,
                runner.main(
                    ["--profile", "changed", "--job", "candidate-core", "--explain"]
                ),
            )
        self.assertIn("candidate-core", output.getvalue())
        environment.pop("CI_GATE_PREPARED_PLAN")
        with (
            mock.patch.object(
                runner, "_authenticated_execution_environment", return_value=environment
            ),
            mock.patch.object(runner, "validate_gate_registry", return_value=()),
            mock.patch.object(runner, "validate_rule_owners", return_value=()),
            contextlib.redirect_stderr(io.StringIO()) as error,
        ):
            self.assertEqual(
                1,
                runner.main(
                    [
                        "--profile",
                        "changed",
                        "--job",
                        "candidate-core",
                        "--requirements",
                    ]
                ),
            )
        self.assertIn("required producer plan is missing", error.getvalue())

    def test_routing_cli_builds_one_plan_for_all_consumers(self) -> None:
        import contextlib
        import io

        environment = {
            **self.environment,
            "GITHUB_ACTIONS": "true",
            "GITHUB_EVENT_NAME": "pull_request",
        }
        with (
            mock.patch.object(
                runner, "_authenticated_execution_environment", return_value=environment
            ),
            mock.patch.object(runner, "validate_gate_registry", return_value=()),
            mock.patch.object(runner, "validate_rule_owners", return_value=()),
            mock.patch.object(runner, "collect_changed_paths", return_value=self.paths),
            mock.patch.object(
                runner,
                "build_public_validation_plan",
                wraps=runner.build_public_validation_plan,
            ) as build,
            contextlib.redirect_stdout(io.StringIO()) as output,
        ):
            self.assertEqual(
                0,
                runner.main(
                    [
                        "--profile",
                        "changed",
                        "--job",
                        "candidate-documents",
                        "--routing",
                    ]
                ),
            )
        self.assertEqual(1, build.call_count)
        fields = dict(line.split("=", 1) for line in output.getvalue().splitlines())
        self.assertEqual(
            (self.paths, self.suites, self.roots, self.plan),
            self.restored(fields["plan"], fields["plan-sha256"]),
        )

    def test_full_link_profile_keeps_broad_capability(self) -> None:
        route = next(
            item
            for item in self.public.validators
            if item.entrypoint.name == "check-document-links.py"
        )
        self.assertEqual(
            ("--mode", "all"),
            runner._context_validator_argv(
                route, runner.ExecutionContext.LOCAL, "full"
            ),
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


class PublicSuiteModelTests(unittest.TestCase):
    def test_supply_chain_full_plan_and_explain_preserve_check_capability(self) -> None:
        root = pathlib.Path(__file__).resolve().parents[2]
        document = contract.load_contract_document(root)
        gates = contract.parse_gate_registry(document, ".github/workflow-contract.yml")
        public = contract.parse_public_gate_contract(document)
        selected = ("operations",)
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

    def test_local_profiles_and_hosted_candidate_share_the_public_runner(self) -> None:
        root = pathlib.Path(__file__).resolve().parents[2]
        document = contract.load_contract_document(root)
        public = contract.parse_public_gate_contract(document)
        self.assertEqual(("changed", "full"), public.profile_names)
        self.assertTrue(public.suite_names)
        jobs = yaml.safe_load((root / ".github/workflows/ci-quality.yml").read_text())[
            "jobs"
        ]
        self.assertEqual(
            {
                "candidate-core",
                "candidate-documents",
                "candidate-quality",
                "candidate-routing",
                "main-security",
            },
            set(jobs),
        )
        self.assertEqual(
            set(public.job_names), {"candidate-core", "candidate-documents"}
        )
        for job_id in public.job_names:
            self.assertEqual(
                2,
                sum(
                    "scripts/validation/run-ci-gate.py" in step.get("run", "")
                    for step in jobs[job_id]["steps"]
                    if isinstance(step, dict)
                ),
            )
        # The aggregate only joins results; it never runs the gate itself.
        self.assertFalse(
            any(
                "run-ci-gate.py" in step.get("run", "")
                for step in jobs["candidate-quality"]["steps"]
            )
        )
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
            check=False,
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
        public = contract.parse_public_gate_contract(
            contract.load_contract_document(ROOT)
        )
        self.assertEqual(
            (
                "profile_names",
                "suites",
                "validators",
                "changed_rules",
                "changed_root_rules",
                "changed_fallback_suites",
                "local_only_gate_ids",
                "hosted_unit_bindings",
                "default_job",
                "job_leaf_gate_ids",
            ),
            tuple(field.name for field in dataclasses.fields(public)),
        )

    def test_lifecycle_aggregate_routes_only_current_owners(self) -> None:
        registry = contract.parse_gate_registry(
            contract.load_contract_document(ROOT),
            ".github/workflow-contract.yml",
        )
        lifecycle = next(
            node
            for node in registry.nodes
            if node.gate_id == "local.document-corpus-lifecycle"
        )
        self.assertEqual(
            ("leaf.local-document-corpus-lifecycle",),
            lifecycle.children,
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
        rendered = tuple(tuple(line.split("\t")) for line in lines)
        plan_by_gate_id = {item.gate_id: item for item in plan}
        expected = tuple(
            (
                validator.suite,
                validator.entrypoint.as_posix(),
                validator.gate_id,
                json.dumps(
                    list(plan_by_gate_id[validator.gate_id].argv),
                    separators=(",", ":"),
                ),
            )
            for validator in public.validators
            if "local" in validator.contexts
        )
        self.assertTrue(all(len(row) == 4 for row in rendered))
        self.assertCountEqual(expected, rendered)
        identities = tuple((row[2], row[1], row[3]) for row in rendered)
        self.assertEqual(len(identities), len(set(identities)))

    def test_full_plan_routes_current_regressions_through_their_public_owner(
        self,
    ) -> None:
        expected_by_suite = {
            "agent-governance": {
                "tests.lib.hooks.test_tool_payload",
            },
            "operations": {
                "tests.lib.supply_chain.test_grype_db_seed",
                "tests.lib.ops.test_compose_core_readiness",
                "tests.validation.test_compose_core_readiness",
                "tests.validation.test_sample_service_delivery_rehearsal",
                "tests.lib.supply_chain.test_supply_chain_policy",
                "tests.validation.test_supply_chain_secure_output",
                "tests.validation.test_supply_chain_wrapper",
            },
            "repository-integrity": {
                "tests.lib.test_surface_ownership",
                "tests.validation.test_reference_stage_repo_contract",
                "tests.validation.test_script_manifest",
                "tests.validation.test_tech_stack_version_contract",
                "tests.validation.test_validator_entrypoints",
            },
        }
        current_modules = set().union(*expected_by_suite.values())
        environments = {
            "local": {},
            "ci-pr": {
                "GITHUB_ACTIONS": "true",
                "GITHUB_EVENT_NAME": "pull_request",
                "EVENT_NAME": "pull_request",
                "PR_BASE_SHA": "1" * 40,
                "PR_HEAD_SHA": "2" * 40,
            },
        }
        hosted_unit_suites = {"operations", "repository-integrity"}
        for context, environ in environments.items():
            for suite, expected in expected_by_suite.items():
                with self.subTest(context=context, suite=suite):
                    plan = _real_public_plan((suite,), environ)
                    actual = {
                        module
                        for invocation in plan
                        if invocation.entrypoint == runner._INTERNAL_ADAPTER_PATH
                        and invocation.argv[:1] == ("run-unittest",)
                        and invocation.argv[-1:] == ("-v",)
                        for module in invocation.argv[1:-1]
                    }
                    context_expected = (
                        expected
                        if context == "local" or suite in hosted_unit_suites
                        else set()
                    )
                    self.assertEqual(context_expected, actual & current_modules)

    def test_validator_ownership_is_derived_from_the_workflow_contract(self) -> None:
        document = contract.load_contract_document(ROOT)
        public = contract.parse_public_gate_contract(document)
        declared = document["public_gate"]["validators"]
        actual = {item.entrypoint.as_posix(): item.suite for item in public.validators}
        self.assertEqual(
            {item["entrypoint"]: item["suite"] for item in declared}, actual
        )
        self.assertEqual(len(actual), len(set(actual)))

        manifest = yaml.safe_load(
            (ROOT / "scripts/manifest.yaml").read_text(encoding="utf-8")
        )
        forbidden = {"public_suites", "execution_argv", "execution_contexts"}
        self.assertFalse(any(forbidden.intersection(row) for row in manifest["files"]))
