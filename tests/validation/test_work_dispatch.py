"""The work dispatcher runs shell workers in disposable Git repositories only."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from pathlib import Path

from scripts.operations import work_dispatch as dispatch


def git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args], check=True, capture_output=True, text=True
    ).stdout


def unit(uid: str, script: str, owned=(), shared=(), depends=(), timeout=30) -> dict:
    return {
        "id": uid,
        "command": ["sh", "-c", script],
        "owned_paths": list(owned),
        "shared_resources": list(shared),
        "depends_on": list(depends),
        "timeout": timeout,
    }


class DispatchTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        self.repo = root / "repo"
        self.state = root / "state"
        self.repo.mkdir()
        git(self.repo, "init", "-q", "-b", "main")
        git(self.repo, "config", "user.email", "t@example.invalid")
        git(self.repo, "config", "user.name", "t")
        (self.repo / "base.txt").write_text("base\n")
        git(self.repo, "add", "base.txt")
        git(self.repo, "commit", "-q", "-m", "base")

    def run_plan(self, units, checks=(), **extra) -> dict:
        plan = {
            "task": "TSK-TEST",
            "brief_revision": "7",
            "max_workers": 2,
            "units": units,
            "integration_checks": [list(c) for c in checks],
            **extra,
        }
        return dispatch.run(self.repo, self.state, plan)

    def test_two_independent_units_run_together_and_integrate(self) -> None:
        report = self.run_plan(
            [
                unit("a", "sleep 1; echo a > a.txt", owned=["a.txt"]),
                unit("b", "sleep 1; echo b > b.txt", owned=["b.txt"]),
            ],
            checks=[["sh", "-c", "test -f a.txt && test -f b.txt"]],
        )
        states = {u["id"]: u["status"] for u in report["units"]}
        self.assertEqual({"a": "succeeded", "b": "succeeded"}, states)
        self.assertEqual("passed", report["integration"]["status"])
        self.assertLess(report["elapsed_seconds"], 1.9)
        patch = Path(report["integration"]["patch"]).read_text()
        self.assertIn("a.txt", patch)
        self.assertIn("b.txt", patch)
        self.assertEqual("", git(self.repo, "status", "--porcelain"))
        self.assertEqual(1, len(git(self.repo, "worktree", "list").splitlines()))

    def test_workers_receive_the_task_brief_and_fence(self) -> None:
        report = self.run_plan(
            [
                unit(
                    "a",
                    'echo "$HY_TASK $HY_BRIEF_REVISION $HY_FENCE" > a.txt',
                    owned=["a.txt"],
                )
            ]
        )
        patch = Path(report["integration"]["patch"]).read_text()
        self.assertIn("+TSK-TEST 7 {", patch)

    def test_a_shared_resource_serialises_its_units(self) -> None:
        report = self.run_plan(
            [
                unit(
                    "a",
                    "sleep 1; echo a > a.txt",
                    owned=["a.txt"],
                    shared=["port:5432"],
                ),
                unit(
                    "b",
                    "sleep 1; echo b > b.txt",
                    owned=["b.txt"],
                    shared=["port:5432"],
                ),
            ]
        )
        first, second = sorted(report["units"], key=lambda u: u["started"])
        self.assertGreaterEqual(second["started"], first["finished"])
        self.assertNotEqual(first["fence"], second["fence"])

    def test_overlapping_owned_paths_serialise(self) -> None:
        report = self.run_plan(
            [
                unit("a", "sleep 1; mkdir -p d; echo a > d/a.txt", owned=["d/"]),
                unit("b", "sleep 1; mkdir -p d; echo b > d/b.txt", owned=["d/b.txt"]),
            ]
        )
        first, second = sorted(report["units"], key=lambda u: u["started"])
        self.assertGreaterEqual(second["started"], first["finished"])

    def test_a_write_outside_ownership_is_rejected(self) -> None:
        report = self.run_plan(
            [unit("a", "echo x > a.txt; echo y > base.txt", owned=["a.txt"])]
        )
        (result,) = report["units"]
        self.assertEqual("rejected", result["status"])
        self.assertIn("base.txt", result["reason"])
        self.assertEqual("not run", report["integration"]["status"])

    def test_a_worker_cannot_replace_another_units_patch(self) -> None:
        report = self.run_plan(
            [
                unit(
                    "a",
                    "sleep 1; echo junk > ../../b.patch; echo a > a.txt",
                    owned=["a.txt"],
                ),
                unit("b", "echo b > b.txt", owned=["b.txt"]),
            ]
        )
        self.assertEqual("passed", report["integration"]["status"])
        patch = Path(report["integration"]["patch"]).read_text()
        self.assertIn("+b\n", patch)

    def test_a_failure_blocks_only_its_downstream(self) -> None:
        report = self.run_plan(
            [
                unit("a", "exit 3", owned=["a.txt"]),
                unit("c", "echo c > c.txt", owned=["c.txt"], depends=["a"]),
                unit("b", "echo b > b.txt", owned=["b.txt"]),
            ]
        )
        states = {u["id"]: u["status"] for u in report["units"]}
        self.assertEqual({"a": "failed", "b": "succeeded", "c": "blocked"}, states)
        self.assertEqual("not run", report["integration"]["status"])

    def test_a_timeout_kills_the_worker(self) -> None:
        report = self.run_plan([unit("a", "sleep 30", owned=["a.txt"], timeout=1)])
        (result,) = report["units"]
        self.assertEqual(("failed", "timeout"), (result["status"], result["reason"]))

    def test_cancel_stops_running_and_pending_workers(self) -> None:
        marker = self.state.parent / "child.pid"
        script = f"sleep 30 & echo $! > {marker}; wait"

        def cancel() -> None:
            deadline = time.monotonic() + 10
            while not marker.exists() and time.monotonic() < deadline:
                time.sleep(0.05)
            time.sleep(0.1)
            dispatch.cancel(self.state)

        threading.Thread(target=cancel).start()
        report = self.run_plan(
            [
                unit("a", script, owned=["a.txt"]),
                unit("b", "echo b > b.txt", owned=["b.txt"], depends=["a"]),
            ]
        )
        states = {u["id"]: u["status"] for u in report["units"]}
        self.assertEqual({"a": "cancelled", "b": "blocked"}, states)
        self.assertEqual("cancelled", report["status"])
        child = int(marker.read_text())
        time.sleep(0.2)
        with self.assertRaises(ProcessLookupError):
            os.kill(child, 0)
        self.assertEqual(1, len(git(self.repo, "worktree", "list").splitlines()))

    def test_a_result_after_the_lease_was_taken_over_is_refused(self) -> None:
        def take_over() -> None:
            time.sleep(1.5)
            store = dispatch.Leases(self.state)
            self.assertIsNotNone(store.acquire(["path:a.txt"], "other-run", 60))

        threading.Thread(target=take_over).start()
        report = self.run_plan(
            [unit("a", "sleep 2.5; echo a > a.txt", owned=["a.txt"])], lease_seconds=1
        )
        (result,) = report["units"]
        self.assertEqual(
            ("rejected", "stale lease"), (result["status"], result["reason"])
        )

    def test_lease_generations_fence_an_expired_holder(self) -> None:
        store = dispatch.Leases(self.state)
        first = store.acquire(["port:1"], "one", 0.2)
        self.assertIsNone(store.acquire(["port:1"], "two", 60))
        time.sleep(0.3)
        second = store.acquire(["port:1"], "two", 60)
        self.assertGreater(second["port:1"], first["port:1"])
        self.assertFalse(store.valid(first, "one"))
        self.assertTrue(store.valid(second, "two"))

    def test_an_integration_check_failure_fails_the_run(self) -> None:
        report = self.run_plan(
            [unit("a", "echo a > a.txt", owned=["a.txt"])],
            checks=[["sh", "-c", "exit 1"]],
        )
        self.assertEqual("succeeded", report["units"][0]["status"])
        self.assertEqual("failed", report["integration"]["status"])
        self.assertEqual("failed", report["status"])

    def test_a_dependent_unit_starts_from_its_upstream_result(self) -> None:
        report = self.run_plan(
            [
                unit("a", "echo a > a.txt", owned=["a.txt"]),
                unit("b", "cat a.txt > b.txt", owned=["b.txt"], depends=["a"]),
            ]
        )
        self.assertEqual(["b.txt"], report["units"][1]["changed"])
        patch = Path(report["integration"]["patch"]).read_text()
        self.assertEqual(2, patch.count("+a\n"))

    def test_cleanup_recovers_after_the_dispatcher_dies(self) -> None:
        plan = self.state.parent / "plan.json"
        plan.write_text(json.dumps({"units": [unit("a", "sleep 30", owned=["a.txt"])]}))
        script = Path(dispatch.__file__)
        dispatcher = subprocess.Popen(
            [
                sys.executable,
                str(script),
                "--repo",
                str(self.repo),
                "--state-dir",
                str(self.state),
                "run",
                str(plan),
            ],
            stdout=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
        )
        deadline = time.monotonic() + 10
        while not list(self.state.glob("runs/*/a.pgid")):
            self.assertLess(time.monotonic(), deadline)
            time.sleep(0.05)
        (pgid_file,) = self.state.glob("runs/*/a.pgid")
        worker = int(pgid_file.read_text())
        dispatcher.kill()
        dispatcher.wait()
        self.assertEqual(2, len(git(self.repo, "worktree", "list").splitlines()))
        removed = dispatch.cleanup(self.repo, self.state)
        self.assertEqual(1, len(removed))
        self.assertIsNotNone(
            dispatch.Leases(self.state).acquire(["path:a.txt"], "next-run", 60)
        )
        time.sleep(0.2)
        with self.assertRaises(ProcessLookupError):
            os.killpg(worker, 0)
        self.assertEqual(1, len(git(self.repo, "worktree", "list").splitlines()))

    def test_a_rename_into_an_owned_path_is_rejected(self) -> None:
        report = self.run_plan([unit("a", "mv base.txt a.txt", owned=["a.txt"])])
        (result,) = report["units"]
        self.assertEqual("rejected", result["status"])
        self.assertIn("base.txt", result["reason"])

    def test_a_unit_without_changes_integrates_and_feeds_dependents(self) -> None:
        report = self.run_plan(
            [
                unit("check", "test -f base.txt"),
                unit("b", "echo b > b.txt", owned=["b.txt"], depends=["check"]),
            ]
        )
        states = {u["id"]: u["status"] for u in report["units"]}
        self.assertEqual({"check": "succeeded", "b": "succeeded"}, states)
        self.assertEqual("passed", report["integration"]["status"])

    def test_background_children_end_with_their_worker(self) -> None:
        marker = self.state.parent / "child.pid"
        report = self.run_plan(
            [
                unit(
                    "a",
                    f"sleep 30 & echo $! > {marker}; echo a > a.txt",
                    owned=["a.txt"],
                )
            ]
        )
        self.assertEqual("succeeded", report["units"][0]["status"])
        time.sleep(0.2)
        with self.assertRaises(ProcessLookupError):
            os.kill(int(marker.read_text()), 0)

    def test_cancel_reaches_a_running_integration_check(self) -> None:
        marker = self.state.parent / "check.pid"

        def cancel() -> None:
            deadline = time.monotonic() + 10
            while not marker.exists() and time.monotonic() < deadline:
                time.sleep(0.05)
            dispatch.cancel(self.state)

        threading.Thread(target=cancel).start()
        report = self.run_plan(
            [unit("a", "echo a > a.txt", owned=["a.txt"])],
            checks=[["sh", "-c", f"echo $$ > {marker}; sleep 30"]],
        )
        self.assertEqual("cancelled", report["status"])
        self.assertLess(report["elapsed_seconds"], 10)
        time.sleep(0.2)
        with self.assertRaises(ProcessLookupError):
            os.kill(int(marker.read_text()), 0)

    def test_an_integration_check_times_out(self) -> None:
        report = self.run_plan(
            [unit("a", "echo a > a.txt", owned=["a.txt"])],
            checks=[["sleep", "30"]],
            integration_timeout=1,
        )
        self.assertEqual("failed", report["integration"]["status"])
        self.assertIn("timeout", report["integration"]["reason"])

    def test_a_damaged_worktree_cannot_stage_into_the_main_repository(self) -> None:
        (self.repo / "user.txt").write_text("user work\n")
        report = self.run_plan(
            [unit("a", "rm -f .git; echo a > a.txt", owned=["a.txt"])]
        )
        self.assertEqual(["a.txt"], report["units"][0].get("changed"))
        self.assertEqual("?? user.txt\n", git(self.repo, "status", "--porcelain"))
        self.assertEqual(1, len(git(self.repo, "worktree", "list").splitlines()))

    def test_an_older_cancel_does_not_stop_a_new_run(self) -> None:
        dispatch.cancel(self.state)
        time.sleep(0.05)
        report = self.run_plan([unit("a", "echo a > a.txt", owned=["a.txt"])])
        self.assertEqual("succeeded", report["status"])

    def test_the_integrated_patch_carries_its_digest(self) -> None:
        report = self.run_plan([unit("a", "echo a > a.txt", owned=["a.txt"])])
        integration = report["integration"]
        digest = hashlib.sha256(Path(integration["patch"]).read_bytes()).hexdigest()
        self.assertEqual(digest, integration["sha256"])

    def test_a_non_utf8_file_name_does_not_crash_the_run(self) -> None:
        report = self.run_plan(
            [unit("a", "mkdir -p d; printf x > \"d/$(printf 'n\\377')\"", owned=["d/"])]
        )
        self.assertEqual("succeeded", report["units"][0]["status"])

    def test_a_command_that_cannot_start_fails_cleanly(self) -> None:
        plan = [unit("a", "true", owned=["a.txt"])]
        plan[0]["command"] = ["no-such-tool-for-dispatch"]
        report = self.run_plan(plan)
        self.assertEqual("failed", report["units"][0]["status"])
        self.assertEqual(1, len(git(self.repo, "worktree", "list").splitlines()))
        self.assertIsNotNone(
            dispatch.Leases(self.state).acquire(["path:a.txt"], "next-run", 60)
        )

    def test_bad_plans_are_refused(self) -> None:
        for units in (
            [unit("a", "true", depends=["b"]), unit("b", "true", depends=["a"])],
            [unit("a", "true", depends=["missing"])],
            [unit("a", "true"), unit("a", "true")],
            [unit("a", "true", owned=["../x"])],
            [unit("a", "true", owned=["."])],
            [unit("/tmp/victim", "true", owned=["x.txt"])],
            [unit("..", "true", owned=["x.txt"])],
            [unit("a/b", "true", owned=["x.txt"])],
        ):
            with self.subTest(units=json.dumps(units)[:80]):
                with self.assertRaises(dispatch.PlanError):
                    self.run_plan(units)


if __name__ == "__main__":
    unittest.main()
