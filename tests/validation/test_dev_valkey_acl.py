"""Synthetic, source-only checks for dev-valkey ACL generation."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[2] / "infra/04-data/dev-db/valkey/scripts/render-acl.sh"


class DevValkeyAclTests(unittest.TestCase):
    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory()
        self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name)
        self.secret_dir = self.root / "secrets"
        self.secret_dir.mkdir()
        (self.root / "admin").write_text("synthetic-admin\n", encoding="utf-8")
        (self.root / "projects.tsv").write_text("# empty\n", encoding="utf-8")

    def render(self) -> subprocess.CompletedProcess[str]:
        env = {
            **os.environ,
            "DEV_VALKEY_ADMIN_SECRET_FILE": str(self.root / "admin"),
            "DEV_VALKEY_PROJECTS_FILE": str(self.root / "projects.tsv"),
            "DEV_VALKEY_PROJECT_SECRETS_DIR": str(self.secret_dir),
            "DEV_VALKEY_ACL_FILE": str(self.root / "users.acl"),
        }
        return subprocess.run(
            ["sh", str(SCRIPT)], env=env, capture_output=True, text=True, check=False
        )

    def test_named_user_network_contract(self) -> None:
        config = (SCRIPT.parents[1] / "config/valkey.conf").read_text(encoding="utf-8")
        self.assertIn("protected-mode no", config)
        self.assertIn("bind 0.0.0.0", config)
        compose = (SCRIPT.parents[2] / "docker-compose.yml").read_text(encoding="utf-8")
        self.assertIn("dev_data_net: {}", compose)
        self.assertIn("user default off", SCRIPT.read_text(encoding="utf-8"))

    def test_empty_metadata_creates_admin_only_without_plaintext(self) -> None:
        result = self.render()
        self.assertEqual(result.returncode, 0, result.stderr)
        acl = (self.root / "users.acl").read_text(encoding="utf-8")
        digest = hashlib.sha256(b"synthetic-admin").hexdigest()
        self.assertEqual(acl, f"user default off\nuser devadmin on #{digest} ~* &* +@all\n")
        self.assertNotIn("synthetic-admin", acl)
        self.assertEqual((self.root / "users.acl").stat().st_mode & 0o777, 0o600)

    def test_project_user_is_limited_to_declared_prefix(self) -> None:
        (self.root / "projects.tsv").write_text(
            "project_a|project_a_runtime|project_a|project_a_password\n", encoding="utf-8"
        )
        (self.secret_dir / "project_a_password").write_text("synthetic-project\n", encoding="utf-8")
        result = self.render()
        self.assertEqual(result.returncode, 0, result.stderr)
        acl = (self.root / "users.acl").read_text(encoding="utf-8")
        digest = hashlib.sha256(b"synthetic-project").hexdigest()
        self.assertIn(
            f"user project_a_runtime on #{digest} ~project_a:* &project_a:* db=0 "
            "+@read +@write +@transaction +ping -@dangerous -@scripting -@pubsub "
            "-scan -clusterscan -keys -randomkey -dbsize -sort\n",
            acl,
        )
        self.assertNotIn("synthetic-project", acl)

    def test_bad_metadata_fails_closed_without_output(self) -> None:
        bad_rows = (
            "project_a|runtime|a|../escape\n",
            "project_a|default|a|secret\n",
            "project_a|runtime|a|secret|extra\n",
            "project_a|runtime|a|missing\n",
            "project_a|runtime|a|secret\nproject_b|runtime|b|secret\n",
            "project_a|runtime|same|secret\nproject_b|other|same|secret\n",
            "project_a|runtime|a|secret\nproject_b|other|b|secret\n",
        )
        (self.secret_dir / "secret").write_text("synthetic-project\n", encoding="utf-8")
        for row in bad_rows:
            with self.subTest(row=row):
                (self.root / "users.acl").unlink(missing_ok=True)
                (self.root / "projects.tsv").write_text(row, encoding="utf-8")
                result = self.render()
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse((self.root / "users.acl").exists())
                self.assertNotIn("synthetic-project", result.stderr)

    def test_multiline_secret_and_symlink_are_rejected(self) -> None:
        (self.root / "projects.tsv").write_text(
            "project_a|runtime|a|secret\n", encoding="utf-8"
        )
        secret = self.secret_dir / "secret"
        secret.write_text("first\nsecond\n", encoding="utf-8")
        self.assertNotEqual(self.render().returncode, 0)
        secret.unlink()
        secret.symlink_to(self.root / "admin")
        self.assertNotEqual(self.render().returncode, 0)


if __name__ == "__main__":
    unittest.main()
