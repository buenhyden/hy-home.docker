"""Synthetic, source-only checks for mng-valkey ACL generation."""

from __future__ import annotations

import hashlib
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = (
    Path(__file__).resolve().parents[2]
    / "infra/04-data/mng-db/valkey/scripts/render-acl.sh"
)


class MngValkeyAclTests(unittest.TestCase):
    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory()
        self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name)
        (self.root / "default").write_text("synthetic-default\n", encoding="utf-8")
        (self.root / "inspector").write_text("synthetic-inspector\n", encoding="utf-8")

    def render(self) -> subprocess.CompletedProcess[str]:
        env = {
            **os.environ,
            "MNG_VALKEY_DEFAULT_SECRET_FILE": str(self.root / "default"),
            "MNG_VALKEY_INSPECTOR_SECRET_FILE": str(self.root / "inspector"),
            "MNG_VALKEY_ACL_FILE": str(self.root / "users.acl"),
        }
        return subprocess.run(
            ["sh", str(SCRIPT)], env=env, capture_output=True, text=True, check=False
        )

    def test_default_user_keeps_shared_secret_and_inspector_is_read_only(self) -> None:
        result = self.render()
        self.assertEqual(result.returncode, 0, result.stderr)
        acl = (self.root / "users.acl").read_text(encoding="utf-8")
        default = hashlib.sha256(b"synthetic-default").hexdigest()
        inspector = hashlib.sha256(b"synthetic-inspector").hexdigest()
        self.assertEqual(
            acl,
            f"user default on #{default} ~* &* +@all\n"
            f"user mnginspector on #{inspector} ~* resetchannels -@all +@read "
            "+@connection -@dangerous +info\n",
        )
        self.assertNotIn("synthetic-", acl)
        self.assertEqual((self.root / "users.acl").stat().st_mode & 0o777, 0o600)

    def test_inspector_cannot_share_the_default_secret(self) -> None:
        (self.root / "inspector").write_text("synthetic-default\n", encoding="utf-8")
        result = self.render()
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.root / "users.acl").exists())

    def test_missing_or_multiline_secret_fails_closed(self) -> None:
        for content in (None, "a\nb\n", "\n"):
            with self.subTest(content=content):
                path = self.root / "inspector"
                if content is None:
                    path.unlink(missing_ok=True)
                else:
                    path.write_text(content, encoding="utf-8")
                result = self.render()
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse((self.root / "users.acl").exists())

    def test_compose_replaces_requirepass_with_the_rendered_acl(self) -> None:
        compose = (SCRIPT.parents[2] / "docker-compose.yml").read_text(encoding="utf-8")
        self.assertNotIn("--requirepass", compose)
        self.assertIn("/usr/local/libexec/mng-valkey/start.sh", compose)
        self.assertIn("/run/valkey:uid=999,gid=999,mode=0700", compose)


if __name__ == "__main__":
    unittest.main()
