"""SEC01 candidate source and synthetic wrapper evidence; runtime stays NOT_RUN."""

import json
import os
import re
import shutil
import subprocess
import tempfile
import tomllib
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
EXPORTER = "oliver006/redis_exporter:v1.93.0-alpine@sha256:93831cd4d5d67687de67c9d5221b14312fea580af8d157583ed9d4459bf2dd70"
EXPORTERS = (
    (
        "infra/04-data/mng-db/docker-compose.yml",
        "mng-valkey-exporter",
        "mng-valkey",
        True,
    ),
    (
        "infra/04-data/dev-db/docker-compose.yml",
        "dev-valkey-exporter",
        "dev-valkey",
        False,
    ),
)


def load(path):
    return yaml.safe_load((ROOT / path).read_text())


class NextStableCandidates(unittest.TestCase):
    def test_all_owned_exporters_use_same_immutable_alpine_candidate(self):
        for path, exporter_name, host, variable_port in EXPORTERS:
            with self.subTest(path=path):
                exporters = [
                    service
                    for service in load(path)["services"].values()
                    if "redis_exporter" in service.get("image", "")
                ]
                self.assertEqual(len(exporters), 1)
                service = exporters[0]
                self.assertEqual(service, load(path)["services"][exporter_name])
                self.assertEqual(service["image"], EXPORTER)
                self.assertEqual(service["entrypoint"], ["/bin/sh", "-c"])
                command = service["command"][0]
                self.assertIn("exec /redis_exporter", command)
                if variable_port:
                    self.assertIn("port=$${VALKEY_PORT}", command)
                    self.assertIn(f'redis://{host}:$$port"', command)
                else:
                    self.assertIn(f"-redis.addr=redis://{host}:6379", command)
                self.assertIn("-web.listen-address=:", command)
                self.assertNotIn("-redis.password=", command)
                self.assertTrue(service["secrets"])
                self.assertIn("/metrics", " ".join(service["healthcheck"]["test"]))

    @unittest.skipUnless(shutil.which("docker"), "docker compose CLI not available")
    def test_rendered_exporter_argv_tracks_listener_without_secret_argv(self):
        for selected_port in ("6379", "16379"):
            with tempfile.TemporaryDirectory(
                prefix="sec01-exporter-render-"
            ) as directory:
                temporary = Path(directory)
                env_file = temporary / "public.env"
                env_file.write_bytes(
                    (ROOT / ".env.example").read_bytes()
                    + f"\nVALKEY_PORT={selected_port}\n".encode("ascii")
                )
                result = subprocess.run(
                    [
                        "docker",
                        "compose",
                        "--project-directory",
                        str(ROOT),
                        "--env-file",
                        str(env_file),
                        "-f",
                        str(ROOT / "docker-compose.yml"),
                        "--profile",
                        "mng",
                        "--profile",
                        "dev-data",
                        "config",
                        "--format",
                        "json",
                    ],
                    cwd=ROOT,
                    env={
                        "COMPOSE_DISABLE_ENV_FILE": "1",
                        "DOCKER_CONFIG": str(temporary / "docker-config"),
                        "DOCKER_HOST": f"unix://{temporary / 'no-daemon.sock'}",
                        "LC_ALL": "C",
                        "PATH": os.environ["PATH"],
                    },
                    capture_output=True,
                    text=True,
                    check=False,
                    timeout=120,
                )
                self.assertEqual(0, result.returncode, result.stderr)
                services = json.loads(result.stdout)["services"]

                secret = temporary / "synthetic-secret"
                secret.write_text("synthetic-only\n", encoding="ascii")
                executable = temporary / "redis_exporter"
                executable.write_text(
                    "#!/usr/bin/python3\n"
                    "import json, os, sys\n"
                    "print(json.dumps({'password_in_env': "
                    "os.environ.get('REDIS_PASSWORD') == 'synthetic-only', "
                    "'args': sys.argv[1:]}))\n",
                    encoding="ascii",
                )
                executable.chmod(0o700)

                for _, exporter_name, host, variable_port in EXPORTERS:
                    with self.subTest(port=selected_port, exporter=exporter_name):
                        service = services[exporter_name]
                        command = " ".join(service["command"])
                        command = command.replace("/redis_exporter", str(executable))
                        command = re.sub(
                            r"/run/secrets/[A-Za-z0-9_]+", str(secret), command
                        ).replace("$$", "$")
                        environment = {
                            "LC_ALL": "C",
                            "PATH": "/usr/bin:/bin",
                            **{
                                key: str(value)
                                for key, value in service.get("environment", {}).items()
                            },
                        }
                        wrapped = subprocess.run(
                            ["/bin/sh", "-c", command],
                            cwd=ROOT,
                            env=environment,
                            capture_output=True,
                            text=True,
                            check=False,
                            timeout=5,
                        )
                        self.assertEqual(0, wrapped.returncode, wrapped.stderr)
                        evidence = json.loads(wrapped.stdout)
                        expected_port = selected_port if variable_port else "6379"
                        self.assertIn(
                            f"-redis.addr=redis://{host}:{expected_port}",
                            evidence["args"],
                        )
                        self.assertTrue(evidence["password_in_env"])
                        self.assertNotIn("synthetic-only", " ".join(evidence["args"]))
                        self.assertFalse(
                            any(
                                arg.startswith("-redis.password")
                                for arg in evidence["args"]
                            )
                        )

    def test_restricted_monitor_acl_options_remain(self):
        for family in ("mng-db", "dev-db"):
            command = next(
                service["command"][0]
                for service in load(f"infra/04-data/{family}/docker-compose.yml")[
                    "services"
                ].values()
                if "redis_exporter" in service.get("image", "")
            )
            self.assertIn("-config-command=-", command)
            self.assertIn("-set-client-name=false", command)
            self.assertIn("-exclude-latency-histogram-metrics", command)
            self.assertIn("-redis.user=" + family.split("-")[0] + "monitor", command)

    def test_oauth_binary_copy_and_nonroot_secret_wrapper_preserved(self):
        dockerfile = (ROOT / "infra/02-auth/oauth2-proxy/Dockerfile").read_text()
        self.assertIn(
            "quay.io/oauth2-proxy/oauth2-proxy:v7.15.5@sha256:8498b0d0ef0a7b29686414000a08aee467f02d0299c9ed1e006a8f33fc017916 AS src",
            dockerfile,
        )
        self.assertIn("COPY --from=src /bin/oauth2-proxy /bin/oauth2-proxy", dockerfile)
        self.assertIn("USER 100:101", dockerfile)
        self.assertIn('ENTRYPOINT ["/docker-entrypoint.sh"]', dockerfile)

    def test_effective_oauth_default_and_override_share_security_candidate(self):
        service = load("infra/02-auth/oauth2-proxy/docker-compose.yml")["services"][
            "oauth2-proxy"
        ]
        choice = service["build"]["dockerfile"]
        self.assertEqual(choice, "${OAUTH2_PROXY_DOCKERFILE:-dev.Dockerfile}")
        effective_default = choice.split(":-", 1)[1][:-1]
        self.assertEqual(effective_default, "dev.Dockerfile")
        expected = "FROM quay.io/oauth2-proxy/oauth2-proxy:v7.15.5@sha256:8498b0d0ef0a7b29686414000a08aee467f02d0299c9ed1e006a8f33fc017916 AS src"
        for selected in (effective_default, "Dockerfile"):
            with self.subTest(selected=selected):
                source = (ROOT / "infra/02-auth/oauth2-proxy" / selected).read_text()
                self.assertEqual(source.splitlines()[0], expected)
        dev = (ROOT / "infra/02-auth/oauth2-proxy/dev.Dockerfile").read_text()
        self.assertIn(
            "COPY --chmod=0555 docker-entrypoint.dev.sh /docker-entrypoint.sh", dev
        )
        self.assertIn("USER oauth2proxy:oauth2proxy", dev)

    def test_oauth_security_fix_has_narrow_trusted_proxy_and_no_auth_bypass(self):
        config = tomllib.loads(
            (ROOT / "infra/02-auth/oauth2-proxy/config/oauth2-proxy.cfg").read_text()
        )
        self.assertEqual(config["trusted_proxy_ips"], ["10.250.1.2/32"])
        self.assertNotIn("trusted_ips", config)
        self.assertNotIn("skip_auth_routes", config)
        self.assertNotIn("skip_auth_regex", config)
        self.assertEqual(config["provider"], "keycloak-oidc")
        self.assertEqual(config["allowed_groups"], ["/admins"])
        self.assertTrue(config["cookie_secure"])

    def test_tempo_candidate_keeps_seaweed_nonroot_wrapper(self):
        dockerfile = (ROOT / "infra/06-observability/tempo/Dockerfile").read_text()
        self.assertIn(
            "grafana/tempo:3.1.0@sha256:3076b8dcdfb32fd6bc5ccef85e7b7313e6199b9cb84366257fc17ecb696db5fd AS upstream",
            dockerfile,
        )
        self.assertIn("COPY --from=upstream /tempo /usr/bin/tempo", dockerfile)
        self.assertIn("USER 10001:10001", dockerfile)
        self.assertIn('ENTRYPOINT ["/docker-entrypoint.sh"]', dockerfile)
        service = load("infra/06-observability/docker-compose.yml")["services"]["tempo"]
        self.assertEqual(service["image"], "hy/tempo:3.1.0-seaweedfs")
        self.assertEqual(service["user"], "10001:10001")
        self.assertEqual(
            service["environment"]["S3_SECRET_KEY_FILE"],
            "/run/secrets/seaweedfs_s3_tempo_secret_key",
        )
        self.assertIn("tempo-data:/var/tempo:rw", service["volumes"])

    def test_tempo_preserves_rollback_block_writer_and_storage_contract(self):
        config = load("infra/06-observability/tempo/config/tempo.yaml")
        storage = config["storage"]["trace"]
        self.assertEqual(storage["block"]["version"], "vParquet4")
        self.assertEqual(storage["backend"], "s3")
        self.assertEqual(storage["s3"]["endpoint"], "seaweedfs-s3:8333")
        self.assertEqual(storage["s3"]["bucket"], "tempo-bucket")
        self.assertEqual(storage["s3"]["secret_key"], "${S3_SECRET_KEY}")
        self.assertTrue(storage["s3"]["forcepathstyle"])
        self.assertTrue(config["stream_over_http_enabled"])
        self.assertNotIn("cache", config)
        # POL-0048: 24h trace retention through the Tempo 3.x backend worker.
        compaction = config["backend_worker"]["compaction"]
        self.assertEqual(compaction["block_retention"], "24h")
        self.assertEqual(compaction["compacted_block_retention"], "1h")
        self.assertEqual(
            config["overrides"]["defaults"]["metrics_generator"]["processors"],
            ["service-graphs", "span-metrics"],
        )

    def run_fixture(
        self,
        family,
        binary,
        env_name,
        empty=False,
        preset=None,
        entrypoint="docker-entrypoint.sh",
    ):
        with tempfile.TemporaryDirectory(prefix="sec01-wrapper-fixture-") as directory:
            base = Path(directory)
            secret = base / "synthetic-secret"
            secret.write_text("" if empty else "synthetic-only\r\n")
            executable = base / "binary"
            executable.write_text(
                "#!/usr/bin/python3\nimport os,json,sys\nprint(json.dumps({'matched':os.environ.get("
                + repr(env_name)
                + ")=="
                + repr(preset or "synthetic-only")
                + ", 'args':sys.argv[1:]}))\n"
            )
            executable.chmod(0o700)
            source = (
                (ROOT / family / entrypoint)
                .read_text()
                .replace(binary, str(executable))
            )
            source = source.replace("/run/secrets/oauth2_valkey_password", str(secret))
            source = source.replace("/run/secrets/mng_valkey_password", str(secret))
            script = base / "entrypoint.sh"
            script.write_text(source)
            env = {
                "PATH": "/usr/bin:/bin",
                "LC_ALL": "C",
                "S3_SECRET_KEY_FILE": str(secret),
            }
            if preset is not None:
                env[env_name] = preset
            return subprocess.run(
                ["/bin/sh", str(script)],
                env=env,
                capture_output=True,
                text=True,
                timeout=5,
                check=False,
            )

    def test_tempo_synthetic_wrapper_trims_secret_and_executes(self):
        result = self.run_fixture(
            "infra/06-observability/tempo", "/usr/bin/tempo", "S3_SECRET_KEY"
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout), {"matched": True, "args": []})
        self.assertEqual(result.stderr, "")

    def test_tempo_empty_secret_fails_before_binary(self):
        result = self.run_fixture(
            "infra/06-observability/tempo",
            "/usr/bin/tempo",
            "S3_SECRET_KEY",
            empty=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertIn("empty secret:", result.stderr)

    def test_oauth_synthetic_wrapper_default_command_and_existing_env(self):
        for preset in (None, "synthetic-existing"):
            result = self.run_fixture(
                "infra/02-auth/oauth2-proxy",
                "/bin/oauth2-proxy",
                "OAUTH2_PROXY_REDIS_PASSWORD",
                preset=preset,
            )
            self.assertEqual(result.returncode, 0)
            self.assertEqual(
                json.loads(result.stdout),
                {"matched": True, "args": ["--config", "/etc/oauth2-proxy.cfg"]},
            )
            self.assertEqual(result.stderr, "")

    def test_effective_dev_wrapper_reads_mng_secret_and_preserves_override(self):
        for preset in (None, "synthetic-existing"):
            result = self.run_fixture(
                "infra/02-auth/oauth2-proxy",
                "/bin/oauth2-proxy",
                "OAUTH2_PROXY_REDIS_PASSWORD",
                preset=preset,
                entrypoint="docker-entrypoint.dev.sh",
            )
            self.assertEqual(result.returncode, 0)
            self.assertEqual(
                json.loads(result.stdout),
                {"matched": True, "args": ["--config", "/etc/oauth2-proxy.cfg"]},
            )
            self.assertEqual(result.stderr, "")


if __name__ == "__main__":
    unittest.main()
