"""Static contract for the host-owned OpenBao audit rotation rule."""

import os
import shlex
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RULE = ROOT / "infra/03-security/openbao/config/logrotate/openbao"
COMPOSE = ROOT / "infra/03-security/openbao/docker-compose.yml"
CONTAINER_ID = "a" * 64


class AuditRotationContract(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        directory = Path(self.temporary.name)
        self.calls = directory / "calls"
        self.docker = directory / "docker"
        self.docker.write_text(
            """#!/bin/sh
printf '%s\n' "$*" >> "$FAKE_DOCKER_CALLS"
if [ "$1" = inspect ]; then
    [ "$FAKE_DOCKER_MODE" != inspect-failure ] || exit 42
    case "$3" in
        *'{{.Id}}'*) printf '%s\n' "$FAKE_DOCKER_ID" ;;
        *)
            if [ "$FAKE_DOCKER_MODE" = bad-labels ]; then
                printf '%s\n' 'true other-project openbao'
            else
                printf '%s\n' 'true hy-home-infra openbao'
            fi
            ;;
    esac
elif [ "$1" = kill ]; then
    exit 0
else
    exit 64
fi
"""
        )
        self.docker.chmod(0o700)

    def tearDown(self):
        self.temporary.cleanup()

    def run_postrotate(self, mode="good", container_id=CONTAINER_ID):
        text = RULE.read_text()
        body = text.split("    postrotate\n", 1)[1].split("    endscript\n", 1)[0]
        body = body.replace("/usr/bin/docker", shlex.quote(str(self.docker)))
        environment = {
            **os.environ,
            "FAKE_DOCKER_CALLS": str(self.calls),
            "FAKE_DOCKER_ID": container_id,
            "FAKE_DOCKER_MODE": mode,
        }
        result = subprocess.run(
            ["/bin/sh", "-c", body],
            env=environment,
            capture_output=True,
            text=True,
            check=False,
        )
        calls = self.calls.read_text().splitlines() if self.calls.exists() else []
        return result, calls

    def test_good_identity_signals_the_captured_full_id(self):
        result, calls = self.run_postrotate()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(calls[-1], f"kill --signal=HUP {CONTAINER_ID}")

    def test_bad_labels_do_not_signal(self):
        result, calls = self.run_postrotate("bad-labels")
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(any(call.startswith("kill ") for call in calls))

    def test_inspect_failure_does_not_signal(self):
        result, calls = self.run_postrotate("inspect-failure")
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(any(call.startswith("kill ") for call in calls))

    def test_invalid_full_id_does_not_signal(self):
        for container_id in ("a" * 63, "g" * 64):
            with self.subTest(container_id=container_id):
                result, calls = self.run_postrotate(container_id=container_id)
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse(any(call.startswith("kill ") for call in calls))
                self.calls.unlink()

    def test_name_replacement_still_signals_the_original_id(self):
        result, calls = self.run_postrotate("replacement")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(calls[-1], f"kill --signal=HUP {CONTAINER_ID}")
        self.assertEqual(calls[-2].split()[-1], CONTAINER_ID)

    def test_rotation_is_bounded_and_lossless(self):
        text = RULE.read_text()
        directives = {line.strip() for line in text.splitlines()}
        self.assertTrue(
            text.startswith(
                "/home/hyunyoun/storage/volumes/security/openbao/audit/audit.json {"
            )
        )
        self.assertTrue(
            {
                "daily",
                "maxsize 256M",
                "rotate 14",
                "su dhcpcd hyunyoun",
                "create 0600 dhcpcd hyunyoun",
                "nocopytruncate",
                "compress",
                "delaycompress",
            }.issubset(directives)
        )
        self.assertNotIn("copytruncate", directives)

    def test_rotation_target_matches_the_compose_audit_device(self):
        compose = COMPOSE.read_text()
        self.assertIn("container_name: openbao", compose)
        self.assertIn('"file_path":"/openbao/audit/audit.json"', compose)
