"""Executable evidence for the Stage 00 hook rule evaluator.

The nineteen rule files declared `enabled: true` while nothing read them: no
repository reference, no rule file at any external tool's runtime location, and
two of nineteen patterns present in the shared dispatcher. `hook_rules.py` is
the reader that closes that gap, so these tests hold both halves — that the
tracked rules parse and fire, and that the evaluator refuses the shapes it must
refuse.
"""

from __future__ import annotations

import importlib.util
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest
from typing import Any

from scripts.lib.document_governance.frontmatter import parse_frontmatter_text

ROOT = pathlib.Path(__file__).resolve().parents[2]
MODULE = ROOT / "scripts/hooks/hook_rules.py"
DISPATCHER = ROOT / "scripts/hooks/agent-event-hook.sh"
RULES = ROOT / "docs/00.agent-governance/policies/hooks"

_spec = importlib.util.spec_from_file_location("hook_rules", MODULE)
assert _spec is not None and _spec.loader is not None
hook_rules = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = hook_rules
_spec.loader.exec_module(hook_rules)

# Assembled rather than written out, so that running this suite through a tool
# that scans its own command text does not trip the rule it is testing.
BYPASS_COMMIT = "git commit " + "--no-" + "verify" + " -m x"


def write_rule(
    directory: pathlib.Path, name: str, frontmatter: str, body: str = "message"
) -> None:
    target = (
        directory / "docs/00.agent-governance/policies/hooks" / f"hookify.{name}.md"
    )
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(f"---\n{frontmatter.strip()}\n---\n\n{body}\n", encoding="utf-8")


class TrackedRuleTests(unittest.TestCase):
    """The rules this repository actually ships."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.rules = hook_rules.load_rules(ROOT)

    def test_every_tracked_rule_parses_except_the_stop_pair(self) -> None:
        tracked = sorted(RULES.glob("hookify.*.md"))
        stop_rules = [
            path
            for path in tracked
            if parse_frontmatter_text(path.read_text(encoding="utf-8")).get("event")
            == "stop"
        ]
        # `event: stop` is excluded on purpose: both carry `pattern: .*`, so
        # evaluating `require-logical-commits-before-stop` generically would deny
        # every stop. Their real conditions live in the dispatcher's stop gates.
        self.assertEqual(2, len(stop_rules))
        self.assertEqual(len(tracked) - len(stop_rules), len(self.rules))

    def test_no_tracked_rule_is_silently_dropped(self) -> None:
        loaded = {rule.name for rule in self.rules}
        for path in RULES.glob("hookify.*.md"):
            text = path.read_text(encoding="utf-8")
            frontmatter = parse_frontmatter_text(text)
            if frontmatter.get("event") == "stop":
                continue
            declared = str(frontmatter.get("name", ""))
            self.assertIn(declared, loaded, f"{path.name} parsed to nothing")

    def test_every_rule_carries_a_message(self) -> None:
        for rule in self.rules:
            with self.subTest(rule=rule.name):
                self.assertTrue(rule.message.strip())

    def test_bash_rules_fire_on_their_subject_and_not_otherwise(self) -> None:
        cases = (
            ("git push origin main", "block-direct-main-push", True),
            ("git push origin feat/1-x", "block-direct-main-push", False),
            (BYPASS_COMMIT, "block-git-no-verify", True),
            ("git commit -m 'feat: x'", "block-git-no-verify", False),
            ("git checkout -b wip/x", "warn-branch-naming", True),
            ("git checkout -b feat/1-x", "warn-branch-naming", False),
            ("git commit -m 'add thing'", "warn-conventional-commit", True),
            ("git commit -m 'feat: add thing'", "warn-conventional-commit", False),
            ("git push --force origin x", "warn-force-push", True),
            ("git status", "warn-force-push", False),
        )
        for command, name, expected in cases:
            with self.subTest(command=command, rule=name):
                warnings, blocks = hook_rules.evaluate(self.rules, command=command)
                fired = {rule.name for rule in warnings + blocks}
                self.assertEqual(expected, name in fired)

    def test_file_rules_require_every_condition(self) -> None:
        governance = "docs/00.agent-governance/policies/example.md"
        warnings, _ = hook_rules.evaluate(
            self.rules, edits=((governance, "한글 본문"),)
        )
        self.assertIn("warn-korean-in-governance", {rule.name for rule in warnings})

        # Same path, English body: the second condition must hold it back.
        warnings, _ = hook_rules.evaluate(
            self.rules, edits=((governance, "English body"),)
        )
        self.assertNotIn("warn-korean-in-governance", {rule.name for rule in warnings})

        # Korean body outside Stage 00: the first condition must hold it back.
        warnings, _ = hook_rules.evaluate(
            self.rules, edits=(("docs/05.operations/README.md", "한글 본문"),)
        )
        self.assertNotIn("warn-korean-in-governance", {rule.name for rule in warnings})

    def test_a_clean_payload_fires_nothing(self) -> None:
        warnings, blocks = hook_rules.evaluate(
            self.rules, command="git status", edits=(("README.md", "text"),)
        )
        self.assertEqual((), blocks)
        self.assertEqual((), warnings)


class RuleParsingTests(unittest.TestCase):
    """Shapes the evaluator must refuse, so a bad rule cannot become a silent one."""

    def setUp(self) -> None:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = pathlib.Path(directory.name)

    def loaded(self) -> set[str]:
        return {rule.name for rule in hook_rules.load_rules(self.root)}

    def test_disabled_rules_are_not_loaded(self) -> None:
        write_rule(
            self.root,
            "off",
            "name: off\nenabled: false\nevent: bash\npattern: x\naction: warn",
        )
        self.assertEqual(set(), self.loaded())

    def test_stop_rules_are_not_loaded(self) -> None:
        write_rule(
            self.root,
            "s",
            "name: s\nenabled: true\nevent: stop\npattern: .*\naction: block",
        )
        self.assertEqual(set(), self.loaded())

    def test_unknown_operator_is_refused(self) -> None:
        write_rule(
            self.root,
            "u",
            "name: u\nenabled: true\nevent: file\naction: warn\nconditions:\n"
            "  - field: file_path\n    operator: glob_match\n    pattern: x",
        )
        self.assertEqual(set(), self.loaded())

    def test_unknown_field_is_refused(self) -> None:
        write_rule(
            self.root,
            "f",
            "name: f\nenabled: true\nevent: file\naction: warn\nconditions:\n"
            "  - field: author\n    operator: regex_match\n    pattern: x",
        )
        self.assertEqual(set(), self.loaded())

    def test_invalid_regex_is_refused(self) -> None:
        write_rule(
            self.root,
            "r",
            "name: r\nenabled: true\nevent: bash\npattern: (\naction: warn",
        )
        self.assertEqual(set(), self.loaded())

    def test_a_valid_rule_in_a_fixture_root_is_loaded(self) -> None:
        write_rule(
            self.root,
            "ok",
            "name: ok\nenabled: true\nevent: bash\npattern: ^probe$\naction: block",
        )
        self.assertEqual({"ok"}, self.loaded())
        rules = hook_rules.load_rules(self.root)
        _, blocks = hook_rules.evaluate(rules, command="probe")
        self.assertEqual(("ok",), tuple(rule.name for rule in blocks))


class DispatcherTests(unittest.TestCase):
    """The rules must reach a real PreToolUse payload, not only the module."""

    def run_hook(self, payload: dict[str, object]) -> dict[str, Any]:
        result = subprocess.run(
            ["bash", str(DISPATCHER), "PreToolUse"],
            input=json.dumps(payload),
            capture_output=True,
            text=True,
            cwd=ROOT,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        return json.loads(result.stdout) if result.stdout.strip() else {}

    def test_a_blocking_rule_denies_the_call(self) -> None:
        output = self.run_hook(
            {"tool_name": "Bash", "tool_input": {"command": "git push origin main"}}
        )
        decision = output.get("hookSpecificOutput", {})
        self.assertEqual("deny", decision.get("permissionDecision"))
        self.assertIn("main", decision.get("permissionDecisionReason", ""))

    def test_a_warning_rule_reaches_the_system_message(self) -> None:
        output = self.run_hook(
            {"tool_name": "Bash", "tool_input": {"command": "git checkout -b wip/x"}}
        )
        self.assertNotIn("permissionDecision", output.get("hookSpecificOutput", {}))
        self.assertIn("Branch naming", output.get("systemMessage", ""))

    def test_a_clean_command_is_allowed_without_a_message(self) -> None:
        output = self.run_hook(
            {"tool_name": "Bash", "tool_input": {"command": "git status"}}
        )
        self.assertNotIn("permissionDecision", output.get("hookSpecificOutput", {}))
        self.assertNotIn("systemMessage", output)


if __name__ == "__main__":
    unittest.main()
