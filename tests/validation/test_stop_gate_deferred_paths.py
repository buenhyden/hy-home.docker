"""Stop gate deferred-path ownership contract tests.

The logical-commit Stop gate must keep blocking undeclared dirty work while
honoring paths that tracked governance explicitly defers to a later unit.
"""

from __future__ import annotations

import json
import os
import pathlib
import subprocess
import tempfile
import textwrap
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
HOOK = ROOT / "scripts/hooks/agent-event-hook.sh"
REGISTRY_RELATIVE = "docs/00.agent-governance/policies/approval-boundaries.md"

OWNING_TASK_RELATIVE = "docs/04.execution/tasks/owning-task.md"


class StopGateDeferredPathTests(unittest.TestCase):
    def _repo(self, name: str) -> pathlib.Path:
        repo = pathlib.Path(name)
        subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
        subprocess.run(
            ["git", "config", "user.email", "t@example.com"], cwd=repo, check=True
        )
        subprocess.run(["git", "config", "user.name", "Test"], cwd=repo, check=True)
        (repo / "docs/04.execution/tasks").mkdir(parents=True)
        (repo / OWNING_TASK_RELATIVE).write_text("# Owning Task\n", encoding="utf-8")
        gate = repo / "scripts/validation/run-ci-gate.py"
        gate.parent.mkdir(parents=True)
        gate.write_text("raise SystemExit(0)\n", encoding="utf-8")
        (repo / "tracked-a.txt").write_text("original a\n", encoding="utf-8")
        (repo / "tracked-b.txt").write_text("original b\n", encoding="utf-8")
        subprocess.run(["git", "add", "-A"], cwd=repo, check=True)
        subprocess.run(["git", "commit", "-qm", "seed"], cwd=repo, check=True)
        return repo

    @staticmethod
    def _write_registry(repo: pathlib.Path, body: str) -> None:
        registry = repo / REGISTRY_RELATIVE
        registry.parent.mkdir(parents=True, exist_ok=True)
        registry.write_text(textwrap.dedent(body), encoding="utf-8")

    @staticmethod
    def _run_stop(repo: pathlib.Path) -> tuple[int, str]:
        environment = dict(os.environ)
        environment["CLAUDE_PROJECT_DIR"] = str(repo)
        environment.pop("AGENT_ALLOW_UNCOMMITTED_STOP", None)
        result = subprocess.run(
            ["bash", str(HOOK), "Stop"],
            cwd=repo,
            input="{}",
            capture_output=True,
            text=True,
            env=environment,
        )
        return result.returncode, result.stdout

    @staticmethod
    def _blocked_paths(stdout: str) -> list[str]:
        for line in stdout.splitlines():
            line = line.strip()
            if not line.startswith("{"):
                continue
            try:
                payload = json.loads(line)
            except ValueError:
                continue
            if payload.get("decision") != "block":
                continue
            reason = payload.get("reason", "")
            if "Uncommitted paths:" not in reason:
                continue
            _, listed = reason.split("Uncommitted paths:", 1)
            return [entry for entry in listed.strip().splitlines() if entry.strip()]
        return []

    def test_clean_tree_does_not_block(self) -> None:
        with tempfile.TemporaryDirectory(prefix="stop-gate-clean.") as name:
            repo = self._repo(name)
            _, stdout = self._run_stop(repo)
            self.assertEqual(self._blocked_paths(stdout), [])

    def test_undeclared_dirty_path_still_blocks(self) -> None:
        with tempfile.TemporaryDirectory(prefix="stop-gate-undeclared.") as name:
            repo = self._repo(name)
            (repo / "tracked-a.txt").write_text("changed a\n", encoding="utf-8")
            _, stdout = self._run_stop(repo)
            self.assertIn("tracked-a.txt", " ".join(self._blocked_paths(stdout)))

    def test_declared_deferred_path_is_exempt(self) -> None:
        with tempfile.TemporaryDirectory(prefix="stop-gate-declared.") as name:
            repo = self._repo(name)
            self._write_registry(
                repo,
                f"""\
                schema: agent-governance/deferred-paths/v1
                deferrals:
                  - path: tracked-a.txt
                    reason: Preserved for the later reviewed unit.
                    owning_task: {OWNING_TASK_RELATIVE}
                """,
            )
            subprocess.run(["git", "add", "-A"], cwd=repo, check=True)
            subprocess.run(["git", "commit", "-qm", "register"], cwd=repo, check=True)
            # Dirty the declared path only after the registry is committed, so
            # the working tree genuinely differs from HEAD.
            (repo / "tracked-a.txt").write_text("changed a\n", encoding="utf-8")
            self.assertNotEqual(
                subprocess.run(
                    ["git", "status", "--porcelain=v1"],
                    cwd=repo,
                    capture_output=True,
                    text=True,
                    check=True,
                ).stdout.strip(),
                "",
                "the declared path must actually be dirty for this test to mean anything",
            )
            _, stdout = self._run_stop(repo)
            self.assertEqual(self._blocked_paths(stdout), [])

    def test_declared_path_does_not_exempt_other_dirty_paths(self) -> None:
        with tempfile.TemporaryDirectory(prefix="stop-gate-mixed.") as name:
            repo = self._repo(name)
            self._write_registry(
                repo,
                f"""\
                schema: agent-governance/deferred-paths/v1
                deferrals:
                  - path: tracked-a.txt
                    reason: Preserved for the later reviewed unit.
                    owning_task: {OWNING_TASK_RELATIVE}
                """,
            )
            subprocess.run(["git", "add", "-A"], cwd=repo, check=True)
            subprocess.run(["git", "commit", "-qm", "register"], cwd=repo, check=True)
            (repo / "tracked-a.txt").write_text("changed a\n", encoding="utf-8")
            (repo / "tracked-b.txt").write_text("changed b\n", encoding="utf-8")
            _, stdout = self._run_stop(repo)
            blocked = " ".join(self._blocked_paths(stdout))
            self.assertIn("tracked-b.txt", blocked)
            self.assertNotIn("tracked-a.txt", blocked)

    def test_incomplete_declaration_does_not_exempt(self) -> None:
        for omitted in ("reason", "owning_task"):
            with (
                self.subTest(omitted=omitted),
                tempfile.TemporaryDirectory(prefix="stop-gate-incomplete.") as name,
            ):
                repo = self._repo(name)
                entry = ["  - path: tracked-a.txt"]
                if omitted != "reason":
                    entry.append("    reason: Preserved for the later reviewed unit.")
                if omitted != "owning_task":
                    entry.append(f"    owning_task: {OWNING_TASK_RELATIVE}")
                self._write_registry(
                    repo,
                    "schema: agent-governance/deferred-paths/v1\ndeferrals:\n"
                    + "\n".join(entry)
                    + "\n",
                )
                subprocess.run(["git", "add", "-A"], cwd=repo, check=True)
                subprocess.run(
                    ["git", "commit", "-qm", "register"], cwd=repo, check=True
                )
                (repo / "tracked-a.txt").write_text("changed a\n", encoding="utf-8")
                _, stdout = self._run_stop(repo)
                self.assertIn("tracked-a.txt", " ".join(self._blocked_paths(stdout)))

    def test_missing_owning_task_does_not_exempt(self) -> None:
        with tempfile.TemporaryDirectory(prefix="stop-gate-missing-task.") as name:
            repo = self._repo(name)
            self._write_registry(
                repo,
                """\
                schema: agent-governance/deferred-paths/v1
                deferrals:
                  - path: tracked-a.txt
                    reason: Preserved for the later reviewed unit.
                    owning_task: docs/04.execution/tasks/does-not-exist.md
                """,
            )
            subprocess.run(["git", "add", "-A"], cwd=repo, check=True)
            subprocess.run(["git", "commit", "-qm", "register"], cwd=repo, check=True)
            (repo / "tracked-a.txt").write_text("changed a\n", encoding="utf-8")
            _, stdout = self._run_stop(repo)
            self.assertIn("tracked-a.txt", " ".join(self._blocked_paths(stdout)))

    def test_malformed_registry_fails_closed(self) -> None:
        for body in ("schema: wrong/schema\ndeferrals: []\n", "deferrals: [\n"):
            with (
                self.subTest(body=body),
                tempfile.TemporaryDirectory(prefix="stop-gate-malformed.") as name,
            ):
                repo = self._repo(name)
                self._write_registry(repo, body)
                subprocess.run(["git", "add", "-A"], cwd=repo, check=True)
                subprocess.run(
                    ["git", "commit", "-qm", "register"], cwd=repo, check=True
                )
                (repo / "tracked-a.txt").write_text("changed a\n", encoding="utf-8")
                _, stdout = self._run_stop(repo)
                self.assertIn("tracked-a.txt", " ".join(self._blocked_paths(stdout)))

    def test_untracked_registry_does_not_exempt(self) -> None:
        with tempfile.TemporaryDirectory(prefix="stop-gate-untracked.") as name:
            repo = self._repo(name)
            self._write_registry(
                repo,
                f"""\
                schema: agent-governance/deferred-paths/v1
                deferrals:
                  - path: tracked-a.txt
                    reason: Preserved for the later reviewed unit.
                    owning_task: {OWNING_TASK_RELATIVE}
                """,
            )
            (repo / "tracked-a.txt").write_text("changed a\n", encoding="utf-8")
            _, stdout = self._run_stop(repo)
            self.assertIn("tracked-a.txt", " ".join(self._blocked_paths(stdout)))


if __name__ == "__main__":
    unittest.main()
