from __future__ import annotations

import dataclasses
import contextlib
import copy
import importlib.util
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock


ROOT = pathlib.Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "scripts/validation/github_workflow_contract.py"
REQUIRED_CI_JOBS = frozenset(
    {
        "validation-changed",
        "validation-full",
    }
)
SUPPLY_CHAIN_SEMANTIC_COMMANDS = (
    (
        "python3 -m unittest tests.validation.test_compose_core_readiness "
        "tests.validation.test_postgres_logical_upgrade_rehearsal "
        "tests.validation.test_grype_db_seed "
        "tests.validation.test_supply_chain_policy "
        "tests.validation.test_sample_service_delivery_rehearsal -v"
    ),
    "python3 scripts/validation/check-supply-chain-policy.py --check",
    (
        "bash scripts/security/"
        "generate-supply-chain-sample-service-summary.sh --check"
    ),
)
CONTROL_PLANE_SEMANTIC_COMMANDS = (
    (
        "python3 -m unittest "
        "tests.validation.test_agent_governance_ci_routing -v"
    ),
    (
        "python3 -m unittest "
        "tests.validation.test_agent_output_eval_fixtures -v"
    ),
)


def load_contract_module():
    spec = importlib.util.spec_from_file_location(
        "github_workflow_contract_under_test",
        MODULE_PATH,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load workflow contract: {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class GithubWorkflowContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.module = load_contract_module()

    def test_storybook_shell_accepts_typed_full_route_direct_and_held(self) -> None:
        script = ROOT / "scripts/validation/check-storybook-contract.sh"
        env = {key: value for key, value in os.environ.items() if key != "PYTHONPATH"}
        env["PYTHONSAFEPATH"] = "1"
        with script.open("rb") as held:
            for path in (str(script), f"/proc/self/fd/{held.fileno()}"):
                with self.subTest(path=path):
                    result = subprocess.run(
                        ["bash", path], cwd=ROOT, env=env,
                        pass_fds=(held.fileno(),), capture_output=True,
                        text=True, check=False,
                    )
                    self.assertEqual(0, result.returncode, result.stderr)

    def test_storybook_shell_rejects_lost_routes_and_changed_quality_contracts(self) -> None:
        for case in ("full-command", "public-route", "full-child", "npm-argv", "threshold"):
            with self.subTest(case=case), self.workflow_fixture() as root:
                subprocess.run(["git", "init", "-q", str(root)], check=True)
                (root / "tests/validation").mkdir(parents=True)
                shutil.copy2(ROOT / "tests/validation/test_run_ci_precommit.sh", root / "tests/validation/test_run_ci_precommit.sh")
                subprocess.run(["git", "-C", str(root), "add", "scripts", ".github", "tests"], check=True)
                project = root / "projects/storybook/nextjs"
                project.mkdir(parents=True)
                for name in ("package.json", "vitest.config.ts"):
                    shutil.copy2(ROOT / "projects/storybook/nextjs" / name, project / name)
                command = ["bash", str(root / "scripts/validation/check-storybook-contract.sh")]
                baseline = subprocess.run(command, cwd=root, capture_output=True, text=True, check=False)
                self.assertEqual(0, baseline.returncode, baseline.stderr)
                if case == "full-command":
                    path = root / ".github/workflows/ci-quality.yml"
                    text = path.read_text(encoding="utf-8")
                    old = "python3 scripts/validation/run-ci-gate.py --profile full"
                    self.assertEqual(1, text.count(old))
                    path.write_text(text.replace(old, "true", 1), encoding="utf-8")
                elif case == "threshold":
                    path = project / "vitest.config.ts"
                    text = path.read_text(encoding="utf-8")
                    self.assertIn("statements: 90", text)
                    path.write_text(text.replace("statements: 90", "statements: 80", 1), encoding="utf-8")
                else:
                    data = self.load_contract_document(root)
                    if case == "public-route":
                        data["public_gate"]["suite_roots"]["repository-integrity"].remove("ci.storybook-coverage")
                    else:
                        node = next(node for node in data["gate_nodes"] if node["gate_id"] == (
                            "ci.validation-full" if case == "full-child" else "leaf.storybook-coverage"
                        ))
                        if case == "full-child":
                            node["children"].remove("ci.storybook-coverage")
                        else:
                            node["argv"][2] = "test"
                    self.write_contract_document(root, data)
                result = subprocess.run(command, cwd=root, capture_output=True, text=True, check=False)
                self.assertEqual(1, result.returncode, result.stderr)
                self.assertIn("FAIL:", result.stderr)

    def test_public_gate_surfaces_do_not_copy_atomic_commands(self) -> None:
        workflow = self.module.load_workflows(ROOT)
        ci = next(
            item for item in workflow if item.path == ".github/workflows/ci-quality.yml"
        )
        run_values = tuple(
            step["run"]
            for job in ci.data["jobs"].values()
            for step in job.get("steps", ())
            if isinstance(step, dict) and "run" in step
        )
        self.assertEqual(
            {
                self.module.CI_DEPENDENCY_BOOTSTRAP,
                "python3 scripts/validation/run-ci-gate.py --profile changed",
                "python3 scripts/validation/run-ci-gate.py --profile full",
            },
            set(run_values),
        )

        pre_commit = self.module._read_bounded_yaml(
            ROOT, pathlib.PurePosixPath(".pre-commit-config.yaml")
        )[1]
        local_entries = tuple(
            hook["entry"]
            for repository in pre_commit["repos"]
            if repository["repo"] == "local"
            for hook in repository["hooks"]
        )
        self.assertEqual(
            {
                "python3 scripts/validation/run-ci-gate.py --profile changed",
                "python3 scripts/validation/run-ci-gate.py --profile full",
            },
            set(local_entries),
        )

        active_surfaces = "\n".join(
            (ROOT / path).read_text(encoding="utf-8")
            for path in (
                "scripts/validation/run-local-qa-gates.sh",
                "scripts/hooks/agent-event-hook.sh",
                "scripts/hooks/post-tool-validate.sh",
                ".claude/settings.json",
            )
        )
        for retired in (
            "check-repo-contracts.sh",
            "recommend-qa-gates.sh",
            "check-document-links.py",
            "check-operations-catalog.py",
            "validate-docker-compose.sh",
        ):
            with self.subTest(retired=retired):
                self.assertNotIn(retired, active_surfaces)

    def test_required_dataclass_interfaces_are_exact(self) -> None:
        expected = {
            "WorkflowFinding": ("code", "path", "message"),
            "TriggerContract": ("events", "branches", "paths", "schedules"),
            "ActionDependency": (
                "action",
                "sha",
                "runtime",
                "manifest_url",
                "retrieved_at",
                "consumers",
                "security_disposition",
            ),
        }
        for name, fields in expected.items():
            with self.subTest(name=name):
                cls = getattr(self.module, name)
                self.assertEqual(fields, tuple(field.name for field in dataclasses.fields(cls)))

    def test_repository_workflows_match_the_exact_contract(self) -> None:
        contract = self.module.load_workflow_contract(ROOT)
        workflows = self.module.load_workflows(ROOT)
        self.assertEqual(7, len(workflows))
        self.assertEqual((), self.module.validate_workflows(ROOT, contract))

    def test_canonical_schema_v2_registry_is_complete_and_expandable(
        self,
    ) -> None:
        contract = self.module.load_workflow_contract(ROOT)
        ci = next(
            workflow
            for workflow in contract.workflows
            if workflow.path == ".github/workflows/ci-quality.yml"
        )
        self.assertEqual(REQUIRED_CI_JOBS, frozenset(ci.jobs))
        self.assertEqual(2, len(ci.jobs))
        # 84 since 2026-08-29: leaf.document-governance-library-regressions,
        # which runs the fourteen mirrored tests/lib/document_governance suites
        # that no profile executed until then.
        # 85 since 2026-08-29: leaf.compose-baseline-regressions, which carries
        # the first failing-case coverage for the two Compose baseline gates.
        # 86 since 2026-08-30: leaf.local-document-metadata-tests, the 261-test
        # metadata suite, which ran under no profile while it was red.
        self.assertEqual(86, len(contract.gate_registry.nodes))
        self.assertEqual(2, len(contract.gate_registry.job_roots))
        self.assertEqual(
            REQUIRED_CI_JOBS,
            frozenset(
                job.job_id for job in contract.gate_registry.job_roots
            ),
        )
        self.assertEqual(3, len(contract.gate_registry.profile_roots))
        self.assertEqual(
            (),
            self.module.validate_gate_registry(ROOT, contract.gate_registry),
        )
        for profile in (
            "ci",
            "local-script-backed",
            "local-harness",
            "local-all-profiles",
        ):
            with self.subTest(profile=profile):
                expanded = self.module.expand_gate_ids(
                    contract.gate_registry,
                    profile,
                    None,
                    True,
                )
                self.assertTrue(expanded)
                self.assertEqual(len(expanded), len(set(expanded)))

    def test_schema_v1_and_duplicate_command_authority_fail_closed(
        self,
    ) -> None:
        self.assertFalse(hasattr(self.module, "ExpensiveCommandOwner"))
        self.assertFalse(hasattr(self.module, "_EXPENSIVE_COMMAND_BASELINE"))
        document = json.loads(
            (ROOT / ".github/workflow-contract.yml").read_text(
                encoding="utf-8"
            )
        )
        self.assertNotIn("expensive_commands", document)
        for workflow in document["workflows"].values():
            for job in workflow["jobs"].values():
                self.assertNotIn("owner_commands", job)

        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            shutil.copytree(ROOT / ".github", root / ".github")
            path = root / ".github/workflow-contract.yml"
            document["schema_version"] = 1
            path.write_text(
                json.dumps(document, indent=2) + "\n",
                encoding="utf-8",
            )
            with self.assertRaises(self.module.WorkflowContractError) as raised:
                self.module.load_workflow_contract(root)
        self.assertEqual("ci-gate-schema-version", raised.exception.code)

    def test_registered_gate_entrypoints_are_tracked_mode_100755(self) -> None:
        contract = self.module.load_workflow_contract(ROOT)
        entrypoints = sorted(
            {
                node.entrypoint.as_posix()
                for node in contract.gate_registry.nodes
                if node.entrypoint is not None
            }
        )
        result = subprocess.run(
            [
                "git",
                "--literal-pathspecs",
                "ls-files",
                "--stage",
                "-z",
                "--",
                *entrypoints,
            ],
            cwd=ROOT,
            capture_output=True,
            check=True,
        )
        modes = {
            record.split(b"\t", 1)[1].decode("utf-8"): record.split(
                b" ", 1
            )[0].decode("ascii")
            for record in result.stdout.rstrip(b"\0").split(b"\0")
        }
        self.assertEqual(set(entrypoints), set(modes))
        self.assertEqual({"100755"}, set(modes.values()))

    def test_action_registry_and_ci_precommit_wiring_are_exact(self) -> None:
        contract = self.module.load_workflow_contract(ROOT)
        self.assertEqual(8, len(contract.actions))
        self.assertEqual(
            {"node24"},
            {action.runtime for action in contract.actions},
        )
        for action in contract.actions:
            with self.subTest(action=action.action):
                self.assertEqual("2026-07-28", action.retrieved_at)
                self.assertIn(f"/{action.sha}/", action.manifest_url)
                self.assertEqual("approved-node24", action.security_disposition)

        workflows = {
            workflow.path: workflow
            for workflow in self.module.load_workflows(ROOT)
        }
        ci_jobs = workflows[".github/workflows/ci-quality.yml"].data["jobs"]
        self.assertIsInstance(ci_jobs, dict)
        changed_steps = ci_jobs["validation-changed"]["steps"]
        full_steps = ci_jobs["validation-full"]["steps"]
        self.assertNotIn(
            "pre-commit/action",
            "\n".join(
                str(step.get("uses", ""))
                for workflow in workflows.values()
                for job in workflow.data.get("jobs", {}).values()
                for step in job.get("steps", [])
                if isinstance(step, dict)
            ),
        )
        self.assertEqual(
            "actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97",
            changed_steps[1]["uses"],
        )
        self.assertEqual(
            (self.module.CI_DEPENDENCY_BOOTSTRAP, "python3 scripts/validation/run-ci-gate.py --profile changed"),
            (changed_steps[3]["run"], changed_steps[4]["run"]),
        )
        self.assertEqual(
            (self.module.CI_DEPENDENCY_BOOTSTRAP, "python3 scripts/validation/run-ci-gate.py --profile full"),
            (full_steps[4]["run"], full_steps[5]["run"]),
        )
        self.assertEqual(
            "pre-commit==4.6.1\n",
            (ROOT / "scripts/requirements-pre-commit.txt").read_text(
                encoding="utf-8"
            ),
        )

    def test_forbidden_trigger_and_action_mutations_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            shutil.copytree(ROOT / ".github", root / ".github")
            workflow = root / ".github/workflows/ci-quality.yml"
            text = workflow.read_text(encoding="utf-8")
            text = text.replace(
                "  workflow_dispatch:\n",
                "  workflow_dispatch:\n  pull_request_target:\n",
                1,
            ).replace(
                "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1",
                "actions/checkout@main",
                1,
            )
            workflow.write_text(text, encoding="utf-8")
            findings = self.module.validate_workflows(
                root,
                self.module.load_workflow_contract(root),
            )
        codes = {finding.code for finding in findings}
        self.assertIn("workflow-trigger-forbidden", codes)
        self.assertIn("action-ref-mutable", codes)

    @staticmethod
    def _required_quality_jobs(module, root: pathlib.Path):
        workflows = {
            workflow.path: workflow
            for workflow in module.load_workflows(root)
        }
        jobs = workflows[".github/workflows/ci-quality.yml"].data["jobs"]
        if not isinstance(jobs, dict):
            raise AssertionError("required-quality jobs must be a mapping")
        return jobs

    @staticmethod
    def _static_gate_profile(program: str) -> str:
        if program == "python3 -m pip install -r scripts/requirements.txt":
            return "bootstrap"
        match = re.fullmatch(
            r"python3 scripts/validation/run-ci-gate\.py --profile (changed|full)",
            program,
        )
        if match is None:
            raise AssertionError(f"non-static public profile program: {program!r}")
        return match.group(1)

    def required_quality_run_programs(self) -> tuple[str, ...]:
        jobs = self._required_quality_jobs(self.module, ROOT)
        return tuple(
            step["run"]
            for job in jobs.values()
            for step in job.get("steps", [])
            if isinstance(step, dict) and isinstance(step.get("run"), str)
        )

    def test_required_run_steps_use_only_static_gate_invocations(self) -> None:
        programs = self.required_quality_run_programs()
        for program in programs:
            if self._static_gate_profile(program) == "bootstrap":
                continue
            self.assertRegex(
                program,
                r"\Apython3 scripts/validation/run-ci-gate\.py "
                r"--profile (changed|full)\Z",
            )
        self.assertCountEqual(("bootstrap", "changed", "bootstrap", "full"), map(self._static_gate_profile, programs))

    def test_required_jobs_select_their_public_profiles_once(self) -> None:
        jobs = self._required_quality_jobs(self.module, ROOT)
        expected = {
            "validation-changed": "changed",
            "validation-full": "full",
        }
        self.assertEqual(set(expected), set(jobs))
        for job_id, job in jobs.items():
            programs = tuple(
                step["run"]
                for step in job.get("steps", [])
                if isinstance(step, dict) and isinstance(step.get("run"), str)
            )
            with self.subTest(job_id=job_id):
                self.assertEqual(("bootstrap", expected[job_id]), tuple(map(self._static_gate_profile, programs)))

    def test_bootstrap_projection_is_exact_and_ordered(self) -> None:
        contract = self.module.load_workflow_contract(ROOT)
        document = next(item for item in self.module.load_workflows(ROOT) if item.path == ".github/workflows/ci-quality.yml")
        self.assertEqual((), self.module._workflow_projection_findings(document.path, document.data, document.data["jobs"], contract))
        bootstrap = "python3 -m pip install -r scripts/requirements.txt"
        for job_id, profile in (("validation-changed", "changed"), ("validation-full", "full")):
            command = f"python3 scripts/validation/run-ci-gate.py --profile {profile}"
            for runs in ([command], [bootstrap], [bootstrap, bootstrap, command],
                         [command, bootstrap], [bootstrap, command, command],
                         [bootstrap + " --upgrade", command],
                         ["python3 -m pip install pyyaml", command],
                         [bootstrap + "\ntrue", command], [bootstrap, "true", command]):
                with self.subTest(job=job_id, runs=runs):
                    data = copy.deepcopy(document.data)
                    steps = data["jobs"][job_id]["steps"]
                    data["jobs"][job_id]["steps"] = [step for step in steps if "run" not in step] + [{"run": run} for run in runs]
                    codes = {finding.code for finding in self.module._workflow_projection_findings(document.path, data, data["jobs"], contract)}
                    self.assertTrue(codes & {"workflow-gate-projection-invalid", "workflow-gate-projection-mismatch"}, codes)

    def test_bootstrap_retains_step_context_and_checkout_guards(self) -> None:
        contract = self.module.load_workflow_contract(ROOT)
        documents = self.module.load_workflows(ROOT)
        document = next(item for item in documents if item.path == ".github/workflows/ci-quality.yml")
        for job_id in ("validation-changed", "validation-full"):
            for key, value in (("if", False), ("env", {"X": "Y"}), ("shell", "bash"),
                               ("working-directory", "scripts"), ("continue-on-error", True), ("checkout-order", True)):
                with self.subTest(job=job_id, key=key):
                    data = copy.deepcopy(document.data)
                    steps = data["jobs"][job_id]["steps"]
                    step = next(step for step in steps if step.get("run") == "python3 -m pip install -r scripts/requirements.txt")
                    if key == "checkout-order":
                        steps.remove(step)
                        steps.insert(0, step)
                    else:
                        step[key] = value
                    changed = dataclasses.replace(document, data=data)
                    with mock.patch.object(self.module, "load_workflows", return_value=tuple(changed if item.path == document.path else item for item in documents)):
                        codes = {finding.code for finding in self.module.validate_workflows(ROOT, contract)}
                    expected = "workflow-gate-checkout-required" if key == "checkout-order" else "workflow-continue-on-error-forbidden" if key == "continue-on-error" else "workflow-gate-execution-context-invalid"
                    self.assertIn(expected, codes)

    def test_workflow_projection_rejects_dynamic_ids_and_free_form_shell(
        self,
    ) -> None:
        mutations = {
            "multiline": "python3 scripts/validation/run-ci-gate.py --profile changed\ntrue",
            "expression": (
                "python3 scripts/validation/run-ci-gate.py --profile ${{ matrix.profile }}"
            ),
            "variable": (
                "profile=changed\n"
                'python3 scripts/validation/run-ci-gate.py --profile "$profile"'
            ),
            "heredoc": "python3 - <<'PY'\nprint('gate')\nPY",
            "substitution": "python3 $(printf scripts/validation/run-ci-gate.py)",
            "eval": "eval python3 scripts/validation/run-ci-gate.py",
            "source": "source scripts/validation/run-local-qa-gates.sh",
            "shell-c": "bash -c 'true'",
            "direct-script": (
                "python3 scripts/validation/check-document-links.py --mode traceability"
            ),
        }
        for label, program in mutations.items():
            with self.subTest(label=label), self.workflow_fixture() as root:
                workflow = root / ".github/workflows/ci-quality.yml"
                text = workflow.read_text(encoding="utf-8")
                text = text.replace(
                    "run: python3 scripts/validation/run-ci-gate.py --profile changed",
                    "run: " + program.replace("\n", "\n          "),
                    1,
                )
                workflow.write_text(text, encoding="utf-8")
                codes = {
                    finding.code
                    for finding in self.module.validate_workflows(
                        root,
                        self.module.load_workflow_contract(root),
                    )
                }
                self.assertIn("workflow-gate-projection-invalid", codes)

    def test_required_run_steps_reject_execution_context_mutations(self) -> None:
        cases = (
            (
                "workflow-defaults-run",
                "permissions:\n  contents: read\n",
                "permissions:\n  contents: read\n\ndefaults:\n  run:\n    shell: bash\n",
            ),
            (
                "job-defaults-run",
                "  validation-changed:\n    if: github.event_name == 'pull_request'\n",
                "  validation-changed:\n    defaults:\n"
                "      run:\n"
                "        working-directory: scripts\n"
                "    if: github.event_name == 'pull_request'\n",
            ),
            (
                "job-if",
                "  validation-changed:\n    if: github.event_name == 'pull_request'\n",
                "  validation-changed:\n    if: false\n",
            ),
            (
                "step-if",
                "      - name: Run changed public validation suites\n"
                "        run: python3 scripts/validation/run-ci-gate.py",
                "      - name: Run changed public validation suites\n"
                "        if: false\n"
                "        run: python3 scripts/validation/run-ci-gate.py",
            ),
            (
                "step-shell",
                "      - name: Run changed public validation suites\n"
                "        run: python3 scripts/validation/run-ci-gate.py",
                "      - name: Run changed public validation suites\n"
                "        shell: bash\n"
                "        run: python3 scripts/validation/run-ci-gate.py",
            ),
            (
                "step-working-directory",
                "      - name: Run changed public validation suites\n"
                "        run: python3 scripts/validation/run-ci-gate.py",
                "      - name: Run changed public validation suites\n"
                "        working-directory: scripts\n"
                "        run: python3 scripts/validation/run-ci-gate.py",
            ),
        )
        for label, old, new in cases:
            with self.subTest(label=label), self.workflow_fixture() as root:
                workflow = root / ".github/workflows/ci-quality.yml"
                text = workflow.read_text(encoding="utf-8")
                self.assertIn(old, text)
                workflow.write_text(text.replace(old, new, 1), encoding="utf-8")
                codes = {
                    finding.code
                    for finding in self.module.validate_workflows(
                        root,
                        self.module.load_workflow_contract(root),
                    )
                }
                self.assertIn("workflow-gate-execution-context-invalid", codes)

    def test_only_registered_run_conditions_are_admitted(self) -> None:
        jobs = self._required_quality_jobs(self.module, ROOT)
        self.assertEqual(
            {
                "validation-changed": "github.event_name == 'pull_request'",
                "validation-full": "github.event_name != 'pull_request'",
            },
            {job_id: job["if"] for job_id, job in jobs.items()},
        )
        conditioned_steps = [
            (job_id, step.get("name"), step["if"])
            for job_id, job in jobs.items()
            for step in job.get("steps", [])
            if isinstance(step, dict) and "run" in step and "if" in step
        ]
        self.assertEqual([], conditioned_steps)

    def test_public_profile_jobs_have_exact_registered_checkout(self) -> None:
        contract = self.module.load_workflow_contract(ROOT)
        jobs = self._required_quality_jobs(self.module, ROOT)
        checkout = next(
            action
            for action in contract.actions
            if action.action == "actions/checkout"
        )
        expected_checkout = {
            "name": "Checkout repository",
            "uses": f"actions/checkout@{checkout.sha}",
            "with": {"persist-credentials": False, "fetch-depth": 0},
        }
        for job_id, job in jobs.items():
            with self.subTest(job_id=job_id):
                self.assertEqual(expected_checkout, job["steps"][0])

    def test_workflow_and_registry_co_mutations_fail_closed(self) -> None:
        with self.workflow_fixture() as root:
            workflow = root / ".github/workflows/ci-quality.yml"
            workflow.write_text(
                workflow.read_text(encoding="utf-8").replace(
                    "run: python3 scripts/validation/run-ci-gate.py "
                    "--profile changed",
                    "run: python3 scripts/validation/run-ci-gate.py "
                    "--profile ci --gate leaf.docs-implementation-alignment",
                    1,
                ),
                encoding="utf-8",
            )
            document = self.load_contract_document(root)
            for record in document["job_roots"]:
                if record["job_id"] == "validation-changed":
                    record["root_gate_id"] = "leaf.docs-implementation-alignment"
                    break
            self.write_contract_document(root, document)
            findings = self.module.validate_workflows(
                root,
                self.module.load_workflow_contract(root),
            )
        self.assertIn(
            "ci-gate-required-job-roots",
            {finding.code for finding in findings},
        )

    def test_ci_and_local_profiles_share_node_definitions(self) -> None:
        contract = self.module.load_workflow_contract(ROOT)
        ci_nodes = {
            node.gate_id: node
            for node in contract.gate_registry.nodes
            if node.gate_id
            in self.module.expand_gate_ids(
                contract.gate_registry,
                "ci",
                None,
                True,
            )
        }
        expected_shared = {
            profile: tuple(
                sorted(
                    set(ci_nodes)
                    & set(
                        self.module.expand_gate_ids(
                            contract.gate_registry,
                            profile,
                            None,
                            True,
                        )
                    )
                )
            )
            for profile in (
                "local-script-backed",
                "local-harness",
                "local-all-profiles",
            )
        }
        script_backed = set(expected_shared["local-script-backed"])
        harness = set(expected_shared["local-harness"])
        all_profiles = set(expected_shared["local-all-profiles"])
        self.assertEqual({"leaf.quickwin-baseline"}, script_backed - harness)
        self.assertEqual(set(), harness - script_backed)
        self.assertEqual(
            {"leaf.compose-all-profiles-validation"},
            all_profiles - script_backed,
        )
        self.assertEqual(set(), script_backed - all_profiles)
        node_by_id = {
            node.gate_id: node for node in contract.gate_registry.nodes
        }
        for profile, shared_ids in expected_shared.items():
            profile_nodes = {
                gate_id: node_by_id[gate_id]
                for gate_id in self.module.expand_gate_ids(
                    contract.gate_registry,
                    profile,
                    None,
                    True,
                )
            }
            for gate_id in shared_ids:
                with self.subTest(profile=profile, gate_id=gate_id):
                    self.assertIs(
                        ci_nodes[gate_id],
                        profile_nodes[gate_id],
                    )

    def test_local_parallel_node_substitution_fails_closed(self) -> None:
        with self.workflow_fixture() as root:
            document = self.load_contract_document(root)
            source = next(
                node
                for node in document["gate_nodes"]
                if node["gate_id"] == "leaf.docs-traceability"
            )
            parallel = dict(source)
            parallel["gate_id"] = "leaf.local-parallel-docs-traceability"
            parallel["suite_key"] = "local-parallel-docs-traceability"
            document["gate_nodes"].append(parallel)
            profile = next(
                record
                for record in document["profile_roots"]
                if record["profile"] == "local-script-backed"
            )
            profile["root_gate_ids"] = [
                parallel["gate_id"]
                if gate_id == "ci.docs-traceability"
                else gate_id
                for gate_id in profile["root_gate_ids"]
            ]
            self.write_contract_document(root, document)
            findings = self.module.validate_workflows(
                root,
                self.module.load_workflow_contract(root),
            )
        self.assertIn(
            "ci-gate-profile-roots",
            {finding.code for finding in findings},
        )

    def test_full_public_profile_owns_storybook_setup_and_coverage(
        self,
    ) -> None:
        contract = self.module.load_workflow_contract(ROOT)
        jobs = self._required_quality_jobs(self.module, ROOT)
        programs = tuple(
            step["run"]
            for step in jobs["validation-full"]["steps"]
            if isinstance(step, dict) and isinstance(step.get("run"), str)
        )
        self.assertEqual(
            (self.module.CI_DEPENDENCY_BOOTSTRAP, "python3 scripts/validation/run-ci-gate.py --profile full"),
            programs,
        )
        document = self.load_contract_document(ROOT)
        self.assertIn(
            "ci.storybook-coverage",
            document["public_gate"]["suite_roots"]["repository-integrity"],
        )
        expanded = self.module.expand_gate_ids(
            contract.gate_registry,
            "ci",
            "ci.storybook-coverage",
            False,
        )
        self.assertEqual(
            (
                "setup.storybook-node-dependencies",
                "setup.storybook-playwright",
                "leaf.storybook-coverage",
            ),
            expanded,
        )

    @contextlib.contextmanager
    def workflow_fixture(self):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            shutil.copytree(ROOT / ".github", root / ".github")
            shutil.copytree(ROOT / "scripts", root / "scripts")
            yield root

    def load_contract_document(self, root: pathlib.Path) -> dict[str, object]:
        return json.loads(
            (root / ".github/workflow-contract.yml").read_text(
                encoding="utf-8"
            )
        )

    def write_contract_document(
        self,
        root: pathlib.Path,
        document: dict[str, object],
    ) -> None:
        (root / ".github/workflow-contract.yml").write_text(
            json.dumps(document, indent=2) + "\n",
            encoding="utf-8",
        )

    def append_aggregate_program(
        self,
        root: pathlib.Path,
        program: str,
    ) -> None:
        aggregate = root / "scripts/validation/check-repo-contracts.sh"
        aggregate.write_text(
            aggregate.read_text(encoding="utf-8")
            + "\n"
            + program.rstrip()
            + "\n",
            encoding="utf-8",
        )

    def append_workflow_program(
        self,
        root: pathlib.Path,
        *,
        name: str,
        program: str,
    ) -> None:
        workflow = root / ".github/workflows/ci-quality.yml"
        text = workflow.read_text(encoding="utf-8")
        anchor = "      - name: Check docs traceability sync\n"
        step = (
            f"      - name: {name}\n"
            "        shell: bash\n"
            "        run: |\n"
            + "".join(f"          {line}\n" for line in program.splitlines())
        )
        self.assertIn(anchor, text)
        workflow.write_text(
            text.replace(anchor, step + anchor, 1),
            encoding="utf-8",
        )

    def semantic_finding_codes(
        self,
        root: pathlib.Path,
    ) -> set[str]:
        findings = self.module.validate_workflows(
            root,
            self.module.load_workflow_contract(root),
        )
        return {
            finding.code
            for finding in findings
            if finding.code
            in {
                "expensive-command-ownership-duplicate",
                "workflow-aggregate-source-invalid",
                "workflow-semantic-command-source-invalid",
            }
        }

    def test_security_and_ownership_mutation_matrix_fails_closed(self) -> None:
        sentinel = "private-workflow-sentinel"
        cases = (
            (
                "pull-request-target",
                ".github/workflows/ci-quality.yml",
                "  workflow_dispatch:\n",
                "  workflow_dispatch:\n  pull_request_target:\n",
                "workflow-trigger-forbidden",
            ),
            (
                "workflow-call",
                ".github/workflows/ci-quality.yml",
                "  workflow_dispatch:\n",
                "  workflow_dispatch:\n  workflow_call:\n",
                "workflow-trigger-forbidden",
            ),
            (
                "workflow-run",
                ".github/workflows/ci-quality.yml",
                "  workflow_dispatch:\n",
                "  workflow_dispatch:\n  workflow_run:\n",
                "workflow-trigger-forbidden",
            ),
            (
                "event-widening",
                ".github/workflows/ci-quality.yml",
                "  workflow_dispatch:\n",
                "  workflow_dispatch:\n  issues:\n    types: [opened]\n",
                "workflow-trigger-mismatch",
            ),
            (
                "branch-widening",
                ".github/workflows/ci-quality.yml",
                "    branches: [main]\n",
                "    branches: [main, dev]\n",
                "workflow-trigger-mismatch",
            ),
            (
                "path-widening",
                ".github/workflows/tech-stack-version-sync.yml",
                "      - 'infra/tech-stack.versions.json'\n",
                "      - 'infra/tech-stack.versions.json'\n      - '.github/**'\n",
                "workflow-trigger-mismatch",
            ),
            (
                "schedule-widening",
                ".github/workflows/stale.yml",
                "    - cron: '30 1 * * *'\n",
                "    - cron: '30 1 * * *'\n    - cron: '0 0 * * *'\n",
                "workflow-trigger-mismatch",
            ),
            (
                "write-all",
                ".github/workflows/ci-quality.yml",
                "permissions:\n  contents: read\n",
                "permissions: write-all\n",
                "workflow-permission-write-all",
            ),
            (
                "job-permission-widening",
                ".github/workflows/ci-quality.yml",
                "  validation-changed:\n    if: github.event_name == 'pull_request'\n    permissions:\n      contents: read\n",
                "  validation-changed:\n    if: github.event_name == 'pull_request'\n    permissions:\n      contents: read\n      issues: read\n",
                "workflow-job-permission-mismatch",
            ),
            (
                "missing-timeout",
                ".github/workflows/ci-quality.yml",
                "  validation-changed:\n    if: github.event_name == 'pull_request'\n    permissions:\n      contents: read\n    runs-on: ubuntu-latest\n    timeout-minutes: 30\n",
                "  validation-changed:\n    if: github.event_name == 'pull_request'\n    permissions:\n      contents: read\n    runs-on: ubuntu-latest\n",
                "workflow-job-timeout-mismatch",
            ),
            (
                "concurrency-widening",
                ".github/workflows/ci-quality.yml",
                "  cancel-in-progress: true\n",
                "  cancel-in-progress: false\n",
                "workflow-concurrency-mismatch",
            ),
            (
                "duplicate-job-identity",
                ".github/workflows/tech-stack-version-sync.yml",
                "jobs:\n  drift-gate:\n",
                (
                    "jobs:\n"
                    "  validation-changed:\n"
                    "    permissions:\n"
                    "      contents: read\n"
                    "    runs-on: ubuntu-latest\n"
                    "    timeout-minutes: 5\n"
                    "    steps: []\n"
                    "  drift-gate:\n"
                ),
                "workflow-job-identity-duplicate",
            ),
            (
                "mutable-action",
                ".github/workflows/ci-quality.yml",
                "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1",
                "actions/checkout@main",
                "action-ref-mutable",
            ),
            (
                "unregistered-action",
                ".github/workflows/ci-quality.yml",
                "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1",
                "example/action@3d3c42e5aac5ba805825da76410c181273ba90b1",
                "action-unregistered",
            ),
            (
                "node20-runtime",
                ".github/workflow-contract.yml",
                "    runtime: node24\n",
                "    runtime: node20\n",
                "action-runtime-unsupported",
            ),
            (
                "unsafe-run-interpolation",
                ".github/workflows/ci-quality.yml",
                "        run: python3 scripts/validation/run-ci-gate.py --profile changed\n",
                f'        run: echo "${{{{ github.event.pull_request.title }}}}-{sentinel}"\n',
                "workflow-run-interpolation-unsafe",
            ),
        )
        for label, relative, old, new, expected_code in cases:
            with self.subTest(label=label), self.workflow_fixture() as root:
                target = root / relative
                if label == "node20-runtime":
                    document = self.load_contract_document(root)
                    action = next(iter(document["actions"].values()))
                    action["runtime"] = "node20"
                    self.write_contract_document(root, document)
                else:
                    text = target.read_text(encoding="utf-8")
                    self.assertIn(old, text)
                    target.write_text(
                        text.replace(old, new, 1),
                        encoding="utf-8",
                    )
                contract = self.module.load_workflow_contract(root)
                findings = self.module.validate_workflows(root, contract)
                codes = {finding.code for finding in findings}
                self.assertIn(expected_code, codes)
                self.assertNotIn(
                    sentinel,
                    "\n".join(finding.message for finding in findings),
                )

    def test_required_permission_contract_co_mutations_fail_baseline(
        self,
    ) -> None:
        required_job_workflow = (
            "  validation-changed:\n"
            "    if: github.event_name == 'pull_request'\n"
            "    permissions:\n"
            "      contents: read\n"
        )
        cases = [
            (
                "top-contents-write",
                "permissions:\n  contents: read\n\nconcurrency:\n",
                "permissions:\n  contents: write\n\nconcurrency:\n",
                (
                    "    permissions:\n"
                    "      contents: read\n"
                    "    concurrency:\n"
                ),
                (
                    "    permissions:\n"
                    "      contents: write\n"
                    "    concurrency:\n"
                ),
            ),
            (
                "job-contents-write",
                required_job_workflow,
                required_job_workflow.replace("contents: read", "contents: write"),
                "",
                "",
            ),
        ]
        for scope in ("packages", "id-token", "issues", "pull-requests"):
            cases.append(
                (
                    f"job-{scope}-write",
                    required_job_workflow,
                    required_job_workflow.replace(
                        "      contents: read\n",
                        f"      contents: read\n      {scope}: write\n",
                    ),
                    "",
                    "",
                )
            )
        cases.append(
            (
                "full-extra-write",
                (
                    "    permissions:\n"
                    "      actions: read\n"
                    "      contents: read\n"
                    "      security-events: write\n"
                ),
                (
                    "    permissions:\n"
                    "      actions: read\n"
                    "      contents: read\n"
                    "      security-events: write\n"
                    "      packages: write\n"
                ),
                "",
                "",
            )
        )

        for (
            label,
            workflow_old,
            workflow_new,
            _contract_old,
            _contract_new,
        ) in cases:
            with self.subTest(label=label), self.workflow_fixture() as root:
                workflow = root / ".github/workflows/ci-quality.yml"
                workflow_text = workflow.read_text(encoding="utf-8")
                self.assertIn(workflow_old, workflow_text)
                workflow.write_text(
                    workflow_text.replace(workflow_old, workflow_new, 1),
                    encoding="utf-8",
                )
                document = self.load_contract_document(root)
                ci = document["workflows"][
                    ".github/workflows/ci-quality.yml"
                ]
                if label == "top-contents-write":
                    ci["permissions"]["contents"] = "write"
                elif label == "full-extra-write":
                    ci["jobs"]["validation-full"]["permissions"]["packages"] = "write"
                else:
                    permissions = ci["jobs"]["validation-changed"][
                        "permissions"
                    ]
                    if label == "job-contents-write":
                        permissions["contents"] = "write"
                    else:
                        permissions[label.removeprefix("job-").removesuffix(
                            "-write"
                        )] = "write"
                self.write_contract_document(root, document)
                contract = self.module.load_workflow_contract(root)
                findings = self.module.validate_workflows(root, contract)
                self.assertIn(
                    "workflow-permission-baseline-invalid",
                    {finding.code for finding in findings},
                )

    @unittest.skip("Wave A retains the inactive semantic parser until Wave C")
    def test_semantic_owner_direct_and_transitive_duplicates_fail_closed(
        self,
    ) -> None:
        workflows = {
            workflow.path: workflow
            for workflow in self.module.load_workflows(ROOT)
        }
        repo_steps = workflows[
            ".github/workflows/ci-quality.yml"
        ].data["jobs"]["repo-contracts"]["steps"]
        repo_commands = "\n".join(
            str(step.get("run", ""))
            for step in repo_steps
            if isinstance(step, dict)
        )
        for marker in (
            "scripts/validation/check-target-surface-contract.py",
            "scripts/validation/check-agentic-audit-semantic-freshness.py",
            "scripts/validation/check-agent-governance-contract.py",
        ):
            with self.subTest(label="current-direct-owner", marker=marker):
                self.assertNotIn(marker, repo_commands)

        cases = ("direct-wrapper", "transitive-aggregate")
        for label in cases:
            with self.subTest(label=label), self.workflow_fixture() as root:
                workflow = root / ".github/workflows/ci-quality.yml"
                workflow_text = workflow.read_text(encoding="utf-8")
                if label == "direct-wrapper":
                    owner = (
                        "      - name: Check repository contracts\n"
                        "        run: bash scripts/validation/"
                        "check-repo-contracts.sh\n"
                    )
                    duplicate = (
                        "      - name: Duplicate hardening owner\n"
                        "        run: if ! bash scripts/hardening/"
                        "check-all-hardening.sh >/tmp/result; then exit 1; fi\n"
                    )
                    self.assertIn(owner, workflow_text)
                    workflow.write_text(
                        workflow_text.replace(owner, duplicate + owner, 1),
                        encoding="utf-8",
                    )
                else:
                    aggregate = (
                        root / "scripts/validation/check-repo-contracts.sh"
                    )
                    aggregate.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(
                        ROOT / "scripts/validation/check-repo-contracts.sh",
                        aggregate,
                    )
                    aggregate.write_text(
                        aggregate.read_text(encoding="utf-8")
                        + (
                            "\nif ! bash scripts/hardening/"
                            "check-all-hardening.sh >/tmp/result; then\n"
                            "  exit 1\n"
                            "fi\n"
                        ),
                        encoding="utf-8",
                    )
                findings = self.module.validate_workflows(
                    root,
                    self.module.load_workflow_contract(root),
                )
                self.assertIn(
                    "expensive-command-ownership-duplicate",
                    {finding.code for finding in findings},
                )

    @unittest.skip("Wave A retains the inactive semantic parser until Wave C")
    def test_supply_chain_semantic_commands_are_all_transitively_owned(
        self,
    ) -> None:
        for command in SUPPLY_CHAIN_SEMANTIC_COMMANDS:
            with self.subTest(command=command), self.workflow_fixture() as root:
                aggregate = root / "scripts/validation/check-repo-contracts.sh"
                aggregate.write_text(
                    aggregate.read_text(encoding="utf-8")
                    + f"\n{command}\n",
                    encoding="utf-8",
                )
                findings = self.module.validate_workflows(
                    root,
                    self.module.load_workflow_contract(root),
                )
                self.assertIn(
                    "expensive-command-ownership-duplicate",
                    {finding.code for finding in findings},
                )

    @unittest.skip("Wave A retains the inactive semantic parser until Wave C")
    def test_semantic_owner_workflow_contract_co_mutations_fail_code_baseline(
        self,
    ) -> None:
        cases = (
            (
                "repo-contracts-control-plane-regressions",
                "repo-contracts",
                CONTROL_PLANE_SEMANTIC_COMMANDS[0],
                "Check agent governance CI routing mutations",
            ),
            (
                "agent-output-eval-fixture-regressions",
                "agent-output-eval-fixture-gate",
                CONTROL_PLANE_SEMANTIC_COMMANDS[1],
                "Check agent-output eval fixture regressions",
            ),
            (
                "supply-chain-deterministic-policy",
                "supply-chain-fixture-policy",
                SUPPLY_CHAIN_SEMANTIC_COMMANDS[1],
                "Check deterministic supply-chain policy fixtures",
            ),
            (
                "supply-chain-summary-freshness",
                "supply-chain-fixture-policy",
                SUPPLY_CHAIN_SEMANTIC_COMMANDS[2],
                "Check supply-chain summary freshness",
            ),
        )
        for identifier, job, command, step_name in cases:
            with self.subTest(identifier=identifier), self.workflow_fixture() as root:
                workflow = root / ".github/workflows/ci-quality.yml"
                workflow_text = workflow.read_text(encoding="utf-8")
                workflow_step = (
                    f"      - name: {step_name}\n"
                    f"        run: {command}\n"
                )
                self.assertIn(workflow_step, workflow_text)
                workflow.write_text(
                    workflow_text.replace(workflow_step, "", 1),
                    encoding="utf-8",
                )

                contract_path = root / ".github/workflow-contract.yml"
                contract_text = contract_path.read_text(encoding="utf-8")
                owner_command = f"          - {command}\n"
                owner_record = (
                    f"  - id: {identifier}\n"
                    "    workflow: .github/workflows/ci-quality.yml\n"
                    f"    job: {job}\n"
                    f"    command: {command}\n"
                )
                self.assertIn(owner_command, contract_text)
                self.assertIn(owner_record, contract_text)
                contract_path.write_text(
                    contract_text.replace(owner_command, "", 1).replace(
                        owner_record,
                        "",
                        1,
                    ),
                    encoding="utf-8",
                )
                with self.assertRaises(
                    self.module.WorkflowContractError
                ) as raised:
                    self.module.load_workflow_contract(root)
                self.assertEqual(
                    "contract-expensive-owner-baseline-invalid",
                    raised.exception.code,
                )

    @unittest.skip("Wave A retains the inactive semantic parser until Wave C")
    def test_semantic_owner_shell_grammar_is_fail_closed_and_data_safe(
        self,
    ) -> None:
        marker = "scripts/hardening/check-all-hardening.sh"
        cases = (
            (
                "direct-executable",
                f"./{marker}\n",
                {"workflow-aggregate-source-invalid"},
            ),
            (
                "variable-indirection",
                f'checker="{marker}"\nbash "$checker"\n',
                {"expensive-command-ownership-duplicate"},
            ),
            (
                "unknown-wrapper",
                f"run_gate {marker}\n",
                {"workflow-aggregate-source-invalid"},
            ),
            (
                "comment",
                f"# bash {marker}\n",
                set(),
            ),
            (
                "quoted-data",
                f"printf '%s\\n' 'bash {marker}'\n",
                set(),
            ),
            (
                "heredoc-data",
                f"cat <<'REPORT'\nbash {marker}\nREPORT\n",
                set(),
            ),
            (
                "quoted-heredoc-lookalike-before-executable",
                (
                    "printf '%s\\n' '<<REPORT'\n"
                    f"./{marker}\n"
                    "REPORT\n"
                ),
                {"workflow-aggregate-source-invalid"},
            ),
        )
        for label, mutation, expected_codes in cases:
            with self.subTest(label=label), self.workflow_fixture() as root:
                aggregate = root / "scripts/validation/check-repo-contracts.sh"
                aggregate.write_text(
                    aggregate.read_text(encoding="utf-8")
                    + "\n"
                    + mutation,
                    encoding="utf-8",
                )
                findings = self.module.validate_workflows(
                    root,
                    self.module.load_workflow_contract(root),
                )
                relevant_codes = {
                    finding.code
                    for finding in findings
                    if finding.code
                    in {
                        "expensive-command-ownership-duplicate",
                        "workflow-aggregate-source-invalid",
                    }
                }
                self.assertEqual(expected_codes, relevant_codes)

    @unittest.skip("Wave A retains the inactive semantic parser until Wave C")
    def test_semantic_owner_complete_program_variable_matrix(
        self,
    ) -> None:
        marker = "scripts/hardening/check-all-hardening.sh"
        safe_cases = (
            (
                "literal-assignment-later-interpreter",
                f'checker="{marker}"\nbash "$checker"',
            ),
            (
                "literal-assignment-same-line-direct",
                f"checker={marker}; bash \"${{checker}}\"",
            ),
        )
        for label, program in safe_cases:
            with self.subTest(label=label), self.workflow_fixture() as root:
                self.append_workflow_program(
                    root,
                    name=f"Duplicate semantic owner {label}",
                    program=program,
                )
                self.assertIn(
                    "expensive-command-ownership-duplicate",
                    self.semantic_finding_codes(root),
                )

        ambiguous_cases = (
            (
                "dynamic-assignment",
                (
                    'prefix="${DYNAMIC_ROOT:-}"\n'
                    f'checker="${{prefix}}/{marker}"\n'
                    'bash "$checker"'
                ),
            ),
            (
                "variable-indirection",
                (
                    f'checker="{marker}"\n'
                    'pointer=checker\n'
                    'bash "${!pointer}"'
                ),
            ),
            (
                "unresolved-variable",
                (
                    f'expected="{marker}"\n'
                    'bash "$unresolved_checker" "$expected"'
                ),
            ),
            (
                "dynamic-direct-executable",
                (
                    'checker="${DYNAMIC_CHECKER:-}"\n'
                    '"$checker"'
                ),
            ),
        )
        for label, program in ambiguous_cases:
            with self.subTest(label=label), self.workflow_fixture() as root:
                self.append_workflow_program(
                    root,
                    name=f"Ambiguous semantic owner {label}",
                    program=program,
                )
                self.assertIn(
                    "workflow-semantic-command-source-invalid",
                    self.semantic_finding_codes(root),
                )

    @unittest.skip("Wave A retains the inactive semantic parser until Wave C")
    def test_non_script_semantic_commands_normalize_safe_wrappers_and_continuations(
        self,
    ) -> None:
        cases = (
            (
                "command-python",
                (
                    "command python3 -m unittest "
                    "tests.validation.test_agent_governance_ci_routing -v"
                ),
            ),
            (
                "env-npm",
                (
                    "env LC_ALL=C npm audit --audit-level=high "
                    "--prefix projects/storybook/nextjs"
                ),
            ),
            (
                "env-options-npm",
                (
                    "env -i --unset HOME LC_ALL=C "
                    "npm audit --audit-level=high "
                    "--prefix projects/storybook/nextjs"
                ),
            ),
            (
                "continued-python",
                (
                    "command python3 -m unittest \\\n"
                    "  tests.validation.test_agent_governance_ci_routing \\\n"
                    "  -v"
                ),
            ),
        )
        for label, program in cases:
            with self.subTest(label=label), self.workflow_fixture() as root:
                self.append_workflow_program(
                    root,
                    name=f"Equivalent non-script owner {label}",
                    program=program,
                )
                self.assertIn(
                    "expensive-command-ownership-duplicate",
                    self.semantic_finding_codes(root),
                )

    @unittest.skip("Wave A retains the inactive semantic parser until Wave C")
    def test_semantic_owner_rejects_dynamic_shell_and_path_aliases(
        self,
    ) -> None:
        marker = "scripts/hardening/check-all-hardening.sh"
        sentinel = "private-semantic-payload"
        cases = (
            ("shell-c", f"bash -c 'bash {marker}'"),
            ("eval", f"eval 'bash {marker}'"),
            ("source", f"source {marker}"),
            ("unknown-wrapper", f"run_gate {marker}"),
            (
                "command-substitution-echo",
                f'echo "$({marker} {sentinel})"',
            ),
            (
                "command-substitution-printf",
                f'printf "%s\\n" "$(bash {marker} {sentinel})"',
            ),
            (
                "process-substitution",
                f"diff <(bash {marker}) /dev/null",
            ),
            (
                "noncanonical-dot-dot",
                (
                    "bash scripts/validation/../hardening/"
                    "check-all-hardening.sh"
                ),
            ),
            (
                "noncanonical-double-slash",
                "bash scripts//hardening/check-all-hardening.sh",
            ),
            (
                "noncanonical-absolute",
                f"bash \"$PWD/{marker}\"",
            ),
        )
        for label, program in cases:
            with self.subTest(label=label), self.workflow_fixture() as root:
                self.append_aggregate_program(root, program)
                findings = self.module.validate_workflows(
                    root,
                    self.module.load_workflow_contract(root),
                )
                self.assertIn(
                    "workflow-aggregate-source-invalid",
                    {finding.code for finding in findings},
                )
                self.assertTrue(
                    all(
                        sentinel not in finding.message
                        for finding in findings
                    )
                )

    @unittest.skip("Wave A retains the inactive semantic parser until Wave C")
    def test_semantic_owner_heredoc_interpolation_is_fail_closed(
        self,
    ) -> None:
        marker = "scripts/hardening/check-all-hardening.sh"
        cases = (
            (
                "quoted-heredoc-data",
                (
                    "cat <<'REPORT'\n"
                    f"$(bash {marker})\n"
                    "REPORT"
                ),
                set(),
            ),
            (
                "unquoted-heredoc-command-substitution",
                (
                    "cat <<REPORT\n"
                    f"$(bash {marker})\n"
                    "REPORT"
                ),
                {"workflow-aggregate-source-invalid"},
            ),
            (
                "unquoted-heredoc-backtick-substitution",
                (
                    "cat <<REPORT\n"
                    f"`bash {marker}`\n"
                    "REPORT"
                ),
                {"workflow-aggregate-source-invalid"},
            ),
        )
        for label, program, expected_codes in cases:
            with self.subTest(label=label), self.workflow_fixture() as root:
                self.append_aggregate_program(root, program)
                self.assertEqual(
                    expected_codes,
                    self.semantic_finding_codes(root),
                )

    @unittest.skip("Wave A retains the inactive semantic parser until Wave C")
    def test_semantic_owner_recurses_literal_helpers_and_fails_closed_on_cycles(
        self,
    ) -> None:
        marker = "scripts/hardening/check-all-hardening.sh"
        cases = ("one-helper", "nested-helper", "python-helper", "cycle")
        for label in cases:
            with self.subTest(label=label), self.workflow_fixture() as root:
                helper_root = root / "scripts/validation"
                helper_root.mkdir(parents=True, exist_ok=True)
                first = helper_root / "task4-semantic-helper-a.sh"
                second = helper_root / "task4-semantic-helper-b.sh"
                if label == "one-helper":
                    first.write_text(
                        f"#!/usr/bin/env bash\nbash {marker}\n",
                        encoding="utf-8",
                    )
                    expected = {
                        "expensive-command-ownership-duplicate"
                    }
                elif label == "nested-helper":
                    first.write_text(
                        (
                            "#!/usr/bin/env bash\n"
                            "bash scripts/validation/"
                            "task4-semantic-helper-b.sh\n"
                        ),
                        encoding="utf-8",
                    )
                    second.write_text(
                        f"#!/usr/bin/env bash\nbash {marker}\n",
                        encoding="utf-8",
                    )
                    expected = {
                        "expensive-command-ownership-duplicate"
                    }
                elif label == "python-helper":
                    first = first.with_suffix(".py")
                    first.write_text(
                        (
                            "#!/usr/bin/env python3\n"
                            "import subprocess\n"
                            "subprocess.run(\n"
                            f'    ["bash", "{marker}"],\n'
                            "    check=True,\n"
                            ")\n"
                        ),
                        encoding="utf-8",
                    )
                    expected = {
                        "expensive-command-ownership-duplicate"
                    }
                else:
                    first.write_text(
                        (
                            "#!/usr/bin/env bash\n"
                            "bash scripts/validation/"
                            "task4-semantic-helper-b.sh\n"
                        ),
                        encoding="utf-8",
                    )
                    second.write_text(
                        (
                            "#!/usr/bin/env bash\n"
                            "bash scripts/validation/"
                            "task4-semantic-helper-a.sh\n"
                        ),
                        encoding="utf-8",
                    )
                    expected = {"workflow-aggregate-source-invalid"}
                self.append_aggregate_program(
                    root,
                    (
                        "python3 scripts/validation/"
                        "task4-semantic-helper-a.py"
                        if label == "python-helper"
                        else (
                            "bash scripts/validation/"
                            "task4-semantic-helper-a.sh"
                        )
                    ),
                )
                self.assertTrue(
                    expected.issubset(self.semantic_finding_codes(root))
                )

    @unittest.skip("Wave A retains the inactive semantic parser until Wave C")
    def test_semantic_helper_depth_file_byte_and_symlink_limits_fail_closed(
        self,
    ) -> None:
        cases = ("depth", "files", "bytes", "symlink")
        for label in cases:
            with self.subTest(label=label), self.workflow_fixture() as root:
                helper_root = root / "scripts/validation"
                helper_root.mkdir(parents=True, exist_ok=True)
                if label == "depth":
                    for index in range(10):
                        successor = (
                            f"bash scripts/validation/task4-depth-{index + 1}.sh\n"
                            if index < 9
                            else "true\n"
                        )
                        (helper_root / f"task4-depth-{index}.sh").write_text(
                            "#!/usr/bin/env bash\n" + successor,
                            encoding="utf-8",
                        )
                    entry = "bash scripts/validation/task4-depth-0.sh"
                elif label == "files":
                    invocations: list[str] = []
                    for index in range(65):
                        relative = (
                            f"scripts/validation/task4-file-{index}.sh"
                        )
                        (root / relative).write_text(
                            "#!/usr/bin/env bash\ntrue\n",
                            encoding="utf-8",
                        )
                        invocations.append(f"bash {relative}")
                    entry = "\n".join(invocations)
                elif label == "bytes":
                    relative = "scripts/validation/task4-large-helper.sh"
                    (root / relative).write_text(
                        "#!/usr/bin/env bash\n#"
                        + ("x" * (256 * 1024))
                        + "\n",
                        encoding="utf-8",
                    )
                    entry = f"bash {relative}"
                else:
                    target = helper_root / "task4-helper-target.sh"
                    target.write_text(
                        "#!/usr/bin/env bash\ntrue\n",
                        encoding="utf-8",
                    )
                    link = helper_root / "task4-helper-link.sh"
                    os.symlink(target.name, link)
                    entry = (
                        "bash scripts/validation/task4-helper-link.sh"
                    )
                self.append_aggregate_program(root, entry)
                self.assertIn(
                    "workflow-aggregate-source-invalid",
                    self.semantic_finding_codes(root),
                )

    @unittest.skip("Wave A retains the inactive semantic parser until Wave C")
    def test_direct_local_executable_requires_tracked_mode_and_admitted_shebang(
        self,
    ) -> None:
        marker = pathlib.PurePosixPath(
            "scripts/hardening/check-all-hardening.sh"
        )
        cases = (
            (
                "tracked-executable",
                "copy",
                True,
                {"expensive-command-ownership-duplicate"},
            ),
            (
                "tracked-non-executable",
                "copy",
                False,
                {"workflow-aggregate-source-invalid"},
            ),
            (
                "untracked-executable",
                "copy-untracked",
                True,
                {"workflow-aggregate-source-invalid"},
            ),
            (
                "invalid-shebang",
                "invalid-shebang",
                True,
                {"workflow-aggregate-source-invalid"},
            ),
            (
                "symlink",
                "symlink",
                True,
                {"workflow-aggregate-source-invalid"},
            ),
        )
        for label, setup, executable, expected_codes in cases:
            with self.subTest(label=label), self.workflow_fixture() as root:
                path = root.joinpath(*marker.parts)
                path.parent.mkdir(parents=True, exist_ok=True)
                if setup == "copy":
                    shutil.copy2(ROOT.joinpath(*marker.parts), path)
                elif setup == "copy-untracked":
                    shutil.copy2(ROOT.joinpath(*marker.parts), path)
                elif setup == "invalid-shebang":
                    path.write_text(
                        "#!/usr/bin/env ruby\nexit 0\n",
                        encoding="utf-8",
                    )
                else:
                    target = path.with_name("tracked-target.sh")
                    target.write_text(
                        "#!/usr/bin/env bash\nexit 0\n",
                        encoding="utf-8",
                    )
                    path.unlink()
                    os.symlink(target.name, path)
                if not path.is_symlink():
                    path.chmod(0o755 if executable else 0o644)

                subprocess.run(
                    ["git", "init", "-q"],
                    cwd=root,
                    check=True,
                    capture_output=True,
                )
                if setup != "copy-untracked":
                    subprocess.run(
                        ["git", "add", marker.as_posix()],
                        cwd=root,
                        check=True,
                        capture_output=True,
                    )
                    if setup == "copy":
                        subprocess.run(
                            [
                                "git",
                                "update-index",
                                (
                                    "--chmod=+x"
                                    if executable
                                    else "--chmod=-x"
                                ),
                                marker.as_posix(),
                            ],
                            cwd=root,
                            check=True,
                            capture_output=True,
                        )
                self.append_aggregate_program(
                    root,
                    f"./{marker.as_posix()}",
                )
                self.assertEqual(
                    expected_codes,
                    self.semantic_finding_codes(root),
                )

    def test_alternate_boolean_trigger_keys_cannot_masquerade_as_on(
        self,
    ) -> None:
        for spelling in ("true", "yes", "ON"):
            with self.subTest(spelling=spelling), self.workflow_fixture() as root:
                workflow = root / ".github/workflows/ci-quality.yml"
                text = workflow.read_text(encoding="utf-8")
                self.assertIn("on:\n", text)
                workflow.write_text(
                    text.replace("on:\n", f"{spelling}:\n", 1),
                    encoding="utf-8",
                )
                with self.assertRaises(
                    self.module.WorkflowContractError
                ) as raised:
                    self.module.load_workflows(root)
                self.assertEqual(
                    "workflow-trigger-key-invalid",
                    raised.exception.code,
                )

    def test_action_registry_and_local_action_policy_fail_closed(self) -> None:
        cases = ("ninth-registered-action", "local-action")
        for label in cases:
            with self.subTest(label=label), self.workflow_fixture() as root:
                workflow = root / ".github/workflows/ci-quality.yml"
                text = workflow.read_text(encoding="utf-8")
                step = (
                    "      - name: Additional Action probe\n"
                    "        uses: "
                )
                if label == "ninth-registered-action":
                    action = "example/action"
                    sha = "0000000000000000000000000000000000000000"
                    step += f"{action}@{sha}\n"
                    contract_data = self.load_contract_document(root)
                    contract_data["actions"][action] = {
                        "sha": sha,
                        "runtime": "node24",
                        "manifest_url": (
                            "https://raw.githubusercontent.com/"
                            f"{action}/{sha}/action.yml"
                        ),
                        "retrieved_at": "2026-07-28",
                        "consumers": [
                            ".github/workflows/ci-quality.yml"
                        ],
                        "security_disposition": "approved-node24",
                    }
                    contract_data["actions"] = dict(
                        sorted(contract_data["actions"].items())
                    )
                    self.write_contract_document(root, contract_data)
                    expected = "action-registry-baseline-invalid"
                else:
                    step += "./.github/actions/private-probe\n"
                    expected = "action-local-reference-forbidden"
                anchor = "      - name: Run changed public validation suites\n"
                self.assertIn(anchor, text)
                workflow.write_text(
                    text.replace(anchor, step + anchor, 1),
                    encoding="utf-8",
                )
                findings = self.module.validate_workflows(
                    root,
                    self.module.load_workflow_contract(root),
                )
                self.assertIn(
                    expected,
                    {finding.code for finding in findings},
                )

    def test_non_gating_permissions_have_exact_workflow_and_job_owners(
        self,
    ) -> None:
        expected = {
            ".github/workflows/document-corpus-lifecycle.yml": (
                {"contents": "read"},
                {"document-corpus-lifecycle": {"contents": "read"}},
            ),
            ".github/workflows/generate-changelog.yml": (
                {"contents": "read"},
                {"changelog": None},
            ),
            ".github/workflows/greetings.yml": (
                {},
                {
                    "issue-greeting": {
                        "contents": "read",
                        "issues": "write",
                    },
                    "pull-request-greeting": {
                        "contents": "read",
                        "issues": "write",
                    },
                },
            ),
            ".github/workflows/pr-labeler.yml": (
                {},
                {
                    "triage": {
                        "contents": "read",
                        "pull-requests": "write",
                    }
                },
            ),
            ".github/workflows/stale.yml": (
                {},
                {
                    "stale": {
                        "contents": "read",
                        "issues": "write",
                        "pull-requests": "write",
                    }
                },
            ),
            ".github/workflows/tech-stack-version-sync.yml": (
                {"contents": "read"},
                {"drift-gate": {"contents": "read"}},
            ),
        }
        contract = {
            workflow.path: workflow
            for workflow in self.module.load_workflow_contract(ROOT).workflows
        }
        documents = {
            workflow.path: workflow
            for workflow in self.module.load_workflows(ROOT)
        }
        actual_write_owners: set[tuple[str, str, str]] = set()
        for path, (top_level, jobs) in expected.items():
            with self.subTest(path=path):
                self.assertEqual(top_level, contract[path].permissions)
                self.assertEqual(top_level, documents[path].data["permissions"])
                self.assertEqual(set(jobs), set(contract[path].jobs))
                raw_jobs = documents[path].data["jobs"]
                self.assertEqual(set(jobs), set(raw_jobs))
                for job_id, permissions in jobs.items():
                    self.assertEqual(
                        permissions,
                        contract[path].jobs[job_id].permissions,
                    )
                    if permissions is None:
                        self.assertNotIn("permissions", raw_jobs[job_id])
                        continue
                    self.assertIn("permissions", raw_jobs[job_id])
                    self.assertEqual(
                        permissions,
                        raw_jobs[job_id]["permissions"],
                    )
                    actual_write_owners.update(
                        (path, job_id, scope)
                        for scope, access in permissions.items()
                        if access == "write"
                    )
        self.assertEqual(
            {
                (
                    ".github/workflows/greetings.yml",
                    "issue-greeting",
                    "issues",
                ),
                (
                    ".github/workflows/greetings.yml",
                    "pull-request-greeting",
                    "issues",
                ),
                (
                    ".github/workflows/pr-labeler.yml",
                    "triage",
                    "pull-requests",
                ),
                (".github/workflows/stale.yml", "stale", "issues"),
                (
                    ".github/workflows/stale.yml",
                    "stale",
                    "pull-requests",
                ),
            },
            actual_write_owners,
        )

    def test_non_gating_permission_co_mutations_fail_baseline(self) -> None:
        cases = (
            (
                "document-corpus-lifecycle",
                ".github/workflows/document-corpus-lifecycle.yml",
                "      contents: read\n",
                "      contents: read\n      issues: write\n",
                "        permissions: {contents: read}\n",
                "        permissions: {contents: read, issues: write}\n",
            ),
            (
                "generate-changelog",
                ".github/workflows/generate-changelog.yml",
                (
                    "  changelog:\n"
                    "    name: Verify changelog contains release tag\n"
                    "    runs-on: ubuntu-latest\n"
                ),
                (
                    "  changelog:\n"
                    "    name: Verify changelog contains release tag\n"
                    "    permissions:\n"
                    "      issues: write\n"
                    "    runs-on: ubuntu-latest\n"
                ),
                "      changelog:\n        permissions: null\n",
                (
                    "      changelog:\n"
                    "        permissions: {issues: write}\n"
                ),
            ),
            (
                "greetings",
                ".github/workflows/greetings.yml",
                (
                    "  issue-greeting:\n"
                    "    if: github.event_name == 'issues'\n"
                    "    permissions:\n"
                    "      issues: write\n"
                    "      contents: read\n"
                ),
                (
                    "  issue-greeting:\n"
                    "    if: github.event_name == 'issues'\n"
                    "    permissions:\n"
                    "      issues: write\n"
                    "      pull-requests: write\n"
                    "      contents: read\n"
                ),
                (
                    "      issue-greeting:\n"
                    "        permissions:\n"
                    "          issues: write\n"
                    "          contents: read\n"
                ),
                (
                    "      issue-greeting:\n"
                    "        permissions:\n"
                    "          issues: write\n"
                    "          pull-requests: write\n"
                    "          contents: read\n"
                ),
            ),
            (
                "pr-labeler",
                ".github/workflows/pr-labeler.yml",
                (
                    "    permissions:\n"
                    "      contents: read\n"
                    "      pull-requests: write\n"
                ),
                (
                    "    permissions:\n"
                    "      contents: read\n"
                    "      pull-requests: write\n"
                    "      issues: write\n"
                ),
                (
                    "      triage:\n"
                    "        permissions:\n"
                    "          contents: read\n"
                    "          pull-requests: write\n"
                ),
                (
                    "      triage:\n"
                    "        permissions:\n"
                    "          contents: read\n"
                    "          pull-requests: write\n"
                    "          issues: write\n"
                ),
            ),
            (
                "stale",
                ".github/workflows/stale.yml",
                (
                    "    permissions:\n"
                    "      issues: write\n"
                    "      pull-requests: write\n"
                    "      contents: read\n"
                ),
                (
                    "    permissions:\n"
                    "      issues: write\n"
                    "      pull-requests: write\n"
                    "      contents: read\n"
                    "      actions: write\n"
                ),
                (
                    "      stale:\n"
                    "        permissions:\n"
                    "          issues: write\n"
                    "          pull-requests: write\n"
                    "          contents: read\n"
                ),
                (
                    "      stale:\n"
                    "        permissions:\n"
                    "          issues: write\n"
                    "          pull-requests: write\n"
                    "          contents: read\n"
                    "          actions: write\n"
                ),
            ),
            (
                "tech-stack-version-sync",
                ".github/workflows/tech-stack-version-sync.yml",
                (
                    "  drift-gate:\n"
                    "    permissions:\n"
                    "      contents: read\n"
                ),
                (
                    "  drift-gate:\n"
                    "    permissions:\n"
                    "      contents: read\n"
                    "      pull-requests: write\n"
                ),
                (
                    "      drift-gate:\n"
                    "        permissions: {contents: read}\n"
                ),
                (
                    "      drift-gate:\n"
                    "        permissions: {contents: read, pull-requests: write}\n"
                ),
            ),
        )

        for (
            label,
            relative,
            workflow_old,
            workflow_new,
            _contract_old,
            _contract_new,
        ) in cases:
            with self.subTest(label=label), self.workflow_fixture() as root:
                workflow = root / relative
                workflow_text = workflow.read_text(encoding="utf-8")
                self.assertIn(workflow_old, workflow_text)
                workflow.write_text(
                    workflow_text.replace(workflow_old, workflow_new, 1),
                    encoding="utf-8",
                )
                document = self.load_contract_document(root)
                job_id, scope = {
                    "document-corpus-lifecycle": (
                        "document-corpus-lifecycle",
                        "issues",
                    ),
                    "generate-changelog": ("changelog", "issues"),
                    "greetings": ("issue-greeting", "pull-requests"),
                    "pr-labeler": ("triage", "issues"),
                    "stale": ("stale", "actions"),
                    "tech-stack-version-sync": (
                        "drift-gate",
                        "pull-requests",
                    ),
                }[label]
                job = document["workflows"][relative]["jobs"][job_id]
                if job["permissions"] is None:
                    job["permissions"] = {}
                job["permissions"][scope] = "write"
                self.write_contract_document(root, document)
                findings = self.module.validate_workflows(
                    root,
                    self.module.load_workflow_contract(root),
                )
                baseline_findings = [
                    finding
                    for finding in findings
                    if finding.code
                    == "workflow-permission-baseline-invalid"
                ]
                self.assertTrue(baseline_findings)
                self.assertEqual(
                    {"workflow permissions differ from the code baseline"},
                    {finding.message for finding in baseline_findings},
                )

    def test_yaml_parser_fails_closed_on_duplicate_unsafe_and_bounded_inputs(
        self,
    ) -> None:
        cases = ("duplicate-key", "symlink", "parent-symlink", "oversize")
        for label in cases:
            with self.subTest(label=label), self.workflow_fixture() as root:
                workflow = root / ".github/workflows/stale.yml"
                if label == "duplicate-key":
                    text = workflow.read_text(encoding="utf-8")
                    workflow.write_text(
                        text.replace(
                            "name: 'Close Stale Issues & PRs'\n",
                            "name: 'Close Stale Issues & PRs'\nname: duplicate\n",
                            1,
                        ),
                        encoding="utf-8",
                    )
                    expected = "yaml-duplicate-key"
                elif label == "symlink":
                    outside = root / "outside.yml"
                    outside.write_text("private-sentinel: true\n", encoding="utf-8")
                    workflow.unlink()
                    workflow.symlink_to(outside)
                    expected = "yaml-file-unsafe"
                elif label == "parent-symlink":
                    outside = root / "outside-workflows"
                    shutil.copytree(workflow.parent, outside)
                    shutil.rmtree(workflow.parent)
                    workflow.parent.symlink_to(outside, target_is_directory=True)
                    expected = "yaml-file-unsafe"
                else:
                    workflow.write_bytes(
                        b"x" * (self.module.MAX_YAML_BYTES + 1)
                    )
                    expected = "yaml-file-oversize"
                with self.assertRaises(self.module.WorkflowContractError) as raised:
                    self.module.load_workflows(root)
                self.assertEqual(expected, raised.exception.code)
                self.assertNotIn("private-sentinel", raised.exception.message)

    def test_mixed_yaml_on_spellings_are_rejected_as_ambiguous(self) -> None:
        matching_trigger = (
            "on:\n"
            "  push:\n"
            "    branches: [main]\n"
            "  pull_request:\n"
            "    branches: [main]\n"
            "  workflow_dispatch:\n"
        )
        malicious_trigger = (
            "  pull_request_target:\n"
            "    types: [private-trigger-sentinel]\n"
        )
        cases = (
            (
                "quoted-matching-first",
                matching_trigger.replace("on:\n", "'on':\n", 1)
                + "on:\n"
                + malicious_trigger,
            ),
            (
                "unquoted-matching-first",
                matching_trigger
                + "'on':\n"
                + malicious_trigger,
            ),
        )
        for label, replacement in cases:
            with self.subTest(label=label), self.workflow_fixture() as root:
                workflow = root / ".github/workflows/ci-quality.yml"
                text = workflow.read_text(encoding="utf-8")
                self.assertIn(matching_trigger, text)
                workflow.write_text(
                    text.replace(matching_trigger, replacement, 1),
                    encoding="utf-8",
                )
                with self.assertRaises(
                    self.module.WorkflowContractError
                ) as raised:
                    self.module.load_workflows(root)
                self.assertEqual(
                    "workflow-trigger-key-ambiguous",
                    raised.exception.code,
                )
                self.assertNotIn(
                    "private-trigger-sentinel",
                    raised.exception.message,
                )

    def test_trigger_key_parser_preserves_normal_and_rejects_quoted_duplicate(
        self,
    ) -> None:
        workflows = self.module.load_workflows(ROOT)
        ci = next(
            workflow
            for workflow in workflows
            if workflow.path == ".github/workflows/ci-quality.yml"
        )
        self.assertIn("on", ci.data)
        self.assertFalse(
            any(type(key) is bool and key is True for key in ci.data)
        )
        unrelated_value = object()
        normalized: dict[object, object] = {
            False: unrelated_value,
            "unrelated-boolean-value": True,
        }
        self.module._normalize_workflow_trigger_key(
            normalized,
            path=".github/workflows/example.yml",
        )
        self.assertIs(unrelated_value, normalized[False])
        self.assertIs(True, normalized["unrelated-boolean-value"])
        with self.assertRaises(self.module.WorkflowContractError) as invalid:
            self.module._normalize_workflow_trigger_key(
                {True: {"workflow_dispatch": None}},
                path=".github/workflows/example.yml",
            )
        self.assertEqual("workflow-trigger-key-invalid", invalid.exception.code)

        with self.workflow_fixture() as root:
            workflow = root / ".github/workflows/ci-quality.yml"
            text = workflow.read_text(encoding="utf-8")
            workflow.write_text(
                text.replace(
                    "on:\n",
                    "'on':\n  workflow_dispatch:\n'on':\n",
                    1,
                ),
                encoding="utf-8",
            )
            with self.assertRaises(self.module.WorkflowContractError) as raised:
                self.module.load_workflows(root)
        self.assertEqual("yaml-duplicate-key", raised.exception.code)

    def test_bounded_reader_completes_short_regular_file_reads(self) -> None:
        real_read = self.module.os.read

        def short_read(descriptor: int, size: int) -> bytes:
            return real_read(descriptor, min(size, 64))

        with mock.patch.object(self.module.os, "read", side_effect=short_read):
            contract = self.module.load_workflow_contract(ROOT)
        self.assertEqual(2, contract.schema_version)
        self.assertEqual(7, len(contract.workflows))

    def test_contract_rejects_noncanonical_workflow_paths(self) -> None:
        with self.workflow_fixture() as root:
            document = self.load_contract_document(root)
            workflow = document["workflows"].pop(
                ".github/workflows/ci-quality.yml"
            )
            document["workflows"][
                ".github/workflows/../ci-quality.yml"
            ] = workflow
            self.write_contract_document(root, document)
            with self.assertRaises(self.module.WorkflowContractError) as raised:
                self.module.load_workflow_contract(root)
        self.assertEqual("contract-workflow-path-invalid", raised.exception.code)


if __name__ == "__main__":
    unittest.main()
