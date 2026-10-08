"""Behavioral smoke coverage for registered validation entrypoints."""

from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tomllib
import unittest
from pathlib import Path

from tests.lib.gate.subprocess_support import gate_root_pass_fds

ROOT = Path(__file__).resolve().parents[2]
PYTHON_ENTRYPOINTS = (
    "scripts/operations/provider_surface_renderer.py",
    "scripts/lib/agent_governance/agent_governance_contract.py",
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

    def test_agent_descriptions_carry_role_routing_text(self) -> None:
        for role in sorted((ROOT / ".agents/roles").glob("*.md")):
            with self.subTest(role=role.stem):
                source = role.read_text(encoding="utf-8")
                overview = source.split("## Overview\n\n", 1)[1].split("\n\n", 1)[0]
                use_when = source.split("### Use When\n\n", 1)[1].split("\n\n", 1)[0]
                claude = (ROOT / ".claude/agents" / role.name).read_text(
                    encoding="utf-8"
                )
                codex = (ROOT / ".codex/agents" / f"{role.stem}.toml").read_text(
                    encoding="utf-8"
                )
                descriptions = (
                    json.loads(claude.split("\ndescription: ", 1)[1].split("\n", 1)[0]),
                    tomllib.loads(codex)["description"],
                )
                for description in descriptions:
                    self.assertIn(" ".join(overview.split()), description)
                    for case in use_when.split("\n- "):
                        case = " ".join(case.removeprefix("- ").split()).rstrip(".")
                        self.assertIn(case, description)

    def test_agent_description_keeps_wrapped_use_when_bullets(self) -> None:
        from scripts.operations import provider_surface_renderer as renderer

        text = (
            "# r\n\n## Overview\n\nDo the work.\n\n### Use When\n\n"
            "- First case wraps\n  onto a second line.\n- Second case.\n\n## Next\n"
        )
        role = renderer.RoleRecord(
            agent_id="r",
            scope="common",
            tier="worker",
            work_profile="adversarial-review",
            permission_profile="read-only",
            tool_profile="inspection",
            skill_ids=(),
            source_path=pathlib.PurePosixPath(".agents/roles/r.md"),
            source_text=text,
        )
        self.assertEqual(
            "Do the work. Use when: First case wraps onto a second line; Second case.",
            renderer._description(role),
        )

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
