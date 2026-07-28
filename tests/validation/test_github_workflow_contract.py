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
            aggregate = root / "scripts/validation/check-repo-contracts.sh"
            aggregate.parent.mkdir(parents=True)
            shutil.copy2(
                ROOT / "scripts/validation/check-repo-contracts.sh",
                aggregate,
            )
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

    def test_required_permission_contract_co_mutations_fail_baseline(
        self,
    ) -> None:
        required_job_workflow = (
            "  docs-traceability:\n"
            "    permissions:\n"
            "      contents: read\n"
        )
        required_job_contract = (
            "      docs-traceability:\n"
            "        permissions: {contents: read}\n"
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
                required_job_contract,
                required_job_contract.replace(
                    "contents: read",
                    "contents: write",
                ),
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
                    required_job_contract,
                    required_job_contract.replace(
                        "{contents: read}",
                        f"{{contents: read, {scope}: write}}",
                    ),
                )
            )
        cases.append(
            (
                "zizmor-extra-write",
                (
                    "    permissions:\n"
                    "      security-events: write\n"
                    "      actions: read\n"
                    "      contents: read\n"
                ),
                (
                    "    permissions:\n"
                    "      security-events: write\n"
                    "      actions: read\n"
                    "      contents: read\n"
                    "      packages: write\n"
                ),
                (
                    "      zizmor:\n"
                    "        permissions:\n"
                    "          security-events: write\n"
                    "          actions: read\n"
                    "          contents: read\n"
                ),
                (
                    "      zizmor:\n"
                    "        permissions:\n"
                    "          security-events: write\n"
                    "          actions: read\n"
                    "          contents: read\n"
                    "          packages: write\n"
                ),
            )
        )

        for (
            label,
            workflow_old,
            workflow_new,
            contract_old,
            contract_new,
        ) in cases:
            with self.subTest(label=label), self.workflow_fixture() as root:
                workflow = root / ".github/workflows/ci-quality.yml"
                workflow_text = workflow.read_text(encoding="utf-8")
                contract_path = root / ".github/workflow-contract.yml"
                contract_text = contract_path.read_text(encoding="utf-8")
                self.assertIn(workflow_old, workflow_text)
                self.assertIn(contract_old, contract_text)
                workflow.write_text(
                    workflow_text.replace(workflow_old, workflow_new, 1),
                    encoding="utf-8",
                )
                contract_path.write_text(
                    contract_text.replace(contract_old, contract_new, 1),
                    encoding="utf-8",
                )
                contract = self.module.load_workflow_contract(root)
                findings = self.module.validate_workflows(root, contract)
                self.assertIn(
                    "workflow-permission-baseline-invalid",
                    {finding.code for finding in findings},
                )

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
            "tests.validation.test_agent_governance_ci_routing",
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
                    contract_path = root / ".github/workflow-contract.yml"
                    contract_data = self.module.yaml.safe_load(
                        contract_path.read_text(encoding="utf-8")
                    )
                    contract_data["actions"].append(
                        {
                            "action": action,
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
                    )
                    contract_data["actions"].sort(
                        key=lambda record: record["action"]
                    )
                    contract_path.write_text(
                        self.module.yaml.safe_dump(
                            contract_data,
                            sort_keys=False,
                        ),
                        encoding="utf-8",
                    )
                    expected = "action-registry-baseline-invalid"
                else:
                    step += "./.github/actions/private-probe\n"
                    expected = "action-local-reference-forbidden"
                anchor = "      - name: Check docs traceability sync\n"
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
            contract_old,
            contract_new,
        ) in cases:
            with self.subTest(label=label), self.workflow_fixture() as root:
                workflow = root / relative
                workflow_text = workflow.read_text(encoding="utf-8")
                contract_path = root / ".github/workflow-contract.yml"
                contract_text = contract_path.read_text(encoding="utf-8")
                self.assertIn(workflow_old, workflow_text)
                self.assertIn(contract_old, contract_text)
                workflow.write_text(
                    workflow_text.replace(workflow_old, workflow_new, 1),
                    encoding="utf-8",
                )
                contract_path.write_text(
                    contract_text.replace(contract_old, contract_new, 1),
                    encoding="utf-8",
                )
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
