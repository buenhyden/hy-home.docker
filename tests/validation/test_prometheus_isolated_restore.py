"""SPEC-0245 W2: isolated Prometheus restore from a stopped-volume tar."""

import hashlib
import importlib.util
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


def _load():
    spec = importlib.util.spec_from_file_location("prometheus_isolated_restore", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FakeDocker:
    """Records argv; answers exec probes like a ready Prometheus."""

    def __init__(self, *, ready=True, count="3"):
        self.calls = []
        self.ready = ready
        self.count = count

    def __call__(self, argv, *, timeout):
        self.calls.append(argv)
        if argv[:2] == ["docker", "exec"]:
            if argv[-1].endswith("/-/ready"):
                return (0 if self.ready else 1), b"Prometheus Server is Ready.\n"
            result = [{"value": [0, self.count]}]
            body = {"status": "success", "data": {"result": result}}
            return 0, json.dumps(body).encode()
        return 0, b"cid\n"


class PrometheusIsolatedRestoreTests(unittest.TestCase):
    def setUp(self):
        self.module = _load()
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.archive = self.tmp / "prometheus-data.tar"
        block = self.tmp / "src" / "01BLOCK"
        block.mkdir(parents=True)
        (block / "meta.json").write_text(
            json.dumps({"minTime": 1_000_000_000_000, "maxTime": 1_760_000_000_000})
        )
        with tarfile.open(self.archive, "w") as tar:
            tar.add(self.tmp / "src", arcname=".")
        self.sha = hashlib.sha256(self.archive.read_bytes()).hexdigest()

    def run_restore(self, docker, **overrides):
        args = {
            "archive": self.archive,
            "sha256": self.sha,
            "workdir": self.tmp / "attempt",
            "keep": False,
            "run": docker,
            "sleep": lambda _s: None,
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

    def test_refuses_an_existing_workdir(self):
        (self.tmp / "attempt").mkdir()
        with self.assertRaisesRegex(self.module.RestoreError, "workdir_exists"):
            self.run_restore(FakeDocker())

    def test_runs_isolated_and_reports_ready_time_and_both_queries(self):
        docker = FakeDocker()
        receipt = self.run_restore(docker)
        run = next(c for c in docker.calls if c[:2] == ["docker", "run"])
        for flag in ("--network=none", "--pull=never", "--cap-drop=ALL"):
            self.assertIn(flag, run)
        self.assertIn(f"--user={os.getuid()}:{os.getgid()}", run)
        self.assertIn(self.module.IMAGE, run)
        self.assertIn("--storage.tsdb.retention.time=36500d", run)
        self.assertEqual("PASS", receipt["result"])
        self.assertEqual(1, receipt["blocks"])
        self.assertIsInstance(receipt["ready_seconds"], float)
        latest = 1_760_000_000 - 3600
        times = [q["time"] for q in receipt["queries"]]
        self.assertEqual([latest, latest - 7 * 86400], times)
        self.assertEqual(["docker", "rm", "-f"], docker.calls[-1][:3])
        self.assertFalse((self.tmp / "attempt").exists(), "scratch kept without --keep")

    def test_an_empty_query_fails_and_still_removes_the_container(self):
        docker = FakeDocker(count="0")
        receipt = self.run_restore(docker, keep=True)
        self.assertEqual("FAIL", receipt["result"])
        self.assertEqual(["docker", "rm", "-f"], docker.calls[-1][:3])
        self.assertTrue((self.tmp / "attempt/receipt.json").exists())

    def test_never_ready_fails(self):
        receipt = self.run_restore(FakeDocker(ready=False), ready_timeout=3)
        self.assertEqual("FAIL", receipt["result"])
        self.assertIsNone(receipt["ready_seconds"])


if __name__ == "__main__":
    unittest.main()
