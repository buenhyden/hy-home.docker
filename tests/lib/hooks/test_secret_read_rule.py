"""The secret content read guard among the hookify rules."""

from __future__ import annotations

import unittest
from pathlib import Path

from scripts.hooks import hook_rules

ROOT = Path(__file__).resolve().parents[3]
RULE = "block-secret-content-read"


def blocked(command: str) -> bool:
    _, blocks = hook_rules.evaluate(hook_rules.load_rules(ROOT), command=command)
    return RULE in {rule.name for rule in blocks}


class SecretContentReadTests(unittest.TestCase):
    def test_reading_secret_or_env_content_is_blocked(self) -> None:
        for command in (
            "cat secrets/db/mng-pg/password.txt",
            "head -n1 ./secrets/auth/token",
            "cd infra && cat ../secrets/a/b.txt",
            "sudo cat /srv/app/secrets/token",
            "base64 secrets/k.pem",
            "x=$(cat secrets/t)",
            "while read l; do echo $l; done < secrets/x.txt",
            "grep -n KEY .env",
            "sed -n 1p /home/u/repo/.env",
            "less .env.local",
            "source .env && echo done",
            "tail infra/app/.env",
            "echo ok\ncat secrets/db/x.txt",
            "grep -rn . secrets",
            "rg -uu TOKEN secrets/",
            "grep -E 'KEY|TOKEN' .env",
            "awk 'BEGIN{FS=\"=\"};{print $2}' .env",
            "sed -n '1p;2p' secrets/x",
            "LC_ALL=C cat .env",
            "env cat .env",
            "timeout 5 cat .env",
            "if true; then cat .env; fi",
            "{ cat .env; }",
            "vim -es '+%p' '+q!' .env",
            "paste .env",
            "cat prod.env",
        ):
            with self.subTest(command=command):
                self.assertTrue(blocked(command))

    def test_metadata_and_unrelated_reads_pass(self) -> None:
        for command in (
            "ls secrets/",
            "ls -la secrets/db",
            "find secrets -type f -name '*.txt'",
            "git ls-files secrets",
            "stat secrets/db/x.txt",
            "test -s secrets/db/x.txt",
            "wc -c secrets/db/x.txt",
            "cat .env.example",
            "cat infra/app/.env.example",
            "grep -rn '.env' docs",
            "grep -rn 'secrets/' docs/README.md",
            "cat docs/secrets-policy.md",
            "docker compose --env-file .env config --services",
            "echo secrets/x",
            "head x.env.example",
            "diff .env.example infra/a/.env.example",
            "sed -i 's/.env/.env.local/' docs/x.md",
            "grep -rn 'secrets' docs",
            "python3 scripts/operations/lab.py --env-file labs/.env check x",
        ):
            with self.subTest(command=command):
                self.assertFalse(blocked(command))


if __name__ == "__main__":
    unittest.main()
