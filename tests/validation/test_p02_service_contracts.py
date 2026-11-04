"""P02 service listener, data endpoint, authentication and Valkey contracts."""

from __future__ import annotations

import hashlib
import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
HARDENING = ROOT / "scripts/hardening/check-all-hardening.sh"
VALKEY_RENDERER = ROOT / "infra/04-data/mng-db/valkey/scripts/render-monitor-acl.sh"
DEDICATED_VALKEY_START = ROOT / "infra/04-data/mng-db/valkey/scripts/start-dedicated.sh"


class _ComposeLoader(yaml.SafeLoader):
    """Load Compose documents while retaining values tagged ``!override``."""


def _construct_override(loader: _ComposeLoader, node: yaml.Node) -> object:
    if isinstance(node, yaml.SequenceNode):
        return loader.construct_sequence(node)
    if isinstance(node, yaml.MappingNode):
        return loader.construct_mapping(node)
    return loader.construct_scalar(node)


_ComposeLoader.add_constructor("!override", _construct_override)


def _compose(relative: str) -> dict:
    return yaml.load(
        (ROOT / relative).read_text(encoding="utf-8"), Loader=_ComposeLoader
    )


def _service(relative: str, name: str) -> dict:
    return _compose(relative)["services"][name]


def _environment(service: dict) -> dict[str, str]:
    value = service.get("environment") or {}
    if isinstance(value, dict):
        return value
    return dict(item.split("=", 1) for item in value)


def _command(service: dict) -> str:
    value = service.get("command") or ""
    return value if isinstance(value, str) else " ".join(str(item) for item in value)


def _render_root(overrides: dict[str, str]) -> dict:
    """Render selected public profiles without contacting a Docker daemon."""
    with tempfile.TemporaryDirectory() as directory:
        temporary = Path(directory)
        env_file = temporary / "public.env"
        env_file.write_bytes(
            (ROOT / ".env.example").read_bytes()
            + b"\n"
            + "".join(
                f"{key}={value}\n" for key, value in sorted(overrides.items())
            ).encode("utf-8")
        )
        args = [
            "docker",
            "compose",
            "--project-directory",
            str(ROOT),
            "--env-file",
            str(env_file),
            "-f",
            str(ROOT / "docker-compose.yml"),
        ]
        for profile in (
            "core",
            "mng",
            "data",
            "admin-data",
            "iac",
            "obs",
            "workflow-airflow",
            "ai",
            "notebook",
            "dedicated-valkey",
            "nginx",
        ):
            args.extend(("--profile", profile))
        args.extend(("config", "--format", "json"))
        environment = {
            "COMPOSE_DISABLE_ENV_FILE": "1",
            "DOCKER_CONFIG": str(temporary / "docker-config"),
            "DOCKER_HOST": f"unix://{temporary / 'no-daemon.sock'}",
            "HOME": str(temporary),
            "PATH": os.environ["PATH"],
        }
        result = subprocess.run(
            args,
            cwd=ROOT,
            env=environment,
            capture_output=True,
            text=True,
            check=False,
            timeout=120,
        )
        if result.returncode:
            raise AssertionError("public Compose configuration did not render")
        return __import__("json").loads(result.stdout)["services"]


class ListenerPortContractTests(unittest.TestCase):
    def test_oauth2_proxy_listener_health_and_gateway_use_one_port(self) -> None:
        service = _service(
            "infra/02-auth/oauth2-proxy/docker-compose.yml", "oauth2-proxy"
        )
        environment = _environment(service)
        self.assertEqual(
            "0.0.0.0:${OAUTH2_PROXY_PORT:-4180}",
            environment.get("OAUTH2_PROXY_HTTP_ADDRESS"),
        )
        self.assertEqual(
            "${OAUTH2_PROXY_PORT:-4180}", environment.get("OAUTH2_PROXY_PORT")
        )
        self.assertEqual(
            "${OAUTH2_PROXY_PORT:-4180}",
            service["labels"][
                "traefik.http.services.oauth2-proxy-svc.loadbalancer.server.port"
            ],
        )
        self.assertIn(
            "127.0.0.1:$${OAUTH2_PROXY_PORT}/ping",
            " ".join(service["healthcheck"]["test"]),
        )
        gatus = _service("infra/06-observability/docker-compose.yml", "gatus")
        self.assertEqual(
            "${OAUTH2_PROXY_PORT:-4180}",
            _environment(gatus).get("OAUTH2_PROXY_PORT"),
        )
        for relative in (
            "infra/06-observability/gatus/config/config.yaml",
            "infra/06-observability/gatus/config/config.oidc.yaml",
        ):
            config = (ROOT / relative).read_text(encoding="utf-8")
            self.assertIn("http://oauth2-proxy:${OAUTH2_PROXY_PORT}/ping", config)

    def test_keycloak_application_and_management_listeners_are_explicit(self) -> None:
        service = _service("infra/02-auth/keycloak/docker-compose.yml", "keycloak")
        environment = _environment(service)
        self.assertEqual("${KEYCLOAK_PORT:-8080}", environment.get("KC_HTTP_PORT"))
        self.assertEqual(
            "${KEYCLOAK_MANAGEMENT_PORT:-9000}",
            environment.get("KC_HTTP_MANAGEMENT_PORT"),
        )
        self.assertEqual(
            "${KEYCLOAK_PORT:-8080}",
            service["labels"][
                "traefik.http.services.keycloak.loadbalancer.server.port"
            ],
        )
        self.assertIn(
            '127.0.0.1/"$${KC_HTTP_MANAGEMENT_PORT}"',
            " ".join(service["healthcheck"]["test"]),
        )

    def test_open_webui_listener_health_and_gateway_use_one_port(self) -> None:
        service = _service("infra/08-ai/open-webui/docker-compose.yml", "open-webui")
        environment = _environment(service)
        self.assertEqual("${OLLAMA_WEBUI_PORT:-8080}", environment.get("PORT"))
        self.assertEqual(
            "${OLLAMA_WEBUI_PORT:-8080}",
            service["labels"][
                "traefik.http.services.open-webui.loadbalancer.server.port"
            ],
        )
        self.assertIn(
            "localhost:$${PORT}/health",
            " ".join(service["healthcheck"]["test"]),
        )

    def test_airflow_api_listener_execution_url_health_and_gateway_agree(self) -> None:
        compose = _compose("infra/07-workflow/airflow/docker-compose.yml")
        service = compose["services"]["airflow-apiserver"]
        environment = _environment(service)
        self.assertEqual("${AIRFLOW_PORT:-8080}", environment.get("AIRFLOW__API__PORT"))
        self.assertEqual(
            "http://airflow-apiserver:${AIRFLOW_PORT:-8080}/execution/",
            environment.get("AIRFLOW__CORE__EXECUTION_API_SERVER_URL"),
        )
        self.assertEqual(
            "${AIRFLOW_PORT:-8080}",
            service["labels"]["traefik.http.services.airflow.loadbalancer.server.port"],
        )
        self.assertIn(
            "localhost:${AIRFLOW_PORT:-8080}/api/v2/monitor/health",
            " ".join(service["healthcheck"]["test"]),
        )

    @unittest.skipUnless(shutil.which("docker"), "docker compose CLI not available")
    def test_public_render_applies_default_and_nondefault_listener_contracts(
        self,
    ) -> None:
        baseline = _render_root({})
        changed = _render_root(
            {
                "AIRFLOW_PORT": "18082",
                "KEYCLOAK_MANAGEMENT_PORT": "19000",
                "KEYCLOAK_PORT": "18080",
                "OAUTH2_PROXY_PORT": "14180",
                "OLLAMA_WEBUI_PORT": "18081",
                "POSTGRES_HOST_PORT": "25439",
                "POSTGRES_PORT": "15432",
                "VALKEY_MNG_HOST_PORT": "26389",
                "VALKEY_PORT": "16379",
            }
        )

        expected = {
            "oauth2-proxy": (
                "OAUTH2_PROXY_HTTP_ADDRESS",
                "0.0.0.0:4180",
                "0.0.0.0:14180",
            ),
            "keycloak": ("KC_HTTP_PORT", "8080", "18080"),
            "open-webui": ("PORT", "8080", "18081"),
            "airflow-apiserver": ("AIRFLOW__API__PORT", "8080", "18082"),
        }
        for service_name, (key, default, override) in expected.items():
            with self.subTest(service=service_name):
                self.assertEqual(
                    default, str(baseline[service_name]["environment"][key])
                )
                self.assertEqual(
                    override, str(changed[service_name]["environment"][key])
                )

        self.assertEqual(
            "19000", str(changed["keycloak"]["environment"]["KC_HTTP_MANAGEMENT_PORT"])
        )
        self.assertEqual(
            "9000", str(baseline["gatus"]["environment"]["KEYCLOAK_MANAGEMENT_PORT"])
        )
        self.assertEqual(
            "19000", str(changed["gatus"]["environment"]["KEYCLOAK_MANAGEMENT_PORT"])
        )
        self.assertEqual(
            "4180", str(baseline["gatus"]["environment"]["OAUTH2_PROXY_PORT"])
        )
        self.assertEqual(
            "14180", str(changed["gatus"]["environment"]["OAUTH2_PROXY_PORT"])
        )
        self.assertEqual(
            "4180", str(baseline["nginx"]["environment"]["OAUTH2_PROXY_PORT"])
        )
        self.assertEqual(
            "14180", str(changed["nginx"]["environment"]["OAUTH2_PROXY_PORT"])
        )
        self.assertEqual("8080", str(baseline["nginx"]["environment"]["KEYCLOAK_PORT"]))
        self.assertEqual("18080", str(changed["nginx"]["environment"]["KEYCLOAK_PORT"]))
        self.assertIn("port=15432", _command(changed["mng-pg"]))
        self.assertEqual(
            "15432", str(changed["mng-pg"]["environment"]["POSTGRES_PORT"])
        )
        self.assertIn(
            '-p "$${POSTGRES_PORT}"',
            " ".join(changed["mng-pg"]["healthcheck"]["test"]),
        )
        self.assertEqual(15432, changed["mng-pg"]["ports"][0]["target"])
        self.assertEqual("25439", str(changed["mng-pg"]["ports"][0]["published"]))
        self.assertEqual(
            "16379", str(changed["mng-valkey"]["environment"]["MNG_VALKEY_PORT"])
        )
        self.assertEqual(16379, changed["mng-valkey"]["ports"][0]["target"])
        self.assertEqual("26389", str(changed["mng-valkey"]["ports"][0]["published"]))
        self.assertEqual(
            "16379",
            str(changed["redisinsight"]["environment"]["RI_REDIS_PORT2"]),
        )
        self.assertEqual(
            "6379",
            str(changed["redisinsight"]["environment"]["RI_REDIS_PORT1"]),
        )
        self.assertEqual(
            "15432",
            str(changed["terrakube-api"]["environment"]["DatasourcePort"]),
        )
        self.assertEqual(
            "16379",
            str(changed["terrakube-api"]["environment"]["TerrakubeRedisPort"]),
        )


class ManagementDataPortContractTests(unittest.TestCase):
    def test_postgres_listener_health_pgbackrest_and_publication_agree(self) -> None:
        service = _service("infra/04-data/mng-db/docker-compose.yml", "mng-pg")
        environment = _environment(service)
        command = _command(service)
        self.assertIn("port=${POSTGRES_PORT:-5432}", command)
        self.assertEqual("${POSTGRES_PORT:-5432}", environment["POSTGRES_PORT"])
        self.assertEqual("${POSTGRES_PORT:-5432}", environment["PGBACKREST_PG1_PORT"])
        self.assertIn(
            '-p "$${POSTGRES_PORT}"', " ".join(service["healthcheck"]["test"])
        )
        self.assertEqual(
            "127.0.0.1:${POSTGRES_HOST_PORT:-25432}:${POSTGRES_PORT:-5432}",
            service["ports"][0],
        )

    def test_compose_sources_do_not_bypass_management_port_contracts(self) -> None:
        offenders: list[tuple[str, str]] = []
        for path in sorted((ROOT / "infra").rglob("docker-compose*.yml")):
            text = path.read_text(encoding="utf-8")
            for literal in ("mng-pg:5432", "mng-valkey:6379"):
                if literal in text:
                    offenders.append((str(path.relative_to(ROOT)), literal))
        self.assertEqual([], offenders)

    def test_redisinsight_keeps_dev_fixed_and_tracks_management_valkey(self) -> None:
        service = _service(
            "infra/04-data/redisinsight/docker-compose.yml", "redisinsight"
        )
        environment = _environment(service)
        self.assertEqual(
            ("dev-valkey", "6379"),
            (environment["RI_REDIS_HOST1"], str(environment["RI_REDIS_PORT1"])),
        )
        self.assertEqual(
            ("mng-valkey", "${VALKEY_PORT:-6379}"),
            (environment["RI_REDIS_HOST2"], environment["RI_REDIS_PORT2"]),
        )

    def test_airflow_uses_declared_management_postgres_and_valkey_ports(self) -> None:
        import importlib.util
        import io
        import shlex
        from urllib.parse import unquote, urlsplit

        source = ROOT / "infra/07-workflow/airflow/connection_uri.py"
        spec = importlib.util.spec_from_file_location("airflow_connection_uri", source)
        helper = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(helper)
        with tempfile.TemporaryDirectory(prefix="p04-rendered-uri-") as temporary:
            secrets = Path(temporary)
            password = " p04-synthetic @:/?#%40+ 한글 "  # gitleaks:allow -- synthetic fixture; never deployed
            for name in ("airflow_db_password", "mng_valkey_password"):
                path = secrets / name
                path.write_text(password, encoding="utf-8")
                path.chmod(0o600)
            for pg_port, valkey_port in ((5432, 6379), (55432, 16379)):
                rendered = _render_root(
                    {"POSTGRES_PORT": str(pg_port), "VALKEY_PORT": str(valkey_port)}
                )
                environment = rendered["airflow-worker"]["environment"]
                for key, mode, host, port in (
                    (
                        "AIRFLOW__DATABASE__SQL_ALCHEMY_CONN_CMD",
                        "metadata",
                        "mng-pg",
                        pg_port,
                    ),
                    (
                        "AIRFLOW__CELERY__RESULT_BACKEND_CMD",
                        "result",
                        "mng-pg",
                        pg_port,
                    ),
                    (
                        "AIRFLOW__CELERY__BROKER_URL_CMD",
                        "broker",
                        "mng-valkey",
                        valkey_port,
                    ),
                ):
                    command = shlex.split(environment[key])
                    self.assertEqual(
                        ["python3", "/opt/airflow/bin/connection_uri.py", mode], command
                    )
                    output, errors = io.StringIO(), io.StringIO()
                    self.assertEqual(
                        0,
                        helper.main(
                            command[2:],
                            environment=environment,
                            secrets_dir=secrets,
                            stdout=output,
                            stderr=errors,
                        ),
                    )
                    parsed = urlsplit(output.getvalue())
                    self.assertEqual((host, port), (parsed.hostname, parsed.port))
                    self.assertEqual(password, unquote(parsed.password))
                    self.assertEqual("", errors.getvalue())

    def test_oauth2_proxy_uses_declared_management_valkey_port(self) -> None:
        environment = _environment(
            _service("infra/02-auth/oauth2-proxy/docker-compose.yml", "oauth2-proxy")
        )
        self.assertEqual(
            "redis://${OAUTH2_PROXY_VALKEY_HOST:-mng-valkey}:${VALKEY_PORT:-6379}",
            environment["OAUTH2_PROXY_REDIS_CONNECTION_URL"],
        )

    def test_terrakube_uses_declared_management_postgres_and_valkey_ports(self) -> None:
        service = _service(
            "infra/09-platform-ops/terrakube/docker-compose.yml", "terrakube-api"
        )
        environment = _environment(service)
        self.assertEqual("${POSTGRES_PORT:-5432}", environment.get("DatasourcePort"))
        self.assertEqual("${VALKEY_PORT:-6379}", environment.get("TerrakubeRedisPort"))


class OpenNotebookPortAndReadinessTests(unittest.TestCase):
    COPY_SET = (
        "scripts/hardening/check-all-hardening.sh",
        "scripts/lib/hardening-lib.sh",
        "infra/08-ai/ollama/docker-compose.yml",
        "infra/08-ai/open-webui/docker-compose.yml",
        "infra/08-ai/open-notebook/docker-compose.yml",
    )

    def test_fixed_image_listeners_are_not_presented_as_configurable(self) -> None:
        service = _service(
            "infra/08-ai/open-notebook/docker-compose.yml", "open_notebook"
        )
        self.assertEqual(
            "127.0.0.1:${OPEN_NOTEBOOK_API_URL:-5055}:5055", service["ports"][0]
        )
        self.assertEqual(["8502"], [str(port) for port in service["expose"]])
        self.assertEqual(
            "8502",
            str(
                service["labels"][
                    "traefik.http.services.open-notebook.loadbalancer.server.port"
                ]
            ),
        )
        self.assertNotIn(
            "OPEN_NOTEBOOK_WEB_URL",
            (ROOT / "infra/08-ai/open-notebook/docker-compose.yml").read_text(),
        )

    def test_healthcheck_is_api_startup_readiness_not_data_directory_presence(
        self,
    ) -> None:
        service = _service(
            "infra/08-ai/open-notebook/docker-compose.yml", "open_notebook"
        )
        health = " ".join(service["healthcheck"]["test"])
        self.assertIn("http://127.0.0.1:5055/health", health)
        self.assertNotIn("test -d", health)
        self.assertNotIn("ollama", health.lower())
        self.assertNotIn("surreal", health.lower())

    def test_registered_hardening_rejects_a_web_listener_override(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for relative in self.COPY_SET:
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text((ROOT / relative).read_text(encoding="utf-8"))
            target = root / "infra/08-ai/open-notebook/docker-compose.yml"
            original = target.read_text(encoding="utf-8")

            def hardening() -> subprocess.CompletedProcess[str]:
                environment = {
                    key: value
                    for key, value in os.environ.items()
                    if key != "HYHOME_CI_GATE_ROOT"
                }
                return subprocess.run(
                    [
                        "bash",
                        str(root / "scripts/hardening/check-all-hardening.sh"),
                        "08-ai",
                    ],
                    cwd=root,
                    env=environment,
                    capture_output=True,
                    text=True,
                    check=False,
                    timeout=30,
                )

            baseline = hardening()
            self.assertEqual(0, baseline.returncode, baseline.stdout + baseline.stderr)
            target.write_text(
                original.replace(
                    "      - 8502", "      - ${OPEN_NOTEBOOK_WEB_URL:-8502}"
                ).replace(
                    "loadbalancer.server.port: 8502",
                    "loadbalancer.server.port: ${OPEN_NOTEBOOK_WEB_URL:-8502}",
                ),
                encoding="utf-8",
            )
            rejected = hardening()
            self.assertNotEqual(0, rejected.returncode)


class DedicatedValkeyContractTests(unittest.TestCase):
    BROKERS = (
        ("infra/07-workflow/airflow/docker-compose.yml", "airflow-valkey"),
        ("infra/07-workflow/n8n/docker-compose.yml", "n8n-valkey"),
        ("infra/02-auth/oauth2-proxy/docker-compose.yml", "oauth2-proxy-valkey"),
    )
    OVERLAYS = (
        "infra/07-workflow/airflow/docker-compose.monitor-acl.yml",
        "infra/07-workflow/n8n/docker-compose.monitor-acl.yml",
        "infra/02-auth/oauth2-proxy/docker-compose.monitor-acl.yml",
    )

    def test_all_brokers_use_the_safe_wrapper_and_one_listener_port(self) -> None:
        self.assertTrue(DEDICATED_VALKEY_START.is_file())
        for relative, name in self.BROKERS:
            with self.subTest(service=name):
                service = _service(relative, name)
                command = _command(service)
                environment = _environment(service)
                self.assertEqual("${VALKEY_PORT:-6379}", environment.get("VALKEY_PORT"))
                self.assertIn("start-dedicated.sh", command)
                self.assertNotIn("requirepass", command)
                self.assertNotIn("$(cat", command)
                self.assertEqual(["${VALKEY_PORT:-6379}"], service["expose"])
                health = " ".join(service["healthcheck"]["test"])
                self.assertIn('-p "$${VALKEY_PORT}"', health)
                self.assertIn("REDISCLI_AUTH", health)
                self.assertNotIn(" -a ", health)
        for relative in self.OVERLAYS:
            with self.subTest(overlay=relative):
                services = _compose(relative)["services"]
                broker = next(
                    name for name in services if not name.endswith("-exporter")
                )
                self.assertIn("start-dedicated.sh", _command(services[broker]))
                overlay_port = _environment(services[broker]).get("VALKEY_PORT")
                self.assertIn(overlay_port, (None, "${VALKEY_PORT:-6379}"))

    def test_exporters_keep_password_out_of_argv_and_track_listener_port(self) -> None:
        for relative, broker in self.BROKERS:
            exporter = _service(relative, broker + "-exporter")
            command = _command(exporter)
            self.assertEqual(
                "${VALKEY_PORT:-6379}",
                _environment(exporter).get("VALKEY_PORT"),
            )
            self.assertIn("port=$${VALKEY_PORT}", command)
            self.assertIn("*[!0-9]*", command)
            self.assertIn('"$$port" -le 65535', command)
            self.assertIn(f"redis://{broker}:$$port", command)
            self.assertIn("REDIS_PASSWORD", command)
            self.assertNotIn("-redis.password=", command)
            self.assertNotIn("-redis.password ", command)

    @unittest.skipUnless(shutil.which("docker"), "docker compose CLI not available")
    def test_root_and_each_monitor_overlay_render_at_nondefault_port(self) -> None:
        for overlay, (_, broker) in zip(self.OVERLAYS, self.BROKERS, strict=True):
            with (
                self.subTest(overlay=overlay),
                tempfile.TemporaryDirectory() as directory,
            ):
                temporary = Path(directory)
                env_file = temporary / "public.env"
                env_file.write_bytes(
                    (ROOT / ".env.example").read_bytes() + b"\nVALKEY_PORT=16379\n"
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
                        "-f",
                        str(ROOT / overlay),
                        "--profile",
                        "dedicated-valkey",
                        "config",
                        "--format",
                        "json",
                    ],
                    cwd=ROOT,
                    env={
                        "COMPOSE_DISABLE_ENV_FILE": "1",
                        "DOCKER_CONFIG": str(temporary / "docker-config"),
                        "DOCKER_HOST": f"unix://{temporary / 'no-daemon.sock'}",
                        "HOME": str(temporary),
                        "PATH": os.environ["PATH"],
                    },
                    capture_output=True,
                    text=True,
                    check=False,
                    timeout=120,
                )
                self.assertEqual(0, result.returncode, "overlay config failed")
                services = __import__("json").loads(result.stdout)["services"]
                rendered = services[broker]
                self.assertEqual("16379", str(rendered["environment"]["VALKEY_PORT"]))
                self.assertEqual(["16379"], rendered["expose"])
                self.assertIn("start-dedicated.sh", _command(rendered))
                self.assertIn(
                    '-p "$${VALKEY_PORT}"',
                    " ".join(rendered["healthcheck"]["test"]),
                )
                exporter = services[broker + "-exporter"]
                self.assertEqual("16379", str(exporter["environment"]["VALKEY_PORT"]))
                exporter_command = _command(exporter)
                self.assertIn("port=$${VALKEY_PORT}", exporter_command)
                self.assertIn(f"redis://{broker}:$$port", exporter_command)

    def _run_wrapper(
        self,
        root: Path,
        secret: Path,
        port: str = "6388",
        monitor: Path | None = None,
    ) -> tuple[subprocess.CompletedProcess[str], Path, Path]:
        output = root / "acl/users.acl"
        output.parent.mkdir(mode=0o700, exist_ok=True)
        args_file = root / "args"
        binary = root / "bin/valkey-server"
        binary.parent.mkdir()
        binary.write_text(
            '#!/bin/sh\nprintf \'%s\\n\' "$@" >"$P02_ARGS_FILE"\n',
            encoding="utf-8",
        )
        binary.chmod(0o755)
        environment = os.environ.copy()
        environment.update(
            {
                "PATH": f"{binary.parent}:/usr/bin:/bin",
                "P02_ARGS_FILE": str(args_file),
                "VALKEY_PORT": port,
            }
        )
        result = subprocess.run(
            [
                "sh",
                str(DEDICATED_VALKEY_START),
                str(secret),
                str(output),
                *((str(monitor),) if monitor is not None else ()),
            ],
            cwd=ROOT,
            env=environment,
            capture_output=True,
            text=True,
            check=False,
            timeout=10,
        )
        return result, output, args_file

    def test_wrapper_hashes_special_characters_and_never_exposes_them(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            secret = root / "secret"
            value = "synthetic !#$%&()*+,-./:;<=>?@[]^_{|}~"
            secret.write_text(value + "\n", encoding="ascii")
            secret.chmod(0o600)
            result, output, args_file = self._run_wrapper(root, secret)
            self.assertEqual(0, result.returncode, result.stderr)
            combined = result.stdout + result.stderr + args_file.read_text()
            self.assertNotIn(value, combined)
            digest = hashlib.sha256(value.encode("ascii")).hexdigest()
            self.assertIn(f"user default reset on #{digest}", output.read_text())
            self.assertEqual(
                [
                    *("--aclfile", str(output), "--appendonly", "yes"),
                    *("--port", "6388", "--maxmemory", "128mb"),
                    *("--maxmemory-policy", "noeviction"),
                ],
                args_file.read_text().splitlines(),
            )

    def test_wrapper_rejects_invalid_ports_before_acl_replacement(self) -> None:
        for port in ("0", "65536", "12x", " 6379", "6379 "):
            with self.subTest(port=port), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                secret = root / "secret"
                secret.write_text("synthetic-safe\n")
                secret.chmod(0o600)
                output = root / "acl/users.acl"
                output.parent.mkdir(mode=0o700)
                output.write_text("previous-safe-acl\n")
                output.chmod(0o600)
                result, _, args_file = self._run_wrapper(root, secret, port)
                self.assertNotEqual(0, result.returncode)
                self.assertEqual("previous-safe-acl\n", output.read_text())
                self.assertFalse(args_file.exists())

    def test_wrapper_rejects_unsafe_secret_without_replacing_acl(self) -> None:
        for case in (
            "missing",
            "empty",
            "multiline",
            "symlink",
            "mode",
            "hardlink-secret",
            "hardlink-output",
        ):
            with self.subTest(case=case), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                secret = root / "secret"
                secret.write_text("synthetic-safe\n")
                secret.chmod(0o600)
                if case == "missing":
                    secret.unlink()
                elif case == "empty":
                    secret.write_bytes(b"")
                elif case == "multiline":
                    secret.write_text("first\nsecond\n")
                elif case == "symlink":
                    target = root / "target"
                    target.write_text("synthetic-safe\n")
                    target.chmod(0o600)
                    secret.unlink()
                    secret.symlink_to(target)
                elif case == "mode":
                    secret.chmod(0o644)
                elif case == "hardlink-secret":
                    os.link(secret, root / "secret-alias")
                output = root / "acl/users.acl"
                output.parent.mkdir(mode=0o700)
                output.write_text("previous-safe-acl\n")
                output.chmod(0o600)
                if case == "hardlink-output":
                    os.link(output, root / "output-alias")
                result, _, args_file = self._run_wrapper(root, secret)
                self.assertNotEqual(0, result.returncode)
                self.assertEqual("previous-safe-acl\n", output.read_text())
                self.assertFalse(args_file.exists())

    def test_wrapper_rejects_duplicate_default_and_monitor_secrets(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            secret = root / "secret"
            secret.write_text("synthetic-safe\n")
            secret.chmod(0o600)
            output = root / "acl/users.acl"
            output.parent.mkdir(mode=0o700)
            output.write_text("previous-safe-acl\n")
            output.chmod(0o600)
            result, _, args_file = self._run_wrapper(root, secret, monitor=secret)
            self.assertNotEqual(0, result.returncode)
            self.assertEqual("previous-safe-acl\n", output.read_text())
            self.assertFalse(args_file.exists())

    def test_signal_during_atomic_move_preserves_previous_acl(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            secret = root / "default"
            secret.write_text("synthetic-safe\n")
            secret.chmod(0o600)
            output = root / "acl/users.acl"
            output.parent.mkdir(mode=0o700)
            output.write_text("previous-safe-acl\n")
            output.chmod(0o600)
            fake = root / "bin/mv"
            fake.parent.mkdir()
            fake.write_text('#!/bin/sh\nkill -TERM "$PPID"\nsleep 1\nexit 1\n')
            fake.chmod(0o755)
            environment = os.environ.copy()
            environment["PATH"] = f"{fake.parent}:/usr/bin:/bin"
            result = subprocess.run(
                ["sh", str(VALKEY_RENDERER), str(secret), str(output)],
                cwd=ROOT,
                env=environment,
                capture_output=True,
                text=True,
                check=False,
                timeout=10,
            )
            self.assertNotEqual(0, result.returncode)
            self.assertEqual("previous-safe-acl\n", output.read_text())
            self.assertEqual([], list(output.parent.glob("users.acl.*")))


class GrafanaStaticRouteContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.labels = _service("infra/06-observability/docker-compose.yml", "grafana")[
            "labels"
        ]

    def test_allow_router_is_exact_get_head_and_uses_standard_chain(self) -> None:
        labels = self.labels
        rule = labels["traefik.http.routers.grafana-static.rule"]
        self.assertIn("Host(`grafana.${DEFAULT_URL}`)", rule)
        self.assertEqual(
            {"/favicon.ico", "/robots.txt"},
            set(re.findall(r"Path\(`([^`]+)`\)", rule)),
        )
        self.assertEqual({"GET", "HEAD"}, set(re.findall(r"`(GET|HEAD)`", rule)))
        self.assertIsNone(
            re.search(r"Method\(\s*`GET`\s*,", rule),
            "Traefik's Method matcher accepts one argument per matcher",
        )
        self.assertNotIn("PathPrefix", rule)
        self.assertEqual(
            200, int(labels["traefik.http.routers.grafana-static.priority"])
        )
        self.assertEqual(
            "gateway-standard-chain@file",
            labels["traefik.http.routers.grafana-static.middlewares"],
        )
        self.assertEqual(
            "grafana-svc", labels["traefik.http.routers.grafana-static.service"]
        )

    def test_deny_router_wins_and_terminates_without_grafana_fallback(self) -> None:
        labels = self.labels
        rule = labels.get("traefik.http.routers.grafana-static-deny.rule", "")
        self.assertEqual(
            {"/favicon.ico", "/robots.txt"},
            set(re.findall(r"Path\(`([^`]+)`\)", rule)),
        )
        self.assertEqual({"GET", "HEAD"}, set(re.findall(r"`(GET|HEAD)`", rule)))
        self.assertIsNone(
            re.search(r"Method\(\s*`GET`\s*,", rule),
            "Traefik's Method matcher accepts one argument per matcher",
        )
        self.assertIn("!", rule)
        self.assertEqual(
            201, int(labels["traefik.http.routers.grafana-static-deny.priority"])
        )
        self.assertEqual(
            "noop@internal",
            labels.get("traefik.http.routers.grafana-static-deny.service"),
        )
        self.assertEqual(
            "gateway-standard-chain@file",
            labels.get("traefik.http.routers.grafana-static-deny.middlewares"),
        )


if __name__ == "__main__":
    unittest.main()
