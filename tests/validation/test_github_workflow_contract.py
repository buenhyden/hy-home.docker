from __future__ import annotations

import dataclasses
import contextlib
import importlib.util
import pathlib
import shutil
import sys
import tempfile
import unittest
from unittest import mock


ROOT = pathlib.Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "scripts/validation/github_workflow_contract.py"
REQUIRED_CI_JOBS = frozenset(
    {
        "docs-traceability",
        "docs-implementation-alignment",
        "repo-contracts",
        "agent-output-eval-fixture-gate",
        "supply-chain-fixture-policy",
        "dependency-vulnerability-audit",
        "git-flow-contract",
        "compose-validation",
        "compose-all-profiles-validation",
        "infrastructure-hardening",
        "template-security-baseline",
        "quickwin-baseline",
        "pre-commit",
        "frontend-quality",
        "storybook-coverage",
        "zizmor",
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
    def setUp(self) -> None:
        self.module = load_contract_module()

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

    def test_ci_quality_retains_sixteen_semantic_job_owners(self) -> None:
        contract = self.module.load_workflow_contract(ROOT)
        ci = next(
            workflow
            for workflow in contract.workflows
            if workflow.path == ".github/workflows/ci-quality.yml"
        )
        self.assertEqual(REQUIRED_CI_JOBS, frozenset(ci.jobs))
        self.assertEqual(16, len(ci.jobs))
        self.assertEqual(16, len(contract.expensive_commands))
        self.assertEqual(
            REQUIRED_CI_JOBS,
            frozenset(owner.job for owner in contract.expensive_commands),
        )

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
        precommit = ci_jobs["pre-commit"]
        steps = precommit["steps"]
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
            steps[1]["uses"],
        )
        self.assertEqual(
            "python -m pip install -r scripts/requirements-pre-commit.txt",
            steps[2]["run"],
        )
        self.assertEqual(
            {
                "name": "Run pre-commit hooks",
                "env": {"SKIP": "eslint-nextjs"},
                "run": "bash scripts/validation/run-ci-precommit.sh",
            },
            steps[3],
        )
        self.assertFalse(
            any(
                "actions/setup-node@" in str(step.get("uses", ""))
                or "npm ci" in str(step.get("run", ""))
                for step in steps
                if isinstance(step, dict)
            )
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

    @contextlib.contextmanager
    def workflow_fixture(self):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            shutil.copytree(ROOT / ".github", root / ".github")
            yield root

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
                "  docs-traceability:\n    permissions:\n      contents: read\n",
                "  docs-traceability:\n    permissions:\n      contents: read\n      issues: read\n",
                "workflow-job-permission-mismatch",
            ),
            (
                "missing-timeout",
                ".github/workflows/ci-quality.yml",
                "  docs-traceability:\n    permissions:\n      contents: read\n    runs-on: ubuntu-latest\n    timeout-minutes: 5\n",
                "  docs-traceability:\n    permissions:\n      contents: read\n    runs-on: ubuntu-latest\n",
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
                    "  repo-contracts:\n"
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
                "        run: bash scripts/validation/check-doc-traceability.sh\n",
                f'        run: echo "${{{{ github.event.pull_request.title }}}}-{sentinel}"\n',
                "workflow-run-interpolation-unsafe",
            ),
        )
        for label, relative, old, new, expected_code in cases:
            with self.subTest(label=label), self.workflow_fixture() as root:
                target = root / relative
                text = target.read_text(encoding="utf-8")
                self.assertIn(old, text)
                target.write_text(text.replace(old, new, 1), encoding="utf-8")
                contract = self.module.load_workflow_contract(root)
                findings = self.module.validate_workflows(root, contract)
                codes = {finding.code for finding in findings}
                self.assertIn(expected_code, codes)
                self.assertNotIn(
                    sentinel,
                    "\n".join(finding.message for finding in findings),
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
            True: {"workflow_dispatch": None},
            False: unrelated_value,
            "unrelated-boolean-value": True,
        }
        self.module._normalize_workflow_trigger_key(
            normalized,
            path=".github/workflows/example.yml",
        )
        self.assertEqual({"workflow_dispatch": None}, normalized["on"])
        self.assertIs(unrelated_value, normalized[False])
        self.assertIs(True, normalized["unrelated-boolean-value"])

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
        self.assertEqual(1, contract.schema_version)
        self.assertEqual(7, len(contract.workflows))

    def test_contract_rejects_noncanonical_workflow_paths(self) -> None:
        with self.workflow_fixture() as root:
            contract_path = root / ".github/workflow-contract.yml"
            text = contract_path.read_text(encoding="utf-8")
            contract_path.write_text(
                text.replace(
                    ".github/workflows/ci-quality.yml:",
                    ".github/workflows/../ci-quality.yml:",
                    1,
                ),
                encoding="utf-8",
            )
            with self.assertRaises(self.module.WorkflowContractError) as raised:
                self.module.load_workflow_contract(root)
        self.assertEqual("contract-workflow-path-invalid", raised.exception.code)


if __name__ == "__main__":
    unittest.main()
