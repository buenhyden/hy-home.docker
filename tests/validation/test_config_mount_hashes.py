"""Host-to-container single-file mount hash check tests (Docker stubbed)."""

import importlib.util
import io
import json
import subprocess
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/operations/check-config-mount-hashes.py"


def _load():
    spec = importlib.util.spec_from_file_location("check_config_mount_hashes", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FakeDocker:
    def __init__(self, mounts: dict, files: dict, helper_files: dict | None = None):
        self.mounts = mounts
        self.files = files
        self.helper_files = helper_files or {}
        self.calls = []

    def __call__(self, argv, **_kwargs):
        self.calls.append(argv)
        if argv[:2] == ["docker", "ps"]:
            out = "".join(f"{name}\n" for name in self.mounts).encode()
            return subprocess.CompletedProcess(argv, 0, out, b"")
        if argv[:2] == ["docker", "inspect"]:
            payload = [
                {"Name": f"/{name}", "Mounts": self.mounts[name]} for name in argv[2:]
            ]
            return subprocess.CompletedProcess(
                argv, 0, json.dumps(payload).encode(), b""
            )
        if argv[:2] == ["docker", "exec"]:
            key = f"{argv[2]}:{argv[4]}"
            if key not in self.files:
                return subprocess.CompletedProcess(argv, 127, b"", b"no cat")
            return subprocess.CompletedProcess(argv, 0, self.files[key], b"")
        if argv[:2] == ["docker", "run"]:
            pid = argv[argv.index("--pid") + 1]
            key = f"{pid}:{argv[-1]}"
            if key not in self.helper_files:
                return subprocess.CompletedProcess(argv, 1, b"", b"denied")
            return subprocess.CompletedProcess(argv, 0, self.helper_files[key], b"")
        raise AssertionError(f"unexpected command: {argv}")


def _bind(source: Path, dest: str) -> dict:
    return {"Type": "bind", "Source": str(source), "Destination": dest}


class ConfigMountHashTests(unittest.TestCase):
    def setUp(self):
        self.module = _load()
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "infra").mkdir()
        (self.root / "secrets").mkdir()
        self.same = self.root / "infra/same.conf"
        self.same.write_bytes(b"alpha-config\n")
        self.stale = self.root / "infra/stale.conf"
        self.stale.write_bytes(b"new-host-bytes\n")
        self.secret = self.root / "secrets/token.txt"
        self.secret.write_bytes(b"do-not-read\n")

    def tearDown(self):
        self.tmp.cleanup()

    def _run(self, docker, *extra):
        out = io.StringIO()
        with redirect_stdout(out):
            code = self.module.main(["--root", str(self.root), *extra], run=docker)
        return code, out.getvalue()

    def test_match_and_diff_report_and_exit_nonzero(self):
        docker = FakeDocker(
            {
                "svc-a": [
                    _bind(self.same, "/etc/a.conf"),
                    _bind(self.stale, "/etc/b.conf"),
                ]
            },
            {
                "svc-a:/etc/a.conf": b"alpha-config\n",
                "svc-a:/etc/b.conf": b"old-bytes\n",
            },
        )
        code, out = self._run(docker)
        self.assertEqual(1, code)
        self.assertRegex(out, r"MATCH\s+svc-a\s+/etc/a.conf\s+infra/same.conf")
        self.assertRegex(out, r"DIFF\s+svc-a\s+/etc/b.conf\s+infra/stale.conf")
        for content in ("alpha-config", "new-host-bytes", "old-bytes"):
            self.assertNotIn(content, out)

    def test_all_match_exits_zero(self):
        docker = FakeDocker(
            {"svc-a": [_bind(self.same, "/etc/a.conf")]},
            {"svc-a:/etc/a.conf": b"alpha-config\n"},
        )
        code, _ = self._run(docker)
        self.assertEqual(0, code)

    def test_secrets_directories_and_outside_paths_are_never_read(self):
        outside = tempfile.NamedTemporaryFile()
        self.addCleanup(outside.close)
        docker = FakeDocker(
            {
                "svc-a": [
                    _bind(self.secret, "/run/secrets/token"),
                    _bind(self.root / "infra", "/etc/dir"),
                    _bind(Path(outside.name), "/etc/outside"),
                    {"Type": "volume", "Source": str(self.same), "Destination": "/v"},
                ]
            },
            {},
        )
        code, out = self._run(docker)
        self.assertEqual(0, code)
        self.assertEqual(
            [],
            [
                c
                for c in docker.calls
                if c[:2] not in (["docker", "ps"], ["docker", "inspect"])
            ],
        )
        self.assertNotIn("secrets", out)

    def test_unreadable_container_file_is_reported_without_failing(self):
        docker = FakeDocker({"svc-a": [_bind(self.same, "/etc/a.conf")]}, {})
        code, out = self._run(docker)
        self.assertEqual(0, code)
        self.assertRegex(out, r"UNREADABLE\s+svc-a\s+/etc/a.conf\s+infra/same.conf")

    def test_reads_through_container_namespace_not_docker_cp(self):
        # docker cp resolves bind mounts to the host Source, so it cannot see a
        # stale inode; the check must read the file from inside the container.
        docker = FakeDocker(
            {"svc-a": [_bind(self.stale, "/etc/b.conf")]},
            {"svc-a:/etc/b.conf": b"old-bytes\n"},
        )
        code, _ = self._run(docker)
        self.assertEqual(1, code)
        self.assertIn(["docker", "exec", "svc-a", "cat", "/etc/b.conf"], docker.calls)
        self.assertFalse([c for c in docker.calls if c[:2] == ["docker", "cp"]])

    def test_helper_image_reads_binaryless_container_via_shared_pid_namespace(self):
        docker = FakeDocker(
            {"svc-a": [_bind(self.stale, "/etc/b.conf")]},
            {},
            {"container:svc-a:/proc/1/root/etc/b.conf": b"old-bytes\n"},
        )
        code, out = self._run(docker, "--helper-image", "alpine:3")
        self.assertEqual(1, code)
        self.assertRegex(out, r"DIFF\s+svc-a\s+/etc/b.conf")
        helper = next(c for c in docker.calls if c[:2] == ["docker", "run"])
        self.assertIn("--rm", helper)
        self.assertIn("alpine:3", helper)
        self.assertEqual(["--network", "none"], helper[helper.index("--network") :][:2])

    def test_without_helper_image_no_container_is_started(self):
        docker = FakeDocker({"svc-a": [_bind(self.same, "/etc/a.conf")]}, {})
        self._run(docker)
        self.assertFalse([c for c in docker.calls if c[:2] == ["docker", "run"]])

    def test_filters_running_containers_by_compose_project(self):
        docker = FakeDocker({}, {})
        self._run(docker)
        self.assertIn("label=com.docker.compose.project=hy-home-infra", docker.calls[0])


if __name__ == "__main__":
    unittest.main()
