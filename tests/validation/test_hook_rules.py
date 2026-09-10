"""Executable evidence for the canonical hook rule evaluator.

The eighteen rule files declared `enabled: true` while nothing read them: no
repository reference, no rule file at any external tool's runtime location, and
two of eighteen patterns present in the shared dispatcher. `hook_rules.py` is
the reader that closes that gap, so these tests hold both halves — that the
tracked rules parse and fire, and that the evaluator refuses the shapes it must
refuse.
"""

from __future__ import annotations

import importlib.util
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest
from typing import Any

from scripts.lib.document_governance.frontmatter import parse_frontmatter_text

ROOT = pathlib.Path(__file__).resolve().parents[2]
MODULE = ROOT / "scripts/hooks/hook_rules.py"
DISPATCHER = ROOT / "scripts/hooks/agent-event-hook.sh"
RULES = ROOT / ".agents/governance/hooks"
TRACKED_RULE_COUNT = 18
EVALUATED_RULE_COUNT = 16

_spec = importlib.util.spec_from_file_location("hook_rules", MODULE)
assert _spec is not None and _spec.loader is not None
hook_rules = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = hook_rules
_spec.loader.exec_module(hook_rules)

# Assembled rather than written out, so that running this suite through a tool
# that scans its own command text does not trip the rule it is testing.
BYPASS_COMMIT = "git commit " + "--no-" + "verify" + " -m x"


def copy_dispatcher_fixture(root: pathlib.Path, *, with_rules: bool) -> None:
    hook_directory = root / "scripts/hooks"
    hook_directory.mkdir(parents=True)
    shutil.copy2(DISPATCHER, hook_directory / DISPATCHER.name)
    shutil.copy2(MODULE, hook_directory / MODULE.name)
    payload = root / "scripts/lib/hooks/tool_payload.py"
    payload.parent.mkdir(parents=True)
    shutil.copy2(ROOT / "scripts/lib/hooks/tool_payload.py", payload)
    if not with_rules:
        return
    policy_directory = root / ".agents/governance/hooks"
    policy_directory.mkdir(parents=True)
    for source in sorted(RULES.glob("hookify.*.md")):
        shutil.copy2(source, policy_directory / source.name)


def write_rule(
    directory: pathlib.Path, name: str, frontmatter: str, body: str = "message"
) -> None:
    target = directory / ".agents/governance/hooks" / f"hookify.{name}.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(f"---\n{frontmatter.strip()}\n---\n\n{body}\n", encoding="utf-8")


class TrackedRuleTests(unittest.TestCase):
    """The rules this repository actually ships."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.rules = hook_rules.load_rules(ROOT)

    def test_every_tracked_rule_parses_except_the_stop_pair(self) -> None:
        tracked = sorted(RULES.glob("hookify.*.md"))
        self.assertEqual(TRACKED_RULE_COUNT, len(tracked))
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
        self.assertEqual(EVALUATED_RULE_COUNT, len(self.rules))
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
        governance = ".agents/governance/example.md"
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

    def test_missing_policy_directory_is_an_error(self) -> None:
        with self.assertRaises(hook_rules.RuleConfigurationError):
            hook_rules.load_rules(self.root)

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
        with self.assertRaises(hook_rules.RuleConfigurationError):
            self.loaded()

    def test_unknown_field_is_refused(self) -> None:
        write_rule(
            self.root,
            "f",
            "name: f\nenabled: true\nevent: file\naction: warn\nconditions:\n"
            "  - field: author\n    operator: regex_match\n    pattern: x",
        )
        with self.assertRaises(hook_rules.RuleConfigurationError):
            self.loaded()

    def test_invalid_regex_is_refused(self) -> None:
        write_rule(
            self.root,
            "r",
            "name: r\nenabled: true\nevent: bash\npattern: (\naction: warn",
        )
        with self.assertRaises(hook_rules.RuleConfigurationError):
            self.loaded()

    def test_oversized_rule_is_an_error(self) -> None:
        write_rule(
            self.root,
            "large",
            "name: large\nenabled: true\nevent: bash\npattern: x\naction: warn",
            "x" * hook_rules.MAX_RULE_BYTES,
        )
        with self.assertRaises(hook_rules.RuleConfigurationError):
            self.loaded()

    def test_symlinked_policy_directory_is_an_error(self) -> None:
        outside = self.root / "outside"
        write_rule(
            outside,
            "ok",
            "name: ok\nenabled: true\nevent: bash\npattern: x\naction: warn",
        )
        policy_parent = self.root / ".agents/governance"
        policy_parent.mkdir(parents=True)
        (policy_parent / "hooks").symlink_to(
            outside / ".agents/governance/hooks", target_is_directory=True
        )
        with self.assertRaises(hook_rules.RuleConfigurationError):
            self.loaded()

    def test_symlinked_rule_is_an_error(self) -> None:
        outside = self.root / "outside.md"
        outside.write_text("outside", encoding="utf-8")
        policy_directory = self.root / ".agents/governance/hooks"
        policy_directory.mkdir(parents=True)
        (policy_directory / "hookify.link.md").symlink_to(outside)
        with self.assertRaises(hook_rules.RuleConfigurationError):
            self.loaded()

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

    def test_canonical_yaml_quoted_condition_key_is_loaded(self) -> None:
        write_rule(
            self.root,
            "quoted",
            "name: quoted\nenabled: true\nevent: file\naction: warn\nconditions:\n"
            '- "field": "file_path"\n  operator: "regex_match"\n  pattern: "\\\\.md$"',
        )
        self.assertEqual({"quoted"}, self.loaded())


class DispatcherTests(unittest.TestCase):
    """The rules must reach a real PreToolUse payload, not only the module."""

    def setUp(self) -> None:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = pathlib.Path(directory.name)
        copy_dispatcher_fixture(self.root, with_rules=True)

    def run_hook(self, payload: dict[str, object]) -> dict[str, Any]:
        environment = os.environ.copy()
        environment["CLAUDE_PROJECT_DIR"] = str(self.root)
        environment.pop("CODEX_PROJECT_DIR", None)
        environment.pop("HY_HOME_HOOK_PROVIDER", None)
        result = subprocess.run(
            [
                "bash",
                str(self.root / "scripts/hooks/agent-event-hook.sh"),
                "PreToolUse",
            ],
            input=json.dumps(payload),
            capture_output=True,
            text=True,
            cwd=self.root,
            env=environment,
            check=False,
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


class DispatcherFailureTests(unittest.TestCase):
    """PreToolUse must fail closed at the actual provider dispatcher boundary."""

    def setUp(self) -> None:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = pathlib.Path(directory.name)
        copy_dispatcher_fixture(self.root, with_rules=False)

    def run_hook(
        self,
        provider: str,
        payload: str | dict[str, object],
        *,
        path: str | None = None,
    ) -> subprocess.CompletedProcess[str]:
        environment = os.environ.copy()
        environment.pop("CODEX_PROJECT_DIR", None)
        environment.pop("CLAUDE_PROJECT_DIR", None)
        environment.pop("HY_HOME_HOOK_PROVIDER", None)
        if provider == "codex":
            environment["CODEX_PROJECT_DIR"] = str(self.root)
            environment["HY_HOME_HOOK_PROVIDER"] = "codex"
        else:
            environment["CLAUDE_PROJECT_DIR"] = str(self.root)
        if path is not None:
            environment["PATH"] = path
        text = payload if isinstance(payload, str) else json.dumps(payload)
        return subprocess.run(
            [
                "bash",
                str(self.root / "scripts/hooks/agent-event-hook.sh"),
                "PreToolUse",
            ],
            input=text,
            capture_output=True,
            text=True,
            cwd=self.root,
            env=environment,
            check=False,
        )

    def assert_denied(self, result: subprocess.CompletedProcess[str]) -> None:
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        output = json.loads(result.stdout)
        decision = output.get("hookSpecificOutput", {})
        self.assertEqual("deny", decision.get("permissionDecision"))

    def test_missing_policy_directory_denies_both_providers(self) -> None:
        payload = {"tool_name": "Bash", "tool_input": {"command": "git status"}}
        for provider in ("claude", "codex"):
            with self.subTest(provider=provider):
                self.assert_denied(self.run_hook(provider, payload))

    def test_invalid_policy_denies_both_providers(self) -> None:
        write_rule(
            self.root,
            "invalid",
            "name: invalid\nenabled: true\nevent: bash\npattern: (\naction: block",
        )
        payload = {"tool_name": "Bash", "tool_input": {"command": "git status"}}
        for provider in ("claude", "codex"):
            with self.subTest(provider=provider):
                self.assert_denied(self.run_hook(provider, payload))

    def test_evaluator_error_denies_both_providers(self) -> None:
        module = self.root / "scripts/hooks/hook_rules.py"
        module.write_text(
            "def load_rules(root): return ()\n"
            "def evaluate(rules, **kwargs): raise RuntimeError('fixture failure')\n",
            encoding="utf-8",
        )
        payload = {"tool_name": "Bash", "tool_input": {"command": "git status"}}
        for provider in ("claude", "codex"):
            with self.subTest(provider=provider):
                self.assert_denied(self.run_hook(provider, payload))

    def test_malformed_payload_denies_both_providers(self) -> None:
        write_rule(
            self.root,
            "ok",
            "name: ok\nenabled: true\nevent: bash\npattern: ^probe$\naction: block",
        )
        for provider in ("claude", "codex"):
            with self.subTest(provider=provider):
                self.assert_denied(self.run_hook(provider, "{"))

    def test_python_failure_exits_two_for_both_providers(self) -> None:
        binary_directory = self.root / "bin"
        binary_directory.mkdir()
        python = binary_directory / "python3"
        python.write_text("#!/usr/bin/env sh\nexit 9\n", encoding="utf-8")
        python.chmod(0o755)
        path = f"{binary_directory}:{os.environ.get('PATH', '')}"
        payload = {"tool_name": "Bash", "tool_input": {"command": "git status"}}
        for provider in ("claude", "codex"):
            with self.subTest(provider=provider):
                result = self.run_hook(provider, payload, path=path)
                self.assertEqual(2, result.returncode, result.stdout + result.stderr)

    def test_large_payload_uses_descriptor_transport_for_both_providers(self) -> None:
        write_rule(
            self.root,
            "ok",
            "name: ok\nenabled: true\nevent: bash\npattern: ^probe$\naction: block",
        )
        payload = {
            "tool_name": "Bash",
            "tool_input": {"command": "git status", "unused": "x" * 200_000},
        }
        for provider in ("claude", "codex"):
            with self.subTest(provider=provider):
                result = self.run_hook(provider, payload)
                self.assertEqual(0, result.returncode, result.stdout + result.stderr)
                self.assertEqual("", result.stdout)


if __name__ == "__main__":
    unittest.main()
