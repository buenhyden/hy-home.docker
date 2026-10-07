import hashlib
import importlib.util
import itertools
import json
import pathlib
import sys
import tempfile
import types
import unittest
from unittest import mock

ROOT = pathlib.Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "infra/11-quality/k6/quality_run.py"
sys.path.insert(0, str(MODULE_PATH.parent))
SPEC = importlib.util.spec_from_file_location("quality_run", MODULE_PATH)
quality_run = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(quality_run)
IMPORT_MODULE_PATH = ROOT / "infra/11-quality/k6/result_import.py"
IMPORT_SPEC = importlib.util.spec_from_file_location(
    "result_import", IMPORT_MODULE_PATH
)
result_import = importlib.util.module_from_spec(IMPORT_SPEC)
assert IMPORT_SPEC.loader is not None
IMPORT_SPEC.loader.exec_module(result_import)
EXECUTOR_PATH = ROOT / "infra/11-quality/k6/container_executor.py"
EXECUTOR_SPEC = importlib.util.spec_from_file_location(
    "container_executor", EXECUTOR_PATH
)
container_executor = importlib.util.module_from_spec(EXECUTOR_SPEC)
assert EXECUTOR_SPEC.loader is not None
sys.modules["container_executor"] = container_executor
EXECUTOR_SPEC.loader.exec_module(container_executor)


def canonical(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


class K6ResultContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.temp.name)
        self.scenarios = self.root / "scenarios"
        self.scenarios.mkdir()
        self.scenario = self.scenarios / "smoke.js"
        self.scenario.write_text("export default function () {}\n", encoding="utf-8")
        self.manifest = {
            "schema_version": "hyhome.quality-run/v1",
            "run_id": "12345678-1234-4abc-8def-1234567890ab",
            "attempt": 1,
            "project_id": "sample-a",
            "environment": "test",
            "generator": "k6",
            "source_revision": "a" * 40,
            "tool_image": "grafana/k6@sha256:" + "b" * 64,
            "fixture_sha256": hashlib.sha256(self.scenario.read_bytes()).hexdigest(),
            "scenario_path": "smoke.js",
            "mock_mode": "function",
            "target": {
                "origin": "http://wiremock:8080",
                "allowed_origins": ["http://wiremock:8080"],
                "allowed_networks": ["10.250.11.0/24"],
                "paths": ["/health", "/v1/items"],
            },
            "redirects": {"policy": "deny", "max_redirects": 0},
            "budget": {
                "users": 2,
                "rate_per_second": 5,
                "duration_seconds": 30,
                "max_iterations": 100,
                "cpu_millis": 500,
                "memory_mib": 256,
            },
            "thresholds": {"http_req_failed": ["rate<0.01"]},
        }

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write_manifest(self, value: object | None = None) -> pathlib.Path:
        path = self.root / "run.json"
        path.write_bytes(canonical(self.manifest if value is None else value))
        return path

    def prepare(self) -> pathlib.Path:
        attempt = self.root / "attempt"
        quality_run.prepare(self.write_manifest(), self.scenarios, attempt)
        return attempt

    @staticmethod
    def summary(*, samples: int = 2, threshold_ok: bool = True) -> dict[str, object]:
        return {
            "metrics": {
                "iterations": {
                    "type": "counter",
                    "contains": "default",
                    "values": {"count": samples, "rate": 1.0},
                },
                "http_req_failed": {
                    "type": "rate",
                    "contains": "default",
                    "values": {"rate": 0.0, "passes": samples, "fails": 0},
                    "thresholds": {"rate<0.01": {"ok": threshold_ok}},
                },
            }
        }

    def write_execution(
        self,
        attempt: pathlib.Path,
        *,
        exit_code: int = 0,
        execution_state: str = "completed",
        summary: object | None = None,
    ) -> None:
        (attempt / "raw-summary.json").write_bytes(
            canonical(self.summary() if summary is None else summary)
        )
        (attempt / "exit.json").write_bytes(
            canonical(
                {
                    "schema_version": "hyhome.quality-exit/v1",
                    "execution_state": execution_state,
                    "exit_code": exit_code,
                    "started_at": "2026-10-03T00:00:00Z",
                    "ended_at": "2026-10-03T00:00:01Z",
                }
            )
        )

    def test_manifest_rejects_public_origin_admin_path_and_excess_budget(self) -> None:
        quality_run.validate_manifest(self.manifest)
        invalid = json.loads(json.dumps(self.manifest))
        invalid["target"]["origin"] = "https://example.com"
        invalid["target"]["allowed_origins"] = ["https://example.com"]
        with self.assertRaisesRegex(quality_run.ContractError, "public target"):
            quality_run.validate_manifest(invalid)

        invalid = json.loads(json.dumps(self.manifest))
        invalid["target"]["paths"] = ["/admin/users"]
        with self.assertRaisesRegex(quality_run.ContractError, "management path"):
            quality_run.validate_manifest(invalid)

        invalid = json.loads(json.dumps(self.manifest))
        invalid["budget"]["duration_seconds"] = 3601
        with self.assertRaisesRegex(quality_run.ContractError, "duration_seconds"):
            quality_run.validate_manifest(invalid)

        invalid = json.loads(json.dumps(self.manifest))
        invalid["redirects"] = {"policy": "same-origin", "max_redirects": 1}
        with self.assertRaisesRegex(quality_run.ContractError, "deny all redirects"):
            quality_run.validate_manifest(invalid)

        invalid = json.loads(json.dumps(self.manifest))
        invalid["target"]["allowed_networks"] = ["0.0.0.0/0"]
        with self.assertRaisesRegex(quality_run.ContractError, "private"):
            quality_run.validate_manifest(invalid)

        invalid = json.loads(json.dumps(self.manifest))
        invalid["target"]["origin"] = "http://localhost:8080"
        invalid["target"]["allowed_origins"] = ["http://localhost:8080"]
        with self.assertRaisesRegex(quality_run.ContractError, "public target"):
            quality_run.validate_manifest(invalid)

    def test_manifest_rejects_wiremock_admin_and_noncanonical_paths(self) -> None:
        for path in (
            "/__admin",
            "/__admin/requests",
            "/%61dmin",
            "/v1/../admin",
            "/v1//items",
            "/v1\\items",
            "/v1/\nitems",
        ):
            with self.subTest(path=path):
                invalid = json.loads(json.dumps(self.manifest))
                invalid["target"]["paths"] = [path]
                with self.assertRaises(quality_run.ContractError):
                    quality_run.validate_manifest(invalid)

    def test_rehearsal_checks_still_reject_failure_when_python_is_optimized(
        self,
    ) -> None:
        import subprocess

        controller = ROOT / "examples/operations/quality-path-guard/acceptance.py"
        program = (
            "import runpy; "
            f"module = runpy.run_path({str(controller)!r}); "
            "module['require_result'](0, {'verdict': 'failed_threshold', "
            "'evidence_state': 'complete'}, 0, 'passed')"
        )
        result = subprocess.run(
            [sys.executable, "-O", "-c", program],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("synthetic quality acceptance failed", result.stderr)

    def test_prepare_binds_scenario_and_refuses_existing_attempt(self) -> None:
        attempt = self.prepare()
        self.assertEqual(
            (attempt / "manifest.json").read_bytes(), canonical(self.manifest)
        )
        with self.assertRaisesRegex(quality_run.ContractError, "already exists"):
            quality_run.prepare(self.write_manifest(), self.scenarios, attempt)

        changed = dict(self.manifest, fixture_sha256="0" * 64)
        with self.assertRaisesRegex(quality_run.ContractError, "fixture_sha256"):
            quality_run.prepare(
                self.write_manifest(changed), self.scenarios, self.root / "attempt-2"
            )

    def test_threshold_and_exit_code_produce_distinct_failed_verdict(self) -> None:
        attempt = self.prepare()
        self.write_execution(attempt, summary=self.summary(threshold_ok=False))
        final = quality_run.finalize(attempt)
        self.assertEqual(final["execution_state"], "completed")
        self.assertEqual(final["evidence_state"], "complete")
        self.assertEqual(final["verdict"], "failed_threshold")

        second = self.root / "attempt-2"
        quality_run.prepare(self.write_manifest(), self.scenarios, second)
        self.write_execution(second, exit_code=107)
        final = quality_run.finalize(second)
        self.assertEqual(final["verdict"], "failed_execution")
        self.assertEqual(final["exit_code"], 107)

    def network_record(self, *, internal: bool = True, peers: int = 1) -> list[object]:
        containers = {
            f"peer-{index}": {
                "Name": "wiremock" if index == 0 else f"unexpected-{index}",
                "IPv4Address": f"10.250.11.{10 + index}/24",
                "IPv6Address": "",
            }
            for index in range(peers)
        }
        return [
            {
                "Id": "network-123",
                "Name": "hyhome-quality-12345678-a1",
                "Driver": "bridge",
                "Scope": "local",
                "Internal": internal,
                "Attachable": False,
                "Labels": {
                    "hyhome.quality.run_id": self.manifest["run_id"],
                    "hyhome.quality.purpose": "k6-wiremock",
                },
                "IPAM": {"Config": [{"Subnet": "10.250.11.0/24"}]},
                "Containers": containers,
            }
        ]

    def peer_record(self) -> list[object]:
        return [
            {
                "Id": "peer-0-full-id",
                "Name": "/wiremock",
                "State": {"Running": True},
                "Config": {
                    "Labels": {
                        "hyhome.quality.run_id": self.manifest["run_id"],
                        "hyhome.quality.role": "wiremock",
                        "hyhome.quality.mock_mode": self.manifest["mock_mode"],
                    },
                    "Cmd": ["--admin-api-require-https"],
                    "ExposedPorts": {"8080/tcp": {}},
                },
                "HostConfig": {"PortBindings": {}, "ExtraHosts": []},
                "NetworkSettings": {
                    "Networks": {
                        "hyhome-quality-12345678-a1": {
                            "Aliases": ["wiremock"],
                            "IPAddress": "10.250.11.10",
                        }
                    },
                    "Ports": {},
                },
            }
        ]

    def test_guarded_executor_runs_only_exact_two_network_fixture(self) -> None:
        from http_guard import COMMAND, configuration

        self.manifest["mock_mode"] = "load"
        config_path = self.root / "routes.json"
        config_path.write_bytes(canonical(configuration(self.manifest)))
        gateway = self.peer_record()[0]
        gateway["Config"].update(
            {
                "Image": "traefik@sha256:" + "c" * 64,
                "Cmd": COMMAND,
                "Env": ["PATH=/usr/bin"],
                "Labels": {
                    "hyhome.quality.run_id": self.manifest["run_id"],
                    "hyhome.quality.role": "http-guard",
                },
            }
        )
        gateway["HostConfig"].update(
            {
                "ReadonlyRootfs": True,
                "Privileged": False,
                "CapDrop": ["ALL"],
                "CapAdd": [],
            }
        )
        gateway["Mounts"] = [
            {
                "Type": "bind",
                "Source": str(config_path),
                "Destination": "/guard/routes.yml",
                "RW": False,
            }
        ]
        gateway["NetworkSettings"]["Networks"]["backend-test"] = {"Aliases": ["guard"]}
        backend = self.peer_record()[0]
        backend["Id"] = "backend-id"
        backend["Config"]["Cmd"] += ["--no-request-journal"]
        backend["Config"]["ExposedPorts"]["8443/tcp"] = {}
        backend["Name"] = "/backend"
        backend["NetworkSettings"]["Networks"] = {
            "backend-test": {"Aliases": ["wiremock", "quality-backend"]}
        }
        network = self.network_record()[0]
        backend_network = dict(
            network,
            Name="backend-test",
            Containers={
                gateway["Id"]: {"Name": "wiremock"},
                backend["Id"]: {"Name": "backend"},
            },
        )
        calls = []

        def fake_run(command, **kwargs):
            calls.append(command)
            if command[3:5] == ["network", "inspect"]:
                record = backend_network if command[-1] == "backend-test" else network
            elif command[3:5] == ["container", "inspect"]:
                record = backend if command[-1] == "backend" else gateway
            else:
                self.assertIn("--max-redirects", command)
                self.assertIn("network-123", command)
                return types.SimpleNamespace(returncode=99)
            return types.SimpleNamespace(
                returncode=0, stdout=json.dumps([record]), stderr=""
            )

        for mutation in (
            "none",
            "bad-config",
            "extra-peer",
            "extra-provider",
            "published-port",
            "malformed-gateway",
            "missing-journal-policy",
            "function-mode",
        ):
            with self.subTest(mutation=mutation):
                attempt = self.root / mutation
                quality_run.prepare(self.write_manifest(), self.scenarios, attempt)
                original_config = config_path.read_bytes()
                if mutation == "bad-config":
                    config_path.write_bytes(b"{}")
                if mutation == "extra-peer":
                    backend_network["Containers"]["unexpected"] = {"Name": "HOME"}
                if mutation == "extra-provider":
                    gateway["Config"]["Cmd"] = [*COMMAND, "--providers.docker=true"]
                if mutation == "published-port":
                    gateway["HostConfig"]["PortBindings"] = {
                        "8080/tcp": [{"HostPort": "8080"}]
                    }
                if mutation == "missing-journal-policy":
                    backend["Config"]["Cmd"] = ["--admin-api-require-https"]
                if mutation == "function-mode":
                    self.manifest["mock_mode"] = "function"
                if mutation == "malformed-gateway":
                    gateway["HostConfig"] = None
                before = len(calls)
                with mock.patch.object(
                    container_executor.subprocess, "run", side_effect=fake_run
                ):
                    if mutation == "none":
                        result = container_executor.execute(
                            self.manifest,
                            self.scenarios,
                            attempt,
                            network["Name"],
                            "wiremock",
                            "/synthetic/docker",
                            "default",
                            config_path,
                            "backend-test",
                            "backend",
                        )
                        self.assertEqual(result, 99)
                        self.assertEqual(
                            json.loads((attempt / "exit.json").read_bytes())[
                                "exit_code"
                            ],
                            99,
                        )
                        self.assertEqual(len(calls) - before, 5)
                    else:
                        with self.assertRaises(container_executor.ExecutorError):
                            container_executor.execute(
                                self.manifest,
                                self.scenarios,
                                attempt,
                                network["Name"],
                                "wiremock",
                                "/synthetic/docker",
                                "default",
                                config_path,
                                "backend-test",
                                "backend",
                            )
                        self.assertFalse(
                            any("run" in command for command in calls[before:])
                        )
                self.manifest["mock_mode"] = "load"
                config_path.write_bytes(original_config)
                backend_network["Containers"].pop("unexpected", None)
                gateway["Config"]["Cmd"] = COMMAND
                backend["Config"]["Cmd"] = [
                    "--admin-api-require-https",
                    "--no-request-journal",
                ]
                gateway["HostConfig"] = {
                    "PortBindings": {},
                    "ExtraHosts": [],
                    "ReadonlyRootfs": True,
                    "Privileged": False,
                    "CapDrop": ["ALL"],
                    "CapAdd": [],
                }

    def test_manifest_v2_telemetry_is_closed_and_v1_stays_valid(self) -> None:
        self.assertEqual(
            "none",
            quality_run.validate_manifest(self.manifest).get(
                "telemetry", {"mode": "none"}
            )["mode"],
        )
        v2 = dict(self.manifest, schema_version="hyhome.quality-run/v2")
        for telemetry, accepted in (
            ({"mode": "none"}, True),
            ({"mode": "otlp"}, True),
            ({"mode": "prometheus-rw"}, False),
            ({"mode": "otlp", "endpoint": "http://alloy:4319"}, False),
            ("otlp", False),
            (None, False),
        ):
            with self.subTest(telemetry=telemetry):
                candidate = dict(v2)
                if telemetry is not None:
                    candidate["telemetry"] = telemetry
                if accepted:
                    quality_run.validate_manifest(candidate)
                else:
                    with self.assertRaises(quality_run.ContractError):
                        quality_run.validate_manifest(candidate)
        with self.assertRaises(quality_run.ContractError):
            quality_run.validate_manifest(
                dict(self.manifest, telemetry={"mode": "none"})
            )

    def test_otlp_runs_only_through_the_approved_metrics_ingress(self) -> None:
        self.manifest.update(
            schema_version="hyhome.quality-run/v2",
            telemetry={"mode": "otlp"},
            mock_mode="load",
        )
        network = self.network_record()[0]
        network["Containers"]["ingress-id"] = {
            "Name": "metrics-ingress",
            "IPv4Address": "10.250.11.20/24",
        }
        peer = self.peer_record()[0]
        ingress = {
            "Id": "ingress-id",
            "Name": "/metrics-ingress",
            "State": {"Running": True},
            "Config": {
                "Image": "grafana/alloy@sha256:" + "d" * 64,
                "Labels": {
                    "hyhome.quality.run_id": self.manifest["run_id"],
                    "hyhome.quality.role": "metrics-ingress",
                },
            },
            "HostConfig": {
                "ReadonlyRootfs": True,
                "Privileged": False,
                "CapDrop": ["ALL"],
                "CapAdd": [],
                "PortBindings": {},
            },
            "NetworkSettings": {
                "Networks": {
                    network["Name"]: {"Aliases": ["metrics-ingress"]},
                    "obs-relay": {"Aliases": []},
                }
            },
        }
        runs: list[list[str]] = []

        def fake_run(command, **kwargs):
            if command[3:5] == ["network", "inspect"]:
                record = network
            elif command[3:5] == ["container", "inspect"]:
                record = ingress if command[-1] == "metrics-ingress" else peer
            else:
                runs.append(command)
                return types.SimpleNamespace(returncode=0)
            return types.SimpleNamespace(
                returncode=0, stdout=json.dumps([record]), stderr=""
            )

        guard = types.SimpleNamespace(validate=lambda *args: None)

        def execute(attempt, metrics_peer="metrics-ingress", egress="obs-relay"):
            quality_run.prepare(self.write_manifest(), self.scenarios, attempt)
            with mock.patch.dict(sys.modules, {"http_guard": guard}):
                with mock.patch.object(
                    container_executor.subprocess, "run", side_effect=fake_run
                ):
                    return container_executor.execute(
                        self.manifest,
                        self.scenarios,
                        attempt,
                        network["Name"],
                        "wiremock",
                        "/synthetic/docker",
                        "default",
                        self.root / "routes.json",
                        "backend-test",
                        "backend",
                        metrics_peer,
                        egress,
                    )

        self.assertEqual(0, execute(self.root / "otlp"))
        command = runs[-1]
        pairs = list(itertools.pairwise(command))
        self.assertIn(("--out", "opentelemetry"), pairs)
        self.assertIn(("--out", "json=/results/raw-points.json"), pairs)
        settings = {
            value.split("=", 1)[0]: value.split("=", 1)[1]
            for flag, value in itertools.pairwise(command)
            if flag == "--env"
        }
        self.assertEqual(
            "metrics-ingress:4318", settings["K6_OTEL_HTTP_EXPORTER_ENDPOINT"]
        )
        self.assertEqual("http/protobuf", settings["K6_OTEL_EXPORTER_PROTOCOL"])
        self.assertEqual("k6_", settings["K6_OTEL_METRIC_PREFIX"])
        self.assertEqual(
            "project.id=sample-a,deployment.environment.name=test,"
            "service.instance.id=12345678-1234-4abc-8def-1234567890ab-a1",
            settings["OTEL_RESOURCE_ATTRIBUTES"],
        )
        self.assertFalse(any("token" in item.lower() for item in command))
        self.assertFalse(any("Authorization" in item for item in command))

        for name, mutate in (
            (
                "published",
                lambda: ingress["HostConfig"].update(PortBindings={"4318/tcp": [{}]}),
            ),
            ("writable", lambda: ingress["HostConfig"].update(ReadonlyRootfs=False)),
            ("image", lambda: ingress["Config"].update(Image="otel/collector:latest")),
            (
                "role",
                lambda: ingress["Config"]["Labels"].update(
                    {"hyhome.quality.role": "wiremock"}
                ),
            ),
            (
                "egress",
                lambda: ingress["NetworkSettings"]["Networks"].update(
                    {
                        "edge-net": ingress["NetworkSettings"]["Networks"].pop(
                            "obs-relay"
                        )
                    }
                ),
            ),
            (
                "alias",
                lambda: ingress["NetworkSettings"]["Networks"][network["Name"]].update(
                    Aliases=[]
                ),
            ),
        ):
            with self.subTest(mutation=name):
                saved = json.loads(json.dumps(ingress))
                mutate()
                before = len(runs)
                with self.assertRaises(container_executor.ExecutorError):
                    execute(self.root / f"bad-{name}")
                self.assertEqual(before, len(runs))
                ingress.clear()
                ingress.update(saved)
        with self.assertRaises(container_executor.ExecutorError):
            execute(self.root / "no-peer", metrics_peer=None)
        with self.assertRaises(container_executor.ExecutorError):
            execute(self.root / "no-egress", egress=None)
        with self.assertRaises(container_executor.ExecutorError):
            execute(self.root / "egress-is-run-net", egress=network["Name"])
        self.manifest["telemetry"] = {"mode": "none"}
        with self.assertRaises(container_executor.ExecutorError):
            execute(self.root / "unexpected-peer")

    def test_container_executor_prepares_limits_but_blocks_without_path_guard(
        self,
    ) -> None:
        attempt = self.root / "container-attempt"
        quality_run.prepare(self.write_manifest(), self.scenarios, attempt)
        calls: list[list[str]] = []

        def fake_run(command: list[str], **kwargs: object) -> object:
            calls.append(command)
            if command[3:5] == ["network", "inspect"]:
                return types.SimpleNamespace(
                    returncode=0,
                    stdout=json.dumps(self.network_record()),
                    stderr="",
                )
            if command[3:5] == ["container", "inspect"]:
                return types.SimpleNamespace(
                    returncode=0,
                    stdout=json.dumps(self.peer_record()),
                    stderr="",
                )
            raise AssertionError("k6 container execution must remain blocked")

        with mock.patch.object(
            container_executor.subprocess, "run", side_effect=fake_run
        ):
            with self.assertRaisesRegex(
                container_executor.ExecutorError, "path enforcement"
            ):
                container_executor.execute(
                    self.manifest,
                    self.scenarios,
                    attempt,
                    "hyhome-quality-12345678-a1",
                    "wiremock",
                    "/synthetic/docker",
                )
        self.assertEqual(len(calls), 2)
        exit_record = json.loads((attempt / "exit.json").read_text(encoding="utf-8"))
        self.assertEqual(exit_record["execution_state"], "interrupted")
        self.assertEqual(exit_record["error_class"], "path_confinement_unavailable")
        self.assertTrue((attempt / "scenario.js").is_file())
        self.assertTrue((attempt / "raw-summary.json").is_file())

    def test_container_executor_rejects_non_internal_or_shared_network(self) -> None:
        for name, network in (
            ("external", self.network_record(internal=False)),
            ("shared", self.network_record(peers=2)),
        ):
            with self.subTest(name=name):
                attempt = self.root / name
                quality_run.prepare(self.write_manifest(), self.scenarios, attempt)
                response = types.SimpleNamespace(
                    returncode=0, stdout=json.dumps(network), stderr=""
                )
                with mock.patch.object(
                    container_executor.subprocess, "run", return_value=response
                ):
                    with self.assertRaises(container_executor.ExecutorError):
                        container_executor.execute(
                            self.manifest,
                            self.scenarios,
                            attempt,
                            "hyhome-quality-12345678-a1",
                            "wiremock",
                            "/synthetic/docker",
                        )
                exit_record = json.loads(
                    (attempt / "exit.json").read_text(encoding="utf-8")
                )
                self.assertEqual(exit_record["execution_state"], "interrupted")
                self.assertEqual(
                    exit_record["error_class"], "isolation_preflight_failed"
                )

    def test_container_executor_rejects_wiremock_without_admin_https(self) -> None:
        attempt = self.root / "unsafe-wiremock"
        quality_run.prepare(self.write_manifest(), self.scenarios, attempt)
        peer = self.peer_record()
        del peer[0]["Config"]["Cmd"]

        def fake_run(command: list[str], **kwargs: object) -> object:
            record = (
                self.network_record()
                if command[3:5] == ["network", "inspect"]
                else peer
            )
            return types.SimpleNamespace(
                returncode=0, stdout=json.dumps(record), stderr=""
            )

        with mock.patch.object(
            container_executor.subprocess, "run", side_effect=fake_run
        ):
            with self.assertRaisesRegex(
                container_executor.ExecutorError, "peer isolation"
            ):
                container_executor.execute(
                    self.manifest,
                    self.scenarios,
                    attempt,
                    "hyhome-quality-12345678-a1",
                    "wiremock",
                    "/synthetic/docker",
                )
        exit_record = json.loads((attempt / "exit.json").read_text(encoding="utf-8"))
        self.assertEqual(exit_record["error_class"], "isolation_preflight_failed")

    def test_container_executor_records_malformed_peer_inspect(self) -> None:
        attempt = self.root / "malformed-wiremock"
        quality_run.prepare(self.write_manifest(), self.scenarios, attempt)
        peer = self.peer_record()
        peer[0]["NetworkSettings"]["Ports"] = ["unexpected"]

        def fake_run(command: list[str], **kwargs: object) -> object:
            record = (
                self.network_record()
                if command[3:5] == ["network", "inspect"]
                else peer
            )
            return types.SimpleNamespace(
                returncode=0, stdout=json.dumps(record), stderr=""
            )

        with mock.patch.object(
            container_executor.subprocess, "run", side_effect=fake_run
        ):
            with self.assertRaisesRegex(
                container_executor.ExecutorError, "peer isolation"
            ):
                container_executor.execute(
                    self.manifest,
                    self.scenarios,
                    attempt,
                    "hyhome-quality-12345678-a1",
                    "wiremock",
                    "/synthetic/docker",
                )
        exit_record = json.loads((attempt / "exit.json").read_text(encoding="utf-8"))
        self.assertEqual(exit_record["execution_state"], "interrupted")
        self.assertEqual(exit_record["error_class"], "isolation_preflight_failed")

    def test_zero_truncated_and_nan_summary_are_incomplete(self) -> None:
        for name, raw in (
            ("zero", canonical(self.summary(samples=0))),
            ("truncated", b'{"metrics":'),
            ("nan", b'{"metrics":{"iterations":{"values":{"count":NaN}}}}\n'),
            (
                "infinity",
                b'{"metrics":{"iterations":{"values":{"count":1e400}}}}\n',
            ),
        ):
            with self.subTest(name=name):
                attempt = self.root / name
                quality_run.prepare(self.write_manifest(), self.scenarios, attempt)
                (attempt / "raw-summary.json").write_bytes(raw)
                (attempt / "exit.json").write_bytes(
                    canonical(
                        {
                            "schema_version": "hyhome.quality-exit/v1",
                            "execution_state": "completed",
                            "exit_code": 0,
                            "started_at": "2026-10-03T00:00:00Z",
                            "ended_at": "2026-10-03T00:00:01Z",
                        }
                    )
                )
                final = quality_run.finalize(attempt)
                self.assertEqual(final["evidence_state"], "incomplete")
                self.assertEqual(final["verdict"], "incomplete")

    def test_summary_with_url_or_cookie_tags_is_not_imported(self) -> None:
        attempt = self.prepare()
        summary = self.summary()
        summary["metrics"]["custom{url:https://example.com?a=1}"] = {
            "type": "counter",
            "contains": "default",
            "values": {"count": 1},
        }
        self.write_execution(attempt, summary=summary)
        final = quality_run.finalize(attempt)
        self.assertEqual(final["verdict"], "incomplete")
        self.assertFalse(final["import_allowed"])
        with self.assertRaisesRegex(quality_run.ContractError, "quarantined"):
            quality_run.prepare_import(attempt, self.root / "sensitive.json")

    def test_interrupted_and_partial_run_never_pass(self) -> None:
        interrupted = self.prepare()
        self.write_execution(interrupted, execution_state="interrupted", exit_code=130)
        final = quality_run.finalize(interrupted)
        self.assertEqual(final["execution_state"], "interrupted")
        self.assertEqual(final["verdict"], "incomplete")

        partial = self.root / "partial"
        quality_run.prepare(self.write_manifest(), self.scenarios, partial)
        final = quality_run.finalize(partial)
        self.assertEqual(final["execution_state"], "interrupted")
        self.assertEqual(final["evidence_state"], "incomplete")
        envelope = quality_run.prepare_import(partial, self.root / "partial.json")
        result_import._validate(envelope)
        self.assertIsNone(envelope["started_at"])
        self.assertIsNone(envelope["ended_at"])

    def test_import_envelope_exact_replay_and_changed_artifact_conflict(self) -> None:
        attempt = self.prepare()
        self.write_execution(attempt)
        quality_run.finalize(attempt)
        output = self.root / "import.json"
        first = quality_run.prepare_import(attempt, output)
        second = quality_run.prepare_import(attempt, output)
        self.assertEqual(first, second)

        raw_summary = attempt / "raw-summary.json"
        raw_summary.chmod(0o640)
        raw_summary.write_bytes(canonical(self.summary(samples=3)))
        raw_summary.chmod(0o440)
        with self.assertRaisesRegex(quality_run.ContractError, "checksum mismatch"):
            quality_run.prepare_import(attempt, output)

    def test_checksum_index_is_bound_to_final_record(self) -> None:
        attempt = self.prepare()
        self.write_execution(attempt)
        quality_run.finalize(attempt)
        checksums_path = attempt / "checksums.json"
        checksums = json.loads(checksums_path.read_text(encoding="utf-8"))
        checksums_path.chmod(0o640)
        checksums["artifacts"][0]["bytes"] += 1
        checksums_path.write_bytes(canonical(checksums))
        checksums_path.chmod(0o440)
        with self.assertRaisesRegex(quality_run.ContractError, "final identity"):
            quality_run.prepare_import(attempt, self.root / "tampered.json")

    def test_database_outage_records_failure_without_changing_raw(self) -> None:
        attempt = self.prepare()
        self.write_execution(attempt)
        quality_run.finalize(attempt)
        raw_digest = hashlib.sha256(
            (attempt / "raw-summary.json").read_bytes()
        ).hexdigest()
        envelope_path = self.root / "import.json"
        envelope = quality_run.prepare_import(attempt, envelope_path)
        self.assertEqual(envelope["ingestion_state"], "pending")
        self.assertTrue(
            all(item["object_ref"] is None for item in envelope["artifacts"])
        )

        unavailable = self.root / "psql-unavailable"
        unavailable.write_text("#!/bin/sh\nexit 7\n", encoding="utf-8")
        unavailable.chmod(0o755)
        receipt, exit_code = result_import.import_db(
            envelope_path, self.root / "failed-receipt.json", str(unavailable)
        )
        self.assertEqual(exit_code, 7)
        self.assertEqual(receipt["ingestion_state"], "failed")
        self.assertEqual(receipt["error_class"], "database_import_failed")
        self.assertEqual(
            hashlib.sha256((attempt / "raw-summary.json").read_bytes()).hexdigest(),
            raw_digest,
        )

    def test_database_import_timeout_writes_failed_receipt(self) -> None:
        attempt = self.prepare()
        self.write_execution(attempt)
        quality_run.finalize(attempt)
        envelope_path = self.root / "import.json"
        quality_run.prepare_import(attempt, envelope_path)
        with mock.patch.object(
            result_import.subprocess,
            "run",
            side_effect=result_import.subprocess.TimeoutExpired("psql", 30),
        ) as run:
            receipt, exit_code = result_import.import_db(
                envelope_path, self.root / "timeout-receipt.json"
            )
        self.assertEqual(exit_code, 124)
        self.assertEqual(receipt["ingestion_state"], "failed")
        self.assertEqual(receipt["error_class"], "database_import_timeout")
        self.assertEqual(run.call_args.kwargs["timeout"], 30)
        self.assertEqual(run.call_args.kwargs["env"]["PGCONNECT_TIMEOUT"], "10")

    def test_database_import_uses_one_function_without_secret_args(self) -> None:
        attempt = self.prepare()
        self.write_execution(attempt)
        quality_run.finalize(attempt)
        envelope_path = self.root / "import.json"
        quality_run.prepare_import(attempt, envelope_path)
        fake_psql = self.root / "psql"
        fake_psql.write_text(
            "#!/usr/bin/env python3\n"
            "import os, sys\n"
            "statement = sys.stdin.read()\n"
            "assert statement.count('quality.import_payload') == 1\n"
            "assert statement.count('decode(') == 2\n"
            "assert all('password' not in item.lower() for item in sys.argv)\n"
            "assert 'API_TOKEN' not in os.environ\n"
            "assert 'PGPASSWORD' not in os.environ\n"
            "assert os.environ['PGPASSFILE'] == '/synthetic/pgpass'\n"
            "print('inserted')\n",
            encoding="utf-8",
        )
        fake_psql.chmod(0o755)
        with mock.patch.dict(
            "os.environ",
            {
                "API_TOKEN": "synthetic",
                "PGPASSWORD": "synthetic",
                "PGPASSFILE": "/synthetic/pgpass",
            },
        ):
            receipt, exit_code = result_import.import_db(
                envelope_path, self.root / "success-receipt.json", str(fake_psql)
            )
        self.assertEqual(exit_code, 0)
        self.assertEqual(receipt["ingestion_state"], "imported")
        self.assertEqual(receipt["database_result"], "inserted")

    def test_import_rejects_passed_verdict_with_incomplete_evidence(self) -> None:
        attempt = self.prepare()
        self.write_execution(attempt)
        quality_run.finalize(attempt)
        envelope = quality_run.prepare_import(attempt, self.root / "import.json")
        envelope["evidence_state"] = "incomplete"
        unsigned = dict(envelope)
        del unsigned["payload_sha256"]
        envelope["payload_sha256"] = hashlib.sha256(canonical(unsigned)).hexdigest()
        with self.assertRaisesRegex(
            result_import.ImportContractError, "verdict and evidence"
        ):
            result_import._validate(envelope)

    def test_root_compose_is_inventory_only(self) -> None:
        compose = (ROOT / "infra/11-quality/k6/docker-compose.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("command:\n      - version", compose)
        self.assertNotIn("command:\n      - run", compose)
        self.assertNotIn("host-gateway", compose)

    def test_cli_exposes_only_confined_load_execution(self) -> None:
        parser = quality_run._parser()
        command_action = next(
            action for action in parser._actions if action.dest == "command"
        )
        self.assertEqual(
            set(command_action.choices),
            {
                "prepare",
                "prepare-guard",
                "run",
                "finalize",
                "prepare-import",
                "import-db",
            },
        )


if __name__ == "__main__":
    unittest.main()
