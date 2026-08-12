from __future__ import annotations

import ast
import contextlib
import importlib.util
import json
import os
import pathlib
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest

import yaml


ROOT = pathlib.Path(__file__).resolve().parents[2]
RECOMMENDER = ROOT / "scripts/validation/recommend-qa-gates.sh"
PRE_COMMIT = ROOT / ".pre-commit-config.yaml"
WORKFLOW = ROOT / ".github/workflows/ci-quality.yml"
GITHUB_INDEX = ROOT / ".github/INDEX.md"
GITHUB_README = ROOT / ".github/README.md"
MAIN_PROTECTION = ROOT / ".github/rulesets/main-protection.md"
GITHUB_GOVERNANCE = (
    ROOT / "docs/00.agent-governance/rules/github-governance.md"
)
ARTIFACT_CONTRACT = (
    ROOT / "docs/00.agent-governance/contracts/agent-governance-artifacts.yaml"
)
GITHUB_OBSERVATION = (
    ROOT
    / "docs/90.references/data/governance/"
    "github-actions-control-plane-observation.yaml"
)
CODEOWNERS = ROOT / ".github/CODEOWNERS"
LABELER = ROOT / ".github/labeler.yml"
PR_TEMPLATE = ROOT / ".github/PULL_REQUEST_TEMPLATE.md"
HARNESS_WRAPPER = ROOT / "scripts/validation/validate-harness.sh"
LOCAL_QA = ROOT / "scripts/validation/run-local-qa-gates.sh"
REPO_CONTRACT = ROOT / "scripts/validation/check-repo-contracts.sh"
TARGET_CLI_COMMAND = "python3 scripts/validation/check-target-surface-contract.py"
TARGET_TEST_COMMAND = (
    "python3 -m unittest tests.validation.test_target_surface_contracts -v"
)
OPERATIONAL_READINESS_TEST_COMMAND = (
    "python3 -m unittest "
    "tests.validation.test_compose_core_readiness "
    "tests.validation.test_postgres_logical_upgrade_rehearsal "
    "tests.validation.test_grype_db_seed "
    "tests.validation.test_supply_chain_policy "
    "tests.validation.test_sample_service_delivery_rehearsal -v"
)
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
SUPPLY_CHAIN_GOVERNANCE_DESCRIPTION = (
    "`ci.supply-chain-fixture-policy`"
)
GITHUB_INDEX_SECTIONS = (
    "Purpose",
    "Surface Map",
    "Authority and Change Routes",
    "Verification",
    "Related Documents",
)
GITHUB_INDEX_LINKS = (
    "./workflows/ci-quality.yml",
    "./rulesets/main-protection.md",
    "../docs/00.agent-governance/rules/github-governance.md",
    "../scripts/validation/run-local-qa-gates.sh",
    "../docs/90.references/data/governance/"
    "github-actions-control-plane-observation.yaml",
)
GITHUB_OBSERVATION_KEYS = {
    "schema_version",
    "observed_at",
    "repository",
    "authority",
    "source_visibility",
    "remote_default_commit",
    "remote_default_source_url",
    "local_base_commit",
    "latest_ci_run_id",
    "latest_ci_source_url",
    "latest_ci_conclusion",
    "observed_ci_jobs",
    "root_cause",
    "managed_workflows",
    "control_plane_verification",
    "public_sources",
    "limitations",
}
GITHUB_MANAGED_WORKFLOWS = (
    (222509952, "Dependabot Updates"),
    (223086017, "CodeQL"),
    (282786058, "Dependency Graph"),
)

TARGET_SURFACE_PATHS = (
    ".prettierignore",
    ".github/workflows/ci-quality.yml",
    "archive/Windows-Network-IP.md",
    "examples/sample-web-service/service.md",
    "infra/04-data/analytics/influxdb/README.md",
    "projects/storybook/README.md",
    "scripts/validation/target_surface_contract.py",
    "secrets/SENSITIVE_ENV_VARS.md.example",
    "tests/validation/test_target_surface_contracts.py",
    "docs/90.references/data/governance/document-corpus-lifecycle/ref-0069-target-surface-convergence.yaml",
)

COUPLED_PATHS = (
    "AGENTS.md",
    "CLAUDE.md",
    "GEMINI.md",
    ".agents/agents/code-reviewer.md",
    ".claude/agents/code-reviewer.md",
    ".codex/agents/code-reviewer.toml",
    ".gemini/agents/code-reviewer.md",
    "docs/00.agent-governance/rules/agentic.md",
    "docs/00.agent-governance/contracts/agent-governance-artifacts.yaml",
    "docs/00.agent-governance/contracts/agent-catalog.yaml",
    "docs/00.agent-governance/contracts/provider-models.yaml",
    "scripts/operations/provider_surface_renderer.py",
    "scripts/validation/agent_governance_contract.py",
    "scripts/validation/agent_output_eval.py",
    "scripts/validation/check-agent-governance-contract.py",
    "scripts/validation/check-repo-contracts.sh",
    "scripts/validation/run-agent-output-eval-fixtures.sh",
    "scripts/validation/run-agent-precommit-all-files.sh",
    "scripts/validation/run-local-qa-gates.sh",
    "scripts/validation/validate-harness.sh",
    "tests/validation/test_agent_governance_contract.py",
    "tests/validation/test_agent_governance_ci_routing.py",
    "tests/validation/test_agent_output_eval_fixtures.py",
    "tests/validation/test_provider_native_surfaces.py",
    "tests/validation/test_provider_surface_renderer.py",
)


class AgentGovernanceRoutingTests(unittest.TestCase):
    def test_target_surface_paths_select_the_focused_gate(self) -> None:
        for path in TARGET_SURFACE_PATHS:
            with self.subTest(path=path):
                result = subprocess.run(
                    ["bash", str(RECOMMENDER), "--files", path],
                    cwd=ROOT,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertIn(TARGET_CLI_COMMAND, result.stdout)
                self.assertIn(TARGET_TEST_COMMAND, result.stdout)

    def test_target_surface_paths_select_the_existing_pre_push_owner(self) -> None:
        data = yaml.safe_load(PRE_COMMIT.read_text(encoding="utf-8"))
        hooks = [
            hook
            for repo in data["repos"]
            if repo["repo"] == "local"
            for hook in repo["hooks"]
            if hook["id"] == "check-repo-contracts"
        ]
        self.assertEqual(1, len(hooks))
        selector = re.compile(hooks[0]["files"])
        for path in TARGET_SURFACE_PATHS:
            with self.subTest(path=path):
                self.assertIsNotNone(selector.fullmatch(path))
        self.assertFalse(
            any(
                hook["id"] == "check-target-surface-contract"
                for repo in data["repos"]
                if repo["repo"] == "local"
                for hook in repo["hooks"]
            )
        )

    def test_local_runner_and_tool_bootstrap_expose_the_target_gate(self) -> None:
        result = subprocess.run(
            ["bash", str(LOCAL_QA), "--list"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn(
            "leaf.local-target-surface-regressions\t"
            "scripts/validation/ci_gate_adapters.py",
            result.stdout,
        )
        self.assertIn(
            "leaf.local-target-surface-contract\t"
            "scripts/validation/check-target-surface-contract.py",
            result.stdout,
        )
        local_text = LOCAL_QA.read_text(encoding="utf-8")
        self.assertIn("--profile local-script-backed", local_text)
        self.assertIn("--profile local-harness", local_text)
        self.assertIn("--profile local-all-profiles", local_text)
        self.assertNotIn(TARGET_CLI_COMMAND, local_text)
        self.assertNotIn(TARGET_TEST_COMMAND, local_text)
        tool_bootstrap = (ROOT / "scripts/operations/use-qa-ci-tools.sh").read_text(
            encoding="utf-8"
        )
        self.assertRegex(tool_bootstrap, r"\bpython3\b.*\bruff\b")

    def test_existing_repo_contracts_job_runs_target_surface_contracts(self) -> None:
        workflow = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
        jobs = workflow["jobs"]
        actual_jobs = set(jobs)
        missing_jobs = sorted(REQUIRED_CI_JOBS - actual_jobs)
        unexpected_jobs = sorted(actual_jobs - REQUIRED_CI_JOBS)
        self.assertEqual(
            ([], []),
            (missing_jobs, unexpected_jobs),
            "required CI job-set drift "
            f"(missing={missing_jobs}, unexpected={unexpected_jobs})",
        )
        repo_steps = jobs["repo-contracts"]["steps"]
        commands = "\n".join(
            str(step.get("run", "")) for step in repo_steps if isinstance(step, dict)
        )
        self.assertNotIn(TARGET_CLI_COMMAND, commands)
        self.assertNotIn("tests.validation.test_target_surface_contracts", commands)
        self.assertEqual(
            0,
            sum(
                step.get("name") == "Check target surface contracts"
                for step in repo_steps
                if isinstance(step, dict)
            ),
        )
        aggregate = REPO_CONTRACT.read_text(encoding="utf-8")
        self.assertNotIn(TARGET_CLI_COMMAND, aggregate)
        contract = json.loads(
            (ROOT / ".github/workflow-contract.yml").read_text(
                encoding="utf-8"
            )
        )
        node_by_id = {
            node["gate_id"]: node for node in contract["gate_nodes"]
        }
        self.assertEqual(
            [
                "leaf.local-target-surface-regressions",
                "leaf.local-target-surface-contract",
                "leaf.local-target-delta-regressions",
                "leaf.local-target-delta-contract",
            ],
            node_by_id["local.target-surface"]["children"],
        )
        local_qa = LOCAL_QA.read_text(encoding="utf-8")
        self.assertIn("--profile local-script-backed", local_qa)
        self.assertNotIn(TARGET_CLI_COMMAND, local_qa)
        self.assertNotIn(TARGET_TEST_COMMAND, local_qa)

    def test_ci_quality_has_exact_sixteen_job_ids(self) -> None:
        workflow = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
        jobs = workflow["jobs"]
        self.assertEqual(16, len(jobs))
        self.assertEqual(REQUIRED_CI_JOBS, frozenset(jobs))

    def test_zizmor_dynamic_tool_is_exactly_pinned(self) -> None:
        workflow = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
        zizmor_steps = [
            step
            for step in workflow["jobs"]["zizmor"]["steps"]
            if isinstance(step, dict)
        ]
        self.assertEqual(
            [
                "python3 scripts/validation/run-ci-gate.py "
                "--profile ci --gate ci.zizmor"
            ],
            [
                step["run"]
                for step in zizmor_steps
                if isinstance(step.get("run"), str)
            ],
        )
        run_steps = [step for step in zizmor_steps if "run" in step]
        self.assertEqual(1, len(run_steps))
        self.assertNotIn(
            "env",
            run_steps[0],
            "offline zizmor must not receive a credential environment",
        )
        adapter = (
            ROOT / "scripts/validation/ci_gate_adapters.py"
        ).read_text(encoding="utf-8")
        self.assertIn("zizmor==1.28.0", adapter)
        self.assertNotIn("zizmor==1.27.0", adapter)

    def test_github_index_is_navigation_only_and_not_readme(self) -> None:
        self.assertTrue(GITHUB_INDEX.is_file(), "missing .github/INDEX.md")
        self.assertFalse(GITHUB_README.exists(), ".github/README.md is forbidden")
        text = GITHUB_INDEX.read_text(encoding="utf-8")
        self.assertFalse(text.startswith("---"), "frontmatter is forbidden")
        self.assertEqual(
            GITHUB_INDEX_SECTIONS,
            tuple(re.findall(r"(?m)^## (.+?)\s*$", text)),
        )
        for link in GITHUB_INDEX_LINKS:
            with self.subTest(link=link):
                self.assertIn(f"]({link})", text)
        for job_id in REQUIRED_CI_JOBS:
            with self.subTest(duplicated_job=job_id):
                self.assertNotIn(f"`{job_id}`", text)
        for pattern in (
            r"(?i)\b(?:must|shall)\b",
            r"(?i)\b16[- ]job\b",
            r"(?i)\b(?:secrets?|vars?|variables?)\.",
            r"\bGITHUB_TOKEN\b",
            r"(?i)\bremote\b.{0,40}\b(?:active|enforced)\b",
            r"(?i)\b(?:active|enforced)\b.{0,40}\bremote\b",
        ):
            with self.subTest(forbidden_policy_pattern=pattern):
                self.assertIsNone(re.search(pattern, text))

        contract = yaml.safe_load(ARTIFACT_CONTRACT.read_text(encoding="utf-8"))
        profiles = [
            profile
            for profile in contract["artifacts"]
            if profile["profile_id"] == "github-navigation-index"
        ]
        self.assertEqual(1, len(profiles))
        self.assertEqual(
            {
                "profile_id": "github-navigation-index",
                "artifact_type": "github-navigation-index",
                "path_pattern": ".github/INDEX.md",
                "repository_section": "harness",
                "canonical": False,
                "required_keys": [],
                "key_order": [],
                "required_sections": list(GITHUB_INDEX_SECTIONS),
                "expected_values": {},
            },
            profiles[0],
        )

    def test_remote_observation_schema_is_exact_and_unverified(self) -> None:
        self.assertTrue(
            GITHUB_OBSERVATION.is_file(),
            "missing GitHub Actions control-plane observation",
        )
        data = yaml.safe_load(GITHUB_OBSERVATION.read_text(encoding="utf-8"))
        self.assertEqual(GITHUB_OBSERVATION_KEYS, set(data))
        self.assertEqual(1, data["schema_version"])
        self.assertEqual("2026-07-26T18:22:32+09:00", data["observed_at"])
        self.assertEqual("buenhyden/hy-home.docker", data["repository"])
        self.assertEqual("non-authoritative-observation", data["authority"])
        self.assertEqual("public-metadata-only", data["source_visibility"])
        self.assertEqual("a897978f", data["remote_default_commit"])
        self.assertEqual(
            "e65bb18fa2f6e3fb6235725750c7c57cbe0227ee",
            data["local_base_commit"],
        )
        self.assertEqual(29777690571, data["latest_ci_run_id"])
        self.assertEqual("failure", data["latest_ci_conclusion"])
        self.assertEqual(15, data["observed_ci_jobs"])
        self.assertEqual("unverified", data["root_cause"])
        self.assertEqual("unverified", data["control_plane_verification"])
        self.assertEqual(
            {
                "repository": "https://github.com/buenhyden/hy-home.docker",
                "actions_secure_use": (
                    "https://docs.github.com/en/actions/reference/security/secure-use"
                ),
                "workflow_monitoring": (
                    "https://docs.github.com/en/actions/how-tos/monitor-workflows"
                ),
                "rulesets": (
                    "https://docs.github.com/en/enterprise-cloud@latest/"
                    "repositories/configuring-branches-and-merges-in-your-"
                    "repository/managing-rulesets/about-rulesets"
                ),
                "zizmor_v1_28_0": (
                    "https://github.com/zizmorcore/zizmor/releases/tag/v1.28.0"
                ),
            },
            data["public_sources"],
        )

        managed = data["managed_workflows"]
        self.assertEqual(3, len(managed))
        self.assertEqual(
            list(GITHUB_MANAGED_WORKFLOWS),
            [(record["id"], record["name"]) for record in managed],
        )
        expected_record_keys = {
            "id",
            "name",
            "management_class",
            "observed_state",
            "last_run",
            "source_visibility",
            "review_owner",
            "retrieved_at",
            "source_url",
        }
        for record in managed:
            with self.subTest(workflow_id=record["id"]):
                self.assertEqual(expected_record_keys, set(record))
                self.assertEqual("github-managed", record["management_class"])
                self.assertEqual("active", record["observed_state"])
                self.assertEqual("unverified", record["last_run"])
                self.assertEqual("public-metadata-only", record["source_visibility"])
                self.assertEqual("ci-cd-engineer", record["review_owner"])
                self.assertEqual(
                    "2026-07-26T18:22:32+09:00",
                    record["retrieved_at"],
                )
                self.assertEqual(
                    "https://api.github.com/repos/buenhyden/hy-home.docker/"
                    f"actions/workflows/{record['id']}",
                    record["source_url"],
                )

    def test_stale_remote_enforcement_claims_use_observation_boundary(self) -> None:
        stale_patterns = (
            r"2026-07-04",
            r"12 remote contexts",
            r"classic branch protection (?:is )?active",
            r"Repository rulesets API returned `0`",
            r"enforce_admins=false",
        )
        for path in (GITHUB_GOVERNANCE, MAIN_PROTECTION):
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=path):
                self.assertIn(
                    "github-actions-control-plane-observation.yaml",
                    text,
                )
                self.assertRegex(
                    text,
                    r"(?is)(?:control[- ]plane.{0,120}unverified|"
                    r"unverified.{0,120}control[- ]plane)",
                )
                for pattern in stale_patterns:
                    self.assertIsNone(re.search(pattern, text, re.IGNORECASE))

    def test_existing_supply_chain_job_runs_focused_operational_suites(
        self,
    ) -> None:
        workflow = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
        job = workflow["jobs"]["supply-chain-fixture-policy"]
        self.assertEqual({"contents": "read"}, job["permissions"])
        matching = [
            step
            for step in job["steps"]
            if isinstance(step, dict)
            and step.get("run")
            == (
                "python3 scripts/validation/run-ci-gate.py "
                "--profile ci --gate ci.supply-chain-fixture-policy"
            )
        ]
        self.assertEqual(1, len(matching))
        self.assertEqual(
            "Check supply-chain fixture policy",
            matching[0].get("name"),
        )
        contract = json.loads(
            (ROOT / ".github/workflow-contract.yml").read_text(encoding="utf-8")
        )
        self.assertEqual(
            (
                "leaf.supply-chain-fixture-policy",
                "leaf.supply-chain-deterministic-policy",
                "leaf.supply-chain-summary-freshness",
            ),
            tuple(
                next(
                    node["children"]
                    for node in contract["gate_nodes"]
                    if node["gate_id"] == "ci.supply-chain-fixture-policy"
                )
            ),
        )
        governance_text = GITHUB_GOVERNANCE.read_text(encoding="utf-8")
        governance_row = re.search(
            r"(?m)^\|\s*`supply-chain-fixture-policy`\s*\|\s*(.*?)\s*\|$",
            governance_text,
        )
        self.assertIsNotNone(governance_row)
        assert governance_row is not None
        self.assertEqual(
            SUPPLY_CHAIN_GOVERNANCE_DESCRIPTION,
            governance_row.group(1),
        )

    def test_supply_chain_focused_regression_routing_fails_closed(self) -> None:
        program = self._workflow_security_program()
        with self._workflow_fixture() as root:
            workflow_path = root / ".github/workflows/ci-quality.yml"
            text = workflow_path.read_text(encoding="utf-8")
            old = "--gate ci.supply-chain-fixture-policy"
            self.assertIn(old, text)
            workflow_path.write_text(
                text.replace(old, "--gate ci.docs-traceability", 1),
                encoding="utf-8",
            )
            result = subprocess.run(
                [sys.executable, "-c", program],
                cwd=root,
                capture_output=True,
                text=True,
                check=False,
            )
        self.assertEqual(1, result.returncode, result.stderr)
        self.assertIn(
            "does not project its root exactly once",
            result.stderr,
        )

    def test_ci_quality_policy_mutations_fail_closed(self) -> None:
        cases = (
            (
                "permissions",
                "repo-contracts:\n    permissions:\n      contents: read",
                "repo-contracts:\n    permissions:\n      contents: read\n      issues: read",
                "permissions differ from the contract",
            ),
            (
                "concurrency",
                "cancel-in-progress: true",
                "cancel-in-progress: false",
                "concurrency differs from the contract",
            ),
            (
                "timeout",
                "repo-contracts:\n    permissions:\n      contents: read\n    runs-on: ubuntu-latest\n    timeout-minutes: 10",
                "repo-contracts:\n    permissions:\n      contents: read\n    runs-on: ubuntu-latest",
                "timeout differs from the contract",
            ),
            (
                "action-pin",
                "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1",
                "actions/checkout@v4",
                "not a full SHA",
            ),
            (
                "unsafe-trigger",
                "  pull_request:\n    branches: [main]",
                "  pull_request_target:\n    branches: [main]",
                "forbidden event is configured",
            ),
            (
                "untrusted-run-input",
                "run: python3 scripts/validation/run-ci-gate.py --profile ci --gate ci.repo-contracts",
                "run: python3 scripts/validation/run-ci-gate.py --profile ci --gate '${{ github.event.pull_request.title }}'",
                "interpolates an Actions expression directly in run",
            ),
            (
                "untrusted-direct-ref",
                "run: python3 scripts/validation/run-ci-gate.py --profile ci --gate ci.repo-contracts",
                "run: python3 scripts/validation/run-ci-gate.py --profile ci --gate '${{ github.ref }}'",
                "interpolates an Actions expression directly in run",
            ),
            (
                "zizmor-credential-env",
                (
                    "        run: python3 scripts/validation/run-ci-gate.py "
                    "--profile ci --gate ci.zizmor"
                ),
                (
                    "        run: python3 scripts/validation/run-ci-gate.py "
                    "--profile ci --gate ci.zizmor\n"
                    "        env:\n"
                    "          AUTH_CONTEXT: synthetic-value"
                ),
                "zizmor must not receive a credential environment",
            ),
            (
                "stable-job-name",
                "  repo-contracts:\n",
                "  target-repo-contracts:\n",
                "job IDs differ from the contract",
            ),
            (
                "artifact-upload",
                "      - name: Check docs traceability sync",
                "      - name: Forbidden artifact upload\n        uses: actions/upload-artifact@0000000000000000000000000000000000000000\n      - name: Check docs traceability sync",
                "artifact upload is outside the approved workflow contract",
            ),
            (
                "artifact-upload-mixed-owner-case",
                "      - name: Check docs traceability sync",
                "      - name: Forbidden artifact upload\n        uses: Actions/upload-artifact@0000000000000000000000000000000000000000\n      - name: Check docs traceability sync",
                "artifact upload is outside the approved workflow contract",
            ),
            (
                "artifact-upload-mixed-action-case",
                "      - name: Check docs traceability sync",
                "      - name: Forbidden artifact upload\n        uses: actions/Upload-Artifact@0000000000000000000000000000000000000000\n      - name: Check docs traceability sync",
                "artifact upload is outside the approved workflow contract",
            ),
        )
        program = self._workflow_security_program()
        for label, old, new, expected in cases:
            with self.subTest(label=label), self._workflow_fixture() as root:
                workflow_path = root / ".github/workflows/ci-quality.yml"
                text = workflow_path.read_text(encoding="utf-8")
                self.assertIn(old, text)
                workflow_path.write_text(text.replace(old, new, 1), encoding="utf-8")
                result = subprocess.run(
                    [sys.executable, "-c", program],
                    cwd=root,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(1, result.returncode, result.stderr)
                self.assertIn(expected, result.stderr)

        with (
            self.subTest(label="ref-env-indirection-fails-projection"),
            self._workflow_fixture() as root,
        ):
            workflow_path = root / ".github/workflows/ci-quality.yml"
            text = workflow_path.read_text(encoding="utf-8")
            old = (
                "        run: python3 scripts/validation/run-ci-gate.py "
                "--profile ci --gate ci.repo-contracts"
            )
            new = (
                "        env:\n"
                "          SAFE_REF: ${{ github.ref }}\n"
                "        run: python3 scripts/validation/run-ci-gate.py "
                '--profile ci --gate "$SAFE_REF"'
            )
            self.assertIn(old, text)
            workflow_path.write_text(text.replace(old, new, 1), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, "-c", program],
                cwd=root,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(1, result.returncode, result.stderr)
            self.assertIn("non-static gate program", result.stderr)

        safe_actions = (
            "actions/download-artifact@0000000000000000000000000000000000000000",
            "example/upload-artifact-helper@0000000000000000000000000000000000000000",
        )
        for action in safe_actions:
            with (
                self.subTest(label="non-upload-action-is-safe", action=action),
                self._workflow_fixture() as root,
            ):
                workflow_path = root / ".github/workflows/ci-quality.yml"
                text = workflow_path.read_text(encoding="utf-8")
                old = "      - name: Check docs traceability sync"
                new = (
                    f"      - name: Safe action control\n        uses: {action}\n{old}"
                )
                self.assertIn(old, text)
                workflow_path.write_text(text.replace(old, new, 1), encoding="utf-8")
                result = subprocess.run(
                    [sys.executable, "-c", program],
                    cwd=root,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(1, result.returncode, result.stderr)
                self.assertIn("direct Action reference is not registered", result.stderr)

    def test_ci_quality_duplicate_yaml_keys_fail_closed(self) -> None:
        sentinel = "duplicate-workflow-secret-sentinel"
        cases = (
            (
                "top-level",
                "permissions:\n  contents: read\n\nconcurrency:",
                "permissions:\n  contents: read\n"
                f"permissions:\n  contents: read # {sentinel}\n\nconcurrency:",
            ),
            (
                "job-id",
                "  docs-implementation-alignment:\n",
                "  docs-traceability:\n"
                "    permissions:\n"
                f"      contents: read # {sentinel}\n"
                "    runs-on: ubuntu-latest\n"
                "    timeout-minutes: 5\n"
                "    steps: []\n\n"
                "  docs-implementation-alignment:\n",
            ),
            (
                "job-policy",
                "    timeout-minutes: 10\n    env:\n      TEMPLATE_GATE_BASE:",
                "    timeout-minutes: 10\n"
                f"    timeout-minutes: 10 # {sentinel}\n"
                "    env:\n"
                "      TEMPLATE_GATE_BASE:",
            ),
        )
        program = self._workflow_security_program()
        for label, old, new in cases:
            with self.subTest(label=label), self._workflow_fixture() as root:
                workflow_path = root / ".github/workflows/ci-quality.yml"
                text = workflow_path.read_text(encoding="utf-8")
                self.assertIn(old, text)
                workflow_path.write_text(text.replace(old, new, 1), encoding="utf-8")
                result = subprocess.run(
                    [sys.executable, "-c", program],
                    cwd=root,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(1, result.returncode, result.stderr)
                self.assertIn("duplicate YAML mapping key", result.stderr)
                self.assertNotIn(sentinel, result.stderr)

    def test_duplicate_workflow_purpose_and_cross_file_job_id_fail_closed(
        self,
    ) -> None:
        cases = (
            (
                "workflow-purpose",
                "duplicate-purpose.yml",
                (
                    "name: Greeting\n"
                    "on:\n"
                    "  workflow_dispatch:\n"
                    "permissions:\n"
                    "  contents: read\n"
                    "jobs:\n"
                    "  unique-purpose-probe:\n"
                    "    permissions:\n"
                    "      contents: read\n"
                    "    runs-on: ubuntu-latest\n"
                    "    timeout-minutes: 5\n"
                    "    steps: []\n"
                ),
                "workflow name is duplicated",
            ),
            (
                "cross-file-job-id",
                "duplicate-job.yml",
                (
                    "name: Unique duplicate-job probe\n"
                    "on:\n"
                    "  workflow_dispatch:\n"
                    "permissions:\n"
                    "  contents: read\n"
                    "jobs:\n"
                    "  repo-contracts:\n"
                    "    permissions:\n"
                    "      contents: read\n"
                    "    runs-on: ubuntu-latest\n"
                    "    timeout-minutes: 5\n"
                    "    steps: []\n"
                ),
                "job identity is duplicated across workflows",
            ),
        )
        program = self._workflow_security_program()
        for label, filename, content, expected in cases:
            with self.subTest(label=label), self._workflow_fixture() as root:
                workflow_path = root / ".github/workflows" / filename
                workflow_path.write_text(content, encoding="utf-8")
                result = subprocess.run(
                    [sys.executable, "-c", program],
                    cwd=root,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(1, result.returncode, result.stderr)
                self.assertIn(expected, result.stderr)

    def test_remote_observation_and_stale_claim_mutations_fail_closed(self) -> None:
        self.assertTrue(
            GITHUB_OBSERVATION.is_file(),
            "missing GitHub Actions control-plane observation",
        )
        sentinel = "remote-observation-private-sentinel"
        cases = (
            (
                "duplicate-observation-key",
                GITHUB_OBSERVATION.relative_to(ROOT),
                "root_cause: unverified\n",
                f"root_cause: unverified\nroot_cause: verified # {sentinel}\n",
                "duplicate YAML mapping key",
            ),
            (
                "control-plane-overclaim",
                GITHUB_OBSERVATION.relative_to(ROOT),
                "control_plane_verification: unverified",
                "control_plane_verification: verified",
                "invalid remote observation field",
            ),
            (
                "root-cause-overclaim",
                GITHUB_OBSERVATION.relative_to(ROOT),
                "root_cause: unverified",
                "root_cause: workflow-defect",
                "invalid remote observation field",
            ),
            (
                "stale-ruleset-claim",
                MAIN_PROTECTION.relative_to(ROOT),
                "## Target Ruleset",
                "Verified read-only on 2026-07-04.\n\n## Target Ruleset",
                "stale active remote-state claim",
            ),
        )
        program = self._stage00_github_program()
        for label, relative, old, new, expected in cases:
            with self.subTest(label=label), self._workflow_fixture() as root:
                target = root / relative
                text = target.read_text(encoding="utf-8")
                self.assertIn(old, text)
                target.write_text(text.replace(old, new, 1), encoding="utf-8")
                result = subprocess.run(
                    [sys.executable, "-c", program],
                    cwd=root,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(1, result.returncode, result.stderr)
                self.assertIn(expected, result.stderr)
                self.assertNotIn(sentinel, result.stderr)

    def test_ruleset_required_check_mismatch_fails_closed(self) -> None:
        program = self._stage00_github_program()
        with self._workflow_fixture() as root:
            ruleset = root / MAIN_PROTECTION.relative_to(ROOT)
            text = ruleset.read_text(encoding="utf-8")
            old = "- `storybook-coverage`\n"
            self.assertIn(old, text)
            ruleset.write_text(text.replace(old, "", 1), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, "-c", program],
                cwd=root,
                capture_output=True,
                text=True,
                check=False,
            )
        self.assertEqual(1, result.returncode, result.stderr)
        self.assertIn("missing required status check", result.stderr)

    def test_governance_required_gate_table_mismatch_fails_closed(
        self,
    ) -> None:
        program = self._stage00_github_program()
        with self._workflow_fixture() as root:
            governance = root / GITHUB_GOVERNANCE.relative_to(ROOT)
            text = governance.read_text(encoding="utf-8")
            old = "| `storybook-coverage`"
            self.assertIn(old, text)
            governance.write_text(
                text.replace(old, "| `renamed-coverage-probe`", 1),
                encoding="utf-8",
            )
            result = subprocess.run(
                [sys.executable, "-c", program],
                cwd=root,
                capture_output=True,
                text=True,
                check=False,
            )
        self.assertEqual(1, result.returncode, result.stderr)
        self.assertIn(
            "required quality gate table differs from typed workflow contract",
            result.stderr,
        )

    def test_repository_metadata_stage00_mutations_fail_closed(self) -> None:
        contract = json.loads(
            (ROOT / ".github/workflow-contract.yml").read_text(
                encoding="utf-8"
            )
        )
        repo_root = next(
            node
            for node in contract["gate_nodes"]
            if node["gate_id"] == "ci.repo-contracts"
        )
        children = tuple(repo_root["children"])
        self.assertLess(
            children.index("leaf.repo-metadata-base"),
            children.index("setup.repo-python-dependencies"),
        )
        self.assertLess(
            children.index("setup.repo-python-dependencies"),
            children.index("leaf.repo-document-metadata"),
        )
        metadata = next(
            node
            for node in contract["gate_nodes"]
            if node["gate_id"] == "leaf.repo-document-metadata"
        )
        self.assertEqual(["TEMPLATE_GATE_BASE"], metadata["allowed_env_keys"])
        workflow = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
        self.assertEqual(
            (
                "python3 scripts/validation/run-ci-gate.py "
                "--profile ci --gate ci.repo-contracts"
            ),
            workflow["jobs"]["repo-contracts"]["steps"][-1]["run"],
        )

    def test_repo_memory_contract_rejects_exact_current_profile_mutation(
        self,
    ) -> None:
        if importlib.util.find_spec("html5lib") is None:
            self.skipTest("html5lib is not installed in the local test runtime")
        program = self._repo_python_program("Governance memory contract")
        sentinel = "private-current-profile-sentinel"
        load_sentinel = "private-contract-load-sentinel"
        with self._memory_contract_fixture() as root:
            baseline = subprocess.run(
                [sys.executable, "-c", program],
                cwd=root,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(0, baseline.returncode, baseline.stderr)

            contract_path = root / ARTIFACT_CONTRACT.relative_to(ROOT)
            original_contract_text = contract_path.read_text(encoding="utf-8")
            contract = yaml.safe_load(original_contract_text)
            profiles = [
                profile
                for profile in contract["artifacts"]
                if profile.get("profile_id") == "governance-current-memory"
            ]
            self.assertEqual(1, len(profiles))
            profiles[0]["required_sections"][-1] = sentinel
            contract_path.write_text(
                yaml.safe_dump(contract, sort_keys=False),
                encoding="utf-8",
            )
            result = subprocess.run(
                [sys.executable, "-c", program],
                cwd=root,
                capture_output=True,
                text=True,
                check=False,
            )
            contract_path.write_text(
                original_contract_text.replace(
                    "schema_version: 1\n",
                    "schema_version: 1\n"
                    f"schema_version: 1 # {load_sentinel}\n",
                    1,
                ),
                encoding="utf-8",
            )
            load_error = subprocess.run(
                [sys.executable, "-c", program],
                cwd=root,
                capture_output=True,
                text=True,
                check=False,
            )

        self.assertEqual(1, result.returncode, result.stderr)
        self.assertIn("AGC-MEMORY-BOUNDS", result.stderr)
        self.assertIn("profile-contract-mismatch", result.stderr)
        self.assertNotIn(sentinel, result.stderr)
        self.assertEqual(1, load_error.returncode, load_error.stderr)
        self.assertIn("AGC-YAML-DUPLICATE-KEY", load_error.stderr)
        self.assertNotIn(load_sentinel, load_error.stderr)

    def test_recommender_selects_coupled_contract_and_eval_gates(self) -> None:
        for path in COUPLED_PATHS:
            with self.subTest(path=path):
                result = subprocess.run(
                    ["bash", str(RECOMMENDER), "--files", path],
                    cwd=ROOT,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertIn(
                    "bash scripts/validation/check-repo-contracts.sh",
                    result.stdout,
                )
                self.assertIn(
                    "bash scripts/validation/run-agent-output-eval-fixtures.sh --check-fixtures --check-regressions",
                    result.stdout,
                )

    def test_pre_push_repo_contract_selector_covers_every_coupled_path(self) -> None:
        data = yaml.safe_load(PRE_COMMIT.read_text(encoding="utf-8"))
        hooks = [
            hook
            for repo in data["repos"]
            if repo["repo"] == "local"
            for hook in repo["hooks"]
            if hook["id"] == "check-repo-contracts"
        ]
        self.assertEqual(1, len(hooks))
        selector = re.compile(hooks[0]["files"])
        for path in COUPLED_PATHS:
            with self.subTest(path=path):
                self.assertIsNotNone(selector.fullmatch(path))

    def test_existing_ci_jobs_run_full_contract_and_semantic_eval_markers(self) -> None:
        workflow = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
        jobs = workflow["jobs"]

        self.assertIn(
            "python3 scripts/validation/run-ci-gate.py "
            "--profile ci --gate ci.repo-contracts",
            "\n".join(
                str(step.get("run", ""))
                for step in jobs["repo-contracts"]["steps"]
                if isinstance(step, dict)
            ),
        )
        self.assertIn(
            "python3 scripts/validation/run-ci-gate.py "
            "--profile ci --gate ci.agent-output-eval-fixture-gate",
            "\n".join(
                str(step.get("run", ""))
                for step in jobs["agent-output-eval-fixture-gate"]["steps"]
                if isinstance(step, dict)
            ),
        )
        aggregate = REPO_CONTRACT.read_text(encoding="utf-8")
        self.assertNotIn(
            "python3 scripts/validation/check-agent-governance-contract.py",
            aggregate,
        )
        self.assertNotRegex(
            aggregate,
            r"(?m)^if ! bash scripts/hardening/check-all-hardening\.sh ",
        )
        self.assertNotRegex(
            aggregate,
            r"(?m)^if ! bash scripts/validation/"
            r"run-agent-output-eval-fixtures\.sh ",
        )
        local_qa = LOCAL_QA.read_text(encoding="utf-8")
        self.assertNotIn("run-agent-output-eval-fixtures.sh", local_qa)
        self.assertNotIn("check-all-hardening.sh", local_qa)
        self.assertEqual(4, local_qa.count("scripts/validation/run-ci-gate.py"))
        self.assertEqual({"contents": "read"}, jobs["repo-contracts"]["permissions"])
        self.assertEqual(
            {"contents": "read"},
            jobs["agent-output-eval-fixture-gate"]["permissions"],
        )

    def test_github_review_surfaces_cover_semantic_harness_evidence(self) -> None:
        owners = CODEOWNERS.read_text(encoding="utf-8")
        for path in (
            "scripts/validation/agent_output_eval.py",
            "scripts/validation/run-agent-output-eval-fixtures.sh",
            "scripts/validation/report-provider-hook-parity.sh",
            "tests/validation/test_agent_governance_ci_routing.py",
            "tests/validation/test_agent_output_eval_fixtures.py",
        ):
            with self.subTest(owner=path):
                self.assertIn(path, owners)

        labeler = LABELER.read_text(encoding="utf-8")
        for provider_path in (
            ".agents/**/*",
            ".claude/**/*",
            ".codex/**/*",
            ".gemini/**/*",
        ):
            with self.subTest(labeler=provider_path):
                self.assertIn(provider_path, labeler)

        template = PR_TEMPLATE.read_text(encoding="utf-8")
        for evidence in (
            "--mode repository --section all",
            "run-agent-output-eval-fixtures.sh --check-fixtures --check-regressions",
            "fixtures_check=pass",
            "regressions_check=pass",
            "command, result, rollback, and skipped-check fields",
        ):
            with self.subTest(evidence=evidence):
                self.assertIn(evidence, template)

        harness = HARNESS_WRAPPER.read_text(encoding="utf-8")
        self.assertIn("run-local-qa-gates.sh --harness", harness)

    def test_local_qa_routes_all_files_through_controlled_wrapper(self) -> None:
        result = subprocess.run(
            ["bash", str(LOCAL_QA), "--list"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stderr)
        for fragment in (
            "scripts/validation/run-agent-precommit-all-files.sh",
            "initially clean linked worktree",
            "tracked Task evidence",
            "--allow-prefix",
        ):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, result.stdout)
        self.assertNotIn("locally use pre-commit", result.stdout)
        self.assertNotIn("pre-commit run --all-files", result.stdout)
        self.assertIn("leaf.ci-precommit-regressions", result.stdout)

    def test_semantic_local_qa_bypass_guard_is_selector_coupled(self) -> None:
        for path in (
            "scripts/validation/run-local-qa-gates.sh",
            "scripts/validation/agent_governance_contract.py",
            "scripts/validation/check-repo-contracts.sh",
            "tests/validation/test_agent_governance_contract.py",
            "tests/validation/test_agent_governance_ci_routing.py",
        ):
            with self.subTest(path=path):
                self.assertIn(path, COUPLED_PATHS)

    def test_aggregate_delegates_local_qa_semantics_to_typed_authority(self) -> None:
        source = REPO_CONTRACT.read_text(encoding="utf-8")
        start = "required_surface_fragments = {"
        end = "\n}\n\nforbidden_ambiguous_fragments"
        aggregate_fragments = source.split(start, 1)[1].split(end, 1)[0]
        self.assertNotIn(
            'pathlib.Path("scripts/validation/run-local-qa-gates.sh")',
            aggregate_fragments,
        )
        self.assertIn('"gate_id": "leaf.repo-contracts"', source)
        self.assertIn(
            '"entrypoint": "scripts/validation/check-repo-contracts.sh"',
            source,
        )
        self.assertNotIn("--mode repository --section all", source)

    def test_script_reference_scan_ignores_only_python_cache_artifacts(self) -> None:
        source = REPO_CONTRACT.read_text(encoding="utf-8")
        start = "section \"Script reference integrity\"\nif ! python3 - <<'PY'; then\n"
        block = source.split(start, 1)[1].split(
            "\nPY\n  failures=$((failures + 1))",
            1,
        )[0]

        with self.subTest("cache-is-ignored"), self._script_reference_fixture() as root:
            result = subprocess.run(
                [sys.executable, "-c", block],
                cwd=root,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(0, result.returncode, result.stderr)

        with (
            self.subTest("source-is-still-checked"),
            self._script_reference_fixture() as root,
        ):
            docs = root / "docs"
            docs.mkdir()
            (docs / "active.md").write_text(
                "Run scripts/validation/missing-active.sh\n",
                encoding="utf-8",
            )
            result = subprocess.run(
                [sys.executable, "-c", block],
                cwd=root,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(1, result.returncode)
            self.assertIn("missing-active.sh", result.stderr)

        with (
            self.subTest("doc-under-cache-name-is-checked"),
            self._script_reference_fixture() as root,
        ):
            docs = root / "docs/__pycache__"
            docs.mkdir(parents=True)
            (docs / "active.md").write_text(
                "Run scripts/validation/missing-active-cache-name.sh\n",
                encoding="utf-8",
            )
            subprocess.run(
                ["git", "add", "-f", "docs/__pycache__/active.md"],
                cwd=root,
                check=True,
            )
            result = subprocess.run(
                [sys.executable, "-c", block],
                cwd=root,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(1, result.returncode)
            self.assertIn("missing-active-cache-name.sh", result.stderr)

        with (
            self.subTest("tracked-pyc-is-checked"),
            self._script_reference_fixture(track_cache=True) as root,
        ):
            result = subprocess.run(
                [sys.executable, "-c", block],
                cwd=root,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(1, result.returncode)
            self.assertIn("missing-cache.sh", result.stderr)

    def test_script_reference_scan_rejects_unsafe_files_without_dereference(
        self,
    ) -> None:
        source = REPO_CONTRACT.read_text(encoding="utf-8")
        start = "section \"Script reference integrity\"\nif ! python3 - <<'PY'; then\n"
        block = source.split(start, 1)[1].split(
            "\nPY\n  failures=$((failures + 1))",
            1,
        )[0]

        with self.subTest("external-symlink"), self._script_reference_fixture() as root:
            docs = root / "docs"
            docs.mkdir()
            sentinel = root / "external-sentinel.md"
            sentinel.write_text(
                "Run scripts/validation/missing-external-sentinel.sh\n",
                encoding="utf-8",
            )
            (docs / "linked.md").symlink_to(sentinel)
            subprocess.run(["git", "add", "docs/linked.md"], cwd=root, check=True)
            result = subprocess.run(
                [sys.executable, "-c", block],
                cwd=root,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(1, result.returncode)
            rendered = result.stdout + result.stderr
            self.assertIn("unsafe script-reference surface", rendered)
            self.assertNotIn("missing-external-sentinel.sh", rendered)

        with self.subTest("broken-symlink"), self._script_reference_fixture() as root:
            docs = root / "docs"
            docs.mkdir()
            (docs / "broken.md").symlink_to(root / "missing-sentinel.md")
            subprocess.run(["git", "add", "docs/broken.md"], cwd=root, check=True)
            result = subprocess.run(
                [sys.executable, "-c", block],
                cwd=root,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(1, result.returncode)
            rendered = result.stdout + result.stderr
            self.assertIn("unsafe script-reference surface", rendered)
            self.assertNotIn("missing-sentinel.md", rendered)

        with self.subTest("fifo"), self._script_reference_fixture() as root:
            docs = root / "docs"
            docs.mkdir()
            os.mkfifo(docs / "pipe.md")
            result = subprocess.run(
                [sys.executable, "-c", block],
                cwd=root,
                capture_output=True,
                text=True,
                check=False,
                timeout=5,
            )
            self.assertEqual(1, result.returncode)
            self.assertIn("unsafe script-reference surface", result.stderr)

    def test_script_reference_scan_enforces_exact_resource_ceilings(self) -> None:
        source = REPO_CONTRACT.read_text(encoding="utf-8")
        start = "section \"Script reference integrity\"\nif ! python3 - <<'PY'; then\n"
        block = source.split(start, 1)[1].split(
            "\nPY\n  failures=$((failures + 1))",
            1,
        )[0]
        expected_constants = (
            "MAX_REFERENCE_SURFACES: Final = 4_096",
            "MAX_REFERENCE_FILE_BYTES: Final = 16 * 1_048_576",
            "MAX_REFERENCE_TOTAL_BYTES: Final = 64 * 1_048_576",
            "MAX_REFERENCE_DISCOVERY_ENTRIES: Final = 8_192",
            "MAX_REFERENCE_GIT_OUTPUT_BYTES: Final = 1_048_576",
            "MAX_REFERENCE_PATH_BYTES: Final = 4_096",
            "MAX_REFERENCE_MATCHES: Final = 16_384",
            "MAX_REFERENCE_UNIQUE_TARGETS: Final = 8_192",
            "MAX_REFERENCE_FAILURES: Final = 4_096",
            "MAX_REFERENCE_FAILURE_BYTES: Final = 1_048_576",
        )
        for constant in expected_constants:
            with self.subTest(constant=constant):
                self.assertIn(constant, block)
        existence_check = block.split("def confined_regular_exists", 1)[1].split(
            "\n\nfailure_bytes = 0", 1
        )[0]
        self.assertIn("open_confined_regular(path)", existence_check)
        self.assertNotIn("read_confined_regular(path)", existence_check)
        for boundary_fragment in (
            "initial = os.lstat(path)",
            "opened = os.fstat(file_descriptor)",
            "aggregate_remaining = MAX_REFERENCE_TOTAL_BYTES - total_reference_bytes",
            "read_limit = min(MAX_REFERENCE_FILE_BYTES, aggregate_remaining)",
            "opened.st_size > read_limit",
            "remaining = read_limit + 1",
            "metadata.st_ctime_ns",
            "metadata_tuple(opened) != metadata_tuple(initial)",
            "metadata_tuple(final) != metadata_tuple(opened)",
        ):
            with self.subTest(boundary_fragment=boundary_fragment):
                self.assertIn(boundary_fragment, block)

        cases = (
            ("surface-below", 3, 8, 16, 16, 2, (b"a", b"b"), 0),
            ("surface-at", 2, 8, 16, 16, 2, (b"a", b"b"), 0),
            ("surface-above", 1, 8, 16, 16, 2, (b"a", b"b"), 1),
            ("file-below", 2, 5, 16, 16, 2, (b"abcd",), 0),
            ("file-at", 2, 4, 16, 16, 2, (b"abcd",), 0),
            ("file-above", 2, 3, 16, 16, 2, (b"abcd",), 1),
            ("total-below", 2, 8, 9, 16, 2, (b"abcd", b"efgh"), 0),
            ("total-at", 2, 8, 8, 16, 2, (b"abcd", b"efgh"), 0),
            ("total-above", 2, 8, 7, 16, 2, (b"abcd", b"efgh"), 1),
            ("discovery-below", 2, 8, 16, 3, 2, (b"a",), 0),
            ("discovery-at", 2, 8, 16, 2, 2, (b"a",), 0),
            ("discovery-above", 2, 8, 16, 1, 2, (b"a",), 1),
        )
        for (
            label,
            surface_limit,
            file_limit,
            total_limit,
            discovery_limit,
            discovery_entries,
            payloads,
            expected,
        ) in cases:
            with self.subTest(label=label), tempfile.TemporaryDirectory() as directory:
                root = pathlib.Path(directory)
                subprocess.run(["git", "init", "-q"], cwd=root, check=True)
                docs = root / "docs"
                docs.mkdir()
                for index, payload in enumerate(payloads):
                    (docs / f"surface-{index}.md").write_bytes(payload)
                while len(list(docs.iterdir())) < discovery_entries - 1:
                    index = len(list(docs.iterdir()))
                    (docs / f"discovery-{index}.md").write_bytes(b"")
                mutated = (
                    block.replace(
                        "MAX_REFERENCE_SURFACES: Final = 4_096",
                        f"MAX_REFERENCE_SURFACES: Final = {surface_limit}",
                    )
                    .replace(
                        "MAX_REFERENCE_FILE_BYTES: Final = 16 * 1_048_576",
                        f"MAX_REFERENCE_FILE_BYTES: Final = {file_limit}",
                    )
                    .replace(
                        "MAX_REFERENCE_TOTAL_BYTES: Final = 64 * 1_048_576",
                        f"MAX_REFERENCE_TOTAL_BYTES: Final = {total_limit}",
                    )
                    .replace(
                        "MAX_REFERENCE_DISCOVERY_ENTRIES: Final = 8_192",
                        f"MAX_REFERENCE_DISCOVERY_ENTRIES: Final = {discovery_limit}",
                    )
                )
                result = subprocess.run(
                    [sys.executable, "-c", mutated],
                    cwd=root,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(expected, result.returncode, result.stderr)
                if expected:
                    self.assertIn("unsafe script-reference surface", result.stderr)

    def test_script_reference_discovery_is_bounded_before_allocation(self) -> None:
        source = REPO_CONTRACT.read_text(encoding="utf-8")
        start = "section \"Script reference integrity\"\nif ! python3 - <<'PY'; then\n"
        block = source.split(start, 1)[1].split(
            "\nPY\n  failures=$((failures + 1))", 1
        )[0]
        scan_loop = block.split("for match in pattern.finditer(text):", 1)[1]
        self.assertLess(
            scan_loop.index('match.end("ref") - match.start("ref")'),
            scan_loop.index('ref = match.group("ref")'),
        )
        git_reader = block.split("def git_paths", 1)[1].split("\n\ntracked =", 1)[0]
        discovery = block.split("def untracked_special_paths", 1)[1].split(
            "\n\nspecial_paths =", 1
        )[0]
        for fragment in (
            "subprocess.Popen(",
            "MAX_REFERENCE_GIT_OUTPUT_BYTES - output_bytes + 1",
            "MAX_REFERENCE_PATH_BYTES",
            "len(paths) > MAX_REFERENCE_SURFACES",
            "process.kill()",
            "process.wait()",
        ):
            with self.subTest(scope="git", fragment=fragment):
                self.assertIn(fragment, git_reader)
        self.assertNotIn("capture_output=True", git_reader)
        self.assertNotIn('.split(b"\\0")', git_reader)
        for fragment in (
            "os.scandir(path)",
            "discovery_count += 1",
            "discovery_count > MAX_REFERENCE_DISCOVERY_ENTRIES",
            "tracked_prefixes: set[pathlib.Path] = set()",
            "if len(tracked_prefixes) >= MAX_REFERENCE_DISCOVERY_ENTRIES",
            "tracked_prefixes.add(parent)",
        ):
            with self.subTest(scope="filesystem", fragment=fragment):
                self.assertIn(fragment, discovery)
        self.assertNotIn("os.listdir", discovery)
        self.assertNotIn("sorted(", discovery)
        self.assertNotIn("tracked_prefixes = {", discovery)

    def test_script_reference_match_target_and_failure_caps_are_exact(self) -> None:
        source = REPO_CONTRACT.read_text(encoding="utf-8")
        start = "section \"Script reference integrity\"\nif ! python3 - <<'PY'; then\n"
        block = source.split(start, 1)[1].split(
            "\nPY\n  failures=$((failures + 1))", 1
        )[0]

        def run(root: pathlib.Path, program: str) -> subprocess.CompletedProcess[str]:
            return subprocess.run(
                [sys.executable, "-c", program],
                cwd=root,
                capture_output=True,
                text=True,
                check=False,
            )

        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            target = root / "scripts/validation/existing.sh"
            target.parent.mkdir(parents=True)
            target.write_text("#!/bin/sh\n", encoding="utf-8")
            readme = root / "README.md"
            readme.write_text("scripts/validation/existing.sh\n" * 2, encoding="utf-8")
            exact = block.replace(
                "MAX_REFERENCE_MATCHES: Final = 16_384",
                "MAX_REFERENCE_MATCHES: Final = 2",
            )
            self.assertEqual(0, run(root, exact).returncode)
            readme.write_text("scripts/validation/existing.sh\n" * 3, encoding="utf-8")
            above = run(root, exact)
            self.assertEqual(1, above.returncode)
            self.assertEqual("FAIL: unsafe script-reference surface\n", above.stderr)

        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            readme = root / "README.md"
            exact_ref = "scripts/validation/exact-path.sh"
            above_ref = "scripts/validation/exact-pathx.sh"
            exact = block.replace(
                "MAX_REFERENCE_PATH_BYTES: Final = 4_096",
                f"MAX_REFERENCE_PATH_BYTES: Final = {len(exact_ref)}",
            )
            readme.write_text(exact_ref + "\n", encoding="utf-8")
            at_limit = run(root, exact)
            self.assertEqual(1, at_limit.returncode)
            self.assertIn("missing script reference", at_limit.stderr)
            readme.write_text(above_ref + "\n", encoding="utf-8")
            above = run(root, exact)
            self.assertEqual(1, above.returncode)
            self.assertEqual("FAIL: unsafe script-reference surface\n", above.stderr)

        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            target_root = root / "scripts/validation"
            target_root.mkdir(parents=True)
            for name in ("one.sh", "two.sh", "three.sh"):
                (target_root / name).write_text("#!/bin/sh\n", encoding="utf-8")
            readme = root / "README.md"
            readme.write_text(
                "scripts/validation/one.sh\nscripts/validation/two.sh\n",
                encoding="utf-8",
            )
            exact = block.replace(
                "MAX_REFERENCE_UNIQUE_TARGETS: Final = 8_192",
                "MAX_REFERENCE_UNIQUE_TARGETS: Final = 2",
            )
            self.assertEqual(0, run(root, exact).returncode)
            readme.write_text(
                "scripts/validation/one.sh\nscripts/validation/two.sh\n"
                "scripts/validation/three.sh\n",
                encoding="utf-8",
            )
            above = run(root, exact)
            self.assertEqual(1, above.returncode)
            self.assertEqual("FAIL: unsafe script-reference surface\n", above.stderr)

        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            readme = root / "README.md"
            readme.write_text(
                "scripts/validation/missing-one.sh\n"
                "scripts/validation/missing-two.sh\n",
                encoding="utf-8",
            )
            exact = block.replace(
                "MAX_REFERENCE_FAILURES: Final = 4_096",
                "MAX_REFERENCE_FAILURES: Final = 2",
            )
            observed = run(root, exact)
            self.assertEqual(1, observed.returncode)
            self.assertEqual(2, observed.stderr.count("missing script reference"))
            readme.write_text(
                readme.read_text(encoding="utf-8")
                + "scripts/validation/missing-three.sh\n",
                encoding="utf-8",
            )
            above = run(root, exact)
            self.assertEqual(1, above.returncode)
            self.assertEqual("FAIL: unsafe script-reference surface\n", above.stderr)

    def test_script_reference_scan_supports_only_approved_root_prefixes(self) -> None:
        source = REPO_CONTRACT.read_text(encoding="utf-8")
        start = "section \"Script reference integrity\"\nif ! python3 - <<'PY'; then\n"
        block = source.split(start, 1)[1].split(
            "\nPY\n  failures=$((failures + 1))", 1
        )[0]

        approved = (
            "$BASE_DIR/scripts/validation/existing.sh",
            "${ROOT}/scripts/validation/existing.sh",
            "$(git rev-parse --show-toplevel)/scripts/validation/existing.sh",
        )
        ignored = (
            "$OTHER/scripts/validation/missing.sh",
            "$(pwd)/scripts/validation/missing.sh",
            "https://example.test/scripts/validation/missing.sh",
            "/tmp/scripts/validation/missing.sh",
            "embedded-scripts/validation/missing.sh",
        )

        def run(root: pathlib.Path) -> subprocess.CompletedProcess[str]:
            return subprocess.run(
                [sys.executable, "-c", block],
                cwd=root,
                capture_output=True,
                text=True,
                check=False,
            )

        for reference in approved:
            with (
                self.subTest(kind="existing", reference=reference),
                tempfile.TemporaryDirectory() as directory,
            ):
                root = pathlib.Path(directory)
                subprocess.run(["git", "init", "-q"], cwd=root, check=True)
                target = root / "scripts/validation/existing.sh"
                target.parent.mkdir(parents=True)
                target.write_text("#!/bin/sh\n", encoding="utf-8")
                (root / "README.md").write_text(reference + "\n", encoding="utf-8")
                self.assertEqual(0, run(root).returncode)

            missing = reference.replace("existing.sh", "missing.sh")
            with (
                self.subTest(kind="missing", reference=reference),
                tempfile.TemporaryDirectory() as directory,
            ):
                root = pathlib.Path(directory)
                subprocess.run(["git", "init", "-q"], cwd=root, check=True)
                (root / "README.md").write_text(missing + "\n", encoding="utf-8")
                result = run(root)
                self.assertEqual(1, result.returncode)
                self.assertIn(
                    "missing script reference scripts/validation/missing.sh",
                    result.stderr,
                )
                self.assertNotIn("$BASE_DIR", result.stderr)
                self.assertNotIn("${ROOT}", result.stderr)
                self.assertNotIn("git rev-parse", result.stderr)

        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            (root / "README.md").write_text("\n".join(ignored) + "\n", encoding="utf-8")
            self.assertEqual(0, run(root).returncode)

    def test_script_reference_scan_bounds_and_ignores_external_uri_contexts(
        self,
    ) -> None:
        source = REPO_CONTRACT.read_text(encoding="utf-8")
        start = "section \"Script reference integrity\"\nif ! python3 - <<'PY'; then\n"
        block = source.split(start, 1)[1].split(
            "\nPY\n  failures=$((failures + 1))", 1
        )[0]

        def run(
            root: pathlib.Path, program: str = block
        ) -> subprocess.CompletedProcess[str]:
            return subprocess.run(
                [sys.executable, "-c", program],
                cwd=root,
                capture_output=True,
                text=True,
                check=False,
            )

        ignored = (
            "https://example.test?next=scripts/validation/missing.sh",
            "https://example.test#scripts/validation/missing.sh",
            "url=https://example.test/scripts/validation/missing.sh",
            "[script](https://example.test/scripts/validation/missing.sh)",
            "<https://example.test/scripts/validation/missing.sh>",
            "data:text/plain,scripts/validation/missing.sh",
            "file:scripts/validation/missing.sh",
            "https://example.test/scripts/validation/missing.sh",
            "/tmp/scripts/validation/missing.sh",
        )
        checked = (
            "SCRIPT=scripts/validation/missing.sh",
            "$BASE_DIR/scripts/validation/missing.sh",
            "${ROOT}/scripts/validation/missing.sh",
            "$(git rev-parse --show-toplevel)/scripts/validation/missing.sh",
        )
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            (root / "README.md").write_text("\n".join(ignored) + "\n", encoding="utf-8")
            self.assertEqual(0, run(root).returncode)

        for reference in checked:
            with (
                self.subTest(reference=reference),
                tempfile.TemporaryDirectory() as directory,
            ):
                root = pathlib.Path(directory)
                subprocess.run(["git", "init", "-q"], cwd=root, check=True)
                (root / "README.md").write_text(reference + "\n", encoding="utf-8")
                result = run(root)
                self.assertEqual(1, result.returncode)
                self.assertIn(
                    "missing script reference scripts/validation/missing.sh",
                    result.stderr,
                )

        self.assertIn("MAX_REFERENCE_CONTEXT_CHARS: Final = 4_096", block)
        self.assertIn("MAX_REFERENCE_CONTEXT_BYTES: Final = 4_096", block)
        scan_loop = block.split("for match in pattern.finditer(text):", 1)[1]
        self.assertLess(
            scan_loop.index("bounded_backward_context(text, match.start"),
            scan_loop.index('ref = match.group("ref")'),
        )

        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            readme = root / "README.md"
            exact = block.replace(
                "MAX_REFERENCE_CONTEXT_CHARS: Final = 4_096",
                "MAX_REFERENCE_CONTEXT_CHARS: Final = 16",
            ).replace(
                "MAX_REFERENCE_CONTEXT_BYTES: Final = 4_096",
                "MAX_REFERENCE_CONTEXT_BYTES: Final = 16",
            )
            readme.write_text(
                ("A" * 15) + "=scripts/validation/missing.sh\n", encoding="utf-8"
            )
            at_limit = run(root, exact)
            self.assertEqual(1, at_limit.returncode)
            self.assertIn("missing script reference", at_limit.stderr)
            readme.write_text(
                ("A" * 16) + "=scripts/validation/missing.sh\n", encoding="utf-8"
            )
            above = run(root, exact)
            self.assertEqual(1, above.returncode)
            self.assertEqual("FAIL: unsafe script-reference surface\n", above.stderr)

    def test_script_reference_scan_rejects_same_inode_metadata_mutation(self) -> None:
        source = REPO_CONTRACT.read_text(encoding="utf-8")
        start = "section \"Script reference integrity\"\nif ! python3 - <<'PY'; then\n"
        block = source.split(start, 1)[1].split(
            "\nPY\n  failures=$((failures + 1))",
            1,
        )[0]
        mutations = (
            (
                "lstat-to-open",
                "        initial = os.lstat(path)",
                "        initial = os.lstat(path)\n        os.chmod(path, 0o600)",
            ),
            (
                "open-to-final",
                "        final = os.fstat(file_descriptor)",
                "        os.chmod(path, 0o600)\n        final = os.fstat(file_descriptor)",
            ),
        )
        for label, mutation_point, replacement in mutations:
            with self.subTest(label=label):
                self.assertIn(mutation_point, block)
                mutated = block.replace(mutation_point, replacement, 1)
                with self._script_reference_fixture() as root:
                    docs = root / "docs"
                    docs.mkdir()
                    (docs / "active.md").write_text(
                        "ordinary prose\n", encoding="utf-8"
                    )
                    result = subprocess.run(
                        [sys.executable, "-c", mutated],
                        cwd=root,
                        capture_output=True,
                        text=True,
                        check=False,
                    )
                self.assertEqual(1, result.returncode)
                self.assertIn("unsafe script-reference surface", result.stderr)
                self.assertNotIn("active.md", result.stderr)

    def test_script_reference_scan_enforces_literal_ceiling_boundaries(self) -> None:
        source = REPO_CONTRACT.read_text(encoding="utf-8")
        start = "section \"Script reference integrity\"\nif ! python3 - <<'PY'; then\n"
        block = source.split(start, 1)[1].split(
            "\nPY\n  failures=$((failures + 1))",
            1,
        )[0]

        def run(
            root: pathlib.Path, program: str = block
        ) -> subprocess.CompletedProcess[str]:
            return subprocess.run(
                [sys.executable, "-c", program],
                cwd=root,
                capture_output=True,
                text=True,
                check=False,
                timeout=60,
            )

        with (
            self.subTest("surfaces-4096-and-4097"),
            tempfile.TemporaryDirectory() as directory,
        ):
            root = pathlib.Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            docs = root / "docs"
            docs.mkdir()
            for index in range(4_096):
                (docs / f"surface-{index:04d}.md").touch()
            self.assertEqual(0, run(root).returncode)
            (docs / "surface-over.md").touch()
            above = run(root)
            self.assertEqual(1, above.returncode)
            self.assertEqual("FAIL: unsafe script-reference surface\n", above.stderr)

        with (
            self.subTest("discovery-8192-and-8193"),
            tempfile.TemporaryDirectory() as directory,
        ):
            root = pathlib.Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            docs = root / "docs"
            docs.mkdir()
            for index in range(8_191):
                (docs / f"entry-{index:04d}").mkdir()
            ignore_start = block.index("def is_ignored(path: pathlib.Path) -> bool:")
            ignore_end = block.index("\n\n\ndef untracked_special_paths", ignore_start)
            fast_discovery = (
                block[:ignore_start]
                + "def is_ignored(path: pathlib.Path) -> bool:\n    return False"
                + block[ignore_end:]
            )
            self.assertEqual(0, run(root, fast_discovery).returncode)
            (docs / "entry-over").mkdir()
            above = run(root, fast_discovery)
            self.assertEqual(1, above.returncode)
            self.assertEqual("FAIL: unsafe script-reference surface\n", above.stderr)

        with (
            self.subTest("file-16mib-and-n-plus-one"),
            tempfile.TemporaryDirectory() as directory,
        ):
            root = pathlib.Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            docs = root / "docs"
            docs.mkdir()
            surface = docs / "surface.md"
            surface.write_bytes(b"\0" * (16 * 1_048_576))
            self.assertEqual(0, run(root).returncode)
            with surface.open("ab") as stream:
                stream.write(b"\0")
            above = run(root)
            self.assertEqual(1, above.returncode)
            self.assertEqual("FAIL: unsafe script-reference surface\n", above.stderr)

        with (
            self.subTest("aggregate-64mib-and-n-plus-one"),
            tempfile.TemporaryDirectory() as directory,
        ):
            root = pathlib.Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            docs = root / "docs"
            docs.mkdir()
            for index in range(4):
                (docs / f"surface-{index}.md").write_bytes(b"\0" * (16 * 1_048_576))
            self.assertEqual(0, run(root).returncode)
            (docs / "surface-4.md").write_bytes(b"\0")
            above = run(root)
            self.assertEqual(1, above.returncode)
            self.assertEqual("FAIL: unsafe script-reference surface\n", above.stderr)

    def test_typed_harness_replacement_covers_removed_aggregate_routes(self) -> None:
        contract_text = (
            ROOT / "scripts/validation/agent_governance_contract.py"
        ).read_text(encoding="utf-8")
        for relative, fragment in (
            (".github/PULL_REQUEST_TEMPLATE.md", "validate-harness.sh"),
            ("scripts/README.md", "validate-harness.sh"),
            ("scripts/README.md", "run-local-qa-gates.sh --harness"),
            ("docs/00.agent-governance/README.md", "harness-implementation-map.md"),
        ):
            with self.subTest(relative=relative, fragment=fragment):
                self.assertIn(relative, contract_text)
                self.assertIn(fragment, contract_text)
        self.assertNotRegex(
            (ROOT / "scripts/validation/check-repo-contracts.sh").read_text(
                encoding="utf-8"
            ),
            r"grep .*validate-harness",
        )

    def test_local_profiles_exclude_compose_env_setup(self) -> None:
        contract = json.loads(
            (ROOT / ".github/workflow-contract.yml").read_text(
                encoding="utf-8"
            )
        )
        node_by_id = {
            node["gate_id"]: node for node in contract["gate_nodes"]
        }

        def expand(roots):
            expanded = []
            seen = set()

            def visit(gate_id):
                if gate_id in seen:
                    return
                seen.add(gate_id)
                node = node_by_id[gate_id]
                if node["kind"] == "aggregate":
                    for child in node["children"]:
                        visit(child)
                else:
                    expanded.append(gate_id)

            for root in roots:
                visit(root)
            return expanded

        for profile in contract["profile_roots"]:
            with self.subTest(profile=profile["profile"]):
                self.assertNotIn(
                    "setup.compose-env",
                    expand(profile["root_gate_ids"]),
                )

    def test_local_wrapper_preserves_existing_env_bytes(self) -> None:
        source = (
            ROOT / "scripts/validation/run-local-qa-gates.sh"
        ).read_text(encoding="utf-8")
        self.assertNotIn("cp .env.example .env", source)
        self.assertNotRegex(source, r"(?:>|>>)\s*\.env(?:\s|$)")
        self.assertNotIn("rm .env", source)

    def test_descriptor_mode_root_and_import_compatibility_set_is_exact(
        self,
    ) -> None:
        expected = {
            "scripts/hardening/check-all-hardening.sh",
            "scripts/operations/sync-provider-surfaces.sh",
            "scripts/operations/sync-tech-stack-versions.sh",
            "scripts/validation/check-agent-governance-contract.py",
            "scripts/validation/check-document-corpus-lifecycle.py",
            "scripts/validation/check-document-metadata.py",
            "scripts/validation/check-supply-chain-policy.py",
        }
        for relative in sorted(expected):
            with self.subTest(relative=relative):
                source = (ROOT / relative).read_text(encoding="utf-8")
                self.assertIn("HYHOME_CI_GATE_ROOT", source)
        references = {
            path.relative_to(ROOT).as_posix()
            for root in (ROOT / "scripts",)
            for path in root.rglob("*")
            if path.is_file()
            and "__pycache__" not in path.parts
            and "HYHOME_CI_GATE_ROOT" in path.read_text(
                encoding="utf-8",
                errors="ignore",
            )
            and path.name
            not in {
                "ci_gate_adapters.py",
                "ci_gate_runner.py",
                "test_ci_gate_runner.py",
            }
        }
        self.assertEqual(expected, references)

    def test_descriptor_compatibility_consumers_validate_root_identity(
        self,
    ) -> None:
        consumers = {
            "scripts/hardening/check-all-hardening.sh": "shell",
            "scripts/operations/sync-provider-surfaces.sh": "shell",
            "scripts/operations/sync-tech-stack-versions.sh": "shell",
            "scripts/validation/check-agent-governance-contract.py": "python",
            "scripts/validation/check-document-corpus-lifecycle.py": "python",
            "scripts/validation/check-document-metadata.py": "python",
            "scripts/validation/check-supply-chain-policy.py": "python",
        }
        diagnostic = "FAIL: invalid HYHOME_CI_GATE_ROOT\n"
        for relative, kind in consumers.items():
            with self.subTest(relative=relative), tempfile.TemporaryDirectory() as directory:
                fixture_root = pathlib.Path(directory) / "repository"
                target = fixture_root / relative
                target.parent.mkdir(parents=True)
                shutil.copy2(ROOT / relative, target)
                validation = fixture_root / "scripts/validation"
                validation.mkdir(parents=True, exist_ok=True)
                sibling = validation / "agent_governance_contract.py"
                if not sibling.exists():
                    shutil.copy2(
                        ROOT / "scripts/validation/agent_governance_contract.py",
                        sibling,
                    )
                if relative.endswith("check-document-corpus-lifecycle.py"):
                    shutil.copy2(
                        ROOT / "scripts/validation/check-document-metadata.py",
                        validation / "check-document-metadata.py",
                    )

                if kind == "shell":
                    source = target.read_text(encoding="utf-8")
                    marker = 'REPO_ROOT="$(_verified_repository_root)"\n'
                    self.assertIn(marker, source)
                    target.write_text(
                        source.replace(
                            marker,
                            marker + "printf '%s\\n' \"$REPO_ROOT\"\nexit 0\n",
                            1,
                        ),
                        encoding="utf-8",
                    )
                    direct_command = ["bash", str(target)]
                else:
                    direct_command = [
                        sys.executable,
                        "-c",
                        (
                            "import importlib.util, pathlib, sys;"
                            "p=pathlib.Path(sys.argv[1]);"
                            "s=importlib.util.spec_from_file_location('probe',p);"
                            "m=importlib.util.module_from_spec(s);"
                            "sys.modules[s.name]=m;"
                            "sys.path.insert(0,str(p.parent));"
                            "s.loader.exec_module(m);"
                            "print(m.ROOT);"
                            "print(sys.modules.get('agent_governance_contract').__file__ "
                            "if p.name == 'check-document-metadata.py' else '-')"
                        ),
                        str(target),
                    ]

                direct_env = os.environ.copy()
                direct_env.pop("HYHOME_CI_GATE_ROOT", None)
                direct = subprocess.run(
                    direct_command,
                    cwd=fixture_root,
                    env=direct_env,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(0, direct.returncode, direct.stderr)
                self.assertEqual(
                    str(fixture_root),
                    direct.stdout.splitlines()[0],
                )

                root_fd = os.open(
                    fixture_root,
                    os.O_RDONLY | getattr(os, "O_DIRECTORY", 0),
                )
                entrypoint_fd = (
                    os.open(target, os.O_RDONLY)
                    if kind == "shell"
                    else None
                )
                try:
                    descriptor_env = direct_env | {
                        "HYHOME_CI_GATE_ROOT": f"/proc/self/fd/{root_fd}"
                    }
                    descriptor_command = (
                        ["bash", f"/proc/self/fd/{entrypoint_fd}"]
                        if entrypoint_fd is not None
                        else direct_command
                    )
                    inherited_fds = (
                        (entrypoint_fd, root_fd)
                        if entrypoint_fd is not None
                        else (root_fd,)
                    )
                    valid = subprocess.run(
                        descriptor_command,
                        cwd=fixture_root,
                        env=descriptor_env,
                        pass_fds=inherited_fds,
                        capture_output=True,
                        text=True,
                        check=False,
                    )
                finally:
                    if entrypoint_fd is not None:
                        os.close(entrypoint_fd)
                    os.close(root_fd)
                self.assertEqual(0, valid.returncode, valid.stderr)
                self.assertRegex(
                    valid.stdout.splitlines()[0],
                    r"\A/proc/self/fd/[0-9]+\Z",
                )
                if relative.endswith("check-document-metadata.py"):
                    self.assertRegex(
                        valid.stdout.splitlines()[1],
                        r"\A/proc/self/fd/[0-9]+/scripts/validation/"
                        r"agent_governance_contract\.py\Z",
                    )

                entrypoint_fd = (
                    os.open(target, os.O_RDONLY)
                    if kind == "shell"
                    else None
                )
                try:
                    invalid = subprocess.run(
                        (
                            ["bash", f"/proc/self/fd/{entrypoint_fd}"]
                            if entrypoint_fd is not None
                            else direct_command
                        ),
                        cwd=fixture_root,
                        env=direct_env
                        | {"HYHOME_CI_GATE_ROOT": "/tmp/not-a-descriptor"},
                        pass_fds=(
                            (entrypoint_fd,)
                            if entrypoint_fd is not None
                            else ()
                        ),
                        capture_output=True,
                        text=True,
                        check=False,
                    )
                finally:
                    if entrypoint_fd is not None:
                        os.close(entrypoint_fd)
                self.assertNotEqual(0, invalid.returncode)
                self.assertEqual(diagnostic, invalid.stderr)

                with tempfile.TemporaryDirectory() as other_directory:
                    other_fd = os.open(
                        other_directory,
                        os.O_RDONLY | getattr(os, "O_DIRECTORY", 0),
                    )
                    entrypoint_fd = (
                        os.open(target, os.O_RDONLY)
                        if kind == "shell"
                        else None
                    )
                    try:
                        mismatched = subprocess.run(
                            (
                                ["bash", f"/proc/self/fd/{entrypoint_fd}"]
                                if entrypoint_fd is not None
                                else direct_command
                            ),
                            cwd=fixture_root,
                            env=direct_env
                            | {
                                "HYHOME_CI_GATE_ROOT": (
                                    f"/proc/self/fd/{other_fd}"
                                )
                            },
                            pass_fds=(
                                (entrypoint_fd, other_fd)
                                if entrypoint_fd is not None
                                else (other_fd,)
                            ),
                            capture_output=True,
                            text=True,
                            check=False,
                        )
                    finally:
                        if entrypoint_fd is not None:
                            os.close(entrypoint_fd)
                        os.close(other_fd)
                self.assertNotEqual(0, mismatched.returncode)
                self.assertEqual(diagnostic, mismatched.stderr)

    def test_typed_repository_wiring_matches_exact_registered_node(self) -> None:
        program = self._repo_python_program("Typed repository gate wiring")
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            contract = root / ".github/workflow-contract.yml"
            contract.parent.mkdir(parents=True)
            shutil.copy2(ROOT / ".github/workflow-contract.yml", contract)
            baseline = subprocess.run(
                [sys.executable, "-c", program],
                cwd=root,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(0, baseline.returncode, baseline.stderr)

            document = json.loads(contract.read_text(encoding="utf-8"))
            repo_leaf = next(
                node
                for node in document["gate_nodes"]
                if node["gate_id"] == "leaf.repo-contracts"
            )
            repo_leaf["profiles"] = ["ci"]
            contract.write_text(
                json.dumps(document, indent=2) + "\n",
                encoding="utf-8",
            )
            mutated = subprocess.run(
                [sys.executable, "-c", program],
                cwd=root,
                capture_output=True,
                text=True,
                check=False,
            )
        self.assertEqual(1, mutated.returncode)
        self.assertEqual(
            "FAIL: typed repository gate wiring differs from the exact contract\n",
            mutated.stderr,
        )

    def test_repository_umbrella_is_wiring_only(self) -> None:
        source = (
            ROOT / "scripts/validation/check-repo-contracts.sh"
        ).read_text(encoding="utf-8")
        contract = json.loads(
            (ROOT / ".github/workflow-contract.yml").read_text(
                encoding="utf-8"
            )
        )
        sibling_entrypoints = {
            node["entrypoint"]
            for node in contract["gate_nodes"]
            if node["kind"] in {"leaf", "setup"}
            and node["gate_id"] != "leaf.repo-contracts"
        }
        dispatched = self._registered_sibling_dispatches(
            source,
            sibling_entrypoints,
        )
        self.assertEqual(set(), dispatched)
        sibling = "scripts/validation/check-target-surface-contract.py"
        assignment_sibling = "scripts/validation/check-document-metadata.py"
        dispatch_mutations = {
            "literal-python": f"\npython3 {sibling}\n",
            "literal-bash": f"\nbash {sibling}\n",
            "direct-executable": f"\n{sibling}\n",
            "quoted-path": f'\npython3 "{sibling}"\n',
            "variable-mediated": (
                f'\nregistered_gate="{sibling}"\npython3 "$registered_gate"\n'
            ),
            "command-wrapper": f"\ncommand python3 {sibling}\n",
            "command-p-wrapper": f"\ncommand -p python3 {sibling}\n",
            "command-pp-wrapper": f"\ncommand -pp python3 {sibling}\n",
            "command-stop-wrapper": f"\ncommand -- python3 {sibling}\n",
            "env-wrapper": f"\nenv LANG=C python3 {sibling}\n",
            "env-dash-wrapper": f"\nenv - python3 {sibling}\n",
            "env-ignore-short-wrapper": f"\nenv -i python3 {sibling}\n",
            "env-ignore-long-wrapper": (
                f"\nenv --ignore-environment python3 {sibling}\n"
            ),
            "env-debug-short-wrapper": f"\nenv -v python3 {sibling}\n",
            "env-debug-long-wrapper": f"\nenv --debug python3 {sibling}\n",
            "env-list-signal-wrapper": (
                f"\nenv --list-signal-handling python3 {sibling}\n"
            ),
            "env-block-signal-wrapper": (
                f"\nenv --block-signal python3 {sibling}\n"
            ),
            "env-block-signal-equals-wrapper": (
                f"\nenv --block-signal=PIPE python3 {sibling}\n"
            ),
            "env-default-signal-wrapper": (
                f"\nenv --default-signal python3 {sibling}\n"
            ),
            "env-default-signal-equals-wrapper": (
                f"\nenv --default-signal=PIPE python3 {sibling}\n"
            ),
            "env-ignore-signal-wrapper": (
                f"\nenv --ignore-signal python3 {sibling}\n"
            ),
            "env-ignore-signal-equals-wrapper": (
                f"\nenv --ignore-signal=PIPE python3 {sibling}\n"
            ),
            "env-unset-short-wrapper": f"\nenv -u NAME python3 {sibling}\n",
            "env-unset-attached-wrapper": f"\nenv -uNAME python3 {sibling}\n",
            "env-unset-long-wrapper": f"\nenv --unset NAME python3 {sibling}\n",
            "env-unset-equals-wrapper": (
                f"\nenv --unset=NAME python3 {sibling}\n"
            ),
            "env-chdir-short-wrapper": f"\nenv -C DIR python3 {sibling}\n",
            "env-chdir-attached-wrapper": f"\nenv -CDIR python3 {sibling}\n",
            "env-chdir-long-wrapper": f"\nenv --chdir DIR python3 {sibling}\n",
            "env-chdir-equals-wrapper": f"\nenv --chdir=DIR python3 {sibling}\n",
            "env-argv0-short-wrapper": f"\nenv -a ARG python3 {sibling}\n",
            "env-argv0-attached-wrapper": f"\nenv -aARG python3 {sibling}\n",
            "env-argv0-long-wrapper": f"\nenv --argv0 ARG python3 {sibling}\n",
            "env-argv0-equals-wrapper": (
                f"\nenv --argv0=ARG python3 {sibling}\n"
            ),
            "env-short-cluster-wrapper": f"\nenv -iv python3 {sibling}\n",
            "env-split-short-cluster-wrapper": (
                f"\nenv -vS'python3 {sibling}'\n"
            ),
            "env-split-short-wrapper": f"\nenv -S 'python3 {sibling}'\n",
            "env-split-attached-wrapper": f"\nenv -S'python3 {sibling}'\n",
            "env-split-long-wrapper": (
                f"\nenv --split-string 'python3 {sibling}'\n"
            ),
            "env-split-equals-wrapper": (
                f"\nenv --split-string='python3 {sibling}'\n"
            ),
            "env-assignment-wrapper": f"\nenv LANG=C python3 {sibling}\n",
            "env-stop-assignment-wrapper": (
                f"\nenv -- NAME=VALUE python3 {sibling}\n"
            ),
            "env-stop-two-assignments-wrapper": (
                f"\nenv -- A=1 B=2 python3 {sibling}\n"
            ),
            "env-stop-assignment-then-command-wrapper": (
                f"\nenv -- NAME={assignment_sibling} python3 {sibling}\n"
            ),
            "env-split-whitespace-wrapper": f"\nenv -S 'python3 {sibling}'\n",
            "env-split-quoted-whitespace-wrapper": (
                f"\nenv -S 'python3 \"{sibling}\"'\n"
            ),
            "env-split-underscore-wrapper": f"\nenv -S 'python3\\_{sibling}'\n",
            "env-split-nested-wrapper": (
                f"\nenv -S 'command -p exec -a gate python3 {sibling}'\n"
            ),
            "env-nested-chain-wrapper": (
                f"\nenv -u HOME command -p exec -a gate python3 {sibling}\n"
            ),
            "exec-wrapper": f"\nexec python3 {sibling}\n",
            "exec-argv0-wrapper": f"\nexec -a NAME python3 {sibling}\n",
            "exec-argv0-attached-wrapper": f"\nexec -aNAME python3 {sibling}\n",
            "exec-clear-wrapper": f"\nexec -c python3 {sibling}\n",
            "exec-login-wrapper": f"\nexec -l python3 {sibling}\n",
            "exec-cluster-wrapper": f"\nexec -cl python3 {sibling}\n",
            "exec-cluster-argv0-wrapper": f"\nexec -claNAME python3 {sibling}\n",
            "exec-stop-wrapper": f"\nexec -- python3 {sibling}\n",
            "helper-indirection": (
                '\nrun_registered_gate() { python3 "$1"; }\n'
                f"run_registered_gate {sibling}\n"
            ),
            "python-subprocess": (
                "\npython3 - <<'PY'\n"
                "import subprocess\n"
                f"subprocess.run(['python3', '{sibling}'], check=False)\n"
                "PY\n"
            ),
            "python-os-system": (
                "\npython3 - <<'PY'\n"
                "import os\n"
                f"os.system('python3 {sibling}')\n"
                "PY\n"
            ),
        }
        for family, mutation in dispatch_mutations.items():
            with self.subTest(family=family):
                self.assertEqual(
                    {sibling},
                    self._registered_sibling_dispatches(
                        source + mutation,
                        sibling_entrypoints,
                    ),
                )
        split_transition_dispatch = {
            "env-split-direct-separated": f"\nenv -S '{sibling}'\n",
            "env-split-direct-attached": f"\nenv -S'{sibling}'\n",
            "env-split-direct-clustered": f"\nenv -vS'{sibling}'\n",
            "env-split-long-separated": (
                f"\nenv --split-string '{sibling}'\n"
            ),
            "env-split-long-equals": (
                f"\nenv --split-string='{sibling}'\n"
            ),
            "env-split-long-python-separated": (
                f"\nenv --split-string 'python3 {sibling}'\n"
            ),
            "env-split-long-python-equals": (
                f"\nenv --split-string='python3 {sibling}'\n"
            ),
            "env-split-nested-dispatch": (
                f"\nenv -S 'command -p exec -a gate python3 {sibling}'\n"
            ),
        }
        for family, mutation in split_transition_dispatch.items():
            with self.subTest(family=family):
                self.assertEqual(
                    {sibling},
                    self._registered_sibling_dispatches(
                        source + mutation,
                        sibling_entrypoints,
                    ),
                    "candidate-closed parser outcome matrix must hold",
                )

        split_transition_no_dispatch = {
            "env-split-query-separated": (
                f"\nenv -S 'command -v python3 {sibling}'\n"
            ),
            "env-split-query-attached": (
                f"\nenv -S'command -v python3 {sibling}'\n"
            ),
            "env-split-query-clustered": (
                f"\nenv -vS'command -v python3 {sibling}'\n"
            ),
            "env-split-query-long-separated": (
                f"\nenv --split-string 'command -v python3 {sibling}'\n"
            ),
            "env-split-query-long-equals": (
                f"\nenv --split-string='command -v python3 {sibling}'\n"
            ),
        }
        for family, mutation in split_transition_no_dispatch.items():
            with self.subTest(family=family):
                self.assertEqual(
                    set(),
                    self._registered_sibling_dispatches(
                        source + mutation,
                        sibling_entrypoints,
                    ),
                    "candidate-closed parser outcome matrix must hold",
                )

        dynamic_relevant_mutations = {
            "direct-named-dynamic-target": f'\n"$RUNNER" {sibling}\n',
            "direct-braced-named-dynamic-target": (
                f'\n"${{RUNNER}}" {sibling}\n'
            ),
            "command-named-dynamic-target": (
                f'\ncommand "$RUNNER" {sibling}\n'
            ),
            "command-braced-named-dynamic-target": (
                f'\ncommand "${{RUNNER}}" {sibling}\n'
            ),
            "python-named-dynamic-script": (
                f'\npython3 "$SCRIPT" {sibling}\n'
            ),
            "python-braced-named-dynamic-script": (
                f'\npython3 "${{SCRIPT}}" {sibling}\n'
            ),
            "bash-named-dynamic-script": f'\nbash "$SCRIPT" {sibling}\n',
            "bash-braced-named-dynamic-script": (
                f'\nbash "${{SCRIPT}}" {sibling}\n'
            ),
            "direct-positional-target": f'\n"$1" {sibling}\n',
            "direct-braced-positional-target": f'\n"${{1}}" {sibling}\n',
            "command-positional-target": f'\ncommand "$1" {sibling}\n',
            "command-braced-positional-target": (
                f'\ncommand "${{1}}" {sibling}\n'
            ),
            "python-positional-script": f'\npython3 "$1" {sibling}\n',
            "python-braced-positional-script": (
                f'\npython3 "${{1}}" {sibling}\n'
            ),
            "bash-positional-script": f'\nbash "$1" {sibling}\n',
            "bash-braced-positional-script": f'\nbash "${{1}}" {sibling}\n',
        }
        for family, mutation in dynamic_relevant_mutations.items():
            with self.subTest(family=family):
                self.assertEqual(
                    {sibling},
                    self._registered_sibling_dispatches(
                        source + mutation,
                        sibling_entrypoints,
                    ),
                    "candidate-closed parser outcome matrix must hold",
                )

        harmless = "not-a-registered-sibling"
        dynamic_no_relevant_mutations = {
            "direct-named-no-relevant": f'\n"$RUNNER" {harmless}\n',
            "direct-braced-named-no-relevant": (
                f'\n"${{RUNNER}}" {harmless}\n'
            ),
            "command-named-no-relevant": (
                f'\ncommand "$RUNNER" {harmless}\n'
            ),
            "command-braced-named-no-relevant": (
                f'\ncommand "${{RUNNER}}" {harmless}\n'
            ),
            "python-named-no-relevant": f'\npython3 "$SCRIPT" {harmless}\n',
            "python-braced-named-no-relevant": (
                f'\npython3 "${{SCRIPT}}" {harmless}\n'
            ),
            "bash-named-no-relevant": f'\nbash "$SCRIPT" {harmless}\n',
            "bash-braced-named-no-relevant": (
                f'\nbash "${{SCRIPT}}" {harmless}\n'
            ),
            "direct-positional-no-relevant": f'\n"$1" {harmless}\n',
            "direct-braced-positional-no-relevant": (
                f'\n"${{1}}" {harmless}\n'
            ),
            "command-positional-no-relevant": f'\ncommand "$1" {harmless}\n',
            "command-braced-positional-no-relevant": (
                f'\ncommand "${{1}}" {harmless}\n'
            ),
            "python-positional-no-relevant": f'\npython3 "$1" {harmless}\n',
            "python-braced-positional-no-relevant": (
                f'\npython3 "${{1}}" {harmless}\n'
            ),
            "bash-positional-no-relevant": f'\nbash "$1" {harmless}\n',
            "bash-braced-positional-no-relevant": (
                f'\nbash "${{1}}" {harmless}\n'
            ),
        }
        for family, mutation in dynamic_no_relevant_mutations.items():
            with self.subTest(family=family):
                self.assertEqual(
                    set(),
                    self._registered_sibling_dispatches(
                        source + mutation,
                        sibling_entrypoints,
                    ),
                    "candidate-closed parser outcome matrix must hold",
                )

        dynamic_query_mutations = {
            "command-named-query-v": f'\ncommand -v "$RUNNER" {sibling}\n',
            "command-named-query-V": f'\ncommand -V "$RUNNER" {sibling}\n',
            "command-named-query-cluster": (
                f'\ncommand -pv "$RUNNER" {sibling}\n'
            ),
            "command-braced-named-query-cluster": (
                f'\ncommand -pV "${{RUNNER}}" {sibling}\n'
            ),
            "command-positional-query-v": f'\ncommand -v "$1" {sibling}\n',
            "command-positional-query-cluster": (
                f'\ncommand -pV "$1" {sibling}\n'
            ),
            "command-braced-positional-query-cluster": (
                f'\ncommand -vp "${{1}}" {sibling}\n'
            ),
        }
        for family, mutation in dynamic_query_mutations.items():
            with self.subTest(family=family):
                self.assertEqual(
                    set(),
                    self._registered_sibling_dispatches(
                        source + mutation,
                        sibling_entrypoints,
                    ),
                    "candidate-closed parser outcome matrix must hold",
                )

        candidate_union_mutations = {
            "env-block-signal-candidate-union": (
                f"\nenv --block-signalX={assignment_sibling} "
                f"python3 {sibling}\n"
            ),
            "env-default-signal-candidate-union": (
                f"\nenv --default-signalX={assignment_sibling} "
                f"python3 {sibling}\n"
            ),
            "env-ignore-signal-candidate-union": (
                f"\nenv --ignore-signalX={assignment_sibling} "
                f"python3 {sibling}\n"
            ),
        }
        for family, mutation in candidate_union_mutations.items():
            with self.subTest(family=family):
                self.assertEqual(
                    {assignment_sibling, sibling},
                    self._registered_sibling_dispatches(
                        source + mutation,
                        sibling_entrypoints,
                    ),
                    "candidate-closed parser outcome matrix must hold",
                )

        valid_signal_operands = {
            "env-block-signal-exact-value": (
                f"\nenv --block-signal={assignment_sibling} true\n"
            ),
            "env-default-signal-exact-value": (
                f"\nenv --default-signal={assignment_sibling} true\n"
            ),
            "env-ignore-signal-exact-value": (
                f"\nenv --ignore-signal={assignment_sibling} true\n"
            ),
        }
        for family, mutation in valid_signal_operands.items():
            with self.subTest(family=family):
                self.assertEqual(
                    set(),
                    self._registered_sibling_dispatches(
                        source + mutation,
                        sibling_entrypoints,
                    ),
                    "candidate-closed parser outcome matrix must hold",
                )

        valid_signal_commands = {
            "env-block-signal-exact-command": (
                f"\nenv --block-signal={assignment_sibling} "
                f"python3 {sibling}\n"
            ),
            "env-default-signal-exact-command": (
                f"\nenv --default-signal={assignment_sibling} "
                f"python3 {sibling}\n"
            ),
            "env-ignore-signal-exact-command": (
                f"\nenv --ignore-signal={assignment_sibling} "
                f"python3 {sibling}\n"
            ),
        }
        for family, mutation in valid_signal_commands.items():
            with self.subTest(family=family):
                self.assertEqual(
                    {sibling},
                    self._registered_sibling_dispatches(
                        source + mutation,
                        sibling_entrypoints,
                    ),
                    "candidate-closed parser outcome matrix must hold",
                )
        for retired in (
            "lifecycle_gate_commands",
            "workflow_gate_commands",
            "generated_freshness_commands",
            "run_generated_freshness_gates",
            "Verify document metadata comparison base",
            "Check changed and new document metadata",
        ):
            with self.subTest(retired=retired):
                self.assertNotIn(retired, source)
        query_or_absent_mutations = {
            "command-query-v": f"\ncommand -v python3 {sibling}\n",
            "command-query-V": f"\ncommand -V python3 {sibling}\n",
            "command-query-pv": f"\ncommand -pv python3 {sibling}\n",
            "command-query-pV": f"\ncommand -pV python3 {sibling}\n",
            "command-query-vp": f"\ncommand -vp python3 {sibling}\n",
            "env-null-short": f"\nenv -0 python3 {sibling}\n",
            "env-null-long": f"\nenv --null python3 {sibling}\n",
            "env-help": f"\nenv --help python3 {sibling}\n",
            "env-version": f"\nenv --version python3 {sibling}\n",
            "env-stop-assignment-only": f"\nenv -- NAME={sibling}\n",
            "env-stop-dash-command": f"\nenv -- -command {sibling}\n",
            "env-split-c-discard": f"\nenv -S 'python3\\c {sibling}'\n",
            "env-split-comment-discard": f"\nenv -S '# python3 {sibling}'\n",
            "env-unset-sibling-operand": f"\nenv -u {sibling}\n",
            "env-chdir-sibling-operand": f"\nenv -C {sibling}\n",
            "env-argv0-sibling-operand": f"\nenv -a {sibling}\n",
            "exec-argv0-sibling-operand": f"\nexec -a {sibling}\n",
        }
        for family, mutation in query_or_absent_mutations.items():
            with self.subTest(family=family):
                self.assertEqual(
                    set(),
                    self._registered_sibling_dispatches(
                        source + mutation,
                        sibling_entrypoints,
                    ),
                )
        fail_closed_mutations = {
            "command-unknown-option": f"\ncommand --bad {sibling}\n",
            "exec-missing-a-operand": "\nexec -a\n",
            "exec-unknown-option": f"\nexec --bad {sibling}\n",
            "env-missing-unset-operand": "\nenv -u\n",
            "env-missing-chdir-operand": "\nenv -C\n",
            "env-missing-argv0-operand": "\nenv -a\n",
            "env-unknown-option": f"\nenv --bad {sibling}\n",
            "env-split-env-expansion": f"\nenv -S '${{GATE}} {sibling}'\n",
            "env-split-invalid-escape": f"\nenv -S 'python3\\x {sibling}'\n",
            "env-split-malformed-quote": f"\nenv -S \"'python3 {sibling}\"\n",
            "env-budget-exhaustion": (
                "\n"
                + " ".join(["env -S '"] + ["env -S "] * 80)
                + f"python3 {sibling}'\n"
            ),
        }
        for family, mutation in fail_closed_mutations.items():
            with self.subTest(family=family):
                self.assertIn(
                    sibling,
                    self._registered_sibling_dispatches(
                        source + mutation,
                        sibling_entrypoints,
                    ),
                )
        self.assertIn(
            sibling,
            self._registered_sibling_dispatches(
                source + f"\nenv -- NAME=VALUE python3 {sibling}\n",
                sibling_entrypoints,
            ),
            "GNU env -- assignment scan must reach command",
        )

    @staticmethod
    def _registered_sibling_dispatches(
        source: str,
        sibling_entrypoints: set[str],
    ) -> set[str]:
        dispatched: set[str] = set()
        heredoc_re = re.compile(
            r"(?ms)^(?P<header>[^\n]*\bpython3\b[^\n]*"
            r"<<[\"']?(?P<tag>[A-Za-z_][A-Za-z0-9_]*)[\"']?[^\n]*)\n"
            r"(?P<body>.*?)^(?P=tag)[ \t]*$"
        )

        def static_value(
            node: ast.AST,
            values: dict[str, object],
        ) -> object | None:
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                return node.value
            if isinstance(node, ast.Name):
                return values.get(node.id)
            if isinstance(node, (ast.List, ast.Tuple)):
                resolved = [static_value(item, values) for item in node.elts]
                if all(isinstance(item, str) for item in resolved):
                    return resolved
            if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
                left = static_value(node.left, values)
                right = static_value(node.right, values)
                if isinstance(left, str) and isinstance(right, str):
                    return left + right
                if isinstance(left, list) and isinstance(right, list):
                    return left + right
            return None

        def command_paths(value: object) -> set[str]:
            if isinstance(value, str):
                try:
                    tokens = shlex.split(value)
                except ValueError:
                    tokens = value.split()
            elif isinstance(value, list):
                tokens = [item for item in value if isinstance(item, str)]
            else:
                return set()
            return sibling_entrypoints.intersection(tokens)

        def python_dispatches(body: str) -> set[str]:
            try:
                tree = ast.parse(body)
            except SyntaxError:
                if (
                    ("subprocess" in body or "os.system" in body)
                    and any(path in body for path in sibling_entrypoints)
                ):
                    return {
                        path
                        for path in sibling_entrypoints
                        if path in body
                    }
                return set()
            values: dict[str, object] = {}
            assignments = [
                node
                for node in ast.walk(tree)
                if isinstance(node, (ast.Assign, ast.AnnAssign))
            ]
            for _ in range(len(assignments) + 1):
                changed = False
                for assignment in assignments:
                    targets = (
                        assignment.targets
                        if isinstance(assignment, ast.Assign)
                        else [assignment.target]
                    )
                    value_node = assignment.value
                    if value_node is None:
                        continue
                    value = static_value(value_node, values)
                    for target in targets:
                        if (
                            isinstance(target, ast.Name)
                            and value is not None
                            and values.get(target.id) != value
                        ):
                            values[target.id] = value
                            changed = True
                if not changed:
                    break
            found: set[str] = set()
            subprocess_sinks = {
                "run",
                "call",
                "check_call",
                "check_output",
                "Popen",
            }
            for node in ast.walk(tree):
                if not isinstance(node, ast.Call) or not node.args:
                    continue
                function = node.func
                is_sink = (
                    isinstance(function, ast.Attribute)
                    and isinstance(function.value, ast.Name)
                    and (
                        (
                            function.value.id == "subprocess"
                            and function.attr in subprocess_sinks
                        )
                        or (
                            function.value.id == "os"
                            and function.attr == "system"
                        )
                    )
                )
                if is_sink:
                    found.update(
                        command_paths(static_value(node.args[0], values))
                    )
            return found

        shell_source = source
        for match in reversed(tuple(heredoc_re.finditer(source))):
            dispatched.update(python_dispatches(match.group("body")))
            shell_source = (
                shell_source[: match.start("body")]
                + "\n" * match.group("body").count("\n")
                + shell_source[match.end("body") :]
            )

        variables: dict[str, str] = {}
        assignment_re = re.compile(
            r"^\s*(?:local\s+|declare(?:\s+-[A-Za-z]+)?\s+)?"
            r"(?P<name>[A-Za-z_][A-Za-z0-9_]*)="
            r"(?P<quote>[\"']?)(?P<value>scripts/[^\"'\s;]+)(?P=quote)\s*$"
        )
        for statement in re.split(r"[;\n]", shell_source.replace("\\\n", " ")):
            match = assignment_re.match(statement)
            if match and match.group("value") in sibling_entrypoints:
                variables[match.group("name")] = match.group("value")

        variable_re = re.compile(
            r"^\$(?:\{(?P<braced>[A-Za-z_][A-Za-z0-9_]*)\}|"
            r"(?P<plain>[A-Za-z_][A-Za-z0-9_]*))$"
        )

        def resolved_path(token: str, positional: str | None = None) -> str | None:
            if token in sibling_entrypoints:
                return token
            if token in {"$1", "${1}"}:
                return positional
            match = variable_re.fullmatch(token)
            if match:
                return variables.get(
                    match.group("braced") or match.group("plain")
                )
            return None

        def command_sink(
            statement: str,
            *,
            positional: str | None = None,
        ) -> set[str]:
            try:
                tokens = shlex.split(statement, comments=True)
            except ValueError:
                return {
                    path
                    for path in sibling_entrypoints
                    if path in statement
                }
            while tokens and tokens[0] in {
                "if",
                "then",
                "elif",
                "while",
                "until",
                "do",
                "!",
                "{",
                "}",
            }:
                tokens.pop(0)
            budget = 8 * (
                1
                + len(tokens)
                + sum(len(token) for token in tokens)
            )

            ParseResult = tuple[str, frozenset[str]]

            def candidate_paths(items: list[str]) -> set[str]:
                found: set[str] = set()
                for token in items:
                    exact = resolved_path(token, positional)
                    if exact is not None:
                        found.add(exact)
                    found.update(
                        path
                        for path in sibling_entrypoints
                        if path in token
                    )
                return found

            def dispatch(paths: set[str]) -> ParseResult:
                return ("dispatch", frozenset(paths))

            def no_dispatch() -> ParseResult:
                return ("no-dispatch", frozenset())

            def ambiguous(items: list[str]) -> ParseResult:
                candidates = candidate_paths(items)
                if not candidates:
                    candidates = set(sibling_entrypoints)
                return ("ambiguous", frozenset(candidates))

            def materialize(result: ParseResult) -> set[str]:
                kind, paths = result
                if kind == "no-dispatch":
                    return set()
                if kind in {"dispatch", "ambiguous"}:
                    return set(paths)
                raise AssertionError("invalid parser outcome")

            def has_relevant_sibling(items: list[str]) -> bool:
                return bool(candidate_paths(items))

            def is_unresolved_dynamic_target(token: str) -> bool:
                is_supported_dynamic = (
                    token in {"$1", "${1}"}
                    or variable_re.fullmatch(token) is not None
                )
                return (
                    is_supported_dynamic
                    and resolved_path(token, positional) is None
                )

            def charge(amount: int = 1) -> bool:
                nonlocal budget
                budget -= amount
                return budget >= 0

            def split_env_static(value: str) -> list[str] | None:
                result: list[str] = []
                current: list[str] = []
                quote: str | None = None
                index = 0
                started = False
                while index < len(value):
                    if not charge():
                        return None
                    character = value[index]
                    if quote is None and character in " \t\n\r\v\f":
                        if started:
                            result.append("".join(current))
                            current = []
                            started = False
                        index += 1
                        continue
                    if quote is None and character == "#":
                        if not started:
                            break
                        current.append(character)
                        started = True
                        index += 1
                        continue
                    if character in {"'", '"'}:
                        if quote is None:
                            quote = character
                        elif quote == character:
                            quote = None
                        else:
                            current.append(character)
                        started = True
                        index += 1
                        continue
                    if character == "\\":
                        if index + 1 >= len(value):
                            return None
                        escape = value[index + 1]
                        if quote == "'" and escape != "'":
                            current.append(character)
                            index += 1
                            continue
                        if escape == "c" and quote is None:
                            break
                        escapes = {
                            "f": "\f",
                            "n": "\n",
                            "r": "\r",
                            "t": "\t",
                            "v": "\v",
                            "#": "#",
                            "$": "$",
                            '"': '"',
                            "'": "'",
                            "\\": "\\",
                        }
                        if escape == "_":
                            if quote == '"':
                                current.append(" ")
                                started = True
                            elif quote is None:
                                if started:
                                    result.append("".join(current))
                                    current = []
                                    started = False
                            else:
                                current.append("_")
                                started = True
                            index += 2
                            continue
                        if escape not in escapes:
                            return None
                        current.append(escapes[escape])
                        started = True
                        index += 2
                        continue
                    if character == "$" and index + 1 < len(value) and value[index + 1] == "{":
                        return None
                    current.append(character)
                    started = True
                    index += 1
                if quote is not None:
                    return None
                if started:
                    result.append("".join(current))
                return result

            def parse_chain(items: list[str]) -> ParseResult:
                if not charge(len(items)):
                    return ambiguous(items)
                if not items:
                    return no_dispatch()
                head = items[0]
                if head == "command":
                    return parse_command(items[1:])
                if head == "exec":
                    return parse_exec(items[1:])
                if head == "env":
                    return parse_env(items[1:])
                if head in {"python3", "bash"}:
                    if len(items) < 2:
                        return no_dispatch()
                    target = items[1]
                    remaining = items[2:]
                    if is_unresolved_dynamic_target(target):
                        if has_relevant_sibling(remaining):
                            return ambiguous([target, *remaining])
                        return no_dispatch()
                    path = resolved_path(target, positional)
                    if path is not None:
                        return dispatch({path})
                    return no_dispatch()
                target = head
                remaining = items[1:]
                if is_unresolved_dynamic_target(target):
                    if has_relevant_sibling(remaining):
                        return ambiguous([target, *remaining])
                    return no_dispatch()
                path = resolved_path(target, positional)
                if path is not None:
                    return dispatch({path})
                return no_dispatch()

            def parse_command(items: list[str]) -> ParseResult:
                index = 0
                query = False
                while index < len(items):
                    token = items[index]
                    if token == "--":
                        index += 1
                        break
                    if not token.startswith("-") or token == "-":
                        break
                    options = token[1:]
                    if not options or any(option not in "pVv" for option in options):
                        return ambiguous(items[index:])
                    if "v" in options or "V" in options:
                        query = True
                    index += 1
                if query:
                    return no_dispatch()
                return parse_chain(items[index:])

            def parse_exec(items: list[str]) -> ParseResult:
                index = 0
                while index < len(items):
                    token = items[index]
                    if token == "--":
                        index += 1
                        break
                    if not token.startswith("-") or token == "-":
                        break
                    options = token[1:]
                    offset = 0
                    while offset < len(options):
                        option = options[offset]
                        if option in {"c", "l"}:
                            offset += 1
                            continue
                        if option != "a":
                            return ambiguous(items[index:])
                        attached = options[offset + 1 :]
                        if attached:
                            offset = len(options)
                        else:
                            index += 1
                            if index >= len(items):
                                return ambiguous(items)
                            offset = len(options)
                    index += 1
                return parse_chain(items[index:])

            def parse_env_split(
                split_value: str,
                tail: list[str],
            ) -> ParseResult:
                split_tokens = split_env_static(split_value)
                if split_tokens is None:
                    return ambiguous([split_value, *tail])
                return parse_env([*split_tokens, *tail])

            signal_options = (
                "--block-signal",
                "--default-signal",
                "--ignore-signal",
            )

            def is_exact_signal_option(token: str) -> bool:
                return token in signal_options or any(
                    token.startswith(option + "=")
                    for option in signal_options
                )

            def is_signal_near_prefix(token: str) -> bool:
                return any(token.startswith(option) for option in signal_options)

            def parse_env(items: list[str]) -> ParseResult:
                index = 0
                while index < len(items):
                    token = items[index]
                    if token == "--":
                        index += 1
                        break
                    if token in {"--help", "--version", "-0", "--null"}:
                        return no_dispatch()
                    if token == "-":
                        index += 1
                        continue
                    if token in {
                        "--ignore-environment",
                        "--debug",
                        "--list-signal-handling",
                    }:
                        index += 1
                        continue
                    if is_exact_signal_option(token):
                        index += 1
                        continue
                    if is_signal_near_prefix(token):
                        return ambiguous(items[index:])
                    consumed_long_operand = False
                    for option in ("--unset", "--chdir", "--argv0"):
                        if token == option:
                            index += 1
                            if index >= len(items):
                                return ambiguous(items)
                            consumed_long_operand = True
                            break
                        if token.startswith(option + "="):
                            consumed_long_operand = True
                            break
                    if consumed_long_operand:
                        index += 1
                        continue
                    if token == "--split-string":
                        if index + 1 >= len(items):
                            return ambiguous(items[index:])
                        return parse_env_split(
                            items[index + 1],
                            items[index + 2 :],
                        )
                    if token.startswith("--split-string="):
                        return parse_env_split(
                            token.split("=", 1)[1],
                            items[index + 1 :],
                        )
                    if token.startswith("--"):
                        return ambiguous(items[index:])
                    if token.startswith("-") and token != "-":
                        options = token[1:]
                        offset = 0
                        while offset < len(options):
                            option = options[offset]
                            if option in {"i", "v"}:
                                offset += 1
                                continue
                            if option == "S":
                                attached = options[offset + 1 :]
                                if attached:
                                    return parse_env_split(
                                        attached,
                                        items[index + 1 :],
                                    )
                                if index + 1 >= len(items):
                                    return ambiguous(items[index:])
                                return parse_env_split(
                                    items[index + 1],
                                    items[index + 2 :],
                                )
                            if option in {"u", "C", "a"}:
                                attached = options[offset + 1 :]
                                if not attached:
                                    index += 1
                                    if index >= len(items):
                                        return ambiguous(items)
                                offset = len(options)
                                continue
                            if option == "0":
                                return no_dispatch()
                            return ambiguous(items[index:])
                        index += 1
                        continue
                    break
                while index < len(items) and "=" in items[index]:
                    index += 1
                return parse_chain(items[index:])

            return materialize(parse_chain(tokens))

        helper_names: set[str] = set()
        helper_re = re.compile(
            r"(?ms)^\s*(?:function\s+)?"
            r"(?P<name>[A-Za-z_][A-Za-z0-9_]*)"
            r"(?:\s*\(\s*\))?\s*\{(?P<body>.*?)\}"
        )
        sentinel = next(iter(sibling_entrypoints), None)
        if sentinel is not None:
            for match in helper_re.finditer(shell_source):
                if any(
                    command_sink(statement, positional=sentinel)
                    for statement in re.split(r"[;\n]", match.group("body"))
                ):
                    helper_names.add(match.group("name"))

        for statement in re.split(r"[;\n]", shell_source.replace("\\\n", " ")):
            if assignment_re.match(statement):
                continue
            dispatched.update(command_sink(statement))
            try:
                tokens = shlex.split(statement, comments=True)
            except ValueError:
                continue
            while tokens and tokens[0] in {
                "if",
                "then",
                "elif",
                "while",
                "until",
                "do",
                "!",
                "{",
                "}",
            }:
                tokens.pop(0)
            if tokens and tokens[0] in helper_names:
                for token in tokens[1:]:
                    path = resolved_path(token)
                    if path is not None:
                        dispatched.add(path)
        return dispatched

    @staticmethod
    def _repo_python_program(section: str) -> str:
        source = REPO_CONTRACT.read_text(encoding="utf-8")
        start = f"section \"{section}\"\nif ! python3 - <<'PY'; then\n"
        return source.split(start, 1)[1].split(
            "\nPY\n  failures=$((failures + 1))",
            1,
        )[0]

    @staticmethod
    def _workflow_security_program() -> str:
        module_root = ROOT / "scripts/validation"
        return (
            "import pathlib, sys\n"
            f"sys.path.insert(0, {str(module_root)!r})\n"
            "from github_workflow_contract import main\n"
            "raise SystemExit(main(['--root', str(pathlib.Path.cwd())]))\n"
        )

    @staticmethod
    def _stage00_github_program() -> str:
        return AgentGovernanceRoutingTests._repo_python_program(
            "Stage 00 GitHub routing contracts"
        )

    @staticmethod
    @contextlib.contextmanager
    def _memory_contract_fixture():
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            governance_root = ROOT / "docs/00.agent-governance"
            governance_rules = governance_root / "rules"
            governance_contracts = governance_root / "contracts"
            shutil.copytree(
                governance_root / "memory",
                root / "docs/00.agent-governance/memory",
            )
            for source in (
                governance_root / "README.md",
                governance_rules / "bootstrap.md",
                governance_rules / "agentic.md",
                governance_rules / "task-checklists.md",
                governance_rules / "stage-authoring-matrix.md",
                governance_contracts / "agent-governance-artifacts.yaml",
                governance_contracts / "agent-catalog.yaml",
                governance_contracts / "provider-models.yaml",
                ROOT
                / "docs/99.templates/templates/governance/memory.template.md",
                ROOT
                / "docs/99.templates/templates/governance/progress.template.md",
                ROOT
                / "docs/04.execution/tasks/"
                "2026-07-26-agent-governance-canonical-convergence.md",
                ROOT / "scripts/validation/agent_governance_contract.py",
            ):
                target = root / source.relative_to(ROOT)
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target)

            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            subprocess.run(
                ["git", "config", "user.email", "fixture@example.invalid"],
                cwd=root,
                check=True,
            )
            subprocess.run(
                ["git", "config", "user.name", "Fixture"],
                cwd=root,
                check=True,
            )
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            subprocess.run(
                ["git", "commit", "-qm", "fixture"],
                cwd=root,
                check=True,
            )
            head = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=root,
                capture_output=True,
                text=True,
                check=True,
            ).stdout.strip()
            current = root / "docs/00.agent-governance/memory/current.md"
            text = current.read_text(encoding="utf-8")
            text, replacements = re.subn(
                r"(?m)^- Verified commit: `[0-9a-f]{40}`$",
                f"- Verified commit: `{head}`",
                text,
            )
            if replacements != 1:
                raise AssertionError("fixture current-memory commit label missing")
            current.write_text(text, encoding="utf-8")
            yield root

    @staticmethod
    @contextlib.contextmanager
    def _workflow_fixture():
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            shutil.copytree(ROOT / ".github", root / ".github")
            for source in (
                GITHUB_GOVERNANCE,
                ARTIFACT_CONTRACT,
                GITHUB_OBSERVATION,
                ROOT / "scripts/validation/ci_gate_contract.py",
                ROOT / "scripts/validation/github_workflow_contract.py",
                ROOT / "scripts/validation/check-repo-contracts.sh",
            ):
                if not source.is_file():
                    continue
                target = root / source.relative_to(ROOT)
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target)
            yield root

    @staticmethod
    @contextlib.contextmanager
    def _script_reference_fixture(*, track_cache: bool = False):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            (root / ".gitignore").write_text("__pycache__/\n", encoding="utf-8")
            cache = root / "scripts/validation/__pycache__"
            cache.mkdir(parents=True)
            cache_file = cache / "module.cpython-312.pyc"
            cache_file.write_bytes(b"scripts/validation/missing-cache.sh")
            if track_cache:
                subprocess.run(
                    [
                        "git",
                        "add",
                        "-f",
                        "scripts/validation/__pycache__/module.cpython-312.pyc",
                    ],
                    cwd=root,
                    check=True,
                )
            yield root


if __name__ == "__main__":
    unittest.main()
