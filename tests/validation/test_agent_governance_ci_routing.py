from __future__ import annotations

import contextlib
import os
import pathlib
import re
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
    "Five focused operational-readiness unittest modules, the deterministic "
    "supply-chain policy check, and the supply-chain summary freshness check"
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
    "docs/90.references/data/governance/document-corpus-lifecycle/target-surface-convergence.yaml",
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
        self.assertIn(TARGET_CLI_COMMAND, result.stdout)
        self.assertIn(TARGET_TEST_COMMAND, result.stdout)
        local_text = LOCAL_QA.read_text(encoding="utf-8")
        self.assertIn(TARGET_CLI_COMMAND, local_text)
        self.assertIn(TARGET_TEST_COMMAND, local_text)
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
        self.assertIn(
            'target_surface_checker="scripts/validation/'
            'check-target-surface-contract.py"',
            aggregate,
        )
        self.assertIn('python3 "$target_surface_checker"', aggregate)
        local_qa = LOCAL_QA.read_text(encoding="utf-8")
        self.assertIn(TARGET_CLI_COMMAND, local_qa)
        self.assertIn(TARGET_TEST_COMMAND, local_qa)

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
        commands = [
            step.get("run")
            for step in zizmor_steps
            if isinstance(step.get("run"), str)
        ]
        self.assertEqual(
            [
                "uvx --from 'zizmor==1.28.0' "
                "zizmor . --format sarif . > results.sarif"
            ],
            [
                command
                for command in commands
                if command is not None and "zizmor" in command
            ],
        )
        self.assertNotIn(
            "zizmor==1.27.0",
            "\n".join(command for command in commands if command is not None),
            "the yanked credential-logging release must be rejected",
        )
        run_steps = [
            step
            for step in zizmor_steps
            if step.get("run")
            == (
                "uvx --from 'zizmor==1.28.0' "
                "zizmor . --format sarif . > results.sarif"
            )
        ]
        self.assertEqual(1, len(run_steps))
        self.assertNotIn(
            "env",
            run_steps[0],
            "offline zizmor must not receive a credential environment",
        )

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
            and step.get("run") == OPERATIONAL_READINESS_TEST_COMMAND
        ]
        self.assertEqual(1, len(matching))
        self.assertEqual(
            "Run focused operational readiness regressions",
            matching[0].get("name"),
        )
        contract = yaml.safe_load(
            (ROOT / ".github/workflow-contract.yml").read_text(encoding="utf-8")
        )
        command_owners = contract["expensive_commands"]
        self.assertEqual(
            1,
            sum(
                owner["job"] == "supply-chain-fixture-policy"
                and owner["command"] == OPERATIONAL_READINESS_TEST_COMMAND
                for owner in command_owners
            ),
        )
        self.assertEqual(
            1,
            len(
                re.findall(
                    r"(?m)^if ! python3 scripts/validation/"
                    r"check-github-workflow-contract\.py; then$",
                    REPO_CONTRACT.read_text(encoding="utf-8"),
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
            old = "          tests.validation.test_grype_db_seed\n"
            self.assertIn(old, text)
            workflow_path.write_text(
                text.replace(old, "", 1),
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
            "semantic owner command must occur exactly once",
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
                "run: bash scripts/validation/check-repo-contracts.sh",
                "run: bash scripts/validation/check-repo-contracts.sh '${{ github.event.pull_request.title }}'",
                "interpolates an Actions expression directly in run",
            ),
            (
                "untrusted-direct-ref",
                "run: bash scripts/validation/check-repo-contracts.sh",
                "run: bash scripts/validation/check-repo-contracts.sh '${{ github.ref }}'",
                "interpolates an Actions expression directly in run",
            ),
            (
                "zizmor-credential-env",
                (
                    "        run: uvx --from 'zizmor==1.28.0' "
                    "zizmor . --format sarif . > results.sarif"
                ),
                (
                    "        run: uvx --from 'zizmor==1.28.0' "
                    "zizmor . --format sarif . > results.sarif\n"
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
            self.subTest(label="ref-env-indirection-is-safe"),
            self._workflow_fixture() as root,
        ):
            workflow_path = root / ".github/workflows/ci-quality.yml"
            text = workflow_path.read_text(encoding="utf-8")
            old = "        run: bash scripts/validation/check-repo-contracts.sh"
            new = (
                "        env:\n"
                "          SAFE_REF: ${{ github.ref }}\n"
                '        run: bash scripts/validation/check-repo-contracts.sh "$SAFE_REF"'
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
            self.assertIn("semantic owner command must occur exactly once", result.stderr)

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
        preflight = (
            "      - name: Verify document metadata comparison base\n"
            "        if: github.event_name == 'pull_request' || "
            "github.event_name == 'push'\n"
            "        shell: bash\n"
            "        run: |\n"
            "          set -euo pipefail\n"
            '          git cat-file -e "${TEMPLATE_GATE_BASE}^{commit}"\n'
            '          git merge-base HEAD "$TEMPLATE_GATE_BASE" >/dev/null\n'
        )
        metadata = (
            "      - name: Check changed and new document metadata\n"
            "        run: python3 scripts/validation/"
            "check-document-metadata.py --mode check-changed\n"
        )
        cases = (
            (
                "event-binding",
                "github.event_name == 'push' && github.event.before || ''",
                "github.event_name == 'push' && github.sha || ''",
                "repository metadata base binding differs from the exact contract",
            ),
            (
                "preflight",
                '          git merge-base HEAD "$TEMPLATE_GATE_BASE" >/dev/null\n',
                "          true\n",
                "repository metadata preflight differs from the exact contract",
            ),
            (
                "ordering",
                preflight + (
                    "      - name: Set up Python for repository contracts\n"
                    "        uses: actions/setup-python@"
                    "5fda3b95a4ea91299a34e894583c3862153e4b97\n"
                    "        with:\n"
                    "          python-version: '3.12'\n"
                    "      - name: Install repository contract Python "
                    "dependencies\n"
                    "        run: python -m pip install -r "
                    "scripts/requirements.txt\n"
                )
                + metadata,
                metadata
                + preflight
                + (
                    "      - name: Set up Python for repository contracts\n"
                    "        uses: actions/setup-python@"
                    "5fda3b95a4ea91299a34e894583c3862153e4b97\n"
                    "        with:\n"
                    "          python-version: '3.12'\n"
                    "      - name: Install repository contract Python "
                    "dependencies\n"
                    "        run: python -m pip install -r "
                    "scripts/requirements.txt\n"
                ),
                "repository metadata steps are out of order",
            ),
        )
        program = self._stage00_github_program()
        for label, old, new, expected in cases:
            with self.subTest(label=label), self._workflow_fixture() as root:
                workflow = root / WORKFLOW.relative_to(ROOT)
                text = workflow.read_text(encoding="utf-8")
                self.assertIn(old, text)
                workflow.write_text(
                    text.replace(old, new, 1),
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
                self.assertIn(expected, result.stderr)

    def test_repo_memory_contract_rejects_exact_current_profile_mutation(
        self,
    ) -> None:
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

        repo_steps = jobs["repo-contracts"]["steps"]
        repo_commands = "\n".join(
            str(step.get("run", "")) for step in repo_steps if isinstance(step, dict)
        )
        self.assertNotIn(
            "check-agent-governance-contract.py --mode repository --section all",
            repo_commands,
        )
        self.assertIn(
            "python3 -m unittest "
            "tests.validation.test_agent_governance_ci_routing -v",
            repo_commands,
        )
        aggregate = REPO_CONTRACT.read_text(encoding="utf-8")
        self.assertRegex(
            aggregate,
            r"python3 scripts/validation/check-agent-governance-contract\.py \\\n"
            r"\s+--mode repository --section all",
        )

        eval_steps = jobs["agent-output-eval-fixture-gate"]["steps"]
        eval_commands = "\n".join(
            str(step.get("run", "")) for step in eval_steps if isinstance(step, dict)
        )
        self.assertIn(
            "run-agent-output-eval-fixtures.sh --check-fixtures --check-regressions",
            eval_commands,
        )
        self.assertIn(
            "python3 -m unittest "
            "tests.validation.test_agent_output_eval_fixtures -v",
            eval_commands,
        )
        self.assertIn("fixtures_check=pass", eval_commands)
        self.assertIn("regressions_check=pass", eval_commands)
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
        self.assertIn(
            "bash scripts/validation/run-agent-output-eval-fixtures.sh "
            "--check-fixtures --check-regressions",
            local_qa,
        )
        self.assertIn(
            "bash scripts/hardening/check-all-hardening.sh",
            local_qa,
        )
        for command in (
            "python3 -m unittest "
            "tests.validation.test_agent_governance_ci_routing -v",
            "python3 -m unittest "
            "tests.validation.test_agent_output_eval_fixtures -v",
        ):
            with self.subTest(local_owner=command):
                self.assertEqual(
                    1,
                    len(
                        re.findall(
                            rf"(?m)^  run_step .+ {re.escape(command)}$",
                            local_qa,
                        )
                    ),
                )
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
        self.assertIn(
            "- bash tests/validation/test_run_ci_precommit.sh",
            result.stdout,
        )

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
        self.assertIn("--mode repository --section all", source)

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
