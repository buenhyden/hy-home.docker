"""Request brief consistency using real isolated Git and private state."""

from __future__ import annotations

import fcntl
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts.lib.hooks import request_brief

SOURCE_ROOT = Path(__file__).resolve().parents[3]


class RequestBriefTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        base = Path(temporary.name).resolve()
        self.root = base / "repo"
        self.root.mkdir()
        self.state_home = base / "state"
        patch = mock.patch.dict(os.environ, {"XDG_STATE_HOME": str(self.state_home)})
        patch.start()
        self.addCleanup(patch.stop)
        (self.root / "policy.md").write_text("Synthetic input\n", encoding="utf-8")
        self.git("init", "-q")
        self.git("add", "policy.md")
        self.git("commit", "-qm", "test: Establish brief fixture")
        self.event = {
            "hook_event_name": "UserPromptSubmit",
            "session_id": "session-a",
            "cwd": str(self.root),
            "prompt": "Prepare the synthetic change",
        }

    def git(self, *arguments: str) -> None:
        subprocess.run(
            [
                "git",
                "-c",
                "user.name=Fixture",
                "-c",
                "user.email=fixture@example.invalid",
                *arguments,
            ],
            cwd=self.root,
            check=True,
            capture_output=True,
        )

    def cli(
        self, command: str, *arguments: str, payload: object | None = None
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                "-m",
                "scripts.lib.hooks.request_brief",
                command,
                self.event["session_id"],
                *arguments,
            ],
            cwd=self.root,
            env={**os.environ, "PYTHONPATH": str(SOURCE_ROOT)},
            input=json.dumps(payload) if payload is not None else "",
            capture_output=True,
            text=True,
            check=False,
            timeout=5,
        )

    def current(self) -> dict[str, str]:
        result = self.cli("status")
        self.assertEqual(0, result.returncode, result.stderr)
        return json.loads(result.stdout)

    def record(self, **changes: object) -> dict:
        status = self.current()
        observed = {key: status[key] for key in request_brief.BINDING_FIELDS}
        return {
            "contract_version": "3.0.1",
            "brief_id": "fixture-brief",
            "revision": 1,
            **observed,
            "goal": "Prepare a synthetic source change",
            "in_scope": ["example.txt", "second.txt"],
            "out_of_scope": ["live systems"],
            "constraints": [],
            "acceptance_criteria": ["The fixture stays within the requested paths"],
            "known_facts": [],
            "assumptions": [],
            "unresolved_questions": [],
            "risk": "low",
            "authority_ref": observed["request_ref"],
            "allowed_mutations": [
                "edit:example.txt",
                "edit:second.txt",
                "dispatch:second.txt",
            ],
            "expected_checks": ["Focused synthetic check"],
            "material_inputs": {},
            "state": "ready",
            **changes,
        }

    def guard(self, *paths: str, agent_id: str | None = None) -> str | None:
        return request_brief.guard_edits(
            self.root,
            {
                **self.event,
                "hook_event_name": "PreToolUse",
                **({"agent_id": agent_id} if agent_id is not None else {}),
            },
            paths,
        )

    def enroll(self, **changes: object) -> dict:
        self.assertIn("session-a", request_brief.observe_request(self.root, self.event))
        brief = self.record(**changes)
        result = self.cli("bind", payload=brief)
        self.assertEqual(0, result.returncode, result.stderr)
        return brief

    def test_clear_brief_checks_exact_paths_and_dispatch_scope(self) -> None:
        self.assertIsNone(self.guard("unrelated.txt"))
        self.enroll()
        self.assertEqual(
            {
                "request_ref",
                "request_digest",
                "request_revision",
                "workspace_id",
                "baseline_id",
            },
            self.current().keys(),
        )
        self.assertIsNone(self.guard("example.txt"))
        self.assertIsNone(self.guard(str(self.root / "example.txt")))
        self.assertIsNone(self.guard())
        self.assertIsNotNone(self.guard("example.txt", "unrelated.txt"))
        self.assertIsNotNone(self.guard("example.txt", agent_id="worker-a"))
        self.assertEqual(0, self.cli("check", "dispatch", "second.txt").returncode)
        self.assertNotEqual(0, self.cli("check", "dispatch", "example.txt").returncode)
        self.assertFalse((self.root / "second.txt").exists())

    def test_correction_rejects_stale_reply_even_when_prompt_text_repeats(self) -> None:
        former = self.enroll()
        request_brief.observe_request(self.root, self.event)
        current = self.current()
        self.assertEqual(former["request_digest"], current["request_digest"])
        self.assertNotEqual(former["request_revision"], current["request_revision"])
        self.assertIsNotNone(self.guard("example.txt"))
        reply = self.cli("bind", payload=former)
        self.assertNotEqual(0, reply.returncode)
        self.assertIsNotNone(self.guard("example.txt"))
        self.assertEqual(0, self.cli("bind", payload=self.record()).returncode)
        self.assertIsNone(self.guard("example.txt"))

    def test_resume_and_compact_require_a_fresh_bind(self) -> None:
        previous = self.enroll()
        for source in ("resume", "compact"):
            with self.subTest(source=source):
                request_brief.invalidate_request(
                    self.root,
                    {**self.event, "hook_event_name": "SessionStart", "source": source},
                )
                self.assertIsNotNone(self.guard("example.txt"))
                self.assertNotEqual(0, self.cli("bind", payload=previous).returncode)
                previous = self.record()
                self.assertEqual(0, self.cli("bind", payload=previous).returncode)

    def test_questions_hold_only_their_affected_actions(self) -> None:
        self.enroll(
            state="needs-clarification",
            unresolved_questions=[
                {
                    "question": "Who may receive the handoff?",
                    "affected_actions": ["edit:second.txt"],
                    "recommendation": "Hold that dispatch",
                }
            ],
        )
        self.assertIsNone(self.guard("example.txt"))
        self.assertNotEqual(0, self.cli("check", "dispatch", "second.txt").returncode)
        request_brief.observe_request(
            self.root, {**self.event, "prompt": "Use the fixture recipient"}
        )
        self.assertEqual(0, self.cli("bind", payload=self.record()).returncode)
        self.assertEqual(0, self.cli("check", "dispatch", "second.txt").returncode)

    def test_material_input_and_git_baseline_movement_block_edits(self) -> None:
        input_path = self.root / "policy.md"
        digest = hashlib.sha256(input_path.read_bytes()).hexdigest()
        self.enroll(material_inputs={"policy.md": digest})
        self.assertIsNone(self.guard("example.txt"))
        input_path.unlink()
        self.assertIsNotNone(self.guard("example.txt"))
        input_path.write_text("Changed synthetic input\n", encoding="utf-8")
        self.assertIsNotNone(self.guard("example.txt"))
        self.git("add", "policy.md")
        self.git("commit", "-qm", "test: Change exact input")
        self.assertIsNotNone(self.guard("example.txt"))
        check = self.cli("check", "dispatch", "second.txt")
        self.assertNotEqual(0, check.returncode)

    def test_invalid_metadata_or_scope_cannot_enroll(self) -> None:
        request_brief.observe_request(self.root, self.event)
        for changes in (
            {"authority_ref": ""},
            {"authority_ref": True},
            {"revision": True},
            {"allowed_mutations": ["edit:../outside"]},
            {"allowed_mutations": ["edit:unrelated.txt"]},
            {"acceptance_criteria": []},
            {"unexpected": "field"},
        ):
            with self.subTest(changes=changes):
                self.assertNotEqual(
                    0, self.cli("bind", payload=self.record(**changes)).returncode
                )
        self.assertIsNone(self.guard("unrelated.txt"))

    def test_uncorroborated_authority_is_recordable_without_permitting_actions(
        self,
    ) -> None:
        for authority in (
            None,
            "draft:approval-true",
            "memory:approved-once",
            "external:opaque",
        ):
            with self.subTest(authority=authority):
                self.enroll(authority_ref=authority)
                self.assertIsNotNone(self.guard("example.txt"))
                result = self.cli("check", "dispatch", "second.txt")
                self.assertNotEqual(0, result.returncode)
                self.assertIn("no locally corroborated native request", result.stderr)

    def test_state_contains_no_prompt_or_brief_prose_and_missing_state_denies(
        self,
    ) -> None:
        brief = self.enroll()
        states = list(self.state_home.rglob("*.json"))
        self.assertEqual(1, len(states))
        payload = states[0].read_text(encoding="utf-8")
        self.assertNotIn(self.event["prompt"], payload)
        self.assertNotIn(brief["goal"], payload)
        states[0].unlink()
        self.assertIsNotNone(self.guard("example.txt"))
        (lock,) = self.state_home.rglob("*.lock")
        lock.unlink()
        self.assertIsNotNone(self.guard("example.txt"))
        request_brief.observe_request(self.root, self.event)
        self.assertIsNotNone(self.guard("example.txt"))

    def test_enrolled_child_edits_need_both_edit_and_dispatch_scope(self) -> None:
        self.enroll(allowed_mutations=["edit:example.txt", "dispatch:example.txt"])
        self.assertIsNone(self.guard("example.txt", agent_id="worker-a"))

    def test_blocked_observation_cannot_leave_an_old_binding_active(self) -> None:
        before = self.enroll()
        (lock_path,) = self.state_home.rglob("*.lock")
        with lock_path.open("r+b") as handle:
            fcntl.flock(handle, fcntl.LOCK_EX)
            self.assertEqual("", request_brief.observe_request(self.root, self.event))
        self.assertIsNotNone(self.guard("example.txt"))
        self.assertNotEqual(0, self.cli("bind", payload=before).returncode)
        self.assertNotEqual(0, self.cli("status").returncode)
        request_brief.invalidate_request(self.root, {**self.event, "source": "resume"})
        self.assertNotEqual(0, self.cli("status").returncode)
        self.assertIsNotNone(self.guard("example.txt"))
        self.enroll()
        self.assertNotIn("prior_authority_ref", self.current())
        replay = self.record(revision=2, authority_ref=before["authority_ref"])
        self.assertEqual(0, self.cli("bind", payload=replay).returncode)
        self.assertIsNotNone(self.guard("example.txt"))

    def test_prior_scope_reuse_requires_the_previous_material_inputs(self) -> None:
        digest = hashlib.sha256((self.root / "policy.md").read_bytes()).hexdigest()
        inputs = {"policy.md": digest}
        extra = self.root / "extra.md"
        extra.write_bytes(b"Newly material fixture\n")
        self.git("add", "extra.md")
        self.git("commit", "-qm", "test: Track the second material fixture")
        original = self.enroll(material_inputs=inputs)
        request_brief.observe_request(self.root, {**self.event, "prompt": "Status?"})
        reference = original["authority_ref"]
        self.assertNotEqual(
            0, self.cli("bind", payload=self.record(authority_ref=reference)).returncode
        )
        added_input = self.record(
            authority_ref=reference,
            material_inputs={
                **inputs,
                "extra.md": hashlib.sha256(extra.read_bytes()).hexdigest(),
            },
        )
        self.assertNotEqual(0, self.cli("bind", payload=added_input).returncode)
        same_inputs = self.record(authority_ref=reference, material_inputs=inputs)
        self.assertEqual(0, self.cli("bind", payload=same_inputs).returncode)
        self.assertIsNone(self.guard("example.txt"))

    def test_bind_rejects_untracked_inputs_before_opening_them(self) -> None:
        (self.root / ".env").write_text("synthetic unavailable material\n")
        request_brief.observe_request(self.root, self.event)
        refusal = self.cli(
            "bind", payload=self.record(material_inputs={".env": "0" * 64})
        )
        self.assertNotEqual(0, refusal.returncode)
        self.assertIn("tracked regular files", refusal.stderr)
        self.assertNotIn("synthetic unavailable material", refusal.stderr)

    def test_material_git_queries_disable_repository_fsmonitor(self) -> None:
        with mock.patch.object(request_brief.subprocess, "run") as run:
            request_brief._git(self.root, "ls-files", "--stage", "--", "policy.md")
        (command,) = run.call_args.args
        self.assertEqual(
            ["git", "-c", "core.fsmonitor=false", "--literal-pathspecs"],
            command[:4],
        )
        self.assertEqual("0", run.call_args.kwargs["env"]["GIT_OPTIONAL_LOCKS"])

    def test_withdrawal_survives_compaction_until_new_request(self) -> None:
        old = self.enroll(state="withdrawn", allowed_mutations=[])
        self.assertIsNotNone(self.guard("example.txt"))
        request_brief.invalidate_request(self.root, {**self.event, "source": "compact"})
        self.assertNotEqual(0, self.cli("status").returncode)
        self.assertIsNotNone(self.guard("example.txt"))
        self.enroll()
        self.assertNotIn("prior_authority_ref", self.current())
        replay = self.record(revision=2, authority_ref=old["authority_ref"])
        self.assertEqual(0, self.cli("bind", payload=replay).returncode)
        self.assertIsNotNone(self.guard("example.txt"))

    def test_prior_authority_rebind_does_not_expand_it_or_auto_bind(self) -> None:
        original = self.enroll()
        reference = original["authority_ref"]
        request_brief.observe_request(self.root, {**self.event, "prompt": "Status?"})
        self.assertEqual(reference, self.current().get("prior_authority_ref"))
        self.assertIsNotNone(self.guard("example.txt"))
        self.assertNotEqual(0, self.cli("bind", payload=original).returncode)
        expanded = self.record(
            authority_ref=reference,
            in_scope=["example.txt", "unexpected.txt"],
            allowed_mutations=["edit:example.txt", "edit:unexpected.txt"],
        )
        self.assertNotEqual(0, self.cli("bind", payload=expanded).returncode)
        narrowed = self.record(
            authority_ref=reference,
            allowed_mutations=["edit:example.txt"],
        )
        self.assertEqual(0, self.cli("bind", payload=narrowed).returncode)
        self.assertIsNone(self.guard("example.txt"))
        self.assertIsNotNone(self.guard("second.txt"))
        attempted_expansion = self.record(revision=2, authority_ref=reference)
        self.assertNotEqual(0, self.cli("bind", payload=attempted_expansion).returncode)


if __name__ == "__main__":
    unittest.main()
