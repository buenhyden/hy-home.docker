"""Folder AGENTS.md delivery through the shared PreToolUse dispatcher."""

from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
import uuid
from pathlib import Path, PurePosixPath

from scripts.lib.hooks import folder_guides

ROOT = Path(__file__).resolve().parents[3]
EVENT_HOOK = ROOT / "scripts/hooks/agent-event-hook.sh"


class FolderGuideTests(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory()
        self.root = Path(self.directory.name)
        (self.root / "AGENTS.md").write_text("root shim\n")
        (self.root / "infra/04-data").mkdir(parents=True)
        (self.root / "infra/AGENTS.md").write_text("infra rules\n")
        (self.root / "docs").mkdir()
        self.session = f"test-{uuid.uuid4().hex}"
        self.addCleanup(folder_guides.reset, self.session)
        self.addCleanup(self.directory.cleanup)

    def test_nearest_guide_skips_the_root_shim(self) -> None:
        self.assertEqual(
            "infra/AGENTS.md",
            folder_guides.nearest_guide(
                self.root, PurePosixPath("infra/04-data/qdrant/compose.yml")
            ),
        )
        self.assertIsNone(
            folder_guides.nearest_guide(self.root, PurePosixPath("docs/x.md"))
        )
        self.assertIsNone(
            folder_guides.nearest_guide(self.root, PurePosixPath("README.md"))
        )

    def test_guide_is_delivered_once_per_session_until_reset(self) -> None:
        target = [str(self.root / "infra/04-data/compose.yml")]
        first = folder_guides.pending_messages(self.root, target, self.session)
        self.assertEqual(1, len(first))
        self.assertIn("`infra/AGENTS.md`", first[0])
        self.assertIn("infra rules", first[0])
        self.assertEqual(
            [], folder_guides.pending_messages(self.root, target, self.session)
        )
        folder_guides.reset(self.session)
        self.assertEqual(
            1, len(folder_guides.pending_messages(self.root, target, self.session))
        )

    def test_without_a_session_id_the_guide_is_always_delivered(self) -> None:
        target = ["infra/x.yml"]
        for _ in range(2):
            self.assertEqual(
                1, len(folder_guides.pending_messages(self.root, target, None))
            )

    def test_paths_outside_the_root_or_unsafe_are_ignored(self) -> None:
        for value in ("/etc/passwd", "../infra/x.yml", "", None, 3):
            self.assertEqual(
                [], folder_guides.pending_messages(self.root, [value], self.session)
            )

    def test_large_guides_are_truncated_with_a_pointer(self) -> None:
        (self.root / "infra/AGENTS.md").write_text(
            "x" * (folder_guides.MAX_GUIDE_BYTES + 10)
        )
        message = folder_guides.pending_messages(self.root, ["infra/a"], None)[0]
        self.assertIn("[truncated at", message)

    def test_read_calls_count_as_targets(self) -> None:
        data = {"tool_name": "Read", "tool_input": {"file_path": "infra/a.yml"}}
        self.assertEqual(["infra/a.yml"], folder_guides.tool_targets(data, ()))
        self.assertEqual(
            ["b"], folder_guides.tool_targets({"tool_name": "Bash"}, ("b",))
        )


class DispatcherDeliveryTests(unittest.TestCase):
    def run_hook(self, event: str, payload: dict[str, object]) -> str:
        result = subprocess.run(
            ["bash", str(EVENT_HOOK), event],
            input=json.dumps(payload),
            capture_output=True,
            text=True,
            cwd=ROOT,
            env={"PATH": "/usr/bin:/bin", "CLAUDE_PROJECT_DIR": str(ROOT)},
            timeout=60,
            check=True,
        )
        return result.stdout

    def test_pre_tool_use_injects_the_folder_guide_once(self) -> None:
        session = f"test-{uuid.uuid4().hex}"
        self.addCleanup(folder_guides.reset, session)
        payload = {
            "hook_event_name": "PreToolUse",
            "session_id": session,
            "tool_name": "Read",
            "tool_input": {"file_path": str(ROOT / "scripts/README.md")},
        }
        first = json.loads(self.run_hook("PreToolUse", payload))
        context = first["hookSpecificOutput"]["additionalContext"]
        self.assertIn("Folder guide `scripts/AGENTS.md`", context)
        self.assertNotIn("Folder guide", self.run_hook("PreToolUse", payload))
        self.run_hook("SessionStart", {"session_id": session, "source": "compact"})
        self.assertIn("Folder guide", self.run_hook("PreToolUse", payload))

    def test_codex_apply_patch_receives_the_folder_guide(self) -> None:
        session = f"test-{uuid.uuid4().hex}"
        self.addCleanup(folder_guides.reset, session)
        patch = (
            "*** Begin Patch\n*** Update File: tests/README.md\n@@\n-a\n+b\n"
            "*** End Patch\n"
        )
        payload = {
            "hook_event_name": "PreToolUse",
            "session_id": session,
            "tool_name": "apply_patch",
            "tool_input": {"command": patch},
        }
        output = json.loads(self.run_hook("PreToolUse", payload))
        self.assertIn(
            "Folder guide `tests/AGENTS.md`",
            output["hookSpecificOutput"]["additionalContext"],
        )


if __name__ == "__main__":
    unittest.main()
