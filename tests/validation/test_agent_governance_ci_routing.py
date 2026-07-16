from __future__ import annotations

import contextlib
import pathlib
import re
import subprocess
import sys
import tempfile
import unittest

import yaml


ROOT = pathlib.Path(__file__).resolve().parents[2]
RECOMMENDER = ROOT / "scripts/validation/recommend-qa-gates.sh"
PRE_COMMIT = ROOT / ".pre-commit-config.yaml"
WORKFLOW = ROOT / ".github/workflows/ci-quality.yml"
CODEOWNERS = ROOT / ".github/CODEOWNERS"
LABELER = ROOT / ".github/labeler.yml"
PR_TEMPLATE = ROOT / ".github/PULL_REQUEST_TEMPLATE.md"
HARNESS_WRAPPER = ROOT / "scripts/validation/validate-harness.sh"
REPO_CONTRACT = ROOT / "scripts/validation/check-repo-contracts.sh"

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
    "scripts/validation/run-agent-output-eval-fixtures.sh",
    "tests/validation/test_agent_governance_contract.py",
    "tests/validation/test_agent_output_eval_fixtures.py",
    "tests/validation/test_provider_native_surfaces.py",
    "tests/validation/test_provider_surface_renderer.py",
)


class AgentGovernanceRoutingTests(unittest.TestCase):
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
                    "bash scripts/validation/run-agent-output-eval-fixtures.sh --check-fixtures",
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
        self.assertIn(
            "check-agent-governance-contract.py --mode repository --section all",
            repo_commands,
        )

        eval_steps = jobs["agent-output-eval-fixture-gate"]["steps"]
        eval_commands = "\n".join(
            str(step.get("run", "")) for step in eval_steps if isinstance(step, dict)
        )
        self.assertIn(
            "run-agent-output-eval-fixtures.sh --check-fixtures", eval_commands
        )
        self.assertIn("fixtures_check=pass", eval_commands)
        self.assertIn("regressions_check=pass", eval_commands)
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
            "run-agent-output-eval-fixtures.sh --check-fixtures",
            "fixtures_check=pass",
            "regressions_check=pass",
            "command, result, rollback, and skipped-check fields",
        ):
            with self.subTest(evidence=evidence):
                self.assertIn(evidence, template)

        harness = HARNESS_WRAPPER.read_text(encoding="utf-8")
        self.assertIn("run-local-qa-gates.sh --harness", harness)

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

    @staticmethod
    @contextlib.contextmanager
    def _script_reference_fixture():
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            cache = root / "scripts/validation/__pycache__"
            cache.mkdir(parents=True)
            (cache / "module.pyc").write_bytes(b"scripts/validation/missing-cache.sh")
            yield root


if __name__ == "__main__":
    unittest.main()
