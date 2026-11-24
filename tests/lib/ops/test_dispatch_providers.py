"""Provider worker adapters build installed-CLI argv and a bounded profile."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts.lib.ops import dispatch_process, dispatch_providers

SPEC = {
    "name": "claude",
    "model": "claude-haiku-5-5",
    "prompt": "write a.txt",
    "max_budget_usd": 0.25,
}


class AdapterTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        home = Path(temporary.name)
        for name in ("claude", "codex"):
            target = home / "versions" / name
            target.parent.mkdir(exist_ok=True)
            target.write_text("binary")
            (home / ".local" / "bin").mkdir(parents=True, exist_ok=True)
            (home / ".local" / "bin" / name).symlink_to(target)
        patcher = mock.patch.object(Path, "home", return_value=home)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.home = home

    def test_claude_runs_print_safe_restricted_with_a_budget_and_no_bypass(self):
        argv, profile = dispatch_providers.launch(SPEC)
        self.assertEqual(str(self.home / "versions/claude"), argv[0])
        for flag in (
            "--print",
            "--safe-mode",
            "--restricted",
            "--no-session-persistence",
        ):
            self.assertIn(flag, argv)
        self.assertEqual("0.25", argv[argv.index("--max-budget-usd") + 1])
        self.assertEqual("Read,Edit,Write,Glob,Grep", argv[argv.index("--tools") + 1])
        self.assertEqual("write a.txt", argv[-1])
        self.assertNotIn("--dangerously-skip-permissions", argv)
        self.assertTrue(profile["share_net"])
        self.assertEqual({"HOME": "/tmp/home"}, profile["env"])
        targets = {target: source for source, target in profile["binds"]}
        self.assertEqual(
            str(self.home / ".claude/.credentials.json"),
            targets["/tmp/home/.claude/.credentials.json"],
        )
        private = [s for s, _ in profile["binds"] if s.startswith(str(self.home))]
        self.assertEqual(
            {
                str(self.home / "versions/claude"),
                str(self.home / ".claude/.credentials.json"),
            },
            set(private),
        )  # nothing else of the personal HOME is visible

    def test_codex_uses_its_own_home_and_the_external_sandbox(self):
        argv, profile = dispatch_providers.launch({**SPEC, "name": "codex"})
        self.assertEqual(["exec", "--json"], argv[1:3])
        self.assertIn("--dangerously-bypass-approvals-and-sandbox", argv)
        self.assertEqual("/tmp/home/.codex", profile["env"]["CODEX_HOME"])

    def test_an_invalid_spec_is_refused_before_anything_starts(self):
        for bad in (
            {**SPEC, "name": "gemini"},
            {**SPEC, "model": " "},
            {**SPEC, "prompt": ""},
            {**SPEC, "max_budget_usd": 0},
            {**SPEC, "max_budget_usd": True},
            {**SPEC, "max_budget_usd": float("nan")},
            {**SPEC, "max_budget_usd": 6},
            {**SPEC, "extra": 1},
        ):
            with self.subTest(bad=bad):
                with self.assertRaises(dispatch_providers.ProviderError):
                    dispatch_providers.validate(bad)

    def test_the_final_json_gives_session_cost_and_error(self):
        claude = json.dumps(
            {
                "type": "result",
                "subtype": "success",
                "is_error": False,
                "session_id": "s",
                "total_cost_usd": 0.02,
                "num_turns": 3,
            }
        )
        found = dispatch_providers.result("claude", "noise\n" + claude + "\n")
        self.assertEqual(
            (False, "s", 0.02),
            (found["is_error"], found["session_id"], found["cost_usd"]),
        )
        self.assertTrue(dispatch_providers.result("claude", "no json")["is_error"])
        codex = "\n".join(
            json.dumps(event)
            for event in (
                {"type": "thread.started"},
                {"type": "turn.completed", "usage": {"input_tokens": 5}},
            )
        )
        self.assertFalse(dispatch_providers.result("codex", codex)["is_error"])
        failed = json.dumps({"type": "turn.failed"})
        self.assertTrue(dispatch_providers.result("codex", failed)["is_error"])

    def test_the_sandbox_adds_only_the_profile_to_the_bounded_boundary(self):
        budget = {
            "cpus": 1,
            "memory_bytes": 1 << 30,
            "disk_bytes": 1 << 20,
            "runtime_seconds": 60,
        }
        with tempfile.TemporaryDirectory() as tree:
            plain, _ = dispatch_process._bounded_command(
                ["x"], "t", budget, cwd=tree, env={}
            )
            _, profile = dispatch_providers.launch(SPEC)
            bounded, _ = dispatch_process._bounded_command(
                ["x"], "t", budget, cwd=tree, env={}, provider=profile
            )
        self.assertNotIn("--share-net", plain)
        self.assertIn("--share-net", bounded)
        self.assertIn("--unshare-all", bounded)
        self.assertIn("--remount-ro", bounded)
        added = [bounded[i + 1] for i, arg in enumerate(bounded) if arg == "--ro-bind"]
        self.assertIn(str(self.home / ".claude/.credentials.json"), added)
        self.assertNotIn(str(self.home), added)  # never the whole HOME


if __name__ == "__main__":
    unittest.main()
