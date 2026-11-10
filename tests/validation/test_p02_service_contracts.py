"""P02 service listener, data endpoint, authentication and Valkey contracts."""

from __future__ import annotations

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


def _render_root(overrides: dict[str, str], profiles: tuple[str, ...] = ()) -> dict:
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
        for profile in profiles or (
            "core",
            "mng",
            "data",
            "admin-data",
            "iac",
            "obs",
            "workflow-airflow",
            "ai",
            "notebook",
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


# A documentation-only address (RFC 5737) marks LAN publications in the render.
LAN_SENTINEL = "198.51.100.7"
LOOPBACK = {"127.0.0.1", "::1"}
# The only host-LAN publications: the Traefik web gateway and the
# POL-0096 cluster exceptions (Loki, Tempo, Alloy OTLP, mng-valkey).
LAN_ALLOWED = {
    "traefik": {80, 443},
    "loki": {3100},
    "tempo": {3200},
    "alloy": {4317, 4318},
    "mng-valkey": {6379},
}


def _publication_violations(services: dict) -> list[str]:
    """Each host publication is loopback or an approved (service, port) on the LAN."""
    found = []
    for name, service in sorted(services.items()):
        for port in service.get("ports") or []:
            host, target = port.get("host_ip") or "0.0.0.0", int(port["target"])
            if host in LOOPBACK:
                continue
            if host == LAN_SENTINEL and target in LAN_ALLOWED.get(name, set()):
                continue
            found.append(f"{name}:{target} on {host}")
    return found


class HostPublicationContractTests(unittest.TestCase):
    def test_every_profile_publishes_only_loopback_or_approved_lan_ports(self) -> None:
        services = _render_root({"HOST_LAN_BIND_IP": LAN_SENTINEL}, ("*",))
        self.assertEqual([], _publication_violations(services))
        # The loopback consumers named by D02 stay published for host callers.
        for name in ("ollama", "open_notebook", "pact-broker", "wiremock"):
            hosts = {p.get("host_ip") for p in services[name].get("ports") or []}
            self.assertEqual({"127.0.0.1"}, hosts, name)

    def test_wildcard_omitted_and_unapproved_lan_publications_are_rejected(
        self,
    ) -> None:
        def one(name, **port):
            return {name: {"ports": [{"target": 8080, **port}]}}

        for services in (
            one("ollama", host_ip="0.0.0.0"),
            one("ollama"),
            one("ollama", host_ip="::"),
            one("ollama", host_ip=LAN_SENTINEL),
            {"loki": {"ports": [{"target": 9999, "host_ip": LAN_SENTINEL}]}},
        ):
            with self.subTest(services=services):
                self.assertTrue(_publication_violations(services))
        self.assertEqual(
            [], _publication_violations(one("wiremock", host_ip="127.0.0.1"))
        )


# SPEC-0266: Traefik backends whose only access control is sso-auth (W1 inventory).
SSO_ONLY_BACKENDS = (
    "alertmanager",
    "alloy",
    "cadvisor",
    "comfyui",
    "flower",
    "loki",
    "mailpit",
    "mlflow",
    "ollama",
    "prometheus",
    "pushgateway",
    "pyroscope",
    "tempo",
    "terrakube-ui",
)
RETIRED_SUBNETS = {"10.250.9.0/24", "10.250.12.0/24"}


def _ingress_network(service: str) -> str:
    return service.replace("-", "_") + "_ingress_net"


COMFYUI_EGRESS_OVERLAY = "infra/08-ai/comfyui/docker-compose.egress.yml"


def _render_all_profiles(*overlays: str) -> dict:
    """Render every profile from `.env.example`, without a Docker daemon."""
    with tempfile.TemporaryDirectory() as directory:
        env = Path(directory) / "public.env"
        env.write_bytes((ROOT / ".env.example").read_bytes())
        result = subprocess.run(
            [
                "docker",
                "compose",
                "--project-directory",
                str(ROOT),
                "--env-file",
                str(env),
                "-f",
                str(ROOT / "docker-compose.yml"),
                *[arg for overlay in overlays for arg in ("-f", str(ROOT / overlay))],
                "--profile",
                "*",
                "config",
                "--format",
                "json",
            ],
            cwd=ROOT,
            env={
                "COMPOSE_DISABLE_ENV_FILE": "1",
                "DOCKER_CONFIG": str(Path(directory) / "docker-config"),
                "DOCKER_HOST": f"unix://{directory}/no-daemon.sock",
                "HOME": directory,
                "PATH": os.environ["PATH"],
            },
            capture_output=True,
            text=True,
            check=False,
            timeout=120,
        )
    if result.returncode:
        raise AssertionError("public Compose configuration did not render")
    return __import__("json").loads(result.stdout)


class SsoOnlyIngressContractTests(unittest.TestCase):
    """Only Traefik reaches an SSO-only backend (SPEC-0266, ADR-0061)."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.config = _render_all_profiles()
        cls.services = cls.config["services"]
        cls.members: dict[str, set[str]] = {}
        for name, service in cls.services.items():
            for network in service.get("networks") or {}:
                cls.members.setdefault(network, set()).add(name)

    def test_each_sso_only_backend_is_reachable_only_from_traefik(self) -> None:
        for name in SSO_ONLY_BACKENDS:
            with self.subTest(service=name):
                service = self.services[name]
                network = _ingress_network(name)
                self.assertNotIn("edge_net", service["networks"])
                self.assertIn(network, service["networks"])
                self.assertEqual({name, "traefik"}, self.members[network])
                declared = self.config["networks"][network]
                self.assertTrue(declared.get("internal"))
                self.assertEqual(
                    "isolated",
                    (declared.get("driver_opts") or {}).get(
                        "com.docker.network.bridge.gateway_mode_ipv4"
                    ),
                )
                self.assertEqual(
                    network, service["labels"].get("traefik.docker.network")
                )

    def test_seaweedfs_s3_metrics_keep_a_non_edge_path(self) -> None:
        # Prometheus and Alloy scrape seaweedfs-s3:9327 (W1 inventory) on a
        # network that reaches no master/volume/filer API.
        self.assertEqual(
            {"seaweedfs-s3", "prometheus", "alloy"},
            self.members["seaweedfs_s3_metrics_net"],
        )
        self.assertTrue(self.config["networks"]["seaweedfs_s3_metrics_net"]["internal"])
        self.assertNotIn("alloy", self.members["seaweedfs_metrics_net"])

    def test_comfyui_has_no_outbound_access_or_host_port_by_default(self) -> None:
        # SPEC-0268: outbound access and the loopback port come only from the
        # maintenance overlay; the default render reaches ComfyUI through
        # Traefik alone.
        self.assertEqual(
            {"comfyui_ingress_net"}, set(self.services["comfyui"]["networks"])
        )
        self.assertNotIn("ports", self.services["comfyui"])
        self.assertNotIn("comfyui_egress_net", self.members)

    def test_comfyui_egress_overlay_adds_only_egress_and_loopback_port(self) -> None:
        optional = _render_all_profiles(COMFYUI_EGRESS_OVERLAY)
        comfyui = optional["services"]["comfyui"]
        self.assertEqual(
            {"comfyui_ingress_net", "comfyui_egress_net"}, set(comfyui["networks"])
        )
        self.assertFalse(optional["networks"]["comfyui_egress_net"].get("internal"))
        self.assertEqual(
            [("127.0.0.1", "8188", 8188)],
            [
                (port.get("host_ip"), str(port.get("published")), port.get("target"))
                for port in comfyui.get("ports") or []
            ],
        )
        for name, service in optional["services"].items():
            if name == "comfyui":
                continue
            with self.subTest(service=name):
                base = self.services[name]
                self.assertEqual(
                    set(base.get("networks") or {}), set(service.get("networks") or {})
                )
                self.assertEqual(base.get("ports"), service.get("ports"))

    def test_subnets_are_distinct_and_avoid_retired_ranges(self) -> None:
        import ipaddress

        subnets = []
        for name, network in self.config["networks"].items():
            for block in (network.get("ipam") or {}).get("config") or []:
                if block.get("subnet"):
                    subnets.append((name, ipaddress.ip_network(block["subnet"])))
        for index, (name, subnet) in enumerate(subnets):
            self.assertNotIn(str(subnet), RETIRED_SUBNETS, name)
            for other, second in subnets[index + 1 :]:
                self.assertFalse(subnet.overlaps(second), f"{name} and {other}")


# Secondary listeners bound to one address on a consumer-only network
# (SPEC-0267). Each row: service, network, fixed address, alias, consumers.
SECONDARY_LISTENERS = (
    (
        "seaweedfs-s3",
        "seaweedfs_s3_metrics_net",
        "10.250.41.2",
        None,
        {"prometheus", "alloy"},
    ),
    (
        "oauth2-proxy",
        "oauth2_proxy_metrics_net",
        "10.250.43.2",
        "oauth2-proxy-metrics",
        {"prometheus"},
    ),
    (
        "keycloak",
        "keycloak_management_net",
        "10.250.44.2",
        "keycloak-management",
        {"prometheus", "gatus"},
    ),
    ("grafana", "grafana_pprof_net", "10.250.45.2", "grafana-pprof", {"alloy"}),
    (
        "traefik",
        "traefik_metrics_net",
        "10.250.46.2",
        "traefik-metrics",
        {"prometheus"},
    ),
    (
        "n8n-worker",
        "n8n_worker_runner_net",
        "10.250.23.2",
        None,
        {"n8n-task-runner-worker"},
    ),
)

# Consumer configuration that must name the network-scoped alias.
LISTENER_REFERENCES = {
    "infra/06-observability/prometheus/config/prometheus.yml": (
        ("traefik-metrics:8082", "traefik:8082"),
        ("oauth2-proxy-metrics:44180", "oauth2-proxy:44180"),
    ),
    "infra/06-observability/prometheus/config/prometheus.dev.yml": (
        ("traefik-metrics:8082", "traefik:8082"),
        ("oauth2-proxy-metrics:44180", "oauth2-proxy:44180"),
    ),
    "infra/06-observability/prometheus/scripts/start.sh": (
        ("keycloak-management:$keycloak_port", "keycloak:$keycloak_port"),
    ),
    "infra/06-observability/gatus/config/config.oidc.yaml": (
        (
            "keycloak-management:${KEYCLOAK_MANAGEMENT_PORT}",
            "keycloak:${KEYCLOAK_MANAGEMENT_PORT}",
        ),
    ),
    "infra/06-observability/gatus/config/config.yaml": (
        (
            "keycloak-management:${KEYCLOAK_MANAGEMENT_PORT}",
            "keycloak:${KEYCLOAK_MANAGEMENT_PORT}",
        ),
    ),
    "infra/06-observability/alloy/config/config.alloy": (
        ("grafana-pprof:6060", "grafana:6060"),
    ),
    "infra/06-observability/alloy/config/config.home.alloy": (
        ("grafana-pprof:6060", "grafana:6060"),
    ),
}


class SecondaryListenerContractTests(unittest.TestCase):
    """Unauthenticated secondary listeners reach only their consumers (SPEC-0267)."""

    setUpClass = classmethod(SsoOnlyIngressContractTests.setUpClass.__func__)

    def _bind_value(self, name: str) -> str:
        service = self.services[name]
        environment = service.get("environment") or {}
        if name == "seaweedfs-s3":
            flags = [arg for arg in service["command"] if arg.startswith("-metricsIp=")]
            return flags[0].split("=", 1)[1] if flags else ""
        if name == "traefik":
            import yaml

            static = yaml.safe_load(
                (ROOT / "infra/01-gateway/traefik/config/traefik.yml").read_text()
            )
            return static["entryPoints"]["metrics"]["address"].rsplit(":", 1)[0]
        key = {
            "oauth2-proxy": "OAUTH2_PROXY_METRICS_ADDRESS",
            "keycloak": "KC_HTTP_MANAGEMENT_HOST",
            "grafana": "GF_DIAGNOSTICS_PROFILING_ADDR",
            "n8n": "N8N_RUNNERS_BROKER_LISTEN_ADDRESS",
            "n8n-worker": "N8N_RUNNERS_BROKER_LISTEN_ADDRESS",
        }[name]
        value = str(environment.get(key, ""))
        return value.rsplit(":", 1)[0] if name == "oauth2-proxy" else value

    def test_each_listener_binds_one_address_on_a_consumer_only_network(self) -> None:
        import ipaddress

        for name, network, address, alias, consumers in SECONDARY_LISTENERS:
            with self.subTest(service=name):
                self.assertEqual({name} | consumers, self.members.get(network))
                declared = self.config["networks"][network]
                self.assertTrue(declared.get("internal"))
                self.assertEqual(
                    "isolated",
                    (declared.get("driver_opts") or {}).get(
                        "com.docker.network.bridge.gateway_mode_ipv4"
                    ),
                )
                block = declared["ipam"]["config"][0]
                dynamic = ipaddress.ip_network(block["ip_range"])
                self.assertNotIn(ipaddress.ip_address(address), dynamic)
                self.assertIn(
                    ipaddress.ip_address(address), ipaddress.ip_network(block["subnet"])
                )
                attachment = self.services[name]["networks"][network] or {}
                self.assertEqual(address, attachment.get("ipv4_address"))
                if alias:
                    self.assertIn(alias, attachment.get("aliases") or [])
                self.assertEqual(address, self._bind_value(name))

    def test_grafana_metrics_require_basic_auth(self) -> None:
        # Grafana serves /metrics on the routed port 3000, so it cannot be
        # bound apart; built-in basic auth guards it instead (SPEC-0267).
        import json

        import yaml

        secret = "grafana_metrics_password"
        environment = self.services["grafana"]["environment"]
        self.assertEqual(
            "prometheus", environment.get("GF_METRICS_BASIC_AUTH_USERNAME")
        )
        self.assertEqual(
            f"/run/secrets/{secret}",
            environment.get("GF_METRICS_BASIC_AUTH_PASSWORD__FILE"),
        )
        self.assertNotIn("GF_METRICS_BASIC_AUTH_PASSWORD", environment)
        for name in ("grafana", "prometheus"):
            with self.subTest(service=name):
                sources = {
                    item.get("source")
                    for item in self.services[name].get("secrets") or []
                }
                self.assertIn(secret, sources)
        for relative in (
            "infra/06-observability/prometheus/config/prometheus.yml",
            "infra/06-observability/prometheus/config/prometheus.dev.yml",
        ):
            with self.subTest(file=relative):
                jobs = yaml.safe_load((ROOT / relative).read_text())["scrape_configs"]
                job = next(item for item in jobs if item["job_name"] == "grafana")
                self.assertEqual(
                    {
                        "username": "prometheus",
                        "password_file": f"/run/secrets/{secret}",
                    },
                    job.get("basic_auth"),
                )
        catalog = json.loads(
            (ROOT / "infra/03-security/openbao/secret-catalog.json").read_text()
        )
        entries = [
            entry
            for entry in catalog["entries"]
            if entry.get("source_path") == f"secrets/observability/grafana/{secret}.txt"
        ]
        self.assertEqual(1, len(entries))
        self.assertIn(
            "infra/06-observability/docker-compose.yml", entries[0]["consumers"]
        )

    def test_observation_aliases_match_compose(self) -> None:
        from scripts.lib.ops.compose_observation import TARGET_ALIASES

        self.assertEqual(
            {alias: name for name, _, _, alias, _ in SECONDARY_LISTENERS if alias},
            TARGET_ALIASES,
        )

    def test_health_checks_use_the_bound_address(self) -> None:
        for name in ("keycloak", "n8n-worker"):
            with self.subTest(service=name):
                address = dict((row[0], row[2]) for row in SECONDARY_LISTENERS)[name]
                test = " ".join(self.services[name]["healthcheck"]["test"])
                self.assertIn(address, test)
                self.assertNotIn("127.0.0.1", test)

    def test_consumers_name_the_network_scoped_alias(self) -> None:
        for relative, pairs in LISTENER_REFERENCES.items():
            text = (ROOT / relative).read_text()
            for wanted, retired in pairs:
                with self.subTest(file=relative, target=wanted):
                    self.assertIn(wanted, text)
                    self.assertNotIn(retired, text)

    def test_state_lives_on_declared_volumes(self) -> None:
        def named_targets(service: str) -> dict[str, str]:
            return {
                mount["target"]: mount.get("source", "")
                for mount in self.services[service].get("volumes") or []
                if mount.get("type") == "volume"
            }

        declared = set(self.config.get("volumes") or {})
        pyroscope = named_targets("pyroscope")
        self.assertIn("/data", pyroscope)
        self.assertIn(pyroscope["/data"], declared)
        comfyui = named_targets("comfyui")
        for directory in ("models", "custom_nodes", "input", "output", "user"):
            with self.subTest(comfyui=directory):
                target = f"/root/ComfyUI/{directory}"
                self.assertIn(target, comfyui)
                self.assertIn(comfyui[target], declared)
        self.assertFalse([t for t in comfyui if t.startswith("/opt/comfyui")])


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
            '10.250.44.2/"$${KC_HTTP_MANAGEMENT_PORT}"',
            " ".join(service["healthcheck"]["test"]),
        )

    def test_open_webui_lab_listener_health_and_port_use_one_port(self) -> None:
        # ADR-0062 amendment: a LAB with no gateway route; the listener is fixed.
        service = _service("labs/open-webui/docker-compose.yml", "open-webui")
        environment = _environment(service)
        self.assertEqual("8080", environment.get("PORT"))
        self.assertEqual(
            ["${LAB_HOST_BIND_IP:-127.0.0.1}:${LAB_OPEN_WEBUI_HOST_PORT:-18095}:8080"],
            service["ports"],
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
        "labs/open-webui/docker-compose.yml",
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


class N8nAssistantSearchContractTests(unittest.TestCase):
    """The n8n Assistant reaches SearXNG only over a private internal network."""

    N8N = "infra/07-workflow/n8n/docker-compose.yml"

    def test_searxng_is_internal_unpublished_and_unprivileged(self) -> None:
        data = _compose(self.N8N)
        service = data["services"]["searxng"]
        self.assertNotIn("ports", service)
        self.assertFalse(service.get("privileged", False))
        self.assertEqual("false", service["labels"]["traefik.enable"])
        self.assertEqual(
            {"n8n_search_net", "n8n_search_outbound_net"}, set(service["networks"])
        )
        self.assertIs(True, data["networks"]["n8n_search_net"]["internal"])
        self.assertNotIn("internal", data["networks"]["n8n_search_outbound_net"])

    def test_only_n8n_main_and_searxng_share_the_search_network(self) -> None:
        services = _compose(self.N8N)["services"]
        members = {
            name
            for name, service in services.items()
            if "n8n_search_net" in (service.get("networks") or {})
        }
        self.assertEqual({"n8n", "searxng"}, members)
        outbound = {
            name
            for name, service in services.items()
            if "n8n_search_outbound_net" in (service.get("networks") or {})
        }
        self.assertEqual({"searxng"}, outbound)

    def test_assistant_uses_the_internal_search_and_a_model_without_a_key(self) -> None:
        environment = _compose(self.N8N)["services"]["n8n"]["environment"]
        self.assertEqual(
            "http://searxng:8080", environment["N8N_INSTANCE_AI_SEARXNG_URL"]
        )
        # An env-set model makes n8n reject the model chosen in the Assistant UI.
        self.assertNotIn("N8N_INSTANCE_AI_MODEL", environment)
        self.assertNotIn("N8N_INSTANCE_AI_MODEL_API_KEY", environment)
        # The code sandbox was held back until the owner chose the privileged
        # Docker-in-Docker runner on 2026-11-09 (see N8nCodeSandboxContractTests).
        self.assertEqual(
            "true", str(environment["N8N_INSTANCE_AI_SANDBOX_ENABLED"]).lower()
        )


class N8nCodeSandboxContractTests(unittest.TestCase):
    """The Assistant code sandbox is the one privileged service, contained (owner, 2026-11-09)."""

    N8N = "infra/07-workflow/n8n/docker-compose.yml"
    SANDBOX = ("n8n-sandbox-certs", "n8n-sandbox-api", "n8n-sandbox-runner-1")

    def setUp(self) -> None:
        self.data = _compose(self.N8N)
        self.services = self.data["services"]

    def test_only_the_runner_is_privileged(self) -> None:
        privileged = sorted(
            name for name, service in self.services.items() if service.get("privileged")
        )
        self.assertEqual(["n8n-sandbox-runner-1"], privileged)

    def test_sandbox_services_have_no_ports_route_or_host_socket(self) -> None:
        for name in self.SANDBOX:
            with self.subTest(service=name):
                service = self.services[name]
                self.assertNotIn("ports", service)
                self.assertEqual("false", service["labels"]["traefik.enable"])
                self.assertEqual(["n8n-sandbox"], service["profiles"])
                mounts = " ".join(str(item) for item in service.get("volumes") or [])
                self.assertNotIn("docker.sock", mounts)

    def test_networks_keep_the_runner_away_from_n8n(self) -> None:
        members = {}
        for name, service in self.services.items():
            for network in service.get("networks") or {}:
                members.setdefault(network, set()).add(name)
        self.assertEqual({"n8n", "n8n-sandbox-api"}, members["n8n_sandbox_net"])
        self.assertEqual(
            {"n8n-sandbox-api", "n8n-sandbox-runner-1"},
            members["n8n_sandbox_runner_net"],
        )
        self.assertEqual({"n8n-sandbox-runner-1"}, members["n8n_sandbox_outbound_net"])
        self.assertEqual(
            {"n8n_sandbox_runner_net", "n8n_sandbox_outbound_net"},
            set(self.services["n8n-sandbox-runner-1"]["networks"]),
        )
        self.assertIs(True, self.data["networks"]["n8n_sandbox_net"]["internal"])
        self.assertIs(True, self.data["networks"]["n8n_sandbox_runner_net"]["internal"])
        self.assertNotIn("internal", self.data["networks"]["n8n_sandbox_outbound_net"])
        self.assertEqual("none", self.services["n8n-sandbox-certs"].get("network_mode"))

    def test_images_are_digest_pinned_and_share_one_release(self) -> None:
        refs = [
            self.services["n8n-sandbox-api"]["image"],
            self.services["n8n-sandbox-certs"]["image"],
            self.services["n8n-sandbox-runner-1"]["image"],
            self.services["n8n-sandbox-runner-1"]["environment"][
                "SANDBOX_RUNNER_DOCKER_SANDBOX_IMAGE"
            ],
        ]
        for ref in refs:
            self.assertRegex(
                ref, r"^n8nio/n8n-sandbox-service-[a-z-]+:1\.8\.1@sha256:[0-9a-f]{64}$"
            )

    def test_keys_come_from_secret_files_not_environment_values(self) -> None:
        n8n = self.services["n8n"]
        self.assertEqual(
            "/run/secrets/n8n_sandbox_api_key",
            n8n["environment"]["N8N_SANDBOX_SERVICE_API_KEY_FILE"],
        )
        self.assertNotIn("N8N_SANDBOX_SERVICE_API_KEY", n8n["environment"])
        for name in ("n8n-sandbox-api", "n8n-sandbox-runner-1"):
            literal = {
                "SANDBOX_API_KEYS",
                "SANDBOX_API_RUNNER_API_KEY",
                "SANDBOX_API_RUNNER_REGISTRATION_TOKEN",
                "SANDBOX_RUNNER_API_KEYS",
                "SANDBOX_RUNNER_REGISTRATION_TOKEN",
            }
            self.assertFalse(literal & set(self.services[name]["environment"]))
        self.assertEqual(
            ["n8n_sandbox_runner_registration_token", "n8n_sandbox_runner_api_key"],
            self.services["n8n-sandbox-runner-1"]["secrets"],
        )

    def test_the_privilege_exception_names_only_the_runner(self) -> None:
        import json

        exceptions = json.loads(
            (ROOT / "infra/common-optimizations.exceptions.json").read_text(
                encoding="utf-8"
            )
        )["exceptions"]
        privileged = sorted(
            item["service"] for item in exceptions if item["control"] == "privileged"
        )
        self.assertEqual(["cadvisor", "n8n-sandbox-runner-1"], privileged)


class SandboxCertificateJobTests(unittest.TestCase):
    def test_ca_key_is_removed_on_every_exit_path(self):
        compose = (ROOT / "infra/07-workflow/n8n/docker-compose.yml").read_text()
        self.assertIn("trap 'rm -f /tls/ca.key' EXIT;", compose)


if __name__ == "__main__":
    unittest.main()
