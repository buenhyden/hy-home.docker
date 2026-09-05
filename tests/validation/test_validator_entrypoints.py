"""Behavioral smoke coverage for registered validation entrypoints."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import unittest

from tests.lib.gate.subprocess_support import gate_root_pass_fds


ROOT = Path(__file__).resolve().parents[2]
PYTHON_ENTRYPOINTS = (
    "scripts/knowledge/generate-llm-wiki.py",
    "scripts/operations/provider_surface_renderer.py",
    "scripts/lib/agent_governance/agent_governance_contract.py",
    "evals/agent_output_eval.py",
    "scripts/validation/check-agent-governance-contract.py",
    "scripts/validation/check-document-corpus-lifecycle.py",
    "scripts/validation/check-document-metadata.py",
    "scripts/validation/check-github-workflow-contract.py",
    "scripts/validation/check-operations-catalog.py",
    "scripts/validation/check-supply-chain-policy.py",
    "scripts/lib/gate/ci_gate_contract.py",
    "scripts/validation/ci_gate_runner.py",
    "scripts/lib/gate/github_workflow_contract.py",
    "scripts/validation/run-ci-gate.py",
)
SHELL_ENTRYPOINTS = (
    "scripts/hardening/check-all-hardening.sh",
    "scripts/hooks/agent-event-hook.sh",
    "scripts/hooks/post-tool-validate.sh",
    "scripts/knowledge/report-graphify-health.sh",
    "scripts/operations/check-compose-core-readiness.sh",
    "scripts/operations/gen-secrets.sh",
    "scripts/operations/rehearse-postgres-logical-upgrade.sh",
    "scripts/operations/sync-tech-stack-versions.sh",
    "scripts/operations/use-qa-ci-tools.sh",
    "evals/run-agent-output-eval-fixtures.sh",
    "scripts/validation/run-agent-precommit-all-files.sh",
    "scripts/validation/validate-docker-compose.sh",
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
                    pass_fds=gate_root_pass_fds(ROOT),
                )
                self.assertEqual(0, completed.returncode, completed.stderr)

    def test_ci_gate_adapter_rejects_unadmitted_commands(self) -> None:
        completed = subprocess.run(
            [sys.executable, "scripts/lib/gate/ci_gate_adapters.py", "unadmitted"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
            pass_fds=gate_root_pass_fds(ROOT),
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
                    pass_fds=gate_root_pass_fds(ROOT),
                )
                self.assertEqual(0, completed.returncode, completed.stderr)
