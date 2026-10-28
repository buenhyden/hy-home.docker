"""Source contracts for the reviewed SEC01 candidate; no deployment receipt."""

import json
import re
import subprocess
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
OPENBAO = "hy-home/openbao:2.7.1-go1.27.3-net0.60.0-r1@sha256:a58fb1109971e506e9de1a360aec48ae07af7b6ccf409f8bac329e30e8fde8c8"

PATCH_STABLE_IMAGES = {
    (
        "infra/06-observability/dozzle/docker-compose.yml",
        "dozzle",
    ): "amir20/dozzle:v11.3.1@sha256:ba65da5af3d2147cfc2ee68ea5a6e35b75d2dff7eeff226151a65c9d77831c02",
    (
        "infra/11-quality/mailpit/docker-compose.yml",
        "mailpit",
    ): "axllent/mailpit:v1.31.5@sha256:94f6b70c1436defae6799d9ac7ff0eeff9540465b842026d5cdb018f1c0234ea",
    (
        "infra/08-ai/ollama/docker-compose.yml",
        "ollama",
    ): "ollama/ollama:0.40.12@sha256:20d1bbfbabe1c97ba4b16301f08a20d8484bcf77047742a3cb71c613d8e12d0b",
    (
        "infra/09-platform-ops/renovate/docker-compose.yml",
        "renovate",
    ): "renovate/renovate:44.151.3-full@sha256:14d0b748ed59c05e1ab64aa325b4f3b07f78c809ca513b86b3b96b0c41426ea1",
    (
        "infra/11-quality/sonarqube/docker-compose.yml",
        "sonarqube",
    ): "sonarqube:26.10.0.133078-community@sha256:0b3408443fb6a311253de27941b10977c9b977fd53be2265947bfe14161308b8",
    (
        "infra/10-communication/stalwart/docker-compose.yml",
        "stalwart",
    ): "stalwartlabs/stalwart:v0.16.27@sha256:c429b311c93db5606598abc1c68225a85a6953183848ae01bee9c6a98885836c",
    (
        "labs/supabase.yml",
        "imgproxy",
    ): "darthsim/imgproxy:v4.0.17@sha256:db0b4b9cd690c8b3590203dea300fb759a18c4ec2af7b37424f0bdef23ce317d",
}

OPEN_WEBUI = "ghcr.io/open-webui/open-webui:v0.12.0-cuda@sha256:3a4f953b604bf8b4df9eaa765278f75180911f180cbdf984b2e7b593891e1c25"


class CandidateContract(unittest.TestCase):
    def test_dozzle_docker_control_plane_is_explicitly_locked_down(self):
        compose = yaml.safe_load(
            (ROOT / "infra/06-observability/dozzle/docker-compose.yml").read_text(
                encoding="utf-8"
            )
        )
        environment = compose["services"]["dozzle"]["environment"]
        expected_controls = {
            "DOZZLE_ENABLE_ACTIONS": "false",
            "DOZZLE_ENABLE_SHELL": "false",
            "DOZZLE_ENABLE_MCP": "false",
            "DOZZLE_AUTO_UPDATE": "off",
            "DOZZLE_UPDATE_CONTAINERS": "off",
            "DOZZLE_RELEASE_CHECK_MODE": "manual",
            "DOZZLE_IMAGE_CHECK_MODE": "off",
            "DOZZLE_DISABLE_SETUP_WIZARD": "true",
        }
        self.assertEqual(
            expected_controls,
            {key: environment.get(key) for key in expected_controls},
        )

    def test_patch_stable_images_use_reviewed_exact_index_digests(self):
        for (path, service), expected in PATCH_STABLE_IMAGES.items():
            with self.subTest(path=path, service=service):
                compose = yaml.safe_load((ROOT / path).read_text(encoding="utf-8"))
                self.assertEqual(compose["services"][service]["image"], expected)

        stalwart_compose = yaml.safe_load(
            (ROOT / "infra/10-communication/stalwart/docker-compose.yml").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(
            stalwart_compose["services"]["stalwart-config"]["image"],
            "hy-home/stalwart-config:0.16.27-cli1.0.13-local",
        )
        dockerfile = (
            ROOT / "infra/10-communication/stalwart/config/Dockerfile"
        ).read_text(encoding="utf-8")
        stalwart_image = PATCH_STABLE_IMAGES[
            ("infra/10-communication/stalwart/docker-compose.yml", "stalwart")
        ]
        self.assertIn(f"FROM {stalwart_image}", dockerfile)

    def test_openwebui_minor_refresh_keeps_exact_cuda_variant(self):
        compose = yaml.safe_load(
            (ROOT / "infra/08-ai/open-webui/docker-compose.yml").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(compose["services"]["open-webui"]["image"], OPEN_WEBUI)

    def test_opensearch_root_args_keep_lab_default_pair_unchanged(self):
        package = ROOT / "infra/04-data/opensearch"
        dockerfile = (package / "Dockerfile").read_text()
        self.assertIn(
            "ARG OPENSEARCH_BASE_IMAGE=opensearchproject/opensearch:3.8.0\n"
            "FROM ${OPENSEARCH_BASE_IMAGE}",
            dockerfile,
        )
        self.assertIn("ARG OPENSEARCH_EXPORTER_VERSION=3.8.0.0", dockerfile)
        exporter_arg = dockerfile.index("ARG OPENSEARCH_EXPORTER_VERSION=")
        exporter_url = dockerfile.index(
            "/releases/download/${OPENSEARCH_EXPORTER_VERSION}/"
        )
        self.assertLess(dockerfile.index("FROM "), exporter_arg)
        self.assertLess(exporter_arg, exporter_url)
        self.assertIn(
            "prometheus-exporter-${OPENSEARCH_EXPORTER_VERSION}.zip", dockerfile
        )
        for plugin in (
            "ingest-attachment",
            "analysis-nori",
            "mapper-annotated-text",
            "mapper-murmur3",
            "mapper-size",
        ):
            self.assertIn(plugin, dockerfile)
        self.assertIn("USER 1000", dockerfile)
        self.assertIn('test "$(id -u opensearch)" = "1000"', dockerfile)

    def test_opensearch_root_selection_does_not_override_lab_builds(self):
        package = ROOT / "infra/04-data/opensearch"
        dashboards = "opensearchproject/opensearch-dashboards:3.9.0@sha256:4bdb8ded547ce7f4c379a10261f1b4aad58726900c215be570a7d1fe86f2a7d8"
        root = yaml.safe_load((package / "docker-compose.yml").read_text())
        lab = yaml.safe_load((ROOT / "labs/opensearch-cluster.yml").read_text())
        self.assertEqual(dashboards, root["services"]["opensearch-dashboards"]["image"])
        self.assertEqual(
            {
                "OPENSEARCH_BASE_IMAGE": "opensearchproject/opensearch:3.9.0@sha256:adfa61f85025d06b4aeb562e7e74fde7e31c437039c93c3862c17e9acebd6c7c",
                "OPENSEARCH_EXPORTER_VERSION": "3.9.0.0",
            },
            root["services"]["opensearch"]["build"]["args"],
        )
        self.assertEqual(
            "opensearchproject/opensearch-dashboards:3.8.0",
            lab["services"]["lab-opensearch-dashboards"]["image"],
        )
        lab_builds = [
            service["build"]
            for service in lab["services"].values()
            if "build" in service
        ]
        self.assertEqual(3, len(lab_builds))
        for build in lab_builds:
            self.assertNotIn("args", build)
            self.assertEqual("Dockerfile", build["dockerfile"])
        entrypoint = (package / "opensearch/opensearch-entrypoint.sh").read_text()
        self.assertIn("-env OPENSEARCH_HASH_PASSWORD", entrypoint)
        self.assertIn(
            "exec /usr/share/opensearch/opensearch-docker-entrypoint.sh", entrypoint
        )

    def test_trino_candidate_uses_official_launcher_and_keeps_secret_boundary(self):
        service = yaml.safe_load(
            (ROOT / "infra/12-analytics/trino/docker-compose.yml").read_text()
        )["services"]["trino"]
        self.assertEqual(
            "trinodb/trino:484@sha256:2704eb53935af5e582d63d6033e9bf99d20c325e9b0e30b1016ef59a4773979f",
            service["image"],
        )
        self.assertEqual(
            ["/usr/lib/trino/bin/launcher", "run", "--etc-dir", "/etc/trino"],
            service["command"],
        )
        self.assertEqual(
            ["/bin/bash", "/opt/hyhome/hyhome-trino.sh"], service["entrypoint"]
        )
        self.assertEqual(["seaweedfs_s3_lakehouse_secret_key"], service["secrets"])
        self.assertIn(
            "./hyhome-trino.sh:/opt/hyhome/hyhome-trino.sh:ro", service["volumes"]
        )
        self.assertTrue(all(port.startswith("127.0.0.1:") for port in service["ports"]))
        self.assertEqual("template-infra-readonly-high", service["extends"]["service"])

    def test_surrealdb_pins_the_same_v2_artifact_without_changing_wrapper(self):
        package = ROOT / "infra/08-ai/open-notebook/surrealdb"
        dockerfile = (package / "Dockerfile").read_text()
        self.assertIn(
            "FROM surrealdb/surrealdb:v2.7.0@sha256:e5d7387e3727bbe2f7cd6d869e48cd34777272258572ead37c9656b25f745723 AS surreal",
            dockerfile,
        )
        self.assertIn("FROM debian:bookworm-slim", dockerfile)
        self.assertIn("COPY --from=surreal /surreal /usr/local/bin/surreal", dockerfile)
        self.assertIn('ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]', dockerfile)

    def registry_component_result(self, registry, *arguments):
        checker = (ROOT / "scripts/hardening/check-all-hardening.sh").read_text()
        start = checker.index("registry_component_image() {")
        end = checker.index("compose_service_image() {", start)
        probe = (
            checker[start:end]
            + '\nTECH_STACK_REGISTRY="$1"\nshift\nregistry_component_image "$@"\n'
        )
        with tempfile.TemporaryDirectory() as temporary:
            registry_path = Path(temporary) / "registry.json"
            registry_path.write_text(json.dumps(registry))
            return subprocess.run(
                ["/bin/bash", "-c", probe, "bash", str(registry_path), *arguments],
                env={"PATH": "/usr/bin:/bin", "LC_ALL": "C"},
                capture_output=True,
                text=True,
                check=False,
                timeout=5,
            )

    def test_registry_component_image_can_select_one_exact_compose_source(self):
        root_image = "oliver006/redis_exporter:v1.93.0-alpine"
        lab_image = "oliver006/redis_exporter:v1.91.1-alpine"
        root_source = "infra/02-auth/oauth2-proxy/docker-compose.yml"
        lab_source = "labs/valkey-cluster.yml"

        def registry(images, sources):
            return {
                "entries": [
                    {
                        "component": "Valkey Exporter",
                        "images": images,
                        "sources": sources,
                    }
                ]
            }

        valid_sources = (
            {"compose_file": root_source, "images": [root_image]},
            {"compose_file": lab_source, "images": [lab_image]},
        )
        selected = self.registry_component_result(
            registry([root_image, lab_image], valid_sources),
            "Valkey Exporter",
            root_source,
        )
        self.assertEqual(
            (selected.returncode, selected.stdout.strip()), (0, root_image)
        )
        self.assertNotEqual(
            self.registry_component_result(
                registry([root_image, lab_image], valid_sources), "Valkey Exporter"
            ).returncode,
            0,
        )
        legacy = self.registry_component_result(
            registry([root_image], valid_sources[:1]), "Valkey Exporter"
        )
        self.assertEqual((legacy.returncode, legacy.stdout.strip()), (0, root_image))
        rejected = (
            (
                registry([root_image, lab_image], valid_sources),
                "unknown/docker-compose.yml",
            ),
            (
                registry([root_image, lab_image], (*valid_sources, valid_sources[0])),
                root_source,
            ),
            (registry([root_image, root_image], valid_sources[:1]), root_source),
            (
                registry(
                    [root_image],
                    ({"compose_file": root_source, "images": [lab_image]},),
                ),
                root_source,
            ),
            (
                registry(
                    [root_image],
                    ({"compose_file": root_source, "images": [root_image, lab_image]},),
                ),
                root_source,
            ),
            (
                registry(
                    [root_image],
                    (
                        {
                            "compose_file": "../docker-compose.yml",
                            "images": [root_image],
                        },
                    ),
                ),
                root_source,
            ),
            (registry([root_image], valid_sources[:1]), "../docker-compose.yml"),
            (registry([root_image], valid_sources[:1]), "/infra/docker-compose.yml"),
            (registry([root_image], valid_sources[:1]), ""),
        )
        for fixture, source in rejected:
            with self.subTest(source=source, fixture=fixture):
                self.assertNotEqual(
                    self.registry_component_result(
                        fixture, "Valkey Exporter", source
                    ).returncode,
                    0,
                )
        for arguments in ((), ("Valkey Exporter", root_source, "extra")):
            self.assertNotEqual(
                self.registry_component_result(
                    registry([root_image], valid_sources[:1]), *arguments
                ).returncode,
                0,
            )
        checker = (ROOT / "scripts/hardening/check-all-hardening.sh").read_text()
        self.assertIn(
            'registry_component_image "Valkey Exporter" "infra/02-auth/oauth2-proxy/docker-compose.yml"',
            checker,
        )

    def test_oauth_exporter_check_rejects_two_failed_image_lookups(self):
        checker = (ROOT / "scripts/hardening/check-all-hardening.sh").read_text()
        functions_start = checker.index("registry_component_image() {")
        functions_end = checker.index(
            "resolve_compose_service_image_cli() {", functions_start
        )
        check_start = checker.index(
            '  if [[ "$oauth_valkey_compose_image" != "$valkey_image" ]]; then'
        )
        check_end = checker.index(
            '  check_service_network "$oauth_full_compose" "oauth2-proxy-valkey"',
            check_start,
        )
        probe = (
            "FAILURES=0\n"
            "fail() { FAILURES=$((FAILURES + 1)); }\n"
            + checker[functions_start:functions_end]
            + "\nvalidate_exporter() {\n"
            + '  local oauth_full_compose="$1"\n'
            + '  local valkey_image="unchanged"\n'
            + '  local oauth_valkey_compose_image="unchanged"\n'
            + checker[check_start:check_end]
            + "  (( FAILURES > 0 ))\n"
            + "}\n"
            + 'TECH_STACK_REGISTRY="$2"\n'
            + 'validate_exporter "$1"\n'
        )
        registry = {
            "entries": [
                {
                    "component": "Valkey Exporter",
                    "images": ["oliver006/redis_exporter:v1.93.0-alpine"],
                    "sources": [
                        {
                            "compose_file": "somewhere/else/docker-compose.yml",
                            "images": ["oliver006/redis_exporter:v1.93.0-alpine"],
                        }
                    ],
                }
            ]
        }
        with tempfile.TemporaryDirectory() as temporary:
            fixture_dir = Path(temporary)
            compose_path = fixture_dir / "docker-compose.yml"
            registry_path = fixture_dir / "registry.json"
            compose_path.write_text("services:\n  unrelated:\n    image: busybox:1.0\n")
            registry_path.write_text(json.dumps(registry))
            result = subprocess.run(
                [
                    "/bin/bash",
                    "-c",
                    probe,
                    "bash",
                    str(compose_path),
                    str(registry_path),
                ],
                env={"PATH": "/usr/bin:/bin", "LC_ALL": "C"},
                capture_output=True,
                text=True,
                check=False,
                timeout=5,
            )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertGreaterEqual(result.stderr.count("FAIL:"), 2)

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
        runbook = (
            ROOT
            / "docs/05.operations/runbooks/04-security-and-secrets/0105-openbao-maintenance-window.md"
        ).read_text()
        image_arguments = re.findall(
            r"(?:openbao/openbao|hy-home/openbao):[^\s]+@sha256:[0-9a-f]{64}",
            runbook,
        )
        # The restart step reads the image from Compose; check-tls-material names it.
        self.assertEqual([OPENBAO], image_arguments)
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
            "grafana/grafana:13.2.4@sha256:dbbc38ea21103cefb50396340cd88afec779c7e070b0a7bf5a75b4ce46651d3f",
        )
        compose = yaml.safe_load(
            (ROOT / "infra/08-ai/ollama/docker-compose.yml").read_text()
        )
        ollama = compose["services"]["ollama"]
        self.assertEqual(
            ollama["image"],
            PATCH_STABLE_IMAGES[("infra/08-ai/ollama/docker-compose.yml", "ollama")],
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
