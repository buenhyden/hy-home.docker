"""The whole-stack Compose start guard among the hookify rules."""

from __future__ import annotations

import unittest
from pathlib import Path

from scripts.hooks import hook_rules

ROOT = Path(__file__).resolve().parents[3]
RULE = "block-whole-stack-compose-start"


def blocked(command: str) -> bool:
    _, blocks = hook_rules.evaluate(hook_rules.load_rules(ROOT), command=command)
    return RULE in {rule.name for rule in blocks}


class WholeStackComposeStartTests(unittest.TestCase):
    def test_an_all_profile_start_is_blocked(self) -> None:
        for command in (
            "docker compose --profile '*' up -d",
            'docker compose --profile "*" up',
            "docker compose --profile=* up -d",
            "docker compose --profile \\* create",
            "docker compose --env-file .env --profile '*' start",
            "docker-compose --profile '*' up -d",
            "cd infra && docker compose --profile '*' up -d",
            "COMPOSE_PROFILES='*' docker compose up -d",
            "COMPOSE_PROFILES=core,* docker compose up -d",
            "export COMPOSE_PROFILES='*'; docker compose up -d",
            "docker compose -f labs/cassandra/docker-compose.yml --profile '*' up -d",
        ):
            with self.subTest(command=command):
                self.assertTrue(blocked(command))

    def test_rendering_and_named_starts_pass(self) -> None:
        for command in (
            "docker compose --profile '*' config --services",
            "docker compose --env-file .env.example --profile '*' config --quiet",
            "docker compose --profile core up -d keycloak",
            "COMPOSE_PROFILES=core docker compose up -d",
            "docker compose up -d",
            "docker compose --profile '*' ps",
            "grep -n \"--profile '*'\" docs/README.md",
        ):
            with self.subTest(command=command):
                self.assertFalse(blocked(command))


if __name__ == "__main__":
    unittest.main()
