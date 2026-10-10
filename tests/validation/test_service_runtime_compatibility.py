"""SPEC-0204 service runtime declarations that must agree before HOME rollout."""

import json
import os
import re
import subprocess
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
N8N = ROOT / "infra/07-workflow/n8n"


def compose(path: str) -> dict:
    return yaml.safe_load((ROOT / path).read_text(encoding="utf-8"))


class RuntimeCompatibilityTests(unittest.TestCase):
    def test_openbao_native_tls_and_backend_ca_share_endpoint(self):
        services = compose("infra/03-security/openbao/docker-compose.yml")["services"]
        server = services["openbao"]
        env = server["environment"]
        for port in (8200, 8240):
            config = json.loads(
                env["BAO_LOCAL_CONFIG"]
                .replace("${OPENBAO_PORT:-8200}", str(port))
                .replace("${OPENBAO_CLUSTER_PORT:-8201}", "8201")
            )
            listener = config["listener"][0]["tcp"]
            self.assertFalse(listener.get("tls_disable", False))
            self.assertTrue(listener["disable_unauthed_rekey_endpoints"])
            self.assertTrue(listener["disable_unauthed_generate_root_endpoints"])
            self.assertEqual(f"0.0.0.0:{port}", listener["address"])
            self.assertEqual(f"https://openbao:{port}", config["api_addr"])
            self.assertEqual("/openbao/tls/server.pem", listener["tls_cert_file"])
            self.assertEqual("/openbao/tls/server-key.pem", listener["tls_key_file"])
        self.assertEqual("/openbao/tls/ca.pem", env["BAO_CACERT"])
        self.assertTrue(
            services["openbao-agent"]["environment"]["VAULT_ADDR"].startswith(
                "https://"
            )
        )
        self.assertIn(
            "https",
            server["labels"][
                "traefik.http.services.openbao.loadbalancer.server.scheme"
            ],
        )
        transport = compose("infra/01-gateway/traefik/dynamic/tls.yaml")["http"][
            "serversTransports"
        ]["openbao-tls"]
        self.assertEqual("openbao", transport["serverName"])
        self.assertEqual(["/openbao-ca/ca.pem"], transport["rootCAs"])
        self.assertFalse(transport.get("insecureSkipVerify", False))

    def test_openbao_private_key_is_outside_shared_cert_directory(self):
        server = compose("infra/03-security/openbao/docker-compose.yml")["services"][
            "openbao"
        ]
        key = next(
            v
            for v in server["volumes"]
            if isinstance(v, dict) and v["target"] == "/openbao/tls/server-key.pem"
        )
        self.assertEqual(
            "${DEFAULT_SECURITY_DIR}/openbao/tls/server-key.pem", key["source"]
        )
        for path in (
            "infra/01-gateway/traefik/docker-compose.yml",
            "infra/06-observability/docker-compose.yml",
        ):
            for service in compose(path)["services"].values():
                for mount in service.get("volumes", []):
                    source = (
                        mount.get("source", "")
                        if isinstance(mount, dict)
                        else mount.split(":")[0]
                    )
                    if "${DEFAULT_SECURITY_DIR}/openbao/tls" in source:
                        self.assertTrue(source.endswith("/ca.pem"), source)

    def test_renderer_issuer_policy_requires_wrapping(self):
        policy = (
            ROOT / "infra/03-security/openbao/config/policies/renderer-issuer.hcl"
        ).read_text()
        issuance = policy.split('path "auth/approle/role/hy-home-renderer/secret-id"')[
            1
        ]
        self.assertIn('min_wrapping_ttl = "30s"', issuance)
        self.assertIn('max_wrapping_ttl = "60s"', issuance)

    def test_renderer_metadata_and_memory_scratch_are_scoped(self):
        policy = (
            ROOT / "infra/03-security/openbao/config/policies/renderer.hcl"
        ).read_text()
        for domain in ("02-auth/keycloak", "06-observability/grafana"):
            self.assertIn(f'path "secret/metadata/hy-home/{domain}"', policy)
        agent = compose("infra/03-security/openbao/docker-compose.yml")["services"][
            "openbao-agent"
        ]
        self.assertIn("/tmp:rw,noexec,nosuid,nodev,size=16m,mode=1777", agent["tmpfs"])

    def test_tls_preflight_fails_closed_without_exposing_tool_output(self):
        script = ROOT / "infra/03-security/openbao/scripts/check-tls-material.sh"
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory)
            for name in ("ca.pem", "server.pem", "server-key.pem"):
                (fixture / name).write_text("private-synthetic-marker")
            tools = fixture / "bin"
            tools.mkdir()
            (tools / "openssl").write_text(
                "#!/bin/sh\necho private-synthetic-marker >&2\nexit 1\n"
            )
            (tools / "openssl").chmod(0o700)
            result = subprocess.run(
                ["sh", str(script), str(fixture), "openbao/openbao:2.6.2"],
                env={**os.environ, "PATH": f"{tools}:{os.environ['PATH']}"},
                capture_output=True,
                check=False,
            )
            self.assertNotEqual(0, result.returncode)
            self.assertIn(b"TLS_MATERIAL FAIL", result.stdout)
            self.assertNotIn(b"private-synthetic-marker", result.stdout + result.stderr)

    def test_documented_renderer_delivery_names_exact_stopped_agent(self):
        runbook = (ROOT / "docs/05.operations/runbooks/0085-openbao.md").read_text()
        self.assertIn(
            "openbao hy-home-infra_openbao-agent-data openbao/openbao:2.6.2 openbao-agent",
            runbook,
        )

    def test_openbao_exception_names_key_and_audit_without_home_claim(self):
        registry = json.loads(
            (ROOT / "infra/common-optimizations.exceptions.json").read_text()
        )
        entry = next(
            row
            for row in registry["exceptions"]
            if row["service"] == "openbao" and row["control"] == "secrets_group"
        )
        self.assertIn("/openbao/audit", entry["reason"])
        self.assertIn("/openbao/tls/server-key.pem", entry["impact"])
        self.assertIn(
            "HOME TLS/audit permissions remain unverified", entry["verification"]
        )

    def test_openbao_audit_is_declared_and_hmac_protected(self):
        config = compose("infra/03-security/openbao/docker-compose.yml")["services"][
            "openbao"
        ]["environment"]["BAO_LOCAL_CONFIG"]
        config = json.loads(
            config.replace("${OPENBAO_PORT:-8200}", "8200").replace(
                "${OPENBAO_CLUSTER_PORT:-8201}", "8201"
            )
        )
        self.assertFalse(config.get("unsafe_allow_api_audit_creation", False))
        audit = config["audit"][0]
        self.assertEqual("file", audit["type"])
        self.assertEqual("p01-file", audit["path"])
        options = audit["options"]
        self.assertEqual("false", options["log_raw"])
        self.assertEqual("true", options["hmac_accessor"])
        self.assertEqual("0600", options["mode"])
        self.assertEqual("/openbao/audit/audit.json", options["file_path"])

    def test_openbao_audit_failure_alert_uses_observed_counters(self):
        groups = compose(
            "infra/06-observability/prometheus/config/alert_rules/alert_rules.openbao.yml"
        )["groups"]
        alerts = {rule["alert"]: rule for group in groups for rule in group["rules"]}
        rule = alerts["OpenBaoAuditFailure"]
        self.assertEqual(
            'increase(vault_audit_log_request_failure{job="openbao"}[5m]) > 0 or increase(vault_audit_log_response_failure{job="openbao"}[5m]) > 0',
            rule["expr"],
        )
        self.assertEqual("critical", rule["labels"]["severity"])
        self.assertEqual("0m", rule["for"])

    def test_openbao_prometheus_nondefault_port_and_invalid_ports(self):
        start = ROOT / "infra/06-observability/prometheus/scripts/start.sh"
        for name in ("prometheus.yml", "prometheus.dev.yml"):
            jobs = compose(f"infra/06-observability/prometheus/config/{name}")[
                "scrape_configs"
            ]
            job = next(j for j in jobs if j["job_name"] == "openbao")
            self.assertEqual("https", job["scheme"])
            self.assertEqual("openbao", job["tls_config"]["server_name"])
            self.assertFalse(job["tls_config"].get("insecure_skip_verify", False))
            self.assertIn("file_sd_configs", job)
        with tempfile.TemporaryDirectory() as directory:
            env = {
                **os.environ,
                "PROMETHEUS_DEV_DATA_EXPECTED": "off",
                "PROMETHEUS_TARGETS_DIR": directory,
                "PROMETHEUS_BIN": "/bin/true",
            }
            for port in ("8240", "x", "0", "65536"):
                result = subprocess.run(
                    ["sh", str(start)],
                    env={**env, "OPENBAO_PORT": port},
                    capture_output=True,
                    check=False,
                )
                self.assertEqual(port == "8240", result.returncode == 0)
                if port == "8240":
                    targets = yaml.safe_load(
                        (Path(directory) / "openbao.yml").read_text()
                    )
                    self.assertEqual(["openbao:8240"], targets[0]["targets"])

    def test_missing_openbao_snapshot_token_fails_backup_unit(self):
        source = (
            ROOT / "infra/09-platform-ops/restic/bin/hyhome-backup.sh"
        ).read_text()
        block = source[
            source.index("# OpenBao Raft snapshot.") : source.index(
                "elif ! running openbao; then"
            )
        ]
        with tempfile.TemporaryDirectory() as directory:
            stale = Path(directory) / "openbao-raft.snap"
            stale.write_text("stale-barrier-encrypted-fixture")
            result = subprocess.run(
                ["bash", "-c", block + "fi\nexit $status\n"],
                env={
                    **os.environ,
                    "repo_root": directory,
                    "staging": directory,
                    "status": "0",
                },
                capture_output=True,
                check=False,
            )
            self.assertNotEqual(0, result.returncode)
            self.assertFalse(stale.exists())

    def test_n8n_instances_and_runners_share_version_and_supported_timeout(self):
        services = compose("infra/07-workflow/n8n/docker-compose.yml")["services"]
        versions = {
            services[name]["build"]["args"]["N8N_VERSION"]
            for name in ("n8n", "n8n-worker")
        }
        versions.update(
            services[name]["image"].split(":", 1)[1].removesuffix("-local")
            for name in (
                "n8n",
                "n8n-worker",
                "n8n-task-runner",
                "n8n-task-runner-worker",
            )
        )
        for dockerfile in ("Dockerfile", "dev.Dockerfile"):
            match = re.search(
                r"^ARG N8N_VERSION=(\S+)$", (N8N / dockerfile).read_text(), re.M
            )
            self.assertIsNotNone(match, dockerfile)
            versions.add(match.group(1))

        self.assertEqual(1, len(versions), f"n8n/runner version mismatch: {versions}")
        for name in ("n8n", "n8n-worker", "n8n-task-runner", "n8n-task-runner-worker"):
            environment = services[name]["environment"]
            self.assertEqual(300, environment["N8N_RUNNERS_TASK_TIMEOUT"])
            self.assertNotIn("N8N_RUNNER_TASK_TIMEOUT", environment)

    def test_n8n_consumes_selected_broker_secret_and_runner_token(self):
        services = compose("infra/07-workflow/n8n/docker-compose.yml")["services"]
        for name in ("n8n", "n8n-worker"):
            environment = services[name]["environment"]
            self.assertIn(
                "${N8N_VALKEY_SECRET:-mng_valkey_password}",
                environment["QUEUE_BULL_REDIS_PASSWORD_FILE"],
            )
            self.assertIn("N8N_VALKEY_SECRET", environment)
            self.assertEqual(
                "${N8N_VALKEY_SECRET:-mng_valkey_password}",
                services[name]["secrets"][0],
            )
            self.assertNotIn("n8n_valkey_password", services[name]["secrets"])
        for entrypoint in ("docker-entrypoint.sh", "docker-entrypoint.dev.sh"):
            script = (N8N / entrypoint).read_text(encoding="utf-8")
            self.assertIn("N8N_VALKEY_SECRET", script, entrypoint)
            result = subprocess.run(["sh", "-n", str(N8N / entrypoint)], check=False)
            self.assertEqual(0, result.returncode, entrypoint)
        for name in ("n8n-task-runner", "n8n-task-runner-worker"):
            runner = services[name]
            self.assertIn("n8n_runner_auth_token", runner["secrets"])
            self.assertNotIn("N8N_RUNNERS_AUTH_TOKEN_FILE", runner["environment"])
            self.assertEqual(["tini", "--", "/bin/sh", "-ec"], runner["entrypoint"])
            command = runner["command"]
            launcher = command if isinstance(command, str) else " ".join(command)
            self.assertIn("/run/secrets/n8n_runner_auth_token", launcher)
            self.assertIn("N8N_RUNNERS_AUTH_TOKEN", launcher)
            self.assertIn("/usr/local/bin/task-runner-launcher", launcher)
            result = subprocess.run(
                ["sh", "-n"], input=launcher, text=True, check=False
            )
            self.assertEqual(0, result.returncode, name)
            with tempfile.TemporaryDirectory() as temporary:
                secret = Path(temporary) / "token"
                stub = Path(temporary) / "launcher"
                stub.write_text(
                    '#!/bin/sh\ntest "$N8N_RUNNERS_AUTH_TOKEN" = synthetic-token\n',
                    encoding="utf-8",
                )
                stub.chmod(0o700)
                simulated = (
                    launcher.replace("$$", "$")
                    .replace("/run/secrets/n8n_runner_auth_token", str(secret))
                    .replace("/usr/local/bin/task-runner-launcher", str(stub))
                )
                for value, expected in (
                    (None, False),
                    ("", False),
                    ("synthetic-token", True),
                ):
                    if value is None:
                        secret.unlink(missing_ok=True)
                    else:
                        secret.write_text(value, encoding="utf-8")
                    result = subprocess.run(
                        ["sh", "-ec", simulated],
                        capture_output=True,
                        text=True,
                        check=False,
                    )
                    self.assertEqual(expected, result.returncode == 0, (name, value))
                    self.assertNotIn("synthetic-token", result.stdout + result.stderr)

    def test_n8n_entrypoints_reject_wrong_or_empty_selected_broker_secret(self):
        for entrypoint in ("docker-entrypoint.sh", "docker-entrypoint.dev.sh"):
            source = (N8N / entrypoint).read_text(encoding="utf-8")
            guard = source[: source.index("if [ -d /opt/custom-certificates ]")]
            with tempfile.TemporaryDirectory() as temporary:
                mount = Path(temporary)
                guard = guard.replace("/run/secrets", str(mount))
                for name in (
                    "n8n_db_password",
                    "n8n_encryption_key",
                    "n8n_runner_auth_token",
                ):
                    (mount / name).write_text("synthetic", encoding="utf-8")
                for host, selected, value, success in (
                    ("mng-valkey", "mng_valkey_password", "synthetic", True),
                    ("n8n-valkey", "n8n_valkey_password", "synthetic", True),
                    ("mng-valkey", "n8n_valkey_password", "synthetic", False),
                    ("mng-valkey", "mng_valkey_password", "", False),
                    ("mng-valkey", "mng_valkey_password", None, False),
                ):
                    for name in ("mng_valkey_password", "n8n_valkey_password"):
                        (mount / name).unlink(missing_ok=True)
                    if value is not None:
                        (mount / selected).write_text(value, encoding="utf-8")
                    environment = os.environ.copy()
                    environment.update(N8N_VALKEY_HOST=host, N8N_VALKEY_SECRET=selected)
                    result = subprocess.run(
                        ["sh", "-c", guard],
                        env=environment,
                        capture_output=True,
                        text=True,
                        check=False,
                    )
                    self.assertEqual(
                        success, result.returncode == 0, (entrypoint, host, selected)
                    )
                    self.assertNotIn("synthetic", result.stdout + result.stderr)

    def test_openbao_sealed_status_is_not_ready(self):
        openbao = compose("infra/03-security/openbao/docker-compose.yml")["services"][
            "openbao"
        ]
        health = openbao["healthcheck"]["test"][1]
        self.assertIn("bao status", health)
        with tempfile.TemporaryDirectory() as temporary:
            stub = Path(temporary) / "bao"
            stub.write_text('#!/bin/sh\nexit "$BAO_SYNTHETIC_RC"\n', encoding="utf-8")
            stub.chmod(0o700)
            for status, expected in ((0, 0), (1, 1), (2, 1)):
                environment = os.environ.copy()
                environment["PATH"] = f"{temporary}:{environment['PATH']}"
                environment["BAO_SYNTHETIC_RC"] = str(status)
                result = subprocess.run(
                    ["sh", "-c", health.replace("$$", "$")],
                    env=environment,
                    check=False,
                )
                self.assertEqual(expected == 0, result.returncode == 0, status)

    def test_crawl4ai_security_pin_and_isolated_optional_network(self):
        data = compose("infra/08-ai/crawl4ai/docker-compose.yml")
        crawler = data["services"]["crawl4ai"]
        version = crawler["image"].split("@", 1)[0].rsplit(":", 1)[1]
        self.assertGreaterEqual(tuple(map(int, version.split("."))), (0, 9, 4))
        self.assertEqual(["crawl4ai"], crawler["profiles"])
        self.assertEqual(["crawl4ai_net", "crawl4ai_egress_net"], crawler["networks"])
        self.assertEqual("false", crawler["labels"]["traefik.enable"])

    def test_crawl4ai_launcher_rejects_short_tokens_without_disclosing_them(self):
        command = compose("infra/08-ai/crawl4ai/docker-compose.yml")["services"][
            "crawl4ai"
        ]["command"]
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            secret = directory / "token"
            arguments = directory / "launcher-argv"
            stub = directory / "launcher"
            stub.write_text(
                '#!/bin/sh\nprintf "%s\\n" "$0" "$@" > "$SYNTHETIC_ARGV_FILE"\n',
                encoding="utf-8",
            )
            simulated = (
                command[2]
                .replace("$$", "$")
                .replace("/run/secrets/crawl4ai_api_token", str(secret))
                .replace("entrypoint.sh", str(stub))
            )
            for value, allowed in (
                (None, False),
                ("", False),
                ("synthetic-12345", False),
                ("synthetic-123456", True),
            ):
                with self.subTest(token_length=None if value is None else len(value)):
                    arguments.unlink(missing_ok=True)
                    secret.unlink(missing_ok=True)
                    if value is not None:
                        secret.write_text(value, encoding="utf-8")
                    result = subprocess.run(
                        [*command[:2], simulated],
                        env={
                            "PATH": "/usr/bin:/bin",
                            "SYNTHETIC_ARGV_FILE": str(arguments),
                        },
                        capture_output=True,
                        text=True,
                        check=False,
                    )
                    self.assertEqual(allowed, result.returncode == 0)
                    self.assertEqual(allowed, arguments.exists())
                    launcher_arguments = (
                        arguments.read_text(encoding="utf-8")
                        if arguments.exists()
                        else ""
                    )
                    if value:
                        self.assertNotIn(
                            value, result.stdout + result.stderr + launcher_arguments
                        )

    def test_cassandra_remains_an_independent_official_image_lab(self):
        lab = compose("labs/cassandra.yml")
        service = lab["services"]["cassandra-node1"]
        self.assertTrue(service["image"].startswith("cassandra:"))
        self.assertEqual("hy-home-lab-cassandra", lab["name"])
        self.assertIn(
            "cassandra-node1-volume:/var/lib/cassandra:rw", service["volumes"]
        )
        self.assertIn(
            "${LAB_DATA_DIR:?set isolated LAB data root}",
            lab["volumes"]["cassandra-node1-volume"]["driver_opts"]["device"],
        )
        self.assertTrue(lab["networks"]["lab_cassandra_core_net"]["internal"])

    def test_no_active_compose_or_dockerfile_uses_a_bitnami_image(self):
        # Bitnami stopped publishing free versioned images; a namespace swap
        # alone would keep its env, UID and data path, so none may remain.
        tracked = subprocess.run(
            ["git", "ls-files", "--", "*docker-compose*.yml", "labs/*.yml",
             "*Dockerfile", "infra/tech-stack.versions.json"],
            cwd=ROOT, capture_output=True, text=True, check=True,
        ).stdout.split()  # fmt: skip
        self.assertTrue(tracked)
        offenders = [
            path
            for path in tracked
            if re.search(r"\bbitnami/|/bitnami\b", (ROOT / path).read_text())
        ]
        self.assertEqual([], offenders)

    def test_every_secret_file_key_names_how_its_image_reads_it(self):
        import json

        with tempfile.TemporaryDirectory() as home:
            rendered = subprocess.run(
                ["docker", "compose", "--env-file", ".env.example",
                 "--profile", "*", "config", "--format", "json"],
                cwd=ROOT, env={"PATH": os.environ["PATH"], "HOME": home},
                capture_output=True, text=True, check=True, timeout=120,
            )  # fmt: skip
        services = json.loads(rendered.stdout)["services"]
        used = {}
        for name, spec in services.items():
            for key in spec.get("environment") or {}:
                if re.search(r"(_FILE|_CMD)$", key) and key not in (
                    "SSL_CERT_FILE",
                    "RENOVATE_CONFIG_FILE",
                ):
                    image = spec["image"].split(":", 1)[0]
                    used.setdefault((image, key), set()).add(name)
        matrix = json.loads((ROOT / "infra/secret-file-support.json").read_text())
        rows = {(row["image"], row["key"]): row for row in matrix["rows"]}
        self.assertEqual(set(used), set(rows))

        policy = (
            ROOT / "docs/05.operations/policies/0078-compose-profile-vocabulary.md"
        ).read_text(encoding="utf-8")
        home_row = next(x for x in policy.splitlines() if x.startswith("| HOME |"))
        home = set(re.findall(r"`([A-Za-z0-9][A-Za-z0-9_.-]*)`", home_row))
        for pair, row in rows.items():
            with self.subTest(pair=pair):
                self.assertIn(row["support"], {"native", "wrapper", "unsupported"})
                self.assertTrue(row["evidence"])
                if row["support"] == "unsupported":
                    # An ignored key leaves the secret unset: such a service
                    # stays out of the HOME selection until it is fixed.
                    self.assertTrue(row.get("blocked"))
                    for service in used[pair]:
                        profiles = set(services[service].get("profiles") or [])
                        self.assertTrue(profiles)
                        self.assertFalse(profiles & home, service)
                path = row["evidence"].split()[0]
                if row["support"] == "wrapper" and path.startswith("infra/"):
                    wrapper = (ROOT / path).read_text(encoding="utf-8")
                    self.assertIn(pair[1].removesuffix("_FILE"), wrapper)

    def test_keycloak_wrapper_refuses_empty_secret_files(self):
        script = compose("infra/02-auth/keycloak/docker-compose.yml")["services"][
            "keycloak"
        ]["entrypoint"][2]
        for name in ("KC_BOOTSTRAP_ADMIN_PASSWORD", "KC_DB_PASSWORD"):
            self.assertIn(f'[ -n "$${name}" ] ||', script)
        self.assertLess(script.index("exit 1"), script.index("exec "))

    def test_sonarqube_exports_its_jdbc_password_from_the_secret(self):
        # The image has no _FILE support; the wrapper refuses an empty secret
        # and keeps the image entrypoint.
        service = compose("infra/11-quality/sonarqube/docker-compose.yml")["services"][
            "sonarqube"
        ]
        script = service["entrypoint"][2]
        self.assertIn("cat /run/secrets/sonarqube_db_password", script)
        self.assertIn('[ -n "$$SONAR_JDBC_PASSWORD" ] ||', script)
        self.assertIn('exec /opt/sonarqube/docker/entrypoint.sh "$$@"', script)
        self.assertFalse([e for e in service["environment"] if "PASSWORD_FILE" in e])

    def test_supabase_smtp_wrapper_consumes_file_and_preserves_arguments(self):
        service = compose("infra/04-data/supabase/docker-compose.yml")["services"][
            "auth"
        ]
        self.assertEqual(["auth"], service.get("command"))
        script = service["entrypoint"][2].replace("$$", "$")
        with tempfile.TemporaryDirectory() as directory:
            secret = Path(directory) / "smtp"
            secret.write_text("synthetic-smtp-password\n")
            env = {"PATH": os.environ["PATH"], "GOTRUE_SMTP_PASS_FILE": str(secret)}
            probe = 'test "$GOTRUE_SMTP_PASS" = synthetic-smtp-password && test "$1" = argument'
            result = subprocess.run(
                [
                    "/bin/sh",
                    "-ec",
                    script,
                    "--",
                    "/bin/sh",
                    "-ec",
                    probe,
                    "--",
                    "argument",
                ],
                env=env,
                capture_output=True,
                text=True,
                timeout=5,
                check=False,
            )
            self.assertEqual(0, result.returncode)
            self.assertEqual("", result.stdout + result.stderr)
            for value in ("", "\n"):
                secret.write_text(value)
                result = subprocess.run(
                    ["/bin/sh", "-ec", script, "--", "true"],
                    env=env,
                    capture_output=True,
                    text=True,
                    timeout=5,
                    check=False,
                )
                self.assertNotEqual(0, result.returncode)
                self.assertNotIn(
                    "synthetic-smtp-password", result.stdout + result.stderr
                )
            secret.unlink()
            result = subprocess.run(
                ["/bin/sh", "-ec", script, "--", "true"],
                env=env,
                capture_output=True,
                text=True,
                timeout=5,
                check=False,
            )
            self.assertNotEqual(0, result.returncode)
            secret.write_text("synthetic-smtp-password")
            result = subprocess.run(
                ["/bin/sh", "-ec", script, "--", "true"],
                env=env | {"GOTRUE_SMTP_PASS": "synthetic-direct-password"},
                capture_output=True,
                text=True,
                timeout=5,
                check=False,
            )
            self.assertNotEqual(0, result.returncode)
            self.assertNotIn("synthetic-direct-password", result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
