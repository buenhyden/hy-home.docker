"""Folder AGENTS.md delivery through the shared PreToolUse dispatcher."""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
import uuid
from pathlib import Path, PurePosixPath
from unittest import mock

from scripts.lib.hooks import folder_guides

ROOT = Path(__file__).resolve().parents[3]
EVENT_HOOK = ROOT / "scripts/hooks/agent-event-hook.sh"


class IsolatedState(unittest.TestCase):
    """Keep delivery records in a throwaway XDG_STATE_HOME."""

    def setUp(self) -> None:
        state = tempfile.TemporaryDirectory()
        self.addCleanup(state.cleanup)
        self.state_home = state.name
        patcher = mock.patch.dict(os.environ, {"XDG_STATE_HOME": state.name})
        patcher.start()
        self.addCleanup(patcher.stop)


class FolderGuideTests(IsolatedState):
    def setUp(self) -> None:
        super().setUp()
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name).resolve()
        (self.root / "AGENTS.md").write_text("root shim\n")
        (self.root / "infra/04-data").mkdir(parents=True)
        (self.root / "infra/AGENTS.md").write_text("infra rules\n")
        (self.root / "docs").mkdir()
        self.git("init", "-q")
        self.git("add", "AGENTS.md", "infra/AGENTS.md")
        self.session = f"test-{uuid.uuid4().hex}"

    def git(self, *args: str) -> None:
        subprocess.run(["git", "-C", str(self.root), *args], check=True)

    def deliver(self, *targets: object, session: object = None) -> list[str]:
        return folder_guides.pending_messages(self.root, list(targets), session)

    def test_nearest_tracked_guide_skips_the_root_shim(self) -> None:
        tracked = folder_guides.tracked_guides(self.root)
        self.assertEqual(frozenset({"infra/AGENTS.md"}), tracked)
        self.assertEqual(
            "infra/AGENTS.md",
            folder_guides.nearest_guide(
                self.root, PurePosixPath("infra/04-data/qdrant/compose.yml"), tracked
            ),
        )
        for target in ("docs/x.md", "README.md"):
            self.assertIsNone(
                folder_guides.nearest_guide(self.root, PurePosixPath(target), tracked)
            )

    def test_guide_is_delivered_once_per_session_until_reset(self) -> None:
        target = str(self.root / "infra/04-data/compose.yml")
        first = self.deliver(target, session=self.session)
        self.assertEqual(1, len(first))
        self.assertIn("`infra/AGENTS.md`", first[0])
        self.assertIn("infra rules", first[0])
        self.assertEqual([], self.deliver(target, session=self.session))
        folder_guides.reset(self.session)
        self.assertEqual(1, len(self.deliver(target, session=self.session)))

    def test_a_subagent_keeps_its_own_record(self) -> None:
        parent = folder_guides.session_key({"session_id": self.session})
        child = folder_guides.session_key(
            {"session_id": self.session, "agent_id": "a1b2"}
        )
        self.assertNotEqual(parent, child)
        self.assertEqual(1, len(self.deliver("infra/a", session=parent)))
        self.assertEqual(1, len(self.deliver("infra/a", session=child)))

    def test_without_a_session_id_the_guide_is_always_delivered(self) -> None:
        for _ in range(2):
            self.assertEqual(1, len(self.deliver("infra/x.yml")))

    def test_untracked_or_ignored_guides_are_not_delivered(self) -> None:
        (self.root / "docs/AGENTS.md").write_text("vendored text\n")
        self.assertEqual([], self.deliver("docs/x.md", session=self.session))

    def test_symlinked_guides_or_parents_are_not_delivered(self) -> None:
        outside = tempfile.TemporaryDirectory()
        self.addCleanup(outside.cleanup)
        (Path(outside.name) / "AGENTS.md").write_text("outside\n")
        (self.root / "linked").symlink_to(outside.name)
        (self.root / "lab").mkdir()
        (self.root / "lab/AGENTS.md").symlink_to(Path(outside.name) / "AGENTS.md")
        self.git("add", "linked", "lab/AGENTS.md")
        self.assertEqual([], self.deliver("linked/x.yml", session=self.session))
        self.assertEqual([], self.deliver("lab/x.yml", session=self.session))

    def test_a_missing_tracked_guide_falls_back_to_an_ancestor(self) -> None:
        (self.root / "infra/04-data/AGENTS.md").write_text("data rules\n")
        self.git("add", "infra/04-data/AGENTS.md")
        (self.root / "infra/04-data/AGENTS.md").unlink()
        message = self.deliver("infra/04-data/x.yml")[0]
        self.assertIn("`infra/AGENTS.md`", message)

    def test_old_records_are_pruned(self) -> None:
        self.deliver("infra/a", session=self.session)
        record = folder_guides._state_file(self.session)
        os.utime(record, (0, 0))
        folder_guides._state_directory()
        self.assertFalse(record.exists())

    def test_paths_outside_the_root_or_unsafe_are_ignored(self) -> None:
        for value in ("/etc/passwd", "../infra/x.yml", "", None, 3):
            self.assertEqual([], self.deliver(value, session=self.session))

    def test_large_guides_are_truncated_with_a_pointer(self) -> None:
        (self.root / "infra/AGENTS.md").write_text(
            "x" * (folder_guides.MAX_GUIDE_BYTES + 10)
        )
        self.assertIn("[truncated at", self.deliver("infra/a")[0])

    def test_an_unreadable_guide_is_not_marked_delivered(self) -> None:
        with mock.patch.object(folder_guides, "_message", side_effect=OSError):
            with self.assertRaises(OSError):
                self.deliver("infra/a", session=self.session)
        self.assertEqual(1, len(self.deliver("infra/a", session=self.session)))

    def test_read_calls_count_as_targets(self) -> None:
        data = {"tool_name": "Read", "tool_input": {"file_path": "infra/a.yml"}}
        self.assertEqual(["infra/a.yml"], folder_guides.tool_targets(data, ()))
        self.assertEqual(
            ["b"], folder_guides.tool_targets({"tool_name": "Bash"}, ("b",))
        )


class DispatcherDeliveryTests(IsolatedState):
    def run_hook(self, event: str, payload: dict[str, object]) -> str:
        result = subprocess.run(
            ["bash", str(EVENT_HOOK), event],
            input=json.dumps(payload),
            capture_output=True,
            text=True,
            cwd=ROOT,
            env={
                "PATH": "/usr/bin:/bin",
                "CLAUDE_PROJECT_DIR": str(ROOT),
                "XDG_STATE_HOME": self.state_home,
            },
            timeout=60,
            check=True,
        )
        return result.stdout

    def payload(self, session: str, **tool: object) -> dict[str, object]:
        return {"hook_event_name": "PreToolUse", "session_id": session, **tool}

    def test_pre_tool_use_injects_the_folder_guide_once(self) -> None:
        session = f"test-{uuid.uuid4().hex}"
        payload = self.payload(
            session,
            tool_name="Read",
            tool_input={"file_path": str(ROOT / "scripts/README.md")},
        )
        first = json.loads(self.run_hook("PreToolUse", payload))
        context = first["hookSpecificOutput"]["additionalContext"]
        self.assertIn("Folder guide `scripts/AGENTS.md`", context)
        self.assertNotIn("Folder guide", self.run_hook("PreToolUse", payload))
        self.run_hook("SessionStart", {"session_id": session, "source": "compact"})
        self.assertIn("Folder guide", self.run_hook("PreToolUse", payload))

    def test_a_denied_call_does_not_consume_the_guide(self) -> None:
        session = f"test-{uuid.uuid4().hex}"
        denied = json.loads(
            self.run_hook(
                "PreToolUse",
                self.payload(
                    session,
                    tool_name="Write",
                    tool_input={
                        "file_path": "docs/03.specs/README.md",
                        "content": "[x](file:///etc/hosts)\n",
                    },
                ),
            )
        )
        self.assertEqual("deny", denied["hookSpecificOutput"]["permissionDecision"])
        allowed = self.run_hook(
            "PreToolUse",
            self.payload(
                session,
                tool_name="Read",
                tool_input={"file_path": str(ROOT / "docs/03.specs/README.md")},
            ),
        )
        self.assertIn("Folder guide `docs/03.specs/AGENTS.md`", allowed)

    def test_codex_apply_patch_receives_the_folder_guide(self) -> None:
        patch = (
            "*** Begin Patch\n*** Update File: tests/README.md\n@@\n-a\n+b\n"
            "*** End Patch\n"
        )
        output = json.loads(
            self.run_hook(
                "PreToolUse",
                self.payload(
                    f"test-{uuid.uuid4().hex}",
                    tool_name="apply_patch",
                    tool_input={"command": patch},
                ),
            )
        )
        self.assertIn(
            "Folder guide `tests/AGENTS.md`",
            output["hookSpecificOutput"]["additionalContext"],
        )


if __name__ == "__main__":
    unittest.main()
