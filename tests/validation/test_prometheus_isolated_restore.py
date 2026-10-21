"""SPEC-0245 W2: isolated Prometheus restore from a stopped-volume tar."""

import hashlib
import importlib.util
import io
import json
import os
import shutil
import tarfile
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/operations/prometheus-isolated-restore.py"
NEWEST = 1_760_000_000
HEAD_MS = (NEWEST + 1800) * 1000


def _load():
    spec = importlib.util.spec_from_file_location("prometheus_isolated_restore", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FakeDocker:
    """Records argv and answers like a restored Prometheus."""

    def __init__(self, *, ready=True, count="3", run_code=0, running=True, rm_code=0,
                 wal_corruptions=0):  # fmt: skip
        self.calls = []
        self.ready, self.count, self.running = ready, count, running
        self.run_code, self.rm_code, self.wal = run_code, rm_code, wal_corruptions

    def __call__(self, argv, *, timeout):
        self.calls.append(argv)
        if argv[:2] == ["docker", "run"]:
            return self.run_code, b"cid\n"
        if argv[:3] == ["docker", "rm", "-f"]:
            return self.rm_code, b""
        if argv[:2] == ["docker", "inspect"]:
            if "{{.State.Running}}" in argv:
                return 0, b"true\n" if self.running else b"false\n"
            return 0, b"true 137\n"
        if argv[:2] == ["docker", "logs"]:
            return 0, b"level=error msg=oom\n"
        url = argv[-1]
        if url.endswith("/-/ready"):
            return (0 if self.ready else 1), b"Prometheus Server is Ready.\n"
        if url.endswith("/metrics"):
            text = (
                f"prometheus_tsdb_head_max_time {HEAD_MS}\n"
                f"prometheus_tsdb_wal_corruptions_total {self.wal}\n"
            )
            return 0, text.encode()
        result = [{"value": [0, self.count]}]
        return 0, json.dumps({"status": "success", "data": {"result": result}}).encode()


class Clock:
    def __init__(self):
        self.now = 0.0

    def __call__(self):
        return self.now

    def sleep(self, seconds):
        self.now += seconds


class PrometheusIsolatedRestoreTests(unittest.TestCase):
    def setUp(self):
        self.module = _load()
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.archive = self.tmp / "prometheus-data.tar"
        block = self.tmp / "src" / "01BLOCK"
        block.mkdir(parents=True)
        meta = {"minTime": 1_000_000_000_000, "maxTime": NEWEST * 1000}
        (block / "meta.json").write_text(json.dumps(meta))
        with tarfile.open(self.archive, "w") as tar:
            tar.add(self.tmp / "src", arcname=".")
        self.sha = hashlib.sha256(self.archive.read_bytes()).hexdigest()

    def run_restore(self, docker, **overrides):
        clock = Clock()
        args = {
            "archive": self.archive,
            "sha256": self.sha,
            "workdir": self.tmp / "attempt",
            "keep": False,
            "run": docker,
            "sleep": clock.sleep,
            "clock": clock,
        }
        args.update(overrides)
        return self.module.restore(**args)

    def test_image_matches_the_compose_pin(self):
        compose = yaml.safe_load(
            (ROOT / "infra/06-observability/docker-compose.yml").read_text()
        )
        self.assertEqual(compose["services"]["prometheus"]["image"], self.module.IMAGE)

    def test_rejects_a_hash_mismatch_before_any_docker_call(self):
        docker = FakeDocker()
        with self.assertRaisesRegex(self.module.RestoreError, "archive_sha256"):
            self.run_restore(docker, sha256="0" * 64)
        self.assertEqual([], docker.calls)
        self.assertFalse((self.tmp / "attempt").exists())

    def test_refuses_an_existing_workdir_or_a_comma(self):
        (self.tmp / "attempt").mkdir()
        with self.assertRaisesRegex(self.module.RestoreError, "workdir_exists"):
            self.run_restore(FakeDocker())
        with self.assertRaisesRegex(self.module.RestoreError, "workdir_comma"):
            self.run_restore(FakeDocker(), workdir=self.tmp / "a,b")

    def test_runs_isolated_and_checks_head_and_blocks(self):
        docker = FakeDocker()
        receipt = self.run_restore(docker, sha256=self.sha.upper())
        run = next(c for c in docker.calls if c[:2] == ["docker", "run"])
        for flag in ("--network=none", "--pull=never", "--cap-drop=ALL",
                     "--security-opt=no-new-privileges", f"--label={self.module.LABEL}",
                     f"--user={os.getuid()}:{os.getgid()}", self.module.IMAGE,
                     "--storage.tsdb.retention.time=36500d"):  # fmt: skip
            self.assertIn(flag, run)
        self.assertTrue(any(a.endswith("prometheus.yml,readonly") for a in run))
        self.assertEqual("PASS", receipt["result"])
        self.assertEqual(1, receipt["blocks"])
        self.assertIsInstance(receipt["extract_seconds"], float)
        self.assertIsInstance(receipt["ready_seconds"], float)
        latest = NEWEST - 3600
        times = [q["time"] for q in receipt["queries"]]
        self.assertEqual([HEAD_MS // 1000 - 300, latest, latest - 7 * 86400], times)
        self.assertEqual(["docker", "rm", "-f"], docker.calls[-1][:3])
        self.assertFalse((self.tmp / "attempt").exists(), "scratch kept without --keep")

    def test_an_empty_query_fails_and_still_removes_the_container(self):
        docker = FakeDocker(count="0")
        receipt = self.run_restore(docker, keep=True)
        self.assertEqual("FAIL", receipt["result"])
        self.assertEqual(["docker", "rm", "-f"], docker.calls[-1][:3])
        self.assertTrue((self.tmp / "attempt/receipt.json").exists())

    def test_a_wal_corruption_fails(self):
        receipt = self.run_restore(FakeDocker(wal_corruptions=1))
        self.assertEqual("FAIL", receipt["result"])

    def test_never_ready_fails_with_evidence_and_cleans_up(self):
        docker = FakeDocker(ready=False)
        receipt = self.run_restore(docker, ready_timeout=30)
        self.assertEqual(
            ("FAIL", "ready_timeout"), (receipt["result"], receipt["failure"])
        )
        self.assertIsNone(receipt["ready_seconds"])
        self.assertIn("log_tail", receipt["exit"])
        self.assertEqual(["docker", "rm", "-f"], docker.calls[-1][:3])
        self.assertFalse((self.tmp / "attempt").exists())

    def test_an_exited_container_stops_the_wait_and_keeps_its_state(self):
        docker = FakeDocker(ready=False, running=False)
        receipt = self.run_restore(docker)
        self.assertEqual("exited", receipt["failure"])
        self.assertEqual("true 137", receipt["exit"]["state"])
        self.assertLess(sum(c[:2] == ["docker", "exec"] for c in docker.calls), 3)

    def test_a_failed_docker_run_fails(self):
        receipt = self.run_restore(FakeDocker(run_code=125))
        self.assertEqual(
            ("FAIL", "docker_run"), (receipt["result"], receipt["failure"])
        )

    def test_scratch_stays_when_the_container_cannot_be_removed(self):
        self.run_restore(FakeDocker(rm_code=1))
        self.assertTrue((self.tmp / "attempt/receipt.json").exists())

    def test_a_traversal_member_is_refused_by_the_extract_filter(self):
        bad = self.tmp / "bad.tar"
        with tarfile.open(bad, "w") as tar:
            info = tarfile.TarInfo("../escape")
            info.size = 1
            tar.addfile(info, io.BytesIO(b"x"))
        sha = hashlib.sha256(bad.read_bytes()).hexdigest()
        with self.assertRaises(tarfile.FilterError):
            self.run_restore(FakeDocker(), archive=bad, sha256=sha)
        self.assertFalse((self.tmp / "escape").exists())


if __name__ == "__main__":
    unittest.main()
