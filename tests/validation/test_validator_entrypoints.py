"""Behavioral smoke coverage for registered validation entrypoints."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[2]
PYTHON_ENTRYPOINTS = (
    "scripts/knowledge/generate-llm-wiki.py",
    "scripts/operations/provider_surface_renderer.py",
    "scripts/validation/agent_governance_contract.py",
    "scripts/validation/agent_output_eval.py",
    "scripts/validation/agentic-research-gate9-evidence.py",
    "scripts/validation/carry_owner_contract.py",
    "scripts/validation/check-agent-governance-contract.py",
    "scripts/validation/check-document-corpus-lifecycle.py",
    "scripts/validation/check-document-metadata.py",
    "scripts/validation/check-github-workflow-contract.py",
    "scripts/validation/check-old-path-gate.py",
    "scripts/validation/check-operations-catalog.py",
    "scripts/validation/check-supply-chain-policy.py",
    "scripts/validation/check-target-surface-contract.py",
    "scripts/validation/check-target-surface-delta-contract.py",
    "scripts/validation/ci_gate_contract.py",
    "scripts/validation/ci_gate_runner.py",
    "scripts/validation/gate2_claim_review_contract.py",
    "scripts/validation/github_workflow_contract.py",
    "scripts/validation/old_path_gate_contract.py",
    "scripts/validation/run-ci-gate.py",
    "scripts/validation/target_surface_contract.py",
)
SHELL_ENTRYPOINTS = (
    "scripts/hardening/check-all-hardening.sh",
    "scripts/hooks/agent-event-hook.sh",
    "scripts/hooks/post-tool-validate.sh",
    "scripts/operations/sync-provider-surfaces.sh",
    "scripts/operations/sync-tech-stack-versions.sh",
    "scripts/operations/use-qa-ci-tools.sh",
    "scripts/validation/run-agent-output-eval-fixtures.sh",
    "scripts/validation/run-agent-precommit-all-files.sh",
    "scripts/validation/run-local-qa-gates.sh",
    "scripts/validation/validate-harness.sh",
)


class ValidatorEntrypointTests(unittest.TestCase):
    def test_python_entrypoints_expose_closed_cli_help(self) -> None:
        for entrypoint in PYTHON_ENTRYPOINTS:
            with self.subTest(entrypoint=entrypoint):
                completed = subprocess.run(
                    [sys.executable, entrypoint, "--help"],
                    cwd=ROOT,
                    check=False,
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
                self.assertEqual(0, completed.returncode, completed.stderr)

    def test_ci_gate_adapter_rejects_unadmitted_commands(self) -> None:
        completed = subprocess.run(
            [sys.executable, "scripts/validation/ci_gate_adapters.py", "unadmitted"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
        self.assertEqual(2, completed.returncode, completed.stderr)

    def test_shell_entrypoints_parse_without_execution(self) -> None:
        for entrypoint in SHELL_ENTRYPOINTS:
            with self.subTest(entrypoint=entrypoint):
                completed = subprocess.run(
                    ["bash", "-n", entrypoint],
                    cwd=ROOT,
                    check=False,
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
                self.assertEqual(0, completed.returncode, completed.stderr)
