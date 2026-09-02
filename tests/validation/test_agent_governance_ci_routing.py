from __future__ import annotations

import json
import os
import pathlib
import subprocess
import tempfile
import unittest

import yaml


ROOT = pathlib.Path(__file__).resolve().parents[2]
POST_TOOL = ROOT / "scripts/hooks/post-tool-validate.sh"


class AgentGovernanceCiRoutingTests(unittest.TestCase):
    def test_github_routing_uses_canonical_stage00_roots(self) -> None:
        paths = (
            ROOT / ".github/CODEOWNERS",
            ROOT / ".github/PULL_REQUEST_TEMPLATE.md",
            ROOT / ".github/labeler.yml",
        )
        text = "\n".join(path.read_text(encoding="utf-8") for path in paths)
        self.assertIn("docs/00.agent-governance/policies/", text)
        self.assertNotIn("docs/00.agent-governance/rules/", text)
        self.assertNotIn("." + "ge" + "mini", text.lower())

    def test_manifest_registers_provider_check_and_renderer(self) -> None:
        manifest = yaml.safe_load((ROOT / "scripts/manifest.yaml").read_text())
        serialized = str(manifest)
        self.assertIn("check-agent-governance-contract.py", serialized)
        self.assertIn("provider_surface_renderer.py", serialized)

    def test_repository_contract_does_not_require_removed_handoff(self) -> None:
        self.assertFalse(
            (ROOT / "scripts/validation/check-repo-contracts.sh").exists()
        )
        manifest = (ROOT / "scripts/manifest.yaml").read_text(encoding="utf-8")
        self.assertNotIn("check-repo-" + "contracts.sh", manifest)

    def test_post_tool_yaml_registry_uses_governance_parser_not_json_tool(self) -> None:
        text = (ROOT / "scripts/hooks/post-tool-validate.sh").read_text()
        self.assertNotIn(
            "python3 -m json.tool docs/00.agent-governance/providers/registry.yaml",
            text,
        )
        self.assertIn("run-ci-gate.py --profile changed", text)
        self.assertNotIn("check-agent-governance-contract.py", text)

    def test_active_workflows_route_provider_validation(self) -> None:
        workflow_text = (
            ROOT / ".github/workflows/ci-quality.yml"
        ).read_text(encoding="utf-8")
        self.assertEqual(1, workflow_text.count("run-ci-gate.py --profile changed"))
        self.assertEqual(1, workflow_text.count("run-ci-gate.py --profile full"))
        self.assertNotIn("--gate", workflow_text)

    def test_post_tool_rejects_unsafe_paths_before_any_write(self) -> None:
        cases = (
            "absolute",
            "traversal",
            "noncanonical",
            "symlink",
            "control",
            "hardlink",
        )
        for case in cases:
            with self.subTest(case=case), tempfile.TemporaryDirectory() as directory:
                base = pathlib.Path(directory)
                root = base / "repo"
                root.mkdir()
                inside = root / "inside.md"
                outside = base / "outside.md"
                inside.write_text("inside trailing space   \n", encoding="utf-8")
                outside.write_text("outside trailing space   \n", encoding="utf-8")
                if case == "absolute":
                    supplied = str(inside)
                    observed = inside
                elif case == "traversal":
                    supplied = "../outside.md"
                    observed = outside
                elif case == "noncanonical":
                    supplied = "./inside.md"
                    observed = inside
                elif case == "symlink":
                    link = root / "linked.md"
                    link.symlink_to(outside)
                    supplied = "linked.md"
                    observed = outside
                elif case == "control":
                    supplied = "inside.md\n../outside.md"
                    observed = outside
                else:
                    os.link(outside, root / "hardlinked.md")
                    supplied = "hardlinked.md"
                    observed = outside
                before = observed.read_bytes()
                result = subprocess.run(
                    ["bash", str(POST_TOOL)],
                    cwd=ROOT,
                    input=json.dumps({"tool_input": {"file_path": supplied}}),
                    capture_output=True,
                    text=True,
                    env={
                        "PATH": "/usr/bin:/bin",
                        "CODEX_PROJECT_DIR": str(root),
                    },
                    check=False,
                )
                self.assertNotEqual(0, result.returncode, result.stdout + result.stderr)
                self.assertEqual(before, observed.read_bytes())


if __name__ == "__main__":
    unittest.main()
