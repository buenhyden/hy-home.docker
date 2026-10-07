from __future__ import annotations

import contextlib
import copy
import dataclasses
import importlib.util
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

from scripts.lib.gate import ci_gate_contract as gate_contract

ROOT = pathlib.Path(__file__).resolve().parents[3]
MODULE_PATH = ROOT / "scripts/lib/gate/github_workflow_contract.py"

REQUIRED_CI_JOBS = frozenset(
    {
        "candidate-quality",
        "main-security",
    }
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
    def test_archive_adoption_regressions_are_required_by_public_gate(self) -> None:
        document = gate_contract.load_contract_document(ROOT)
        gate = next(
            node
            for node in document["gate_nodes"]
            if node["gate_id"] == "leaf.document-governance-library-regressions"
        )
        for module in (
            "archive_assessments",
            "archive_snapshots",
            "archive_catalog_contract",
        ):
            self.assertIn(f"tests.lib.document_governance.test_{module}", gate["argv"])

    def test_optional_runtime_skips_keep_all_required_module_selectors(self) -> None:
        document = gate_contract.load_contract_document(ROOT)
        gate = next(
            node
            for node in document["gate_nodes"]
            if node["gate_id"] == "leaf.compose-baseline-regressions"
        )
        arguments = gate["argv"]
        boundary = arguments.index("--optional-runtime-skips")
        self.assertEqual(
            [
                "tests.validation.test_compose_baseline_gates",
                "tests.validation.test_dev_data_boundary",
                "tests.validation.test_dev_pg_provision",
                "tests.validation.test_dev_valkey_acl",
                "tests.validation.test_lab_credential_argv",
                "tests.validation.test_infra_tier_layout",
                "tests.validation.test_openwebui_oidc_entrypoint",
                "tests.validation.test_gatus_oidc",
                "tests.validation.test_mng_pg_init_sql",
                "tests.validation.test_config_mount_hashes",
                "tests.validation.test_service_wiring_contracts",
                "tests.validation.test_service_runtime_compatibility",
                "tests.validation.test_perf_db_contract",
                "tests.validation.test_k6_results",
                "tests.validation.test_quality_mock_lab",
                "tests.validation.test_quality_observability",
                "tests.validation.test_quality_object_store",
                "tests.validation.test_quality_raw_points",
                "tests.validation.test_locust_telemetry",
            ],
            arguments[1:boundary],
        )
        self.assertEqual(5, len(arguments[boundary + 1 : -1]))
        self.assertTrue(
            all(
                scope.rsplit(".", 1)[0] in arguments[1:boundary]
                for scope in arguments[boundary + 1 : -1]
            )
        )
        self.assertEqual([], gate["allowed_env_keys"])

    def setUp(self) -> None:
        self.module = load_contract_module()

    def test_quality_workflow_has_one_remote_candidate_route(self) -> None:
        workflow = next(
            workflow
            for workflow in self.module.load_workflows(ROOT)
            if workflow.path == ".github/workflows/ci-quality.yml"
        )
        document = self.load_contract_document(ROOT)

        self.assertEqual(
            {
                "branches": ["main"],
                "types": ["opened", "synchronize", "reopened"],
            },
            workflow.data["on"]["pull_request"],
        )
        self.assertNotIn("workflow_dispatch", workflow.data["on"])
        self.assertEqual(REQUIRED_CI_JOBS, set(workflow.data["jobs"]))
        candidate = workflow.data["jobs"]["candidate-quality"]
        self.assertEqual({"contents": "read"}, candidate["permissions"])
        self.assertEqual(
            "github.event_name == 'pull_request'",
            candidate["if"],
        )
        self.assertEqual(
            {
                "EVENT_NAME": "pull_request",
                "PR_BASE_SHA": "${{ github.event.pull_request.base.sha }}",
                "PR_HEAD_SHA": "${{ github.event.pull_request.head.sha }}",
            },
            candidate["env"],
        )
        self.assertEqual(
            1,
            sum(
                step.get("run")
                == "python3 scripts/validation/run-ci-gate.py --profile changed"
                for step in candidate["steps"]
                if isinstance(step, dict)
            ),
        )
        quality_contract = document["workflows"][".github/workflows/ci-quality.yml"]
        self.assertEqual(
            workflow.data["on"]["pull_request"],
            quality_contract["triggers"]["pull_request"],
        )
        self.assertNotIn("workflow_dispatch", quality_contract["triggers"])
        self.assertEqual(REQUIRED_CI_JOBS, set(quality_contract["jobs"]))

    def test_quality_workflow_concurrency_separates_event_types(self) -> None:
        expected_group = "${{ github.workflow }}-${{ github.event_name }}-${{ github.event.pull_request.number || github.ref }}"
        workflow = next(
            workflow
            for workflow in self.module.load_workflows(ROOT)
            if workflow.path == ".github/workflows/ci-quality.yml"
        )
        document = self.load_contract_document(ROOT)
        contract = document["workflows"][".github/workflows/ci-quality.yml"]

        self.assertEqual(expected_group, workflow.data["concurrency"]["group"])
        self.assertIs(True, workflow.data["concurrency"]["cancel-in-progress"])
        self.assertEqual(expected_group, contract["concurrency"]["group"])
        self.assertIs(True, contract["concurrency"]["cancel-in-progress"])

    def test_public_plans_run_precommit_before_expensive_gates_without_loss(
        self,
    ) -> None:
        document = self.load_contract_document(ROOT)
        public = gate_contract.parse_public_gate_contract(document)
        registry = self.module.load_workflow_contract(ROOT).gate_registry
        changed_style = next(
            node for node in registry.nodes if node.gate_id == "leaf.changed-style"
        )
        self.assertEqual(
            ("--mode", "pr-merge"),
            changed_style.argv,
        )
        changed_paths = (".github/workflows/ci-quality.yml",)
        suites = gate_contract.select_public_suites(public, "changed", changed_paths)
        changed = gate_contract.expand_public_gate_ids(
            registry,
            gate_contract.public_root_gate_ids(
                public, suites, changed_paths=changed_paths
            ),
        )
        self.assertIn("leaf.changed-style", changed)
        self.assertIn("leaf.commit-message-contract", changed)
        self.assertIn("leaf.zizmor", changed)
        self.assertNotIn("leaf.dependency-vulnerability-audit", changed)
        self.assertNotIn("leaf.frontend-build", changed)

        full = gate_contract.expand_public_gate_ids(registry, registry.public_roots)
        positions = {gate_id: index for index, gate_id in enumerate(full)}
        for gate_id in (
            "leaf.dependency-vulnerability-audit",
            "leaf.frontend-build",
            "leaf.storybook-coverage",
            "leaf.zizmor",
        ):
            self.assertLess(positions["leaf.changed-style"], positions[gate_id])

    def test_storybook_shell_accepts_typed_full_route_direct_and_held(self) -> None:
        script = ROOT / "scripts/validation/check-storybook-contract.sh"
        env = {key: value for key, value in os.environ.items() if key != "PYTHONPATH"}
        env["PYTHONSAFEPATH"] = "1"
        with script.open("rb") as held:
            for path in (str(script), f"/proc/self/fd/{held.fileno()}"):
                with self.subTest(path=path):
                    result = subprocess.run(
                        ["bash", path],
                        cwd=ROOT,
                        env=env,
                        pass_fds=(held.fileno(),),
                        capture_output=True,
                        text=True,
                        check=False,
                    )
                    self.assertEqual(0, result.returncode, result.stderr)

    def test_storybook_shell_rejects_lost_routes_and_changed_quality_contracts(
        self,
    ) -> None:
        for case in (
            "public-route",
            "full-child",
            "npm-argv",
            "threshold",
        ):
            with self.subTest(case=case), self.workflow_fixture() as root:
                subprocess.run(["git", "init", "-q", str(root)], check=True)
                (root / "tests/validation").mkdir(parents=True)
                shutil.copy2(
                    ROOT / "tests/validation/test_run_ci_precommit.sh",
                    root / "tests/validation/test_run_ci_precommit.sh",
                )
                subprocess.run(
                    ["git", "-C", str(root), "add", "scripts", ".github", "tests"],
                    check=True,
                )
                project = root / "projects/storybook/nextjs"
                project.mkdir(parents=True)
                for name in (
                    "package.json",
                    "vitest.config.ts",
                    ".storybook/main.ts",
                    "packages/ui/package.json",
                ):
                    target = project / name
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(ROOT / "projects/storybook/nextjs" / name, target)
                command = [
                    "bash",
                    str(root / "scripts/validation/check-storybook-contract.sh"),
                ]
                baseline = subprocess.run(
                    command, cwd=root, capture_output=True, text=True, check=False
                )
                self.assertEqual(0, baseline.returncode, baseline.stderr)
                if case == "threshold":
                    path = project / "vitest.config.ts"
                    text = path.read_text(encoding="utf-8")
                    self.assertIn("statements: 90", text)
                    path.write_text(
                        text.replace("statements: 90", "statements: 80", 1),
                        encoding="utf-8",
                    )
                else:
                    data = self.load_contract_document(root)
                    if case == "public-route":
                        data["public_gate"]["suite_roots"][
                            "repository-integrity"
                        ].remove("ci.storybook-coverage")
                    else:
                        node = next(
                            node
                            for node in data["gate_nodes"]
                            if node["gate_id"]
                            == (
                                "ci.storybook-coverage"
                                if case == "full-child"
                                else "leaf.storybook-coverage"
                            )
                        )
                        if case == "full-child":
                            node["children"].remove("leaf.storybook-coverage")
                        else:
                            node["argv"][2] = "test"
                    self.write_contract_document(root, data)
                result = subprocess.run(
                    command, cwd=root, capture_output=True, text=True, check=False
                )
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
                "python3 scripts/lib/gate/ci_gate_adapters.py run-zizmor-sarif",
                "python3 -m pip install -r scripts/requirements.txt -r scripts/requirements-pre-commit.txt",
                'python3 scripts/validation/run-ci-gate.py --profile changed --requirements >> "$GITHUB_OUTPUT"',
                "docker version",
                "python3 scripts/validation/run-ci-gate.py --profile changed",
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
        self.assertEqual(set(), set(local_entries))

        active_surfaces = "\n".join(
            (ROOT / path).read_text(encoding="utf-8")
            for path in (
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
                self.assertEqual(
                    fields, tuple(field.name for field in dataclasses.fields(cls))
                )

    def test_repository_workflows_match_the_exact_contract(self) -> None:
        contract = self.module.load_workflow_contract(ROOT)
        workflows = self.module.load_workflows(ROOT)
        # Derived, not pinned: the loaded set is exactly the tracked workflow
        # files, so adding or removing one needs no edit here.
        on_disk = {
            path.relative_to(ROOT).as_posix()
            for path in (ROOT / ".github/workflows").glob("*.yml")
        }
        self.assertEqual(on_disk, {document.path for document in workflows})
        self.assertEqual((), self.module.validate_workflows(ROOT, contract))

    def test_ci_installs_each_frontend_dependency_tree_once(self) -> None:
        contract = self.module.load_workflow_contract(ROOT)
        nodes = {node.gate_id: node for node in contract.gate_registry.nodes}
        selected = gate_contract.expand_public_gate_ids(
            contract.gate_registry,
            contract.gate_registry.public_roots,
        )
        installers = [
            nodes[key]
            for key in selected
            if nodes[key].argv
            == ("run-npm", "ci", "--prefix", "projects/storybook/nextjs")
        ]
        self.assertEqual(1, len(installers))

    def test_greeting_write_scope_matches_comment_target(self) -> None:
        workflow = next(
            document
            for document in self.module.load_workflows(ROOT)
            if document.path == ".github/workflows/greetings.yml"
        )
        self.assertEqual(
            {"contents": "read", "issues": "write", "pull-requests": "read"},
            workflow.data["jobs"]["issue-greeting"]["permissions"],
        )
        self.assertEqual(
            {"contents": "read", "issues": "read", "pull-requests": "write"},
            workflow.data["jobs"]["pull-request-greeting"]["permissions"],
        )

    def test_contract_uses_one_environment_free_compose_leaf(self) -> None:
        contract = self.module.load_workflow_contract(ROOT)
        nodes = {node.gate_id: node for node in contract.gate_registry.nodes}
        compose = [
            node
            for node in nodes.values()
            if str(node.entrypoint) == "scripts/validation/validate-docker-compose.sh"
        ]
        self.assertEqual(
            ["leaf.compose-validation"],
            [node.gate_id for node in compose],
        )
        self.assertEqual((), compose[0].allowed_env_keys)
        self.assertIn(
            "leaf.compose-validation",
            nodes["local.compose-validation"].children,
        )
        self.assertIn(
            "local.compose-validation",
            contract.gate_registry.public_roots,
        )

    def test_required_quality_jobs_do_not_inherit_compose_selection(self) -> None:
        workflow = next(
            item
            for item in self.module.load_workflows(ROOT)
            if item.path == ".github/workflows/ci-quality.yml"
        )
        self.assertEqual(REQUIRED_CI_JOBS, set(workflow.data["jobs"]))
        self.assertNotIn("env", workflow.data)
        self.assertEqual(
            {
                "EVENT_NAME": "pull_request",
                "PR_BASE_SHA": "${{ github.event.pull_request.base.sha }}",
                "PR_HEAD_SHA": "${{ github.event.pull_request.head.sha }}",
            },
            workflow.data["jobs"]["candidate-quality"]["env"],
        )
        self.assertNotIn("HYHOME_COMPOSE_PROFILES", str(workflow.data))

    def test_required_workflow_rejects_inherited_compose_selection(self) -> None:
        contract = self.module.load_workflow_contract(ROOT)
        documents = self.module.load_workflows(ROOT)
        document = next(
            item
            for item in documents
            if item.path == ".github/workflows/ci-quality.yml"
        )
        data = copy.deepcopy(document.data)
        data["env"] = {"HYHOME_COMPOSE_PROFILES": "core data obs workflow"}
        changed = dataclasses.replace(document, data=data)

        with mock.patch.object(
            self.module,
            "load_workflows",
            return_value=tuple(
                changed if item.path == document.path else item for item in documents
            ),
        ):
            codes = {
                finding.code
                for finding in self.module.validate_workflows(ROOT, contract)
            }
        self.assertIn("workflow-gate-environment-invalid", codes)

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
        declared = self.load_contract_document(ROOT)["gate_nodes"]
        self.assertEqual(len(declared), len(contract.gate_registry.nodes))
        public = self.module.parse_public_gate_contract(
            self.load_contract_document(ROOT)
        )
        self.assertEqual(("changed", "full"), public.profile_names)
        self.assertEqual(
            self.module.public_root_gate_ids(public, public.suite_names),
            contract.gate_registry.public_roots,
        )
        self.assertEqual(
            (),
            self.module.validate_gate_registry(ROOT, contract.gate_registry),
        )
        expanded = gate_contract.expand_public_gate_ids(
            contract.gate_registry,
            contract.gate_registry.public_roots,
        )
        self.assertTrue(expanded)
        self.assertEqual(len(expanded), len(set(expanded)))

    def test_schema_v1_and_duplicate_command_authority_fail_closed(
        self,
    ) -> None:
        self.assertFalse(hasattr(self.module, "ExpensiveCommandOwner"))
        self.assertFalse(hasattr(self.module, "_EXPENSIVE_COMMAND_BASELINE"))
        document = json.loads(
            (ROOT / ".github/workflow-contract.yml").read_text(encoding="utf-8")
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
            record.split(b"\t", 1)[1].decode("utf-8"): record.split(b" ", 1)[0].decode(
                "ascii"
            )
            for record in result.stdout.rstrip(b"\0").split(b"\0")
        }
        self.assertEqual(set(entrypoints), set(modes))
        self.assertEqual({"100755"}, set(modes.values()))

    def test_action_evidence_date_is_a_real_nonfuture_iso_date(self) -> None:
        self.assertTrue(self.module._valid_retrieval_date("2026-09-02"))
        self.assertTrue(self.module._valid_retrieval_date("2026-09-19"))
        for value in ("", "2026-99-01", "2026-02-30", "9999-01-01", "2026-9-2"):
            with self.subTest(value=value):
                self.assertFalse(self.module._valid_retrieval_date(value))

    def test_action_registry_and_ci_precommit_wiring_are_exact(self) -> None:
        contract = self.module.load_workflow_contract(ROOT)
        self.assertEqual(8, len(contract.actions))
        self.assertEqual(
            {"node24"},
            {action.runtime for action in contract.actions},
        )
        for action in contract.actions:
            with self.subTest(action=action.action):
                self.assertTrue(self.module._valid_retrieval_date(action.retrieved_at))
                self.assertIn(f"/{action.sha}/", action.manifest_url)
                self.assertEqual("approved-node24", action.security_disposition)

        workflows = {
            workflow.path: workflow for workflow in self.module.load_workflows(ROOT)
        }
        ci_jobs = workflows[".github/workflows/ci-quality.yml"].data["jobs"]
        self.assertIsInstance(ci_jobs, dict)
        security_steps = ci_jobs["main-security"]["steps"]
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
            security_steps[1]["uses"],
        )
        setup_uv = next(
            f"{action.action}@{action.sha}"
            for action in contract.actions
            if action.action == "astral-sh/setup-uv"
        )
        self.assertEqual(setup_uv, security_steps[2]["uses"])
        self.assertEqual(
            "python3 scripts/lib/gate/ci_gate_adapters.py run-zizmor-sarif",
            security_steps[3]["run"],
        )
        self.assertIn("github/codeql-action/upload-sarif@", security_steps[4]["uses"])
        self.assertEqual(
            "pre-commit==4.6.1\ncommitizen==4.15.1\n",
            (ROOT / "scripts/requirements-pre-commit.txt").read_text(encoding="utf-8"),
        )

    def test_forbidden_trigger_and_action_mutations_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            shutil.copytree(ROOT / ".github", root / ".github")
            workflow = root / ".github/workflows/ci-quality.yml"
            text = workflow.read_text(encoding="utf-8")
            text = text.replace(
                "on:\n  push:\n",
                "on:\n  pull_request_target:\n  push:\n",
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
            workflow.path: workflow for workflow in module.load_workflows(root)
        }
        jobs = workflows[".github/workflows/ci-quality.yml"].data["jobs"]
        if not isinstance(jobs, dict):
            raise AssertionError("required-quality jobs must be a mapping")
        return jobs

    def test_only_registered_run_conditions_are_admitted(self) -> None:
        jobs = self._required_quality_jobs(self.module, ROOT)
        self.assertEqual(
            {
                "candidate-quality": "github.event_name == 'pull_request'",
                "main-security": "github.event_name == 'push' && github.ref == 'refs/heads/main'",
            },
            {job_id: job["if"] for job_id, job in jobs.items()},
        )
        conditioned_steps = [
            (job_id, step.get("name"), step["if"])
            for job_id, job in jobs.items()
            for step in job.get("steps", [])
            if isinstance(step, dict) and "run" in step and "if" in step
        ]
        self.assertEqual(
            [
                (
                    "candidate-quality",
                    "Verify selected Docker prerequisite",
                    "steps.prerequisites.outputs.docker == 'true'",
                )
            ],
            conditioned_steps,
        )

    def test_required_quality_jobs_have_exact_registered_checkout(self) -> None:
        contract = self.module.load_workflow_contract(ROOT)
        jobs = self._required_quality_jobs(self.module, ROOT)
        checkout = next(
            action for action in contract.actions if action.action == "actions/checkout"
        )
        expected_checkout = {
            "name": "Checkout repository",
            "uses": f"actions/checkout@{checkout.sha}",
            "with": {"persist-credentials": False, "fetch-depth": 0},
        }
        for job_id, job in jobs.items():
            with self.subTest(job_id=job_id):
                self.assertEqual(expected_checkout, job["steps"][0])

    def test_main_security_is_independent_from_candidate_validation(self) -> None:
        jobs = self._required_quality_jobs(self.module, ROOT)
        security = jobs["main-security"]
        candidate = jobs["candidate-quality"]
        self.assertNotIn("needs", security)
        self.assertNotIn("needs", candidate)
        self.assertEqual(
            {"contents": "read", "security-events": "write"}, security["permissions"]
        )
        self.assertEqual({"contents": "read"}, candidate["permissions"])
        self.assertEqual(
            ["python3 scripts/lib/gate/ci_gate_adapters.py run-zizmor-sarif"],
            [step["run"] for step in security["steps"] if "run" in step],
        )
        self.assertEqual(
            1,
            sum(
                step.get("run")
                == "python3 scripts/validation/run-ci-gate.py --profile changed"
                for step in candidate["steps"]
            ),
        )
        self.assertTrue(
            any("upload-sarif@" in step.get("uses", "") for step in security["steps"])
        )
        document = next(
            item
            for item in self.module.load_workflows(ROOT)
            if item.path == ".github/workflows/ci-quality.yml"
        )
        contract = self.module.load_workflow_contract(ROOT)
        cases = (
            (
                "candidate-dependency",
                "candidate-quality",
                lambda job: job.update({"needs": "main-security"}),
                "workflow-gate-dependency-invalid",
            ),
            (
                "security-sarif-upload",
                "main-security",
                lambda job: job["steps"].pop(),
                "workflow-gate-projection-mismatch",
            ),
            (
                "security-setup-uv",
                "main-security",
                lambda job: job["steps"].pop(2),
                "workflow-gate-projection-mismatch",
            ),
            (
                "security-condition",
                "main-security",
                lambda job: job.update({"if": "false"}),
                "workflow-gate-execution-context-invalid",
            ),
            (
                "security-continue-on-error",
                "main-security",
                lambda job: job.update({"continue-on-error": True}),
                "workflow-gate-execution-context-invalid",
            ),
            (
                "candidate-continue-on-error",
                "candidate-quality",
                lambda job: job.update({"continue-on-error": True}),
                "workflow-gate-execution-context-invalid",
            ),
            (
                "candidate-validation",
                "candidate-quality",
                lambda job: job["steps"].pop(),
                "workflow-gate-projection-mismatch",
            ),
            (
                "security-checkout-order",
                "main-security",
                lambda job: job["steps"].insert(1, job["steps"].pop(0)),
                "workflow-gate-projection-mismatch",
            ),
            (
                "security-command-injection",
                "main-security",
                lambda job: job["steps"][3].update({"run": "bash -c true"}),
                "workflow-gate-projection-mismatch",
            ),
        )
        for label, job_id, mutation, expected in cases:
            with self.subTest(label=label):
                data = copy.deepcopy(document.data)
                mutation(data["jobs"][job_id])
                findings = self.module._workflow_projection_findings(
                    document.path, data, data["jobs"], contract
                )
                self.assertIn(expected, {finding.code for finding in findings})

    def test_legacy_profile_root_substitution_fails_closed(self) -> None:
        with self.workflow_fixture() as root:
            document = self.load_contract_document(root)
            document["profile_roots"] = []
            self.write_contract_document(root, document)
            with self.assertRaises(self.module.WorkflowContractError) as caught:
                self.module.load_workflow_contract(root)
        self.assertEqual("ci-gate-document-fields", caught.exception.code)

    def test_local_full_public_profile_owns_storybook_setup_and_coverage(
        self,
    ) -> None:
        contract = self.module.load_workflow_contract(ROOT)
        document = self.load_contract_document(ROOT)
        public = self.module.parse_public_gate_contract(document)
        self.assertEqual(("changed", "full"), public.profile_names)
        self.assertEqual(
            public.suite_names,
            self.module.select_public_suites(public, "full", ()),
        )
        self.assertIn(
            "ci.storybook-coverage",
            document["public_gate"]["suite_roots"]["repository-integrity"],
        )
        expanded = gate_contract.expand_public_gate_ids(
            contract.gate_registry,
            ("ci.storybook-coverage",),
        )
        self.assertEqual(
            (
                "setup.frontend-node-dependencies",
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
            (root / ".github/workflow-contract.yml").read_text(encoding="utf-8")
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

    def test_security_and_ownership_mutation_matrix_fails_closed(self) -> None:
        sentinel = "private-workflow-sentinel"
        cases = (
            (
                "pull-request-target",
                ".github/workflows/ci-quality.yml",
                "on:\n",
                "on:\n  pull_request_target:\n",
                "workflow-trigger-forbidden",
            ),
            (
                "workflow-call",
                ".github/workflows/ci-quality.yml",
                "on:\n",
                "on:\n  workflow_call:\n",
                "workflow-trigger-forbidden",
            ),
            (
                "workflow-run",
                ".github/workflows/ci-quality.yml",
                "on:\n",
                "on:\n  workflow_run:\n",
                "workflow-trigger-forbidden",
            ),
            (
                "event-widening",
                ".github/workflows/ci-quality.yml",
                "on:\n",
                "on:\n  issues:\n    types: [opened]\n",
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
                ".github/workflows/ci-quality.yml",
                "    branches: [main]\n",
                "    branches: [main]\n    paths: ['.github/**']\n",
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
                "  main-security:\n    if: github.event_name == 'push' && github.ref == 'refs/heads/main'\n    permissions:\n      contents: read\n      security-events: write\n",
                "  main-security:\n    if: github.event_name == 'push' && github.ref == 'refs/heads/main'\n    permissions:\n      contents: read\n      security-events: write\n      issues: read\n",
                "workflow-job-permission-mismatch",
            ),
            (
                "missing-timeout",
                ".github/workflows/ci-quality.yml",
                "  main-security:\n    if: github.event_name == 'push' && github.ref == 'refs/heads/main'\n    permissions:\n      contents: read\n      security-events: write\n    runs-on: ubuntu-latest\n    timeout-minutes: 15\n",
                "  main-security:\n    if: github.event_name == 'push' && github.ref == 'refs/heads/main'\n    permissions:\n      contents: read\n      security-events: write\n    runs-on: ubuntu-latest\n",
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
                ".github/workflows/stale.yml",
                "jobs:\n  stale:\n",
                (
                    "jobs:\n"
                    "  main-security:\n"
                    "    permissions:\n"
                    "      contents: read\n"
                    "    runs-on: ubuntu-latest\n"
                    "    timeout-minutes: 5\n"
                    "    steps: []\n"
                    "  stale:\n"
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
                "        run: python3 scripts/lib/gate/ci_gate_adapters.py run-zizmor-sarif\n",
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
            "  main-security:\n"
            "    if: github.event_name == 'push' && github.ref == 'refs/heads/main'\n"
            "    permissions:\n"
            "      contents: read\n"
            "      security-events: write\n"
        )
        cases = [
            (
                "top-contents-write",
                "permissions:\n  contents: read\n\nconcurrency:\n",
                "permissions:\n  contents: write\n\nconcurrency:\n",
                ("    permissions:\n      contents: read\n    concurrency:\n"),
                ("    permissions:\n      contents: write\n    concurrency:\n"),
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
                ci = document["workflows"][".github/workflows/ci-quality.yml"]
                if label == "top-contents-write":
                    ci["permissions"]["contents"] = "write"
                else:
                    permissions = ci["jobs"]["main-security"]["permissions"]
                    if label == "job-contents-write":
                        permissions["contents"] = "write"
                    else:
                        permissions[
                            label.removeprefix("job-").removesuffix("-write")
                        ] = "write"
                self.write_contract_document(root, document)
                contract = self.module.load_workflow_contract(root)
                findings = self.module.validate_workflows(root, contract)
                self.assertIn(
                    "workflow-required-permission-invalid",
                    {finding.code for finding in findings},
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
                with self.assertRaises(self.module.WorkflowContractError) as raised:
                    self.module.load_workflows(root)
                self.assertEqual(
                    "workflow-trigger-key-invalid",
                    raised.exception.code,
                )

    def test_action_registry_and_local_action_policy_fail_closed(self) -> None:
        cases = ("local-action",)
        for label in cases:
            with self.subTest(label=label), self.workflow_fixture() as root:
                workflow = root / ".github/workflows/ci-quality.yml"
                text = workflow.read_text(encoding="utf-8")
                step = "      - name: Additional Action probe\n        uses: "
                if label == "eighth-registered-action":
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
                        "retrieved_at": "2026-09-02",
                        "consumers": [".github/workflows/ci-quality.yml"],
                        "security_disposition": "approved-node24",
                    }
                    contract_data["actions"] = dict(
                        sorted(contract_data["actions"].items())
                    )
                    self.write_contract_document(root, contract_data)
                    expected = "workflow-gate-projection-mismatch"
                else:
                    step += "./.github/actions/private-probe\n"
                    expected = "action-local-reference-forbidden"
                anchor = "      - name: Audit merged workflow revision\n"
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
            ".github/workflows/generate-changelog.yml": (
                {"contents": "read"},
                {"release": {"contents": "write"}},
            ),
            ".github/workflows/greetings.yml": (
                {},
                {
                    "issue-greeting": {
                        "contents": "read",
                        "issues": "write",
                        "pull-requests": "read",
                    },
                    "pull-request-greeting": {
                        "contents": "read",
                        "issues": "read",
                        "pull-requests": "write",
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
        }
        contract = {
            workflow.path: workflow
            for workflow in self.module.load_workflow_contract(ROOT).workflows
        }
        documents = {
            workflow.path: workflow for workflow in self.module.load_workflows(ROOT)
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
                    ".github/workflows/generate-changelog.yml",
                    "release",
                    "contents",
                ),
                (
                    ".github/workflows/greetings.yml",
                    "issue-greeting",
                    "issues",
                ),
                (
                    ".github/workflows/greetings.yml",
                    "pull-request-greeting",
                    "pull-requests",
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
                    workflow.write_bytes(b"x" * (self.module.MAX_YAML_BYTES + 1))
                    expected = "yaml-file-oversize"
                with self.assertRaises(self.module.WorkflowContractError) as raised:
                    self.module.load_workflows(root)
                self.assertEqual(expected, raised.exception.code)
                self.assertNotIn("private-sentinel", raised.exception.message)

    def test_mixed_yaml_on_spellings_are_rejected_as_ambiguous(self) -> None:
        matching_trigger = "on:\n  push:\n    branches: [main]\n"
        malicious_trigger = (
            "  pull_request_target:\n    types: [private-trigger-sentinel]\n"
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
                matching_trigger + "'on':\n" + malicious_trigger,
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
                with self.assertRaises(self.module.WorkflowContractError) as raised:
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
        self.assertFalse(any(type(key) is bool and key is True for key in ci.data))
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
        self.assertEqual(
            len(list((ROOT / ".github/workflows").glob("*.yml"))),
            len(contract.workflows),
        )

    def test_contract_rejects_noncanonical_workflow_paths(self) -> None:
        with self.workflow_fixture() as root:
            document = self.load_contract_document(root)
            workflow = document["workflows"].pop(".github/workflows/ci-quality.yml")
            document["workflows"][".github/workflows/../ci-quality.yml"] = workflow
            self.write_contract_document(root, document)
            with self.assertRaises(self.module.WorkflowContractError) as raised:
                self.module.load_workflow_contract(root)
        self.assertEqual("contract-workflow-path-invalid", raised.exception.code)


if __name__ == "__main__":
    unittest.main()
