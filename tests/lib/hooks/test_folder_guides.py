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
from scripts.lib.hooks.request_brief import BINDING_FIELDS

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

    def test_reminders_name_the_guide_on_every_edit(self) -> None:
        for _ in range(2):
            messages = folder_guides.pending_messages(
                self.root, [], self.session, edits=("infra/a.yml",), full=False
            )
            self.assertEqual(1, len(messages))
            self.assertIn("Folder guide for this edit: `infra/AGENTS.md`", messages[0])

    def claude_edit(self) -> list[str]:
        return folder_guides.pending_messages(
            self.root,
            ["infra/a.yml"],
            self.session,
            edits=("infra/a.yml",),
            full=False,
        )

    def test_claude_gets_full_text_only_when_the_shim_cannot_import(self) -> None:
        shim = self.root / "infra/CLAUDE.md"
        outside = tempfile.TemporaryDirectory()
        self.addCleanup(outside.cleanup)
        linked = Path(outside.name) / "CLAUDE.md"
        linked.write_text("@AGENTS.md\n")
        for state in ("missing", "symlink", "no-import", "shim"):
            with self.subTest(state=state):
                folder_guides.reset(self.session)
                shim.unlink(missing_ok=True)
                if state == "symlink":
                    shim.symlink_to(linked)
                elif state == "no-import":
                    shim.write_text("# infra\n")
                elif state == "shim":
                    shim.write_text(
                        "<!-- m -->\n\n# infra Folder Guide\n\n@AGENTS.md\n"
                    )
                full_text = any("infra rules" in m for m in self.claude_edit())
                self.assertEqual(state != "shim", full_text)

    def test_a_claude_read_skips_git(self) -> None:
        with mock.patch.object(folder_guides, "tracked_guides") as tracked:
            self.assertEqual(
                [],
                folder_guides.pending_messages(
                    self.root, ["infra/a.yml"], self.session, full=False
                ),
            )
        tracked.assert_not_called()

    def test_restart_message_lists_tracked_guides(self) -> None:
        message = folder_guides.restart_message(self.root)
        self.assertIn("- `infra/AGENTS.md`", message)
        self.assertNotIn("- `AGENTS.md`", message)

    def test_read_calls_count_as_targets(self) -> None:
        data = {"tool_name": "Read", "tool_input": {"file_path": "infra/a.yml"}}
        self.assertEqual(["infra/a.yml"], folder_guides.tool_targets(data, ()))
        self.assertEqual(
            ["b"], folder_guides.tool_targets({"tool_name": "Bash"}, ("b",))
        )


class DispatcherDeliveryTests(IsolatedState):
    PATCH = "*** Begin Patch\n*** Update File: {path}\n@@\n-a\n+b\n*** End Patch\n"

    def run_hook(
        self, event: str, payload: dict[str, object], *, provider: str = ""
    ) -> str:
        env = {
            "PATH": "/usr/bin:/bin",
            "CLAUDE_PROJECT_DIR": str(ROOT),
            "XDG_STATE_HOME": self.state_home,
            "HY_HOME_CAPTURE_DIR": str(Path(self.state_home) / "capture"),
        }
        if provider:
            env["HY_HOME_HOOK_PROVIDER"] = provider
        command = ["bash", str(EVENT_HOOK), event]
        if provider == "codex":
            env["CODEX_PROJECT_DIR"] = str(ROOT)
        if provider == "claude":
            adapter = {
                "UserPromptSubmit": "user-prompt-submit.sh",
                "SessionStart": "session-start.sh",
                "PreCompact": "pre-compact.sh",
                "PreToolUse": "docker-compose-pre.sh",
            }[event]
            command = ["bash", str(ROOT / ".claude/hooks" / adapter)]
        result = subprocess.run(
            command,
            input=json.dumps({"hook_event_name": event, "cwd": str(ROOT), **payload}),
            capture_output=True,
            text=True,
            cwd=ROOT,
            env=env,
            timeout=60,
            check=True,
        )
        return result.stdout

    def payload(self, session: str, **tool: object) -> dict[str, object]:
        return {"hook_event_name": "PreToolUse", "session_id": session, **tool}

    def codex_patch(self, session: str, path: str) -> dict[str, object]:
        return self.payload(
            session,
            tool_name="apply_patch",
            tool_input={"command": self.PATCH.format(path=path)},
        )

    def test_prompt_submit_supplies_a_request_revision_without_prompt_text(
        self,
    ) -> None:
        prompt = "Move one explicitly named file."
        for provider in ("claude", "codex"):
            with self.subTest(provider=provider):
                session = f"test-{uuid.uuid4().hex}"
                output = self.run_hook(
                    "UserPromptSubmit",
                    {"session_id": session, "prompt": prompt},
                    provider=provider,
                )
                context = json.loads(output)["hookSpecificOutput"]["additionalContext"]
                self.assertIn(f"request_brief status {session}", context)
                self.assertNotIn(prompt, context)
                status = self.brief_command("status", session)
                self.assertEqual(0, status.returncode, status.stderr)
                self.assertIn("request_revision", json.loads(status.stdout))

    def brief_command(
        self, *args: str, record: dict[str, object] | None = None
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["/usr/bin/python3", "-m", "scripts.lib.hooks.request_brief", *args],
            input=json.dumps(record) if record is not None else "",
            capture_output=True,
            text=True,
            cwd=ROOT,
            env={"PATH": "/usr/bin:/bin", "XDG_STATE_HOME": self.state_home},
            timeout=5,
            check=False,
        )

    def prompt(self, provider: str, session: str, text: str) -> None:
        self.run_hook(
            "UserPromptSubmit",
            {"session_id": session, "prompt": text},
            provider=provider,
        )

    def brief_record(self, session: str) -> dict[str, object]:
        status = self.brief_command("status", session)
        self.assertEqual(0, status.returncode, status.stderr)
        binding = json.loads(status.stdout)
        return {
            **{key: binding[key] for key in BINDING_FIELDS},
            "contract_version": "3.0.1",
            "brief_id": "fixture-brief",
            "revision": 1,
            "goal": "Update two named guides",
            "in_scope": ["scripts/README.md", "tests/README.md"],
            "out_of_scope": ["scripts/manifest.yaml"],
            "constraints": ["Keep changes local"],
            "acceptance_criteria": ["Check the changed guides"],
            "known_facts": [],
            "assumptions": [],
            "unresolved_questions": [],
            "risk": "low",
            "authority_ref": binding["request_ref"],
            "allowed_mutations": [
                "edit:scripts/README.md",
                "edit:tests/README.md",
                "dispatch:scripts/README.md",
            ],
            "expected_checks": ["Review the guide diff"],
            "material_inputs": {},
            "state": "ready",
        }

    def assert_edit_denied(
        self, provider: str, payload: dict[str, object], denied: bool
    ) -> None:
        output = self.run_hook("PreToolUse", payload, provider=provider)
        result = json.loads(output)["hookSpecificOutput"] if output else {}
        self.assertEqual(denied, result.get("permissionDecision") == "deny", result)
        self.assertNotEqual("allow", result.get("permissionDecision"))

    def scoped_edit(self, provider: str, session: str, path: str) -> dict[str, object]:
        if provider == "codex":
            return self.codex_patch(session, path)
        return self.payload(
            session, tool_name="Write", tool_input={"file_path": str(ROOT / path)}
        )

    def test_enrolled_edit_scope_is_checked_on_both_provider_adapters(self) -> None:
        for provider in ("claude", "codex"):
            with self.subTest(provider=provider):
                session = f"test-{uuid.uuid4().hex}"
                self.prompt(provider, session, "Update the two guides.")
                record = self.brief_record(session)
                saved = self.brief_command("bind", session, record=record)
                self.assertEqual(0, saved.returncode, saved.stderr)

                inside = self.scoped_edit(provider, session, "scripts/README.md")
                outside = self.scoped_edit(provider, session, "scripts/manifest.yaml")
                self.assert_edit_denied(provider, inside, False)
                self.assert_edit_denied(provider, outside, True)
                if provider == "codex":
                    patch = self.PATCH.format(path="scripts/manifest.yaml")
                    nested = self.payload(
                        session,
                        tool_name="exec",
                        tool_input={
                            "code": f"await tools.apply_patch({json.dumps(patch)})"
                        },
                    )
                    self.assert_edit_denied(provider, nested, True)
                else:
                    self.assert_edit_denied(
                        provider, {**inside, "agent_id": "worker"}, False
                    )
                    worker = self.scoped_edit(provider, session, "tests/README.md")
                    self.assert_edit_denied(
                        provider,
                        {**worker, "agent_id": "worker"},
                        True,
                    )
                self.prompt(provider, session, "Cancel the guide work.")
                self.assertNotEqual(
                    0, self.brief_command("bind", session, record=record).returncode
                )
                self.assert_edit_denied(provider, inside, True)

    def test_questions_and_context_changes_hold_only_prepared_work(self) -> None:
        for provider in ("claude", "codex"):
            with self.subTest(provider=provider):
                self.check_question_transitions(provider)

    def test_large_user_prompt_invalidates_an_enrolled_brief(self) -> None:
        session = f"test-{uuid.uuid4().hex}"
        self.prompt("codex", session, "Update the named guide.")
        record = self.brief_record(session)
        bound = self.brief_command("bind", session, record=record)
        self.assertEqual(0, bound.returncode, bound.stderr)
        self.prompt("codex", session, "Cancel the prior change. " + "x" * 140_000)
        current = self.brief_record(session)
        self.assertNotEqual(record["request_revision"], current["request_revision"])
        self.assert_edit_denied(
            "codex", self.codex_patch(session, "scripts/README.md"), True
        )

    def check_question_transitions(self, provider: str) -> None:
        session = f"test-{uuid.uuid4().hex}"
        self.prompt(provider, session, "Review the two guides.")
        record = {
            **self.brief_record(session),
            "state": "needs-clarification",
            "unresolved_questions": [
                {
                    "question": "Does the test guide move too?",
                    "affected_actions": ["edit:tests/README.md"],
                    "recommendation": "Keep the test guide until confirmed.",
                }
            ],
        }
        saved = self.brief_command("bind", session, record=record)
        self.assertEqual(0, saved.returncode, saved.stderr)
        affected = self.scoped_edit(provider, session, "tests/README.md")
        independent = self.scoped_edit(provider, session, "scripts/README.md")
        self.assert_edit_denied(provider, affected, True)
        self.assert_edit_denied(provider, independent, False)
        dispatch = self.brief_command(
            "check",
            session,
            "dispatch",
            record["request_revision"],
            str(record["revision"]),
            "scripts/README.md",
        )
        self.assertEqual(0, dispatch.returncode, dispatch.stderr)
        self.prompt(provider, session, "Yes, update the test guide.")
        self.assert_edit_denied(provider, affected, True)
        ready = self.brief_command("bind", session, record=self.brief_record(session))
        self.assertEqual(0, ready.returncode, ready.stderr)
        self.assert_edit_denied(provider, affected, False)
        authority_ref = self.brief_record(session)["authority_ref"]
        sequences = (
            (("PreCompact", {}), ("SessionStart", {"source": "compact"})),
            (("SessionStart", {"source": "resume"}),),
        )
        for events in sequences:
            with self.subTest(events=events):
                for event, details in events:
                    self.run_hook(
                        event, {"session_id": session, **details}, provider=provider
                    )
                    self.assert_edit_denied(provider, independent, True)
                status = self.brief_command("status", session)
                self.assertEqual(0, status.returncode, status.stderr)
                self.assertEqual(
                    authority_ref, json.loads(status.stdout).get("prior_authority_ref")
                )
                fresh = self.brief_command(
                    "bind",
                    session,
                    record={
                        **self.brief_record(session),
                        "authority_ref": authority_ref,
                    },
                )
                self.assertEqual(0, fresh.returncode, fresh.stderr)
                self.assert_edit_denied(provider, independent, False)

    def test_codex_receives_the_guide_once_and_again_after_compaction(self) -> None:
        session = f"test-{uuid.uuid4().hex}"
        payload = self.codex_patch(session, "tests/README.md")
        first = self.run_hook("PreToolUse", payload, provider="codex")
        self.assertIn("Folder guide `tests/AGENTS.md` applies", first)
        second = self.run_hook("PreToolUse", payload, provider="codex")
        self.assertNotIn("applies to files under", second)
        self.assertIn("Folder guide for this edit: `tests/AGENTS.md`", second)
        self.run_hook(
            "SessionStart",
            {"session_id": session, "source": "compact"},
            provider="codex",
        )
        third = self.run_hook("PreToolUse", payload, provider="codex")
        self.assertIn("Folder guide `tests/AGENTS.md` applies", third)

    def test_claude_gets_a_path_reminder_on_every_edit_and_no_text(self) -> None:
        session = f"test-{uuid.uuid4().hex}"
        read = self.run_hook(
            "PreToolUse",
            self.payload(
                session,
                tool_name="Read",
                tool_input={"file_path": str(ROOT / "scripts/README.md")},
            ),
        )
        self.assertNotIn("Folder guide", read)
        edit = self.payload(
            session,
            tool_name="Edit",
            tool_input={
                "file_path": "scripts/README.md",
                "old_string": "a",
                "new_string": "b",
            },
        )
        for _ in range(2):
            output = self.run_hook("PreToolUse", edit)
            self.assertIn("Folder guide for this edit: `scripts/AGENTS.md`", output)
            self.assertNotIn("applies to files under", output)

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
                provider="codex",
            )
        )
        self.assertEqual("deny", denied["hookSpecificOutput"]["permissionDecision"])
        allowed = self.run_hook(
            "PreToolUse",
            self.codex_patch(session, "docs/03.specs/README.md"),
            provider="codex",
        )
        self.assertIn("Folder guide `docs/03.specs/AGENTS.md` applies", allowed)

    def test_session_restart_asks_to_reread_the_folder_guides(self) -> None:
        for source in ("compact", "resume"):
            output = json.loads(
                self.run_hook("SessionStart", {"session_id": "s", "source": source})
            )
            context = output["hookSpecificOutput"]["additionalContext"]
            self.assertIn("re-read the nearest folder `AGENTS.md`", context)
            self.assertIn("- `infra/AGENTS.md`", context)
        startup = self.run_hook(
            "SessionStart", {"session_id": "s", "source": "startup"}
        )
        self.assertNotIn("re-read the nearest folder", startup)

    def test_hook_capture_goes_to_the_test_directory(self) -> None:
        self.run_hook("SessionStart", {"session_id": "s", "source": "startup"})
        store = Path(self.state_home) / "capture" / "capture.sqlite3"
        self.assertTrue(store.is_file())


if __name__ == "__main__":
    unittest.main()
