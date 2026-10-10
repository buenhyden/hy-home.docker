"""Source contracts for the reviewed SEC01 candidate; no deployment receipt."""

import json
import re
import subprocess
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
OPENBAO = "openbao/openbao:2.7.1@sha256:6d2b93856e3fcf7b18ad855a0b51eaba474dc8b79cf554379ea32034797d2acf"


class CandidateContract(unittest.TestCase):
    def test_oauth_hardening_admits_only_equal_stable_digest_build_sources(self):
        checker = (ROOT / "scripts/hardening/check-all-hardening.sh").read_text()
        start = checker.index("  local oauth_source_image oauth_dev_source_image")
        end = checker.index('  check_contains "$oauth_dockerfile"', start)
        section = checker[start:end]
        probe = (
            "fail() { exit 1; }\n"
            'validate_sources() { local oauth_dockerfile="$1" oauth_dev_dockerfile="$2"\n'
            + section
            + '\n}\nvalidate_sources "$@"\n'
        )
        image = "quay.io/oauth2-proxy/oauth2-proxy:v7.15.5@sha256:" + "a" * 64
        rejected = (
            image[:-1],
            image.replace("v7.15.5", "latest"),
            image.replace("v7.15.5", "v7.15.5-rc1"),
            image.replace("a" * 64, "A" * 64),
            image.split("@")[0],
        )
        with tempfile.TemporaryDirectory() as temporary:
            production, development = [
                Path(temporary) / name for name in ("Dockerfile", "dev.Dockerfile")
            ]
            for left, right, expected in (
                (image, image, 0),
                (image, image.replace("7.15.5", "7.15.4"), 1),
                *((bad, bad, 1) for bad in rejected),
            ):
                with self.subTest(left=left, right=right):
                    production.write_text(f"FROM {left} AS src\n")
                    development.write_text(f"FROM {right} AS src\n")
                    result = subprocess.run(
                        [
                            "/bin/bash",
                            "-c",
                            probe,
                            "bash",
                            str(production),
                            str(development),
                        ],
                        env={"PATH": "/usr/bin:/bin", "LC_ALL": "C"},
                        capture_output=True,
                        check=False,
                        timeout=5,
                    )
                    self.assertEqual(result.returncode, expected)

    def test_server_agent_and_backup_share_candidate(self):
        compose = yaml.safe_load(
            (ROOT / "infra/03-security/openbao/docker-compose.yml").read_text()
        )
        for name in ("openbao", "openbao-agent"):
            self.assertEqual(compose["services"][name]["image"], OPENBAO)
        backup = (
            ROOT / "infra/09-platform-ops/restic/bin/hyhome-backup.sh"
        ).read_text()
        self.assertIn("docker exec -i openbao sh -ec", backup)
        self.assertIn("bao operator raft snapshot save", backup)
        config = json.loads(
            compose["services"]["openbao"]["environment"]["BAO_LOCAL_CONFIG"]
        )
        self.assertEqual(list(config["storage"]), ["raft"])
        self.assertFalse(config["listener"][0]["tcp"]["tls_disable"])
        self.assertEqual(config["audit"][0]["options"]["log_raw"], "false")

    def test_grafana_and_ollama_candidates_keep_runtime_controls(self):
        compose = yaml.safe_load(
            (ROOT / "infra/06-observability/docker-compose.yml").read_text()
        )
        self.assertEqual(
            compose["services"]["grafana"]["image"],
            "grafana/grafana:13.2.3@sha256:b28bae15e219c998fb0e0424ed724930cc61b1f61fb404d47c862f9a23f9e572",
        )
        compose = yaml.safe_load(
            (ROOT / "infra/08-ai/ollama/docker-compose.yml").read_text()
        )
        ollama = compose["services"]["ollama"]
        self.assertEqual(
            ollama["image"],
            "ollama/ollama:0.40.2@sha256:b86366bb528bbf7f1424435d165028497a5b69bf6ddb4fa5a87102e2b79f44fb",
        )
        self.assertIn("OLLAMA_NO_CLOUD=1", ollama["environment"])
        self.assertEqual(
            ollama["deploy"]["resources"]["reservations"]["devices"][0]["count"], 1
        )

    def test_home_image_managers_exclude_lab(self):
        config = json.loads((ROOT / "renovate.json5").read_text())
        patterns = config["docker-compose"]["managerFilePatterns"]

        def matches(path):
            return any(re.search(pattern[1:-1], path) for pattern in patterns)

        self.assertTrue(matches("infra/04-data/dev-db/docker-compose.yml"))
        self.assertTrue(matches("infra/03-security/openbao/docker-compose.yml"))
        self.assertFalse(matches("labs/comfyui.yml"))
        self.assertIn("labs/**", config["ignorePaths"])


if __name__ == "__main__":
    unittest.main()
