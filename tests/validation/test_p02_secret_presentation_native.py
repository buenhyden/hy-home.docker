"""Opt-in proof of Compose file-backed secret metadata for Valkey ACL rendering."""

from __future__ import annotations

import hashlib
import json
import os
import secrets
import subprocess
import tempfile
import time
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
RENDERER = ROOT / "infra/04-data/mng-db/valkey/scripts/render-monitor-acl.sh"
IMAGE = "python:3.13.15-alpine"
DOCKER_HOST = "unix:///var/run/docker.sock"


@unittest.skipUnless(
    os.environ.get("HYHOME_P02_SECRET_NATIVE") == "1",
    "set HYHOME_P02_SECRET_NATIVE=1 for disposable Compose secret metadata proof",
)
class ComposeSecretPresentationNativeTests(unittest.TestCase):
    """Use synthetic bytes only; inspect metadata and digests, never secret text."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.temporary = tempfile.TemporaryDirectory(prefix="hy-p02-secret-")
        cls.addClassCleanup(cls.temporary.cleanup)
        cls.root = Path(cls.temporary.name)
        cls.host_uid = os.getuid()
        cls.host_gid = os.getgid()
        if cls.host_uid == 999 or cls.host_gid == 999:
            raise unittest.SkipTest(
                "host identity overlaps runtime 999:999; cannot prove wrong-owner "
                "or supplementary-group behavior"
            )
        cls.docker_environment = {
            "COMPOSE_DISABLE_ENV_FILE": "1",
            "DOCKER_HOST": DOCKER_HOST,
            "HOME": str(cls.root),
            "PATH": "/usr/bin:/bin",
        }
        inspected = cls.docker("image", "inspect", IMAGE, check=False)
        if inspected.returncode:
            raise unittest.SkipTest(f"required cached image unavailable: {IMAGE}")
        image_data = json.loads(inspected.stdout)
        if len(image_data) != 1 or not image_data[0]["Id"].startswith("sha256:"):
            raise RuntimeError("cached Python image identity is ambiguous")
        cls.image_id = image_data[0]["Id"]

    @classmethod
    def docker(
        cls, *args: str, check: bool = True, timeout: int = 90
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["/usr/bin/docker", "--host", DOCKER_HOST, *args],
            capture_output=True,
            text=True,
            check=check,
            timeout=timeout,
            env=cls.docker_environment,
        )

    def run_case(self, mode: int) -> tuple[str, str, int, str, int]:
        case = self.root / f"case-{mode:o}"
        case.mkdir(mode=0o700)
        synthetic = case / "synthetic.secret"
        synthetic_value = b"p02-synthetic-compose-secret"
        synthetic.write_bytes(synthetic_value + b"\n")
        synthetic.chmod(mode)
        source_stat = synthetic.stat()
        self.assertEqual(self.host_uid, source_stat.st_uid)
        self.assertEqual(self.host_gid, source_stat.st_gid)
        project = f"hyp02secret{mode:o}{os.getpid()}{secrets.token_hex(2)}"
        container = project + "-probe"
        script = """set -u
printf '%s\n' 'previous-safe-acl' > /run/valkey/users.acl
chmod 0600 /run/valkey/users.acl
stat -c '%u:%g:%a:%h' /run/secrets/synthetic > /run/valkey/metadata
printf '%s:%s:' "$(id -u)" "$(id -g)" > /run/valkey/process-identity
id -G >> /run/valkey/process-identity
if /bin/sh /fixture/render-monitor-acl.sh /run/secrets/synthetic /run/valkey/users.acl >/dev/null 2>&1; then
  rc=0
else
  rc=$?
fi
printf '%s\n' "$${rc}" > /run/valkey/renderer-exit
sha256sum /run/valkey/users.acl | cut -d' ' -f1 > /run/valkey/output-digest
find /run/valkey -maxdepth 1 -name 'users.acl.*' | wc -l > /run/valkey/temp-count
touch /run/valkey/ready
exec sleep 300
"""
        compose = {
            "services": {
                "probe": {
                    "image": self.image_id,
                    "pull_policy": "never",
                    "container_name": container,
                    "user": "999:999",
                    "group_add": [str(self.host_gid)],
                    "network_mode": "none",
                    "read_only": True,
                    "cap_drop": ["ALL"],
                    "security_opt": ["no-new-privileges:true"],
                    "cpus": 1,
                    "mem_limit": "128m",
                    "pids_limit": 64,
                    "stop_grace_period": "1s",
                    "secrets": ["synthetic"],
                    "volumes": [f"{RENDERER}:/fixture/render-monitor-acl.sh:ro"],
                    "tmpfs": [
                        "/run/valkey:rw,noexec,nosuid,nodev,mode=0700,uid=999,gid=999"
                    ],
                    "command": ["/bin/sh", "-c", script],
                }
            },
            "secrets": {"synthetic": {"file": str(synthetic)}},
        }
        compose_path = case / "compose.yml"
        compose_path.write_text(yaml.safe_dump(compose, sort_keys=False))
        compose_args = (
            "compose",
            "--project-directory",
            str(case),
            "-p",
            project,
            "-f",
            str(compose_path),
        )
        try:
            started = self.docker(
                *compose_args,
                "up",
                "-d",
                "--no-build",
                "--pull",
                "never",
                timeout=120,
                check=False,
            )
            self.assertEqual(0, started.returncode, started.stderr)
            for _ in range(100):
                ready = self.docker(
                    "exec",
                    container,
                    "test",
                    "-f",
                    "/run/valkey/ready",
                    check=False,
                )
                if ready.returncode == 0:
                    break
                time.sleep(0.05)
            else:
                raise AssertionError("synthetic secret probe did not become ready")

            def read_result(name: str) -> str:
                result = self.docker(
                    "exec", container, "cat", f"/run/valkey/{name}", check=False
                )
                self.assertEqual(0, result.returncode, name)
                return result.stdout.strip()

            return (
                read_result("metadata"),
                read_result("process-identity"),
                int(read_result("renderer-exit")),
                read_result("output-digest"),
                int(read_result("temp-count")),
            )
        finally:
            self.docker(
                *compose_args,
                "down",
                "--remove-orphans",
                "--volumes",
                check=False,
                timeout=120,
            )

    def test_group_readable_secret_succeeds_and_unsafe_modes_fail_closed(self) -> None:
        previous_digest = hashlib.sha256(b"previous-safe-acl\n").hexdigest()
        secret_digest = hashlib.sha256(b"p02-synthetic-compose-secret").hexdigest()
        expected_acl = f"user default reset on #{secret_digest} ~* &* +@all\n".encode()
        success_digest = hashlib.sha256(expected_acl).hexdigest()
        for mode, should_succeed in (
            (0o640, True),
            (0o400, False),
            (0o644, False),
            (0o444, False),
        ):
            with self.subTest(mode=oct(mode)):
                metadata, identity, renderer_exit, output_digest, temp_count = (
                    self.run_case(mode)
                )
                self.assertEqual(
                    f"{self.host_uid}:{self.host_gid}:{mode:o}:1", metadata
                )
                process_uid, process_gid, process_groups = identity.split(":", 2)
                self.assertEqual("999", process_uid)
                self.assertEqual("999", process_gid)
                self.assertIn("999", process_groups.split())
                self.assertIn(str(self.host_gid), process_groups.split())
                self.assertEqual(0, temp_count)
                if should_succeed:
                    self.assertEqual(0, renderer_exit)
                    self.assertEqual(success_digest, output_digest)
                else:
                    self.assertNotEqual(0, renderer_exit)
                    self.assertEqual(previous_digest, output_digest)


if __name__ == "__main__":
    unittest.main()
