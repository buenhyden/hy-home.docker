from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

from tests.validation.test_hook_rules import copy_dispatcher_fixture

ROOT = Path(__file__).resolve().parents[2]


class NativeHookRoutingTests(unittest.TestCase):
    def setUp(self) -> None:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        copy_dispatcher_fixture(self.root, with_rules=True)
        subprocess.run(["git", "init", "-q"], cwd=self.root, check=True)

    def run_hook(self, payload: dict, *, post: bool = False):
        command = (
            ["bash", str(ROOT / "scripts/hooks/post-tool-validate.sh"), "--check"]
            if post
            else [
                "bash",
                str(self.root / "scripts/hooks/agent-event-hook.sh"),
                "PreToolUse",
            ]
        )
        return subprocess.run(
            command,
            cwd=self.root,
            input=json.dumps(payload),
            text=True,
            capture_output=True,
            check=False,
            env={"PATH": os.defpath, "CODEX_PROJECT_DIR": str(self.root)},
        )

    def test_native_patch_reaches_governance_and_secret_file_rules(self) -> None:
        for path, replacement, denied in (
            (".agents/knowledge/example.md", "Example", False),
            ("compose.yml", "POSTGRES_PASSWORD: fixture-only-value", True),
            (
                "compose\u2028*** Update File: ordinary.yml",
                "POSTGRES_PASSWORD: fixture-only-value",
                True,
            ),
        ):
            with self.subTest(path=path):
                result = self.run_hook(
                    {
                        "tool_name": "apply_patch",
                        "tool_input": {
                            "command": f"*** Begin Patch\n*** Add File: {path}\n+{replacement}\n*** End Patch"
                        },
                    }
                )
                self.assertEqual(0, result.returncode, result.stderr)
                output = json.loads(result.stdout)
                if denied:
                    self.assertEqual(
                        "deny", output["hookSpecificOutput"]["permissionDecision"]
                    )
                else:
                    self.assertIn(
                        "Canonical agent governance edit", output["systemMessage"]
                    )

    def test_native_absolute_post_checks_content_without_rewriting(self) -> None:
        target = self.root / "broken.json"
        target.write_text("{broken   \n")
        result = self.run_hook(
            {
                "tool_name": "Edit",
                "tool_input": {"file_path": str(target), "new_string": "{broken"},
            },
            post=True,
        )
        self.assertNotEqual(0, result.returncode)
        self.assertIn("Expecting property name", result.stderr)
        self.assertEqual("{broken   \n", target.read_text())

    def test_multifile_patch_checks_second_target_and_empty_patch_fails(self) -> None:
        (self.root / "valid.json").write_text("{}\n")
        (self.root / "broken.json").write_text("{broken\n")
        patch = "*** Begin Patch\n*** Update File: valid.json\n@@\n+{}\n*** Update File: broken.json\n@@\n+{broken\n*** End Patch"
        result = self.run_hook(
            {"tool_name": "apply_patch", "tool_input": {"command": patch}}, post=True
        )
        self.assertNotEqual(0, result.returncode)
        self.assertIn("Expecting property name", result.stderr)
        for post in (False, True):
            with self.subTest(post=post):
                result = self.run_hook(
                    {"tool_name": "apply_patch", "tool_input": {}}, post=post
                )
                if post:
                    self.assertNotEqual(0, result.returncode)
                else:
                    self.assertEqual(
                        "deny",
                        json.loads(result.stdout)["hookSpecificOutput"][
                            "permissionDecision"
                        ],
                    )

    def test_native_config_has_no_arbitrary_git_or_python_grants(self) -> None:
        allow = json.loads((ROOT / ".claude/settings.json").read_text())["permissions"][
            "allow"
        ]
        self.assertNotIn("Bash(git:*)", allow)
        self.assertNotIn("Bash(python3:*)", allow)
        self.assertIn(
            "Bash(python3 scripts/validation/run-ci-gate.py --profile changed:*)", allow
        )

    def test_mixed_valid_invalid_targets_are_denied_before_tool_use(self) -> None:
        result = self.run_hook(
            {
                "tool_name": "MultiEdit",
                "tool_input": {
                    "edits": [
                        {"file_path": "safe", "new_string": "ok"},
                        {"file_path": 42},
                    ]
                },
            }
        )
        self.assertEqual(
            "deny",
            json.loads(result.stdout)["hookSpecificOutput"]["permissionDecision"],
        )
